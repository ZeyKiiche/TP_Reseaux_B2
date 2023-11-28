import scapy.all as scapy

def handle_packet(packet):
    if len(packet[scapy.Raw].load) == 1:
        print("Caractère caché:", packet[scapy.Raw].load.decode())
        exit()

def icmp_exf_receive():
    print("Sniffing en cours...")
    scapy.sniff(filter="icmp", prn=handle_packet, store=0)
    
icmp_exf_receive()