#!/bin/bash
nodes='master worker1 worker2'
for node in $nodes
do 
    sleep 3
    echo $node
    docker exec $node jps
    echo 
done
