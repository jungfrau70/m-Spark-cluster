Prerequsites:
- Centos7

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark'
cd $WORKDIR

## (if required) clean the existing data
rm -rf db.sql/ hive-postgres-data/ spark-apps/ spark-data


## Instanticate the containers
docker-compose up -d

docker stats

#########################################################################################
# 1. (deploy-server) re-exchange ssh keys
#########################################################################################

bash reexchange-ssh-key.sh


#########################################################################################
# 2. (deploy-server) re-initialize hadoop and spark jars
#########################################################################################

bash reinitialize-hadoop.sh


#########################################################################################
# 3. (deploy-server) Build custom images and push them to docker registry
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/5_Spark'
cd $WORKDIR

export id='jungfrau70'
export version=9

bash rebuild-docker-images.sh


#########################################################################################
# 4. Setup Hive metastore with PostgrSQL 9.2.24
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
# 5. Initialize Hive
#########################################################################################
## Initialize Hive Metastore
docker exec -it master /opt/hive/bin/schematool -dbType postgres -initSchema

docker exec \
    -it hive-postgres \
    psql -U postgres \
    -d metastore
\d
\q
\q

#########################################################################################
# 6. (deploy-server) Start Cluster
#########################################################################################

## Start cluster
~/start-hadoop-cluster.sh && \
~/start-spark-cluster.sh

## Stop cluster
~/stop-spark-cluster.sh && \
~/stop-hadoop-cluster.sh

## Check cluster
~/check-cluster.sh
