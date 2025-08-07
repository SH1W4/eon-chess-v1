from typing import Dict, Any
from datetime import datetime
from .base_monitor import BaseMonitor

class NarrativeMonitor(BaseMonitor):
    """Monitor específico para o conector narrativo."""
    
    def __init__(self):
        super().__init__("narrative_monitor")
        self.story_elements = []
        self.active_flows = {}
        self.narrative_cache = {}
        
    async def check_health(self):
        """Verifica a saúde do conector narrativo."""
        metrics = await self.collect_metrics()
        
        # Métricas de fluxo narrativo
        self.add_metric(
            "flow_coherence",
            metrics["flow_coherence"],
            threshold=0.85
        )
        
        # Métricas de elementos
        self.add_metric(
            "element_consistency",
            metrics["element_consistency"],
            threshold=0.80
        )
        
        # Métricas de cache
        self.add_metric(
            "cache_hit_rate",
            metrics["cache_hit_rate"],
            threshold=0.65
        )
        
        # Métricas de performance
        self.add_metric(
            "processing_latency",
            metrics["processing_latency"],
            threshold=0.90  # Menor é melhor
        )
        
        # Verificação de estado
        await self.validate_state(metrics)
        
    async def collect_metrics(self) -> Dict[str, float]:
        """Coleta métricas do conector narrativo."""
        return {
            "flow_coherence": self._calculate_flow_coherence(),
            "element_consistency": self._calculate_element_consistency(),
            "cache_hit_rate": self._calculate_cache_performance(),
            "processing_latency": self._calculate_processing_latency(),
            "active_flows": len(self.active_flows),
            "story_elements": len(self.story_elements),
            "cache_size": len(self.narrative_cache),
            "last_update": datetime.now().timestamp()
        }
        
    async def validate_state(self, state: Dict[str, Any]) -> bool:
        """Valida o estado do conector narrativo."""
        # Verifica atualização temporal
        if state.get("last_update", 0) < datetime.now().timestamp() - 300:  # 5 minutos
            await self.handle_error("Estado narrativo desatualizado")
            return False
            
        # Verifica coerência dos fluxos
        if state.get("flow_coherence", 0) < 0.5:
            await self.handle_error("Baixa coerência nos fluxos narrativos")
            return False
            
        # Verifica consistência dos elementos
        if state.get("element_consistency", 0) < 0.4:
            await self.handle_error("Inconsistência nos elementos narrativos")
            return False
            
        # Verifica performance do cache
        if state.get("cache_hit_rate", 0) < 0.3:
            self.logger.warning("Performance do cache narrativo abaixo do ideal")
            
        return True
        
    async def attempt_recovery(self):
        """Tenta recuperar o conector narrativo."""
        self.logger.info("Tentando recuperar conector narrativo...")
        
        try:
            # Pausa fluxos ativos
            await self._pause_active_flows()
            
            # Limpa caches
            self.narrative_cache.clear()
            
            # Valida elementos existentes
            await self._validate_story_elements()
            
            # Reinicia fluxos
            await self._restart_flows()
            
            # Verifica recuperação
            metrics = await self.collect_metrics()
            if await self.validate_state(metrics):
                self.logger.info("Recuperação do conector narrativo bem-sucedida")
                self.recovery_attempts = 0
                return True
                
        except Exception as e:
            self.logger.error(f"Falha na recuperação narrativa: {e}")
            
        return False
        
    def _calculate_flow_coherence(self) -> float:
        """Calcula a coerência dos fluxos narrativos."""
        if not self.active_flows:
            return 0.0
        
        # Simula cálculo de coerência
        return min(len(self.active_flows) / 5, 1.0)
        
    def _calculate_element_consistency(self) -> float:
        """Calcula a consistência dos elementos narrativos."""
        if not self.story_elements:
            return 0.0
            
        # Simula cálculo de consistência
        return min(len(self.story_elements) / 20, 1.0)
        
    def _calculate_cache_performance(self) -> float:
        """Calcula a performance do cache narrativo."""
        if not self.narrative_cache:
            return 0.0
            
        # Simula taxa de acerto do cache
        return 0.75  # Valor inicial de exemplo
        
    def _calculate_processing_latency(self) -> float:
        """Calcula a latência de processamento narrativo."""
        # Simula latência (menor é melhor)
        return 0.85  # Valor inicial de exemplo
        
    async def _pause_active_flows(self):
        """Pausa fluxos narrativos ativos."""
        for flow_id in self.active_flows:
            self.active_flows[flow_id] = "paused"
            
    async def _validate_story_elements(self):
        """Valida elementos narrativos existentes."""
        valid_elements = []
        for element in self.story_elements:
            if self._is_element_valid(element):
                valid_elements.append(element)
        self.story_elements = valid_elements
        
    def _is_element_valid(self, element: Any) -> bool:
        """Verifica se um elemento narrativo é válido."""
        # Implementar validação específica
        return True
        
    async def _restart_flows(self):
        """Reinicia fluxos narrativos."""
        for flow_id in self.active_flows:
            if self.active_flows[flow_id] == "paused":
                self.active_flows[flow_id] = "active"
