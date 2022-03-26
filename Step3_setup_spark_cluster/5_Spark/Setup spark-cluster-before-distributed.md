Prerequsites:
- Centos7
- Docker engine
- SSH server in deploy-server
- Ansible in deploy-server
- Hadoop cluster with yarn
- Hive Server (with postgres metastore)

Reference:
- https://www.docker.com/blog/how-to-deploy-on-remote-docker-hosts-with-docker-compose/
- https://velog.io/@somnode/hadoop-cluster-install
- https://velog.io/@somnode/spark-cluster-install

export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/5_Spark/'

#########################################################################################
# 1. (deploy-server) Download Hadoop 
#########################################################################################

cd $WORKDIR

cat >download-hadoop-cluster.sh<<EOF
#!/bin/bash
cd /opt
rm -rf hadoop*
yum install -y wget
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz --no-check-certificate
tar -xzf hadoop-3.2.2.tar.gz
ln -s hadoop-3.2.2 hadoop
rm -rf hadoop-3.2.2.tar.gz

EOF

chmod u+x ./download-hadoop-cluster.sh 
./download-hadoop-cluster.sh 


#########################################################################################
# 2. (deploy-server) Download Hive
#########################################################################################

cd $WORKDIR

cat >download-hive.sh<<EOF
#!/bin/bash
### Download Hive.
cd /opt
wget https://mirrors.ocf.berkeley.edu/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz

### Untar Hive File.
tar xzf apache-hive-3.1.2-bin.tar.gz

### Archive Hive tar file.
rm -rf apache-hive-3.1.2-bin.tar.gz

### Create a soft link.
ln -s /opt/apache-hive-3.1.2-bin /opt/hive


EOF

chmod u+x ./download-hive.sh 
./download-hive.sh 


#########################################################################################
# 3. (deploy-server) Download Spark cluster
#########################################################################################

cd $WORKDIR

## Install Python3
cat >install-python3.yaml<<EOF
---
- hosts: cluster
  tasks:
    - name: Install python3 package
      become: true
      yum:
        name:
          - python3
        state: latest
    - name: Remove file
      ansible.builtin.file:
        state: absent
        path: /usr/bin/python
    - name: Create a symbolic link
      ansible.builtin.file:
        src: /usr/bin/python3.6
        dest: /usr/bin/python
        owner: root
        group: root
        state: link
EOF

ansible-playbook install-python3.yaml


## Install Miniconda

cat >install-conda.yaml<<EOF
---
- hosts: cluster
  tasks:
    - name: Install Conda
      block:
        - name: Download Miniconda
          get_url:
            url: https://repo.anaconda.com/miniconda/Miniconda3-py39_4.11.0-Linux-x86_64.sh
            dest: /tmp/Miniconda3-py39_4.11.0-Linux-x86_64.sh
            # checksum: md5:a946ea1d0c4a642ddf0c3a26a18bb16d
            mode: 0550
        - name: Create conda folder
          become: True
          file:
            path: /opt/miniconda3
            state: directory
            # owner: root
            mode: 755
            recurse: yes
        - name: Run the installer
          shell: /tmp/Miniconda3-py39_4.11.0-Linux-x86_64.sh -b -u -p /opt/miniconda3
        - name: Remove the installer
          file:
            state: absent
            path: /tmp/Miniconda3-py39_4.11.0-Linux-x86_64.sh
        - name: Add miniconda bin to path
          become: True
          shell: echo 'export PATH=/opt/miniconda3/bin:$PATH' >> ~/.bashrc # /etc/profile
        - name: conda - read permission for all
          become: True
          file:
            path: /opt/miniconda3
            mode: +r
            recurse: yes
        - name: conda - execution permission for all
          become: True
          file:
            path: /opt/miniconda3/bin
            mode: +x
            recurse: yes
EOF

ansible-playbook install-conda.yaml


## Download Spark
cat >install-spark-cluster.sh<<EOFEOF
#!/bin/bash
cd /opt
rm -rf spark*
yum install -y wget
wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz --no-check-certificate
tar -xzf spark-2.4.8-bin-hadoop2.7.tgz
ln -s spark-2.4.8-bin-hadoop2.7 spark
rm -rf spark-2.4.8-bin-hadoop2.7.tgz

