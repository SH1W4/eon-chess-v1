from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ArquimaxCapabilities:
    pattern_analysis: bool = True
    move_evaluation: bool = True
    adaptive_learning: bool = True
    symbiotic_integration: bool = True
    real_time_monitoring: bool = True
    quantum_enhancement: bool = False  # Desativado por padrão

class ArquimaxConfig:
    def __init__(self):
        self.capabilities = ArquimaxCapabilities()
        self.monitoring = {}

class ArquimaxConfigManager:
    def __init__(self):
        self._config = ArquimaxConfig()

    def get_config(self) -> ArquimaxConfig:
        """Retorna configuração atual."""
        return self._config

    def validate_config(self) -> bool:
        """Valida configuração atual.
        
        Returns:
            bool: True se configuração é válida
        """
        # Simples validação: pelo menos 4 capacidades ativas
        active_capabilities = sum(1 for cap, enabled in 
                                self._config.capabilities.__dict__.items() 
                                if enabled)
        return active_capabilities >= 4

    def update_config(self, **kwargs):
        """Atualiza configuração.
        
        Args:
            **kwargs: Valores para atualizar
        """
        if 'monitoring' in kwargs:
            self._config.monitoring.update(kwargs['monitoring'])
