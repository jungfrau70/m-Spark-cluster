
Prerequsites:
- deploy-server
- hadoop/spark cluster
- mongodb

#########################################################################################
# 1. (deploy-server) Upload data in hadoop
#########################################################################################

export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

docker cp ../database.csv master:/root/
docker exec master /opt/hadoop/bin/hdfs dfs -put /root/database.csv /
docker exec master /opt/hadoop/bin/hdfs dfs -ls /


#########################################################################################
# 2. (deploy-server) Check if spark-submit works 
#########################################################################################

export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

## Check if spark-submit works  ( 
Livy        : http://localhost:8998/
Spark-master: http://localhost:8080/
spark-worker: http://localhost:8081/


#########################################################################################
# 3. (deploy-server) Check if spark-submit works
#########################################################################################

## WORKDIR
export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

## Add spark-livy in /etc/hosts
cat >>/etc/hosts<<EOF
172.18.0.22  spark-livy
EOF

## Check if name resolution works
ping spark-livy
PING spark-livy (172.18.0.22) 56(84) bytes of data.
64 bytes from spark-livy (172.18.0.22): icmp_seq=1 ttl=64 time=0.

## Create Spark Session
curl -X POST -d '{"kind": "pyspark"}' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/

{"id":1,"name":null,"appId":null,"owner":null,"proxyUser":null,"state":"starting","kind":"pyspark","appInfo":{"driverLogUrl":null,"sparkUiUrl":null},"log":["stdout: ","\nstderr: "]}


## Submit Spark Job
curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "for i in range(1,10):  print(i)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/0/statements


## Submit Spark Job
curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "spark.sparkContext.applicationId" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/0/statements
