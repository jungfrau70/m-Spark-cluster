#!/bin/bash
for serviceName in 3_Kafka 4_Airflow 5_Spark 6_Livy A_MongoDB B_Postgres C_MySQL
do
	workdir=/root/PySpark/Step3_setup_cluster/${serviceName}
	echo ${workdir}
	cd ${workdir}
	docker-compose up -d
	sleep 10
	cd -
done
