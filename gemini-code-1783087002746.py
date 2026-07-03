import os

# Definimos la estructura del proyecto (Carpetas y Archivos)
# El diccionario tiene como clave la ruta del archivo y como valor su contenido base
estructura_proyecto = {
    # 1. CI/CD Pipeline - GitHub Actions
    ".github/workflows/databricks-deploy.yml": """name: 'Databricks IaC Deploy'

on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  terraform_plan:
    name: 'Terraform Plan'
    runs-on: ubuntu-latest
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan

  terraform_apply:
    name: 'Terraform Apply'
    runs-on: ubuntu-latest
    needs: terraform_plan
    if: github.event_name == 'push'
    environment: production  # Bloqueo de seguridad / Aprobación manual en GitHub
    env:
      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
      DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init

      - name: Terraform Apply
        run: terraform apply -auto-approve
""",

    # 2. Terraform - Providers
    "providers.tf": """terraform {
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
""",

    # 3. Terraform - Main (Recursos)
    "main.tf": """# Creación del SQL Warehouse Serverless optimizado para Tableau / BI
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
}
""",

    # 4. Terraform - Variables
    "variables.tf": """# Definición de variables por si se requiere parametrizar el entorno en el futuro
variable "environment" {
  type        = string
  description = "Entorno de despliegue (dev, qa, prod)"
  default     = "prod"
}
""",

    # 5. Script/Notebook de Python para Databricks
    "notebooks/etl_usuarios.py": """# Databricks notebook source
# MAGIC %md
# MAGIC # Pipeline de Carga de Usuarios (Capa Silver/Gold)

# COMMAND ----------
# Código de simulación de carga y escritura en formato Delta
data = [("1", "Santi", "Buenos Aires"), ("2", "Elena", "Córdoba"), ("3", "Lucas", "Rosario")]
columns = ["id", "nombre", "ciudad"]

df = spark.createDataFrame(data, schema=columns)

# Guardamos en formato Delta en el catálogo analítico
df.write.format("delta").mode("overwrite").saveAsTable("default.usuarios_test")

print("Proceso ETL finalizado con éxito.")
""",

    # 6. Archivo .gitignore para no subir basura de Terraform a GitHub
    ".gitignore": """# Archivos locales de Terraform
.terraform/*
*.tfstate
*.tfstate.backup
*.tfvars
*.tfvars.json

# Logs y configuración del sistema
.DS_Store
.idea/
.vscode/
*.log
""",

    # 7. README explicativo del repositorio (Suma mil puntos en el perfil)
    "README.md": """# Databricks GitOps Infrastructure Template

Este repositorio contiene el "Modern Data Stack Template" para automatizar la infraestructura de Databricks utilizando **Terraform** y pipelines de CI/CD con **GitHub Actions**.

## 🏗️ Arquitectura del Pipeline
1. **Pull Request a main:** Se dispara el workflow de GitHub Actions ejecutando un `terraform plan` de validación estática.
2. **Push/Merge a main:** El pipeline se pausa requiriendo aprobación manual mediante **GitHub Environments (production)**. Al ser aprobado, ejecuta un `terraform apply` que impacta la infraestructura de Databricks en la nube.

## 🛠️ Recursos Administrados
- **SQL Warehouse Serverless:** Configurado para la concurrencia de herramientas de BI como Tableau/Looker.
- **Production Notebooks:** Despliegue automatizado de scripts de PySpark hacia el workspace.
"""
}

def crear_estructura():
    print("🚀 Iniciando la creación del árbol de directorios para GitHub...")
    
    for ruta_archivo, contenido in estructura_proyecto.items():
        # Obtener el directorio base del archivo
        directorio = os.path.dirname(ruta_archivo)
        
        # Si el archivo está dentro de una carpeta, creamos la carpeta si no existe
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
            print(f"📁 Carpeta creada: {directorio}")
            
        # Crear y escribir el archivo
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido.strip() + "\\n")
        print(f"📄 Archivo creado: {ruta_archivo}")

    print("\\n✨ ¡Todo listo! Estructura generada a la perfección.")
    print("👉 Para subirlo a tu GitHub ejecutá estos comandos en tu terminal:")
    print("   1. git init")
    print("   2. git add .")
    print("   3. git commit -m 'Initial commit: Databricks IaC template'")

if __name__ == "__main__":
    crear_estructura()