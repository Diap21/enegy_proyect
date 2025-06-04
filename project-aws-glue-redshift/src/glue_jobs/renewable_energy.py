import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer datos cargados
processed_df = spark.read.csv("s3://pe-processed-data/processed/", header=True)
com_aut_df = spark.read.csv("s3://pe-processed-data/dim_com_aut/", header=True)

# Renombrar la columna para evitar ambigüedad
com_aut_df = com_aut_df.withColumnRenamed("comunidad_autonoma", "com_aut")

# TRANSFORMACIÓN
porcentaje_renovable = (
    processed_df.join(com_aut_df, "id_comunidad")
    .groupBy("com_aut")
    .agg(
        F.round(
            F.sum(F.when(F.col("uso_energia_renovable") == "Si", 1).otherwise(0)) * 100.0 / F.count("*"),
            2
        ).alias("porcentaje_renovable")
    )
    .orderBy("com_aut")
)

# Escribir resultados como CSV
output_path = "s3://pe-final-data/temp/glue-results/renewable_percentage_csv"
porcentaje_renovable.coalesce(1).write.mode("overwrite").csv(
    output_path,
    header=True,
    sep=","
)