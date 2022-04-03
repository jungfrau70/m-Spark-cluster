
export WORKDIR='/root/PySpark/workspace/4_Airflow'
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

## Create virtual env - pipeline
export WORKDIR='/root/PySpark/workspace/7_Airflow'
cd $WORKDIR

conda env create -f environment.yml
conda env list

base     *...
pipeline  ...

#conda remove --name pipeline --all

conda activate pipeline


#########################################################################################
# 3. (deploy-server, pipeline) Install python packages
#########################################################################################

# (pipeline) Install apache-airflow related packages
export AIRFLOW_HOME=~/airflow
export AIRFLOW_VERSION="2.2.4"
export PYTHON_VERSION="3.7"
export PYSPARK_VERSION="3.0.3"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip --version
pip install --upgrade pip
pip install -r requirements.txt

#########################################################################################
# 4. (deploy-server, pipeline) Check python packages
#########################################################################################

pip show apache-airflow
pip show apache-airflow-providers-apache-spark
pip show pyspark

#########################################################################################
# 5. (deploy-server, pipeline) Add pipeline virtual env into ipykernel
#########################################################################################

## (option) Add pipeline virtual env into ipykernel
(pipeline) python -m ipykernel install --user --name pipeline --display-name "Python (pipeline)"

(pipeline) jupyter kernelspec list 

## Remove ipykernel
#jupyter kernelspec remove pipeline

#########################################################################################
# 6. (deploy-server, pipeline) Start jupyter lab
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

