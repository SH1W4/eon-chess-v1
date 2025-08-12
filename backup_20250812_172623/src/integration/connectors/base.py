from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import logging

from ..cache.manager import CacheManager
from ..monitoring.metrics import MetricsCollector

logger = logging.getLogger(__name__)

class BaseConnector(ABC):
    """Interface base para todos os conectores do sistema."""
    
    def __init__(
        self,
        config: Dict[str, Any],
        cache_manager: CacheManager,
        metrics_collector: MetricsCollector
    ):
        self.config = config
        self.cache_manager = cache_manager
        self.metrics_collector = metrics_collector
        self.name = self.__class__.__name__
        
        # Estado interno
        self._state = {
            "status": "initialized",
            "connected": False,
            "last_error": None,
            "metrics": {}
        }
        
        # Configuração específica
        self._setup_config()
        
    def _setup_config(self):
        """Configura parâmetros específicos do conector."""
        self.tipo = self.config["tipo"]
        self.cache_enabled = self.config.get("cache", True)
        self.validation_enabled = self.config.get("validacao", True)
        
        # Configuração de adaptação
        adapt_config = self.config.get("adaptacao", {})
        self.adaptation_mode = adapt_config.get("modo", "padrao")
        self.evolution_enabled = adapt_config.get("evolucao", False)
        self.optimization_enabled = adapt_config.get("otimizacao", False)
    
    @abstractmethod
    async def connect(self) -> bool:
        """Estabelece conexão com o sistema externo."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Desconecta do sistema externo."""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Valida a conexão atual."""
        pass
    
    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa dados através do conector."""
        pass
    
    @abstractmethod
    async def optimize(self) -> bool:
        """Otimiza o conector para melhor performance."""
        pass
    
    async def _pre_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Pré-processamento de dados antes do processamento principal."""
        try:
            # Validação
            if self.validation_enabled:
                self._validate_data(data)
            
            # Cache check
            if self.cache_enabled:
                cache_key = self._generate_cache_key(data)
                cached_result = await self.cache_manager.get(cache_key)
                if cached_result:
                    logger.debug(f"Cache hit para {self.name}")
                    return cached_result
            
            # Métricas
            self.metrics_collector.record_connector_processing(self.name)
            
            return data
            
        except Exception as e:
            logger.error(f"Erro no pré-processamento de {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
    
    async def _post_process(
        self,
        original_data: Dict[str, Any],
        processed_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Pós-processamento de dados após o processamento principal."""
        try:
            # Cache update
            if self.cache_enabled:
                cache_key = self._generate_cache_key(original_data)
                await self.cache_manager.set(cache_key, processed_data)
            
            # Métricas
            self.metrics_collector.record_connector_processed(self.name)
            
            # Otimização adaptativa
            if self.optimization_enabled:
                await self._adaptive_optimization()
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Erro no pós-processamento de {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
    
    def _validate_data(self, data: Dict[str, Any]) -> bool:
        """Valida os dados de entrada."""
        if not isinstance(data, dict):
            raise ValueError(f"Dados inválidos para {self.name}: deve ser um dicionário")
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
    
    async def _adaptive_optimization(self):
        """Realiza otimização adaptativa baseada em métricas."""
        current_metrics = self.metrics_collector.get_connector_metrics(self.name)
        
        # Análise de performance
        if current_metrics.get("latency", 0) > self.config.get("max_latency", 1000):
            logger.warning(f"Alta latência detectada em {self.name}")
            await self.optimize()
        
        # Análise de erros
        error_rate = current_metrics.get("error_rate", 0)
        if error_rate > 0.1:  # 10% de erro
            logger.warning(f"Alta taxa de erro em {self.name}: {error_rate}")
            self._state["status"] = "degraded"
    
    def get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do conector."""
        return {
            **self._state,
            "config": {
                "tipo": self.tipo,
                "cache_enabled": self.cache_enabled,
                "validation_enabled": self.validation_enabled,
                "adaptation_mode": self.adaptation_mode
            },
            "metrics": self.metrics_collector.get_connector_metrics(self.name)
        }
    
    def close(self):
        """Fecha o conector de forma segura."""
        try:
            asyncio.run(self.disconnect())
            self._state["connected"] = False
            self._state["status"] = "closed"
            logger.info(f"Conector {self.name} fechado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao fechar conector {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
