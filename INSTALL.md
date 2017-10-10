# kazoo-ansible Installation Instruction

## Setup
Complete these steps on the Ansible Host that will run kazoo-ansible.

1. SSH into the Ansible host
   ```bash
   $ ssh kazoo-ansible.lan
   ```
2. Bootstrap the Ansible host
   ```bash
   $ bash <(curl -s https://raw.githubusercontent.com/kazoo-ansible/kazoo-ansible/master/ansible_host_bootstrap.sh)
   ```
3. Edit /etc/ansible/hosts (Hint: Press i for insert mode and Escape for command mode)
   ```bash
   $ sudo vi /etc/ansible/hosts
   ```
4. Modify hosts based on your cluster configuration (these are merely suggested configurations)
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
5. Save hosts
   ```bash
   :wq<enter>
   ```
6. Edit group_vars/all (Hint: Press i for insert mode and Escape for command mode)
   ```bash
   $ vi group_vars/all
   ```
7. Modify group_vars based on your cluster configuration
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
8. Save group_vars
   ```bash
   :wq<enter>
   ```
9. SSH into each Kazoo node to cache the password in known_hosts
   ```bash
   $ ssh kazoo.lan
   The authenticity of host 'kazoo.lan (127.0.0.1)' can't be established.
   ECDSA key fingerprint is SHA256:JtNSVrHMsgGAdFoek0R15Gm0Pjczi3kMOTgNSic0dq4.
   ECDSA key fingerprint is MD5:6d:07:fc:a4:36:ac:89:23:5e:e6:a6:8d:1e:e6:fe:8d.
   Are you sure you want to continue connecting (yes/no)? yes
   Warning: Permanently added 'kazoo.lan' (ECDSA) to the list of known hosts.
   Last login: Tue Oct 10 02:46:40 2017 from cnd4220hd2.lan
   $ logout
   ```
10. Bootstrap the Kazoo nodes
    ```bash
    $ ansible-playbook bootstrap.yml --ask-pass --ask-sudo-pass
    SSH password:
    SUDO password[defaults to SSH password]:
    ```
## Running kazoo-ansible Playbook
1. SSH into the Ansible host
   ```bash
   $ ssh kazoo-ansible.lan
   ```
2. Run the kazoo-ansible Ansible Playbook
   ```bash
   $ cd ~/kazoo-ansible
   $ ansible-playbook site.yml
   ```

## Post Playbook Steps
1. SSH into one of the Kazoo nodes with the kazoo role
   ```bash
   $ ssh kazoo.lan
   ```
2. Import FreeSwitch Media
   ```bash
   # EN-US prompts
   $ sup kazoo_media_maintenance import_prompts /opt/kazoo/sounds/en/us/
   
   # Add additional prompts as needed
   # sup kazoo_media_maintenance import_prompts /opt/kazoo/sounds/fr/ca fr-ca
   ```
3. Create the Kazoo Master Administrator Account
   ```bash
   # Create an account with your own account name, realm, username, and password
   $ sup crossbar_maintenance create_account YOUR_ACCOUNT_NAME YOUR_REALM YOUR_USERNAME YOUR_PASSWORD
   ```
4. Initialize MonsterUI Applications
   ```bash
   # Initialize MonsterUI using the Kazoo domain set in group_vars/all
   $ sup crossbar_maintenance init_apps /var/www/html/monster-ui/apps https://kazoo_domain.lan/crossbar/v2
   ```

