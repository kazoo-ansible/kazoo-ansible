#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json

DBs = ['_users', '_replicator', '_global_changes']

def main():
    module = AnsibleModule(
        argument_spec = dict(
            current_node=dict(required=True, type='str'),
            couch_user=dict(required=True, type='str'),
            couch_password=dict(required=True, type='str', no_log=True),
        ),
        supports_check_mode=True
    )
    
    current_node = module.params['current_node']
    couch_user = module.params['couch_user']
    couch_password = module.params['couch_password']

    try:
        missing_dbs = get_missing_dbs(current_node, couch_user, couch_password)
    
        if not missing_dbs:
            module.exit_json(changed=False)
    
        if module.check_mode:
            module.exit_json(changed=True)
    
        create_dbs(current_node, couch_user, couch_password, missing_dbs)
    except Exception as ex:
	module.fail_json(msg=str(ex))
    
    module.exit_json(changed=True)

def get_missing_dbs(current_node, couch_user, couch_password):
    missing_dbs = []
    
    for db in DBs: 
        try:
            response = open_url('http://' + couch_user + ':' + \
                    couch_password + '@' + current_node + ':5984/' + \
                    db, force_basic_auth=True)
        except Exception as ex:
            if '404' in str(ex):
                missing_dbs.append(db)
            else:
                raise(ex)
    
    return missing_dbs

def create_dbs(current_node, couch_user, couch_password, missing_dbs):
    for db in missing_dbs:
        try:
            response = open_url('http://' + couch_user + ':' + \
                    couch_password + '@'+ current_node + ':5984/' + \
                    db, method='PUT', data=json.dumps({}), force_basic_auth=True)
        except Exception as ex:
            if '412' in str(ex):
                # Ignore race condition in DB creation
                pass
            else:
                raise ex

if __name__ == '__main__':
    main()

