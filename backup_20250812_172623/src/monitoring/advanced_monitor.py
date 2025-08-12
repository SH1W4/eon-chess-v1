from typing import Dict, List, Any, Optional
from datetime import datetime
import threading
import json
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class MetricPoint:
    """Ponto de métrica com timestamp"""
    value: float
    timestamp: datetime
    metadata: Dict = field(default_factory=dict)

@dataclass
class Alert:
    """Alerta do sistema de monitoramento"""
    level: str
    message: str
    timestamp: datetime
    context: Dict = field(default_factory=dict)

class AdvancedMonitor:
    """Sistema avançado de monitoramento"""
    
    def __init__(self):
        self.metrics: Dict[str, List[MetricPoint]] = {}
        self.alerts: List[Alert] = []
        self._lock = threading.Lock()
        self._alert_callbacks: List[callable] = []
        
    def record_metric(self, name: str, value: float, metadata: Optional[Dict] = None) -> None:
        """Registra uma métrica"""
        with self._lock:
            if name not in self.metrics:
                self.metrics[name] = []
            
            point = MetricPoint(
                value=value,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            self.metrics[name].append(point)
            
            # Verifica thresholds
            self._check_thresholds(name, point)
    
    def get_metric_history(self, name: str, limit: Optional[int] = None) -> List[MetricPoint]:
        """Retorna histórico de uma métrica"""
        with self._lock:
            history = self.metrics.get(name, [])
            if limit:
                return history[-limit:]
            return history
    
    def add_alert_callback(self, callback: callable) -> None:
        """Adiciona callback para alertas"""
        self._alert_callbacks.append(callback)
    
    def raise_alert(self, level: str, message: str, context: Optional[Dict] = None) -> None:
        """Gera um alerta"""
        alert = Alert(
            level=level,
            message=message,
            timestamp=datetime.now(),
            context=context or {}
        )
        
        with self._lock:
            self.alerts.append(alert)
            
        # Notifica callbacks
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Erro no callback de alerta: {e}")
    
    def get_recent_alerts(self, limit: Optional[int] = None) -> List[Alert]:
        """Retorna alertas recentes"""
        with self._lock:
            if limit:
                return self.alerts[-limit:]
            return self.alerts.copy()
    
    def _check_thresholds(self, metric_name: str, point: MetricPoint) -> None:
        """Verifica thresholds para métricas"""
        thresholds = {
            'cultural_expression': {'warning': 0.3, 'critical': 0.1},
            'style_consistency': {'warning': 0.4, 'critical': 0.2},
            'cache_hit_rate': {'warning': 0.5, 'critical': 0.3},
            'analysis_time': {'warning': 1.0, 'critical': 2.0}
        }
        
        if metric_name in thresholds:
            threshold = thresholds[metric_name]
            
            if point.value <= threshold['critical']:
                self.raise_alert(
                    'CRITICAL',
                    f'Métrica {metric_name} em nível crítico: {point.value}',
                    {'threshold': threshold['critical'], 'value': point.value}
                )
            elif point.value <= threshold['warning']:
                self.raise_alert(
                    'WARNING',
                    f'Métrica {metric_name} em nível de alerta: {point.value}',
                    {'threshold': threshold['warning'], 'value': point.value}
                )
    
    def persist_metrics(self, filepath: str) -> None:
        """Persiste métricas em disco"""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with self._lock:
            metrics_data = {
                name: [
                    {
                        'value': point.value,
                        'timestamp': point.timestamp.isoformat(),
                        'metadata': point.metadata
                    }
                    for point in points
                ]
                for name, points in self.metrics.items()
            }
            
            with open(filepath, 'w') as f:
                json.dump(metrics_data, f)
    
    def load_metrics(self, filepath: str) -> None:
        """Carrega métricas do disco"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            with self._lock:
                self.metrics = {
                    name: [
                        MetricPoint(
                            value=point['value'],
                            timestamp=datetime.fromisoformat(point['timestamp']),
                            metadata=point['metadata']
                        )
                        for point in points
                    ]
                    for name, points in data.items()
                }
        except FileNotFoundError:
            pass  # Ignora se arquivo não existe

# Exemplo de callback para Slack
def slack_alert_callback(alert: Alert) -> None:
    """Envia alerta para Slack"""
    # Implementação do envio para Slack aqui
    print(f"[SLACK] {alert.level}: {alert.message}")

# Exemplo de callback para email
def email_alert_callback(alert: Alert) -> None:
    """Envia alerta por email"""
    # Implementação do envio de email aqui
    print(f"[EMAIL] {alert.level}: {alert.message}")

# Exemplo de uso
def monitor_example():
    monitor = AdvancedMonitor()
    
    # Adiciona callbacks
    monitor.add_alert_callback(slack_alert_callback)
    monitor.add_alert_callback(email_alert_callback)
    
    # Registra algumas métricas
    monitor.record_metric('cultural_expression', 0.2)
    monitor.record_metric('style_consistency', 0.8)
    monitor.record_metric('cache_hit_rate', 0.6)
    
    # Gera um alerta manual
    monitor.raise_alert(
        'WARNING',
        'Detecção de padrão cultural incomum',
        {'pattern': 'spiral_attack'}
    )
    
    # Persiste métricas
    monitor.persist_metrics('metrics.json')
    
    return {
        'metrics': {
            name: len(points)
            for name, points in monitor.metrics.items()
        },
        'alerts': len(monitor.alerts)
    }

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
        if component not in self.component_metrics:
            self.component_metrics[component] = ComponentMetrics(
                component_name=component,
                execution_time=0.1,
                success_rate=0.95,
                error_count=2,
                last_execution=datetime.now()
            )
        return self.component_metrics[component]

    async def _collect_performance_metrics(self) -> PerformanceMetrics:
        """Coleta métricas de performance do sistema"""
        self.performance_metrics = PerformanceMetrics(
            moves_analyzed=1000,
            patterns_recognized=50,
            learning_iterations=100,
            adaptation_score=0.8,
            quantum_operations=20
        )
        return self.performance_metrics

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
        # Inicializa métricas se não existirem
        if component not in self.component_metrics:
            self.component_metrics[component] = ComponentMetrics(
                component_name=component,
                execution_time=0.1,
                success_rate=0.95,
                error_count=2,
                last_execution=datetime.now()
            )
        return self.component_metrics[component]
