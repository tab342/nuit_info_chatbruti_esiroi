# Nuit de l'info — Chatbruti TEAM ESIROI

- [Résumé](#résumé)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnement](#fonctionnement)
  - [Architecture générale](#architecture-générale)
  - [Modification automatique du prompt](#modification-automatique-du-prompt)
  - [Détection automatique de questions](#détection-automatique-de-questions)
  - [Génération de réponses idiotes](#génération-de-réponses-idiotes)
  - [Mode normal : réponse en deux étapes](#mode-normal--réponse-en-deux-étapes)
  - [Version avec historique](#version-avec-historique)
  - [Version personnalisée](#version-personnalisée)
- [Commandes disponibles](#commandes-disponibles)
- [Notes & bonnes pratiques](#notes--bonnes-pratiques)
- [Contribuer / Dépannage](#contribuer--dépannage)

---

## Résumé

Ceci est la version locale et CLI du projet **Chat'bruti** de la nuit de l'info 2025 : un chatbot volontairement idiot basé sur un modèle local (via Ollama — ex. Gemma).  
Le bot produit des réponses absurdes, fausses, répétitives ou caricaturales — parfois en créole — avec pour but l’expérimentation, l’humour et la pédagogie autour des LLM locaux.

---

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/tab342/nuit_info_chatbruti_esiroi
cd nuit_info_chatbruti_esiroi
```
### ⚠️ Note pour distributions Debian / Ubuntu

Pour pouvoir créer un environnement virtuel Python 3.13 sur les distros Debian-based, installez le package suivant :
```bash
sudo apt install python3.13-venv
```
## Utilisation
Lancer le script `chatbruti.sh`\
Ce script automatise les étapes suivantes :
- création d'un venv Python
- installation des dépendances nécessaires (requests, etc.)
- vérification et installation d'Ollama si nécessaire
- vérification si le modèle IA est déjà pull (évite un re-pull inutile)
- démarrage du serveur Ollama (ollama serve)
- lancement du chatbot Python
- arrêt propre du serveur Ollama à la fin du script

## Fonctionnement

Chat'bruti CLI fonctionne entièrement en local via Ollama. Le comportement du bot est obtenu par une première requète de transformation de prompt pour déformer la requète, puis une seconde pour répondre à la requète déformée, ce qui donne des résultats complètement décalés et souvent surprenants.
