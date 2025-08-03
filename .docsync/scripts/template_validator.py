import os
import re
import yaml
import logging
from typing import Dict, List, Set

class TemplateValidator:
    """Validador de templates do DOCSYNC."""
    
    def __init__(self):
        """Inicializa o validador de templates."""
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.templates = self._load_templates()
        self.required_sections = self._get_required_sections()
        
    def _load_templates(self) -> Dict:
        """Carrega templates disponíveis."""
        templates_path = os.path.join(self.base_path, '.docsync', 'templates')
        templates = {}
        
        for filename in os.listdir(templates_path):
            if filename.endswith('.md'):
                with open(os.path.join(templates_path, filename), 'r', encoding='utf-8') as f:
                    templates[filename] = f.read()
        
        return templates
    
    def _get_required_sections(self) -> Dict[str, Set[str]]:
        """Define seções obrigatórias para cada tipo de documento."""
        return {
            'technical': {
                '## Visão Geral',
                '## Integração',
                '## Componentes',
                '## Métricas',
                '## Validação',
                '## Exemplos de Uso',
                '## Documentação Técnica',
                '## Manutenção',
                '## Referências'
            },
            'user': {
                '## Visão Geral',
                '## Como Usar',
                '## Configurações',
                '## Suporte'
            },
            'cultural': {
                '## Tema Cultural',
                '## Elementos',
                '## Narrativas',
                '## Interações'
            },
            'development': {
                '## Estrutura',
                '## Dependências',
                '## Testes',
                '## Deployment'
            }
        }
    
    def validate_document(self, doc_path: str, doc_type: str) -> List[str]:
        """Valida um documento específico."""
        errors = []
        
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Validar seções obrigatórias
            required = self.required_sections.get(doc_type, set())
            found_sections = set(re.findall(r'^##\s+.*$', content, re.MULTILINE))
            
            missing_sections = required - found_sections
            if missing_sections:
                errors.append(f"Seções obrigatórias faltando: {missing_sections}")
            
            # Validar formatação YAML (se existir)
            yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', content, re.DOTALL)
            for block in yaml_blocks:
                try:
                    yaml.safe_load(block)
                except yaml.YAMLError as e:
                    errors.append(f"Erro no bloco YAML: {str(e)}")
            
            # Validar links internos
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
            for text, link in links:
                if link.startswith('/') and not os.path.exists(os.path.join(self.base_path, link.lstrip('/'))):
                    errors.append(f"Link quebrado: {link}")
            
        except Exception as e:
            errors.append(f"Erro ao validar documento: {str(e)}")
        
        return errors
    
    def validate_directory(self, dir_path: str, doc_type: str) -> Dict[str, List[str]]:
        """Valida todos os documentos em um diretório."""
        results = {}
        
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    errors = self.validate_document(full_path, doc_type)
                    if errors:
                        results[full_path] = errors
        
        return results
    
    def generate_report(self, validation_results: Dict[str, List[str]]) -> str:
        """Gera relatório de validação."""
        report = ["# Relatório de Validação de Templates\n"]
        
        if not validation_results:
            report.append("✅ Todos os documentos estão válidos!")
        else:
            for doc_path, errors in validation_results.items():
                report.append(f"\n## {os.path.basename(doc_path)}")
                for error in errors:
                    report.append(f"- ❌ {error}")
        
        return "\n".join(report)

def main():
    """Função principal de validação."""
    validator = TemplateValidator()
    
    # Validar cada tipo de documentação
    doc_types = {
        'technical': 'docs/technical',
        'user': 'docs/user',
        'cultural': 'docs/cultural',
        'development': 'docs/development'
    }
    
    all_results = {}
    for doc_type, path in doc_types.items():
        full_path = os.path.join(validator.base_path, path)
        if os.path.exists(full_path):
            results = validator.validate_directory(full_path, doc_type)
            all_results.update(results)
    
    # Gerar e salvar relatório
    report = validator.generate_report(all_results)
    report_path = os.path.join(validator.base_path, '.docsync', 'reports', 'validation_report.md')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Relatório de validação gerado em: {report_path}")

if __name__ == "__main__":
    main()
