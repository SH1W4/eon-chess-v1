#!/usr/bin/env python3
"""
Script para corrigir caminhos de arquivos HTML após reorganização
Converte ../styles/ -> web/styles/ e ../utils/ -> web/utils/
"""

import os
import re
from pathlib import Path

def fix_html_paths():
    """Corrige todos os caminhos nos arquivos HTML"""
    
    # Diretório das páginas
    pages_dir = Path("web/pages")
    
    if not pages_dir.exists():
        print("❌ Diretório web/pages não encontrado!")
        return
    
    # Padrões para substituir
    patterns = [
        (r'\.\./styles/', 'web/styles/'),
        (r'\.\./utils/', 'web/utils/'),
        (r'\.\./src/ai/', 'src/ai/')
    ]
    
    # Contadores
    total_files = 0
    fixed_files = 0
    total_replacements = 0
    
    # Processar cada arquivo HTML
    for html_file in pages_dir.glob("*.html"):
        total_files += 1
        print(f"🔍 Processando: {html_file}")
        
        try:
            # Ler conteúdo
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Aplicar todas as substituições
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            # Se houve mudanças, salvar arquivo
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Contar substituições
                for pattern, replacement in patterns:
                    count = len(re.findall(pattern, original_content))
                    if count > 0:
                        total_replacements += count
                        print(f"  ✅ {pattern} -> {replacement}: {count} substituições")
                
                fixed_files += 1
            else:
                print(f"  ℹ️  Nenhuma mudança necessária")
                
        except Exception as e:
            print(f"  ❌ Erro ao processar {html_file}: {e}")
    
    # Resumo
    print(f"\n🎯 RESUMO DA CORREÇÃO:")
    print(f"📁 Arquivos processados: {total_files}")
    print(f"🔧 Arquivos corrigidos: {fixed_files}")
    print(f"🔄 Total de substituições: {total_replacements}")
    
    if fixed_files > 0:
        print(f"✅ Correção concluída com sucesso!")
    else:
        print(f"ℹ️  Nenhuma correção necessária!")

if __name__ == "__main__":
    print("🚀 Iniciando correção de caminhos HTML...")
    fix_html_paths()
    print("✨ Processo concluído!")
