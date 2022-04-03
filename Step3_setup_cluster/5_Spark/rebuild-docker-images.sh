#!/bin/bash

## Create Docker images
docker ps -a
docker commit master $id/ubuntu18.04:de-master.$version
docker commit worker1 $id/ubuntu18.04:de-worker1.$version
docker commit worker2 $id/ubuntu18.04:de-worker2.$version

## Push to repository
docker login

docker push $id/ubuntu18.04:de-master.$version
docker push $id/ubuntu18.04:de-worker1.$version
docker push $id/ubuntu18.04:de-worker2.$version

## Change in docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-master.*/$id\/ubuntu18.04:de-master.$version/g" docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-worker1.*/$id\/ubuntu18.04:de-worker1.$version/g" docker-compose.yml
sed -i "s/$id\/ubuntu18.04:de-worker2.*/$id\/ubuntu18.04:de-worker2.$version/g" docker-compose.yml
cat docker-compose.yml | grep -i jungfrau