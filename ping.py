# on importe la lib scapy
from scapy.all import *

# on craft un ping : c'est de l'ICMP
# type 8 pour ICMP echo request (le ping)
ping = ICMP(type=8)

# on craft un paquet : IP src et IP dst
# 10.33.76.218 : l'IP de mon PC chez moi
# 10.33.77.246 : l'IP de ma box chez moi, ma passerelle
packet = IP(src="10.33.76.218", dst="10.33.77.246")

# on craft une trame : MAC src et MAC dst
# 84:14:4D:10:5E:AF : la MAC de mon PC chez moi
# 98:3b:8f:b4:db:38 : la MAC de ma box chez moi, ma passerelle
frame = Ether(src="84:14:4D:10:5E:AF", dst="98:3b:8f:b4:db:38")

# on emboîte le tout avec le caractère /
final_frame = frame/packet/ping

# srp() c'est pour send & receive
# fonction à utiliser quand on envoie un truc et qu'on attend une réponse
# ici, on envoie un ping et on attend un pong
answers, unanswered_packets = srp(final_frame, timeout=10)

# on a récupéré les pongs dans answers
# et les pings qui n'ont jamais eu de réponses sont dans unanswered_packets
print(f"Pong reçu : {answers[0]}")
