#!/usr/bin/python3

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import socket

def get_ip_google():
    try:
        response = open_url('http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
            headers={'Metadata-Flavor': 'Google'}, timeout=1)
        
        return (response.read(), None)
    except:
        return (None, None)

def get_ip_ec2():
    try:
        response = open_url('http://169.254.169.254/latest/meta-data/public-ipv4',
            headers={'Metadata-Flavor': 'Google'}, timeout=1)

        return (response.read(), None)
    except:
        return (None, None)

def get_ip_other():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ipv4 = s.getsockname()[0]
    except:
        ipv4 = None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('2001:4860:4860::8888', 80))
        ipv6 = s.getsockname()[0]
    except:
        ipv6 = None
    
    return (ipv4, ipv6)

def get_ip():
    ipv4 = None
    ipv6 = None
    
    for ip_method in [get_ip_google, get_ip_ec2, get_ip_other]:
        ipv4_result, ipv6_result = ip_method()
        
        if ipv4_result and not ipv4:
            ipv4 = ipv4_result
        
        if ipv6_result and not ipv6:
            ipv6 = ipv6_result
        
        if ipv4 is not None and ipv6 is not None:
            break
    
    return (ipv4, ipv6)


def main():
    module = AnsibleModule(
        argument_spec = dict(),
        supports_check_mode=True
    )

    (ipv4, ipv6) = get_ip()

    print(json.dumps({
        'changed': False,
        'ansible_facts': {
            'public_ipv4': ipv4,
            'public_ipv6': ipv6
        }
    }))

if __name__ == '__main__':
    main()

