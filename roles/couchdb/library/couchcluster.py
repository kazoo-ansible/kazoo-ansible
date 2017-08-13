#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import socket

def main():
    module = AnsibleModule(
        argument_spec = dict(
            current_node=dict(required=True, type='str'),
            node_1=dict(required=True, type='str'),
            couch_user=dict(required=True, type='str'),
            couch_password=dict(required=True, type='str', no_log=True),
        ),
        supports_check_mode=True
    )

    node_1 = module.params['node_1']
    current_node = 'couchdb@' + module.params['current_node']
    couch_user = module.params['couch_user']
    couch_password = module.params['couch_password']

    try:
        response = open_url('http://' + couch_user + ':' + \
                couch_password + '@' + node_1 + ':5984/_membership', \
                force_basic_auth=True)
        docs = json.loads(response.read())
        nodes = docs['cluster_nodes']
    except Exception as ex:
        module.fail_json(msg=str(ex))
    
    if current_node in nodes:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)
    
    try:
        response = open_url('http://' + couch_user + ':' + couch_password + \
                '@' + node_1 + ':5986/_nodes/' + current_node, method='PUT', \
                data=json.dumps({}), force_basic_auth=True)
    except Exception as ex:
        module.fail_json(msg=str(ex))

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()

