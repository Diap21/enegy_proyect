import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. Leer el archivo CSV desde S3
datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://result-finales/temp/glue-results/renewable_percentage_csv",
    "enewable_percentage",
    "part-00000-23d1b14a-99a4-4046-b01e-3ecf55b1b8a0-c000.csv"]
    },
    format="csv",
    format_options={
        "withHeader": True,
        "separator": ","
    }
)

# 2. Escribir los datos en Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=datasource0,
    catalog_connection="Redshift_Conn",
    connection_options={
        "dbtable": "renewable_percentage",           
        "database": "dev"       
    },
    redshift_tmp_dir="s3://result-finales/temp/glue-copy"
)

job.commit()
