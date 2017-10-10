# kazoo-ansible Installation Instruction

## Ansible Host Setup
Complete these steps on the Ansible Host that will run kazoo-ansible.

1. SSH into the Ansible host
   ```bash
   ssh kazoo-ansible.lan
   ```
2. Install prerequisites
   ```bash
   sudo yum install -y git ansible
   ```
3. Generate an SSH key that will be used to manage Kazoo nodes
   ```bash
   ssh-keygen
   Generating public/private rsa key pair.
   Enter file in which to save the key (/home/tnewman/.ssh/id_rsa):
   Created directory '/home/tnewman/.ssh'.
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /home/tnewman/.ssh/id_rsa.
   Your public key has been saved in /home/tnewman/.ssh/id_rsa.pub.
   The key fingerprint is:
   SHA256:pGm0idNfRBpfr0BdQszc/sAxIs8PKlqrAuesmc5cXa4 tnewman@kazoo.lan
   The key's randomart image is:
   +---[RSA 2048]----+
   |        . o*+o.  |
   |         *..*o+  |
   |      . o ++ +.o |
   |     + * . .+.+  |
   |    o B S ...o o |
   |  . .+ +o..   . .|
   |   =. .ooo       |
   | o ++ ...        |
   | .B. .E.         |
   +----[SHA256]-----+
   ```
4. Copy the contents ~/.ssh/id_rsa.pub, so the public key can be used for the 
   Kazoo Node Setup
   ```bash
   cat ~/.ssh/id_rsa.pub
   # Copy this public key to the clipboard
   ssh-rsa AAA...wLX tnewman@kazoo.lan
   ```
5. Clone the kazoo-ansible repo
   ```bash
   cd ~
   git clone https://github.com/kazoo-ansible/kazoo-ansible
   ```
6. Install the latest kazoo-ansible roles
   ```bash
   cd ~/kazoo-ansible
   sudo ansible-galaxy install -r requirements.yml
   ```

## Kazoo Node Setup
Complete these steps on every Kazoo node that will be managed by kazoo-ansible.

1. SSH into the Kazoo node
   ```bash
   ssh kazoo.lan
   ```
2. Open the sudoers file
   ```bash
   sudo visudo
   ```
3. Comment the wheel group line
   ```bash
   ## Allows people in group wheel to run all commands
   # %wheel        ALL=(ALL)       ALL
   ```
4. Uncomment the passwordless wheel group
   ```bash
   ## Same thing without a password
   %wheel  ALL=(ALL)       NOPASSWD: ALL
   ```
5. Save the sudoers file
   ```bash
   :wq<enter>
   ```
6. Create the .ssh directory
   ```bash
   mkdir ~/.ssh
   chmod 644 ~/.ssh
   ```
7. Open the authorized_keys file
   ```bash
   vim ~/.ssh/authorized_keys
   ```
8. Save the authorized_keys file
   ```bash
   :wq<enter>
   ```
9. Copy paste the public key created on the Ansible Host
   ```bash
   # Paste the public key copied to the clipboard above
   ssh-rsa AAA...qtb tnewman@kazoo.lan
   ```
9. Modify the permissions of authorized_keys
   ```bash
   chmod 644 ~/.ssh/authorized_keys
   ```
