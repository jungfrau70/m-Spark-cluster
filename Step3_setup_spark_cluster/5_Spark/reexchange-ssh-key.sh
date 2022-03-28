#!/bin/bash


## Set root's password for ssh key exchange
nodes='master worker1 worker2'
for node in $nodes
do
    echo $node
    docker exec -it $node passwd
done

## Remove existing known_hosts for ReSet
rm -rf ~/.ssh/known_hosts*

## Add nodes to new known_hosts in deploy-server(=master)
nodes='master worker1 worker2'
for node in $nodes
do 
  ssh root@$node
done

## Copy authorized_keys to workers
nodes='worker1 worker2'
for node in $nodes
do
    docker exec -it $node rm -rf ~/.ssh
    ssh-copy-id root@$node
done

## Check if ssh works
docker exec -it master ssh worker1
docker exec -it master ssh worker2
