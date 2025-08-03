import os
import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional

class DocMonitor:
    def __init__(self):
        self.base_path = os.getcwd()
        self.docs_path = os.path.join(self.base_path, 'docs')
        self.metrics_path = os.path.join(self.base_path, '.docsync', 'metrics')
        self.health_checks = {
            'links': self._check_links,
            'images': self._check_images,
            'sections': self._check_sections,
            'consistency': self._check_consistency
        }
        
    def monitor_all(self):
        """Monitora todos os documentos"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'documents': {},
            'global': {
                'total_docs': 0,
                'broken_links': 0,
                'missing_sections': 0,
                'consistency_issues': 0
            }
        }
        
        for root, _, files in os.walk(self.docs_path):
            for file in files:
                if file.endswith('.md'):
                    doc_path = os.path.join(root, file)
                    rel_path = os.path.relpath(doc_path, self.docs_path)
                    
                    doc_metrics = self._check_document(doc_path)
                    metrics['documents'][rel_path] = doc_metrics
                    
                    # Atualiza métricas globais
                    metrics['global']['total_docs'] += 1
                    metrics['global']['broken_links'] += len(doc_metrics['broken_links'])
                    metrics['global']['missing_sections'] += len(doc_metrics['missing_sections'])
                    metrics['global']['consistency_issues'] += len(doc_metrics['consistency_issues'])
        
        self._save_metrics(metrics)
        return metrics
    
    def _check_document(self, doc_path: str) -> Dict:
        """Verifica um documento específico"""
        with open(doc_path, 'r') as f:
            content = f.read()
            
        metrics = {
            'last_checked': datetime.now().isoformat(),
            'size': len(content),
            'broken_links': [],
            'missing_sections': [],
            'consistency_issues': [],
            'health_score': 100.0
        }
        
        # Executa verificações
        for check_name, check_func in self.health_checks.items():
            check_result = check_func(content)
            metrics.update(check_result)
            
            # Ajusta health score
            if check_result.get('issues', []):
                metrics['health_score'] -= len(check_result['issues']) * 5
                
        metrics['health_score'] = max(0.0, metrics['health_score'])
        return metrics
    
    def _check_links(self, content: str) -> Dict:
        """Verifica links no documento"""
        import re
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        broken_links = []
        
        for text, link in links:
            if link.startswith('http'):
                continue  # Skip external links
                
            full_path = os.path.join(self.docs_path, link)
            if not os.path.exists(full_path):
                broken_links.append({
                    'text': text,
                    'link': link,
                    'type': 'broken_internal_link'
                })
                
        return {'broken_links': broken_links}
    
    def _check_images(self, content: str) -> Dict:
        """Verifica imagens no documento"""
        import re
        images = re.findall(r'!\[([^\]]*)\]\(([^\)]+)\)', content)
        missing_images = []
        
        for alt, src in images:
            if src.startswith('http'):
                continue  # Skip external images
                
            full_path = os.path.join(self.docs_path, src)
            if not os.path.exists(full_path):
                missing_images.append({
                    'alt': alt,
                    'src': src,
                    'type': 'missing_image'
                })
                
        return {'missing_images': missing_images}
    
    def _check_sections(self, content: str) -> Dict:
        """Verifica seções obrigatórias"""
        required_sections = {
            'README.md': ['Visão Geral', 'Instalação', 'Uso'],
            'api/README.md': ['Endpoints', 'Autenticação', 'Exemplos'],
            'guides/': ['Introdução', 'Como Usar', 'Próximos Passos']
        }
        
        found_sections = []
        for line in content.split('\n'):
            if line.startswith('## '):
                found_sections.append(line[3:].strip())
                
        missing_sections = []
        for doc_pattern, sections in required_sections.items():
            for section in sections:
                if section not in found_sections:
                    missing_sections.append({
                        'section': section,
                        'type': 'missing_required_section'
                    })
                    
        return {'missing_sections': missing_sections}
    
    def _check_consistency(self, content: str) -> Dict:
        """Verifica consistência do documento"""
        issues = []
        
        # Verifica formatação
        if '\n\n\n' in content:
            issues.append({
                'type': 'multiple_empty_lines',
                'description': 'Multiple consecutive empty lines found'
            })
            
        # Verifica hierarquia de títulos
        lines = content.split('\n')
        prev_level = 0
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > prev_level + 1:
                    issues.append({
                        'type': 'invalid_heading_hierarchy',
                        'line': i,
                        'content': line
                    })
                prev_level = level
                
        return {'consistency_issues': issues}
    
    def _save_metrics(self, metrics: Dict):
        """Salva métricas"""
        os.makedirs(self.metrics_path, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metrics_file = os.path.join(self.metrics_path, f'metrics_{timestamp}.json')
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
            
    def generate_report(self, metrics: Dict) -> str:
        """Gera relatório baseado nas métricas"""
        report = f"""# Relatório de Saúde da Documentação
Gerado em: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Métricas Globais
- Total de Documentos: {metrics['global']['total_docs']}
- Links Quebrados: {metrics['global']['broken_links']}
- Seções Faltantes: {metrics['global']['missing_sections']}
- Problemas de Consistência: {metrics['global']['consistency_issues']}

## Documentos com Problemas
"""
        
        for doc_path, doc_metrics in metrics['documents'].items():
            if doc_metrics['broken_links'] or doc_metrics['missing_sections'] or doc_metrics['consistency_issues']:
                report += f"\n### {doc_path}\n"
                report += f"Health Score: {doc_metrics['health_score']}%\n"
                
                if doc_metrics['broken_links']:
                    report += "\nLinks Quebrados:\n"
                    for link in doc_metrics['broken_links']:
                        report += f"- {link['text']} ({link['link']})\n"
                        
                if doc_metrics['missing_sections']:
                    report += "\nSeções Faltantes:\n"
                    for section in doc_metrics['missing_sections']:
                        report += f"- {section['section']}\n"
                        
                if doc_metrics['consistency_issues']:
                    report += "\nProblemas de Consistência:\n"
                    for issue in doc_metrics['consistency_issues']:
                        report += f"- {issue['type']}"
                        if 'line' in issue:
                            report += f" (linha {issue['line']})"
                        report += "\n"
                        
        return report

def main():
    """Função principal"""
    monitor = DocMonitor()
    metrics = monitor.monitor_all()
    
    # Gera e salva relatório
    report = monitor.generate_report(metrics)
    report_path = os.path.join(monitor.metrics_path, 'latest_report.md')
    with open(report_path, 'w') as f:
        f.write(report)
        
    print(f"Relatório de saúde gerado em: {report_path}")

if __name__ == "__main__":
    main()
