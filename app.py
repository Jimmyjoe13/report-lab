#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import io
from datetime import datetime
from flask import Flask, jsonify, send_file, request, render_template_string
from werkzeug.utils import secure_filename
from generate_pdf import generate_pdf_from_data, load_template, fill_template

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

# Créer les dossiers nécessaires
os.makedirs('templates', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Page d'accueil avec formulaire
HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Générateur de CV PDF</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        h1 { color: #1a237e; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        textarea { width: 100%; min-height: 400px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #1a237e; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0d47a1; }
        .error { color: red; margin-top: 10px; }
        .success { color: green; margin-top: 10px; }
        .info { background: #e3f2fd; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Générateur de CV PDF</h1>
        <div class="info">
            <p><strong>Comment utiliser :</strong></p>
            <ol>
                <li>Collez vos données JSON dans le champ ci-dessous</li>
                <li>Cliquez sur "Générer le PDF"</li>
                <li>Téléchargez votre CV</li>
            </ol>
        </div>
        
        <form id="cvForm" action="/generate" method="POST">
            <div class="form-group">
                <label for="jsonData">Données JSON du CV :</label>
                <textarea id="jsonData" name="jsonData" placeholder="Collez ici vos données JSON...">{{ default_json }}</textarea>
            </div>
            <button type="submit">Générer le PDF</button>
        </form>
        
        <div id="message"></div>
    </div>
    
    <script>
        document.getElementById('cvForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = 'Génération en cours...';
            messageDiv.className = '';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonData: document.getElementById('jsonData').value
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    messageDiv.innerHTML = `<p class="success">PDF généré avec succès!</p>
                        <p><a href="${data.download_url}" target="_blank">Télécharger le CV</a></p>`;
                } else {
                    const error = await response.json();
                    messageDiv.innerHTML = `<p class="error">Erreur: ${error.error}</p>`;
                }
            } catch (error) {
                messageDiv.innerHTML = `<p class="error">Erreur: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>
"""

# Données JSON par défaut
DEFAULT_JSON = """{
  "name": "YBE",
  "title": "Développeur Java",
  "experience": "7",
  "skills": [
    "Java (V8-17)", "SpringBoot", "Spring Batch", "Spring Security", 
    "SQL", "Angular (V14)", 
    "GitLab CI/CD", "SonarQube", 
    "Artifactory", "Jira", 
    "Architecture Rest", "Microservices", 
    "API", "JUnit", 
    "Kubernetes", "Scrum"
  ],
  "skillLevels": [
    {"name": "Français", "level": 5},
    {"name": "Anglais", "level": 4}
  ],
  "languages": [
    {"language": "Français", "level": "Courant"},
    {"language": "Anglais", "level": "Bilingue"}
  ],
  "diplomas": [
    {"year": "2019", "title": "Master en ingénierie de conception et développement des applications"},
    {"year": "2015", "title": "Licence en Electronique - automatiques et informatique"}
  ],
  "experienceSummary": [
    {
      "period": "Aout 21 – Octobre 24",
      "duration": "3 ans 2 mois",
      "company": "GRDF - Paris",
      "role": "Ingénieur Full Stack"
    }
  ],
  "experiences": [
    {
      "period": "Aout 21 – Octobre 24",
      "company": "GRDF - Paris",
      "duration": "3 ans 2 mois",
      "role": "Ingénieur développement full stack",
      "project": "Projet e_omni : application pour la gestion des techniciens",
      "methodology": "Agile Scrum",
      "team": "10 Développeurs",
      "responsibilities": [
        "Analyser les contrats de services",
        "Développement des web services",
        "Tests unitaires et intégration continue"
      ],
      "environment": [
        {"category": "Backend", "tools": "Spring Boot 3, Java 17, Kafka"},
        {"category": "Frontend", "tools": "Angular 14"},
        {"category": "Base de données", "tools": "PostgreSQL"}
      ]
    }
  ]
}"""

@app.route('/')
def home():
    """Page d'accueil avec formulaire"""
    return render_template_string(HOME_PAGE, default_json=DEFAULT_JSON)

@app.route('/health')
def health():
    """Endpoint de santé pour Railway"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/generate', methods=['POST'])
def generate():
    """Générer le PDF à partir des données JSON"""
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data or 'jsonData' not in data:
            return jsonify({"error": "Données JSON manquantes"}), 400
        
        # Parser les données JSON
        try:
            cv_data = json.loads(data['jsonData'])
        except json.JSONDecodeError as e:
            return jsonify({"error": f"JSON invalide: {str(e)}"}), 400
        
        # Générer le nom du fichier
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"cv_{timestamp}.pdf"
        output_path = os.path.join('output', filename)
        
        # Charger le template
        template_path = os.path.join('templates', 'cv_template.rml')
        
        # Générer le PDF
        success = generate_pdf_from_data(cv_data, template_path, output_path)
        
        if success:
            # Retourner l'URL de téléchargement
            download_url = f"/download/{filename}"
            return jsonify({
                "status": "success",
                "filename": filename,
                "download_url": download_url
            })
        else:
            return jsonify({"error": "Erreur lors de la génération du PDF"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Télécharger un PDF généré"""
    try:
        # Sécuriser le nom de fichier
        filename = secure_filename(filename)
        file_path = os.path.join('output', filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "Fichier non trouvé"}), 404
            
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype='application/pdf')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API endpoint pour générer un PDF (retourne le fichier directement)"""
    try:
        # Récupérer les données JSON
        cv_data = request.get_json()
        if not cv_data:
            return jsonify({"error": "Données JSON manquantes"}), 400
        
        # Générer le PDF en mémoire
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"cv_{timestamp}.pdf"
        output_path = os.path.join('output', filename)
        
        # Générer le PDF
        success = generate_pdf_from_data(cv_data, None, output_path)
        
        if success:
            # Retourner le PDF
            return send_file(
                output_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({"error": "Erreur lors de la génération du PDF"}), 500
        
    except Exception as e:
        print(f"Erreur API: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Copier le template par défaut s'il n'existe pas
    template_path = os.path.join('templates', 'cv_template.rml')
    if not os.path.exists(template_path):
        with open('cv_template.rml', 'r', encoding='utf-8') as src:
            with open(template_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
    
    # Lancer l'application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
