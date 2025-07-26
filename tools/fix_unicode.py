#!/usr/bin/env python3
"""
Script para limpar caracteres Unicode problemáticos.
"""
import sys

def fix_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Criar backup
        with open(file_path + '.bak', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Substituir caracteres problemáticos
        content = content.replace('\u003e', '>')  # Substitui -\u003e por ->
        content = content.replace('\u003c', '<')  # Substitui \u003c= por <=
        
        # Salvar arquivo corrigido
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Arquivo {file_path} corrigido com sucesso!")
        
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        # Restaurar backup em caso de erro
        try:
            with open(file_path + '.bak', 'r', encoding='utf-8') as f:
                content = f.read()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Backup restaurado.")
        except:
            print("ERRO: Não foi possível restaurar o backup!")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python fix_unicode.py arquivo")
        sys.exit(1)
    
    fix_file(sys.argv[1])