### spark-defaults.conf
### Update /opt/spark/conf/spark-defaults.conf with below properties.
cat >/opt/spark/conf/spark-defaults.conf<<EOF
spark.driver.extraJavaOptions     -Dderby.system.home=/tmp/derby/
spark.sql.repl.eagerEval.enabled  true
spark.master                      yarn
spark.eventLog.enabled            true
spark.eventLog.dir                hdfs:///spark-logs
spark.history.provider            org.apache.spark.deploy.history.FsHistoryProvider
spark.history.fs.logDirectory     hdfs:///spark-logs
spark.history.fs.update.interval  10s
spark.history.ui.port             18080
spark.yarn.historyServer.address  master:18080
spark.yarn.jars                   hdfs:///spark-jars/*.jar
EOF

EOFEOF

chmod u+x download-spark-cluster.sh
./download-spark-cluster.sh

#########################################################################################
# 4. Configure Hadoop cluster
#########################################################################################

cd $WORKDIR

cat >configure-hadoop-cluster.sh<<EOFEOF
## Modify slaves file
cat >/opt/hadoop/etc/hadoop/slaves<<EOF
worker1
worker2
worker3
worker4
EOF

## Modify workers file
cat >/opt/hadoop/etc/hadoop/workers<<EOF
worker1
worker2
worker3
worker4
EOF

## Modify the configuration files required to run hadoop

cat >/opt/hadoop/etc/hadoop/hadoop-env.sh<<EOF
#!/bin/bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop

EOF
chmod u+x /opt/hadoop/etc/hadoop/hadoop-env.sh

#cat core-site.xml
#sed -i 's/<configuration>//g' core-site.xml
#sed -i 's/<\/configuration>//g'  core-site.xml

cat >core-site.xml<<EOF
<?xml version="1.0"?>
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/tmp</value>
        <description>A base for other temporary directories.</description>
    </property>
    <property>
        <name>fs.default.name</name>
       <value>hdfs://master:9000</value>
    </property>
</configuration>
EOF

#cat hdfs-site.xml
#sed -i 's/<configuration>//g' hdfs-site.xml
#sed -i 's/<\/configuration>//g' hdfs-site.xml

cat >hdfs-site.xml<<EOF
<?xml version="1.0"?>
<configuration>
        <property>
             <name>dfs.replication</name>
             <value>3</value>
        </property>
        <property>
             <name>dfs.namenode.name.dir</name>
             <value>file:/home/hadoop/tmp/dfs/name</value>
        </property>
        <property>
             <name>dfs.datanode.data.dir</name>
             <value>file:/home/hadoop/tmp/dfs/data</value>
        </property>
</configuration>
EOF

#cat mapred-site.xml
#sed -i 's/<configuration>//g' mapred-site.xml
#sed -i 's/<\/configuration>//g' mapred-site.xml

