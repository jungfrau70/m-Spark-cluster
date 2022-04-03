Prerequsites:
- Docker engine
- Hadoop cluster with yarn
- Hive with postgres metastore
- Spark cluster with standalone

References:
- book: https://www.manning.com/books/data-pipelines-with-apache-airflow
- github : https://github.com/BasPH/data-pipelines-with-apache-airflow
- https://maxcotec.com/2021/11/apache-airflow-architecture#What-you-will-Learn
- https://github.com/maxcotec/Apache-Airflow
- https://github.com/Anant/example-airflow-and-spark.git

docker stats

#########################################################################################
# 1. Start Apache Airflow
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_cluster/4_Airflow'
cd $WORKDIR

docker-compose up -d [--build]

## (if required) clean up 
docker-compose rm -svf

#########################################################################################
# 2. Watch Services
#########################################################################################

watch docker-compose ps

#########################################################################################
# 3. Scale-out Airflow-worker
#########################################################################################

docker-compose scale airflow-worker=3