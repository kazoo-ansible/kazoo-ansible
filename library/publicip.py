#!/usr/bin/python3

from six.moves.urllib import request
import json
import socket

def main():
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

def get_google_ip():
    try:
        req = request.Request('http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip')
        req.add_header('Metadata-Flavor', 'Google')
        return request.urlopen(req).read()
    except:
        return None

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == '__main__':
    main()

