Prerequsites:
- Centos7
- Docker engine
- SSH server in deploy-server
- Ansible in deploy-server

Reference:
- https://titanwolf.org/Network/Articles/Article?AID=824350f7-a9c7-44c2-9154-5e1949e9bd8c


#########################################################################################
# 1. Instanticate ansible cluster 
     -. Change the docker image with the one for ansible cluster 
#########################################################################################

## Set IPs 
cat >/etc/hosts<<EOF
127.0.0.1   localhost
172.18.0.11  hadoop-master
172.18.0.31  hadoop-worker1
172.18.0.32  hadoop-worker2
172.18.0.33  hadoop-worker3
EOF

export WORKDIR='/root/PySpark/Step3_setup_cluster/x_Hadoop'
cd $WORKDIR

## Check the docker image
cp ../2_Ansible/docker-compose.yml .
cp docker-compose.yml docker-compose-first.yml

cat docker-compose-first.yml | grep -i container_name
cat docker-compose-first.yml | grep -i image
cat docker-compose-first.yml | grep -i ipv4_address

## Change hostname 
sed -i 's/master/hadoop-master/g' docker-compose-first.yml
sed -i 's/worker1/hadoop-worker1/g' docker-compose-first.yml
sed -i 's/worker2/hadoop-worker2/g' docker-compose-first.yml
sed -i 's/worker3/hadoop-worker3/g' docker-compose-first.yml

## Change image 
sed -i 's/centos:centos7.9.2009/jungfrau70\/centos7:ansible.1/g' docker-compose-first.yml


## Check the docker image
cat docker-compose-first.yml | grep -i container_name
cat docker-compose-first.yml | grep -i image
cat docker-compose-first.yml | grep -i ipv4_address

## Instanticate the containers
docker-compose -f docker-compose-first.yml up [-d]

#########################################################################################
# 2. Inject host's SSH keys into Docker Machine with Docker Compose
#########################################################################################
rm -rf ~/.ssh/known_hosts
nodes='hadoop-master hadoop-worker1 hadoop-worker2 hadoop-worker3'

for node in $nodes
do
    docker exec -it $node rm -rf ~/.ssh
    ssh-copy-id root@$node
done

<!-- #########################################################################################
# 3. (Alternative to #2) Generate SSH keys for cluster in deploy-server
#    Distribue them to the cluster
#########################################################################################

## Generate ssh keys
su -
rm -rf ~/.ssh
ssh-keygen

## Cleanu up
for cid in $(docker ps -a -q)
do
     docker exec $cid rm -rf ~/.ssh
done

## Copy to linux cluster nodes
nodes='hadoop-master hadoop-worker1 hadoop-worker2 hadoop-worker3'
for node in $nodes
do
  ssh-copy-id root@$node
done -->

#########################################################################################
# 3. Check if ansible cluster works in deploy-server
#########################################################################################

## Set ansible hosts
cat >/etc/ansible/hosts<<EOF
[cluster]
hadoop-master ansible_host=172.18.0.11 ansible_user=root
hadoop-worker1 ansible_host=172.18.0.31 ansible_user=root
hadoop-worker2 ansible_host=172.18.0.32 ansible_user=root
hadoop-worker3 ansible_host=172.18.0.33 ansible_user=root

[master]
hadoop-master ansible_host=172.18.0.11 ansible_user=root

[worker]
hadoop-worker1 ansible_host=172.18.0.31 ansible_user=root
hadoop-worker2 ansible_host=172.18.0.32 ansible_user=root
hadoop-worker3 ansible_host=172.18.0.33 ansible_user=root
EOF

cat /etc/hosts
cat /etc/ansible/hosts

ansible -m ping all


#########################################################################################
# 4. Install Openjdk in the fixed containers
#########################################################################################

su -
ansible cluster -m yum -a "name=java-1.8.0-openjdk,java-1.8.0-openjdk-devel state=latest"

docker exec hadoop-master /usr/bin/java -version

#########################################################################################
# 5. Setup and Configure Hadoop (in deploy-server)
#########################################################################################

cd PySpark/Step3_setup_spark_cluster/3_Hadoop/

cat >install-hadoop-cluster.sh<<EOFEOF
!/bin/bash
cd /opt
rm -rf hadoop*
yum install -y wget
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz --no-check-certificate
tar -xzf hadoop-3.3.1.tar.gz
ln -s hadoop-3.3.1 hadoop
rm -rf hadoop-3.3.1.tar.gz

## Modify slaves file
cat >/opt/hadoop/etc/hadoop/slaves<<EOF
hadoop-worker1
hadoop-worker2
hadoop-worker3
EOF

## Modify slaves file
cat >/opt/hadoop/etc/hadoop/workers<<EOF
hadoop-worker1
hadoop-worker2
hadoop-worker3
EOF

## Modify the configuration files required to run hadoop

cd /opt/hadoop/etc/hadoop

#cat core-site.xml
sed -i 's/<configuration>//g' core-site.xml
sed -i 's/<\/configuration>//g'  core-site.xml

