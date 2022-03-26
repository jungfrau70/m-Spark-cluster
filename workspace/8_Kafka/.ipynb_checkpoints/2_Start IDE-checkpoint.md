export WORKDIR='/root/PySpark/workspace/8_Kafka'
cd $WORKDIR

#########################################################################################
# 1. (deploy-server) Install Anaconda
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

## Create virtual env - kafka
export WORKDIR='/root/PySpark/workspace/8_Kafka'
cd $WORKDIR

conda env create -f environment.yml
conda env list

# conda environments:
#
base                     /opt/conda
kafka                    /opt/conda/envs/kafka
pipeline              *  /opt/conda/envs/pipeline

#conda remove --name pipeline --all

conda activate kafka

#########################################################################################
# 3. (deploy-server, kafka) Install python packages
#########################################################################################

# (kafka) Install kafka related packages

pip --version
pip install --upgrade pip
pip install -r requirements.txt

#########################################################################################
# 4. (deploy-server, kafka) Check python packages
#########################################################################################

pip show kafka-python

#########################################################################################
# 5. (deploy-server, kafka) Add pipeline virtual env into ipykernel
#########################################################################################

## (option) Add pipeline virtual env into ipykernel
(pipeline) python -m ipykernel install --user --name pipeline --display-name "Python (kafka)"

(pipeline) jupyter kernelspec list 

## Remove ipykernel
#jupyter kernelspec remove kafka

#########################################################################################
# 6. (deploy-server, kafka) Start jupyter lab
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
