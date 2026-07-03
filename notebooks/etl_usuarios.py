# Databricks notebook source
# MAGIC %md
# MAGIC # Pipeline de Carga de Usuarios (Capa Silver/Gold)

# COMMAND ----------
# Código de simulación de carga y escritura en formato Delta
data = [("1", "Santi", "Buenos Aires"), ("2", "Elena", "Córdoba"), ("3", "Lucas", "Rosario")]
columns = ["id", "nombre", "ciudad"]

df = spark.createDataFrame(data, schema=columns)

# Guardamos en formato Delta en el catálogo analítico
df.write.format("delta").mode("overwrite").saveAsTable("default.usuarios_test")

print("Proceso ETL finalizado con éxito.")\n