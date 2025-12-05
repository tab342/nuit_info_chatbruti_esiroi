#!/usr/bin/env bash

set -e

### --- Fonctions --- ###

cleanup() {
    echo "[*] Arrêt du serveur Ollama..."
    pkill -f "ollama serve" || true
    exit 0
}

#trap cleanup INT TERM EXIT


echo "[*] Vérification d'Ollama..."

if ! command -v ollama >/dev/null 2>&1; then
    echo "[!] Ollama non installé. Installation..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[✔] Ollama est déjà installé."
fi

echo "[*] (Re)démarrage du serveur Ollama..."
pkill -f "ollama serve" 2>/dev/null || true

nohup ollama serve >/dev/null 2>&1 &
sleep 2

MODEL="gemma3:1b"

echo "[*] Vérification du modèle '$MODEL'..."

if ollama list | grep -q "^$MODEL"; then
    echo "[✔] Modèle '$MODEL' déjà présent."
else
    echo "[*] Modèle absent, téléchargement..."
    ollama pull "$MODEL"
fi

echo "[*] Préparation de l'environnement Python..."

if [ ! -d ".venv" ]; then
    echo "[*] Création d'un venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if ! python3 -c "import requests" >/dev/null 2>&1; then
    echo "[*] Installation de la bibliothèque 'requests'..."
    pip install --quiet requests
fi

if [ ! -f "test.py" ]; then
    echo "[❌] test.py introuvable dans le dossier courant."
    exit 1
fi

echo "[*] Exécution de test.py..."
python3 test.py

cleanup
