import boto3
import csv
import io
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info(f"Evento recibido: {event}")  # Debug 1: Verificar evento
    
    try:
        # Extraer bucket y key
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Procesando: {bucket_name}/{file_key}")  # Debug 2
        
        # Leer archivo
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Procesar CSV (ejemplo)
        reader = csv.reader(io.StringIO(csv_content))
        header = next(reader)
        processed_rows = [row for row in reader if all(row)]
        
        # Generar CSV en memoria
        output_csv = io.StringIO()
        writer = csv.writer(output_csv)
        writer.writerow(header)
        writer.writerows(processed_rows)
        
        # Particionado por fecha
        current_date = datetime.now()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")
        processed_key = f"processed/year={year}/month={month}/day={day}/{file_key.split('/')[-1]}"
        logger.info(f"Ruta destino: {processed_key}")  # Debug 3
        
        # Subir a S3
        s3.put_object(
            Bucket='pe-processed-data',
            Key=processed_key,
            Body=output_csv.getvalue().encode('utf-8')
        )
        logger.info("Archivo subido exitosamente")  # Debug 4
        
        return {'statusCode': 200}
        
    except Exception as e:
        logger.error(f"ERROR: {str(e)}")  # Debug 5
        raise