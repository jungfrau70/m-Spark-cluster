#!/bin/bash
for i in `docker exec master jps | grep -i RunJar | awk '{print $1}'`
do
    echo $i
    docker exec master kill -9 $i
done
exit
