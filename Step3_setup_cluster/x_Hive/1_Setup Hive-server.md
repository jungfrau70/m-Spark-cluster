Prerequsites:
- Centos7
- Docker engine & Docker-compose
- Ansible
- Hadoop (with yarn)

Reference:
- 

#########################################################################################
# 1. ENVIRONMENT
#########################################################################################

cat >setup-cluster-envs.sh<<EOFEOF
## Set IPs 
cat >/etc/hosts<<EOF
127.0.0.1   localhost

172.18.0.11  hive-postgres

172.18.0.21  master
172.18.0.31  worker1
172.18.0.32  worker2
172.18.0.33  worker3
172.18.0.34  worker4
EOF

## Set ansible hosts
cat >/etc/ansible/hosts<<EOF
[cluster]
master ansible_host=172.18.0.21 ansible_user=root
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root
worker3 ansible_host=172.18.0.33 ansible_user=root
worker4 ansible_host=172.18.0.34 ansible_user=root

[master]
master ansible_host=172.18.0.21 ansible_user=root

[worker]
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root
worker3 ansible_host=172.18.0.33 ansible_user=root
worker4 ansible_host=172.18.0.34 ansible_user=root

EOF

cat /etc/hosts
cat /etc/ansible/hosts

## Set hostname
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker exec -it $node /usr/bin/hostnamectl set-hostname $node
done

EOFEOF

chmod u+x setup-cluster-envs.sh
./setup-cluster-envs.sh


## Check the docker image
# (if not exits) git clone https://github.com/jungfrau70/team2.git PySpark

export WORKDIR='/root/PySpark/Step3_setup_cluster/x_Hive'
cd $WORKDIR

cat >cluster.env<<EOF
#Java
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64
export PATH=${JAVA_HOME}/bin:${PATH}

#Hadoop
export HADOOP_HOME=/opt/hadoop
export YARN_CONF_DIR=/opt/hadoop/etc/hadoop
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

#Hive
export HIVE_HOME=/opt/hive

#Spark
export SPARK_HOME=/opt/spark3
export SPARK_MASTER=spark://master:7077
export SPARK_WORKER_CORES=1
export SPARK_WORKER_MEMORY=1G
export SPARK_DRIVER_MEMORY=1G
export SPARK_EXECUTOR_MEMORY=1G
export SPARK_WORKLOAD=worker
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hadoop/lib/native

#export PATH=/opt/hadoop/bin:/opt/hadoop/sbin:${PATH}
#export PATH=${PATH}:${HIVE_HOME}/bin
#export PATH=${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:

EOF

## (if required) clean up containers
docker ps -a
docker-compose -f spark-docker-compose.yml down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

## Instanticate the containers
docker-compose up -d
docker exec -it master /bin/bash

cat >>~/.bashrc<<EOF
#Java
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64
export PATH=${JAVA_HOME}/bin:${PATH}

#Hadoop
export HADOOP_HOME=/opt/hadoop
export YARN_CONF_DIR=/opt/hadoop/etc/hadoop
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root

#Hive
export HIVE_HOME=/opt/hive

#Spark
export SPARK_HOME=/opt/spark3
export SPARK_MASTER=spark://master:7077
export SPARK_WORKER_CORES=1
export SPARK_WORKER_MEMORY=1G
export SPARK_DRIVER_MEMORY=1G
export SPARK_EXECUTOR_MEMORY=1G
export SPARK_WORKLOAD=worker
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hadoop/lib/native

#export PATH=/opt/hadoop/bin:/opt/hadoop/sbin:${PATH}
#export PATH=${PATH}:${HIVE_HOME}/bin
#export PATH=${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:

EOF

scp ~/.barhrc worker1:$pwd
scp ~/.barhrc worker2:$pwd
scp ~/.barhrc worker3:$pwd
scp ~/.barhrc worker4:$pwd

#########################################################################################
# 2. HOSTNAME (from deploy-server)
#########################################################################################

### Check hostname
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker exec -it $node /usr/bin/hostname
done

