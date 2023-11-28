from scapy.all import *


dns_server = "8.8.8.8"  
query_domain = "ynov.com"

dns_request = Ether()/IP(dst=dns_server)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=query_domain))
response, nullresp = srp(dns_request, timeout=2, verbose=False)

data_response = response[0][1]
print(data_response)