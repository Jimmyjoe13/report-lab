from flask import Flask, request, render_template, send_file, jsonify
import os
import generate_pdf

app = Flask(__name__)

from flask import Flask, request, render_template, send_file, jsonify
import os
import generate_pdf
import json
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return f"Erreur dans le JSON: {str(e)}", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        output_path = tmp_file.name

    template_path = os.path.join('templates', 'cv_template.rml')
    success = generate_pdf.generate_pdf_from_data(data, template_path, output_path)

    if not success:
        return "Erreur lors de la génération du PDF", 500

    return send_file(output_path, mimetype='application/pdf', as_attachment=True, download_name='cv.pdf')

if __name__ == '__main__':
    # Copier le template par défaut s'il n'existe pas
    template_path = os.path.join('templates', 'cv_template.rml')
    if not os.path.exists(template_path):
        # Essayer de trouver le template dans plusieurs endroits
        possible_paths = ['cv_template.rml', './cv_template.rml', '../cv_template.rml']
        for path in possible_paths:
            if os.path.exists(path):
                os.makedirs('templates', exist_ok=True)
                with open(path, 'r', encoding='utf-8') as src:
                    with open(template_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"Template copié depuis {path}")
                break
        else:
            print("ATTENTION: Template cv_template.rml non trouvé!")
    
    # Lancer l'application
    port = int(os.environ.get('PORT', 8080))
    print(f"Démarrage de l'application sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
