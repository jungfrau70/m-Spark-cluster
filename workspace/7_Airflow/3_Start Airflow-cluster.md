Prerequsites:
- deploy-server

#########################################################################################
# 1. Start Apache Airflow
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/7_Airflow/'
cd $WORKDIR

docker-compose up

#########################################################################################
# 2. Watch Services
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/7_Airflow/'
cd $WORKDIR

watch docker-compose ps

#########################################################################################
# 3. (deploy-server) Open Airflow WebUI
#########################################################################################

## Open web browser
http://localhost:8080

    - DAGs (shows dags from database)
    
## Crontab
http://crontab.guru

#########################################################################################
# 4. (if required) Scale-out Airflow-worker
#########################################################################################

docker-compose scale airflow-worker=3


