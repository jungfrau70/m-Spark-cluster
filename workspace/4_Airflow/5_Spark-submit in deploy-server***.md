
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
# 2. (deploy-server) Start MongoDB
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/A_MongoDB'
cd $WORKDIR

docker-compose up -d

#########################################################################################
# 3. (deploy-server) Install hadoop
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark/'
cd $WORKDIR
bash config/install-hadoop.sh 
cp config/hadoop-env.sh /opt/hadoop/etc/hadoop/

#########################################################################################
# 3. (deploy-server) Set Spark ENV
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark/'
cd $WORKDIR

cp config/spark-env.sh /opt/spark/conf/
cp config/hadoop-env.sh /opt/hadoop/etc/hadoop/
## vi /opt/spark/conf/spark-env.sh

source /opt/spark/conf/spark-env.sh 
source /opt/hadoop/etc/hadoop/hadoop-env.sh

export PATH=/opt/spark/bin:/opt/spark/sbin:$PATH
which spark-submit


#########################################################################################
# 4. (deploy-server) Check if spark-submit works with mongodb
#########################################################################################

export WORKDIR='/root/PySpark/workspace/4_Airflow/SparkSubmitOperator'
cd $WORKDIR

spark-submit \
        --master yarn \
        --deploy-mode cluster \
        pi.py

spark-submit \
        --master yarn \
        --deploy-mode cluster \
        --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
        step1_preprocess.py 

#########################################################################################
# 5. (deploy-server) Check if spark-submit works 
#########################################################################################

export WORKDIR='/root/PySpark/workspace/4_Airflow/SparkSqlOperator'
cd $WORKDIR

source ../config/hadoop-env.sh 

spark-submit --master yarn --deploy-mode cluster pi.py

#########################################################################################
# 6. (deploy-server) Restart yarn cluster
#########################################################################################

~/stop-hadoop-cluster.sh &&
~/start-hadoop-cluster.sh