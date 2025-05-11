import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch


def generate_pdf_from_data(data, template_path, output_path):
    """Génère le PDF à partir de données déjà chargées"""
    try:
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Déboguer le template_path si fourni
        if template_path:
            print(f"Template path: {template_path}, exists: {os.path.exists(template_path)}")
            if not os.path.exists(template_path):
                print(f"Template not found at {template_path}")
                template_path = None
        
        # Générer le PDF directement avec ReportLab
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Titre avec style personnalisé
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=20,
            alignment=1,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=20
        )
        # Vérifier si data est un dict ou une liste
        if isinstance(data, dict):
            elements.append(Paragraph(f"{data.get('name', '')} - {data.get('title', '')}", title_style))
            elements.append(Paragraph(f"{data.get('experience', '')} ans d'expérience", title_style))
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            # Prendre le premier élément si c'est une liste de dicts
            elements.append(Paragraph(f"{data[0].get('name', '')} - {data[0].get('title', '')}", title_style))
            elements.append(Paragraph(f"{data[0].get('experience', '')} ans d'expérience", title_style))
        else:
            elements.append(Paragraph("Données invalides", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Compétences
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceBefore=15,
            spaceAfter=10
        )
        elements.append(Paragraph("Compétences", heading_style))
        
        # Organiser les compétences en tableau
        if isinstance(data, dict):
            skills = data.get('skills', [])
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            skills = data[0].get('skills', [])
        else:
            skills = []
        skill_data = []
        row = []
        for i, skill in enumerate(skills):
            row.append(skill)
            if (i + 1) % 3 == 0 or i == len(skills) - 1:
                skill_data.append(row)
                row = []
        
        if skill_data:
            skill_table = Table(skill_data, colWidths=[2*inch, 2*inch, 2*inch])
            skill_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ]))
            elements.append(skill_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Expériences
        elements.append(Paragraph("Expériences professionnelles", heading_style))
        if isinstance(data, dict):
            experiences = data.get('experiences', [])
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            experiences = data[0].get('experiences', [])
        else:
            experiences = []
        for exp in experiences:
            exp_style = ParagraphStyle(
                'ExpTitle',
                parent=styles['Heading3'],
                fontSize=14,
                textColor=colors.HexColor('#000080'),
                spaceBefore=10,
                spaceAfter=5
            )
            elements.append(Paragraph(f"{exp.get('period', '')} - {exp.get('company', '')}", exp_style))
            elements.append(Paragraph(f"<b>Poste:</b> {exp.get('role', '')}", styles['Normal']))
            elements.append(Paragraph(f"<b>Projet:</b> {exp.get('project', '')}", styles['Normal']))
            elements.append(Paragraph(f"<b>Méthodologie:</b> {exp.get('methodology', '')}", styles['Normal']))
            elements.append(Paragraph(f"<b>Équipe:</b> {exp.get('team', '')}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Responsabilités
            elements.append(Paragraph("<b>Responsabilités:</b>", styles['Normal']))
            for resp in exp.get('responsibilities', []):
                bullet_style = ParagraphStyle(
                    'BulletItem',
                    parent=styles['Normal'],
                    leftIndent=20,
                    bulletIndent=10
                )
                elements.append(Paragraph(f"• {resp}", bullet_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # Environnement technique
            elements.append(Paragraph("<b>Environnement technique:</b>", styles['Normal']))
            for env in exp.get('environment', []):
                elements.append(Paragraph(f"• <b>{env.get('category', '')}:</b> {env.get('tools', '')}", bullet_style))
            elements.append(Spacer(1, 0.25*inch))
        
        # Diplômes
        elements.append(Paragraph("Formation", heading_style))
        if isinstance(data, dict):
            diplomas = data.get('diplomas', [])
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            diplomas = data[0].get('diplomas', [])
        else:
            diplomas = []
        if isinstance(diplomas, list):
            for diploma in diplomas:
                elements.append(Paragraph(f"{diploma.get('year', '')} - {diploma.get('title', '')}", styles['Normal']))
        else:
            elements.append(Paragraph("Données invalides pour les diplômes", styles['Normal']))
        
        # Générer le PDF
        doc.build(elements)
        print(f"PDF généré avec succès : {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        import traceback
        traceback.print_exc()
        return False
