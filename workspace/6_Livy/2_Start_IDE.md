Prerequsites:
- Started deploy-server

export WORKDIR='/root/PySpark/workspace/7_Airflow'
cd $WORKDIR


#########################################################################################
# 1. (deploy-server) Activate Virtual Environment
#########################################################################################

## virtual env - livy
conda activate livy


#########################################################################################
# 2. (deploy-server, livy) Start jupyter lab
#########################################################################################

jupyter lab
