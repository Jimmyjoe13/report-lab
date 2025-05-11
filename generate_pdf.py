def generate_pdf(data_path, template_path, output_path):
    """Génère le PDF"""
    # Charger les données et le template
    data = load_data(data_path)
    template = load_template(template_path)
    
    # Remplir le template
    filled_template = fill_template(template, data)
    
    # Générer le PDF
    try:
        rml2pdf.go(filled_template.encode('utf-8'), output_path)
        print(f"PDF généré avec succès : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        sys.exit(1)

def generate_pdf_from_data(data, template_path, output_path):
    """Génère le PDF à partir de données déjà chargées"""
    try:
        # Charger le template
        template = load_template(template_path)
        
        # Remplir le template
        filled_template = fill_template(template, data)
        
        # Générer le PDF
        rml2pdf.go(filled_template.encode('utf-8'), output_path)
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        return False