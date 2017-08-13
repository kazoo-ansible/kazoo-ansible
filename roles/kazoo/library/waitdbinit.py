#!/usr/bin/python3

from ansible.module_utils.basic import *
import ansible.module_utils.urls

KAZOO_DBS = ['accounts', 'acdc', 'alerts' , 'anonymous_cdrs', \
        'dedicated_ips', 'faxes', 'global_provisioner', 'oauth', \
        'offnet', 'pending_notifications', 'port_requests', 'ratedeck', \
        'services', 'sip_auth', 'system_auth', 'system_config', 'system_data', \
        'system_media', 'system_schemas', 'tasks', 'token_auth', 'webhooks']

open_url = ansible.module_utils.urls.open_url

def main():
    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode = True
    )

    while True:
        try:
            response = open_url('http://localhost:15984/_all_dbs')
            dbs = json.loads(response.read())
        except Exception as ex:
            module.fail_json(msg=str(ex))

        if set(KAZOO_DBS).issubset(set(dbs)):
            break

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()

