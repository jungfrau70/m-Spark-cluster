import airflow
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from pyspark.sql import SparkSession, functions

def processo_etl_spark():
    spark = SparkSession \
        .builder \
        .appName("step1_preprocess") \
        .config("spark.jars.packages",
                "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,mysql:mysql-connector-java:8.0.28") \
        .config("spark.mongodb.input.uri", "mongodb://root:go2team@mongo:27017/Financeiro?authSource=admin") \
        .config("spark.mongodb.output.uri", "mongodb://root:go2team@mongo:27017/Financeiro?authSource=admin") \
        .config("spark.driver.maxResultSize", "8g") \
        .config("spark.network.timeout", 10000000) \
        .config("spark.executor.heartbeatInterval", 10000000) \
        .config("spark.storage.blockManagerSlaveTimeoutMs", 10000000) \
        .config("spark.executor.memory", "10g") \
        .master("spark://master:7077") \
        .getOrCreate()

    inicio = datetime.now()
    print(inicio)
    ###################################
    # Spark tasks
    ###################################
    termino = datetime.now()
    print(termino)
    print(termino - inicio)

default_args = {
    'owner': 'jih',
    'start_date': datetime(2020, 11, 18),
    'retries': 10,
    'retry_delay': timedelta(hours=1)
}
with airflow.DAG('step1_preprocess',
                  default_args=default_args,
                  schedule_interval='0 1 * * *') as dag:
    task_elt_documento_pagar = PythonOperator(
        task_id='step1_preprocess',
        python_callable=processo_etl_spark
    )
