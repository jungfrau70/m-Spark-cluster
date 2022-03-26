Prerequsites:
- Centos7
- Docker engine
- SSH server in deploy-server
- Ansible in deploy-server
- Hadoop master

Reference:
- https://titanwolf.org/Network/Articles/Article?AID=824350f7-a9c7-44c2-9154-5e1949e9bd8c


#########################################################################################
# 1. Set ENVIRONMENT variables
#########################################################################################

## Check the docker image
# (if not exits) git clone https://github.com/jungfrau70/team2.git PySpark
cd ~/PySpark/Step4_setup_spark_cluster/3_Hadoop/

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

cat docker-compose-3rd.yml | grep -i container_name
cat docker-compose-3rd.yml | grep -i image
cat docker-compose-3rd.yml | grep -i ipv4_address

cp docker-compose-3rd.yml docker-compose-4th.yml
<!-- ## Change hostname 
sed -i 's/master/hadoop-master/g' docker-compose-3rd.yml
sed -i 's/worker1/hadoop-worker1/g' docker-compose-3rd.yml
sed -i 's/worker2/hadoop-worker2/g' docker-compose-3rd.yml
sed -i 's/worker3/hadoop-worker3/g' docker-compose-3rd.yml

## Change image 
sed -i 's/jungfrau70\/centos7:ansible.1/jungfrau70\/centos7:hadoop.1/g' docker-compose-3rd.yml


## Check the docker image
cat docker-compose-first.yml | grep -i container_name
cat docker-compose-first.yml | grep -i image
cat docker-compose-first.yml | grep -i ipv4_address -->

## Instanticate the containers
docker-compose -f docker-compose-4th.yml up -d

#########################################################################################
# 2. HOSTNAMEs
#########################################################################################

## Set hostname
nodes='hadoop-master hadoop-worker1 hadoop-worker2 hadoop-worker3'
for node in $nodes
do
    docker exec -it $node /usr/bin/hostnamectl set-hostname $node
done

## Check hostname
nodes='hadoop-master hadoop-worker1 hadoop-worker2 hadoop-worker3'
for node in $nodes
do
    docker exec -it $node /usr/bin/hostname
done

#########################################################################################
# 3. Inject host's SSH keys into Docker Machine with Docker Compose
#########################################################################################
rm ~/.ssh/known_hosts
nodes='hadoop-master hadoop-worker1 hadoop-worker2 hadoop-worker3'

for node in $nodes
do
    docker exec -it $node rm -rf ~/.ssh
    ssh-copy-id root@$node
done

#########################################################################################
# 4. Check if ansible cluster works
#########################################################################################

## Set IPs 
cat >/etc/hosts<<EOF
127.0.0.1   localhost
172.18.0.11  hadoop-master
172.18.0.31  hadoop-worker1
172.18.0.32  hadoop-worker2
172.18.0.33  hadoop-worker3
EOF

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

## Check If Ansible cluster works
ansible -m ping all

#########################################################################################
# 5. Check SSH among hadoop cluster
      volumes:
        - ~/.ssh:/root/.ssh:ro
#########################################################################################
cd ~/PySpark/Step3_setup_spark_cluster/3_Hadoop/

docker exec -it hadoop-master /bin/bash
docker exec -it hadoop-master /usr/bin/ssh hadoop-worker1

#########################################################################################
# 6. Install Openjdk in the fixed containers
#########################################################################################

su -
ansible cluster -m yum -a "name=java-1.8.0-openjdk,java-1.8.0-openjdk-devel state=latest"

docker exec hadoop-master /usr/bin/java -version

#########################################################################################
# 7. Formatting namenode
Instanticate hadoop cluster 
     -. Change the docker image with the one for ansible cluster 
#########################################################################################

## Check If Hadoop cluster works
docker exec -it hadoop-master /bin/bash

cd /opt/hadoop/bin
hdfs namenode -format

#########################################################################################
# 8. Start hadoop cluster
#########################################################################################

cat >>$HADOOP_HOME/etc/hadoop/hadoop-env.sh<<EOF
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.322.b06-1.el7_9.x86_64/
EOF

cat $HADOOP_HOME/etc/hadoop/hadoop-env.sh | grep JAVA_HOME

nodes = 'hadoop-worker1 hadoop-worker2 hadoop-worker3'
for node in $nodes
do
  scp $HADOOP_HOME/etc/hadoop/hadoop-env.sh $node:$HADOOP_HOME/etc/hadoop/hadoop-env.sh
done

cd $HADOOP_HOME/sbin
start-dfs.sh
start-yarn.sh

start-all.sh
stop-all.sh

## (in case of second run) Modify worker file
cat >/opt/hadoop/etc/hadoop/workers<<EOF
hadoop-worker1
hadoop-worker2
hadoop-worker3
EOF

for node in hadoop-worker1 hadoop-worker2 hadoop-worker3
do
  scp /opt/hadoop/etc/hadoop/workers $node:/opt/hadoop/etc/hadoop/workers
done

## :: go to 4. Formatting namenode

#########################################################################################
# 9. Check process
#########################################################################################

## in cluster-master
[root@cluster-master sbin]# jps
2484 SecondaryNameNode
2648 Jps
2315 NameNode

## in cluster-slave
[root@cluster-slave1 logs]# jps
27502 DataNode
27583 Jps

#########################################################################################
# 10. Experience hadoop
#########################################################################################

## Try to upload files in the master terminal
hdfs dfs -put anaconda-post.log /
hdfs dfs -ls /


#########################################################################################
# 11. Build image
#########################################################################################

## Commit Docker image and push to repository
docker ps -a
docker commit hadoop-master jungfrau70/centos7:hadoop.11

docker login                                                 
docker push jungfrau70/centos7:hadoop.11

cp docker-compose-4th.yml docker-compose-5th.yml
sed -i 's/jungfrau70\/centos7:hadoop.1/jungfrau70\/centos7:hadoop.11/g' docker-compose-5th.yml

cp docker-compose-5th.yml hadoop-docker-compose.yml

#########################################################################################
# 12. Clean up
#########################################################################################

docker ps -a
docker-compose -f hadoop-docker-compose.yml down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

#########################################################################################
# 13. Backup and restore in VMware Workstation Player
#########################################################################################

Copy folder and rename it
