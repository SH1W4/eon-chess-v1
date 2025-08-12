from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

@dataclass
class HealthMetric:
    """Métrica de saúde do sistema."""
    name: str
    value: float
    threshold: float
    status: str  # 'healthy', 'warning', 'critical'
    timestamp: datetime

@dataclass
class SystemAlert:
    """Alerta do sistema."""
    level: str  # 'info', 'warning', 'error', 'critical'
    message: str
    source: str
    timestamp: datetime
    metrics: Optional[Dict[str, float]] = None

class BaseMonitor:
    """Monitor base para todos os conectores."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.metrics: Dict[str, HealthMetric] = {}
        self.alerts: List[SystemAlert] = []
        self.recovery_attempts = 0
        self.max_recovery_attempts = 3
        self.check_interval = 60  # segundos
        
    async def start_monitoring(self):
        """Inicia o monitoramento contínuo."""
        self.logger.info(f"Iniciando monitoramento para {self.name}")
        while True:
            try:
                await self.check_health()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")
                await self.handle_error(str(e))
    
    async def check_health(self):
        """Verifica a saúde do sistema."""
        raise NotImplementedError("Implementar em subclasses")
    
    async def collect_metrics(self) -> Dict[str, float]:
        """Coleta métricas do sistema."""
        raise NotImplementedError("Implementar em subclasses")
    
    async def validate_state(self, state: Dict[str, Any]) -> bool:
        """Valida o estado do sistema."""
        raise NotImplementedError("Implementar em subclasses")
    
    async def handle_error(self, error: str):
        """Manipula erros do sistema."""
        alert = SystemAlert(
            level="error",
            message=error,
            source=self.name,
            timestamp=datetime.now()
        )
        self.alerts.append(alert)
        
        if self.recovery_attempts < self.max_recovery_attempts:
            self.recovery_attempts += 1
            await self.attempt_recovery()
        else:
            self.logger.critical(f"Máximo de tentativas de recuperação atingido para {self.name}")
    
    async def attempt_recovery(self):
        """Tenta recuperar o sistema após falha."""
        raise NotImplementedError("Implementar em subclasses")
    
    def add_metric(self, name: str, value: float, threshold: float):
        """Adiciona uma nova métrica."""
        status = self._calculate_status(value, threshold)
        metric = HealthMetric(
            name=name,
            value=value,
            threshold=threshold,
            status=status,
            timestamp=datetime.now()
        )
        self.metrics[name] = metric
        
        if status != "healthy":
            self._create_metric_alert(metric)
    
    def _calculate_status(self, value: float, threshold: float) -> str:
        """Calcula o status com base no valor e threshold."""
        if value >= threshold:
            return "healthy"
        elif value >= threshold * 0.7:
            return "warning"
        else:
            return "critical"
    
    def _create_metric_alert(self, metric: HealthMetric):
        """Cria um alerta baseado em uma métrica."""
        alert = SystemAlert(
            level="warning" if metric.status == "warning" else "critical",
            message=f"Métrica {metric.name} em estado {metric.status}: {metric.value}",
            source=self.name,
            timestamp=datetime.now(),
            metrics={metric.name: metric.value}
        )
        self.alerts.append(alert)
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Retorna um resumo do estado de saúde."""
        return {
            "name": self.name,
            "status": self._calculate_overall_status(),
            "metrics": {name: metric.__dict__ for name, metric in self.metrics.items()},
            "alerts": [alert.__dict__ for alert in self.alerts[-5:]],  # últimos 5 alertas
            "recovery_attempts": self.recovery_attempts
        }
    
    def _calculate_overall_status(self) -> str:
        """Calcula o status geral do sistema."""
        if not self.metrics:
            return "unknown"
            
        statuses = [metric.status for metric in self.metrics.values()]
        if any(status == "critical" for status in statuses):
            return "critical"
        elif any(status == "warning" for status in statuses):
            return "warning"
        else:
            return "healthy"
