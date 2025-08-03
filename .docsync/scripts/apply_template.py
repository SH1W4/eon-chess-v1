#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

def create_backup(file_path):
    """Cria backup do arquivo original."""
    backup_dir = os.path.join(
        os.path.dirname(os.path.dirname(file_path)),
        '.docsync',
        'backup',
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(file_path, os.path.join(backup_dir, os.path.basename(file_path)))

def apply_template(file_path, template_path):
    """Aplica o template ao documento mantendo o conteúdo existente."""
    # Criar backup
    create_backup(file_path)
    
    # Ler template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Ler documento atual
    with open(file_path, 'r', encoding='utf-8') as f:
        current_content = f.read()
    
    # Extrair seções existentes
    sections = {}
    current_section = None
    current_text = []
    
    for line in current_content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_text).strip()
            current_section = line[3:].strip()
            current_text = []
        elif line.startswith('# '):
            sections['title'] = line[2:].strip()
        else:
            current_text.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_text).strip()
    
    # Aplicar conteúdo existente ao template
    new_content = template_content
    
    # Substituir seções
    if 'title' in sections:
        new_content = new_content.replace('{{module_name}}', sections['title'])
    if 'Visão Geral' in sections:
        new_content = new_content.replace('{{module_description}}', sections['Visão Geral'])
    if 'Documentação Técnica' in sections:
        new_content = new_content.replace('{{technical_details}}', sections['Documentação Técnica'])
    
    # Salvar novo conteúdo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    """Função principal."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    template_path = os.path.join(base_dir, '.docsync', 'templates', 'docsync', 'technical_module.md')
    docs_dir = os.path.join(base_dir, 'docs', 'technical')
    
    # Procurar documentos técnicos
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Aplicando template em: {file_path}")
                apply_template(file_path, template_path)

if __name__ == '__main__':
    main()
