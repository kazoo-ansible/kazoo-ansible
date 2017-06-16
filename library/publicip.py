#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import socket

def get_google_ip():
    try:
        response = open_url('http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
                method='GET', headers={'Metadata-Flavor': 'Google'})
        return response.read()
    except:
        return None

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def main():
    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode=True
    )

    google_ip = get_google_ip()

    if google_ip:
        ip = google_ip
    else:
        ip = get_ip()

    print(json.dumps({
        'changed': False,
        'ansible_facts': {
            'public_ipv4': ip
        }
    }))

if __name__ == '__main__':
    main()

