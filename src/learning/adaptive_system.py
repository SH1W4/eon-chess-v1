from typing import Dict, List, Any
from dataclasses import dataclass
import chess
import numpy as np

@dataclass
class ArquimaxConfig:
    """Configuração do sistema ARQUIMAX."""
    capabilities: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = {
                'pattern_recognition': True,
                'adaptive_learning': True,
                'real_time_analysis': True,
                'strategic_planning': True
            }

class AdaptiveAnalyzer:
    """Analisador adaptativo com integração ARQUIMAX."""
    
    def __init__(self, learning_rate: float = 0.01):
        """Inicializa o analisador adaptativo.
        
        Args:
            learning_rate: Taxa de aprendizado para adaptação.
        """
        self.learning_rate = learning_rate
        self.arquimax_config = ArquimaxConfig()
        self.pattern_weights = {
            'center_control': 1.0,
            'development': 1.0,
            'pawn_structure': 1.0,
            'king_safety': 1.0,
            'material_balance': 1.0,
            'piece_activity': 1.0
        }
        
    def analyze_position(self, board: chess.Board) -> Dict[str, Any]:
        """Analisa uma posição do tabuleiro.
        
        Args:
            board: Objeto Board do python-chess.
            
        Returns:
            Dict com análise da posição.
        """
        # Extrai características da posição
        features = self._extract_features(board)
        
        # Identifica padrões
        patterns = self._identify_patterns(board, features)
        
        # Calcula score
        score = self._calculate_score(features, patterns)
        
        # Calcula confiança
        confidence = self._calculate_confidence(features, patterns)
        
        return {
            'features': features,
            'patterns': patterns,
            'score': score,
            'confidence': confidence
        }
    
    def _extract_features(self, board: chess.Board) -> Dict[str, float]:
        """Extrai características da posição."""
        features = {}
        
        # Material
        material_balance = 0
        for piece_type in chess.PIECE_TYPES:
            material_balance += len(board.pieces(piece_type, chess.WHITE))
            material_balance -= len(board.pieces(piece_type, chess.BLACK))
        features['material_balance'] = material_balance
        
        # Atividade das peças
        white_mobility = len(list(board.legal_moves))
        board.turn = chess.BLACK
        black_mobility = len(list(board.legal_moves))
        board.turn = chess.WHITE
        features['piece_activity'] = (white_mobility - black_mobility) / 20.0  # Normalizado
        
        return features
    
    def _identify_patterns(self, board: chess.Board, features: Dict[str, float]) -> List[str]:
        """Identifica padrões na posição."""
        patterns = []
        
        # Centro
        center_pieces = 0
        for square in [chess.E4, chess.D4, chess.E5, chess.D5]:
            piece = board.piece_at(square)
            if piece is not None:
                center_pieces += 1
        if center_pieces >= 2:
            patterns.append('center_control')
        
        # Desenvolvimento
        developed_pieces = 0
        for square in [chess.B1, chess.G1, chess.C1, chess.F1]:
            if board.piece_at(square) is None:
                developed_pieces += 1
        if developed_pieces >= 2:
            patterns.append('development')
        
        # Estrutura de peões
        pawn_files = set()
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.piece_type == chess.PAWN:
                pawn_files.add(chess.square_file(square))
        if len(pawn_files) >= 4:
            patterns.append('pawn_structure')
        
        return patterns
    
    def _calculate_score(self, features: Dict[str, float], patterns: List[str]) -> float:
        """Calcula score da posição."""
        score = 0.0
        
        # Contribuição das características
        for feature, value in features.items():
            if feature in self.pattern_weights:
                score += value * self.pattern_weights[feature]
        
        # Contribuição dos padrões
        for pattern in patterns:
            if pattern in self.pattern_weights:
                score += self.pattern_weights[pattern]
        
        # Normaliza para [-1, 1]
        return np.tanh(score)
    
    def _calculate_confidence(self, features: Dict[str, float], patterns: List[str]) -> float:
        """Calcula confiança na análise."""
        # Base na quantidade de características e padrões identificados
        feature_confidence = len(features) / 5.0  # Máximo esperado de 5 características
        pattern_confidence = len(patterns) / 3.0  # Máximo esperado de 3 padrões
        
        # Média ponderada
        confidence = 0.7 * feature_confidence + 0.3 * pattern_confidence
        
        # Limita entre 0 e 1
        return max(0.0, min(1.0, confidence))
