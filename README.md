# Databricks GitOps Infrastructure Template

Este repositorio contiene el "Modern Data Stack Template" para automatizar la infraestructura de Databricks utilizando **Terraform** y pipelines de CI/CD con **GitHub Actions**.

## 🏗️ Arquitectura del Pipeline
1. **Pull Request a main:** Se dispara el workflow de GitHub Actions ejecutando un `terraform plan` de validación estática.
2. **Push/Merge a main:** El pipeline se pausa requiriendo aprobación manual mediante **GitHub Environments (production)**. Al ser aprobado, ejecuta un `terraform apply` que impacta la infraestructura de Databricks en la nube.

## 🛠️ Recursos Administrados
- **SQL Warehouse Serverless:** Configurado para la concurrencia de herramientas de BI como Tableau/Looker.
- **Production Notebooks:** Despliegue automatizado de scripts de PySpark hacia el workspace.\n