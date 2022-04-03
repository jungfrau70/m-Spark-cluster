Prerequsites:
- Started deploy-server

export WORKDIR='/root/PySpark/workspace/4_Airflow'
cd $WORKDIR


#########################################################################################
# 1. (deploy-server) Activate Virtual Environment
#########################################################################################

## virtual env - pipeline
conda activate pipeline


#########################################################################################
# 2. (deploy-server, pipeline) Start jupyter lab
#########################################################################################

jupyter lab
