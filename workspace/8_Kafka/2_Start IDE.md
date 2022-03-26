Prerequsites:
- Started deploy-server

export WORKDIR='/root/PySpark/workspace/8_Kafka'
cd $WORKDIR


#########################################################################################
# 1. (deploy-server) Activate Virtual Environment
#########################################################################################

## virtual env - kafka
conda activate kafka


#########################################################################################
# 2. (deploy-server, kafka) Start jupyter lab
#########################################################################################

jupyter lab