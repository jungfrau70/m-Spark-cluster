#!/bin/bash

~/stop-hadoop-cluster.sh &&
~/stop-spark-cluster.sh

~/stop-hive-server2.sh &&
~/stop-spark-history-server.sh 

sleep 5

nodes='master worker1 worker2'
for node in $nodes
do
    docker exec $node rm -rf /home/hadoop/tmp/
done

docker exec master /opt/hadoop/bin/hdfs namenode -format

~/start-hadoop-cluster.sh

sleep 5

docker cp ~/configure-directories.sh master:/root/
docker exec -it master /bin/bash /root/configure-directories.sh