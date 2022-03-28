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

docker-compose up --build

#########################################################################################
# 1. Set Root's password for cluster nodes
#########################################################################################

## Set root's password for ssh key exchange
nodes='master worker1 worker2'
for node in $nodes
do 
    echo $node
    docker exec -it $node passwd
done

#########################################################################################
# 2. Distribute SSH keys to cluster 
#########################################################################################

## Generate ssh key
ssh-keygen -t rsa
cd ~/.ssh
cat id_rsa.pub > authorized_keys

## Remove known_hosts for ReSet, if exists
rm -rf ~/.ssh/known_hosts 

## Add nodes to known_hosts in deploy-server
nodes='master worker1 worker2'
for node in $nodes
do 
  ssh root@$node
done

## Add nodes to known_hosts in deploy-server
nodes='master worker1 worker2'
for node in $nodes
do
    docker exec -it $node rm -rf ~/.ssh
    ssh-copy-id root@$node
done

## Check if ansible works
ansible -m ping cluster

## Check if ssh works
docker exec -it master ssh worker1
docker exec -it master ssh worker2


#########################################################################################
# 3. (deploy-server) Create scripts for Start/Stop Cluster
#########################################################################################

## Stop hadoop-custer
cat >stop-hadoop-cluster.sh<<EOF
#!/bin/bash
docker exec master /opt/hadoop/sbin/stop-all.sh
#docker exec master sudo /opt/hadoop/sbin/stop-all.sh

nodes='master worker1 worker2'
for node in \$nodes
do
    sleep 3
    echo \$node
    docker exec \$node jps
    echo
done
EOF
chmod u+x stop-hadoop-cluster.sh 

## Start hadoop-custer
cat >start-hadoop-cluster.sh<<EOF
#!/bin/bash
docker exec master /opt/hadoop/sbin/start-all.sh
#docker exec master sudo /opt/hadoop/sbin/start-all.sh

nodes='master worker1 worker2'
for node in \$nodes
do 
    sleep 3
    echo \$node
    docker exec \$node jps
    echo 
done
EOF
chmod u+x ./start-hadoop-cluster.sh 

## Stop spark-custer
cat >stop-spark-cluster.sh<<EOF
#!/bin/bash
docker exec master /opt/spark/sbin/stop-all.sh
#docker exec master sudo /opt/spark/sbin/stop-all.sh

nodes='master worker1 worker2'
for node in \$nodes
do
    sleep 3
    echo \$node
    docker exec \$node jps
    echo 
done
EOF
chmod u+x stop-spark-cluster.sh 

## Start spark-custer
cat >start-spark-cluster.sh<<EOF
#!/bin/bash
docker exec master /opt/spark/sbin/start-all.sh
#docker exec master sudo /opt/spark/sbin/start-all.sh

nodes='master worker1 worker2'
for node in \$nodes
do 
    sleep 3
    echo \$node
    docker exec \$node jps
    echo 
done
EOF
chmod u+x ./start-spark-cluster.sh 

## Check cluster
cat >check-cluster.sh<<EOF
#!/bin/bash
nodes='master worker1 worker2'
for node in \$nodes
do 
    sleep 3
    echo \$node
    docker exec \$node jps
    echo 
done
EOF
chmod u+x ./check-cluster.sh 

## Start Hive-server2
cat >start-hive-server2.sh<<EOF
#!/bin/bash
docker exec master /opt/hive/bin/hive --service metastore &
docker exec master /opt/hive/bin/hive --service hiveserver2 &
docker exec master ps -ef | grep -i hive
EOF
chmod u+x start-hive-server2.sh

## Stop Hive-server2
cat >stop-hive-server2.sh<<EOF
#!/bin/bash
for i in \`docker exec master jps | grep -i RunJar | awk '{print \$1}'\`
do
    echo \$i
    docker exec master kill -9 \$i
done
exit
EOF

chmod u+x stop-hive-server2.sh

## Start Spark history server
cat >start-spark-history-server.sh<<EOF
#!/bin/bash
docker exec master /opt/spark/sbin/start-history-server.sh &
EOF
chmod u+x ./start-spark-history-server.sh

## Stop Spark history server
cat >stop-spark-history-server.sh<<EOF
#!/bin/bash
docker exec master /opt/spark/sbin/stop-history-server.sh &
EOF
chmod u+x ./stop-spark-history-server.sh


#########################################################################################
# 4. Build the docker image for ansible cluster 
#########################################################################################

docker ps -a

## build custom docker image
docker exec master lsb_release -a
docker commit master jungfrau70/ubuntu18.04:de-cluster.4

## push customer docker image
docker image ls
docker login
docker push jungfrau70/ubuntu18.04:de-cluster.4

#########################################################################################
# 5. (if rquired) Clean up
#########################################################################################

cd 

## Remove all data
docker ps -a
docker-compose down

export WORKDIR='/root/PySpark/Step4_setup_airflow_cluster/1_Spark/'
cd $WORKDIR

rm -rf db.sql postgres-data spark-apps spark-data

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

cat >/etc/hosts<<EOF
127.0.0.1   localhost
EOF

cat >/etc/ansible/hosts<<EOF
EOF
