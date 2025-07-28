from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import sys
import os


# Agrega la carpeta 'src' al path de Python
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
if src_path not in sys.path:
    sys.path.append(src_path)

# Importacion de los modulos
import extract_api
import transform_spark
import load_db

# Función de extracción
def extract(ti):
    data = extract_api.get_data()
    if data:
        ti.xcom_push(key='raw_data', value=data)
        print(f"Extracción exitosa. {len(data)} registros extraídos.")
    else:
        print("Error en la extracción o no hay datos.")

# Función de transformación
def transform(ti):
    raw_data = ti.xcom_pull(task_ids='extract_task', key='raw_data')
    if raw_data:
        df = transform_spark.transform_data(raw_data)
        data_dicts = df.toPandas().to_dict(orient='records')
        ti.xcom_push(key='transformed_data', value=data_dicts)
        print(f"Transformación exitosa. {len(data_dicts)} registros transformados.")
    else:
        print("No hay datos crudos para transformar.")

# Función de carga
def load(ti):
    transformed_data = ti.xcom_pull(task_ids='transform_task', key='transformed_data')
    if transformed_data:
        load_db.insert_data(transformed_data)
        print("Carga completada.")
    else:
        print("No hay datos transformados para cargar.")

# Configuración del DAG
default_args = {
    'start_date': datetime(2025, 1, 1),
    'retries': 1
}

with DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL de la Api CoinGecko a PostgreSQL',
    schedule_interval='0 17 * * *',
    catchup=False,
    tags=['prueba']
) as dag:

    t1 = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    t2 = PythonOperator(
        task_id='transform_task',
        python_callable=transform
    )

    t3 = PythonOperator(
        task_id='load_task',
        python_callable=load
    )

    # Flujo ETL
    t1 >> t2 >> t3
