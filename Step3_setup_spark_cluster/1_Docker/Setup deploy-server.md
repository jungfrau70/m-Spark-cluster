Prerequsites:
- Centos7 with VMWare 
  . 2 core, 
  . 4g RAM, 
  . 100g HDD, 
  . Bridged Network Adapter

#########################################################################################
# 1. Install Docker Engine on CentOS (=deploy-server)
     https://docs.docker.com/engine/install/centos/
#########################################################################################

su -

cat >install-docker.sh<<EOF
yum remove -y docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
rm -rf /var/lib/docker
rm -rf /var/lib/containerd

yum install -y yum-utils
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
yum list docker-ce --showduplicates | sort -r

systemctl start docker
systemctl enable docker.service
systemctl enable containerd.service
docker ps -a
systemctl status docker
netstat -lntp | grep dockerd
EOF

chmod u+x install-docker.sh
./install-docker.sh

docker

## Add docker group, and sudoers
groupadd docker
usermod -aG docker centos  # same id as windows user
newgrp docker 

usermod -aG wheel centos
cat >>/etc/sudoers<<EOF
user_name ALL=(ALL)  ALL
EOF

#########################################################################################
# 2. Install docker-compose 
     https://docs.docker.com/compose/install/
#########################################################################################

cat >install-docker-compose.sh<<EOF
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
EOF

chmod u+x install-docker-compose.sh
./install-docker-compose.sh
docker-compose

#########################################################################################
# 3. Install utils 
#########################################################################################

yum install -y git which wget

## Set hostname of deploy-server
cat >~/etc/hostname<<EOF
deploy-server
EOF

#########################################################################################
# 4. Backup and restore in VMware Workstation Player
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
