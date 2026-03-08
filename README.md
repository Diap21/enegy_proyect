# ⚡ Pipeline ETL — Comercializadora de Energía

## Descripción

Una compañía comercializadora de energía compra electricidad a generadores en el mercado mayorista. Tras una serie de contratos y control de riesgos de precios, la energía se vende a usuarios finales: clientes residenciales, comerciales e industriales.

El sistema de la compañía exporta información de **proveedores**, **clientes** y **transacciones** en archivos CSV. Este proyecto implementa un pipeline ETL en AWS que ingesta, transforma y disponibiliza esos datos para análisis.

## Arquitectura

![Arquitectura del pipeline](.project-aws-glue-redshift/docs/arquitectura.png)

El flujo sigue un modelo de capas (raw → processed → final):

1. **Ingesta (CSV):** Los archivos CSV de proveedores, clientes y transacciones se cargan al bucket S3 de la **capa raw**.
2. **Función Lambda:** Se dispara automáticamente al detectar nuevos archivos en la capa raw. Realiza validaciones iniciales y mueve los datos a la **capa processed**.
3. **Capa Processed (S3):** Almacena los datos ya validados y listos para transformación.
4. **Catálogo de Datos (AWS Glue Crawler):** Cataloga los esquemas de los archivos en la capa processed, haciéndos consultables.
5. **Consultas (Amazon Athena):** Permite explorar los datos procesados mediante SQL directamente sobre S3.
6. **Glue Job:** Ejecuta las transformaciones de negocio y esquemas sobre los datos, generando la **capa final-data**.
7. **Visualización / Consumo:** Los datos finales quedan disponibles para dashboards, reportes o consumo por parte de otras aplicaciones.

## Tecnologías

| Servicio | Rol |
|---|---|
| Amazon S3 | Almacenamiento por capas (raw, processed, final-data) |
| AWS Lambda | Validación y movimiento automático de archivos |
| AWS Glue Crawler | Catalogación de esquemas |
| AWS Glue Job | Transformaciones ETL (PySpark) |
| Amazon Athena | Consultas SQL sobre S3 |

## Estructura del proyecto

```
.
├── lambda/
│   └── handler.py              # Función Lambda de validación e ingesta
├── glue/
│   └── etl_job.py              # Glue Job con transformaciones de negocio
├── data/
│   ├── proveedores.csv
│   ├── clientes.csv
│   └── transacciones.csv
├── arquitectura.png
└── README.md
```

## Cómo ejecutar

1. **Crear los buckets S3** con las capas: `raw/`, `processed/`, `final-data/`.
2. **Desplegar la función Lambda** desde `lambda/handler.py` y configurar el trigger de S3 sobre la capa `raw/`.
3. **Configurar el Glue Crawler** apuntando a la capa `processed/`.
4. **Crear el Glue Job** con el script `glue/etl_job.py`.
5. **Subir los archivos CSV** al bucket `raw/` para iniciar el pipeline.
6. **Consultar resultados** en Athena o desde la capa `final-data/`.

## Datos de entrada

| Archivo | Contenido |
|---|---|
| `proveedores.csv` | Generadores del mercado mayorista |
| `clientes.csv` | Usuarios finales (residencial, comercial, industrial) |
| `transacciones.csv` | Compras y ventas de energía |

## Autor

Diana — Data Engineer
