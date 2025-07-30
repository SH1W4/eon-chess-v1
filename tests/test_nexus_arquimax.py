"""
Teste integrado do sistema NEXUS-ARQUIMAX.
Implementa o workflow completo de integração.
"""
import pytest
import chess
import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from src.nexus.core import NexusCore
from src.arquimax.config import ArquimaxConfigManager
from src.patterns.core import PatternAnalyzer
from src.analysis.move_analyzer import MoveAnalyzer

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IntegrationMetrics:
    """Métricas da integração."""
    # Métricas ARQUIMAX
    arquimax_active_capabilities: int = 0
    arquimax_success_rate: float = 0.0
    arquimax_execution_time: float = 0.0
    arquimax_health_status: Dict[str, float] = None
    
    # Métricas NEXUS
    nexus_active_connectors: int = 0
    nexus_sync_rate: float = 0.0
    nexus_convergence: float = 0.0
    nexus_response_time: float = 0.0

class IntegrationTester:
    """Testador da integração NEXUS-ARQUIMAX."""
    
    def __init__(self, stockfish_path: Optional[str] = None):
        """
        Inicializa testador.
        
        Args:
            stockfish_path: Caminho para Stockfish
        """
        # Componentes principais
        self.nexus = NexusCore()
        self.config_manager = ArquimaxConfigManager()
        
        # Estado do teste
        self.start_time = None
        self.metrics = IntegrationMetrics(
            arquimax_health_status={}
        )
        
        # Posições de teste
        self.test_positions = self._create_test_positions()
    
    def run_integration_test(self):
        """Executa teste de integração completo."""
        self.start_time = time.time()
        logger.info("=== Iniciando Integração NEXUS-ARQUIMAX ===")
        
        try:
            # Fase 1: Ativação Híbrida
            self._run_hybrid_activation()
            
            # Fase 2: Configuração Unificada
            self._run_unified_configuration()
            
            # Fase 3: Monitoramento Integrado
            self._run_integrated_monitoring()
            
            # Fase 4: Validação Cruzada
            self._run_cross_validation()
            
            # Fase 5: Análise Simbiótica
            self._run_symbiotic_analysis()
            
            # Relatório final
            self._generate_final_report()
            
            # Validações finais
            self._validate_integration()
            
        finally:
            self.nexus.close()
    
    def _run_hybrid_activation(self):
        """Fase 1: Ativação Híbrida."""
        logger.info("--- Fase 1: Ativação Híbrida ---")
        
        # Ativa NEXUS
        self.nexus.activate()
        self.metrics.nexus_active_connectors = len(self.nexus.connectors)
        
        # Valida configuração ARQUIMAX
        config = self.config_manager.get_config()
        active_capabilities = sum(1 for cap, enabled in config.capabilities.__dict__.items() 
                                if enabled)
        self.metrics.arquimax_active_capabilities = active_capabilities
        
        assert self.nexus.is_active, "NEXUS não está ativo"
        assert self.config_manager.validate_config(), "Configuração ARQUIMAX inválida"
    
    def _run_unified_configuration(self):
        """Fase 2: Configuração Unificada."""
        logger.info("--- Fase 2: Configuração Unificada ---")
        
        # Configuração de monitoramento
        monitoring_config = {
            'accuracy_threshold': 0.75,
            'adaptation_rate': 0.2,
            'sampling_rate': 2.0
        }
        self.config_manager.update_config(monitoring=monitoring_config)
        
        # Validação de configuração
        assert self.config_manager.validate_config(), "Configuração inválida após atualização"
    
    def _run_integrated_monitoring(self):
        """Fase 3: Monitoramento Integrado."""
        logger.info("--- Fase 3: Monitoramento Integrado ---")
        
        # Análise inicial
        for position in self.test_positions[:2]:  # Teste parcial
            analysis = self.nexus.analyze_position(position)
            
            # Valida análise
            assert 'evaluation' in analysis, "Análise sem avaliação"
            assert 'patterns' in analysis, "Análise sem padrões"
            assert 'best_moves' in analysis, "Análise sem melhores lances"
            
            # Atualiza métricas
            self.metrics.nexus_response_time += analysis['analysis_time']
        
        self.metrics.nexus_response_time /= 2
    
    def _run_cross_validation(self):
        """Fase 4: Validação Cruzada."""
        logger.info("--- Fase 4: Validação Cruzada ---")
        
        success_count = 0
        total_tests = len(self.test_positions)
        
        for position in self.test_positions:
            try:
                # Análise NEXUS
                nexus_analysis = self.nexus.analyze_position(position)
                
                # Validações básicas
                if (nexus_analysis['confidence'] > 0.6 and
                    len(nexus_analysis['patterns']) > 0 and
                    len(nexus_analysis['best_moves']) > 0):
                    success_count += 1
                
            except Exception as e:
                logger.error(f"Erro na validação: {str(e)}")
        
        self.metrics.arquimax_success_rate = success_count / total_tests
    
    def _run_symbiotic_analysis(self):
        """Fase 5: Análise Simbiótica."""
        logger.info("--- Fase 5: Análise Simbiótica ---")
        
        # Coleta métricas NEXUS
        nexus_metrics = self.nexus.get_metrics()
        self.metrics.nexus_sync_rate = nexus_metrics.sync_rate
        self.metrics.nexus_convergence = nexus_metrics.convergence
        
        # Métricas de saúde
        for name, connector in self.nexus.connectors.items():
            self.metrics.arquimax_health_status[name] = (
                1.0 - (connector.metrics['errors'] / max(1, connector.metrics['requests']))
            )
        
        self.metrics.arquimax_execution_time = time.time() - self.start_time
    
    def _generate_final_report(self):
        """Gera relatório final."""
        logger.info("=== Relatório de Integração ===")
        
        logger.info("Status ARQUIMAX:")
        logger.info(f"- Capacidades ativas: {self.metrics.arquimax_active_capabilities}/6")
        logger.info(f"- Taxa de sucesso: {self.metrics.arquimax_success_rate*100:.1f}%")
        logger.info(f"- Tempo de execução: {self.metrics.arquimax_execution_time:.2f} segundos")
        
        logger.info("Status NEXUS:")
        logger.info(f"- Conectores ativos: {self.metrics.nexus_active_connectors}/4")
        logger.info(f"- Sincronização: {self.metrics.nexus_sync_rate*100:.1f}%")
        logger.info(f"- Convergência: {self.metrics.nexus_convergence*100:.1f}%")
        
        logger.info("=== Integração NEXUS-ARQUIMAX Concluída ===")
    
    def _validate_integration(self):
        """Validações finais da integração."""
        assert self.metrics.arquimax_active_capabilities >= 4, "Poucas capacidades ativas"
        assert self.metrics.arquimax_success_rate > 0.7, "Taxa de sucesso baixa"
        assert self.metrics.nexus_active_connectors >= 3, "Poucos conectores ativos"
        assert self.metrics.nexus_sync_rate > 0.6, "Taxa de sincronização baixa"
        assert self.metrics.nexus_convergence > 0.5, "Convergência baixa"
        assert all(health > 0.7 for health in self.metrics.arquimax_health_status.values()), \
            "Saúde do sistema comprometida"
    
    def _create_test_positions(self) -> List[chess.Board]:
        """Cria posições de teste."""
        positions = []
        
        # Posição inicial
        positions.append(chess.Board())
        
        # Ruy Lopez
        board = chess.Board()
        moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
        for move in moves:
            board.push(chess.Move.from_uci(move))
        positions.append(board.copy())
        
        # Siciliana
        board = chess.Board()
        moves = ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4"]
        for move in moves:
            board.push(chess.Move.from_uci(move))
        positions.append(board.copy())
        
        # Gambito da Dama
        board = chess.Board()
        moves = ["d2d4", "d7d5", "c2c4"]
        for move in moves:
            board.push(chess.Move.from_uci(move))
        positions.append(board.copy())
        
        return positions

def test_nexus_arquimax_integration():
    """Teste principal da integração."""
    stockfish_path = "/opt/homebrew/bin/stockfish"  # Ajuste conforme necessário
    tester = IntegrationTester(stockfish_path=stockfish_path)
    tester.run_integration_test()
