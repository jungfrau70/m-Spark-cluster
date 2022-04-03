Prerequsites:
- Start Spark/Hadoop cluster
- Start Hive2 Server
- Start Spark History Server

#########################################################################################
# 1. (master) Test Spark cluster
#########################################################################################

docker exec -it master /bin/bash

### Move to working direcotry
cd ~/workspace

### Apply ENV variables
source /opt/spark/conf/spark-env.sh
source /opt/hadoop/etc/hadoop/hadoop-env.sh

### Only if hadoop cluster is running
pyspark --master yarn (default)
pyspark --master local

### Only if spark cluster is running
pyspark --master spark://master:7077
pyspark --master local

### Validate Spark using Python 
/opt/spark/bin/pyspark --master yarn

### After starting Hive2 server, ..
spark.sql('show databases').show()
spark.sql('create database test').show()
spark.sql('use test').show()
spark.sql('create table spark (col1 int)').show()
spark.sql('show tables').show()
spark.sql('insert into spark values(20)')
spark.sql('select * from spark').show() 
exit()

### Validate the custom table location
hdfs dfs -ls /apps/hive/warehouse

### Start pyspark with jupyter
set PYSPARK_DRIVER_PYTHON=jupyter
set PYSPARK_DRIVER_PYTHON_OPTS='notebook'

export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

pyspark

#########################################################################################
# 2. (master) Setup Jupyter server
#########################################################################################
#pip install jupyter_contrib_nbextensions

docker exec -it master /bin/bash
env

jupyter notebook --generate-config
jupyter notebook password

cat >/root/.jupyter/jupyter_notebook_config.py<<EOF
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True
EOF

#export PYSPARK_DRIVER_PYTHON=jupyter
#export PYSPARK_DRIVER_PYTHON_OPTS=notebook
#unset PYSPARK_DRIVER_PYTHON
#unset PYSPARK_DRIVER_PYTHON_OPTS

### Move to working direcotry
cd ~/workspace

pyspark


#########################################################################################
# 3. (deploy-server) Revise the docker images 
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark'
cd $WORKDIR

id='jungfrau70'
version=7

## Create Docker images
docker ps -a
docker commit master $id/ubuntu18.04:de-master.$version
docker commit worker1 $id/ubuntu18.04:de-worker1.$version
docker commit worker2 $id/ubuntu18.04:de-worker2.$version

## Push to repository
docker login

docker push $id/ubuntu18.04:de-master.$version
docker push $id/ubuntu18.04:de-worker1.$version
docker push $id/ubuntu18.04:de-worker2.$version

## Change in docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-master.*/$id\/ubuntu18.04:de-master.$version/g" docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-worker1.*/$id\/ubuntu18.04:de-worker1.$version/g" docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-worker2.*/$id\/ubuntu18.04:de-worker2.$version/g" docker-compose.yml
cat docker-compose.yml | grep -i jungfrau


#########################################################################################
# 4. Backup and restore in VMware Workstation Player
#########################################################################################

Copy folder and rename it

docker image 의 layer 를 보고 싶으면:
$ docker history [image-tag-name]
예: docker history python:3.6


## Start mysql
docker-compose -f mysql-docker-compose.yml up