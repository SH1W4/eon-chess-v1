from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import logging

from ..protocols.base import BaseProtocol
from ..cache.manager import CacheManager
from ..monitoring.metrics import MetricsCollector

logger = logging.getLogger(__name__)

class BaseAdapter(ABC):
    """Interface base para todos os adaptadores do sistema."""
    
    def __init__(
        self,
        config: Dict[str, Any],
        protocol: BaseProtocol,
        cache_manager: CacheManager,
        metrics_collector: MetricsCollector
    ):
        self.config = config
        self.protocol = protocol
        self.cache_manager = cache_manager
        self.metrics_collector = metrics_collector
        self.name = self.__class__.__name__
        
        # Estado interno
        self._state = {
            "status": "initialized",
            "active": False,
            "last_error": None,
            "metrics": {}
        }
        
        # Configuração específica
        self._setup_config()
    
    def _setup_config(self):
        """Configura parâmetros específicos do adaptador."""
        self.interface = self.config["interface"]
        self.cache_enabled = self.config.get("cache", True)
        
        # Configuração de monitoramento
        monitor_config = self.config.get("monitoramento", {})
        self.metrics_enabled = monitor_config.get("metricas", True)
        self.alerts_enabled = monitor_config.get("alertas", True)
        self.logs_enabled = monitor_config.get("logs", True)
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Inicializa o adaptador."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Desliga o adaptador."""
        pass
    
    @abstractmethod
    async def adapt(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Adapta os dados para o formato necessário."""
        pass
    
    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Valida os dados adaptados."""
        pass
    
    @abstractmethod
    async def optimize(self) -> bool:
        """Otimiza o adaptador para melhor performance."""
        pass
    
    async def _pre_adapt(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Pré-processamento antes da adaptação."""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Validação inicial
            if not self._validate_input(data):
                raise ValueError(f"Dados de entrada inválidos para {self.name}")
            
            # Cache check
            if self.cache_enabled:
                cache_key = self._generate_cache_key(data)
                cached_result = await self.cache_manager.get(cache_key)
                if cached_result:
                    logger.debug(f"Cache hit para {self.name}")
                    return cached_result
            
            # Métricas
            if self.metrics_enabled:
                self.metrics_collector.record_adapter_processing(
                    self.name,
                    asyncio.get_event_loop().time() - start_time
                )
            
            return data
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento de {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
    
    async def _post_adapt(
        self,
        original_data: Dict[str, Any],
        adapted_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Pós-processamento após a adaptação."""
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Validação do resultado
            if not await self.validate(adapted_data):
                raise ValueError(f"Dados adaptados inválidos em {self.name}")
            
            # Cache update
            if self.cache_enabled:
                cache_key = self._generate_cache_key(original_data)
                await self.cache_manager.set(cache_key, adapted_data)
            
            # Métricas
            if self.metrics_enabled:
                self.metrics_collector.record_adapter_processed(
                    self.name,
                    asyncio.get_event_loop().time() - start_time
                )
            
            # Logs
            if self.logs_enabled:
                logger.info(
                    f"Adaptação concluída em {self.name}",
                    extra={
                        "adapter": self.name,
                        "processing_time": asyncio.get_event_loop().time() - start_time
                    }
                )
            
            return adapted_data
            
        except Exception as e:
            logger.error(f"Erro no pós-processamento de {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validação básica dos dados de entrada."""
        if not isinstance(data, dict):
            return False
        return True
    
    def _generate_cache_key(self, data: Dict[str, Any]) -> str:
        """Gera uma chave única para cache."""
        import hashlib
        import json
        
        # Serializa dados de forma determinística
        serialized = json.dumps(data, sort_keys=True)
        
        # Gera hash SHA-256
        hasher = hashlib.sha256()
        hasher.update(serialized.encode())
        
        return f"{self.name}:{hasher.hexdigest()}"
    
    async def _check_health(self) -> bool:
        """Verifica a saúde do adaptador."""
        try:
            # Verifica protocolo
            if not await self.protocol.check_health():
                logger.warning(f"Protocolo não saudável em {self.name}")
                return False
            
            # Verifica cache
            if self.cache_enabled:
                cache_health = await self.cache_manager.check_health()
                if not cache_health:
                    logger.warning(f"Cache não saudável em {self.name}")
                    return False
            
            # Verifica métricas
            if self.metrics_enabled:
                metrics_health = self.metrics_collector.check_health()
                if not metrics_health:
                    logger.warning(f"Métricas não saudáveis em {self.name}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar saúde de {self.name}: {str(e)}")
            return False
    
    def get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do adaptador."""
        return {
            **self._state,
            "config": {
                "interface": self.interface,
                "cache_enabled": self.cache_enabled,
                "metrics_enabled": self.metrics_enabled,
                "alerts_enabled": self.alerts_enabled
            },
            "protocol": self.protocol.get_state(),
            "metrics": self.metrics_collector.get_adapter_metrics(self.name)
        }
    
    def close(self):
        """Fecha o adaptador de forma segura."""
        try:
            asyncio.run(self.shutdown())
            self._state["active"] = False
            self._state["status"] = "closed"
            logger.info(f"Adaptador {self.name} fechado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao fechar adaptador {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
