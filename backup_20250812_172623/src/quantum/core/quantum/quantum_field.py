"""Implementação do campo quântico para o sistema de xadrez"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
try:
    from src.traditional.models import Position, Piece, PieceType, Color
except Exception:
    from src.traditional.models.models import Position, Piece, PieceType, Color

# Constantes
DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),  # Ortogonais
    (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonais
]

KNIGHT_MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]

# Thresholds for piece influence
INFLUENCE_THRESHOLD = 0.3  # Piece can move to square
ATTACK_THRESHOLD = 0.3     # Piece can attack/capture on square
CONTROL_THRESHOLD = 0.2    # Piece exerts control over square

class QuantumField:
    """Campo quântico que representa a influência das peças no tabuleiro"""
    
    def __init__(self):
        """Inicializa o campo quântico"""
        self.white_influence = np.zeros((8, 8))
        self.black_influence = np.zeros((8, 8))
        self.piece_fields: Dict[Position, np.ndarray] = {}
        
    def calculate_piece_field(self, piece: Piece) -> np.ndarray:
        """Calcula o campo de influência de uma peça específica"""
        field = np.zeros((8, 8))
        
        if piece.type == PieceType.PAWN:
            self._add_pawn_field(field, piece)
        elif piece.type == PieceType.KNIGHT:
            self._add_knight_field(field, piece)
        elif piece.type == PieceType.BISHOP:
            self._add_sliding_field(field, piece, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
        elif piece.type == PieceType.ROOK:
            self._add_sliding_field(field, piece, [(0, 1), (0, -1), (1, 0), (-1, 0)])
        elif piece.type == PieceType.QUEEN:
            self._add_sliding_field(field, piece, DIRECTIONS)
        elif piece.type == PieceType.KING:
            self._add_king_field(field, piece)
            
        return field
    
    def _add_pawn_field(self, field: np.ndarray, piece: Piece):
        """Adiciona campo de influência do peão"""
        direction = 1 if piece.color == Color.WHITE else -1
        rank, file = piece.position.rank - 1, piece.position.file - 1

        # Adiciona influência diagonal (ataques)
        for df in [-1, 1]:
            new_rank = rank + direction
            new_file = file + df
            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                field[new_rank, new_file] = 1.0  # Full influence for attacks
        
        # Adiciona influência para frente
        new_rank = rank + direction
        if 0 <= new_rank < 8:
            field[new_rank, file] = 0.8  # Strong influence in front
            
            # Segunda casa à frente (somente na posição inicial)
            if (piece.color == Color.WHITE and rank == 1) or \
               (piece.color == Color.BLACK and rank == 6):
                new_rank = rank + (direction * 2)
                if 0 <= new_rank < 8:
                    field[new_rank, file] = 0.6  # Moderate influence two squares ahead
    
    def _add_knight_field(self, field: np.ndarray, piece: Piece):
        """Adiciona campo de influência do cavalo"""
        rank, file = piece.position.rank - 1, piece.position.file - 1
        
        for dr, df in KNIGHT_MOVES:
            new_rank = rank + dr
            new_file = file + df
            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                field[new_rank, new_file] = 1.0
    
    def _add_sliding_field(self, field: np.ndarray, piece: Piece, directions: List[Tuple[int, int]]):
        """Adiciona campo de influência de peças que deslizam (bispo, torre, rainha)"""
        rank, file = piece.position.rank - 1, piece.position.file - 1
        
        for dr, df in directions:
            current_rank = rank
            current_file = file
            
            for distance in range(1, 8):
                current_rank += dr
                current_file += df
                
                # Para se sair do tabuleiro
                if not (0 <= current_rank < 8 and 0 <= current_file < 8):
                    break
                
                # Marca a casa como atacada
                field[current_rank, current_file] = 1.0
    
    def _add_king_field(self, field: np.ndarray, piece: Piece):
        """Adiciona campo de influência do rei"""
        rank, file = piece.position.rank - 1, piece.position.file - 1
        
        for dr, df in DIRECTIONS:
            new_rank = rank + dr
            new_file = file + df
            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                field[new_rank, new_file] = 1.0
    
    def update_field(self, pieces: Dict[Position, Piece]):
        """Atualiza o campo global com todas as peças"""
        self.white_influence.fill(0)
        self.black_influence.fill(0)
        self.piece_fields.clear()
        
        for piece in pieces.values():
            field = self.calculate_piece_field(piece)
            self.piece_fields[piece.position] = field
            
            if piece.color == Color.WHITE:
                self.white_influence += field
            else:
                self.black_influence += field
    
    def is_in_check(self, color: Color, king_pos: Position) -> bool:
        """Verifica se o rei está em xeque usando o campo de influência"""
        # Convert to 0-based indices
        rank, file = king_pos.rank - 1, king_pos.file - 1
        if not (0 <= rank < 8 and 0 <= file < 8):
            return False
            
        # Get attack field from opposite color
        attacker_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        attack_field = self.white_influence if attacker_color == Color.WHITE else self.black_influence
        
        # Check if king's square is attacked
        return bool(attack_field[rank, file] >= 0.3)
    
    def get_control_score(self, color: Color) -> float:
        """Calcula o score de controle do tabuleiro para uma cor"""
        field = self.white_influence if color == Color.WHITE else self.black_influence
        return np.sum(field > CONTROL_THRESHOLD)
    
    def is_square_attacked(self, pos: Position, by_color: Color) -> bool:
        """Verifica se uma casa está sob ataque de uma cor específica"""
        field = self.white_influence if by_color == Color.WHITE else self.black_influence
        rank, file = pos.rank - 1, pos.file - 1
        if 0 <= rank < 8 and 0 <= file < 8:
            return field[rank, file] > 0  # Qualquer influência conta como ataque
        return False
    
    def get_piece_mobility(self, piece: Piece) -> float:
        """Calcula a mobilidade de uma peça baseada no seu campo"""
        if piece.position not in self.piece_fields:
            return 0.0
        field = self.piece_fields[piece.position]
        return np.sum(field > INFLUENCE_THRESHOLD)
    
    def simulate_move(self, from_pos: Position, to_pos: Position, pieces: Dict[Position, Piece]) -> 'QuantumField':
        """Simula um movimento e retorna o novo campo"""
        new_field = QuantumField()
        new_pieces = pieces.copy()
        
        # Simula o movimento
        piece = new_pieces.pop(from_pos)
        new_pieces[to_pos] = Piece(
            type=piece.type,
            color=piece.color,
            position=to_pos,
            has_moved=True
        )
        
        # Atualiza o campo
        new_field.update_field(new_pieces)
        return new_field
