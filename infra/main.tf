provider "azurerm" {
  features {
  }
}

resource "azurerm_linux_function_app" "example" {
    name                = "itmgdemohttp"
    resource_group_name = azurerm_resource_group.example.name
    location            = azurerm_resource_group.example.location

  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
  service_plan_id            = azurerm_service_plan.example.id

  site_config {
    application_stack {
        python_version = "3.10"
    }
  }
  
}

resource "azurerm_resource_group" "example" {
    name     = "demofunctions"
    location = "West Europe"
}

resource "azurerm_service_plan" "example" {
    name                = "itmgdemohttp"
    location            = azurerm_resource_group.example.location
    resource_group_name = azurerm_resource_group.example.name
    os_type             = "Linux"
    sku_name            = "Y1"
}

resource "azurerm_storage_account" "example" {
    name                     = "itmgdemohttp"
    resource_group_name      = azurerm_resource_group.example.name
    location                 = azurerm_resource_group.example.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}