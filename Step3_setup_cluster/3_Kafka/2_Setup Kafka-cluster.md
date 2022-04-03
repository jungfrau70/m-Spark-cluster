
References:
- https://towardsdatascience.com/connecting-the-dots-python-spark-and-kafka-19e6beba6404

# Kafka - 분산데이터스트리밍 플랫폼

export WORKDIR='/root/PySpark/Step3_setup_cluster/3_Kafka'
cd $WORKDIR

#########################################################################################
# 1. Reset docker setting
#########################################################################################

docker-compose rm -svf

or 
containers=`docker ps -a | grep -e 'kafka\|zoo' | awk '{print $1}'`
for container in $containers
do
    docker stop $container
    docker rm $container
done

#########################################################################################
# 2. Start kafka cluster with docker-compose
#########################################################################################

## Start services
docker-compose up -d

## Watch services
watch docker-compose ps

## Inspace container
docker inspect kafdrop


#########################################################################################
# 3. (deploy-server) Hands on in kafka custer
#########################################################################################

## Create New Topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic first-cluster-topic \
                                    --partitions 1 \
                                    --replication-factor 1


#########################################################################################
# 4. Stop kafka cluster
#########################################################################################

## Stop services
docker-compose down
