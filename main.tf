# Creación del SQL Warehouse Serverless optimizado para Tableau / BI
resource "databricks_sql_endpoint" "bi_warehouse" {
  name             = "Prod-Tableau-Warehouse"
  cluster_size     = "2X-Small"
  auto_stop_mins   = 20
  enable_serverless_compute = true
}

# Despliegue automatizado de un Notebook base de ETL en el Workspace
resource "databricks_notebook" "etl_base" {
  source = "${path.module}/notebooks/etl_usuarios.py"
  path   = "/Shared/Production/etl_usuarios"
  format = "SOURCE"
}\n