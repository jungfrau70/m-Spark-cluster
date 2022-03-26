# Kafka - 분산데이터스트리밍 플랫폼

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/A_Mongo'
cd $WORKDIR

#########################################################################################
# 1. Reset docker setting
#########################################################################################

docker-compose rm -svf

#########################################################################################
# 2. Start MongoDB with docker-compose
#########################################################################################

## Start services
docker-compose up -d


#########################################################################################
# 3. Stop MongoDB
#########################################################################################

## Stop services
docker-compose down

or 
containers=`docker ps -a | grep -e 'mongo' | awk '{print $1}'`
for container in $containers
do
    docker stop $container
    docker rm $container
done
