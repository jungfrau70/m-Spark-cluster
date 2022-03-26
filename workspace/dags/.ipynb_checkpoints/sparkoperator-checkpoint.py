# %load ../dags/sparkoperator.py

from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator

default_args = {
    'start_date': datetime(2022, 1, 1)
}

with DAG(dag_id="spark-example",
         schedule_interval="@daily",
         default_args=default_args,
         tags=['spark'],
         catchup=False
        ) as dag:
    sql_job = SparkSqlOperator(sql="show databases", master='spark://master:7077', task_id="sql_job")
