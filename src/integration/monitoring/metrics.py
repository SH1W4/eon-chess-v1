from typing import Dict, Any, List, Optional
import time
import logging
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class MetricPoint:
    """Ponto de métrica com valor e timestamp."""
    value: float
    timestamp: float = time.time()

class MetricsCollector:
    """Coletor de métricas do sistema de integração."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Configuração da coleta
        metrics_config = config.get("metricas", {})
        self.collection_enabled = True
        self.retention_days = metrics_config.get("retencao", 90)
        
        # Métricas por componente
        self.connector_metrics: Dict[str, Dict[str, List[MetricPoint]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.adapter_metrics: Dict[str, Dict[str, List[MetricPoint]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.system_metrics: Dict[str, List[MetricPoint]] = defaultdict(list)
        
        # Configuração do storage
        storage_config = metrics_config.get("storage", {})
        self.storage_type = storage_config.get("tipo", "victoria")
        self.storage_retention = storage_config.get("retencao", 90)
        
        # Inicialização do storage
        self._setup_storage()
    
    def _setup_storage(self):
        """Configura o storage de métricas."""
        try:
            if self.storage_type == "victoria":
                # Configurar VictoriaMetrics
                pass
            elif self.storage_type == "prometheus":
                # Configurar Prometheus
                pass
            else:
                logger.warning(f"Tipo de storage não suportado: {self.storage_type}")
                
        except Exception as e:
            logger.error(f"Erro ao configurar storage de métricas: {str(e)}")
    
    def record_connector_processing(
        self,
        connector_name: str,
        processing_time: Optional[float] = None
    ):
        """Registra início de processamento em um conector."""
        if not self.collection_enabled:
            return
            
        try:
            current_time = time.time()
            
            # Registra timestamp de início
            self.connector_metrics[connector_name]["processing_start"].append(
                MetricPoint(current_time)
            )
            
            # Registra tempo de processamento se fornecido
            if processing_time is not None:
                self.connector_metrics[connector_name]["processing_time"].append(
                    MetricPoint(processing_time)
                )
                
            # Limpa métricas antigas
            self._cleanup_old_metrics()
            
        except Exception as e:
            logger.error(
                f"Erro ao registrar processamento do conector {connector_name}: {str(e)}"
            )
    
    def record_connector_processed(
        self,
        connector_name: str,
        processing_time: Optional[float] = None
    ):
        """Registra conclusão de processamento em um conector."""
        if not self.collection_enabled:
            return
            
        try:
            current_time = time.time()
            
            # Registra timestamp de conclusão
            self.connector_metrics[connector_name]["processing_end"].append(
                MetricPoint(current_time)
            )
            
            # Calcula e registra tempo total de processamento
            if processing_time is not None:
                self.connector_metrics[connector_name]["total_time"].append(
                    MetricPoint(processing_time)
                )
            
            # Registra throughput
            self._update_throughput(connector_name)
            
            # Persiste métricas
            self._persist_metrics()
            
        except Exception as e:
            logger.error(
                f"Erro ao registrar conclusão do conector {connector_name}: {str(e)}"
            )
    
    def record_adapter_processing(
        self,
        adapter_name: str,
        processing_time: Optional[float] = None
    ):
        """Registra início de processamento em um adaptador."""
        if not self.collection_enabled:
            return
            
        try:
            current_time = time.time()
            
            # Registra timestamp de início
            self.adapter_metrics[adapter_name]["processing_start"].append(
                MetricPoint(current_time)
            )
            
            # Registra tempo de processamento se fornecido
            if processing_time is not None:
                self.adapter_metrics[adapter_name]["processing_time"].append(
                    MetricPoint(processing_time)
                )
            
            # Limpa métricas antigas
            self._cleanup_old_metrics()
            
        except Exception as e:
            logger.error(
                f"Erro ao registrar processamento do adaptador {adapter_name}: {str(e)}"
            )
    
    def record_adapter_processed(
        self,
        adapter_name: str,
        processing_time: Optional[float] = None
    ):
        """Registra conclusão de processamento em um adaptador."""
        if not self.collection_enabled:
            return
            
        try:
            current_time = time.time()
            
            # Registra timestamp de conclusão
            self.adapter_metrics[adapter_name]["processing_end"].append(
                MetricPoint(current_time)
            )
            
            # Calcula e registra tempo total de processamento
            if processing_time is not None:
                self.adapter_metrics[adapter_name]["total_time"].append(
                    MetricPoint(processing_time)
                )
            
            # Registra throughput
            self._update_throughput(adapter_name, is_adapter=True)
            
            # Persiste métricas
            self._persist_metrics()
            
        except Exception as e:
            logger.error(
                f"Erro ao registrar conclusão do adaptador {adapter_name}: {str(e)}"
            )
    
    def record_error(
        self,
        source: str,
        target: str,
        error: str
    ):
        """Registra um erro no sistema."""
        if not self.collection_enabled:
            return
            
        try:
            current_time = time.time()
            
            # Registra erro para source
            self._record_component_error(source, error, current_time)
            
            # Registra erro para target
            self._record_component_error(target, error, current_time)
            
            # Registra erro de sistema
            self.system_metrics["errors"].append(
                MetricPoint(1, current_time)
            )
            
            # Atualiza taxa de erro
            self._update_error_rate()
            
            # Persiste métricas
            self._persist_metrics()
            
        except Exception as e:
            logger.error(f"Erro ao registrar erro de sistema: {str(e)}")
    
    def _record_component_error(
        self,
        component: str,
        error: str,
        timestamp: float
    ):
        """Registra erro para um componente específico."""
        try:
            # Identifica tipo de componente
            if component in self.connector_metrics:
                metrics = self.connector_metrics[component]
            elif component in self.adapter_metrics:
                metrics = self.adapter_metrics[component]
            else:
                return
            
            # Registra erro
            metrics["errors"].append(MetricPoint(1, timestamp))
            metrics["last_error"] = error
            metrics["error_count"] = len(metrics["errors"])
            
            # Atualiza taxa de erro do componente
            total_ops = len(metrics.get("processing_end", []))
            if total_ops > 0:
                error_rate = len(metrics["errors"]) / total_ops
                metrics["error_rate"].append(
                    MetricPoint(error_rate, timestamp)
                )
            
        except Exception as e:
            logger.error(
                f"Erro ao registrar erro para componente {component}: {str(e)}"
            )
    
    def _update_throughput(
        self,
        component: str,
        is_adapter: bool = False
    ):
        """Atualiza métricas de throughput."""
        try:
            metrics = (
                self.adapter_metrics[component]
                if is_adapter
                else self.connector_metrics[component]
            )
            
            # Calcula throughput dos últimos 5 minutos
            current_time = time.time()
            window_start = current_time - 300  # 5 minutos
            
            recent_processed = [
                m for m in metrics["processing_end"]
                if m.timestamp > window_start
            ]
            
            throughput = len(recent_processed) / 300  # ops/s
            metrics["throughput"].append(
                MetricPoint(throughput, current_time)
            )
            
        except Exception as e:
            logger.error(f"Erro ao atualizar throughput: {str(e)}")
    
    def _update_error_rate(self):
        """Atualiza taxa de erro do sistema."""
        try:
            current_time = time.time()
            window_start = current_time - 300  # 5 minutos
            
            # Conta erros recentes
            recent_errors = [
                m for m in self.system_metrics["errors"]
                if m.timestamp > window_start
            ]
            
            # Conta operações recentes
            recent_ops = 0
            for metrics in self.connector_metrics.values():
                recent_ops += len([
                    m for m in metrics.get("processing_end", [])
                    if m.timestamp > window_start
                ])
            
            for metrics in self.adapter_metrics.values():
                recent_ops += len([
                    m for m in metrics.get("processing_end", [])
                    if m.timestamp > window_start
                ])
            
            # Calcula taxa de erro
            if recent_ops > 0:
                error_rate = len(recent_errors) / recent_ops
                self.system_metrics["error_rate"].append(
                    MetricPoint(error_rate, current_time)
                )
            
        except Exception as e:
            logger.error(f"Erro ao atualizar taxa de erro: {str(e)}")
    
    def _cleanup_old_metrics(self):
        """Remove métricas antigas."""
        try:
            cutoff_time = time.time() - (self.retention_days * 86400)
            
            # Limpa métricas de conectores
            for connector_metrics in self.connector_metrics.values():
                for metric_list in connector_metrics.values():
                    metric_list[:] = [
                        m for m in metric_list
                        if m.timestamp > cutoff_time
                    ]
            
            # Limpa métricas de adaptadores
            for adapter_metrics in self.adapter_metrics.values():
                for metric_list in adapter_metrics.values():
                    metric_list[:] = [
                        m for m in metric_list
                        if m.timestamp > cutoff_time
                    ]
            
            # Limpa métricas do sistema
            for metric_list in self.system_metrics.values():
                metric_list[:] = [
                    m for m in metric_list
                    if m.timestamp > cutoff_time
                ]
            
        except Exception as e:
            logger.error(f"Erro ao limpar métricas antigas: {str(e)}")
    
    def _persist_metrics(self):
        """Persiste métricas no storage configurado."""
        try:
            if self.storage_type == "victoria":
                self._persist_to_victoria()
            elif self.storage_type == "prometheus":
                self._persist_to_prometheus()
            
        except Exception as e:
            logger.error(f"Erro ao persistir métricas: {str(e)}")
    
    def _persist_to_victoria(self):
        """Persiste métricas no VictoriaMetrics."""
        # Implementar persistência no VictoriaMetrics
        pass
    
    def _persist_to_prometheus(self):
        """Persiste métricas no Prometheus."""
        # Implementar persistência no Prometheus
        pass
    
    def get_connector_metrics(self, connector_name: str) -> Dict[str, Any]:
        """Retorna métricas de um conector específico."""
        try:
            metrics = self.connector_metrics[connector_name]
            return self._process_component_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas do conector: {str(e)}")
            return {}
    
    def get_adapter_metrics(self, adapter_name: str) -> Dict[str, Any]:
        """Retorna métricas de um adaptador específico."""
        try:
            metrics = self.adapter_metrics[adapter_name]
            return self._process_component_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas do adaptador: {str(e)}")
            return {}
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais do sistema."""
        try:
            return {
                "system": self._process_system_metrics(),
                "connectors": {
                    name: self._process_component_metrics(metrics)
                    for name, metrics in self.connector_metrics.items()
                },
                "adapters": {
                    name: self._process_component_metrics(metrics)
                    for name, metrics in self.adapter_metrics.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter métricas atuais: {str(e)}")
            return {}
    
    def _process_component_metrics(
        self,
        metrics: Dict[str, List[MetricPoint]]
    ) -> Dict[str, Any]:
        """Processa métricas de um componente."""
        try:
            result = {}
            
            # Processa cada tipo de métrica
            for metric_type, values in metrics.items():
                if not values:
                    continue
                
                # Calcula estatísticas básicas
                if metric_type in ["processing_time", "total_time", "latency"]:
                    recent_values = [v.value for v in values[-100:]]
                    if recent_values:
                        result[metric_type] = {
                            "current": recent_values[-1],
                            "avg": sum(recent_values) / len(recent_values),
                            "min": min(recent_values),
                            "max": max(recent_values)
                        }
                
                # Processa métricas de erro
                elif metric_type in ["errors", "error_rate"]:
                    recent_values = [v.value for v in values[-100:]]
                    if recent_values:
                        result[metric_type] = recent_values[-1]
                
                # Processa throughput
                elif metric_type == "throughput":
                    recent_values = [v.value for v in values[-10:]]
                    if recent_values:
                        result[metric_type] = sum(recent_values) / len(recent_values)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao processar métricas de componente: {str(e)}")
            return {}
    
    def _process_system_metrics(self) -> Dict[str, Any]:
        """Processa métricas do sistema."""
        try:
            result = {}
            
            # Processa cada tipo de métrica
            for metric_type, values in self.system_metrics.items():
                if not values:
                    continue
                
                # Calcula taxa de erro do sistema
                if metric_type == "error_rate":
                    recent_values = [v.value for v in values[-100:]]
                    if recent_values:
                        result[metric_type] = sum(recent_values) / len(recent_values)
                
                # Conta total de erros
                elif metric_type == "errors":
                    result[metric_type] = len(values)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao processar métricas do sistema: {str(e)}")
            return {}
    
    def check_health(self) -> bool:
        """Verifica a saúde do sistema de métricas."""
        try:
            # Verifica se coleta está ativa
            if not self.collection_enabled:
                return False
            
            # Verifica conexão com storage
            if self.storage_type == "victoria":
                # Implementar verificação de conexão com VictoriaMetrics
                pass
            elif self.storage_type == "prometheus":
                # Implementar verificação de conexão com Prometheus
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar saúde das métricas: {str(e)}")
            return False
    
    def close(self):
        """Fecha conexões e persiste métricas finais."""
        try:
            # Persiste métricas finais
            self._persist_metrics()
            
            # Desativa coleta
            self.collection_enabled = False
            
            logger.info("Sistema de métricas fechado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao fechar sistema de métricas: {str(e)}")
            raise
