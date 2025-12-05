#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"


function Cleanup {
    Write-Host "[*] Arrêt du serveur Ollama..."
    Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}

$cancelEvent = Register-EngineEvent PowerShell.Exiting -Action { Cleanup }


Write-Host "[*] Vérification d'Ollama..."

if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Ollama non installé. Installation..."

    $installer = "$env:TEMP\ollama-installer.exe"
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer

    Write-Host "[*] Exécution de l'installateur..."
    Start-Process $installer -Wait
}
else {
    Write-Host "[✔] Ollama déjà installé."
}


Write-Host "[*] (Re)démarrage du serveur Ollama..."

Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Process "ollama" "serve" -WindowStyle Hidden
Start-Sleep -Seconds 2


$model = "gemma3:1b"
Write-Host "[*] Vérification du modèle '$model'..."

$models = ollama list

if ($models -match "^$model") {
    Write-Host "[✔] Modèle déjà présent."
} else {
    Write-Host "[*] Modèle absent, téléchargement..."
    ollama pull $model
}


Write-Host "[*] Préparation de l'environnement Python..."

if (!(Test-Path ".\.venv")) {
    Write-Host "[*] Création d'un venv..."
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

try {
    python -c "import requests" 2>$null
} catch {
    Write-Host "[*] Installation de requests..."
    pip install requests | Out-Null
}

if (!(Test-Path ".\test.py")) {
    Write-Host "[X] test.py introuvable."
    Cleanup
    exit 1
}

Write-Host "[*] Exécution de test.py..."

python test.py
$exitCode = $LASTEXITCODE

Cleanup
exit $exitCode
