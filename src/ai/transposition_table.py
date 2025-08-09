"""
Transposition Table e Advanced Evaluator para IA adaptativa
"""
from typing import Dict, Tuple, Optional, Any
from types import SimpleNamespace
import hashlib


class TranspositionTable:
    """Tabela de transposição para armazenar posições já avaliadas"""
    
    def __init__(self, max_size: int = 1000000):
        self.table: Dict[str, Tuple[float, int]] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get_hash(self, board: Any) -> str:
        """Gera hash único para uma posição do tabuleiro"""
        # Simplificado - em produção usaria Zobrist hashing
        board_str = str(board)
        return hashlib.md5(board_str.encode()).hexdigest()
    
    def lookup(self, board: Any, depth: int) -> Optional[float]:
        """Procura uma posição na tabela"""
        key = self.get_hash(board)
        if key in self.table:
            stored_score, stored_depth = self.table[key]
            if stored_depth >= depth:
                self.hits += 1
                return stored_score
        self.misses += 1
        return None
    
    def store(self, board: Any, score: float, depth: int):
        """Armazena uma avaliação na tabela"""
        key = self.get_hash(board)
        
        # Se a tabela está cheia, remove entradas antigas
        if len(self.table) >= self.max_size:
            # Remove 10% das entradas mais antigas
            to_remove = list(self.table.keys())[:int(self.max_size * 0.1)]
            for k in to_remove:
                del self.table[k]
        
        self.table[key] = (score, depth)
    
    def clear(self):
        """Limpa a tabela"""
        self.table.clear()
        self.hits = 0
        self.misses = 0
    
    def get_hit_rate(self) -> float:
        """Retorna a taxa de acerto da tabela"""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total


class AdvancedEvaluator:
    """Avaliador avançado de posições"""
    
    def __init__(self):
        self.feature_weights = {
            'material': 1.0,
            'mobility': 0.3,
            'king_safety': 0.5,
            'pawn_structure': 0.4,
            'piece_activity': 0.35,
            'center_control': 0.25
        }
    
    def evaluate(self, board: Any, color: Any) -> Tuple[float, Dict[str, float]]:
        """
        Avalia uma posição retornando score e features
        
        Returns:
            Tuple[float, Dict]: (score total, dicionário de features)
        """
        features = {}
        
        # Material (simplificado)
        features['material'] = self._evaluate_material(board, color)
        
        # Mobilidade
        features['mobility'] = self._evaluate_mobility(board, color)
        
        # Segurança do rei
        features['king_safety'] = self._evaluate_king_safety(board, color)
        
        # Estrutura de peões
        features['pawn_structure'] = self._evaluate_pawn_structure(board, color)
        
        # Atividade das peças
        features['piece_activity'] = self._evaluate_piece_activity(board, color)
        
        # Controle do centro
        features['center_control'] = self._evaluate_center_control(board, color)
        
        # Calcula score total ponderado
        total_score = sum(
            features[name] * weight 
            for name, weight in self.feature_weights.items()
        )
        
        return total_score, SimpleNamespace(**features)
    
    def _evaluate_material(self, board: Any, color: Any) -> float:
        """Avalia material"""
        # Valores padrão das peças
        piece_values = {
            'PAWN': 1.0,
            'KNIGHT': 3.0,
            'BISHOP': 3.2,
            'ROOK': 5.0,
            'QUEEN': 9.0,
            'KING': 0.0
        }
        
        score = 0.0
        if hasattr(board, 'piece_list'):
            for piece in board.piece_list:
                value = piece_values.get(piece.type.name, 0)
                if piece.color == color:
                    score += value
                else:
                    score -= value
        
        return score
    
    def _evaluate_mobility(self, board: Any, color: Any) -> float:
        """Avalia mobilidade das peças"""
        # Simplificado - conta movimentos possíveis
        return 0.0  # Placeholder
    
    def _evaluate_king_safety(self, board: Any, color: Any) -> float:
        """Avalia segurança do rei"""
        # Simplificado - verifica proteção do rei
        return 0.0  # Placeholder
    
    def _evaluate_pawn_structure(self, board: Any, color: Any) -> float:
        """Avalia estrutura de peões"""
        # Simplificado - verifica peões passados, isolados, etc
        return 0.0  # Placeholder
    
    def _evaluate_piece_activity(self, board: Any, color: Any) -> float:
        """Avalia atividade das peças"""
        # Simplificado - verifica desenvolvimento e posicionamento
        return 0.0  # Placeholder
    
    def _evaluate_center_control(self, board: Any, color: Any) -> float:
        """Avalia controle do centro"""
        # Simplificado - verifica controle das casas centrais
        return 0.0  # Placeholder
