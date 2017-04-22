#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import socket

def main():
    module = AnsibleModule(
        argument_spec = dict(
            node_1=dict(required=True, type='str')
        ),
        supports_check_mode=True
    )

    node_1 = module.params['node_1']
    current_node = 'bigcouch@' + socket.gethostname()

    try:
        response = open_url('http://' + node_1 + ':5986/nodes/_all_docs')
        docs = json.loads(response.read())
    except Exception as ex:
        module.fail_json(msg=str(ex))
    
    nodes = [doc['key'] for doc in docs['rows']]

    if current_node in nodes:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)
    
    try:
        response = open_url('http://' + node_1 + ':5986/nodes/bigcouch@' + node, method='PUT', \
                headers={'Content-Type':'application/json'}, data=json.dumps({}))
    except Exception as ex:
        module.fail_json(msg=str(ex))

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()

