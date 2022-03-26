
Prerequsites:
- deploy-server
- hadoop/spark cluster

#########################################################################################
# 1. (deploy-server) Upload data in hadoop
#########################################################################################

export WORKDIR='/root/PySpark/workspace'
cd $WORKDIR

docker cp 4_MongoDB/database.csv master:/root/
docker exec master /opt/hadoop/bin/hdfs dfs -put /root/database.csv /
docker exec master /opt/hadoop/bin/hdfs dfs -ls /

#########################################################################################
# 2. (master) check if the environment sets properly
#########################################################################################

docker exec -it master /bin/bash

which spark-submit
#/usr/local/spark/bin/spark-submit

which python3
#/usr/bin/python3


#########################################################################################
# 3. (master) Check if spark-submit works 
#########################################################################################

export WORKDIR='/root/workspace/7_Airflow'
cd $WORKDIR

## Check if spark-submit works  ( http://localhost:9090/ )

cd BashOperator

cd PythonOperator

cd SparkSqlOperator
spark-submit pi.py

#########################################################################################
# 4. (deploy-server) Start MongoDB
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/A_Mongo'
cd $WORKDIR

docker-compose up -d

#########################################################################################
# 5. (master) Check if spark-submit works with mongodb
#########################################################################################

export WORKDIR='/root/workspace/7_Airflow/SparkSubmitOperator'
cd $WORKDIR

spark-submit \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

#########################################################################################
# 5. (deploy-server) Check if spark-submit works with mongodb
#########################################################################################

export WORKDIR='/root/PySpark/workspace/7_Airflow/SparkSubmitOperator'
cd $WORKDIR

spark-submit \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

#########################################################################################
# 6. (deploy-server) Restart cluster
#########################################################################################
~/stop-spark-cluster.sh && \
~/stop-hadoop-cluster.sh && \
~/start-hadoop-cluster.sh && \
~/start-spark-cluster.sh 