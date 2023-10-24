# TP2 : Environnement virtuel

## Tableau d'adressage

| Node             | LAN1 `10.1.1.0/24` | LAN2 `10.1.2.0/24` |
| ---------------- | ------------------ | ------------------ |
| `node1.lan1.tp2` | `10.1.1.11`        | x                  |
| `node2.lan1.tp2` | `10.1.1.12`        | x                  |
| `node1.lan2.tp2` | x                  | `10.1.2.11`        |
| `node2.lan2.tp2` | x                  | `10.1.2.12`        |
| `router.tp2`     | `10.1.1.254`       | `10.1.2.254`       |

## Compte-rendu

☀️ Sur **`node1.lan1.tp2`**

- afficher ses cartes réseau

```
[fmaxance@node1lan1tp2tp2 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:e8:08:89 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fee8:889/64 scope link
       valid_lft forever preferred_lft forever
```

- afficher sa table de routage

```
[fmaxance@node1lan1tp2tp2 ~]$ ip route show
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.11 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s8 proto static metric 100
```

- prouvez qu'il peut joindre `node2.lan2.tp2`

```
[fmaxance@node1lan1tp2tp2 ~]$ ping 10.1.2.12
PING 10.1.2.12 (10.1.2.12) 56(84) bytes of data.
64 bytes from 10.1.2.12: icmp_seq=1 ttl=63 time=1.03 ms
64 bytes from 10.1.2.12: icmp_seq=2 ttl=63 time=0.925 ms
64 bytes from 10.1.2.12: icmp_seq=3 ttl=63 time=0.949 ms
64 bytes from 10.1.2.12: icmp_seq=4 ttl=63 time=1.51 ms
^C
--- 10.1.2.12 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 0.925/1.103/1.507/0.236 ms
```

- prouvez avec un `traceroute` que le paquet passe bien par `router.tp2`

```
[fmaxance@node1lan1tp2tp2 ~]$ traceroute 10.1.2.12
traceroute to 10.1.2.12 (10.1.2.12), 30 hops max, 60 byte packets
 1  10.1.1.254 (10.1.1.254)  0.684 ms  0.648 ms  0.638 ms
 2  10.1.2.12 (10.1.2.12)  0.911 ms !X  0.852 ms !X  0.835 ms !X
```

# II. Interlude accès internet

☀️ **Sur `router.tp2`**

