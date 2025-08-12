from typing import Any, Dict, Optional, List
from datetime import datetime
import asyncio
from ..base_connector import BaseConnector
from .narrative_state import NarrativeState, StoryElement, NarrativeFlow
from .cache_manager import NarrativeCache
from .validator import NarrativeValidator

class NarrativeConnector(BaseConnector):
    """
    Conector para o sistema Narrativo.
    Gerencia o fluxo narrativo, histórias e elementos narrativos do sistema.
    """
    
    def __init__(self):
        super().__init__()
        # Inicializa o gerenciador de estado narrativo
        self._narrative_state = NarrativeState()
        # Inicializa cache e validador
        self._cache = NarrativeCache()
        self._validator = NarrativeValidator()
        # Fluxos narrativos ativos
        self._active_flows: List[NarrativeFlow] = []
        # Métricas de performance
        self._performance_metrics = {
            "cache_hits": 0,
            "cache_misses": 0,
            "validation_success": 0,
            "validation_failures": 0,
            "processing_times": []
        }
        # Estado de otimização
        self._optimization_state = {
            "last_optimization": datetime.now(),
            "optimization_interval": 3600,  # 1 hora
            "current_load": 0.0
        }
    
    async def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Inicializa o conector narrativo com configurações específicas.
        Args:
            config: Configurações incluindo elementos narrativos iniciais,
                   fluxos predefinidos e parâmetros de storytelling.
        """
        try:
            if config:
                # Configura o estado narrativo com os parâmetros fornecidos
                await self._narrative_state.configure(config)
                
                # Configura cache
                if "cache_config" in config:
                    self._cache = NarrativeCache(**config["cache_config"])
                
                # Pré-carrega dados
                await self._preload_data()
                
                # Configura fluxos narrativos iniciais
                if "initial_flows" in config:
                    self._active_flows = [
                        NarrativeFlow(**flow) 
                        for flow in config["initial_flows"]
                    ]
                    
                # Inicia otimização periódica
                if config.get("enable_optimization", True):
                    asyncio.create_task(self._periodic_optimization())
                    
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Erro na inicialização do conector narrativo: {e}")
            return False
    
    async def _preload_data(self):
        """Pré-carrega dados essenciais no cache."""
        patterns = ["opening_sequence", "midgame_patterns", "endgame_scenarios"]
        for pattern in patterns:
            await self._cache.preload(pattern)
    
    async def _periodic_optimization(self):
        """Executa otimização periódica do sistema."""
        while True:
            try:
                await asyncio.sleep(self._optimization_state["optimization_interval"])
                await self._optimize_system()
            except Exception as e:
                print(f"Erro na otimização periódica: {e}")
    
    async def _optimize_system(self):
        """Otimiza o sistema baseado em métricas e estado atual."""
        # Otimiza cache
        cache_stats = self._cache.get_stats()
        if cache_stats["hit_rate"] < 0.5:
            # Ajusta tamanho do cache
            new_size = min(cache_stats["max_size"] * 2, 10000)
            self._cache.max_size = new_size
            
        # Otimiza fluxos
        active_flows = len(self._active_flows)
        if active_flows > 10:
            # Prioriza fluxos mais ativos
            self._active_flows.sort(key=lambda x: x.usage_count, reverse=True)
            self._active_flows = self._active_flows[:10]
            
        # Atualiza estado
        self._optimization_state.update({
            "last_optimization": datetime.now(),
            "current_load": len(self._active_flows) / 10  # Normalizado para 0-1
        })
    
    async def connect(self) -> bool:
        """
        Estabelece conexão com o sistema narrativo.
        Prepara os fluxos narrativos e elementos de história.
        """
        if not self._is_initialized:
            raise RuntimeError("Conector narrativo não inicializado")
        try:
            # Verifica recursos narrativos
            resources_available = await self._check_resources()
            if not resources_available:
                return False
                
            # Inicializa sistema de storytelling
            await self._narrative_state.initialize_storytelling()
            
            # Prepara fluxos narrativos
            await self._prepare_narrative_flows()
            
            return True
        except Exception as e:
            print(f"Erro na conexão narrativa: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """
        Desconecta do sistema narrativo.
        Salva o estado atual das histórias e fluxos.
        """
        try:
            # Salva estado narrativo atual
            await self._narrative_state.save_checkpoint()
            # Finaliza fluxos narrativos ativos
            await self._finalize_active_flows()
            # Limpa cache
            self._cache.clear()
            return True
        except Exception as e:
            print(f"Erro na desconexão narrativa: {e}")
            return False
    
    async def get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do sistema narrativo."""
        try:
            base_state = await self._narrative_state.get_current_state()
            cache_stats = self._cache.get_stats()
            optimization_stats = self._optimization_state.copy()
            
            return {
                **base_state,
                "cache_stats": cache_stats,
                "optimization": optimization_stats,
                "active_flows": len(self._active_flows),
                "performance": self._performance_metrics
            }
        except Exception as e:
            print(f"Erro ao obter estado narrativo: {e}")
            return {}
    
    async def update_state(self, new_state: Dict[str, Any]) -> bool:
        """
        Atualiza o estado do sistema narrativo.
        Args:
            new_state: Novo estado narrativo a ser aplicado, incluindo
                      novas histórias, fluxos e elementos narrativos.
        """
        try:
            # Valida o novo estado
            validation_results = await self._validator.validate(new_state)
            if not all(result.passed for result in validation_results):
                return False
            
            # Atualiza estado
            await self._narrative_state.update(new_state)
            # Atualiza cache se necessário
            if "cache_update" in new_state:
                await self._cache.update(new_state["cache_update"])
            return True
        except Exception as e:
            print(f"Erro na atualização do estado narrativo: {e}")
            return False
    
    async def verify_health(self) -> bool:
        """
        Verifica a saúde do sistema narrativo.
        Analisa coerência das histórias e fluxos narrativos.
        """
        try:
            # Verifica saúde do estado narrativo
            state_health = await self._narrative_state.is_healthy()
            # Verifica coerência dos fluxos
            flow_health = await self._verify_narrative_flows()
            # Verifica integridade do cache
            cache_health = self._cache.get_stats()["hit_rate"] > 0.5
            
            return all([state_health, flow_health, cache_health])
        except Exception as e:
            print(f"Erro na verificação de saúde narrativa: {e}")
            return False
    
    async def _check_resources(self) -> bool:
        """Verifica disponibilidade de recursos narrativos."""
        try:
            return True
        except Exception:
            return False
    
    async def _prepare_narrative_flows(self):
        """Prepara os fluxos narrativos do sistema."""
        try:
            for flow in self._active_flows:
                await flow.prepare()
        except Exception as e:
            print(f"Erro ao preparar fluxos narrativos: {e}")
    
    async def _finalize_active_flows(self):
        """Finaliza os fluxos narrativos ativos."""
        try:
            for flow in self._active_flows:
                await flow.finalize()
            self._active_flows.clear()
        except Exception as e:
            print(f"Erro ao finalizar fluxos narrativos: {e}")
    
    async def _verify_narrative_flows(self) -> bool:
        """Verifica a saúde dos fluxos narrativos."""
        try:
            return all(flow.is_healthy() for flow in self._active_flows)
        except Exception:
            return False
