
Reference:
- https://www.elastic.co/guide/en/beats/filebeat/current/setup-repositories.html

#########################################################################################
# 1. (deploy-server) Install filebeat
#########################################################################################

export WORKDIR='/root/PySpark/workspace/3_Kafka'
cd $WORKDIR

bash config/install-filebeat.sh 

mkdir -p ~/PySpark/workspace/logs/

chown -R 50000:50000 ~/PySpark/workspace/logs/

cp filebeat.yml /etc/filebeat/

systemctl start filebeat

systemctl status filebeat