from scapy.all import sniff

def print_it_please(packet):
    packet_source_ip = packet['IP'].src
    packet_dest_ip = packet['IP'].dst
    packet_source_tcp = packet['TCP'].sport
    packet_dest_tcp = packet['TCP'].dport
    print("TCP SYN ACK reçu !")
    print(f"- Adresse IP src : {packet_source_ip}")
    print(f"- Adresse IP dst : {packet_dest_ip}")
    print(f"- Port TCP src : {packet_source_tcp}")
    print(f"- Port TCP dst : {packet_dest_tcp}")

sniff(filter="tcp", prn=print_it_please, count=1)