- prouvez que vous avez un accès internet (ping d'une IP publique)

```
[fmaxance@routertp2 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=56 time=12.7 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=56 time=14.2 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=56 time=12.9 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=56 time=13.2 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3007ms
rtt min/avg/max/mdev = 12.739/13.264/14.238/0.582 ms
```

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

```
[fmaxance@routertp2 ~]$ ping google.com
PING google.com (142.250.201.174) 56(84) bytes of data.
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=1 ttl=56 time=26.2 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=2 ttl=56 time=27.1 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=3 ttl=56 time=24.9 ms
64 bytes from par21s23-in-f14.1e100.net (142.250.201.174): icmp_seq=4 ttl=56 time=25.0 ms
^C
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3058ms
rtt min/avg/max/mdev = 24.857/25.804/27.141/0.923 ms
```

☀️ **Accès internet LAN1 et LAN2**

- ajoutez une route par défaut sur les deux machines du LAN1

```
[fmaxance@node1lan1tp2tp2 ~]$ sudo ip route add default via 10.1.1.254 dev enp0s8
```

```
[fmaxance@node2lan1tp2 ~]$ sudo ip route add default via 10.1.1.254 dev enp0s8
```

- ajoutez une route par défaut sur les deux machines du LAN2

```
[fmaxance@node1lan2tp2tp2 ~]$ sudo ip route add default via 10.1.2.254 dev enp0s8
```

```
[fmaxance@node2lan2tp2 ~]$ sudo ip route add default via 10.1.2.254 dev enp0s8
```

- configurez l'adresse d'un serveur DNS que vos machines peuvent utiliser pour résoudre des noms

```
[fmaxance@node2lan1tp2 ~]$ cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.12
NETMASK=255.255.255.0

DNS1=8.8.8.8
```

- prouvez que `node2.lan1.tp2` a un accès internet :
  - il peut ping une IP publique

  ```
  [fmaxance@node2lan1tp2 ~]$ ping 8.8.8.8
  PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
  64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=16.1 ms
  64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=17.8 ms
  64 bytes from 8.8.8.8: icmp_seq=3 ttl=113 time=16.5 ms
  64 bytes from 8.8.8.8: icmp_seq=4 ttl=113 time=16.7 ms
  ^C
  --- 8.8.8.8 ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3016ms
  rtt min/avg/max/mdev = 16.102/16.768/17.773/0.618 ms
  ```

  - il peut ping un nom de domaine public

  ```
  [fmaxance@node2lan1tp2 ~]$ ping google.com
  PING google.com (142.250.179.110) 56(84) bytes of data.
  64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=1 ttl=114 time=16.8 ms
  64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=2 ttl=114 time=17.8 ms
  64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=3 ttl=114 time=17.4 ms
  64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=4 ttl=114 time=16.6 ms
  ^C
  --- google.com ping statistics ---
  4 packets transmitted, 4 received, 0% packet loss, time 3098ms
  rtt min/avg/max/mdev = 16.588/17.139/17.757/0.456 ms
  ```

# III. Services réseau

## 1. DHCP

☀️ **Sur `dhcp.lan1.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp2` devient `dhcp.lan1.tp2`)
- changez son adresse IP en `10.1.1.253`

```
[fmaxance@dhcplan1tp2tp2 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
[sudo] password for fmaxance:
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.253
NETMASK=255.255.255.0

DNS1=8.8.8.8
```

- setup du serveur DHCP
  - commande d'installation du paquet

```
[fmaxance@dhcplan1tp2tp2 ~]$ sudo dnf install dhcp-server -y
Rocky Linux 9 - BaseOS                                                                   15 kB/s | 4.1 kB     00:00
Rocky Linux 9 - AppStream                                                                14 kB/s | 4.5 kB     00:00
Rocky Linux 9 - AppStream                                                               6.4 MB/s | 7.1 MB     00:01
Rocky Linux 9 - Extras                                                                   10 kB/s | 2.9 kB     00:00
Dependencies resolved.
...
```

  - fichier de conf

  ```
  [fmaxance@dhcplan1tp2tp2 ~]$ sudo cat dhcpd.conf
  [sudo] password for fmaxance:
  #
  # DHCP Server Configuration file.
  #   see /usr/share/doc/dhcp-server/dhcpd.conf.example
  #   see dhcpd.conf(5) man page



  default-lease-time 900;
  max-lease-time 10800;
  ddns-update-style none;
  authoritative;

  subnet 10.1.1.0 netmask 255.255.255.0 {
    interface enp0s8;
    range 10.1.1.100 10.1.1.200;
    option routers 10.1.1.254;
    option subnet-mask 255.255.255.0;
    option domain-name-servers 8.8.8.8;
  }
  ```

  - service actif

  ```
  [fmaxance@dhcplan1tp2 ~]$ sudo systemctl status dhcpd
  ● dhcpd.service - DHCPv4 Server Daemon
      Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
      Active: active (running) since Mon 2023-10-23 00:04:44 CEST; 14s ago
        Docs: man:dhcpd(8)
              man:dhcpd.conf(5)
    Main PID: 1855 (dhcpd)
      Status: "Dispatching packets..."
        Tasks: 1 (limit: 11051)
      Memory: 5.2M
          CPU: 15ms
      CGroup: /system.slice/dhcpd.service
              └─1855 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid

  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Config file: /etc/dhcp/dhcpd.conf
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Database file: /var/lib/dhcpd/dhcpd.leases
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: PID file: /var/run/dhcpd.pid
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Source compiled to use binary-leases
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Wrote 0 leases to leases file.
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Listening on LPF/enp0s8/08:00:27:35:01:38/10.1.1.0/24
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Sending on   LPF/enp0s8/08:00:27:35:01:38/10.1.1.0/24
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Sending on   Socket/fallback/fallback-net
  Oct 23 00:04:44 dhcplan1tp2 dhcpd[1855]: Server starting service.
  Oct 23 00:04:44 dhcplan1tp2 systemd[1]: Started DHCPv4 Server Daemon.
  ```

