from pyspark.sql import SparkSession

spark = SparkSession \
        .builder \
        .master('local') \
        .appName('Python Spark SQL basic example') \
        .getOrCreate()
        
print("Spark Object is created ...")

print(spark.sparkContext.getConf().getAll())

# print("Number of partitions for shuffle changed to : " + str(spark.conf.get('spark.sql.shuffle.partitions')))

spark.stop()