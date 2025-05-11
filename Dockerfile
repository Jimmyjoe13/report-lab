FROM python:3.10-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
# Copier le code de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p /app/output /app/data /app/templates

# Définir la commande par défaut
CMD ["python", "generate_pdf.py"]
