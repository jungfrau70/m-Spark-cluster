
Prerequsites:
- deploy-server
- hadoop/spark cluster
- mongodb

References:
- https://shortn0tes.blogspot.com/2020/03/airflow-livy-spark.html?m=1
- 

#########################################################################################
# 1. (deploy-server) WebUI
#########################################################################################

## Check if spark-submit works  ( 
Livy        : http://localhost:8998/
Hadoop      : http://localhost:8088/


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
# 2. (deploy-server) Create an interactive session
#########################################################################################

curl -X POST \
        -d '{   "kind": "pyspark", 
                "name": "pyspark",
                "driverMemory": "1G",
                "driverCores": 1,
                "executorCores": 2,
                "executorMemory": "2G",
                "numExecutors": 2
        }' \
        -H "Content-Type: application/json" \
        spark-livy:8998/sessions/

curl -X POST -d '{"kind": "spark", "name": "spark" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/

curl -X POST -d '{"kind": "sparkr", "name": "sparkr" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/

curl -X POST -d '{"kind": "sql", "name": "sql" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/


#########################################################################################
# 3. (deploy-server) Get the session info
#########################################################################################

curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions | python3 -m json.tool

{"from":0,"total":1,"sessions":[{"id":1,.....

export sessionId=0
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId} | python3 -m json.tool
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/logs
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/state


#########################################################################################
# 4. (deploy-server) Submit Spark jobs
#########################################################################################

export sessionId=0
       
curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "for i in range(1,10):  print(i)"
        }' -H "Content-Type: application/json" \
        --url http://spark-livy:8998/sessions/${sessionId}/statements

curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "for i in range(1,10):  print(i)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements


curl -X POST -d '{ 
        "kind": "spark",
        "code": "spark.range(1000 * 1000 * 1000).count()" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements

export sessionId=3

curl -X POST -d '{ 
        "kind": "spark",
        "code": "spark.range(1000 * 1000 * 1000).count()" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements

export sessionId=4

curl -X POST -d '{ 
        "kind": "spark",
        "code": "df <- as.DataFrame(\nlist(\"One\", \"Two\", \"Three\", \"Four\"),\n\"Smth else\")\nhead(df)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements

export sessionId=5

curl -X POST -d '{ 
        "kind": "spark",
        "code": "SELECT 1" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements
        
#########################################################################################
# 5. (deploy-server) Delete the spark session in Livy
#########################################################################################

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/6

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/7

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/8

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/9

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/10

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/11

