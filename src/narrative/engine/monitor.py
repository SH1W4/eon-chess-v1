#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Monitoramento do Motor Narrativo AEON
"""

import logging
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class MonitorConfig:
    """Configuração do sistema de monitoramento"""
    metrics_enabled: bool = True
    alert_enabled: bool = True
    performance_tracking: bool = True
    log_level: str = "INFO"
    alert_threshold: float = 0.75

class Monitor:
    """Sistema de monitoramento e métricas"""
    
    def __init__(self, config: Optional[MonitorConfig] = None):
        self.config = config or MonitorConfig()
        self.initialized = False
        self.metrics = {}
        self.alerts = []
        self.start_time = None
        logger.info("Inicializando Sistema de Monitoramento...")
    
    def initialize(self, mode: str = "standard") -> bool:
        """Inicializa o sistema de monitoramento"""
        try:
            logger.info(f"Iniciando monitoramento no modo: {mode}")
            self._setup_metrics()
            self._initialize_alert_system()
            self._setup_performance_tracking()
            self.start_time = datetime.now()
            self.initialized = True
            logger.info("Sistema de monitoramento inicializado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro na inicialização: {e}")
            return False
    
    def _setup_metrics(self):
        """Configura sistema de métricas"""
        if self.config.metrics_enabled:
            logger.info("Configurando sistema de métricas...")
            self.metrics = {
                "performance": {
                    "response_time": [],
                    "processing_time": [],
                    "memory_usage": []
                },
                "quality": {
                    "narrative_coherence": [],
                    "cultural_relevance": [],
                    "adaptation_rate": []
                },
                "system": {
                    "uptime": 0,
                    "total_requests": 0,
                    "error_count": 0
                }
            }
    
    def _initialize_alert_system(self):
        """Inicializa sistema de alertas"""
        if self.config.alert_enabled:
            logger.info("Inicializando sistema de alertas...")
            # Implementar sistema de alertas
            pass
    
    def _setup_performance_tracking(self):
        """Configura tracking de performance"""
        if self.config.performance_tracking:
            logger.info("Configurando tracking de performance...")
            # Implementar tracking de performance
            pass
    
    def record_metric(self, category: str, name: str, value: float):
        """Registra uma métrica
        - Para métricas baseadas em lista, usa append
        - Para contadores numéricos (int/float), realiza incremento cumulativo
        """
        if not self.initialized or not self.config.metrics_enabled:
            return
        
        try:
            if category in self.metrics and name in self.metrics[category]:
                current = self.metrics[category][name]
                if isinstance(current, list):
                    current.append(value)
                elif isinstance(current, (int, float)):
                    # Incrementa contadores numéricos com o valor informado
                    self.metrics[category][name] = current + value
                else:
                    # Caso métrica tenha tipo inesperado, substitui pelo valor
                    self.metrics[category][name] = value
                logger.debug(f"Métrica registrada: {category}.{name} = {value}")
        except Exception as e:
            logger.error(f"Erro ao registrar métrica: {e}")
    
    def check_alerts(self) -> List[Dict]:
        """Verifica e retorna alertas ativos"""
        if not self.initialized or not self.config.alert_enabled:
            return []
        
        current_alerts = []
        try:
            # Verificar métricas de performance
            if self.metrics["performance"]["response_time"]:
                avg_response = sum(self.metrics["performance"]["response_time"]) / \
                             len(self.metrics["performance"]["response_time"])
                if avg_response > self.config.alert_threshold:
                    current_alerts.append({
                        "type": "performance",
                        "metric": "response_time",
                        "value": avg_response,
                        "threshold": self.config.alert_threshold,
                        "timestamp": datetime.now()
                    })
            
            # Verificar métricas de qualidade
            if self.metrics["quality"]["narrative_coherence"]:
                avg_coherence = sum(self.metrics["quality"]["narrative_coherence"]) / \
                               len(self.metrics["quality"]["narrative_coherence"])
                if avg_coherence < self.config.alert_threshold:
                    current_alerts.append({
                        "type": "quality",
                        "metric": "narrative_coherence",
                        "value": avg_coherence,
                        "threshold": self.config.alert_threshold,
                        "timestamp": datetime.now()
                    })
        except Exception as e:
            logger.error(f"Erro ao verificar alertas: {e}")
        
        return current_alerts
    
    def get_metrics_summary(self) -> Dict:
        """Retorna resumo das métricas"""
        if not self.initialized:
            return {}
        
        summary = {}
        try:
            for category in self.metrics:
                summary[category] = {}
                for metric, values in self.metrics[category].items():
                    if isinstance(values, list) and values:
                        summary[category][metric] = {
                            "current": values[-1],
                            "average": sum(values) / len(values),
                            "min": min(values),
                            "max": max(values)
                        }
                    else:
                        summary[category][metric] = values
        except Exception as e:
            logger.error(f"Erro ao gerar resumo de métricas: {e}")
        
        return summary
    
    def get_status(self) -> Dict:
        """Retorna status atual do monitor"""
        return {
            "initialized": self.initialized,
            "metrics_enabled": self.config.metrics_enabled,
            "alert_enabled": self.config.alert_enabled,
            "performance_tracking": self.config.performance_tracking,
            "uptime": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "active_alerts": len(self.check_alerts())
        }
    
    def cleanup(self):
        """Limpa recursos do monitor"""
        logger.info("Finalizando monitoramento...")
        self.metrics.clear()
        self.alerts.clear()
        self.initialized = False
