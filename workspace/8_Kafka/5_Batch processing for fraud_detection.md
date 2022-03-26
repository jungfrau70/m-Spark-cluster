export WORKDIR='/root/PySpark/workspace/8_Kafka'
cd $WORKDIR

mkdir fraud_detection

#########################################################################################
# 1. Download NYC trip data
#########################################################################################




#########################################################################################
# 2. Create topic
#########################################################################################

## Create topic
#PAYMENT_TOPIC = "payments"
#FRAUD_TOPIC = "fraud_payments"
#LEGIT_TOPIC = "legit_payments"

docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic payments \
                                    --partitions 3 \
                                    --replication-factor 2
                                    
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic fraud_payments \
                                    --partitions 3 \
                                    --replication-factor 2
                                    
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic legit_payments \
                                    --partitions 3 \
                                    --replication-factor 2

or
in Kafka WebUI (=kafdrop)

## List topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --list

## Delete topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --delete \
                                    --topic legit_payments
                                    
#########################################################################################
# 3. Open IDE
#########################################################################################

## Open IDE
jupyter lab

## Create producer and run
trips_consumer.ipynb

## Create producer and run
trips_producer.ipynb
