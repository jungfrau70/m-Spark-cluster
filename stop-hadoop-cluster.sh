#!/bin/bash
docker exec master /opt/hadoop/sbin/stop-all.sh
#docker exec master sudo /opt/hadoop/sbin/stop-all.sh

nodes='master worker1 worker2'
for node in $nodes
do
    sleep 3
    echo $node
    docker exec $node jps
    echo
done
