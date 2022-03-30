#!/bin/bash
### Download Hive.
cd /opt
wget https://dlcdn.apache.org/hive/hive-2.3.9/apache-hive-2.3.9-bin.tar.gz --no-check-certificate
tar xzf apache-hive-2.3.9-bin.tar.gz
rm -rf apache-hive-2.3.9-bin.tar.gz
ln -s apache-hive-2.3.9-bin hive

#wget https://mirrors.ocf.berkeley.edu/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz --no-check-certificate
#tar xzf apache-hive-3.1.2-bin.tar.gz
#rm -rf apache-hive-3.1.2-bin.tar.gz
#ln -s /opt/apache-hive-3.1.2-bin /opt/hive