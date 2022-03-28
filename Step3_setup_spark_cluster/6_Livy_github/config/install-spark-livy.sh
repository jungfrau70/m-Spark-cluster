#!/bin/bash
cd /opt
rm -rf livy*

apt-get update -y && apt-get install -y unzip \
    && curl "https://dlcdn.apache.org/incubator/livy/0.7.1-incubating/apache-livy-0.7.1-incubating-bin.zip" -O \
    && unzip "apache-livy-0.7.1-incubating-bin" \
    && rm -rf "apache-livy-0.7.1-incubating-bin.zip" \
    && ln -s "apache-livy-0.7.1-incubating-bin" livy \
    && mkdir ./livy/logs
    
    # \
    #&& chown -R 1001:1001 $LIVY_HOME