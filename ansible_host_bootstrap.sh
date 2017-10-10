#!/bin/bash
set -e

echo " #  #  ##  #### #### #### "
echo " # #  #  #    # #  # #  # "
echo " ##   ####  ##  #  # #  # "
echo " # #  #  # #    #  # #  # "
echo " #  # #  # #### #### #### "
echo "    Ansible  Bootstrap    "
echo ""

echo "Installing Prerequisites"
sudo yum install -y git ansible

echo "Cloning kazoo-ansible Repository"
git clone https://github.com/kazoo-ansible/kazoo-ansible ~/kazoo-ansible

echo "Installing kazoo-ansible Roles"
sudo ansible-galaxy install -r ~/kazoo-ansible/requirements.yml

if [[ -f ~/.ssh/id_rsa && -f ~/.ssh/id_rsa.pub ]]; then
    echo "SSH keypair exists. Skipping..."
else
    echo "Generating SSH keypair"
    ssh-keygen -f ~/.ssh/id_rsa -t rsa -N ''
fi

cd ~/kazoo-ansible

