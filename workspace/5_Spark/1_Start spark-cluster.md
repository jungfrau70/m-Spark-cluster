#########################################################################################
# 1. (deploy-server) Preparation to start services
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark/'
cd $WORKDIR

## (If required) Instanticate the containers
rm -rf db.sql/ hive-postgres-data/ spark-apps/ spark-data

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
# 3. (deploy-server) Stop hadoop/spark services
#########################################################################################

## Stop hive and history servers
~/stop-hive-server2.sh && \
~/stop-spark-history-server.sh

## Stop cluster
~/stop-spark-cluster.sh && \
~/stop-hadoop-cluster.sh


#########################################################################################
# 4. (deploy-server) Preparation to start services
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark/'
cd $WORKDIR

docker-compose down