# Kafka - 분산데이터스트리밍 플랫폼

#########################################################################################
# 1. Install Apache Kafka
#########################################################################################

export WORKDIR="/root/PySpark/Step3_setup_cluster/3_Kafka"
cd $WORKDIR

bash ./config/install-kafka.sh

#########################################################################################
# 2. Check the config settings
#########################################################################################

cd /opt/kafka

## zookeeper config with regular expression
cat config/zookeeper.properties | grep -v -e "^#" -e "^$" 

vi config/zookeeper.properties
:q!

## server(=broker) config with PATTERN
cat config/server.properties | grep -v '^$\|^#'

vi config/server.properties
:q!

## producer with PATTERN
cat config/producer.properties | grep -v '^$\|^#'

vi config/producer.properties
:q!

## consumer with PATTERN
cat config/consumer.properties | grep -v ^'$\|#'

vi config/consumer.properties
:q!

#########################################################################################
# 3. Start Apache Kafka
#########################################################################################

## Move the kafka home
cd /opt/kafka

## Start Zookeeper
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties

## Start Kafka broker ( depends on: Zookeeper )
bin/kafka-server-start.sh -daemon config/server.properties


#########################################################################################
# 4. Check Apache Kafka
#########################################################################################

## Install jdk in Centos 7
yum search java-1.8.0-openjdk
yum install java-1.8.0-openjdk
yum install java-1.8.0-openjdk-devel

## Install jdk in Ubuntu 20.04
apt install openjdk-8-jdk-headless

## jps
52913 Kafka
49555 QuorumPeerMain
53063 Jps  

## zookeeper:2181
netstat -an | grep 2181

## LISTEN
tcp6       0      0 :::2181                 :::*                    LISTEN   


#########################################################################################
# 5. Create New Topic
#########################################################################################

./bin/kafka-topics.sh

## broker:9092
./bin/kafka-topics.sh --create --topic first-topic --bootstrap-server localhost:9092  --partitions 3 --replication-factor 1


#########################################################################################
# 6. Get the list of Topic
#########################################################################################

./bin/kafka-topics.sh --list --bootstrap-server localhost:9092 


#########################################################################################
# 7. Get the specific topic info in detail
#########################################################################################

./bin/kafka-topics.sh --describe --bootstrap-server localhost:9092


#########################################################################################
# 8. Delete the specific topic
#########################################################################################

#./bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic first-topic


#########################################################################################
# 9. Get into Kafka console producer
#########################################################################################

./bin/kafka-console-producer.sh 
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic

## Sending message
>first message

## for Exit
^d

#########################################################################################
# A. Get into Kafka console consumer
#########################################################################################

./bin/kafka-console-consumer.sh
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic
>

## Check if messaging(producer,consumer) works
Producer> Hello
Consumer> ?

## list the consumer group that generated uniquely and automatically
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
...

## Open consumer console with consumer group option
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic --group first-group

## List the consumer group
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list  
...
first-group

## Describe the specific consumer group
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group first-group
...


#########################################################################################
# B. Hands-on with 1 partition
#########################################################################################

## in 1st pane
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic

## in 3rd pane
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic --group first-group

## in 4th pane
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic first-topic --group first-group

## list the consumer group that generated uniquely and automatically
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

## Describe the specific consumer group
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group first-group

## in 1st pane
Producer> Hello

## Check if all consumer get the message
   No, only one consumer get it.

Consumer> ?


## in 2nd pane
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic

## in 2nd pane
Producer> Hello from 2nd producer

## Check if all consumer get the message
   No, only one consumer get it.

Consumer> ?

## Result ##
Even though we send messing from multiple producers, only one consumer get the messages.
It is because first-topic has only one partition.

#########################################################################################
# C. Hands-on with 2 partitions
#########################################################################################

## Create new topic with 2 partitions
bin/kafka-topics.sh --create --topic second-topic --bootstrap-server localhost:9092  --partitions 2 --replication-factor 1


## in 1st pane
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic second-topic

## in 2nd pane
./bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic second-topic

## in 3rd pane
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic second-topic --group second-group --partitions 2

## in 4th pane
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic second-topic --group second-group

## list the consumer group that generated uniquely and automatically
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
...

## Describe the specific consumer group
./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group second-group


## Result ##
When we send messing from multiple producers, two partitions get the messages evenly (maybe round-robin).
It is because second-topic has 2 partitions.
It show workload balancing in distrubeted environment. The number of partitions are critical for distributed processing, workload balancing.

#########################################################################################
# D. Stop services
#########################################################################################

## Move the kafka home
cd /opt/kafka

## Stop Kafka broker ( depends on: Zookeeper )
bin/kafka-server-stop.sh

## Stop Zookeeper
bin/zookeeper-server-stop.sh

## Check if they went down
netstat -an | grep 2181
netstat -an | grep 9092

( No LISTEN port )

jps