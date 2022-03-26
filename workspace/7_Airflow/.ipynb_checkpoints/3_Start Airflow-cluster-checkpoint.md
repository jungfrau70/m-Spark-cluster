Prerequsites:
- deploy-server

#########################################################################################
# 1. (deploy-server) Preparation to start services
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark/'
cd $WORKDIR

docker-compose up -d

#########################################################################################
# 2. (deploy-server) Start hadoop/spark services
#########################################################################################

## Start cluster
~/start-hadoop-cluster.sh && \
~/start-spark-cluster.sh

~/start-hive-server2.sh && \
~/start-spark-history-server.sh

## Check cluster
~/check-cluster.sh

docker exec master /opt/hadoop/bin/hdfs dfs -ls /


#########################################################################################
# 3. Start Apache Airflow
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/7_Airflow/'
cd $WORKDIR

docker-compose up

#########################################################################################
# 4. Watch Services
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/7_Airflow/'
cd $WORKDIR

watch docker-compose ps

#########################################################################################
# 5. (deploy-server) Open Airflow WebUI
#########################################################################################

## Open web browser
http://localhost:8080

    - DAGs (shows dags from database)
    
## Crontab
http://crontab.guru

#########################################################################################
# 5. (if required) Scale-out Airflow-worker
#########################################################################################

docker-compose scale airflow-worker=3

#########################################################################################
# 6. (deploy-server, pipeline) Start jupyter lab
#########################################################################################

export WORKDIR='/root/PySpark/workspace/'
cd $WORKDIR

jupyter lab

#########################################################################################
# 9. (master) Start Jupyter lab
#########################################################################################

docker exec -it master /bin/bash

## Move to working direcotry
cd ~/workspace

## Read env
source /usr/local/spark/conf/spark-env.sh

## Start pyspark with jupyter
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

cd ~/workspace
pyspark --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

## Examples
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

pyspark --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

pyspark --packages org.postgresql:postgresql:42.3.3

