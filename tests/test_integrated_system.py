"""
Teste integrado do sistema de xadrez com NEXUS-ARQUIMAX.
"""
import pytest
import chess
import logging
from src.analysis.data_visualization import LichessIntegration, ChessVisualizer, GameMetrics
from src.learning.adaptive_system import AdaptiveAnalyzer
from dataclasses import dataclass
from typing import Dict, List
import time

@dataclass
class SystemMetrics:
    """Métricas do sistema integrado."""
    arquimax_capabilities: int
    arquimax_success_rate: float
    arquimax_execution_time: float
    nexus_connectors: int
    nexus_sync_rate: float
    nexus_convergence: float

class IntegratedTester:
    """Testador integrado do sistema."""
    
    def __init__(self):
        """Inicializa componentes do sistema."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Componentes principais
        self.analyzer = AdaptiveAnalyzer(
            stockfish_path="/opt/homebrew/bin/stockfish",
            learning_rate=0.01
        )
        self.visualizer = ChessVisualizer()
        
        # Métricas do sistema
        self.metrics = SystemMetrics(
            arquimax_capabilities=0,
            arquimax_success_rate=0.0,
            arquimax_execution_time=0.0,
            nexus_connectors=0,
            nexus_sync_rate=0.0,
            nexus_convergence=0.0
        )
    
    def run_integration_test(self):
        """Executa teste de integração completo."""
        self.logger.info("=== Iniciando Integração NEXUS-ARQUIMAX ===")
        
        # Fase 1: Ativação Híbrida
        self.logger.info("--- Fase 1: Ativação Híbrida ---")
        self._activate_hybrid_system()
        
        # Fase 2: Configuração Unificada
        self.logger.info("--- Fase 2: Configuração Unificada ---")
        self._setup_unified_configuration()
        
        # Fase 3: Monitoramento Integrado
        self.logger.info("--- Fase 3: Monitoramento Integrado ---")
        self._activate_monitoring()
        
        # Fase 4: Validação Cruzada
        self.logger.info("--- Fase 4: Validação Cruzada ---")
        self._cross_validate_system()
        
        # Fase 5: Análise Simbiótica
        self.logger.info("--- Fase 5: Análise Simbiótica ---")
        self._run_symbiotic_analysis()
        
        # Relatório Final
        self._generate_final_report()
    
    def _activate_hybrid_system(self):
        """Ativa sistema híbrido."""
        start_time = time.time()
        
        # Teste de abertura clássica
        board = chess.Board()
        
        # Ruy Lopez
        moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
        
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            board.push(move)
            
            # Análise adaptativa
            analysis = self.analyzer.analyze_position(board)
            
            # Atualiza métricas
            self.metrics.arquimax_capabilities += 1
            if analysis['confidence'] > 0.7:
                self.metrics.arquimax_success_rate += 1
        
        self.metrics.arquimax_execution_time = time.time() - start_time
        self.metrics.arquimax_success_rate /= len(moves)
    
    def _setup_unified_configuration(self):
        """Configura sistema unificado."""
        # Verifica configuração ARQUIMAX
        arquimax_config = self.analyzer.arquimax_config
        
        # Ativa conectores NEXUS
        self.metrics.nexus_connectors = sum([
            arquimax_config['capabilities']['pattern_recognition'],
            arquimax_config['capabilities']['adaptive_learning'],
            arquimax_config['capabilities']['real_time_analysis'],
            arquimax_config['capabilities']['strategic_planning']
        ])
    
    def _activate_monitoring(self):
        """Ativa monitoramento integrado."""
        board = chess.Board()
        
        # Siciliana
        moves = ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4"]
        
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            board.push(move)
            
            # Análise com monitoramento
            analysis = self.analyzer.analyze_position(board)
            
            # Atualiza métricas de sincronização
            self.metrics.nexus_sync_rate += analysis['confidence']
        
        self.metrics.nexus_sync_rate /= len(moves)
    
    def _cross_validate_system(self):
        """Realiza validação cruzada."""
        board = chess.Board()
        
        # Defesa Francesa
        moves = ["e2e4", "e7e6", "d2d4", "d7d5"]
        
        total_patterns = 0
        correct_patterns = 0
        success_rate = 0.0
        
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            board.push(move)
            
            # Análise com validação
            analysis = self.analyzer.analyze_position(board)
            
            # Conta padrões identificados
            patterns = analysis['patterns']
            total_patterns += len(patterns)
            
            # Valida padrões conhecidos
            for pattern in patterns:
                if pattern in ["center_control", "development", "pawn_structure"]:
                    correct_patterns += 1
            
            # Calcula taxa de sucesso para convergência
            success_rate += analysis['confidence']
        
        # Calcula convergência como média entre taxa de sucesso e identificação de padrões
        pattern_rate = correct_patterns / max(1, total_patterns)
        success_rate = success_rate / len(moves)
        self.metrics.nexus_convergence = (pattern_rate + success_rate) / 2
    
    def _run_symbiotic_analysis(self):
        """Executa análise simbiótica."""
        board = chess.Board()
        
        # Gambito da Dama
        moves = ["d2d4", "d7d5", "c2c4"]
        
        for move_uci in moves:
            move = chess.Move.from_uci(move_uci)
            board.push(move)
            
            # Análise completa
            analysis = self.analyzer.analyze_position(board)
            
            # Gera métricas para visualização
            metrics = GameMetrics(
                moves=len(moves),
                material_balance=[analysis['features']['material_balance']],
                position_scores=[analysis['score']],
                piece_activity=[analysis['features']['piece_activity']],
                tactical_opportunities=[len(analysis['patterns'])],
                strategic_patterns=analysis['patterns']
            )
            
            # Cria visualização
            self.visualizer.create_dashboard(metrics)
    
    def _generate_final_report(self):
        """Gera relatório final."""
        self.logger.info("=== Relatório de Integração ===")
        
        self.logger.info("Status ARQUIMAX:")
        self.logger.info(f"- Capacidades ativas: {self.metrics.arquimax_capabilities}/4")
        self.logger.info(f"- Taxa de sucesso: {self.metrics.arquimax_success_rate*100:.1f}%")
        self.logger.info(f"- Tempo de execução: {self.metrics.arquimax_execution_time:.2f} segundos")
        
        self.logger.info("Status NEXUS:")
        self.logger.info(f"- Conectores ativos: {self.metrics.nexus_connectors}/4")
        self.logger.info(f"- Sincronização: {self.metrics.nexus_sync_rate*100:.1f}%")
        self.logger.info(f"- Convergência: {self.metrics.nexus_convergence*100:.1f}%")
        
        self.logger.info("=== Integração NEXUS-ARQUIMAX Concluída ===")

def test_integrated_system():
    """Teste principal do sistema integrado."""
    tester = IntegratedTester()
    tester.run_integration_test()
    
    # Validações
    assert tester.metrics.arquimax_capabilities > 0
    assert tester.metrics.arquimax_success_rate > 0.5
    assert tester.metrics.arquimax_execution_time > 0
    assert tester.metrics.nexus_connectors > 0
    assert tester.metrics.nexus_sync_rate > 0.5
    assert tester.metrics.nexus_convergence > 0.3

if __name__ == "__main__":
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Executa teste
    test_integrated_system()
