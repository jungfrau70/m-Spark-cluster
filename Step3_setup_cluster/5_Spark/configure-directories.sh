source /opt/hadoop/etc/hadoop/hadoop-env.sh
### create directories for logs and jars in HDFS. 
hdfs dfs -rm -r /spark-jars
hdfs dfs -rm -r /spark-logs

hdfs dfs -mkdir /spark-jars
hdfs dfs -mkdir /spark-logs
hdfs dfs -mkdir -p /apps/hive/warehouse

hdfs dfs -ls /spark-jars
hdfs dfs -ls /spark-logs
hdfs dfs -ls /apps/hive/warehouse

### Copy Spark jars to HDFS folder as part of spark.yarn.jars.
hdfs dfs -put /opt/spark/jars/* /spark-jars
hdfs dfs -put /opt/hive/lib/postgresql-42.2.24.jar /spark-jars

hdfs dfs -ls /spark-jars/postgresql-42.2.24.jar
