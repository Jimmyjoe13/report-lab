#!/bin/bash

# Script de démarrage pour Railway

# Afficher des informations de débogage
echo "Starting application..."
echo "Current directory: $(pwd)"
echo "PORT environment variable: $PORT"

# Créer les dossiers nécessaires
mkdir -p templates data output
echo "Created necessary directories"

# Copier le template RML s'il n'existe pas
if [ ! -f templates/cv_template.rml ]; then
    cp cv_template.rml templates/
    echo "Copied cv_template.rml to templates directory"
fi

# Vérifier les fichiers
echo "Files in current directory: $(ls -la)"
echo "Files in templates directory: $(ls -la templates)"

# Vérifier les permissions
chmod -R 777 templates output data
echo "Set permissions on directories"

# Vérifier l'installation de Python et des dépendances
python --version
pip list | grep reportlab
pip list | grep flask
echo "Python and dependencies verified"

# Vérifier et définir le port
if [ -z "$PORT" ]; then
    export PORT=8080
    echo "PORT was not set, defaulting to 8080"
else
    echo "PORT is set to $PORT"
fi

# Démarrer l'application avec Gunicorn
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn app:app --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 120 --log-level debug
