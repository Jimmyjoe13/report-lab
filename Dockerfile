FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p /app/output /app/data /app/templates

# Copier le template RML dans le bon dossier
RUN if [ -f cv_template.rml ]; then cp cv_template.rml templates/; fi

# Rendre le script exécutable
RUN chmod +x startup.sh

# Variables d'environnement par défaut
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Exposer le port
EXPOSE 8080

# Utiliser startup.sh comme point d'entrée
CMD ["./startup.sh"]