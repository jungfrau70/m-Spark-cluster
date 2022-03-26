#!/usr/bin/env python

from __future__ import print_function

if __name__ == '__main__':

#     import findspark
#     findspark.init()

    import pyspark
    from pyspark.sql import SparkSession  
    from pyspark.sql.types import *
    from pyspark.sql.functions import *


    # In[4]:


    # Configure spark session
    spark = SparkSession    .builder    .master('local[2]')    .appName('quake_etl')    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1')    .getOrCreate()


    # In[5]:


    # Load the dataset 
    df_load = spark.read.csv(r"database.csv", header=True)
    # Preview df_load
    df_load.take(1)


    # In[6]:


    # Drop fields we don't need from df_load
    lst_dropped_columns = ['Depth Error', 'Time', 'Depth Seismic Stations','Magnitude Error','Magnitude Seismic Stations','Azimuthal Gap', 'Horizontal Distance','Horizontal Error',
        'Root Mean Square','Source','Location Source','Magnitude Source','Status']

    df_load = df_load.drop(*lst_dropped_columns)
    # Preview df_load
    df_load.show(5)


    # In[7]:


    # Create a year field and add it to the dataframe
    df_load = df_load.withColumn('Year', year(to_timestamp('Date', 'dd/MM/yyyy')))
    # Preview df_load
    df_load.show(5)


    # In[8]:


    # Build the quakes frequency dataframe using the year field and counts for each year
    df_quake_freq = df_load.groupBy('Year').count().withColumnRenamed('count', 'Counts')
    # Preview df_quake_freq
    df_quake_freq.show(5)


    # In[9]:


    # Preview df_load schema
    df_load.printSchema()


    # In[10]:


    # Cast some fields from string into numeric types
    df_load = df_load.withColumn('Latitude', df_load['Latitude'].cast(DoubleType()))    .withColumn('Longitude', df_load['Longitude'].cast(DoubleType()))    .withColumn('Depth', df_load['Depth'].cast(DoubleType()))    .withColumn('Magnitude', df_load['Magnitude'].cast(DoubleType()))

    # Preview df_load
    df_load.show(5)


    # In[11]:


    # Preview df_load schema
    df_load.printSchema()


    # In[12]:


    # Create avg magnitude and max magnitude fields and add to df_quake_freq
    df_max = df_load.groupBy('Year').max('Magnitude').withColumnRenamed('max(Magnitude)', 'Max_Magnitude')
    df_avg = df_load.groupBy('Year').avg('Magnitude').withColumnRenamed('avg(Magnitude)', 'Avg_Magnitude')


    # In[13]:


    # Join df_max, and df_avg to df_quake_freq
    df_quake_freq = df_quake_freq.join(df_avg, ['Year']).join(df_max, ['Year'])
    # Preview df_quake_freq
    df_quake_freq.show(5)


    # In[14]:


    # Remove nulls
    df_load.dropna()
    df_quake_freq.dropna()


    # In[15]:


    # Preview dataframes
    df_load.show(5)


    # In[16]:


    df_quake_freq.show(5)


    # In[17]:


    # Build the tables/collections in mongodb
    # Write df_load to mongodb
    df_load.write.format('mongo')    .mode('overwrite')    .option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Quake.quakes').save()


    # In[18]:


    # Write df_quake_freq to mongodb
    df_quake_freq.write.format('mongo')    .mode('overwrite')    .option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Quake.quake_freq').save()


    # In[19]:


    spark.stop()

