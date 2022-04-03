export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

cp config/hosts /etc/hosts

#########################################################################################
# 1. Start Services
#########################################################################################

## Move the kafka home
cd /opt/kafka

## Start Zookeeper
bin/zookeeper-server-start.sh -daemon config/zookeeper.properties

## Start Kafka broker ( depends on: Zookeeper )
bin/kafka-server-start.sh -daemon config/server.properties


#########################################################################################
# 2. Check Apache Kafka
#########################################################################################

jps

52913 Kafka
49555 QuorumPeerMain
53063 Jps  

#########################################################################################
# 3. Stop Services
#########################################################################################

## Move the kafka home
cd /opt/kafka

## Stop Kafka broker ( depends on: Zookeeper )
bin/kafka-server-stop.sh 

## Stop Zookeeper
bin/zookeeper-server-stop.sh 

## Check
jps

58952 Jps
