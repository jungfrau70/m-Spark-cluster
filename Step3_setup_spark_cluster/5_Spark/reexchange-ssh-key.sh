#!/bin/bash

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
# 2. Clean up the existing keys and ...
#########################################################################################

## Clean up
nodes='master worker1 worker2'
for node in $nodes
do 
    docker exec -it $node rm -rf ~/.ssh
done

#########################################################################################
# 2. Distribute SSH keys to cluster 
#########################################################################################

## Generate ssh key
docker exec -it master ssh-keygen -t rsa
docker exec -it master cp ~/.ssh/id_rsa.pub \
~/.ssh/authorized_keys

## Add authorized_keys into worker1, worker2
nodes='worker1 worker2'
for node in $nodes
do
    docker exec -it master ssh-copy-id root@$node
done

## Add nodes to known_hosts in deploy-server
nodes='master worker1 worker2'
for node in $nodes
do 
  docker exec -it master ssh root@$node
done

## Check if ssh works
docker exec -it master ssh worker1
docker exec -it master ssh worker2
