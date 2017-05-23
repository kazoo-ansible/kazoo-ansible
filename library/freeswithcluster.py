#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
from subprocess import Popen, PIPE, STDOUT

def main():
    module = AnsibleModule(
        argument_spec = dict(
            erlang_cookie = dict(required=True, type='str'),
            freeswitch_hosts = dict(required=True, type='list')
        ),
        supports_check_mode=True
    )

    p = Popen(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'list_fs_nodes'],\
            stdout=PIPE, stderr=PIPE)
    out, error = p.communicate()

    if p.returncode:
        module.fail_json(msg=error)

    existing_hosts = [line.replace('freeswitch@', '') for line in out.splitlines()]

    freeswitch_hosts = module.params['freeswitch_hosts']

    new_hosts = [host for host in freeswitch_hosts if host not in existing_hosts]

    if module.check_mode:
        module.exit_json(changed=len(new_hosts) != 0)

    for host in new_hosts:
        p = Popen(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'add_fs_node',\
                'freeswitch@' + host], stdout=PIPE, stderr=PIPE)
        out, error = p.communicate()

        if p.returncode:
            if error != '{error,node_exists}':
                module.fail_json(msg=error)

    module.exit_json(changed=len(new_hosts) != 0)

if __name__ == '__main__':
    main()

