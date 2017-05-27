#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
from subprocess import Popen, PIPE, STDOUT
import re

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


    p = Popen(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls',\
            'acl_summary'], stdout=PIPE, stderr=PIPE)
    out, error = p.communicate()

    if p.returncode:
        module.fail_json(msg=error)

    existing_ips = [match[1] for match in re.findall(regex, out)]
    kamailio_ips = module.params['kamailio_ips']

    new_ips = [ip for ip in kamailio_ips if ip not in existing_ips]

    if module.check_mode:
        module.exit_json(changed=len(new_ips) != 0)

    for ip in new_ips:
        p = Popen(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'allow_sbc',\
                ip, ip], stdout=PIPE, stderr=PIPE)
        out, error = p.communicate()

        if p.returncode:
            module.fail_json(msg=error)

    module.exit_json(changed=len(new_ips) != 0)

if __name__ == '__main__':
    main()

