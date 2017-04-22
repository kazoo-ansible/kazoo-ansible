#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
from urlparse import urlparse

def main():
    module = AnsibleModule(
        argument_spec = dict(
            couchdb_group=dict(required=True, type='list')
        ),
        supports_check_mode=True
    )

    couchdb_group = module.params['couchdb_group']
    
    if not couchdb_group:
        module.fail_json(msg='No hosts specified in supplied couchdb_group.')
    
    node_1 = couchdb_group[0]

    try:
        response = open_url('http://' + node_1 + ':5986/nodes/_all_docs')
        docs = json.loads(response.read())
    except Exception as ex:
        module.fail_json(msg=str(ex))
    
    current_nodes = [urlparse(doc['key']).netloc for doc in docs['rows']]
    
    new_nodes = [host for host in couchdb_group if not host in current_nodes]

    if not new_nodes:
        module.exit_json(changed=False)

    if module.check_mode:
        module.exit_json(changed=True)

    for node in new_nodes:
        try:
            response = open_url('http://' + node_1 + ':5986/nodes', method='POST', \
                    headers={'Content-Type':'application/json'}, data=json.dumps({}))
        except Exception as ex:
            module.fail_json(msg=str(ex))

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()

