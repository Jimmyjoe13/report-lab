#!/bin/bash

# Script pour construire et exécuter le générateur de CV

echo "🚀 Construction de l'image Docker..."
docker build -t cv-generator .

echo "📝 Génération du PDF..."
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/templates:/app/templates" \
  -v "$(pwd)/output:/app/output" \
  cv-generator

echo "✅ PDF généré dans le dossier output/"