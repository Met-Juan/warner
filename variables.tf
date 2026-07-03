# Definición de variables por si se requiere parametrizar el entorno en el futuro
variable "environment" {
  type        = string
  description = "Entorno de despliegue (dev, qa, prod)"
  default     = "prod"
}