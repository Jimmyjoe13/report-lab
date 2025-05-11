# Déploiement sur Railway.app

Ce guide explique comment déployer le générateur de CV PDF sur Railway.app.

## Prérequis

- Un compte Railway.app
- Git installé localement
- Le code source du projet

## Structure du projet pour Railway

```
cv-generator/
├── app.py                  # Application Flask principale
├── generate_pdf.py         # Module de génération PDF
├── cv_template.rml        # Template RML
├── requirements.txt       # Dépendances Python
├── railway.json          # Configuration Railway
├── Procfile              # Configuration du processus
├── startup.sh           # Script de démarrage
└── .env.example         # Exemple de variables d'environnement
```

## Étapes de déploiement

### 1. Préparer le projet

1. Assurez-vous que tous les fichiers sont présents
2. Initialisez un dépôt Git si ce n'est pas déjà fait :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

### 2. Déployer sur Railway

1. Connectez-vous à [Railway.app](https://railway.app)
2. Cliquez sur "New Project"
3. Choisissez "Deploy from GitHub repo" ou "Deploy from CLI"

#### Option A: Déploiement depuis GitHub

1. Connectez votre compte GitHub
2. Sélectionnez votre dépôt
3. Railway détectera automatiquement la configuration

#### Option B: Déploiement depuis CLI

1. Installez Railway CLI :
   ```bash
   npm install -g @railway/cli
   ```

2. Connectez-vous :
   ```bash
   railway login
   ```

3. Initialisez le projet :
   ```bash
   railway init
   ```

4. Déployez :
   ```bash
   railway up
   ```

### 3. Configuration des variables d'environnement

Dans le dashboard Railway, ajoutez ces variables d'environnement :

- `SECRET_KEY`: Une clé secrète aléatoire pour Flask
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `0`

### 4. Configuration de la licence RLextra

**Important**: RLextra nécessite une licence. Vous avez plusieurs options :

1. **Licence d'évaluation**: Obtenez une licence d'essai sur [reportlab.com](https://www.reportlab.com)
2. **Licence commerciale**: Achetez une licence pour un usage en production
3. **Alternative**: Modifiez le code pour utiliser uniquement ReportLab standard (fonctionnalités limitées)

Pour configurer la licence dans Railway :
- Ajoutez la variable d'environnement `RL_LICENSE` avec votre clé de licence

## Utilisation de l'API

Une fois déployé, votre application sera accessible à l'URL fournie par Railway.

### Interface Web

Visitez l'URL principale pour accéder à l'interface web où vous pouvez :
1. Coller vos données JSON
2. Générer le PDF
3. Télécharger le résultat

### API REST

Vous pouvez aussi utiliser l'API directement :

```bash
curl -X POST https://votre-app.railway.app/api/generate \
  -H "Content-Type: application/json" \
  -d @cv_data.json \
  --output cv.pdf
```

### Endpoints disponibles

- `GET /` : Interface web
- `GET /health` : Statut de l'application
- `POST /generate` : Générer un PDF (interface web)
- `POST /api/generate` : API pour générer un PDF
- `GET /download/<filename>` : Télécharger un PDF généré

## Maintenance

### Logs

Consultez les logs dans le dashboard Railway ou via CLI :
```bash
railway logs
```

### Mise à jour

Pour mettre à jour l'application :
```bash
git add .
git commit -m "Update"
railway up
```

## Dépannage

### Problèmes courants

1. **Erreur de licence RLextra**
   - Vérifiez que la variable `RL_LICENSE` est configurée
   - Assurez-vous que la licence est valide

2. **Erreur de mémoire**
   - Railway a des limites de mémoire selon le plan
   - Optimisez la génération PDF pour les gros documents

3. **Timeout**
   - La génération de PDF complexes peut prendre du temps
   - Ajustez le timeout dans `startup.sh` si nécessaire

### Support

Pour plus d'aide :
- Documentation Railway : [docs.railway.app](https://docs.railway.app)
- Logs de l'application : Vérifiez les logs dans le dashboard
- Variables d'environnement : Assurez-vous qu'elles sont correctement configurées