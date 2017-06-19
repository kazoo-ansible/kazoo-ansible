#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import socket

def get_ip(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((addr, 80))
        return s.getsockname()[0]
    except:
        return None

def main():
    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode=True
    )

    ipv4 = get_ip('8.8.8.8')
    ipv6 = get_ip('2001:4860:4860::8888')

    print(json.dumps({
        'changed': False,
        'ansible_facts': {
            'public_ipv4': ipv4,
            'public_ipv6': ipv6
        }
    }))

if __name__ == '__main__':
    main()