cat >mapred-site.xml<<EOF
<?xml version="1.0"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapred.job.tracker</name>
    <value>http://master:9001</value>
  </property>
  <property>
    <name>mapred.child.java.opts</name>
    <value>-Xmx256m</value>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=/opt/hadoop</value>
  </property>
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=/opt/hadoop</value>
  </property>
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=/opt/hadoop</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*,$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*,$HADOOP_MAPRED_HOME/share/hadoop/common/*,$HADOOP_MAPRED_HOME/share/hadoop/common/lib/*,$HADOOP_MAPRED_HOME/share/hadoop/yarn/*,$HADOOP_MAPRED_HOME/share/hadoop/yarn/lib/*,$HADOOP_MAPRED_HOME/share/hadoop/hdfs/*,$HADOOP_MAPRED_HOME/share/hadoop/hdfs/lib/*</value>
  </property>
</configuration>
EOF

#cat yarn-site.xml
#sed -i 's/<configuration>//g' yarn-site.xml
#sed -i 's/<\/configuration>//g' yarn-site.xml

cat >yarn-site.xml<<EOF
<?xml version="1.0"?>
<configuration>
    <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
    </property>
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>master</value>
    </property>
    <property>
      <name>yarn.resourcemanager.address</name>
      <value>master:18040</value>
    </property>
</configuration>
EOF

EOFEOF

chmod u+x configure-hadoop-cluster.sh
./configure-hadoop-cluster.sh

#########################################################################################
# 5. Configure Hive
#########################################################################################

cd $WORKDIR

cat >configure-hive-cluster.sh<<EOFEOF

### add HIVE_HOME in ENV ( hadoop.env )
cat >/opt/hive/conf/hive-env.sh<<EOF
export HIVE_HOME=/opt/hive
export PATH=$PATH:${HIVE_HOME}/bin

EOF
chmod u+x /opt/hive/conf/hive-env.sh

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

  <property>
    <name>hive.metastore.schema.verification</name>
    <value>false</value>
  </property>

  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>hdfs://master:9000/apps/hive/warehouse</value>
  </property>

  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://master:9083</value>
    <description>Hive metastore Thrift server</description>
  </property>

  <property>
    <name>hdatanucleus.autoStartMechanismMode</name>
    <value>ignored</value>
  </property>

  <property>
    <name>hive.server2.transport.mode</name>
    <value>binary</value>
  </property>

  <property>
    <name>hive.server2.authentication</name>
    <value>NOSASL</value>
  </property>

  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>

  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>

  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>

  <property>
    <name>hive.server2.thrift.min.worker.threads</name>
    <value>5</value>
  </property>

  <property>
    <name>hive.server2.thrift.max.worker.threads</name>
    <value>500</value>
  </property>

</configuration>
EOF
 
### Remove the conflicting Guava Files if present.
rm -rf /opt/hive/lib/guava-19.0.jar
cp /opt/hadoop/share/hadoop/hdfs/lib/guava-27.0-jre.jar /opt/hive/lib/

ls -al /opt/hive/lib/guava-27.0-jre.jar

### Download a postgresql jar file and copy it to /opt/hive/lib/
wget https://jdbc.postgresql.org/download/postgresql-42.2.24.jar
mv postgresql-42.2.24.jar /opt/hive/lib/postgresql-42.2.24.jar

ls -al /opt/hive/lib/postgresql-42.2.24.jar

EOFEOF

chmod u+x configure-hive-cluster.sh
./configure-hive-cluster.sh

#########################################################################################
# 6. Configure Spark cluster
#########################################################################################

cd $WORKDIR

cat >configure-spark-cluster.sh<<EOFEOF
cat >/opt/spark/conf/slaves<<EOF
worker1
worker2
worker3
worker4
EOF

### spark-env.sh 
cat >/opt/spark/conf/spark-env.sh<<EOF
#Java
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64

#Hadoop
export HADOOP_HOME=/opt/hadoop
export HADOOP_INSTALL_DIR=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE=$HADOOP_HOME/lib/native
export HADOOP_OPTS="-Djava libary.path=$HADOOP_HOME/lib/native"

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
export SPARK_HOME=/opt/spark
export PYSPARK_PYTHON=python
export SPARK_MASTER=spark://master:7077
export SPARK_WORKER_CORES=1
export SPARK_WORKER_MEMORY=1G
export SPARK_DRIVER_MEMORY=1G
export SPARK_EXECUTOR_MEMORY=1G
export SPARK_MASTER_HOST=master
export SPARK_WORKLOAD=worker

export PATH=${JAVA_HOME}/bin:${PATH}
export PATH=/opt/hadoop/bin:/opt/hadoop/sbin:${PATH}
export PATH=${PATH}:${HIVE_HOME}/bin
export PATH=${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/hadoop/lib/native
EOF

EOFEOF

chmod u+x /opt/spark/conf/spark-env.sh

## Install  Postgres JDBC jar in Spark jars folder.
wget https://jdbc.postgresql.org/download/postgresql-42.2.19.jar \
    -O /opt/spark/jars/postgresql-42.2.19.jar

ls -al /opt/spark/jars/postgresql-42.2.19.jar

## Install  MongoDB JDBC jar in Spark jars folder.
## https://docs.mongodb.com/spark-connector/current/
## https://mvnrepository.com/artifact/org.mongodb.spark/mongo-spark-connector_2.11/2.4.0
wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.11/2.4.0/mongo-spark-connector_2.11-2.4.0.jar -O /opt/spark/jars/mongo-spark-connector_2.11-2.4.0.jar

ls -al /opt/spark/jars/mongo-spark-connector_2.11-2.4.0.jar

chmod u+x configure-spark-cluster.sh
./configure-spark-cluster.sh

#########################################################################################
# 7. Inject host's SSH keys into Docker Machine with Docker Compose
#########################################################################################
rm -rf ~/.ssh/known_hosts
nodes='master worker1 worker2 worker3 worker4'

for node in $nodes
do
    docker exec -it $node rm -rf ~/.ssh
    ssh-copy-id root@$node
done

#########################################################################################
# 8. Upload custom files to master
#########################################################################################

cd $WORKDIR
docker exec master /bin/rm -rf /opt/*

cat >upload-custom-files.sh<<EOFEOF
#!/bin/bash

## Package files
cd /opt
rm -rf *.tar
tar cf hadoop-dis.tar hadoop hadoop-3.2.2
tar cf hive-dis.tar hive apache-hive-3.1.2-bin
tar cf spark-dis.tar spark spark-2.4.8-bin-hadoop2.7

## Hadoop
cd /opt
docker cp hadoop-dis.tar master:/opt/
docker exec master /usr/bin/tar -xf /opt/hadoop-dis.tar -C /opt
docker exec master /usr/bin/rm -rf /opt/hadoop-dis.tar

## Spark
cd /opt
docker cp spark-dis.tar master:/opt/
docker exec master /usr/bin/tar -xf /opt/spark-dis.tar -C /opt
docker exec master /usr/bin/rm -rf /opt/spark-dis.tar

## Hive
cd /opt
docker cp hive-dis.tar master:/opt/
docker exec master /usr/bin/tar -xf /opt/hive-dis.tar -C /opt
docker exec master /usr/bin/rm -rf /opt/hive-dis.tar
docker exec master ln -s /opt/hive/conf/hive-site.xml /opt/spark/conf/

rm -rf *.tar

EOFEOF

chmod u+x upload-custom-files.sh
./upload-custom-files.sh


#########################################################################################
# 9. ansible hosts
#########################################################################################

## Set ansible hosts
cat >/etc/ansible/hosts<<EOF
[cluster]
master ansible_host=172.18.0.11 ansible_user=root
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root

[master]
master ansible_host=172.18.0.11 ansible_user=root

[worker]
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root
EOF


#########################################################################################
# 10. Install Openssh server for cluster nodes
#########################################################################################

## Centos7
cat >install-openssh-centos7.sh<<EOF
#!/bin/bash
yum install -y openssh-server openssh-clients openssh-askpass

sed -i '/StrictHostKeyChecking/s/^#[ \t]*//g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking True/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
cat /etc/ssh/ssh_config | grep StrictHostKeyChecking

