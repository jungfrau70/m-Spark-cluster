
import findspark

findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import math
import string
import random

import os
spark_version = '2.4.8'
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12-3.1.2,org.apache.kafka:kafka-clients-3.1.0.jar:{}'.format(spark_version)


print("PySpark Structured Streaming with Kafka Application Started …")

spark = SparkSession \
        .master(local) \
        .builder \
        .appName("PySpark Structured Streaming with Kafka") \
        .getOrCreate()

# Construct a streaming DataFrame that reads from testtopic
KAFKA_OUTPUT_TOPIC_NAME_CONS = "airflow-log"
KAFKA_BOOTSTRAP_SERVERS_CONS = ["kafka1:19091", "kafka2:19092", "kafka3:19093"]

lines = spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS) \
                .option("startingOffsets", "earliest") \
                .option("failOnDataLoss","False") \
                .option("subscribe", KAFKA_OUTPUT_TOPIC_NAME_CONS) \
                .load()

words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

print(type(words))
# print(type(stream_df))
    
# consolSink = stream_df \
#                 .writeStream \
#                 .queryName("kafka_spark_console")\
#                 .format("console") \
#                 .option("truncate", "false")\
#                 .start()

# 메모리에 저장
# memorySink = stream_df \
#               .writeStream \
#               .queryName("kafka_spark_memory")\
#               .format("console") \
#               .start()

# spark.sql("SELECT * FROM kafka_spark_memory").show()
