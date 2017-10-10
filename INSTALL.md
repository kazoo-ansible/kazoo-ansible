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
7. Edit /etc/ansible/hosts (Hint: Press i for insert mode and Escape for command mode)
   ```bash
   sudo vi /etc/ansible/hosts
   ```
8. Modify hosts based on your cluster configuration (these are merely suggested configurations)
   ```ini
   # Single node cluster
   [kazoo]
   kazoo.lan
   
   [monsterui]
   kazoo.lan
   
   [couchdb]
   kazoo.lan
   
   [rabbitmq]
   kazoo.lan
   
   [kamailio]
   kazoo.lan
   
   [freeswitch]
   kazoo.lan
   
   # Multiple node cluster
   [kazoo]
   kazoo1.lan
   kazoo2.lan
   kazoo3.lan
   
   [monsterui]
   kazoo1.lan
   kazoo2.lan
   kazoo3.lan
   
   [couchdb]
   kazoo1.lan
   kazoo2.lan
   kazoo3.lan
   
   [rabbitmq]
   kazoo1.lan
   kazoo2.lan
   
   [kamailio]
   kazoo1.lan
   kazoo2.lan
   kazoo3.lan
   
   [freeswitch]
   kazoo1.lan
   kazoo2.lan
   kazoo3.lan
   ```
9. Save hosts
   ```bash
   :wq<enter>
   ```
10. Edit group_vars/all (Hint: Press i for insert mode and Escape for command mode)
    ```bash
    vi group_vars/all
    ```
11. Modify group_vars based on your cluster configuration
    ```yaml
    ---
    # The domain used to access Monster UI
    kazoo_domain: kazoo.lan
    
    # Enables Let's Encrypt. Set to no to manage TLS certificates manually
    kazoo_enable_lets_encrypt: yes
    
    # Usernames that can either be left alone or changed
    couch_user: couchdb
    rabbitmq_user: rabbitmq
    
    # Passwords and cookies that should definitely be changed
    erlang_cookie: changeme
    rabbitmq_password: changeme
    couch_password: changeme
    
    # Manually-managed TLS certificate to secure Crossbar and MonsterUI if 
    # Let's Encrypt is disabled
    kazoo_tls_certificate: |
      -----BEGIN CERTIFICATE-----
      Your certificate here!
      -----END CERTIFICATE-----
    kazoo_tls_private_key: |
      -----BEGIN PRIVATE KEY-----
      Your private key here
      -----END PRIVATE KEY-----
    ```
12. Save group_vars
    ```bash
    :wq<enter>
    ```

## Kazoo Node Setup
Complete these steps on every Kazoo node that will be managed by kazoo-ansible.

1. SSH into the Kazoo node
   ```bash
   ssh kazoo.lan
   ```
2. Open the sudoers file (Hint: Press i for insert mode and Escape for command mode)
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
   chmod 700 ~/.ssh
   ```
7. Open the authorized_keys file (Hint: Press i for insert mode and Escape for command mode)
   ```bash
   vi ~/.ssh/authorized_keys
   ```
8. Copy paste the public key created on the Ansible Host
   ```bash
   # Paste the public key copied to the clipboard above
   ssh-rsa AAA...qtb tnewman@kazoo.lan
   ```
9. Save the authorized_keys file
   ```bash
   :wq<enter>
   ```
10. Modify the permissions of authorized_keys
    ```bash
    chmod 644 ~/.ssh/authorized_keys
    ```

## Running kazoo-ansible Playbook
1. SSH into the Ansible host
   ```bash
   ssh kazoo-ansible.lan
   ```
2. Run the kazoo-ansible Ansible Playbook
   ```bash
   cd ~/kazoo-ansible
   ansible-playbook site.yml
   ```

## Post Playbook Steps
1. SSH into one of the Kazoo nodes with the kazoo role
   ```bash
   ssh kazoo.lan
   ```
2. Import FreeSwitch Media
   ```bash
   # EN-US prompts
   sup kazoo_media_maintenance import_prompts /opt/kazoo/sounds/en/us/
   
   # Add additional prompts as needed
   # sup kazoo_media_maintenance import_prompts /opt/kazoo/sounds/fr/ca fr-ca
   ```
3. Create the Kazoo Master Administrator Account
   ```bash
   # Create an account with your own account name, realm, username, and password
   sup crossbar_maintenance create_account YOUR_ACCOUNT_NAME YOUR_REALM YOUR_USERNAME YOUR_PASSWORD
   ```
4. Initialize MonsterUI Applications
   ```bash
   # Initialize MonsterUI using the Kazoo domain set in group_vars/all
   sup crossbar_maintenance init_apps /var/www/html/monster-ui/apps https://kazoo_domain.lan/crossbar/v2
   ```