#########################################################################################
# 3. Start Hadoop cluster
#########################################################################################

## (if required) Remove data in hadoop-cluster
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker exec $node /usr/bin/rm -rf /home/hadoop/tmp/
done
docker exec master /opt/hadoop/bin/hdfs namenode -format


## Stop hadoop-custer
cat >stop-hadoop-cluster.sh<<EOF
docker exec master /opt/hadoop/sbin/stop-all.sh

nodes='master worker1 worker2 worker3 worker4'
for node in \$nodes
do
    sleep 3
    echo \$node
    docker exec \$node jps
done
EOF

chmod u+x stop-hadoop-cluster.sh 
./stop-hadoop-cluster.sh


## Start hadoop-custer
cat >start-hadoop-cluster.sh<<EOF
docker exec master /opt/hadoop/sbin/start-all.sh

nodes='master worker1 worker2 worker3 worker4'
for node in \$nodes
do 
    sleep 3
    echo \$node
    docker exec \$node jps
    echo 
done
EOF

chmod u+x ./start-hadoop-cluster.sh 
./start-hadoop-cluster.sh 


#########################################################################################
# 4. Setup PostgrSQL 9.2.24
     Now,Lets Set up Postgress Image in the Docker Container
#########################################################################################

## Download Docker Image
docker pull postgres:9.6.24

## Create the Container of type Postgress Image.
docker create \
    --name hive-postgres \
    -p 6432:5432 \
    --env-file=postgres.env \
    --network netgroup \
    --ip 172.18.0.11 \
    postgres:9.6.24

## List Containers
docker ps -a

## Remove Containers
docker rm [container-id]
	
## Start the Container. 
docker start hive-postgres

### Check if the container is running.
docker logs -f hive-postgres

hit Control+c To come out.

### Convert docker to docker-compose, and start up
docker-compose -f postgres-docker-compose.yml up

### We can validate if we are able to run postgress from docker.

docker exec \
    -it hive-postgres \
    psql -U postgres
	
### Createa database "metastore" for hive in postgress.
CREATE DATABASE metastore;
CREATE USER hive WITH ENCRYPTED PASSWORD 'go2team';
GRANT ALL ON DATABASE metastore TO hive;	

\l to list
\q to exit postgress	

### If you want to access postgress from hadoop-master, we have to install a postgress client.
docker exec -it master /bin/bash
ps -a
yum install postgresql-server postgresql-contrib

psql -h hive-postgres \
    -p 5432 \
    -d metastore \
    -U hive \
    -W 

\d to list tables.
\q to exit

#########################################################################################
# 3. Setup Hive
     Now,Lets Set up Postgress Image in the Docker Container
#########################################################################################

### Download Hive.
cd /opt
wget https://mirrors.ocf.berkeley.edu/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz

### Untar Hive File.
tar xzf apache-hive-3.1.2-bin.tar.gz

### Archive Hive tar file.
rm -rf apache-hive-3.1.2-bin.tar.gz

### Create a soft link.
ln -s /opt/apache-hive-3.1.2-bin /opt/hive

### add HIVE_HOME in ENV ( hadoop.env )
export HIVE_HOME=/opt/hive
export PATH=$PATH:${HIVE_HOME}/bin

#########################################################################################
# 4. Configure Hive
#########################################################################################


###hive-site.xml : Global Configuration File for Hive

cat >/opt/hive/conf/hive-site.xml<<EOF
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:postgresql://hive-postgres:5432/metastore</value>
    <description>JDBC Driver Connection for PostgrSQL</description>
  </property>
 
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>org.postgresql.Driver</value>
    <description>PostgreSQL metastore driver class name</description>
  </property>
 
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
    <description>Database User Name</description>
  </property>
 
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>go2team</value>
    <description>Database User Password</description>
  </property>
</configuration>
EOF
 
### Remove the conflicting Guava Files if present.
rm -rf /opt/hive/lib/guava-19.0.jar
cp /opt/hadoop/share/hadoop/hdfs/lib/guava-27.0-jre.jar /opt/hive/lib/

