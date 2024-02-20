import azure.functions as func
from solaredge_influxdb.solaredge import Equipment

import os
import logging
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta, timezone

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="setUser", methods=["POST"])
def setUser(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("Invalid JSON")
            return func.HttpResponse("Invalid JSON", status_code=400)
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )
    else:
        return func.HttpResponse(
            "Nothing could be saved as a name should be passed",
            status_code=400,
        )


@app.timer_trigger(
    schedule="0 */15 * * * *",
    arg_name="myTimer",
    run_on_startup=True,
    use_monitor=True,
)
def get_solar(myTimer: func.TimerRequest) -> None:
    sun = Sun(52.5, 5.6)
    current_time = datetime.now(timezone.utc)
    logging.debug(f"Current time: {current_time}")
    try:
        sunrise = sun.get_sunrise_time()
        sunset = sun.get_sunset_time()
        logging.debug(f"Sunrise: {sunrise}, Sunset: {sunset}")

    except SunTimeException:
        logging.error("Failed to retrieve sunrise/sunset times")
        raise Exception(
            "Application requires sunset and sunrise times to prevent unnecessary API calls"
        )
    if (
        sunrise - timedelta(minutes=30)
        < current_time
        < sunset + timedelta(minutes=30)
    ):
        api_key = os.getenv("API_KEY")
        EquipmentClient = Equipment(api_key)
        for inverter in EquipmentClient.inverters:
            tech_data = EquipmentClient.get_technical_data(
                inverter.serialNumber,
                myTimer.schedule - timedelta(minutes=15),
                myTimer.schedule,
            )
            if tech_data is None:
                logging.error("Failed to retrieve technical data")
                continue

    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function executed.")
