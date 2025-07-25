"""
Módulo de configuração do ARQUIMAX.
Define capacidades e configurações do sistema.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class ArquimaxCapabilities:
    """Capacidades do ARQUIMAX."""
    pattern_recognition: bool = True
    adaptive_learning: bool = True
    real_time_analysis: bool = True
    strategic_planning: bool = True
    monitoring: bool = True
    task_management: bool = True

@dataclass
class ArquimaxMonitoring:
    """Configurações de monitoramento."""
    accuracy_threshold: float = 0.8
    adaptation_rate: float = 0.1
    confidence_minimum: float = 0.7
    pattern_sensitivity: float = 0.6
    sampling_rate: float = 1.0
    metrics_buffer_size: int = 1000

@dataclass
class ArquimaxTaskManager:
    """Configurações do gerenciador de tarefas."""
    async_execution: bool = True
    cache_enabled: bool = True
    metrics_collection: bool = True
    max_concurrent_tasks: int = 4
    task_timeout: float = 5.0
    retry_attempts: int = 3

@dataclass
class ArquimaxConfig:
    """Configuração completa do ARQUIMAX."""
    capabilities: ArquimaxCapabilities
    monitoring: ArquimaxMonitoring
    task_manager: ArquimaxTaskManager
    version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"

class ArquimaxConfigManager:
    """Gerenciador de configuração do ARQUIMAX."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa gerenciador.
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config_path = config_path or 'config/arquimax_config.yaml'
        self.config = self._load_default_config()
        
        if Path(self.config_path).exists():
            self._load_config()
    
    def _load_default_config(self) -> ArquimaxConfig:
        """Carrega configuração padrão."""
        return ArquimaxConfig(
            capabilities=ArquimaxCapabilities(),
            monitoring=ArquimaxMonitoring(),
            task_manager=ArquimaxTaskManager()
        )
    
    def _load_config(self):
        """Carrega configuração do arquivo."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Atualiza capacidades
            if 'capabilities' in config_data:
                for key, value in config_data['capabilities'].items():
                    if hasattr(self.config.capabilities, key):
                        setattr(self.config.capabilities, key, value)
            
            # Atualiza monitoramento
            if 'monitoring' in config_data:
                for key, value in config_data['monitoring'].items():
                    if hasattr(self.config.monitoring, key):
                        setattr(self.config.monitoring, key, value)
            
            # Atualiza gerenciador de tarefas
            if 'task_manager' in config_data:
                for key, value in config_data['task_manager'].items():
                    if hasattr(self.config.task_manager, key):
                        setattr(self.config.task_manager, key, value)
            
            # Atualiza configurações gerais
            if 'version' in config_data:
                self.config.version = config_data['version']
            if 'environment' in config_data:
                self.config.environment = config_data['environment']
            if 'log_level' in config_data:
                self.config.log_level = config_data['log_level']
            
            logger.info(f"Configuração ARQUIMAX carregada: {self.config_path}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            logger.info("Usando configuração padrão")
    
    def save_config(self):
        """Salva configuração atual."""
        config_data = {
            'version': self.config.version,
            'environment': self.config.environment,
            'log_level': self.config.log_level,
            'capabilities': self.config.capabilities.__dict__,
            'monitoring': self.config.monitoring.__dict__,
            'task_manager': self.config.task_manager.__dict__
        }
        
        try:
            # Cria diretório se não existir
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(config_data, f, default_flow_style=False)
            
            logger.info(f"Configuração ARQUIMAX salva: {self.config_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {str(e)}")
    
    def get_config(self) -> ArquimaxConfig:
        """Retorna configuração atual."""
        return self.config
    
    def update_config(self, 
                     capabilities: Optional[Dict] = None,
                     monitoring: Optional[Dict] = None,
                     task_manager: Optional[Dict] = None,
                     **kwargs):
        """
        Atualiza configuração.
        
        Args:
            capabilities: Novas capacidades
            monitoring: Novas configurações de monitoramento
            task_manager: Novas configurações do gerenciador
            **kwargs: Outras configurações
        """
        # Atualiza capacidades
        if capabilities:
            for key, value in capabilities.items():
                if hasattr(self.config.capabilities, key):
                    setattr(self.config.capabilities, key, value)
        
        # Atualiza monitoramento
        if monitoring:
            for key, value in monitoring.items():
                if hasattr(self.config.monitoring, key):
                    setattr(self.config.monitoring, key, value)
        
        # Atualiza gerenciador
        if task_manager:
            for key, value in task_manager.items():
                if hasattr(self.config.task_manager, key):
                    setattr(self.config.task_manager, key, value)
        
        # Atualiza configurações gerais
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # Salva alterações
        self.save_config()
    
    def validate_config(self) -> bool:
        """Valida configuração atual."""
        try:
            # Validações básicas
            assert isinstance(self.config.version, str), "Versão inválida"
            assert self.config.environment in ["development", "production", "test"], "Ambiente inválido"
            assert self.config.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"], "Nível de log inválido"
            
            # Validações de monitoramento
            assert 0 <= self.config.monitoring.accuracy_threshold <= 1, "Limiar de precisão inválido"
            assert 0 <= self.config.monitoring.adaptation_rate <= 1, "Taxa de adaptação inválida"
            assert 0 <= self.config.monitoring.confidence_minimum <= 1, "Confiança mínima inválida"
            assert 0 <= self.config.monitoring.pattern_sensitivity <= 1, "Sensibilidade de padrões inválida"
            assert self.config.monitoring.sampling_rate > 0, "Taxa de amostragem inválida"
            assert self.config.monitoring.metrics_buffer_size > 0, "Tamanho de buffer inválido"
            
            # Validações do gerenciador
            assert self.config.task_manager.max_concurrent_tasks > 0, "Número de tarefas inválido"
            assert self.config.task_manager.task_timeout > 0, "Timeout inválido"
            assert self.config.task_manager.retry_attempts >= 0, "Número de tentativas inválido"
            
            return True
            
        except AssertionError as e:
            logger.error(f"Validação falhou: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return False
