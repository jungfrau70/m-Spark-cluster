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
# 2. (deploy-server) Start jupyter lab
#########################################################################################

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

jupyter lab
