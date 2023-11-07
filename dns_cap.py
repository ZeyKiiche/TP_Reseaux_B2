from scapy.all import *

def dns_response(packet):
    if DNSRR in packet and packet[DNS].qr == 1:
        print(packet[DNSRR].rdata)

sniff(filter="udp port 53", prn=dns_response)
