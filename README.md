# Proyecto ETL de Criptomonedas con Airflow, PySpark y PostgreSQL

crypto-etl-pipeline es un pipeline ETL automatizado que extrae datos de criptomonedas desde la API de CoinGecko, los transforma con PySpark y los carga en PostgreSQL, todo orquestado con Apache Airflow.

## Estructura del Proyecto


```
crypto-etl-pipeline/
├── dags/
│   └── etl_dag.py
├── src/
│   ├── extract_api.py
│   ├── transform_spark.py
│   └── load_db.py
├── requirements.txt
└── README.md
```


## Tecnologías Usadas

- Ubuntu 20.04.6 LTS
- Python 3.8+
- Apache Airflow
- Apache Spark (PySpark)
- PostgreSQL
- CoinGecko API


## Ejecución del Proyecto

1. Clona el repositorio.
2. Crea y activa un entorno virtual.

Primero se debe tener el terminal de Ubuntu. Si el sistema operativo que maneja es Windows, se puede descargar directamente de Microsoft Store. Una vez abierto el terminal, dirigirse a la carpeta del repositorio clonado y ejecutar en el terminal:

python -m venv venv
source venv/bin/activate

3. Instala las dependencias
Para instalar las dependencias necesarias, el proyecto tiene un archivo llamado requirements.txt que contiene todo lo necesario. Para instalarlo se debe ejecutar en el terminal el siguiente comando:

pip install -r requirements.txt


4. Configura PostgreSQL
Asegúrate de que el servidor PostgreSQL esté corriendo y tener presente las credenciales de la base de datos. se debe modificar el archivo load_db.py los siguientes elementos

            dbname='Your_DataBase',
            user='Your_User',
            password='Your_password',
            host='Your_host',
            port='Your_port'

Se debe crear la tabla llamada "coins" para el almacenamiento de información. Para esto se debe ejecutar en la base de datos el siguiente script:

CREATE TABLE coins (
    id TEXT PRIMARY KEY,
    name TEXT,
    symbol TEXT,
    current_price DOUBLE PRECISION,
    market_cap DOUBLE PRECISION
);


Además de la creación de la tabla, se sugiere crear 2  indices para la búsqueda de nombre y el símbolo de la moneda como buenas practicas a la hora de consultar la tabla:

-- Índice por el nombre de la criptomoneda: 
```
CREATE INDEX idx_coins_name ON coins(name);
```

-- Índice por el símbolo de la criptomoneda: 
```
CREATE INDEX idx_coins_symbol ON coins(symbol);
```


5. Ejecuta Airflow
Se configura Airflow con sus credenciales de la siguiente manera:

```
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create \
  --username admin \
  --firstname Your_name \
  --lastname your_lastname \
  --role Admin \
  --email admin@example.com \
  --password your_password
```

Una vez configurado, se debe tener 2 terminales para ejecutar 2 procesos de Airflow, uno la parte grafica web y la otra la funcional. Para eso ambos terminales de Ubuntu deben estar en la carpeta proyecto e iniciar el entorno virtual. Una vez dentro se debe ejecutar en el primer terminal el siguiente comando:

```
airflow scheduler
```

Y en el segundo terminal el siguiente comando:

```
airflow webserver --port 9090
```

6. Accede a la interfaz de Airflow
Ve a: http://localhost:9090

```
Usuario: Your_user

Contraseña: your_password
```

Activa el DAG llamado etl_dag y ejecútalo manualmente o espera su ejecución automática diaria a las 12:00 PM (hora Colombia).

7. Visualización de los datos
Para ver el resultado del proyecto se puede generar una consulta sencilla en base de datos para ver el resultado

```
SELECT * FROM coins;
```
8. Ajuste de número de datos
El proyecto consulta la API con el archivo extract_api.py, agrupa los datos en paquetes de 20 con la variable per_page y por último toma el número de paquete 1 (los primeros 20 datos encontrados) con la variable page. Si se quiere codificar el número de datos que se quiere quiere consultar a la API o que numero de paquete consultara, modificar estos valores numéricos.

📈 Frecuencia de Ejecución
Este DAG se ejecuta diariamente a las 12:00 PM (hora Colombia). Si se desea cambiar la hora se debe ajustar en el archivo etl_dag.py en la variable schedule_interval (tener en cuenta la hora del servidor, ya que puede no coincidir con la hora local del usuario).

