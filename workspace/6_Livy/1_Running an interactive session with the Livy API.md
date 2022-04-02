
Prerequsites:
- deploy-server
- hadoop/spark cluster
- mongodb

References:
- https://docs.cloudera.com/cdp-private-cloud-base/7.1.6/running-spark-applications/topics/spark-interactive-session-livy-api.html?

#########################################################################################
# 1. (deploy-server) WebUI
#########################################################################################

## Check if spark-submit works  ( 
Livy        : http://localhost:8998/
Hadoop      : http://localhost:8088/


#########################################################################################
# 2. (deploy-server) Create an interactive session
#########################################################################################

curl -X POST -d '{"kind": "pyspark" }' \
  -H "Content-Type: application/json" \
  spark-livy:8998/sessions/

#########################################################################################
# 3. (deploy-server) Get the session info
#########################################################################################

curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions

{"from":0,"total":1,"sessions":[{"id":1,.....

export sessionId=1
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/logs
curl -X GET -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/${sessionId}/state


#########################################################################################
# 4. (deploy-server) Submit Spark jobs
#########################################################################################

export sessionId=1

curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "for i in range(1,10):  print(i)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements


curl -X POST -d '{ 
        "kind": "pyspark",
        "code": "print(spark)" 
        }' -H "Content-Type: application/json" spark-livy:8998/sessions/${sessionId}/statements


#########################################################################################
# 5. (deploy-server) Delete the spark session in Livy
#########################################################################################

curl -X DELETE -d '{"kind": "pyspark"}'   -H "Content-Type: application/json"   spark-livy:8998/sessions/0



