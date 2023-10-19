# TP1 : Maîtrise réseau du poste

# I. Basics

☀️ **Carte réseau WiFi**

L'adresse MAC de votre carte WiFi : 

```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Adresse physique . . . . . . . . . . . : 84-14-4D-10-5E-AF
```

L'adresse IP de votre carte WiFi :

```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Adresse IPv4. . . . . . . . . . . . . .: 172.20.10.3(préféré)
```

Le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi : 

```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Masque de sous-réseau. . . . . . . . . : 255.255.255.240
```
Et en notation CIDR : ``255.255.255.240/20``

---

☀️ **Déso pas déso**

L'adresse de réseau du LAN auquel vous êtes connectés en WiFi : ``172.20.10.0``

L'adresse de broadcast : ``172.20.10.15``

Le nombre d'adresses IP disponibles dans ce réseau est : ``14``

---

☀️ **Hostname**

Déterminer le hostname de votre PC :

```plaintext
PS C:\Users\maxfe> hostname
SmegMSI
```

---

☀️ **Passerelle du réseau**

L'adresse IP de la passerelle du réseau :
```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
Passerelle par défaut. . . . . . . . . : 172.20.10.1
```

L'adresse MAC de la passerelle du réseau :
```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Adresse physique . . . . . . . . . . . : 84-14-4D-10-5E-AF
```

---

☀️ **Serveur DHCP et DNS**

L'adresse IP du serveur DHCP qui vous a filé une IP :
```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
    Serveur DHCP . . . . . . . . . . . . . : 172.20.10.1
```

L'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet :
```plaintext
PS C:\Users\maxfe> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Serveurs DNS. . .  . . . . . . . . . . : fe80::40c7:11ff:fec6:5064%30
   172.20.10.1
```

---

☀️ **Table de routage**

Dans votre table de routage, laquelle est la route par défaut :
```plaintext
PS C:\Users\maxfe> route print
IPv4 Table de routage
===========================================================================
Itinéraires actifs :
Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
          0.0.0.0          0.0.0.0      172.20.10.1      172.20.10.3     50
```

---

# II. Go further

---

☀️ **Hosts ?**

Faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1` :

```plaintext
PS C:\Windows\System32\drivers\etc> cat hosts
51.75.205.76 kymonovps
1.1.1.1 b2.hello.vous
```


Prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1` :
```plaintext
PS C:\Users\maxfe> ping b2.hello.vous

Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=93 ms TTL=53
Réponse de 1.1.1.1 : octets=32 temps=47 ms TTL=53
Réponse de 1.1.1.1 : octets=32 temps=163 ms TTL=53

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 3, reçus = 3, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 47ms, Maximum = 163ms, Moyenne = 101ms
```

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

![Youtube](/images/Capture_YTB_UDP.png)

L'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo : ``2001:860:de11:22b::d``

Le port du serveur auquel vous êtes connectés : ``443``

Le port que votre PC a ouvert en local pour se connecter au port du serveur distant : ``53103``

---

☀️ **Requêtes DNS**

A quelle adresse IP correspond le nom de domaine `www.ynov.com` :
```plaintext
PS C:\Users\maxfe> nslookup www.ynov.com
Serveur :   UnKnown
Address:  fe80::40c7:11ff:fec6:5064

Réponse ne faisant pas autorité :
Nom :    www.ynov.com
Addresses:  2606:4700:20::681a:ae9
          2606:4700:20::ac43:4ae2
          2606:4700:20::681a:be9
          104.26.10.233
          104.26.11.233
          172.67.74.226
```
Il y a trois adresses IP.

A quel nom de domaine correspond l'IP `174.43.238.89`
```plaintext
PS C:\Users\maxfe> nslookup 174.43.238.89
Serveur :   UnKnown
Address:  fe80::40c7:11ff:fec6:5064

Nom :    89.sub-174-43-238.myvzw.com
Address:  174.43.238.89
```
Le nom de domaine est ``myvzw.com``.

---

☀️ **Hop hop hop**

Par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```plaintext
PS C:\Users\maxfe> tracert www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [2606:4700:20::681a:be9]
avec un maximum de 30 sauts :

  1     1 ms     1 ms     1 ms  2a04:cec0:1121:7e38:ddbb:17ea:94df:72ad
  2     *        *        *     Délai d’attente de la demande dépassé.
  3     *        *        *     Délai d’attente de la demande dépassé.
  4    96 ms    79 ms    26 ms  2001:860:b215:5100::14:4
  5    56 ms    16 ms    19 ms  2001:860:b215:5100::15:2
  6    42 ms    17 ms     *     2001:860:b215:5100::11:4
  7    18 ms    37 ms    15 ms  2001:860:bbe0:192::1
  8    21 ms    25 ms    53 ms  2001:860:bbee:14a::1
  9     *        *        *     Délai d’attente de la demande dépassé.
 10    63 ms    23 ms    33 ms  2400:cb00:538:3::
 11    42 ms    25 ms    26 ms  2606:4700:20::681a:be9

Itinéraire déterminé.
```

---

☀️ **IP publique**

L'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

Je suis en partage de connexion avec mon tél parce que le réseau d'Ynov est kssé ;(

Bref je vais sur ce site : https://www.whatismyip.com/
Et mon IP publique (IPv6) est : ``2a04:cec0:1121:7e38:dc01:cd13:7077:fa98``

---

☀️ **Scan réseau**

Combien il y a de machines dans le LAN auquel vous êtes connectés

```plaintext
PS C:\Users\maxfe> nmap -sn 172.20.10.1-254
Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-12 12:28 Paris, Madrid (heure dÆÚtÚ)
Nmap scan report for 172.20.10.1
Host is up (0.0065s latency).
MAC Address: 42:C7:11:C6:50:64 (Unknown)
Nmap scan report for 172.20.10.3
Host is up.
Stats: 0:00:07 elapsed; 15 hosts completed (2 up), 239 undergoing Ping Scan
Ping Scan Timing: About 2.62% done; ETC: 12:31 (0:03:06 remaining)
Stats: 0:00:11 elapsed; 15 hosts completed (2 up), 239 undergoing Ping Scan
Ping Scan Timing: About 4.71% done; ETC: 12:31 (0:03:02 remaining)
Stats: 0:00:44 elapsed; 15 hosts completed (2 up), 239 undergoing Ping Scan
Ping Scan Timing: About 22.07% done; ETC: 12:31 (0:02:32 remaining)
Stats: 0:01:33 elapsed; 15 hosts completed (2 up), 239 undergoing Ping Scan
Ping Scan Timing: About 47.18% done; ETC: 12:31 (0:01:43 remaining)
Nmap done: 254 IP addresses (2 hosts up) scanned in 197.28 seconds
```

# III. Le requin

☀️ **Capture ARP**

[Capture ARP](/wireshark/arp.pcap)

J'utilise le filtre "arp" dans Wireshark pour mieux voir ce trafic.

---

☀️ **Capture DNS**

[Capture DNS](/wireshark/dns.pcap)

J'utilise la commande `nslookup google.com`
J'utilise le filtre "dns" dans Wireshark pour mieux voir ce trafic.

---

☀️ **Capture TCP**

[Capture TCP](/wireshark/tcp.pcap)

J'utilise le filtre "tcp" dans Wireshark pour mieux voir ce trafic.

---