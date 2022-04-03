Prerequsites:
- Centos7 (=deploy-server)
- Docker engine in deploy-server

References:
- https://www.docker.com/blog/how-to-deploy-on-remote-docker-hosts-with-docker-compose/


#########################################################################################
# 1. Install Ansible using epel
     https://www.snel.com/support/how-to-install-ansible-on-centos-7/
#########################################################################################

su - 

cat >install-ansible.sh<<
yum -y update
yum search epel-release
yum install -y epel-release
yum -y update
yum -y install ansible
EOF

chmod u+x ./install-ansible.sh
./install-ansible.sh

ansible --version

#########################################################################################
# 2. Generate SSH keys 
#########################################################################################

## Generate ssh keys
su -
ssh-keygen

#########################################################################################
# 3. Create linux cluster with the fixed IPs using docker
#########################################################################################

## Download Docker Image
docker pull centos:centos7.9.2009

cat >setup-docker-4-hadoop.sh<<EOFEOF
## Set IPs 
cat >/etc/hosts<<EOF
127.0.0.1   localhost
172.18.0.11  master
172.18.0.31  worker1
172.18.0.32  worker2
172.18.0.33  worker3
EOF

## Create Docker Network
docker network create --subnet=172.18.0.0/16 netgroup

## Create fixed IP containers
docker run -d --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup --name master -h master --net netgroup --ip 172.18.0.11 centos:centos7.9.2009 /usr/sbin/init
docker run -d --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup --name worker1 -h worker1 --net netgroup --ip 172.18.0.31 centos:centos7.9.2009 /usr/sbin/init
docker run -d --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup --name worker2 -h worker2 --net netgroup --ip 172.18.0.32 centos:centos7.9.2009 /usr/sbin/init
docker run -d --privileged -ti -v /sys/fs/cgroup:/sys/fs/cgroup --name worker3 -h worker3 --net netgroup --ip 172.18.0.33 centos:centos7.9.2009 /usr/sbin/init

## Set hostnames 
docker exec -it master /usr/bin/hostnamectl set-hostname master;
docker exec -it worker1 /usr/bin/hostnamectl set-hostname worker1;
docker exec -it worker2 /usr/bin/hostnamectl set-hostname worker2;
docker exec -it worker3 /usr/bin/hostnamectl set-hostname worker3

## Check hostnames 
docker exec -it master /bin/hostname;
docker exec -it worker1 /bin/hostname;
docker exec -it worker2 /bin/hostname;
docker exec -it worker3 /bin/hostname

EOFEOF

chmod u+x setup-docker-4-hadoop.sh 
./setup-docker-4-hadoop.sh 

#########################################################################################
# 4. Convert the containerized linux cluster into docker-compose.yml
#########################################################################################

## clean up Containers
docker ps -a
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker image ls
docker system prune -a

## Create docker-compose.yml
git clone https://github.com/jungfrau70/team2.git PySpark
cd /root/PySpark/Step3_setup_cluster/1_Ansible

ls -al docker-compose.yml

## Instanciate docker-compose.yml

docker-compose up

#########################################################################################
# 5. Set Root's password for cluster nodes
#########################################################################################

cd ~

## Set root passwd 
docker exec -it master passwd
docker exec -it worker1 passwd
docker exec -it worker2 passwd
docker exec -it worker3 passwd

#########################################################################################
# 6. Install Openssh server for cluster nodes
#########################################################################################

cat >install-openssh.sh<<EOF
!/bin/bash
yum install -y openssh-server openssh-clients openssh-askpass

sed -i '/StrictHostKeyChecking/s/^#[ \t]*//g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking ask/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed -i 's/StrictHostKeyChecking True/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
cat /etc/ssh/ssh_config | grep StrictHostKeyChecking

sed -i '/PermitRootLogin yes/s/^#[ \t]*//g' /etc/ssh/sshd_config
cat /etc/ssh/sshd_config | grep PermitRootLogin

systemctl restart sshd
systemctl status sshd
systemctl enable sshd.service
EOF

chmod u+x install-openssh.sh 
docker ps -a

nodes='master worker1 worker2 worker3'
for node in $nodes
do
     docker cp install-openssh.sh $node:/root/
     docker exec -it $node /bin/bash /root/install-openssh.sh
done

#########################################################################################
# 7. Distribute SSH keys to cluster 
#########################################################################################

## Copy to linux cluster nodes

for node in $nodes
do
     ssh-copy-id root@$node
done

#########################################################################################
# 8. Check if ansible cluster works
#########################################################################################

## Set ansible hosts
cat >/etc/ansible/hosts<<EOF
[cluster]
master ansible_host=172.18.0.11 ansible_user=root
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root
worker3 ansible_host=172.18.0.33 ansible_user=root

[master]
master ansible_host=172.18.0.11 ansible_user=root

[worker]
worker1 ansible_host=172.18.0.31 ansible_user=root
worker2 ansible_host=172.18.0.32 ansible_user=root
worker3 ansible_host=172.18.0.33 ansible_user=root
EOF

ansible -m ping cluster

#########################################################################################
# 9. Build the docker image for ansible cluster 
#########################################################################################

docker ps -a

## build custom docker image
docker commit master jungfrau70/centos7:ansible.1

## push customer docker image
docker image ls
docker login
docker push jungfrau70/centos7:ansible.1

#########################################################################################
# 10. Clean up
#########################################################################################

docker ps -a
docker-compose down
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network rm netgroup
docker system prune -a

cat >/etc/hosts<<EOF
127.0.0.1   localhost
EOF

cat >/etc/ansible/hosts<<EOF
EOF

#########################################################################################
# 11. Backup and restore in VMware Workstation Player
#########################################################################################

Copy folder and rename it

<!-- ## Shrink the image

https://cumulocity.com/guides/edge/backup-and-restore/#:~:text=Backup%20and%20restore-,Backup%20and%20restore%20in%20VMware%20Workstation%20Player,Open%20and%20follow%20the%20prompts.

Open the VMware Tools Control Panel.
In Windows, double-click the VMware Tools icon in the system tray, or go to Start > Control Panel > VMware Tools.

Click the Shrink tab.
Ensure that your boot drive is selected, click Prepare to Shrink, and follow the prompts.

## Creating a backup in VMware Workstation Pro

1. Shut down the Edge appliance.
2. Select the Edge appliance that you want to back up.
3. Click File > Export to OVF.
4. Click Save.

## Restoring an Edge appliance in VMware Workstation Pro

1. Click File > Open.
2. Select the Edge appliance that you want to restore and click Open.
3. Click Import. -->