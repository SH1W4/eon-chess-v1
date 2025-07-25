"""
Módulo de análise de jogadas.
Integra com ARQUIMAX para análise profunda de movimentos.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
import chess
import chess.engine
import numpy as np
from src.learning.adaptive_system import AdaptiveAnalyzer
from src.patterns.core import PatternAnalyzer

@dataclass
class MoveAnalysis:
    """Análise detalhada de um movimento."""
    move: chess.Move
    score: float
    evaluation: float
    patterns: List[str]
    tactical_value: float
    strategic_value: float
    complexity: float
    confidence: float

class MoveAnalyzer:
    """Analisador avançado de jogadas."""
    
    def __init__(self,
                 adaptive_analyzer: Optional[AdaptiveAnalyzer] = None,
                 pattern_analyzer: Optional[PatternAnalyzer] = None,
                 stockfish_path: Optional[str] = None):
        """
        Inicializa analisador.
        
        Args:
            adaptive_analyzer: Analisador adaptativo
            pattern_analyzer: Analisador de padrões
            stockfish_path: Caminho para Stockfish
        """
        self.adaptive_analyzer = adaptive_analyzer or AdaptiveAnalyzer()
        self.pattern_analyzer = pattern_analyzer or PatternAnalyzer()
        
        # Engine para validação
        self.engine = None
        if stockfish_path:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        
        # Cache de análises
        self.analysis_cache = {}
    
    def analyze_move(self, board: chess.Board, move: chess.Move) -> MoveAnalysis:
        """
        Analisa movimento específico.
        
        Args:
            board: Posição atual
            move: Movimento a analisar
            
        Returns:
            Análise detalhada do movimento
        """
        # Verifica cache
        cache_key = (board.fen(), move.uci())
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        # Faz movimento
        board.push(move)
        
        # Análise adaptativa
        adaptive_analysis = self.adaptive_analyzer.analyze_position(board)
        
        # Análise de padrões
        pattern_analysis = self.pattern_analyzer.analyze_position(board)
        
        # Validação com engine
        engine_score = 0.0
        if self.engine:
            result = self.engine.analyse(board, chess.engine.Limit(time=0.1))
            engine_score = result['score'].relative.score() / 100.0
        
        # Desfaz movimento
        board.pop()
        
        # Combina análises
        analysis = MoveAnalysis(
            move=move,
            score=adaptive_analysis['score'],
            evaluation=engine_score,
            patterns=pattern_analysis['patterns'],
            tactical_value=self._calculate_tactical_value(adaptive_analysis, pattern_analysis),
            strategic_value=self._calculate_strategic_value(adaptive_analysis, pattern_analysis),
            complexity=self._calculate_complexity(adaptive_analysis, pattern_analysis),
            confidence=adaptive_analysis['confidence']
        )
        
        # Atualiza cache
        self.analysis_cache[cache_key] = analysis
        
        return analysis
    
    def analyze_moves(self, board: chess.Board, moves: List[chess.Move]) -> List[MoveAnalysis]:
        """
        Analisa lista de movimentos.
        
        Args:
            board: Posição atual
            moves: Lista de movimentos
            
        Returns:
            Lista de análises
        """
        return [self.analyze_move(board, move) for move in moves]
    
    def analyze_position_moves(self, board: chess.Board) -> List[MoveAnalysis]:
        """
        Analisa todos os movimentos legais.
        
        Args:
            board: Posição atual
            
        Returns:
            Lista de análises
        """
        return self.analyze_moves(board, list(board.legal_moves))
    
    def get_best_moves(self, board: chess.Board, n: int = 3) -> List[MoveAnalysis]:
        """
        Retorna os n melhores movimentos.
        
        Args:
            board: Posição atual
            n: Número de movimentos
            
        Returns:
            Lista dos melhores movimentos
        """
        analyses = self.analyze_position_moves(board)
        return sorted(analyses, key=lambda x: x.score, reverse=True)[:n]
    
    def _calculate_tactical_value(self, adaptive_analysis: Dict, pattern_analysis: Dict) -> float:
        """Calcula valor tático do movimento."""
        tactical_patterns = [p for p in pattern_analysis['patterns'] 
                           if p in ['fork', 'pin', 'discovery', 'sacrifice']]
        
        return (
            len(tactical_patterns) * 0.2 +
            adaptive_analysis['features']['piece_activity'] * 0.3 +
            adaptive_analysis['features']['material_balance'] * 0.5
        )
    
    def _calculate_strategic_value(self, adaptive_analysis: Dict, pattern_analysis: Dict) -> float:
        """Calcula valor estratégico do movimento."""
        strategic_patterns = [p for p in pattern_analysis['patterns']
                            if p in ['center_control', 'pawn_structure', 'king_safety']]
        
        return (
            len(strategic_patterns) * 0.3 +
            adaptive_analysis['features']['center_control'] * 0.3 +
            adaptive_analysis['features']['king_safety'] * 0.2 +
            adaptive_analysis['features']['pawn_structure'] * 0.2
        )
    
    def _calculate_complexity(self, adaptive_analysis: Dict, pattern_analysis: Dict) -> float:
        """Calcula complexidade do movimento."""
        return (
            len(pattern_analysis['patterns']) * 0.4 +
            adaptive_analysis['features']['piece_activity'] * 0.3 +
            (1 - adaptive_analysis['confidence']) * 0.3
        )
    
    def close(self):
        """Fecha recursos."""
        if self.engine:
            self.engine.quit()
