#!/usr/bin/env python3
"""
Script para corrigir caminhos em arquivos HTML para servidor local
Converte caminhos relativos para absolutos quando servido de web/pages
"""

import os
import re
from pathlib import Path

def fix_html_paths():
    """Corrigir caminhos em todos os arquivos HTML"""
    pages_dir = Path("web/pages")
    
    if not pages_dir.exists():
        print("❌ Diretório web/pages não encontrado")
        return
    
    # Padrões de substituição
    replacements = [
        # CSS - caminhos relativos para absolutos
        (r'href="\.\./styles/', 'href="/web/styles/'),
        (r'href="\.\./styles/', 'href="/web/styles/'),
        
        # JavaScript - caminhos relativos para absolutos
        (r'src="\.\./utils/', 'src="/web/utils/'),
        (r'src="\.\./utils/', 'src="/web/utils/'),
        
        # AI modules - caminhos relativos para absolutos
        (r'src="\.\./src/ai/', 'src="/web/src/ai/'),
        (r'src="\.\./src/ai/', 'src="/web/src/ai/'),
    ]
    
    html_files = list(pages_dir.glob("*.html"))
    print(f"🔍 Encontrados {len(html_files)} arquivos HTML")
    
    fixed_count = 0
    for html_file in html_files:
        print(f"📝 Processando: {html_file.name}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Aplicar todas as substituições
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # Se houve mudanças, salvar o arquivo
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {html_file.name} - Corrigido")
                fixed_count += 1
            else:
                print(f"ℹ️ {html_file.name} - Sem alterações necessárias")
                
        except Exception as e:
            print(f"❌ Erro ao processar {html_file.name}: {e}")
    
    print(f"\n🎯 Resumo: {fixed_count} arquivos corrigidos de {len(html_files)}")

if __name__ == "__main__":
    fix_html_paths()
