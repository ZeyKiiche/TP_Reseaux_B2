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

- capture Wireshark de votre `nmap`
- je ne veux voir que les trames envoyées/reçues par `nmap` dans la capture

🌞 **Connectez-vous au serveur**

- éditer le code du client pour qu'il se connecte à la bonne IP et au bon port
- utilisez l'application !
- vous devez déterminer, si c'est pas déjà fait, à quoi sert l'application

## 2. Exploit

➜ **On est face à une application qui, d'une façon ou d'une autre, prend ce que le user saisit, et l'évalue.**

Ca doit lever un giga red flag dans votre esprit de hacker ça. Tu saisis ce que tu veux, et le serveur le lit et l'interprète.

🌞 **Injecter du code serveur**

- démerdez-vous pour arriver à faire exécuter du code arbitraire au serveur
- tu sais comment te co au serveur, et tu sais que ce que tu lui envoies, il l'évalue
- vous pouvez normalement avoir une injection de code :
  - exécuter du code Python
  - et normalement, exécuter des commandes shell depuis cette injection Python

## 3. Reverse shell

➜ **Injecter du code c'est bien mais...**

- souvent c'est ***chiant*** si on veut vraiment prendre le contrôle du serveur
- genre ici, à chaque commande, faut lancer une connexion au serveur étou, relou
- on pourrait lancer un serveur à nous sur la machine, et s'y connecter, mais s'il y a un firewall, c'est niquéd
- ***reverse shell* à la rescousse** : l'idée c'est de lancer un shell sur le serveur victime

> C'est *comme* une session SSH, mais c'est à la main, et c'est le serveur qui se connecte à toi pour que toi tu aies le shell. Genre c'est l'inverse de d'habitude. D'où le nom : *reverse* shell.

➜ **Pour pop un reverse shell**

- **en premier**
  - sur une machine que tu contrôles
  - tu lances un programme en écoute sur un port donné
  - un ptit `nc -lvp 9999` par exemple
- **en deuxième**
  - sur la machine où tu veux un shell, là où t'as de l'injection de code
  - tu demandes à l'OS d'ouvrir un port, et de se connecter à ton port ouvert sur la machine que tu contrôles
  - tu lances un shell (`bash` par exemple)
  - ce `bash` va "s'accrocher" à la session TCP
- **enfin**
  - tu retournes sur la machine que tu contrôles
  - et normalement, dans ta session `nc -lvp 9999`, t'as un shell qui a pop

➜ **Long story short**

- une commande sur une machine que tu contrôles
- une commande injectée sur le serveur victime
- t'as un shell sur le serveur victime depuis la machine que tu contrôles

> Quand tu commences à être bon en bash/réseau étou tu peux pondre ça tout seul. Mais sinon, on se contente de copier des commandes trouvées sur internet c'est très bien.

🌞 **Obtenez un reverse shell sur le serveur**

- si t'as injection de code, t'as sûrement possibilité de pop un reverse shell
- y'a plein d'exemple sur [le très bon hacktricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells/linux)

🌞 **Pwn**

- voler les fichiers `/etc/shadow` et `/etc/passwd`
- voler le code serveur de l'application
- déterminer si d'autres services sont disponibles sur la machine

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
