from dataclasses import dataclass
from typing import Dict, List, Optional
import asyncio
import logging
import time
from datetime import datetime

@dataclass
class SystemHealth:
    cpu_usage: float
    memory_usage: float
    response_time: float
    error_rate: float
    system_load: float

@dataclass
class ComponentMetrics:
    component_name: str
    execution_time: float
    success_rate: float
    error_count: int
    last_execution: datetime

@dataclass
class PerformanceMetrics:
    moves_analyzed: int
    patterns_recognized: int
    learning_iterations: int
    adaptation_score: float
    quantum_operations: int

class AdvancedMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_health = SystemHealth(0.0, 0.0, 0.0, 0.0, 0.0)
        self.component_metrics: Dict[str, ComponentMetrics] = {}
        self.performance_metrics = PerformanceMetrics(0, 0, 0, 0.0, 0)
        self.alert_thresholds = {
            'cpu_usage': 0.8,
            'memory_usage': 0.8,
            'error_rate': 0.1,
            'response_time': 1.0
        }

    async def start_monitoring(self):
        """Inicia o monitoramento do sistema"""
        self.logger.info("Iniciando monitoramento avançado")
        await asyncio.gather(
            self._monitor_system_health(),
            self._monitor_components(),
            self._monitor_performance()
        )

    async def _monitor_system_health(self):
        """Monitora a saúde geral do sistema"""
        while True:
            try:
                # Coleta métricas do sistema
                self.system_health.cpu_usage = await self._get_cpu_usage()
                self.system_health.memory_usage = await self._get_memory_usage()
                self.system_health.response_time = await self._get_response_time()
                self.system_health.error_rate = await self._get_error_rate()
                self.system_health.system_load = await self._get_system_load()

                # Verifica alertas
                await self._check_health_alerts()

                await asyncio.sleep(5)  # Intervalo de monitoramento
            except Exception as e:
                self.logger.error(f"Erro no monitoramento de saúde: {str(e)}")
                await asyncio.sleep(10)  # Intervalo maior em caso de erro

    async def _monitor_components(self):
        """Monitora métricas específicas de componentes"""
        components = ['arquimax', 'nexus', 'chess_engine', 'learner']
        while True:
            try:
                for component in components:
                    metrics = await self._get_component_metrics(component)
                    self.component_metrics[component] = metrics
                    await self._analyze_component_health(component, metrics)

                await asyncio.sleep(10)  # Intervalo de monitoramento
            except Exception as e:
                self.logger.error(f"Erro no monitoramento de componentes: {str(e)}")
                await asyncio.sleep(15)

    async def _monitor_performance(self):
        """Monitora métricas de performance"""
        while True:
            try:
                self.performance_metrics = await self._collect_performance_metrics()
                await self._analyze_performance()
                await asyncio.sleep(15)  # Intervalo de monitoramento
            except Exception as e:
                self.logger.error(f"Erro no monitoramento de performance: {str(e)}")
                await asyncio.sleep(20)

    async def _get_cpu_usage(self) -> float:
        """Obtém uso de CPU"""
        # Implementação simplificada - pode ser expandida
        return 0.5

    async def _get_memory_usage(self) -> float:
        """Obtém uso de memória"""
        # Implementação simplificada - pode ser expandida
        return 0.6

    async def _get_response_time(self) -> float:
        """Obtém tempo de resposta médio"""
        # Implementação simplificada - pode ser expandida
        return 0.1

    async def _get_error_rate(self) -> float:
        """Obtém taxa de erros"""
        # Implementação simplificada - pode ser expandida
        return 0.02

    async def _get_system_load(self) -> float:
        """Obtém carga do sistema"""
        # Implementação simplificada - pode ser expandida
        return 0.7

    async def _get_component_metrics(self, component: str) -> ComponentMetrics:
        """Obtém métricas específicas de um componente"""
        return ComponentMetrics(
            component_name=component,
            execution_time=0.1,
            success_rate=0.95,
            error_count=2,
            last_execution=datetime.now()
        )

    async def _collect_performance_metrics(self) -> PerformanceMetrics:
        """Coleta métricas de performance do sistema"""
        return PerformanceMetrics(
            moves_analyzed=1000,
            patterns_recognized=50,
            learning_iterations=100,
            adaptation_score=0.8,
            quantum_operations=20
        )

    async def _check_health_alerts(self):
        """Verifica e gera alertas baseados na saúde do sistema"""
        if self.system_health.cpu_usage > self.alert_thresholds['cpu_usage']:
            self.logger.warning(f"Alerta: CPU usage alto ({self.system_health.cpu_usage:.2%})")

        if self.system_health.memory_usage > self.alert_thresholds['memory_usage']:
            self.logger.warning(f"Alerta: Memory usage alto ({self.system_health.memory_usage:.2%})")

        if self.system_health.error_rate > self.alert_thresholds['error_rate']:
            self.logger.warning(f"Alerta: Error rate alto ({self.system_health.error_rate:.2%})")

        if self.system_health.response_time > self.alert_thresholds['response_time']:
            self.logger.warning(f"Alerta: Response time alto ({self.system_health.response_time:.2f}s)")

    async def _analyze_component_health(self, component: str, metrics: ComponentMetrics):
        """Analisa saúde de um componente específico"""
        if metrics.success_rate < 0.9:
            self.logger.warning(f"Alerta: Baixa taxa de sucesso no componente {component}")
        
        if metrics.error_count > 10:
            self.logger.warning(f"Alerta: Alto número de erros no componente {component}")

    async def _analyze_performance(self):
        """Analisa métricas de performance"""
        if self.performance_metrics.adaptation_score < 0.6:
            self.logger.warning("Alerta: Baixa taxa de adaptação")

        if self.performance_metrics.quantum_operations < 10:
            self.logger.warning("Alerta: Baixo número de operações quânticas")

    async def get_system_status(self) -> Dict:
        """Retorna status completo do sistema"""
        return {
            'health': self.system_health,
            'components': self.component_metrics,
            'performance': self.performance_metrics
        }

    async def get_component_status(self, component: str) -> Optional[ComponentMetrics]:
        """Retorna status de um componente específico"""
        return self.component_metrics.get(component)
