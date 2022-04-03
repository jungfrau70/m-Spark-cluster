
Prerequsites:
- deploy-server


#########################################################################################
# 1. (deploy-server) Check Environment
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark'
cd $WORKDIR

## Check if spark-submit/hdfs works, and then (if not installed) Install Spark
which spark-submit
which hdfs

## Set PATH ENV
cat >>~/.bashrc<<EOF
export PATH=/opt/conda/bin:/opt/conda/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/conda/bin:/opt/spark/bin:/opt/spark/sbin:/opt/hadoop/bin:/opt/hadoop/sbin:/opt/hive/bin:/usr/lib/jvm/java-11-openjdk-11.0.14.1.1-1.el7_9.x86_64/bin:/root/.vscode-server/bin/c722ca6c7eed3d7987c0d5c3df5c45f6b15e77d1/bin/remote-cli

source /opt/spark/conf/spark-env.sh
source /opt/hadoop/etc/hadoop/hadoop-env.sh
EOF

source ~/.bashrc

## (if not installed) Install Spark and Hadoop
bash config/install-spark.sh
bash config/install-hadoop.sh

## Copy their configs 
cp config/spark-env.sh /opt/spark/conf/
cp config/hadoop-env.sh /opt/hadoop/etc/hadoop/

## Check if spark-submit/hdfs works, and then (if not installed) Install Spark
which spark-submit
which hdfs


-------------------------------------------------------
export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"

pyspark --master local --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.3
