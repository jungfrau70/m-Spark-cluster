#!/bin/bash

## Install Anaconda in silent mode
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh -b -p /opt/conda
rm -rf Anaconda3-2021.11-Linux-x86_64.sh 

## Conda init
eval "$(/opt/conda/bin/conda shell.bash hook)"
conda init
cat ~/.bashrc

## (If required) add ENV in .bashrc
cat >>~/.bashrc<<EOF
export PATH=$PATH:/opt/conda/bin/
EOF