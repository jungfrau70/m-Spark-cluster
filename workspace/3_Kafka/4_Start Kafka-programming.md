
Prerequsites:
- Activated virtual environement, kafka

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

#########################################################################################
# 1. Create kafka consumer, and run
#########################################################################################

## in jupyter lab
cluster_consumer.ipynb

## in vscode
cd cluster
python cluster/cluster-consumer.py


#########################################################################################
# 2. Create kafka producer, and run
#########################################################################################

## in jupyter lab
cluster_producer.ipynb

## in vscode
clster/cluster-producer.py
python cluster/cluster-producer.py

