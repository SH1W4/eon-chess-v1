#!/usr/bin/env python3
"""
AEON MCP CLI
CLI para execução do Model Context Protocol
"""

import argparse
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/mcp_execution.log')
    ]
)
logger = logging.getLogger('aeon_mcp')

class MCPExecutor:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.mcp_spec = self._load_yaml(self.project_root / 'docs' / 'MCP_SPECIFICATION.md')
        self.superscope = self._load_yaml(self.project_root / 'docs' / 'TASKMASH_MCP_SUPERSCOPE.md')
        self.arkitect_workflow = self._load_yaml(self.project_root / '.arkitect' / 'workflows' / 'mcp_superscope.yaml')

    def _load_yaml(self, path):
        """Carrega arquivo YAML ou extrai YAML de arquivo Markdown"""
        try:
            if path.suffix == '.md':
                # Extrair blocos YAML do markdown
                content = path.read_text()
                yaml_blocks = []
                in_yaml = False
                current_block = []
                
                for line in content.split('\n'):
                    if line.strip() == '```yaml':
                        in_yaml = True
                        continue
                    elif line.strip() == '```' and in_yaml:
                        in_yaml = False
                        yaml_blocks.append('\n'.join(current_block))
                        current_block = []
                        continue
                        
                    if in_yaml:
                        current_block.append(line)
                
                # Combinar todos os blocos YAML
                combined_yaml = '\n'.join(yaml_blocks)
                return yaml.safe_load(combined_yaml)
            else:
                return yaml.safe_load(path.read_text())
        except Exception as e:
            logger.error(f"Erro ao carregar {path}: {e}")
            return {}

    def run_phase(self, phase_name):
        """Executa uma fase específica do MCP"""
        logger.info(f"Iniciando fase: {phase_name}")
        
        # Validar fase
        if phase_name not in self.arkitect_workflow['phases']:
            logger.error(f"Fase {phase_name} não encontrada")
            return False
            
        phase = self.arkitect_workflow['phases'][phase_name]
        
        # Executar cada task da fase
        for task in phase:
            logger.info(f"Executando task: {task['name']}")
            try:
                if task.get('automated', False):
                    self._run_automated_task(task)
                else:
                    self._run_development_task(task)
                    
                # Validar resultado
                if 'validation' in task:
                    self._validate_task(task)
                    
            except Exception as e:
                logger.error(f"Erro na task {task['name']}: {e}")
                return False
                
        logger.info(f"Fase {phase_name} concluída com sucesso")
        return True

    def _run_automated_task(self, task):
        """Executa uma task automatizada"""
        logger.info(f"Executando task automatizada: {task['name']}")
        # Verificar dependências
        if 'dependencies' in task:
            for dep in task['dependencies']:
                logger.info(f"Verificando dependência: {dep}")
                
        # Executar triggers
        if 'triggers' in task:
            for trigger in task['triggers']:
                logger.info(f"Executando trigger: {trigger}")
                
        # Processar outputs
        if 'outputs' in task:
            for output in task['outputs']:
                logger.info(f"Gerando output: {output}")

    def _run_development_task(self, task):
        """Executa uma task de desenvolvimento"""
        logger.info(f"Iniciando task de desenvolvimento: {task['name']}")
        logger.info(f"Descrição: {task['description']}")
        
        # Processar subtasks se existirem
        if 'subtasks' in task:
            for subtask in task['subtasks']:
                logger.info(f"Processando subtask: {subtask}")

    def _validate_task(self, task):
        """Valida o resultado de uma task"""
        logger.info(f"Validando task: {task['name']}")
        
        if 'validation' in task and 'criteria' in task['validation']:
            for criterion in task['validation']['criteria']:
                logger.info(f"Verificando critério: {criterion}")

    def list_phases(self):
        """Lista todas as fases disponíveis"""
        logger.info("Fases disponíveis:")
        for phase_name in self.arkitect_workflow['phases']:
            logger.info(f"- {phase_name}")

    def show_status(self):
        """Mostra o status atual do MCP"""
        logger.info("Status do MCP:")
        # Carregar métricas
        metrics = self.arkitect_workflow.get('metrics', {})
        for category, values in metrics.items():
            logger.info(f"\n{category.upper()}:")
            for metric, details in values.items():
                logger.info(f"- {metric}: {details}")

def main():
    parser = argparse.ArgumentParser(description='AEON MCP CLI - Execute Model Context Protocol tasks')
    parser.add_argument('action', choices=['run', 'list', 'status'], help='Ação a ser executada')
    parser.add_argument('--phase', help='Nome da fase a ser executada')
    
    args = parser.parse_args()
    executor = MCPExecutor()
    
    if args.action == 'run':
        if not args.phase:
            logger.error("Fase não especificada. Use --phase NOME_DA_FASE")
            sys.exit(1)
        success = executor.run_phase(args.phase)
        sys.exit(0 if success else 1)
    elif args.action == 'list':
        executor.list_phases()
    elif args.action == 'status':
        executor.show_status()

if __name__ == '__main__':
    main()
