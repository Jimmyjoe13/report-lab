# Générateur de CV PDF

Ce projet permet de générer un CV en PDF à partir d'un template RML et de données JSON.

## Structure du projet

```
cv-generator/
├── Dockerfile              # Configuration Docker
├── docker-compose.yml      # Configuration Docker Compose
├── requirements.txt        # Dépendances Python
├── generate_pdf.py         # Script principal de génération
├── build_and_run.sh       # Script pour builder et lancer
├── templates/
│   └── cv_template.rml    # Template RML du CV
├── data/
│   └── cv_data.json       # Données du CV en JSON
└── output/                # Dossier des PDFs générés
```

## Installation

### Prérequis
- Docker
- Docker Compose (optionnel)

### Instructions

1. Clonez ou téléchargez ce projet
2. Placez vos données dans `data/cv_data.json`
3. Personnalisez le template dans `templates/cv_template.rml` si nécessaire

## Utilisation

### Méthode 1: Avec Docker Compose

```bash
docker-compose up --build
```

### Méthode 2: Avec le script bash

```bash
chmod +x build_and_run.sh
./build_and_run.sh
```

### Méthode 3: Commandes Docker manuelles

```bash
# Construire l'image
docker build -t cv-generator .

# Exécuter le container
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/templates:/app/templates" \
  -v "$(pwd)/output:/app/output" \
  cv-generator
```

## Personnalisation

### Modification des données
Éditez le fichier `data/cv_data.json` pour modifier les informations du CV.

### Modification du template
Éditez le fichier `templates/cv_template.rml` pour modifier le design du CV. Le format RML est similaire à HTML mais adapté pour générer des PDFs.

## Résultat

Le PDF généré sera disponible dans le dossier `output/` avec un nom de fichier incluant la date et l'heure de génération.

## Dépannage

Si vous rencontrez des problèmes:

1. Vérifiez que Docker est installé et en cours d'exécution
2. Assurez-vous que les dossiers `data`, `templates` et `output` existent
3. Vérifiez les permissions des fichiers
4. Consultez les logs Docker en cas d'erreur

## Technologies utilisées

- Python 3.10
- ReportLab
- RLextra (pour le support RML)
- Docker