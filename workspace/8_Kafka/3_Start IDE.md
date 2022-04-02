Prerequsites:
- Started deploy-server

#########################################################################################
# 1. (deploy-server) Activate Virtual Environment
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

## Start jupyter
jupyter lab

## vscode
(kafka) [root@deploy-server cluster]#
