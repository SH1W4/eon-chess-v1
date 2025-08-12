import os
import re
import glob

def fix_unicode_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Substitui os caracteres unicode
        content = content.replace('\\u003c', '<')
        content = content.replace('\\u003e', '>')
        content = content.replace('\\u0026', '&')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'✓ Corrigido: {filepath}')
            return True
        return False
    except Exception as e:
        print(f'✗ Erro em {filepath}: {e}')
        return False

# Encontra todos os arquivos .tsx e .ts
tsx_files = glob.glob('**/*.tsx', recursive=True)
ts_files = glob.glob('**/*.ts', recursive=True)
all_files = tsx_files + ts_files

print(f"Verificando {len(all_files)} arquivos TypeScript...")
fixed_count = 0

for filepath in all_files:
    if fix_unicode_in_file(filepath):
        fixed_count += 1

print(f"\n✓ Total de arquivos corrigidos: {fixed_count}")
