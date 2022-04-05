#!/bin/bash

~/start-hadoop-cluster.sh
sleep 1
~/start-spark-cluster.sh
sleep 1
~/start-spark-history-server.sh
sleep 1
~/start-hive-server2.sh
echo ""
echo "Finished"
