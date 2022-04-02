
Prerequsites:
- deploy-server
- hadoop/spark cluster
- mongodb

References:
- https://docs.cloudera.com/cdp-private-cloud-base/7.1.6/running-spark-applications/topics/spark-interactive-session-livy-api.html?


#########################################################################################
# 1. (deploy-server) Upload data in hadoop
#########################################################################################

export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

docker cp ../database.csv master:/root/
docker exec master /opt/hadoop/bin/hdfs dfs -put /root/database.csv /
docker exec master /opt/hadoop/bin/hdfs dfs -ls /

docker cp ./pi.py master:/root/
docker exec master /opt/hadoop/bin/hdfs dfs -put /root/pi.py /
docker exec master /opt/hadoop/bin/hdfs dfs -ls /

#########################################################################################
# 2. (deploy-server) Check Environment
#########################################################################################

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark'
cd $WORKDIR

## Check if spark-submit/hdfs works, and then (if not installed) Install Spark
which spark-submit
which hdfs

## Set PATH ENV
cat >>~/.bashrc<<EOF
export PATH=/opt/conda/bin:/opt/conda/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/conda/bin:/opt/spark/bin:/opt/spark/sbin:/opt/hadoop/bin:/opt/hadoop/sbin:/opt/hive/bin:/usr/lib/jvm/java-11-openjdk-11.0.14.1.1-1.el7_9.x86_64/bin:/root/.vscode-server/bin/c722ca6c7eed3d7987c0d5c3df5c45f6b15e77d1/bin/remote-cli

source /opt/spark/conf/spark-env.sh
source /opt/hadoop/etc/hadoop/hadoop-env.sh
EOF

source ~/.bashrc

## (if not installed) Install Spark and Hadoop
bash config/install-spark.sh
bash config/install-hadoop.sh

## Copy their configs 
cp config/spark-env.sh /opt/spark/conf/
cp config/hadoop-env.sh /opt/hadoop/etc/hadoop/

#########################################################################################
# 3. (deploy-server) Submit a batch job using Livy
#########################################################################################

export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

conda env list

conda activate livy

jupyter lab

## Example - spark-submit
spark-submit \
--class org.apache.spark.examples.SparkPi \
--jars a.jar,b.jar \
--pyFiles a.py,b.py \
--files foo.txt,bar.txt \
--archives foo.zip,bar.tar \
--master yarn \
--deploy-mode cluster \
--driver-memory 10G \
--driver-cores 1 \
--executor-memory 20G \
--executor-cores 3 \
--num-executors 50 \
--queue default \
--name test \
--proxy-user foo \
--conf spark.jars.packages=xxx \
/path/to/examples.jar \
1000

## Example - spark-submit using Livy
curl -X POST -d '{ "pyFiles": ["hdfs://master:9000/pi.py"] }' \
        -H "Content-Type: application/json"   spark-livy:8998/batches
curl -X POST -d '{ "pyFiles": ["/root/PySpark/workspace/5_Spark/pi.py"] }' \
        -H "Content-Type: application/json"   spark-livy:8998/batches

## in python3 with requests, textwrap
data = {
  'code': textwrap.dedent("""
    import random
    NUM_SAMPLES = 100000
    def sample(p):
      x, y = random.random(), random.random()
      return 1 if x*x + y*y < 1 else 0

    count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
    print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)
    """)
}

r = requests.post(statements_url, data=json.dumps(data), headers=headers)
pprint.pprint(r.json())


curl -X POST -d '{ "file":"<path to application jar>", "className":"<classname in jar>" }'  -H "X-Requested-By: admin"

curl -X POST -d '{"kind": "pyspark" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/

curl -X POST -d '{ "kind": "pyspark", "pyFiles": "pi.py", "executorMemory": "2g" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/livy/batches/

curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions


curl -X POST -d '{ "className": "org.apache.spark.examples.SparkPi", "pyFiles": ["pi.py", "b.py"], }' \
        -H "Content-Type: application/json"   spark-livy:8998/livy/batches

## Livy REST JSON protocol
{
        "className": "org.apache.spark.examples.SparkPi",
        "jars": ["a.jar", "b.jar"],
        "pyFiles": ["a.py", "b.py"],
        "file": "hdfs://master:9000/pi.py",
        "files": ["foo.txt", "bar.txt"],
        "archives": ["foo.zip", "bar.tar"],
        "driverMemory": "1G",
        "driverCores": 1,
        "executorCores": 2,
        "executorMemory": "2G",
        "numExecutors": 2,
        "queue": "default",
        "name": "test",
        "proxyUser": "foo",
        "conf": {"spark.jars.packages": "xxx"},
        "file": "hdfs:///path/to/examples.jar",
        "args": [1000],
}

#########################################################################################
# 3. (deploy-server) Get the session info
#########################################################################################

curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions
export sessionId=2
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}

{"from":0,"total":1,"sessions":[{"id":1,.....

curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/livy/batches

export sessionId=1
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/logs
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/state


#########################################################################################
# 4. (deploy-server) Submit Spark jobs
#########################################################################################

export sessionId=2

curl -X POST -d '{ 
        "kind": "pyspark",
        "pyFiles": ["pi.py"],
        }' -H "Content-Type: application/json" spark-livy:8998/livy/batches


curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "print(spark)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements

#########################################################################################
# 5. (deploy-server) Delete the spark session in Livy
#########################################################################################

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/0