cat >>core-site.xml<<EOF
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/tmp</value>
        <description>A base for other temporary directories.</description>
    </property>
    <!-- file system properties -->
    <property>
        <name>fs.default.name</name>
       <value>hdfs://hadoop-master:9000</value>
    </property>
</configuration>
EOF

#cat hdfs-site.xml
sed -i 's/<configuration>//g' hdfs-site.xml
sed -i 's/<\/configuration>//g' hdfs-site.xml

cat >>hdfs-site.xml<<EOF
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
sed -i 's/<configuration>//g' mapred-site.xml
sed -i 's/<\/configuration>//g' mapred-site.xml

cat >>mapred-site.xml<<EOF
<configuration>
  <property>  
    <name>mapreduce.framework.name</name>  
    <value>yarn</value>  
  </property>  
    <property>
        <name>mapred.job.tracker</name>
        <value>http://hadoop-master:9001</value>
    </property>
</configuration>
EOF

#cat yarn-site.xml
sed -i 's/<configuration>//g' yarn-site.xml
sed -i 's/<\/configuration>//g' yarn-site.xml

cat >>yarn-site.xml<<EOF
<configuration>
    <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
    </property>
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>hadoop-master</value>
    </property>
    <property>
      <name>yarn.resourcemanager.address</name>
      <value>hadoop-master:18040</value>
    </property>
</configuration>
EOF
EOFEOF

chmod u+x ./install-hadoop-cluster.sh 
./install-hadoop-cluster.sh 

## (option) Create a Hadoop user (a user specially prepared for Hadoop), and the following operations are performed under the root user

<!-- useradd -m hadoop -s /bin/bash
passwd hadoop
chown -R hadoop:hadoop hadoop
chown -R hadoop:hadoop /opt/hadoop/logs
su hadoop -->

#########################################################################################
# 6. Setting java and hadoop environment variables
#########################################################################################

## create hadoop.env

cd PySpark/Step3_setup_spark_cluster/3_Hadoop/

cat >hadoop.env<<EOF
#Java
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64
export PATH=\${JAVA_HOME}/bin:\${PATH}
#Hadoop
export HADOOP_HOME=/opt/hadoop
export PATH=\${HADOOP_HOME}/bin:\${HADOOP_HOME}/sbin:\${PATH}
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root
EOF

## hadoop-env 
cp docker-compose-first.yml docker-compose-second.yml

## add ENV into docker-compose-second.yml
    command:
      - |
        /usr/bin/hostnamectl set-hostname hadoop-worker3
    env_file:
      - hadoop.env

## restart with docker-compose-second.yml
docker-compose down
docker-compose -f docker-compose-second.yml up

## distribue the custom hadoop to hadoop-master
cd /opt
tar -cf hadoop-dis.tar hadoop hadoop-3.3.1
docker cp hadoop-dis.tar hadoop-master:/opt
docker exec hadoop-master /usr/bin/tar -xf /opt/hadoop-dis.tar -C /opt
docker exec hadoop-master /usr/bin/rm -rf /opt/hadoop-dis.tar

#########################################################################################
# 7. Build custom image
#########################################################################################

## Commit Docker image and push to repository
docker ps -a
docker commit hadoop-master jungfrau70/centos7:hadoop.1  

docker login                                                 
docker push jungfrau70/centos7:hadoop.1

## Restart docker-compose with lastest docker image
cd PySpark/Step3_setup_spark_cluster/3_Hadoop/
docker-compose down

cp docker-compose-second.yml docker-compose-3rd.yml 
sed -i 's/jungfrau70\/centos7:ansible.1/jungfrau70\/centos7:hadoop.1/g' docker-compose-3rd.yml 

docker-compose -f docker-compose-3rd.yml up -d

#########################################################################################
# 8. Clean up
#########################################################################################

docker ps -a
docker-compose -f docker-compose-3rd.yml down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

cat >/etc/hosts<<EOF
127.0.0.1   localhost
EOF

cat >/etc/ansible/hosts<<EOF
EOF

#########################################################################################
# 9. Backup and restore in VMware Workstation Player
#########################################################################################

Copy folder and rename it

<!-- ## Shrink the image

https://cumulocity.com/guides/edge/backup-and-restore/#:~:text=Backup%20and%20restore-,Backup%20and%20restore%20in%20VMware%20Workstation%20Player,Open%20and%20follow%20the%20prompts.

Open the VMware Tools Control Panel.
In Windows, double-click the VMware Tools icon in the system tray, or go to Start > Control Panel > VMware Tools.

Click the Shrink tab.
Ensure that your boot drive is selected, click Prepare to Shrink, and follow the prompts.

## Creating a backup in VMware Workstation Pro

1. Shut down the Edge appliance.
2. Select the Edge appliance that you want to back up.
3. Click File > Export to OVF.
4. Click Save.

## Restoring an Edge appliance in VMware Workstation Pro

1. Click File > Open.
2. Select the Edge appliance that you want to restore and click Open.
3. Click Import. -->
