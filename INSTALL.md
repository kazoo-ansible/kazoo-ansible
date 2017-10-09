# kazoo-ansible Installation Instruction

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
8. Copy paste the public key created on the Ansible Host
   ```bash
   ssh-rsa AAA...qtb tnewman@kazoo.lan
   ```
9. Modify the permissions of authorized_keys
   ```bash
   chmod 644 ~/.ssh/authorized_keys
   ```
