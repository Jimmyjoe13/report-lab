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