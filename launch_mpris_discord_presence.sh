#!/bin/bash

# Attend 30 secondes avant de lancer le script
sleep 30

# Définit le chemin d'accès au répertoire contenant ce script de lancement
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Construit le chemin d'accès au script Python
PYTHON_SCRIPT_PATH="$SCRIPT_DIR/main.py"

# Exécutez votre script Python
/bin/python "$PYTHON_SCRIPT_PATH"