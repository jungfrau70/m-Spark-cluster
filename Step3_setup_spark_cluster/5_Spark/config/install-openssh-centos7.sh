#!/bin/bash
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
