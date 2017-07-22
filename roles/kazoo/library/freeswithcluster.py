#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import sup

def main():
    module = AnsibleModule(
        argument_spec = dict(
            erlang_cookie = dict(required=True, type='str'),
            freeswitch_hosts = dict(required=True, type='list')
        ),
        supports_check_mode=True
    )

    erlang_cookie = module.params['erlang_cookie']
    freeswitch_hosts = module.params['freeswitch_hosts']

    try:
        existing_hosts = sup.get_fs_nodes(erlang_cookie)

        new_hosts = [host for host in freeswitch_hosts if host not in existing_hosts]
        extra_hosts = [host for host in existing_hosts if host not in freeswitch_hosts]

        changed = len(new_hosts) + len(extra_hosts) != 0

        if module.check_mode:
            module.exit_json(changed=changed)

        for host in new_hosts:
            sup.add_fs_node(erlang_cookie, host)

        for host in extra_hosts:
            sup.remove_fs_node(erlang_cookie, host)

        module.exit_json(changed=changed)

    except IOError as error:
        module.fail_json(msg=error)

if __name__ == '__main__':
    main()

