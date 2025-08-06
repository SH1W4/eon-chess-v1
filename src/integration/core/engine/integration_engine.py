from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
import logging
import json

from ...config.config_loader import ConfigLoader
from ...protocols.base import BaseProtocol
from ...connectors.base import BaseConnector
from ...adapters.base import BaseAdapter
from ...cache.manager import CacheManager
from ...monitoring.metrics import MetricsCollector

logger = logging.getLogger(__name__)

@dataclass
class IntegrationState:
    """Estado do sistema de integração."""
    connector_states: Dict[str, Any]
    adapter_states: Dict[str, Any]
    cache_state: Dict[str, Any]
    performance_metrics: Dict[str, float]

class IntegrationEngine:
    """Motor principal do sistema de integração."""
    
    def __init__(self, config_path: str):
        self.config = ConfigLoader.load(config_path)
        self.cache_manager = CacheManager(self.config["sistema_integracao"]["cache"])
        self.metrics_collector = MetricsCollector(
            self.config["sistema_integracao"]["monitoramento"]
        )
        
        # Inicialização dos componentes
        self.connectors: Dict[str, BaseConnector] = {}
        self.adapters: Dict[str, BaseAdapter] = {}
        self.protocols: Dict[str, BaseProtocol] = {}
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Inicializa todos os componentes do sistema."""
        self._init_protocols()
        self._init_connectors()
        self._init_adapters()
        
    def _init_protocols(self):
        """Inicializa os protocolos de comunicação."""
        protocol_config = self.config["protocolos_integracao"]
        for name, config in protocol_config.items():
            protocol_class = self._get_protocol_class(config["tipo"])
            self.protocols[name] = protocol_class(config)
            
    def _init_connectors(self):
        """Inicializa os conectores do sistema."""
        connector_config = self.config["sistema_integracao"]["conectores"]
        for name, config in connector_config.items():
            connector_class = self._get_connector_class(config["tipo"])
            self.connectors[name] = connector_class(
                config,
                self.cache_manager,
                self.metrics_collector
            )
            
    def _init_adapters(self):
        """Inicializa os adaptadores do sistema."""
        adapter_config = self.config["sistema_integracao"]["adaptadores"]
        for name, config in adapter_config.items():
            adapter_class = self._get_adapter_class(config["interface"])
            self.adapters[name] = adapter_class(
                config,
                self.protocols[config["protocolo"]],
                self.cache_manager,
                self.metrics_collector
            )
    
    @staticmethod
    def _get_protocol_class(tipo: str) -> type:
        """Retorna a classe do protocolo baseado no tipo."""
        from ...protocols import (
            HTTP2Protocol,
            GRPCProtocol,
            CustomProtocol
        )
        
        protocol_map = {
            "http2": HTTP2Protocol,
            "grpc": GRPCProtocol,
            "custom": CustomProtocol
        }
        return protocol_map[tipo]
    
    @staticmethod
    def _get_connector_class(tipo: str) -> type:
        """Retorna a classe do conector baseado no tipo."""
        from ...connectors import (
            CulturalConnector,
            QuantumConnector,
            NarrativeConnector
        )
        
        connector_map = {
            "cultural": CulturalConnector,
            "quantico": QuantumConnector,
            "narrativo": NarrativeConnector
        }
        return connector_map[tipo]
    
    @staticmethod
    def _get_adapter_class(interface: str) -> type:
        """Retorna a classe do adaptador baseado na interface."""
        from ...adapters import (
            RestAdapter,
            StreamAdapter,
            AdaptiveAdapter
        )
        
        adapter_map = {
            "rest": RestAdapter,
            "stream": StreamAdapter,
            "adaptativa": AdaptiveAdapter
        }
        return adapter_map[interface]
    
    async def process_message(
        self,
        source: str,
        target: str,
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Processa uma mensagem entre sistemas."""
        try:
            # Registro e métricas
            self.metrics_collector.record_message_received(source, target)
            logger.info(f"Processando mensagem de {source} para {target}")
            
            # Cache check
            cache_key = self._generate_cache_key(source, target, message)
            cached_result = await self.cache_manager.get(cache_key)
            if cached_result:
                logger.debug("Resultado encontrado em cache")
                return cached_result
            
            # Processamento
            source_connector = self.connectors[source]
            target_adapter = self.adapters[target]
            
            # Transformação e adaptação
            processed_message = await source_connector.process(message)
            adapted_message = await target_adapter.adapt(processed_message)
            
            # Cache do resultado
            await self.cache_manager.set(cache_key, adapted_message)
            
            # Métricas finais
            self.metrics_collector.record_message_processed(source, target)
            
            return adapted_message
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            self.metrics_collector.record_error(source, target, str(e))
            raise
    
    def _generate_cache_key(
        self,
        source: str,
        target: str,
        message: Dict[str, Any]
    ) -> str:
        """Gera uma chave de cache para a mensagem."""
        message_hash = hash(json.dumps(message, sort_keys=True))
        return f"{source}:{target}:{message_hash}"
    
    async def get_system_state(self) -> IntegrationState:
        """Retorna o estado atual do sistema de integração."""
        return IntegrationState(
            connector_states={
                name: connector.get_state()
                for name, connector in self.connectors.items()
            },
            adapter_states={
                name: adapter.get_state()
                for name, adapter in self.adapters.items()
            },
            cache_state=await self.cache_manager.get_stats(),
            performance_metrics=self.metrics_collector.get_current_metrics()
        )
    
    async def optimize_performance(self):
        """Otimiza a performance do sistema."""
        logger.info("Iniciando otimização de performance")
        
        # Otimização de cache
        await self.cache_manager.optimize()
        
        # Otimização de conectores
        for connector in self.connectors.values():
            await connector.optimize()
        
        # Otimização de adaptadores
        for adapter in self.adapters.values():
            await adapter.optimize()
        
        # Coleta e análise de métricas
        metrics = self.metrics_collector.get_current_metrics()
        if metrics["latency"] > self.config["performance"]["otimizacao"]["timeout"]:
            logger.warning("Alta latência detectada, ajustando configurações")
            await self._adjust_performance_settings()
    
    async def _adjust_performance_settings(self):
        """Ajusta configurações de performance baseado em métricas."""
        current_state = await self.get_system_state()
        
        # Ajuste de cache
        if current_state.performance_metrics["cache_hit_rate"] < 0.8:
            await self.cache_manager.adjust_ttl(
                increment=300  # Aumenta TTL em 5 minutos
            )
        
        # Ajuste de batch
        if current_state.performance_metrics["batch_efficiency"] < 0.7:
            self.config["performance"]["otimizacao"]["batch_size"] *= 1.5
            
        # Ajuste de timeouts
        if current_state.performance_metrics["timeout_rate"] > 0.1:
            for protocol in self.protocols.values():
                protocol.increase_timeout(factor=1.2)
    
    def shutdown(self):
        """Desliga o sistema de integração de forma segura."""
        logger.info("Iniciando shutdown do sistema de integração")
        
        # Fecha conectores
        for connector in self.connectors.values():
            connector.close()
            
        # Fecha adaptadores
        for adapter in self.adapters.values():
            adapter.close()
            
        # Fecha cache
        self.cache_manager.close()
        
        # Fecha coletor de métricas
        self.metrics_collector.close()
        
        logger.info("Sistema de integração desligado com sucesso")
