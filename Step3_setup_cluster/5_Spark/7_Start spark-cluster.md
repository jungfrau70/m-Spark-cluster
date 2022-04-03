Prerequsites:
- deploy-server

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

#bash reexchange-ssh-key.sh


#########################################################################################
# 2. (deploy-server) re-initialize hadoop and spark jars
#########################################################################################

bash reinitialize-hadoop.sh


#########################################################################################
# 3. (deploy-server) Build custom images and push them to docker registry
#########################################################################################

id='jungfrau70'
version=9

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
#####
~/start-spark-history-server.sh &&
~/start-hive-server2.sh

## Stop cluster
~/stop-spark-cluster.sh && \
~/stop-hadoop-cluster.sh
#####
~/stop-spark-history-server.sh &&
~/stop-hive-server2.sh

## Check cluster
~/check-cluster.sh
