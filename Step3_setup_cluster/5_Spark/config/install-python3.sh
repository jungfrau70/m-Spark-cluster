#!/bin/bash
yum install -y https://repo.ius.io/ius-release-el7.rpm
yum update
yum install -y python36u python36u-libs python36u-devel python36u-pip

#wget https://repo.continuum.io/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh -O /opt/Anaconda3-5.0.0.1-Linux-x86_64.sh
#bash Anaconda3-5.0.0.1-Linux-x86_64.sh -b -u -p /opt/conda
#rm -rf /opt/Anaconda3-5.0.0.1-Linux-x86_64.sh
#/opt/conda/bin/conda init bash
#/opt/conda/bin/conda install -c anaconda jupyter 
#/opt/conda/bin/conda install -c conda-forge jupyterlab findspark pyspark==2.4.8