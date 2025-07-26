#!/usr/bin/env python3
"""
Script para limpeza de bytes nulos em arquivos Python.
Parte do sistema NEXUS-ARQUIMAX.
"""
import os
import shutil
import sys
from pathlib import Path

def clean_file(file_path):
    """Limpa bytes nulos de um arquivo, criando backup antes."""
    # Criar backup
    backup_path = str(file_path) + '.bak'
    shutil.copy2(file_path, backup_path)
    
    try:
        # Ler conteúdo original
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Remover bytes nulos
        cleaned = content.replace(b'\x00', b'')
        
        # Verificar se houve mudanças
        if content == cleaned:
            print(f"Arquivo limpo (sem alterações): {file_path}")
            os.remove(backup_path)  # Remove backup se não houve mudanças
            return False
        
        # Escrever conteúdo limpo
        with open(file_path, 'wb') as f:
            f.write(cleaned)
        
        print(f"Arquivo limpo (com backup): {file_path}")
        return True
        
    except Exception as e:
        # Em caso de erro, restaurar backup
        print(f"Erro ao limpar {file_path}: {e}")
        shutil.copy2(backup_path, file_path)
        return False

def main():
    """Função principal que processa a lista de arquivos."""
    target_files = [
        "framework/symbiotic_framework_blueprint.py",
        "src/core/board.py",
        "install_symbiotic.py",
        "giden_analysis.py",
        "setup_framework.py",
        "ai/pipeline/ai_profile.py",
        "ai/pipeline/ai.py",
        "ai/pipeline/main.py",
        "examples/cultural_ai_demo.py",
        "examples/cultural_demo.py",
        "examples/adaptive_ai_demo.py",
        "tests/test_engine.py",
        "tests/test_adaptive_ai.py",
        "tests/test_core.py"
    ]
    
    # Encontrar diretório raiz do projeto
    project_root = Path.cwd()
    while not (project_root / '.git').exists() and project_root != project_root.parent:
        project_root = project_root.parent
    
    cleaned_files = 0
    for rel_path in target_files:
        file_path = project_root / rel_path
        if file_path.exists():
            if clean_file(file_path):
                cleaned_files += 1
        else:
            print(f"Arquivo não encontrado: {file_path}")
    
    print(f"\nProcesso concluído. {cleaned_files} arquivos foram limpos.")

if __name__ == '__main__':
    main()