☀️ **Sur `node1.lan1.tp2`**

- demandez une IP au serveur DHCP

```
[fmaxance@node1lan1tp2 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
[sudo] password for fmaxance: 
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=dhcp
ONBOOT=yes


DNS1=8.8.8.8

[fmaxance@node1lan1tp2 ~]$ sudo nmcli con reload
[fmaxance@node1lan1tp2 ~]$ sudo nmcli con up enp0s8
```

- prouvez que vous avez bien récupéré une IP *via* le DHCP

```
enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:8c:1d:6f brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.5/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 86044sec preferred_lft 86044sec
    inet6 fe80::a00:27ff:fe8c:1d6f/64 scope link 
       valid_lft forever preferred_lft forever
```

- prouvez que vous avez bien récupéré l'IP de la passerelle

```
[fmaxance@node1lan1tp2 ~]$ ip route show
default via 10.1.1.254 dev enp0s8 
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.5 metric 100 
```

- prouvez que vous pouvez `ping node1.lan2.tp2`

```
[fmaxance@node1lan1tp2 ~]$ ping 10.1.2.11
PING 10.1.2.11 (10.1.2.11) 56(84) bytes of data.
64 bytes from 10.1.2.11: icmp_seq=1 ttl=63 time=1.81 ms
64 bytes from 10.1.2.11: icmp_seq=2 ttl=63 time=2.12 ms
64 bytes from 10.1.2.11: icmp_seq=3 ttl=63 time=2.31 ms
^C
--- 10.1.2.11 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2008ms
rtt min/avg/max/mdev = 1.879/2.138/2.437/0.229 ms
```

## 2. Web web web

☀️ **Sur `web.lan2.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan2.tp2` devient `web.lan2.tp2`)
- setup du service Web
  - installation de NGINX
  
```
[fmaxance@weblan2tp2 ~]$ sudo dnf install nginx -y
```

  - configuration NGINX

```
[fmaxance@weblan2tp2 nginx]$ cat nginx.conf | grep root
      root         /var/www/site_nul/;
```

  - service actif

```
[fmaxance@weblan2tp2 var]$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.
```

  - ouverture du port firewall

```
[fmaxance@weblan2tp2 ~]$ sudo firewall-cmd --add-port=80/tcp --permanent
success
[fmaxance@weblan2tp2 ~]$ sudo firewall-cmd --reload
success
```

- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)

```
[fmaxance@weblan2tp2 nginx]$ ss -altnp
State                    Recv-Q                   Send-Q                                     Local Address:Port                                       Peer Address:Port                   Process                   
LISTEN                   0                        128                                              0.0.0.0:22                                              0.0.0.0:*                                                
LISTEN                   0                        511                                              0.0.0.0:80                                              0.0.0.0:*                                                
LISTEN                   0                        128                                                 [::]:22                                                 [::]:*                                                
LISTEN                   0                        511                                                 [::]:80                    
```

- prouvez que le firewall est bien configuré

```
[fmaxance@weblan2tp2 nginx]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s8
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 80/tcp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: 
```

☀️ **Sur `node1.lan1.tp2`**

- éditez le fichier `hosts` pour que `site_nul.tp2` pointe vers l'IP de `web.lan2.tp2`

```
[fmaxance@node1lan2tp2 ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.2.12   site_nul.tp2
```

- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp2`

```
[fmaxance@node1lan2tp2 ~]$ curl site_nul.tp2
mon site nul
```