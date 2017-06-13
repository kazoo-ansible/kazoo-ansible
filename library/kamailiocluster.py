#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
from subprocess import Popen, PIPE, STDOUT
import re
import sup

def main():
    module = AnsibleModule(
        argument_spec = dict(
            erlang_cookie = dict(required=True, type='str'),
            kamailio_ips = dict(required=True, type='list')
        ),
        supports_check_mode=True
    )

    # Matches Name  |  IP
    regex = re.compile(r'(\S+)\s*?\|\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\/\d+', re.MULTILINE)

    cookie = module.params['erlang_cookie']

    try:
        existing_ips = sup.get_sbc_acls(cookie)
        kamailio_ips = module.params['kamailio_ips']

        new_ips = [ip for ip in kamailio_ips if ip not in existing_ips]
        extra_ips = [ip for ip in existing_ips if ip not in kamailio_ips]

        changed = len(new_ips) + len(extra_ips) != 0

        if module.check_mode:
            module.exit_json(changed=changed)

        for ip in extra_ips:
            sup.remove_sbc_acl(cookie, ip)

        for ip in new_ips:
            sup.add_sbc_acl(cookie, ip)

        module.exit_json(changed=changed)

    except IOError as error:
        module.fail_json(msg=error.value)
    
if __name__ == '__main__':
    main()

