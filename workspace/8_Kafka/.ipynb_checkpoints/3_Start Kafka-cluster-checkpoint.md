#########################################################################################
# 1. Start kafka cluster with docker-compose
#########################################################################################

## Start services
docker-compose up -d

## Watch services
watch docker-compose ps

## (if required) Clean up
docker-compose rm -svf


#########################################################################################
# 2. Open kafka WebUI (=kafdrop)
#########################################################################################

## Forward a port in vscode
9000

## Open webbrowser
http://localhost:9000


#########################################################################################
# 3. Perform hands-on in Kafka cluster
#########################################################################################

## Create topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic 3rd-cluster-topic \
                                    --partitions 3 \
                                    --replication-factor 2

## Delete topic on WebUI

## Create topic on WebUI

## Go to IDE
jupyter lab

## Create producer and run
cluster_producer.ipynb

## Create consumer and run
cluster_consumer.ipynb


#########################################################################################
# 3. Stop kafka cluster
#########################################################################################

## Stop services
docker-compose down
