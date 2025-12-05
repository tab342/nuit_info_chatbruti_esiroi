# Nuit de l'info Chatbruti TEAM ESIROI

  
- [Nuit de l'info Chatbruti TEAM ESIROI](#nuit-de-linfo-chatbruti-team-esiroi)
  - [Résumé](#résumé)
  - [Installation](#installation)
  - [Utilisation](#utilisation)
    - [Linux/Mac:](#linuxmac)
    - [Windows:](#windows)
  - [Fonctionnement](#fonctionnement)



Résumé
------

Un petit projet ludique: un "chatbot idiot" — un agent volontairement simpliste et caricatural conçu pour des expérimentations, de l'amusement ou des démonstrations pédagogiques. Il répond de façon naïve, répétitive ou absurde selon une personnalité définie.

Installation
------------

Cloner le dépôt:

```bash
git clone https://github.com/tab342/nuit_info_chatbruti_esiroi
cd nuit_info_chatbruti_esiroi
```

## Utilisation

### Linux/Mac:
Lancer le script `chatbruti.sh`\
Toutes les dépendences et le lancement local de l'IA sont installées par lui.

### Windows:
Il est à noter que ce projet a été fait sous linux et mac uniquement, aucun des membres de l'équipe ne possédant un ordinateur windows disponible. Cependant, la méthode suivante est *théoriquement* sensé fonctionner:
1. Dans une console PowerShell, rendre les fichiers PowerShell éxecutables pour cette session:
```ps
Set-ExecutionPolicy -Scope Process Bypass
```
2. Lancer le script `chatbruti.ps1`

## Fonctionnement
Pour avoir un projet un maximum pratique et responsable, nous avons décidé d'héberger l'IA de Chat'bruti localement sur la machine de l'utilisateur. Lors de la première utilisation, tous les prérequis seront téléchargés, puis l'IA fonctionnera de manière complètement autonome.\
Comme méthode pour rendre le chatbot idiot, et le plus drôle possible, nous avons décidé de faire un traitement de prompt en deux étapes: d'abord, la requète est envoyée à l'IA avec un prompt très spécifique lui demandant de ne pas y répondre, mais de le modifier, en gardant le sujet de la phrase mais en modifiant verbes et compléments. Ensuite, cette requète modifiée est renvoyée à l'IA, cette fois-ci en lui demandant d'y répondre. De cette façon, l'IA répond plus ou moins sur le sujet (parfois même à la bonne question, si le 1er prompt renvoie une question très peu modifiée), mais souvent très décalé. La partie la plus drôle est souvent de se demander comment, au juste, il a pu déformer la question pour arriver à un résultat.

