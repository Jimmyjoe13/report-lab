#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def load_data(data_path):
    """Charge les données JSON"""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        sys.exit(1)

def load_template(template_path):
    """Charge le template RML"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erreur lors du chargement du template : {e}")
        sys.exit(1)

def fill_template(template, data):
    """Remplit le template avec les données"""
    # Remplacer les variables simples
    filled = template.replace('{{name}}', data.get('name', ''))
    filled = filled.replace('{{title}}', data.get('title', ''))
    filled = filled.replace('{{experience}}', str(data.get('experience', '')))
    
    # Compétences
    skills_xml = ""
    for skill in data.get('skills', []):
        skills_xml += f'<listItem><para>{skill}</para></listItem>\n'
    filled = filled.replace('{{skills}}', skills_xml)
    
    # Niveaux de compétences
    skill_levels_xml = ""
    for skill in data.get('skillLevels', []):
        name = skill.get('name', '')
        level = skill.get('level', 0)
        skill_levels_xml += f'<listItem><para>{name}: {level}/5</para></listItem>\n'
    filled = filled.replace('{{skillLevels}}', skill_levels_xml)
    
    # Langues
    languages_xml = ""
    for lang in data.get('languages', []):
        language = lang.get('language', '')
        level = lang.get('level', '')
        languages_xml += f'<listItem><para>{language}: {level}</para></listItem>\n'
    filled = filled.replace('{{languages}}', languages_xml)
    
    # Diplômes
    diplomas_xml = ""
    for diploma in data.get('diplomas', []):
        year = diploma.get('year', '')
        title = diploma.get('title', '')
        diplomas_xml += f'<listItem><para>{year} - {title}</para></listItem>\n'
    filled = filled.replace('{{diplomas}}', diplomas_xml)
    
    # Résumé des expériences
    exp_summary_xml = ""
    for exp in data.get('experienceSummary', []):
        period = exp.get('period', '')
        duration = exp.get('duration', '')
        company = exp.get('company', '')
        role = exp.get('role', '')
        exp_summary_xml += f'<listItem><para>{period} ({duration}) - {company} - {role}</para></listItem>\n'
    filled = filled.replace('{{experienceSummary}}', exp_summary_xml)
    
    # Expériences détaillées
    experiences_xml = ""
    for exp in data.get('experiences', []):
        period = exp.get('period', '')
        company = exp.get('company', '')
        duration = exp.get('duration', '')
        role = exp.get('role', '')
        project = exp.get('project', '')
        methodology = exp.get('methodology', '')
        team = exp.get('team', '')
        
        experiences_xml += f'<h2>{period} - {company}</h2>\n'
        experiences_xml += f'<para><b>Durée:</b> {duration}</para>\n'
        experiences_xml += f'<para><b>Poste:</b> {role}</para>\n'
        experiences_xml += f'<para><b>Projet:</b> {project}</para>\n'
        experiences_xml += f'<para><b>Méthodologie:</b> {methodology}</para>\n'
        experiences_xml += f'<para><b>Équipe:</b> {team}</para>\n'
        
        # Responsabilités
        experiences_xml += '<para><b>Responsabilités:</b></para>\n<ul>\n'
        for resp in exp.get('responsibilities', []):
            experiences_xml += f'<li><para>{resp}</para></li>\n'
        experiences_xml += '</ul>\n'
        
        # Environnement technique
        experiences_xml += '<para><b>Environnement technique:</b></para>\n<ul>\n'
        for env in exp.get('environment', []):
            category = env.get('category', '')
            tools = env.get('tools', '')
            experiences_xml += f'<li><para>{category}: {tools}</para></li>\n'
        experiences_xml += '</ul>\n'
        
        experiences_xml += '<spacer length="0.2in"/>\n'
    
    filled = filled.replace('{{experiences}}', experiences_xml)
    
    return filled

def generate_pdf(data_path, template_path, output_path):
    """Génère le PDF"""
    # Charger les données et le template
    data = load_data(data_path)
    template = load_template(template_path)
    
    # Remplir le template
    filled_template = fill_template(template, data)
    
    # Générer le PDF
    try:
        # Utiliser ReportLab directement au lieu de rlextra
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Titre
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph(f"{data.get('name', '')} - {data.get('title', '')}", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Compétences
        elements.append(Paragraph("Compétences", styles['Heading2']))
        for skill in data.get('skills', []):
            elements.append(Paragraph(f"• {skill}", styles['Normal']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Expériences
        elements.append(Paragraph("Expériences", styles['Heading2']))
        for exp in data.get('experiences', []):
            elements.append(Paragraph(f"{exp.get('period', '')} - {exp.get('company', '')}", styles['Heading3']))
            elements.append(Paragraph(f"Poste: {exp.get('role', '')}", styles['Normal']))
            elements.append(Paragraph(f"Projet: {exp.get('project', '')}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Responsabilités
            elements.append(Paragraph("Responsabilités:", styles['Normal']))
            for resp in exp.get('responsibilities', []):
                elements.append(Paragraph(f"• {resp}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Environnement technique
            elements.append(Paragraph("Environnement technique:", styles['Normal']))
            for env in exp.get('environment', []):
                elements.append(Paragraph(f"• {env.get('category', '')}: {env.get('tools', '')}", styles['Normal']))
            elements.append(Spacer(1, 0.25*inch))
        
        # Diplômes
        elements.append(Paragraph("Formation", styles['Heading2']))
        for diploma in data.get('diplomas', []):
            elements.append(Paragraph(f"{diploma.get('year', '')} - {diploma.get('title', '')}", styles['Normal']))
        
        # Générer le PDF
        doc.build(elements)
        print(f"PDF généré avec succès : {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        return False

def generate_pdf_from_data(data, template_path, output_path):
    """Génère le PDF à partir de données déjà chargées"""
    try:
        # Générer le PDF directement avec ReportLab
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Titre
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph(f"{data.get('name', '')} - {data.get('title', '')}", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        # Compétences
        elements.append(Paragraph("Compétences", styles['Heading2']))
        for skill in data.get('skills', []):
            elements.append(Paragraph(f"• {skill}", styles['Normal']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Expériences
        elements.append(Paragraph("Expériences", styles['Heading2']))
        for exp in data.get('experiences', []):
            elements.append(Paragraph(f"{exp.get('period', '')} - {exp.get('company', '')}", styles['Heading3']))
            elements.append(Paragraph(f"Poste: {exp.get('role', '')}", styles['Normal']))
            elements.append(Paragraph(f"Projet: {exp.get('project', '')}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Responsabilités
            elements.append(Paragraph("Responsabilités:", styles['Normal']))
            for resp in exp.get('responsibilities', []):
                elements.append(Paragraph(f"• {resp}", styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Environnement technique
            elements.append(Paragraph("Environnement technique:", styles['Normal']))
            for env in exp.get('environment', []):
                elements.append(Paragraph(f"• {env.get('category', '')}: {env.get('tools', '')}", styles['Normal']))
            elements.append(Spacer(1, 0.25*inch))
        
        # Diplômes
        elements.append(Paragraph("Formation", styles['Heading2']))
        for diploma in data.get('diplomas', []):
            elements.append(Paragraph(f"{diploma.get('year', '')} - {diploma.get('title', '')}", styles['Normal']))
        
        # Générer le PDF
        doc.build(elements)
        print(f"PDF généré avec succès : {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la génération du PDF : {e}")
        return False

if __name__ == "__main__":
    # Vérifier les arguments
    if len(sys.argv) != 4:
        print("Usage: python generate_pdf.py <data_path> <template_path> <output_path>")
        sys.exit(1)
    
    data_path = sys.argv[1]
    template_path = sys.argv[2]
    output_path = sys.argv[3]
    
    generate_pdf(data_path, template_path, output_path)
