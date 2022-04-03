#!/bin/bash
cd /opt
rm -rf spark*

# wget https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz --no-check-certificate
# tar -xzf spark-3.2.1-bin-hadoop3.2.tgz
# rm -rf spark-3.2.1-bin-hadoop3.2.tgz
# ln -s spark-3.2.1-bin-hadoop3.2 spark

wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.6.tgz --no-check-certificate
tar -xzf spark-2.4.8-bin-hadoop2.6.tgz
rm -rf spark-2.4.8-bin-hadoop2.6.tgz
ln -s spark-2.4.8-bin-hadoop2.6 spark

# wget https://dlcdn.apache.org/spark/spark-3.0.3/spark-3.0.3-bin-hadoop3.2.tgz --no-check-certificate
# tar -xzf spark-3.0.3-bin-hadoop3.2.tgz
# rm -rf spark-3.0.3-bin-hadoop3.2.tgz
# ln -s spark-3.0.3-bin-hadoop3.2 spark

# get https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz --no-check-certificate
# tar -xzf spark-3.1.2-bin-hadoop3.2.tgz
# rm -rf spark-3.1.2-bin-hadoop3.2.tgz
# ln -s spark-3.1.2-bin-hadoop3.2 spark

# wget https://dlcdn.apache.org/spark/spark-3.1.3/spark-3.1.3-bin-hadoop2.7.tgz --no-check-certificate
# tar -xzf spark-3.1.3-bin-hadoop2.7.tgz
# ln -s spark-3.1.3-bin-hadoop2.7 spark
# rm -rf spark-3.1.3-bin-hadoop2.7.tgz