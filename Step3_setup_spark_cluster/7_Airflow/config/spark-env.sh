#Java
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=${JAVA_HOME}/bin:${PATH}

#Python
export PYTHON_HOME=/opt/conda/envs/pipeline
export PATH=${PYTHON_HOME}/bin:${PATH}

#Spark
export SPARK_LOCAL_IP='127.0.0.1'
export SPARK_MASTER_HOST=master
export SPARK_WORKER_INSTANCES=1
export SPARK_EXECUTOR_CORES=1
export SPARK_EXECUTOR_MEMORY=4g
export SPARK_HOME=/opt/spark
export PYSPARK_PYTHON=python3

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hadoop/lib/native
export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}
