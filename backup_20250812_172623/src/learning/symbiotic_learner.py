from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import logging
from core.board.board import Board, Position, Piece
from arquimax.chess_integration import PositionAnalysis, ARQUIMAXChessIntegrator

@dataclass
class LearningMetrics:
    adaptation_rate: float
    pattern_recognition: float
    evolution_score: float
    convergence_rate: float

@dataclass
class PositionPattern:
    features: np.ndarray
    evaluation: float
    frequency: int
    success_rate: float

class SymbioticLearner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.arquimax = ARQUIMAXChessIntegrator()
        self.position_patterns: Dict[str, PositionPattern] = {}
        self.learning_rate = 0.1
        self.pattern_threshold = 0.7
        self.metrics = LearningMetrics(0.0, 0.0, 0.0, 0.0)

    async def learn_from_position(self, board: Board, analysis: PositionAnalysis) -> LearningMetrics:
        """Aprende a partir de uma posição analisada"""
        self.logger.info("Iniciando aprendizado simbiótico da posição")

        # Extrai características da posição
        features = await self._extract_position_features(board)
        
        # Identifica ou cria padrão
        pattern_key = self._get_pattern_key(features)
        if pattern_key in self.position_patterns:
            pattern = self.position_patterns[pattern_key]
            await self._update_pattern(pattern, analysis)
        else:
            pattern = await self._create_new_pattern(features, analysis)
            self.position_patterns[pattern_key] = pattern

        # Atualiza métricas de aprendizado
        await self._update_learning_metrics(pattern)
        
        return self.metrics

    async def _extract_position_features(self, board: Board) -> np.ndarray:
        """Extrai características relevantes da posição"""
        features = []
        
        # Material balance
        features.extend(await self._extract_material_features(board))
        
        # Piece positions
        features.extend(await self._extract_position_features_array(board))
        
        # Control and activity
        features.extend(await self._extract_control_features(board))
        
        return np.array(features)

    async def _extract_material_features(self, board: Board) -> List[float]:
        """Extrai características relacionadas ao material"""
        piece_counts = {
            'wp': 0, 'wn': 0, 'wb': 0, 'wr': 0, 'wq': 0,
            'bp': 0, 'bn': 0, 'bb': 0, 'br': 0, 'bq': 0
        }
        
        for piece in board.pieces.values():
            key = ('w' if piece.color.value == 'white' else 'b') + piece.type.value[0].lower()
            if key in piece_counts:
                piece_counts[key] += 1
                
        return list(piece_counts.values())

    async def _extract_position_features_array(self, board: Board) -> List[float]:
        """Extrai características posicionais em formato de array"""
        features = []
        for rank in range(1, 9):
            for file in range(1, 9):
                pos = Position(rank, file)
                piece = board.get_piece(pos)
                if piece:
                    # Codifica a peça e sua cor
                    piece_value = (1 if piece.color.value == 'white' else -1) * \
                                (1 + list(piece.type.__class__.__members__.keys()).index(piece.type.name))
                else:
                    piece_value = 0
                features.append(piece_value)
        return features

    async def _extract_control_features(self, board: Board) -> List[float]:
        """Extrai características de controle do tabuleiro"""
        features = []
        
        # Centro control
        center_control = await self._calculate_center_control(board)
        features.append(center_control)
        
        # Piece activity
        piece_activity = await self._calculate_piece_activity(board)
        features.append(piece_activity)
        
        # King safety
        king_safety = await self._calculate_king_safety(board)
        features.append(king_safety)
        
        return features

    async def _calculate_center_control(self, board: Board) -> float:
        """Calcula o controle do centro"""
        center_squares = [
            Position(4, 4), Position(4, 5),
            Position(5, 4), Position(5, 5)
        ]
        
        white_control = sum(1 for pos in center_squares if board.is_square_attacked(pos, 'white'))
        black_control = sum(1 for pos in center_squares if board.is_square_attacked(pos, 'black'))
        
        return (white_control - black_control) / 4.0

    async def _calculate_piece_activity(self, board: Board) -> float:
        """Calcula a atividade das peças"""
        white_moves = len(board.get_valid_moves('white'))
        black_moves = len(board.get_valid_moves('black'))
        
        return (white_moves - black_moves) / (white_moves + black_moves + 1)

    async def _calculate_king_safety(self, board: Board) -> float:
        """Calcula a segurança dos reis"""
        # Implementação simplificada - pode ser expandida
        return 0.0

    async def _update_pattern(self, pattern: PositionPattern, analysis: PositionAnalysis):
        """Atualiza um padrão existente"""
        pattern.frequency += 1
        pattern.evaluation = (pattern.evaluation * (pattern.frequency - 1) + 
                            analysis.score) / pattern.frequency
        
        # Atualiza taxa de sucesso baseado na análise
        success_factor = analysis.winning_chances * analysis.complexity
        pattern.success_rate = (pattern.success_rate * (pattern.frequency - 1) + 
                              success_factor) / pattern.frequency

    async def _create_new_pattern(self, features: np.ndarray, analysis: PositionAnalysis) -> PositionPattern:
        """Cria um novo padrão"""
        return PositionPattern(
            features=features,
            evaluation=analysis.score,
            frequency=1,
            success_rate=analysis.winning_chances
        )

    async def _update_learning_metrics(self, pattern: PositionPattern):
        """Atualiza métricas de aprendizado"""
        # Adaptation rate
        self.metrics.adaptation_rate = min(pattern.frequency / 100, 1.0)
        
        # Pattern recognition
        self.metrics.pattern_recognition = len(self.position_patterns) / 1000
        
        # Evolution score
        self.metrics.evolution_score = pattern.success_rate
        
        # Convergence rate
        total_patterns = len(self.position_patterns)
        stable_patterns = sum(1 for p in self.position_patterns.values() 
                            if p.frequency > 5 and p.success_rate > 0.6)
        self.metrics.convergence_rate = stable_patterns / (total_patterns + 1)

    def _get_pattern_key(self, features: np.ndarray) -> str:
        """Gera uma chave única para um padrão"""
        return str(hash(features.tobytes()))
