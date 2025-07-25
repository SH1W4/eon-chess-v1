"""
Módulo central do NEXUS.
Responsável pela integração e orquestração dos componentes.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import time
import logging
import chess
from src.learning.adaptive_system import AdaptiveAnalyzer
from src.patterns.core import PatternAnalyzer
from src.narrative.engine import NarrativeEngine
from src.analysis.move_analyzer import MoveAnalyzer

# Configuração de logging
logger = logging.getLogger(__name__)

@dataclass
class NexusMetrics:
    """Métricas do NEXUS."""
    total_requests: int = 0
    success_rate: float = 0.0
    response_time: float = 0.0
    error_rate: float = 0.0
    component_health: Dict[str, float] = None
    sync_rate: float = 0.0
    convergence: float = 0.0

class ComponentConnector:
    """Conector de componente do NEXUS."""
    
    def __init__(self, name: str, component: Any):
        self.name = name
        self.component = component
        self.is_active = False
        self.last_sync = 0
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'response_time': 0.0
        }
    
    def activate(self):
        """Ativa conector."""
        self.is_active = True
    
    def deactivate(self):
        """Desativa conector."""
        self.is_active = False
    
    def sync(self):
        """Sincroniza conector."""
        self.last_sync = time.time()
    
    def update_metrics(self, success: bool, response_time: float):
        """Atualiza métricas do conector."""
        self.metrics['requests'] += 1
        if not success:
            self.metrics['errors'] += 1
        self.metrics['response_time'] = (
            (self.metrics['response_time'] * (self.metrics['requests'] - 1) + response_time)
            / self.metrics['requests']
        )

class NexusCore:
    """Núcleo do sistema NEXUS."""
    
    def __init__(self,
                 config_path: str = 'config/nexus_config.yaml',
                 stockfish_path: Optional[str] = None):
        """
        Inicializa núcleo NEXUS.
        
        Args:
            config_path: Caminho configuração
            stockfish_path: Caminho Stockfish
        """
        # Componentes principais
        self.adaptive_analyzer = AdaptiveAnalyzer(
            stockfish_path=stockfish_path
        )
        self.pattern_analyzer = PatternAnalyzer()
        self.narrative_engine = NarrativeEngine(
            config_path='src/narrative/chess_config.yaml',
            patterns_path='src/narrative/chess_patterns.yaml',
            history_path='src/narrative/chess_tactics_history.yaml'
        )
        self.move_analyzer = MoveAnalyzer(
            adaptive_analyzer=self.adaptive_analyzer,
            pattern_analyzer=self.pattern_analyzer,
            stockfish_path=stockfish_path
        )
        
        # Conectores
        self.connectors = {
            'adaptive': ComponentConnector('adaptive', self.adaptive_analyzer),
            'pattern': ComponentConnector('pattern', self.pattern_analyzer),
            'narrative': ComponentConnector('narrative', self.narrative_engine),
            'move': ComponentConnector('move', self.move_analyzer)
        }
        
        # Métricas
        self.metrics = NexusMetrics(
            component_health={name: 1.0 for name in self.connectors}
        )
        
        # Estado
        self.is_active = False
        self.start_time = None
    
    def activate(self):
        """Ativa sistema NEXUS."""
        logger.info("Ativando NEXUS...")
        
        # Ativa conectores
        for connector in self.connectors.values():
            connector.activate()
            connector.sync()
        
        self.is_active = True
        self.start_time = time.time()
        
        logger.info("NEXUS ativado com sucesso")
    
    def deactivate(self):
        """Desativa sistema NEXUS."""
        logger.info("Desativando NEXUS...")
        
        # Desativa conectores
        for connector in self.connectors.values():
            connector.deactivate()
        
        self.is_active = False
        
        logger.info("NEXUS desativado")
    
    def analyze_position(self, board: chess.Board) -> Dict:
        """
        Analisa posição integrando todos os componentes.
        
        Args:
            board: Posição atual
            
        Returns:
            Análise integrada
        """
        if not self.is_active:
            raise RuntimeError("NEXUS não está ativo")
        
        start_time = time.time()
        
        try:
            # Análise adaptativa
            adaptive_analysis = self._execute_component(
                'adaptive',
                lambda: self.adaptive_analyzer.analyze_position(board)
            )
            
            # Análise de padrões
            pattern_analysis = self._execute_component(
                'pattern',
                lambda: self.pattern_analyzer.analyze_position(board)
            )
            
            # Análise de movimentos
            move_analysis = self._execute_component(
                'move',
                lambda: self.move_analyzer.get_best_moves(board)
            )
            
            # Geração de narrativa
            narrative = self._execute_component(
                'narrative',
                lambda: self.narrative_engine.generate_position_narrative(board)
            )
            
            # Integra resultados
            analysis = {
                'evaluation': adaptive_analysis['score'],
                'features': adaptive_analysis['features'],
                'patterns': pattern_analysis['patterns'],
                'best_moves': [
                    {
                        'move': ma.move.uci(),
                        'score': ma.score,
                        'evaluation': ma.evaluation,
                        'tactical_value': ma.tactical_value,
                        'strategic_value': ma.strategic_value,
                        'complexity': ma.complexity
                    }
                    for ma in move_analysis
                ],
                'narrative': narrative,
                'confidence': adaptive_analysis['confidence'],
                'analysis_time': time.time() - start_time
            }
            
            # Atualiza métricas
            self._update_metrics(True, time.time() - start_time)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise: {str(e)}")
            self._update_metrics(False, time.time() - start_time)
            raise
    
    def _execute_component(self, name: str, operation: callable) -> Any:
        """Executa operação em componente com métricas."""
        if not self.connectors[name].is_active:
            raise RuntimeError(f"Componente {name} não está ativo")
        
        start_time = time.time()
        try:
            result = operation()
            self.connectors[name].update_metrics(True, time.time() - start_time)
            return result
        except Exception as e:
            self.connectors[name].update_metrics(False, time.time() - start_time)
            raise
    
    def _update_metrics(self, success: bool, response_time: float):
        """Atualiza métricas do sistema."""
        self.metrics.total_requests += 1
        
        if success:
            self.metrics.success_rate = (
                (self.metrics.success_rate * (self.metrics.total_requests - 1) + 1)
                / self.metrics.total_requests
            )
        else:
            self.metrics.error_rate = (
                (self.metrics.error_rate * (self.metrics.total_requests - 1) + 1)
                / self.metrics.total_requests
            )
        
        self.metrics.response_time = (
            (self.metrics.response_time * (self.metrics.total_requests - 1) + response_time)
            / self.metrics.total_requests
        )
        
        # Atualiza saúde dos componentes
        for name, connector in self.connectors.items():
            if connector.metrics['requests'] > 0:
                self.metrics.component_health[name] = 1 - (
                    connector.metrics['errors'] / connector.metrics['requests']
                )
        
        # Calcula taxa de sincronização
        current_time = time.time()
        sync_threshold = 5.0  # 5 segundos
        synced_components = sum(
            1 for c in self.connectors.values()
            if c.is_active and (current_time - c.last_sync) < sync_threshold
        )
        self.metrics.sync_rate = synced_components / len(self.connectors)
        
        # Calcula convergência
        self.metrics.convergence = (
            self.metrics.success_rate * 0.4 +
            self.metrics.sync_rate * 0.3 +
            (sum(self.metrics.component_health.values()) / len(self.connectors)) * 0.3
        )
    
    def get_metrics(self) -> NexusMetrics:
        """Retorna métricas atuais."""
        return self.metrics
    
    def close(self):
        """Fecha recursos."""
        self.deactivate()
        self.move_analyzer.close()
