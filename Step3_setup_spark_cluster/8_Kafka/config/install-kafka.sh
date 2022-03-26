#!/bin/bash
cd /opt
rm -rf kafka*

wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.12-3.1.0.tgz --no-check-certificate
tar -xzf kafka_2.12-3.1.0.tgz
rm -rf kafka_2.12-3.1.0.tgz
ln -s kafka_2.12-3.1.0 kafka