# %load 4_MongoDB/step1_preprocess.py
## Load Packages

import pyspark
from pyspark.sql import SparkSession  
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.conf import SparkConf

import os
system_name = os.getenv('HOSTNAME')
print(system_name)
            
### Configure spark session
spark = SparkSession\
   .builder\
   .master('spark://master:7077')\
   .appName('quake_etl')\
   .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
   .config('spark.driver.bindAddress', 'master')\
   .getOrCreate()

spark.sparkContext._conf.getAll()

# Load the dataset 
df_load = spark.read.csv('hdfs://master:9000/database.csv', header=True)

# Drop fields we don't need from df_load
lst_dropped_columns = ['Depth Error', 'Time', 'Depth Seismic Stations','Magnitude Error','Magnitude Seismic Stations','Azimuthal Gap', 'Horizontal Distance','Horizontal Error',
    'Root Mean Square','Source','Location Source','Magnitude Source','Status']
df_load = df_load.drop(*lst_dropped_columns)

# Create a year field and add it to the dataframe
df_load = df_load.withColumn('Year', year(to_timestamp('Date', 'dd/MM/yyyy')))

# Build the quakes frequency dataframe using the year field and counts for each year
df_quake_freq = df_load.groupBy('Year').count().withColumnRenamed('count', 'Counts')

# Cast some fields from string into numeric types
df_load = df_load.withColumn('Latitude', df_load['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_load['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_load['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_load['Magnitude'].cast(DoubleType()))

# Create avg magnitude and max magnitude fields and add to df_quake_freq
df_max = df_load.groupBy('Year').max('Magnitude').withColumnRenamed('max(Magnitude)', 'Max_Magnitude')
df_avg = df_load.groupBy('Year').avg('Magnitude').withColumnRenamed('avg(Magnitude)', 'Avg_Magnitude')

# Join df_max, and df_avg to df_quake_freq
df_quake_freq = df_quake_freq.join(df_avg, ['Year']).join(df_max, ['Year'])

# Remove nulls
df_load.dropna()
df_quake_freq.dropna()

# Build the tables/collections in mongodb
# Write df_load to mongodb
df_load.write.format('mongo')\
    .mode('overwrite')\
    .option('spark.mongodb.output.uri', 'mongodb://root:go2team@mongo:27017/Quake.quakes?authSource=admin').save()

# Write df_quake_freq to mongodb
df_quake_freq.write.format('mongo')\
    .mode('overwrite')\
    .option('spark.mongodb.output.uri', 'mongodb://root:go2team@mongo:27017/Quake.quake_freq?authSource=admin').save()

spark.stop()
