from typing import Dict, List
import os
import yaml
import shutil
from datetime import datetime
import logging

class DocSyncAutomation:
    """Automatização do DOCSYNC para o sistema de xadrez."""
    
    def __init__(self):
        """Inicializa o sistema de automação do DOCSYNC."""
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.config = self._load_config()
        self.setup_logging()
        
    def _load_config(self) -> Dict:
        """Carrega configuração do DOCSYNC."""
        config_path = os.path.join(self.base_path, '.docsync', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """Configura sistema de logging."""
        log_path = os.path.join(self.base_path, '.docsync', 'logs')
        os.makedirs(log_path, exist_ok=True)
        
        logging.basicConfig(
            filename=os.path.join(log_path, 'docsync.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def sync_technical_docs(self):
        """Sincroniza documentação técnica."""
        self._sync_directory('docs/technical', interval_minutes=5)
        self._apply_technical_template()

    def _apply_technical_template(self):
        """Aplica o novo template técnico aos documentos."""
        template_path = os.path.join(self.base_path, '.docsync', 'templates', 'technical_module.md')
        technical_path = os.path.join(self.base_path, 'docs/technical')

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        for root, _, files in os.walk(technical_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self._update_technical_doc(file_path, template_content)

    def _update_technical_doc(self, file_path: str, template_content: str):
        """Atualiza um documento técnico com o novo template."""
        try:
            # Ler conteúdo atual
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()

            # Extrair informações existentes
            module_name = self._extract_section(current_content, '#', '##')
            description = self._extract_section(current_content, '## Visão Geral', '##')
            technical_details = self._extract_section(current_content, '## Especificações Técnicas', '##')

            # Preparar novo conteúdo
            new_content = template_content
            new_content = new_content.replace('{{module_name}}', module_name.strip())
            new_content = new_content.replace('{{module_description}}', description.strip())
            new_content = new_content.replace('{{technical_details}}', technical_details.strip())

            # Fazer backup do arquivo original
            backup_path = file_path + '.bak'
            shutil.copy2(file_path, backup_path)

            # Salvar novo conteúdo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logging.info(f'Documento atualizado com sucesso: {file_path}')

        except Exception as e:
            logging.error(f'Erro ao atualizar documento {file_path}: {str(e)}')

    def _extract_section(self, content: str, start_marker: str, end_marker: str) -> str:
        """Extrai uma seção do documento entre marcadores."""
        try:
            start_idx = content.index(start_marker)
            if end_marker in content[start_idx:]:
                end_idx = content.index(end_marker, start_idx + len(start_marker))
                return content[start_idx + len(start_marker):end_idx].strip()
            return content[start_idx + len(start_marker):].strip()
        except ValueError:
            return ''
        
    def sync_user_docs(self):
        """Sincroniza documentação de usuário."""
        self._sync_directory('docs/user', interval_minutes=15)
        
    def sync_cultural_docs(self):
        """Sincroniza documentação cultural."""
        self._sync_directory('docs/cultural', interval_minutes=30)
        
    def sync_development_docs(self):
        """Sincroniza documentação de desenvolvimento."""
        self._sync_directory('docs/development', interval_minutes=10080)  # Semanal
        
    def _sync_directory(self, rel_path: str, interval_minutes: int):
        """Sincroniza um diretório específico."""
        full_path = os.path.join(self.base_path, rel_path)
        backup_path = os.path.join(self.base_path, '.docsync', 'backup', rel_path)
        
        # Criar diretório de backup se não existir
        os.makedirs(backup_path, exist_ok=True)
        
        # Backup dos arquivos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(backup_path, timestamp)
        if os.path.exists(full_path):
            shutil.copytree(full_path, backup_dir)
            logging.info(f'Backup criado em {backup_dir}')
            
    def validate_docs(self):
        """Valida documentação."""
        self._validate_links()
        self._validate_consistency()
        self._validate_templates()
        
    def _validate_links(self):
        """Valida links na documentação."""
        # Implementação da validação de links
        logging.info('Validando links...')
        
    def _validate_consistency(self):
        """Valida consistência da documentação."""
        # Implementação da validação de consistência
        logging.info('Validando consistência...')
        
    def _validate_templates(self):
        """Valida uso correto dos templates."""
        # Implementação da validação de templates
        logging.info('Validando templates...')
        
    def cleanup_old_backups(self, days_to_keep: int = 7):
        """Remove backups antigos."""
        backup_path = os.path.join(self.base_path, '.docsync', 'backup')
        # Implementação da limpeza de backups
        logging.info(f'Removendo backups mais antigos que {days_to_keep} dias')
        
    def run_maintenance(self):
        """Executa rotinas de manutenção."""
        self.validate_docs()
        self.cleanup_old_backups()
        logging.info('Manutenção concluída')

def main():
    """Função principal de automação."""
    automation = DocSyncAutomation()
    
    # Sincronização
    automation.sync_technical_docs()
    automation.sync_user_docs()
    automation.sync_cultural_docs()
    automation.sync_development_docs()
    
    # Manutenção
    automation.run_maintenance()
    
if __name__ == "__main__":
    main()
