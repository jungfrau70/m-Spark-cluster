#!/bin/bash
docker exec master /opt/hadoop/sbin/start-all.sh
#docker exec master sudo /opt/hadoop/sbin/start-all.sh

nodes='master worker1 worker2'
for node in $nodes
do 
    sleep 3
    echo $node
    docker exec $node jps
    echo 
done
