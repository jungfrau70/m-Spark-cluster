

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

mkdir trips

#########################################################################################
# 1. Download NYC trip data
#########################################################################################

## NYC Taxi & Limousine Commission website
https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Download trip data
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv -O trips/yellow_tripdata_2021-01.csv


#########################################################################################
# 2. Create topic
#########################################################################################

## Create topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --create \
                                    --topic trips \
                                    --partitions 3 \
                                    --replication-factor 2
or
in Kafka WebUI (=kafdrop)

## Delete topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --delete \
                                    --topic trips

## List topic
docker exec -it kafka1 kafka-topics --bootstrap-server=kafka1:19091 \
                                    --list

#########################################################################################
# 3. Open IDE
#########################################################################################

## Open IDE
jupyter lab --allow-root

## Create producer and run
trips_consumer.ipynb

## Create producer and run
trips_producer.ipynb
