#!/bin/bash
docker exec master /opt/hive/bin/hive --service metastore &
docker exec master /opt/hive/bin/hive --service hiveserver2 &
docker exec master ps -ef | grep -i hive
