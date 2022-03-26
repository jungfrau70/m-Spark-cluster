Prerequsites:
- Hadoop cluster with yarn
- Hive with postgres metastore
- Spark cluster as standalone

#########################################################################################
# 1. (deploy-server) Start services
#########################################################################################

cd ~/PySpark
git clone https://github.com/jungfrau70/team2.git .
or
git pull origin master

## Instanticate the cluster containers
export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark/'
cd $WORKDIR

## Instanticate MongoDB
docker-compose -f mongo-docker-compose.yml down
rm -rf mongodb-data/
docker-compose -f mongo-docker-compose.yml up -d (--build)

## Container stats
docker stats

#########################################################################################
# 2. (deploy-server) Format Hadoop namenode
#########################################################################################

nodes='master worker1 worker2'
for node in $nodes
do
    docker exec $node rm -rf /home/hadoop/tmp/
done
docker exec master /opt/hadoop/bin/hdfs namenode -format


#########################################################################################
# 3. (deploy-server) Setup Hive metastore with PostgrSQL 9.2.24
     Now,Lets Set up Postgress Image in the Docker Container
#########################################################################################
docker exec \
    -it hive-postgres \
    psql -U postgres
	
### Createa database "metastore" for hive in postgress.
CREATE DATABASE metastore;
CREATE USER hive WITH ENCRYPTED PASSWORD 'go2team';
GRANT ALL ON DATABASE metastore TO hive;	

## Validate Metadata Tables
\l to list
\q to exit postgress


#########################################################################################
# 4. (deploy-server) Initialize Hive Metastore
#########################################################################################

docker exec -it master /opt/hive/bin/schematool -dbType postgres -initSchema

docker exec \
    -it hive-postgres \
    psql -U postgres \
    -d metastore
\d
\q
\q


#########################################################################################
# 5. (deploy-server) Create directories in hdfs 
#########################################################################################

## Start cluster
~/start-hadoop-cluster.sh && \
~/start-spark-cluster.sh && \
~/start-hive-server2.sh

## Copy spark-jars, and ... in Hadoop
docker cp configure-directories.sh master:/root/ &&
docker exec -it master /bin/bash /root/configure-directories.sh

## Check services
~/check-cluster.sh

#########################################################################################
# 6. (master) Start pysaprk with jupyter
#########################################################################################

docker exec -it master /bin/bash

## Move to working direcotry
cd ~/workspace

## Read env
source /usr/local/spark/conf/spark-env.sh

## Setup Jupyter
jupyter notebook --generate-config
jupyter notebook password

cat >/root/.jupyter/jupyter_notebook_config.py<<EOF
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True
EOF

## Start pyspark with jupyter

export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

## Must match with Spark version
pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

pyspark --conf "spark.mongodb.input.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --conf "spark.mongodb.output.uri=mongodb://root:go2team@mongo/Quake.quakes?authSource=admin" \
        --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

pyspark --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1

pyspark --packages org.postgresql:postgresql:42.3.3
                   org.postgresql:postgresql:42.3.3

~/start-spark-history-server.sh

q

docker exec \
    -it postgres \
    psql -U postgres