from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

@dataclass
class ProcessorState:
    """
    Estado de um processador quântico.
    Mantém informações sobre capacidade, utilização e saúde.
    """
    id: str
    capacity: float = 0.0
    utilization: float = 0.0
    temperature: float = 0.0
    error_rate: float = 0.0
    status: str = "inactive"

@dataclass
class QuantumState:
    """
    Estado do sistema quântico.
    Gerencia estados dos processadores e métricas do sistema.
    """
    # Timestamp da última atualização
    last_update: datetime = field(default_factory=datetime.now)
    
    # Lista de processadores ativos
    processors: List[ProcessorState] = field(default_factory=list)
    
    # Métricas de performance
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Estado do sistema
    system_state: Dict[str, Any] = field(default_factory=dict)
    
    # Status geral
    health_status: str = "unknown"
    
    def __init__(self):
        """Inicializa o estado com valores padrão."""
        self.last_update = datetime.now()
        self.processors = []
        self.performance_metrics = {
            "processing_power": 0.0,
            "memory_usage": 0.0,
            "error_correction_rate": 0.0
        }
        self.system_state = {
            "active_processes": 0,
            "resource_allocation": {},
            "error_queue": []
        }
        self.health_status = "initialized"
        
    async def configure(self, config: Dict[str, Any]) -> None:
        """
        Configura o estado com base nas configurações fornecidas.
        Args:
            config: Configurações incluindo setup de processadores e limites do sistema.
        """
        try:
            # Configura processadores
            if "processors" in config:
                self.processors = [
                    ProcessorState(
                        id=proc["id"],
                        capacity=proc.get("capacity", 0.0),
                        status="configured"
                    )
                    for proc in config["processors"]
                ]
                
            # Configura métricas de performance
            if "performance_limits" in config:
                self.performance_metrics.update(config["performance_limits"])
                
            # Configura estado do sistema
            if "system_config" in config:
                self.system_state.update(config["system_config"])
                
            self.last_update = datetime.now()
        except Exception as e:
            raise ValueError(f"Erro na configuração do estado quântico: {e}")
            
    async def initialize_processors(self) -> None:
        """Inicializa os processadores configurados."""
        try:
            for processor in self.processors:
                # Simula inicialização do processador
                processor.status = "active"
                processor.utilization = 0.0
                processor.temperature = 20.0  # temperatura inicial em Celsius
                processor.error_rate = 0.01   # taxa de erro inicial
        except Exception as e:
            raise RuntimeError(f"Erro na inicialização dos processadores: {e}")
            
    async def get_current_state(self) -> Dict[str, Any]:
        """Retorna o estado atual completo."""
        return {
            "last_update": self.last_update.isoformat(),
            "processors": [asdict(p) for p in self.processors],
            "performance_metrics": self.performance_metrics,
            "system_state": self.system_state,
            "health_status": self.health_status
        }
        
    async def update(self, new_state: Dict[str, Any]) -> None:
        """
        Atualiza o estado com novos valores.
        Args:
            new_state: Novos valores para atualização do estado.
        """
        try:
            # Atualiza métricas de processadores
            if "processors" in new_state:
                for proc_update in new_state["processors"]:
                    for processor in self.processors:
                        if processor.id == proc_update["id"]:
                            for key, value in proc_update.items():
                                if hasattr(processor, key):
                                    setattr(processor, key, value)
                                    
            # Atualiza métricas de performance
            if "performance_metrics" in new_state:
                self.performance_metrics.update(new_state["performance_metrics"])
                
            # Atualiza estado do sistema
            if "system_state" in new_state:
                self.system_state.update(new_state["system_state"])
                
            self.last_update = datetime.now()
        except Exception as e:
            raise ValueError(f"Erro na atualização do estado quântico: {e}")
            
    async def save_checkpoint(self) -> Dict[str, Any]:
        """Salva um checkpoint do estado atual."""
        return await self.get_current_state()
        
    async def is_healthy(self) -> bool:
        """
        Verifica se o estado está saudável.
        Considera métricas dos processadores e do sistema.
        """
        try:
            # Verifica tempo desde última atualização
            time_since_update = (datetime.now() - self.last_update).total_seconds()
            if time_since_update > 3600:  # 1 hora
                self.health_status = "stale"
                return False
                
            # Verifica processadores
            active_processors = [p for p in self.processors if p.status == "active"]
            if not active_processors:
                self.health_status = "no_active_processors"
                return False
                
            # Verifica métricas de performance
            for proc in active_processors:
                if proc.error_rate > 0.1:  # 10% taxa de erro máxima
                    self.health_status = "high_error_rate"
                    return False
                if proc.temperature > 80.0:  # 80°C temperatura máxima
                    self.health_status = "overheating"
                    return False
                    
            # Verifica estado do sistema
            if len(self.system_state["error_queue"]) > 100:  # máximo de erros em fila
                self.health_status = "error_queue_full"
                return False
                
            self.health_status = "healthy"
            return True
        except Exception:
            self.health_status = "error"
            return False
