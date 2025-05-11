#!/bin/bash

# Script de démarrage pour Railway

# Créer les dossiers nécessaires
mkdir -p templates data output

# Copier le template RML s'il n'existe pas
if [ ! -f templates/cv_template.rml ]; then
    cp cv_template.rml templates/
fi

# Démarrer l'application avec Gunicorn
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120