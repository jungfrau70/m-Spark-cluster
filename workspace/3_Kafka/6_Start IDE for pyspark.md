Prerequsites:
- Started deploy-server

#########################################################################################
# 1. (deploy-server) Activate Virtual Environment
#########################################################################################

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

## Create kafka virtual environment
conda env create -f environment.yml

## Remove kafka virtual environment
conda env remove -n kafka

## Check conda environments
conda env list
# conda environments:
#
base                  *  /opt/conda
kafka                    /opt/conda/envs/kafka

## Activate virtual environment, kafka
conda activate kafka

#########################################################################################
# 2. (deploy-server) Start pyspark with jupyter lab
#########################################################################################

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'

pyspark --master local --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.1.3