sed -i '/PermitRootLogin yes/s/^#[ \t]*//g' /etc/ssh/sshd_config
cat /etc/ssh/sshd_config | grep PermitRootLogin

systemctl restart sshd
systemctl status sshd
systemctl enable sshd.service
EOF

chmod u+x install-openssh-centos7.sh

docker ps -a

nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker cp install-openssh-centos7.sh $node:/root/
    docker exec -it $node /bin/bash /root/install-openssh-centos7.sh
done

## Openkbs
cat >install-openssh-debian.sh<<EOF
#!/bin/bash
export PATH=/sbin:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
apt-get update -y && apt-get upgrade -y
apt-get install -y systemd
apt-get install -y openssh-server

sed -i '/StrictHostKeyChecking/s/^#[ \t]*//g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking True/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
cat /etc/ssh/ssh_config | grep StrictHostKeyChecking

sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
cat /etc/ssh/sshd_config | grep PermitRootLogin
cat /etc/ssh/sshd_config | grep PasswordAuthentication

service ssh start
service ssh restart
service ssh status
EOF

chmod u+x install-openssh-debian.sh

docker ps -a

nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    #docker cp install-openssh-centos7.sh $node:/root/
    #docker exec -it $node /bin/bash /root/install-openssh-centos7.sh

    docker cp install-openssh-debian.sh $node:/root/
    docker exec -it $node sudo /bin/bash /root/install-openssh-debian.sh
done


## Ubuntu
cat >install-openssh-ubuntu.sh<<EOF
#!/bin/bash
export PATH=/sbin:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
apt-get update -y && apt-get upgrade -y
apt-get install -y systemd
apt-get install -y openssh-server

sed -i '/StrictHostKeyChecking/s/^#[ \t]*//g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking True/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
cat /etc/ssh/ssh_config | grep StrictHostKeyChecking

sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
cat /etc/ssh/sshd_config | grep PermitRootLogin
cat /etc/ssh/sshd_config | grep PasswordAuthentication

service ssh start
service ssh restart
service ssh status
EOF

chmod u+x install-openssh-ubuntu.sh

docker ps -a

nodes='master worker1 worker2 worker3 worker4'
for node in $nodes
do
    docker cp install-openssh-ubuntu.sh $node:/root/
    docker exec -it $node /bin/bash /root/install-openssh-ubuntu.sh
done
