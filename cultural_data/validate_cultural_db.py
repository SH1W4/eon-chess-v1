#!/usr/bin/env python3
"""
Validador do Banco de Dados Cultural do ChessMaster
"""

import os
import yaml
import json
import re
from typing import List, Dict, Any
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='cultural_validation.log'
)

class CulturalDBValidator:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.errors = []
        self.warnings = []

    def validate_file_naming(self, filepath: str) -> bool:
        """Valida o padrão de nomenclatura dos arquivos."""
        filename = os.path.basename(filepath)
        if not filename.islower():
            self.warnings.append(f"Arquivo {filename} deve usar apenas lowercase")
            return False
        if ' ' in filename:
            self.errors.append(f"Arquivo {filename} não deve conter espaços")
            return False
        return True

    def validate_yaml_file(self, filepath: str) -> bool:
        """Valida a estrutura de arquivos YAML."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Validações básicas
            if not isinstance(data, dict):
                self.errors.append(f"YAML {filepath} deve ter estrutura de dicionário")
                return False
            
            # Validações específicas por tipo
            if 'type' in data:
                if data['type'] == 'cultural_pieces':
                    return self.validate_pieces_config(data, filepath)
                elif data['type'] == 'ancient_civilization':
                    return self.validate_theme_config(data, filepath)
            
            return True
        except yaml.YAMLError as e:
            self.errors.append(f"Erro ao parsear YAML {filepath}: {str(e)}")
            return False

    def validate_markdown_file(self, filepath: str) -> bool:
        """Valida a estrutura de arquivos Markdown."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Validações básicas de Markdown
            if not content.startswith('# '):
                self.warnings.append(f"Markdown {filepath} deve começar com título nível 1")
                return False
            
            # Verifica seções obrigatórias por tipo
            if 'research' in filepath:
                required_sections = ['## Introdução', '## Conclusão', '## Referências']
            elif 'lessons' in filepath:
                required_sections = ['## Visão Geral', '## Elementos Culturais']
            elif 'stories' in filepath:
                required_sections = ['## Prólogo', '## Epílogo']
            else:
                required_sections = []

            for section in required_sections:
                if section not in content:
                    self.errors.append(f"Markdown {filepath} deve conter seção {section}")
                    return False
            
            return True
        except Exception as e:
            self.errors.append(f"Erro ao ler Markdown {filepath}: {str(e)}")
            return False

    def validate_pieces_config(self, data: Dict[str, Any], filepath: str) -> bool:
        """Valida configuração de peças."""
        required_keys = ['name', 'type', 'culture', 'pieces']
        for key in required_keys:
            if key not in data:
                self.errors.append(f"Configuração de peças {filepath} deve conter {key}")
                return False
        
        required_pieces = ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']
        for piece in required_pieces:
            if piece not in data['pieces']:
                self.errors.append(f"Configuração {filepath} deve definir peça {piece}")
                return False
        
        return True

    def validate_theme_config(self, data: Dict[str, Any], filepath: str) -> bool:
        """Valida configuração de tema cultural."""
        required_keys = ['name', 'type', 'attributes', 'narrative_elements']
        for key in required_keys:
            if key not in data:
                self.errors.append(f"Configuração de tema {filepath} deve conter {key}")
                return False
        return True

    def validate_directory_structure(self) -> bool:
        """Valida a estrutura de diretórios."""
        required_dirs = [
            'research/historical',
            'research/cultural',
            'research/strategic',
            'configurations/themes',
            'configurations/narratives',
            'configurations/pieces',
            'content/stories',
            'content/lessons',
            'content/philosophy'
        ]

        for dir_path in required_dirs:
            full_path = os.path.join(self.base_path, dir_path)
            if not os.path.isdir(full_path):
                self.errors.append(f"Diretório obrigatório ausente: {dir_path}")
                return False
        return True

    def validate_all(self) -> bool:
        """Executa todas as validações."""
        is_valid = True
        
        # Valida estrutura de diretórios
        if not self.validate_directory_structure():
            is_valid = False

        # Percorre todos os arquivos
        for root, _, files in os.walk(self.base_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                
                # Ignora arquivos de sistema
                if filename.startswith('.'):
                    continue

                # Valida nomenclatura
                if not self.validate_file_naming(filepath):
                    is_valid = False

                # Valida conteúdo baseado na extensão
                if filename.endswith('.yaml'):
                    if not self.validate_yaml_file(filepath):
                        is_valid = False
                elif filename.endswith('.md'):
                    if not self.validate_markdown_file(filepath):
                        is_valid = False

        return is_valid

    def print_report(self):
        """Imprime relatório de validação."""
        print("\n=== Relatório de Validação ===")
        
        if self.errors:
            print("\nERROS:")
            for error in self.errors:
                print(f"- {error}")
        
        if self.warnings:
            print("\nAVISOS:")
            for warning in self.warnings:
                print(f"- {warning}")
        
        if not self.errors and not self.warnings:
            print("\nNenhum problema encontrado!")

def main():
    # Caminho base do banco de dados cultural
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Cria e executa validador
    validator = CulturalDBValidator(base_path)
    is_valid = validator.validate_all()
    
    # Imprime relatório
    validator.print_report()
    
    # Registra resultado no log
    if is_valid:
        logging.info("Validação concluída com sucesso")
    else:
        logging.error("Validação falhou")
        
    return 0 if is_valid else 1

if __name__ == '__main__':
    exit(main())
