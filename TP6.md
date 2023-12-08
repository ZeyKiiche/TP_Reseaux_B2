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



## IV. Trafic Global System for Mobile communications

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Trafic-Global-System-for-Mobile-communications)

🌞 **Write-up de l'épreuve**