### Download a postgresql jar file and copy it to /opt/hive/lib/
wget https://jdbc.postgresql.org/download/postgresql-42.2.24.jar
mv postgresql-42.2.24.jar /opt/hive/lib/postgresql-42.2.24.jar


#########################################################################################
# 5. Distribute to Hadoop-master
#########################################################################################

## distribue the custom hadoop to hadoop-master
cd /opt
tar -cf hive-dis.tar hive apache-hive-3.1.2-bin
docker cp hive-dis.tar master:/opt/
docker exec master /usr/bin/tar -xf /opt/hive-dis.tar -C /opt
docker exec master /usr/bin/rm -rf /opt/hive-dis.tar


#########################################################################################
# 5. Initialize Hive
#########################################################################################
## Initialize Hive Metastore
docker exec -it master /bin/bash

schematool -dbType postgres -initSchema

### if not found:
export HIVE_HOME=/opt/hive
export PATH=$PATH:${HIVE_HOME}/bin

## Validate Metadata Tables (from hadoop-master)
psql -h hive-postgres \
    -p 5432 \
    -d metastore \
    -U hive \

\d
\q

### Validate Metadata Tables from deploy-server
docker exec \
    -it hive-postgres \
    psql -U postgres \
    -d metastore
	
#########################################################################################
# 5. Re-configure hadoop-Cluster
     Check if hadoop-cluster is running
     If not, start haddop-cluster
#########################################################################################

## Re-configure hadoop-Cluster

vi /opt/hadoop/etc/hadoop/mapred-site.xml

cd /opt/hadoop/etc/hadoop/
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do 
    docker cp mapred-site.xml $node:`pwd`
done
cd ~

## Check changes
cd /opt/hadoop/etc/hadoop/
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker exec $node cat `pwd`/mapred-site.xml
done
cd ~

cat >stop-hadoop-cluster.sh<<EOF
## Stop hadoop-custer
docker exec master /opt/hadoop/sbin/stop-all.sh

nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do 
    docker exec $node jps
done
EOF

chmod u+x stop-hadoop-cluster.sh
./stop-hadoop-cluster.sh

## (if required) Remove data in hadoop-cluster
nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker exec $node /usr/bin/rm -rf /home/hadoop/tmp/
done
docker exec master /opt/hadoop/bin/hdfs namenode -format


cat >start-hadoop-cluster.sh<<EOF
## Start hadoop-custer
docker exec master /opt/hadoop/sbin/start-all.sh

nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do 
    sleep 3
    echo $node
    docker exec $node jps
    echo 
done
EOF

chmod u+x start-hadoop-cluster.sh
./start-hadoop-cluster.sh

#########################################################################################
# 5. Test Hive
     Check if hadoop-cluster is running
     If not, start haddop-cluster
#########################################################################################

## Start hive-client
docker exec -it master /bin/bash

export HIVE_HOME=/opt/hive
export PATH=$PATH:${HIVE_HOME}/bin
hive

hive> 
CREATE DATABASE TEST;
CREATE TABLE SPARK(COL1 int);
INSERT INTO SPARK VALUES(10);
select count(*) from spark;

#########################################################################################
# 8. Clean up (in deploy-server)
#########################################################################################

## Stop hadoop-cluster
docker exec master /opt/hadoop/sbin/stop-all.sh

## Remove all data
docker ps -a
docker-compose -f hadoop-docker-compose.yml down
docker-compose -f postgres-docker-compose.yml down

<!-- rm -rf /root/PySpark/Step4_spark/4_Hive/db.sql
rm -rf /root/PySpark/Step4_spark/4_Hive/db.sql -->

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

<!-- cat >/etc/hosts<<EOF
127.0.0.1   localhost
EOF

cat >/etc/ansible/hosts<<EOF
EOF -->

#########################################################################################
# 9. Backup and restore in VMware Workstation Player
#########################################################################################

Copy folder and rename it