#!/bin/bash
cd /usr/local
rm -rf livy*
yum install -y wget
wget https://dlcdn.apache.org/incubator/livy/0.7.1-incubating/apache-livy-0.7.1-incubating-bin.zip --no-check-certificate
unzip apache-livy-0.7.1-incubating-bin.zip
rm -rf apache-livy-0.7.1-incubating-bin.zip
ln -s apache-livy-0.7.1-incubating-bin livy
