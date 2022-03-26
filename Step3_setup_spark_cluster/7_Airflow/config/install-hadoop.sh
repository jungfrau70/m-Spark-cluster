#!/bin/bash
cd /opt
rm -rf hadoop*

wget https://dlcdn.apache.org/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz --no-check-certificate
tar -xzf hadoop-3.2.2.tar.gz
ln -s hadoop-3.2.2 hadoop
rm -rf hadoop-3.2.2.tar.gz

#wget https://archive.apache.org/dist/hadoop/common/hadoop-2.8.0/hadoop-2.8.0.tar.gz --no-check-certificate
#tar -xzf hadoop-2.8.0.tar.gz
#rm -rf hadoop-2.8.0.tar.gz
#ln -s hadoop-2.8.0 hadoop

#wget https://archive.apache.org/dist/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz --no-check-certificate
#tar -xzf hadoop-2.7.7.tar.gz
#ln -s hadoop-2.7.7 hadoop
#rm -rf hadoop-2.7.7.tar.gz

#wget https://dlcdn.apache.org/hadoop/common/hadoop-2.10.1/hadoop-2.10.1.tar.gz --no-check-certificate
#tar -xzf hadoop-2.10.1.tar.gz
#ln -s hadoop-2.10.1 hadoop
#rm -rf hadoop-2.10.1.tar.gz

#wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz --no-check-certificate
#tar -xzf hadoop-3.3.1.tar.gz
#ln -s hadoop-3.3.1 hadoop
#rm -rf hadoop-3.3.1.tar.gz