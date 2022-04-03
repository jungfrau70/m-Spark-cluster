References:
-. https://karthiksharma1227.medium.com/integrating-kafka-with-pyspark-845b065ab2e5

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

cp config/hosts /etc/hosts

ping kafka1

#########################################################################################
# 1. Start kafka-cluster
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/3_Kafka'
cd $WORKDIR

docker-compose up -d

watch docker-compose ps
Every 2.0s: docker-compose ps                                                                                   Fri Apr  1 13:47:56 2022

  Name                 Command               State                                   Ports
---------------------------------------------------------------------------------------------------------------------------
kafdrop     /kafdrop.sh                      Up      0.0.0.0:9000->9000/tcp,:::9000->9000/tcp
kafka1      /etc/confluent/docker/run        Up      0.0.0.0:9091->9091/tcp,:::9091->9091/tcp, 9092/tcp
kafka2      /etc/confluent/docker/run        Up      0.0.0.0:9092->9092/tcp,:::9092->9092/tcp
kafka3      /etc/confluent/docker/run        Up      9092/tcp, 0.0.0.0:9093->9093/tcp,:::9093->9093/tcp
zookeeper   /docker-entrypoint.sh zkSe ...   Up      0.0.0.0:2181->2181/tcp,:::2181->2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp


#########################################################################################
# 2. Open kafka WebUI (=kafdrop)
#########################################################################################

## Forward a port in vscode
9000

or 
Ctrl + Shift + P, type "Forward a port"

## Open webbrowser
http://localhost:9000


## Create topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic 3rd-cluster-topic \
                                    --partitions 3 \
                                    --replication-factor 2

## Delete topic on WebUI

## Create topic on WebUI



#########################################################################################
# 4. Stop kafka cluster
#########################################################################################

## Stop services
docker-compose down

## (if required) Clean up
#docker-compose rm -svf