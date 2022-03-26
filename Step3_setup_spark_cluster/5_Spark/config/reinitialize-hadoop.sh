!/bin/bash

~/stop-hadoop-cluster.sh

nodes='master worker1 worker2'
for node in $nodes
do
    docker exec $node rm -rf /home/hadoop/tmp/
done

docker exec master /opt/hadoop/bin/hdfs namenode -format

~/start-hadoop-cluster.sh
docker exec -it master /bin/bash /root/configure-directories.sh