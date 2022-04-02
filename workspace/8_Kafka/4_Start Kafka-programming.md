
#########################################################################################
# 1. Start kafka-cluster
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/8_Kafka'
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
# 2. Preprea working environment
#########################################################################################

export WORKDIR='/root/PySpark/workspace/8_Kafka'
cd $WORKDIR

## Check conda environments
conda env list
# conda environments:
#
base                  *  /opt/conda
kafka                    /opt/conda/envs/kafka

## Activate virtual environment, kafka
conda activate kafka

## ping to kafka servers
ping kafka1
ping kafka2
ping kafka3

## (if required) copy the hosts file to deploy-server
cp config/hosts /etc/hosts

#########################################################################################
# 3. Install packages
#########################################################################################

pip --version
which python

pip install kafka-python

or 
pip install -r requirements.txt

#########################################################################################
# 4. Check if it works
#########################################################################################

(kafka) [root@deploy-server 8_Kafka]# python
Python 3.7.0 (default, Oct  9 2018, 10:31:47) 
[GCC 7.3.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import kafka
>>> kafka
<module 'kafka' from '/opt/conda/envs/kafka/lib/python3.7/site-packages/kafka/__init__.py'>


#########################################################################################
# 5. Create kafka producer
#########################################################################################

mkdir cluster  # cd cluster


