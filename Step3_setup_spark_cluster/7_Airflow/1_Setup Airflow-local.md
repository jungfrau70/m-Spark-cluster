Prerequsites:
- Started hadoop/spark cluster
- Created python virtual env with Airflow

Reference:
- https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html

export WORKDIR='/root/PySpark/workspace/'
cd $WORKDIR

#########################################################################################
# 1. (deploy-server) Activate Virtual Environment - pipeline
#########################################################################################

(base) conda-env list
(base) conda activate pipeline

#########################################################################################
# 2. (pipeline) Start Airflow
#########################################################################################

## Get helps
airflow -h

airflow webserver --port 8081

## (Option) Make the loading example enabled/desabled
sed -i "107s/True/False/" ~/airflow/airflow.cfg  # Disable
sed -i "107s/False/True/" ~/airflow/airflow.cfg  # Enable
sed -i "s/dags_folder =.*/dags_folder = .\/dags/g" ~/airflow/airflow.cfg  

## Initialize database
airflow db -h
airflow db init

#airflow db reset
#airflow db upgrade

## Create users
airflow users -h
airflow users list
airflow users create \
    --username admin \
    --firstname InHwan \
    --lastname Jung \
    --role Admin \
    --email smilepro@admin.org

## Start Scheduler
airflow scheduler -D

## Start Webserver, default port is 8080
airflow webserver --port 8081


#########################################################################################
# 3. (deploy-server) Airflow CLI hands-on
#########################################################################################

## Show Dags
(pipeline) airflow dags -h
(pipeline) airflow dags list

## Show tasks
(pipeline) airflow tasks -h
(pipeline) airflow tasks list example_xcom

## Trigger(run) tasks
(pipeline) airflow dags -h
(pipeline) airflow dags trigger -h
(pipeline) airflow dags trigger -e 2022-03-21 example_xcom


#########################################################################################
# 4. (deploy-server) Airflow WebUI hands-on
#########################################################################################

## Open web browser
http://localhost:8081

    - DAGs (shows dags from database)
    
## Crontab
http://crontab.guru
