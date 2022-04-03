Prerequsites:
- Started hadoop/spark cluster
- Started Airflow

Reference:
- https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html


#########################################################################################
# 1. (deploy-server)  Start MongoDB
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/A_MongoDB'
cd $WORKDIR

docker-compose -f mongo-docker-compose.yml up -d
