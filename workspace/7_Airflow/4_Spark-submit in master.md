
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

## Set ENV variables
cat >>~/.bashrc<<EOF
source /usr/local/spark/conf/spark-env.sh
EOF

## Exit
Ctrl + D

docker exec -it master /bin/bash

## Check if it works
which spark-submit
#/usr/local/spark/bin/spark-submit

which python3
#/usr/bin/python3


#########################################################################################
# 3. (master) Check if spark-submit works 
#########################################################################################

export WORKDIR='/root/workspace/7_Airflow/SparkSubmitOperator'
cd $WORKDIR

## Check if spark-submit works  ( 
        
Standalone : http://localhost:9090/ 
Yarn       : http://localhost:8088/


#########################################################################################
# 4. (deploy-server) Start MongoDB
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/A_Mongo'
cd $WORKDIR

docker-compose up -d

#########################################################################################
# 5. (master) Check if spark-submit works
#########################################################################################

## Set ENV variables
cat >>~/.bashrc<<EOF
source /opt/hadoop/etc/hadoop/hadoop-env.sh 
EOF

## WORKDIR
export WORKDIR='/root/workspace/7_Airflow/SparkSubmitOperator'
cd $WORKDIR

## standalone and client
spark-submit --master spark://master:7077 --deploy-mode client pi.py

## yarn and client
spark-submit --master yarn --deploy-mode client pi.py

## yarn and cluster
spark-submit --master yarn --deploy-mode cluster pi.py

## local
spark-submit --master local pi.py

#########################################################################################
# 5. (master) Check if spark-submit works with mongodb
#########################################################################################

export WORKDIR='/root/workspace/7_Airflow/SparkSubmitOperator'
cd $WORKDIR

spark-submit \
        --master yarn \
        --deploy-mode cluster \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 


spark-submit \
        --master yarn \
        --deploy-mode client \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

spark-submit \
        --master spark://master:7077 \
        --deploy-mode client \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

spark-submit \
        --master local[*] \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

#########################################################################################
# 6. (deploy-server) Restart yarn cluster
#########################################################################################

~/stop-hadoop-cluster.sh 
~/start-hadoop-cluster.sh

#########################################################################################
# 7. (deploy-server) Restart spark cluster
#########################################################################################

~/stop-spark-cluster.sh 
~/start-spark-cluster.sh