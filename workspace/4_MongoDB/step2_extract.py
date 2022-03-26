import pyspark
from pyspark.sql import SparkSession  
from pyspark.sql.types import *
from pyspark.sql.functions import *

### Configure spark session
spark = SparkSession\
   .builder\
   .master('spark://master:7077')\
   .appName('quake_etl')\
   .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
   .getOrCreate()

# Load the test data file into a dataframe
df_test = spark.read.csv('hdfs://master:9000/query.csv', header=True)

# Load the training data from mongo into a dataframe
df_train = spark.read.format('mongo')\
    .option('spark.mongodb.input.uri', 'mongodb://root:go2team@mongo:27017/Quake.quakes?authSource=admin').load()

# Select fields we will use and discard fields we don't need
df_test_clean = df_test['time', 'latitude', 'longitude', 'mag', 'depth']

# Rename fields
df_test_clean = df_test_clean.withColumnRenamed('time', 'Date')\
    .withColumnRenamed('latitude', 'Latitude')\
    .withColumnRenamed('longitude', 'Longitude')\
    .withColumnRenamed('mag', 'Magnitude')\
    .withColumnRenamed('depth', 'Depth')

# Cast some string fields into numeric fields
df_test_clean = df_test_clean.withColumn('Latitude', df_test_clean['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_test_clean['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_test_clean['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_test_clean['Magnitude'].cast(DoubleType()))

# Create training and testing dataframes
df_testing = df_test_clean['Latitude', 'Longitude', 'Magnitude', 'Depth']
df_training = df_train['Latitude', 'Longitude', 'Magnitude', 'Depth']

# Drop records with null values from our dataframes
df_testing = df_testing.dropna()
df_training = df_training.dropna()

spark.stop()
