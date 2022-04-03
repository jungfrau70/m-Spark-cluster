export WORKDIR='/root/PySpark/workspace/7_MLOps'
cd $WORKDIR


conda env create -f environment.yml
conda activate mlops
pip install -r requirements.txt

git init
dvc init

create step_01.py
create step_02.py
create dvc.yaml

dvc repro

git remote add origin https://github.com/jungfrau70/mlops.git
git add . && git commit -m "My first commit"
git push origin master
