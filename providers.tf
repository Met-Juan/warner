terraform {
  required_version = ">= 1.0.0"
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "databricks" {
  # Las credenciales se toman automáticamente de las variables de entorno:
  # DATABRICKS_HOST y DATABRICKS_TOKEN
}