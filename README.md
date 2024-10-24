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
```

## 3. Reverse shell

🌞 **Obtenez un reverse shell sur le serveur**

```bash
```

🌞 **Pwn**

/etc/shadow
```bash
```

/etc/passwd
```bash
```

voler le code serveur de l'application
```bash
```

déterminer si d'autres services sont disponibles sur la machine
```bash
```

## II. Remédiation

🌞 **Proposer une remédiation dév**

- le code serveur ne doit pas exécuter n'importe quoi
- il faut préserver la fonctionnalité de l'outil
- **vous devez donc proposer une version mise à jour du code**
  - code serveur ? code client ? les deux
  - les fonctionnalités doivent être préservées
  - les vulnérabilités doivent être fixed

🌞 **Proposer une remédiation système**

- l'environnement dans lequel tourne le service est foireux (le user utilisé ?)
- la machine devrait bloquer les connexions sortantes (pas de reverse shell possible)
- **vous devez donc proposer une suite d'étapes pour empêcher l'exploitation**
  - l'app vulnérable doit fonctionner
  - mais l'exploitation que vous avez utilisé doit être impossible
  - c'est un des jobs de l'admin (et du mec de sécu qui fait des recommandations aux admins) : héberger des apps vulnérables, mais empêcher l'exploitation