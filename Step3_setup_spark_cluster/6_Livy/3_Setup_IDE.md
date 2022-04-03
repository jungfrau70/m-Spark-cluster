
export WORKDIR='/root/PySpark/workspace/6_Livy'
cd $WORKDIR

#########################################################################################
# 1. (deploy-server) (if not installed) Install Anaconda
#########################################################################################

## Install Anaconda in silent mode
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh -b -p /opt/conda
rm -rf Anaconda3-2021.11-Linux-x86_64.sh 

## Initialize Conda
eval "$(/opt/conda/bin/conda shell.bash hook)"
conda init
cat ~/.bashrc

## (If required) add ENV in .bashrc
cat >>~/.bashrc<<EOF
export PATH=$PATH:/opt/conda/bin/
EOF

^D
## New Terminal

#########################################################################################
# 2. (deploy-server) Create Virtual Environment
#########################################################################################

## Create virtual env - livy
export WORKDIR='/root/PySpark/Step3_setup_spark_cluster/6_Livy'
cd $WORKDIR

conda env create -f environment.yml
conda env list

base     *...
livy      ...

#conda remove --name livy --all

conda activate livy


#########################################################################################
# 3. (deploy-server, livy) Install python packages
#########################################################################################

pip --version
pip install --upgrade pip
pip install -r requirements.txt

#########################################################################################
# 4. (deploy-server, pipeline) Check python packages
#########################################################################################

pip show requests


#########################################################################################
# 5. (deploy-server, pipeline) Start jupyter lab
#########################################################################################

#(id required) pip install jupyter_contrib_nbextensions

jupyter notebook --generate-config
jupyter notebook password

## (If required)
wget http://es.archive.ubuntu.com/ubuntu/pool/main/libf/libffi/libffi7_3.3-4_amd64.deb
dpkg -i libffi7_3.3-4_amd64.deb
rm -f libffi7_3.3-4_amd64.deb

cat >/root/.jupyter/jupyter_notebook_config.py<<EOF
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True
EOF

jupyter lab

## Exit
Ctrl + C
