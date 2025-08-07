from dataclasses import dataclass
from typing import Dict, List, Tuple
from src.core.board.board import Board, Position, Piece, Color, PieceType

@dataclass
class PositionalFeatures:
    """Características posicionais avaliadas"""
    center_control: float = 0.0
    piece_mobility: float = 0.0
    pawn_structure: float = 0.0
    king_safety: float = 0.0
    piece_coordination: float = 0.0
    space_advantage: float = 0.0
    development: float = 0.0

class AdvancedEvaluator:
    """Avaliador avançado de posição"""
    
    def __init__(self):
        # Fatores de peso para diferentes aspectos da posição
        self.weights = {
            'material': 1.0,
            'center_control': 0.3,
            'mobility': 0.2,
            'pawn_structure': 0.15,
            'king_safety': 0.25,
            'piece_coordination': 0.2,
            'space': 0.1,
            'development': 0.15
        }
        
        # Define as casas centrais e o centro estendido
        self.center_squares = {(3,3), (3,4), (4,3), (4,4)}
        self.extended_center = {(2,2), (2,3), (2,4), (2,5),
                              (3,2), (3,3), (3,4), (3,5),
                              (4,2), (4,3), (4,4), (4,5),
                              (5,2), (5,3), (5,4), (5,5)}
        
    def evaluate(self, board: Board, color: Color) -> Tuple[float, PositionalFeatures]:
        """Avalia a posição com todos os fatores"""
        features = PositionalFeatures()
        
        # Avalia controle do centro
        features.center_control = self._evaluate_center_control(board, color)
        
        # Avalia mobilidade das peças
        features.piece_mobility = self._evaluate_mobility(board, color)
        
        # Avalia estrutura de peões
        features.pawn_structure = self._evaluate_pawn_structure(board, color)
        
        # Avalia segurança do rei
        features.king_safety = self._evaluate_king_safety(board, color)
        
        # Avalia coordenação das peças
        features.piece_coordination = self._evaluate_piece_coordination(board, color)
        
        # Avalia vantagem de espaço
        features.space_advantage = self._evaluate_space(board, color)
        
        # Avalia desenvolvimento
        features.development = self._evaluate_development(board, color)
        
        # Calcula pontuação total ponderada
        total_score = (
            self.weights['center_control'] * features.center_control +
            self.weights['mobility'] * features.piece_mobility +
            self.weights['pawn_structure'] * features.pawn_structure +
            self.weights['king_safety'] * features.king_safety +
            self.weights['piece_coordination'] * features.piece_coordination +
            self.weights['space'] * features.space_advantage +
            self.weights['development'] * features.development
        )
        
        return total_score, features
    
    def _evaluate_center_control(self, board: Board, color: Color) -> float:
        """Avalia o controle do centro"""
        score = 0.0
        
        # Conta peças controlando o centro
        for rank in range(2, 6):
            for file in range(2, 6):
                pos = Position(rank=rank, file=file)
                if (rank, file) in self.center_squares:
                    weight = 0.5
                else:
                    weight = 0.3
                    
                piece = board.get_piece(pos)
                if piece:
                    if piece.color == color:
                        score += weight
                    else:
                        score -= weight
                        
                # Avalia casas atacadas
                if board.is_square_attacked(pos, color):
                    score += weight * 0.5
                if board.is_square_attacked(pos, Color.BLACK if color == Color.WHITE else Color.WHITE):
                    score -= weight * 0.5
                    
        return score
    
    def _evaluate_mobility(self, board: Board, color: Color) -> float:
        """Avalia a mobilidade das peças"""
        score = 0.0
        piece_mobility_weights = {
            PieceType.PAWN: 0.1,
            PieceType.KNIGHT: 0.3,
            PieceType.BISHOP: 0.3,
            PieceType.ROOK: 0.4,
            PieceType.QUEEN: 0.5
        }
        
        for piece in board.piece_list:
            if piece.type == PieceType.KING:
                continue
                
            moves = board.get_valid_moves(piece.position)
            mobility = len(moves) * piece_mobility_weights.get(piece.type, 0.2)
            
            if piece.color == color:
                score += mobility
            else:
                score -= mobility
                
        return score
    
    def _evaluate_pawn_structure(self, board: Board, color: Color) -> float:
        """Avalia a estrutura de peões"""
        score = 0.0
        pawns_by_file = {i: [] for i in range(1, 9)}
        
        # Mapeia peões por coluna
        for piece in board.piece_list:
            if piece.type == PieceType.PAWN:
                pawns_by_file[piece.position.file].append(piece)
        
        # Avalia estrutura
        for file in range(1, 9):
            pawns = pawns_by_file[file]
            
            # Peões dobrados (ruim)
            if len(pawns) > 1:
                score -= 0.3 * (len(pawns) - 1)
            
            # Peões isolados (ruim)
            if len(pawns) > 0:
                has_neighbor = False
                if file > 1 and pawns_by_file[file-1]:
                    has_neighbor = True
                if file < 8 and pawns_by_file[file+1]:
                    has_neighbor = True
                if not has_neighbor:
                    score -= 0.4
                    
            # Peões passados (bom)
            for pawn in pawns:
                if pawn.color == color:
                    is_passed = True
                    target_rank = range(pawn.position.rank - 1, 0, -1) if color == Color.WHITE else range(pawn.position.rank + 1, 9)
                    for r in target_rank:
                        if any(p for p in board.piece_list 
                              if p.type == PieceType.PAWN 
                              and p.color != color
                              and abs(p.position.file - pawn.position.file) <= 1
                              and ((color == Color.WHITE and p.position.rank < pawn.position.rank)
                                   or (color == Color.BLACK and p.position.rank > pawn.position.rank))):
                            is_passed = False
                            break
                    if is_passed:
                        score += 0.6
                        
        return score
    
    def _evaluate_king_safety(self, board: Board, color: Color) -> float:
        """Avalia a segurança do rei"""
        score = 0.0
        
        # Encontra o rei
        king = next((p for p in board.piece_list if p.type == PieceType.KING and p.color == color), None)
        if not king:
            return -999.0  # Rei não encontrado (não deve acontecer em jogo normal)
            
        # Penalidade por estar em xeque
        if board.is_in_check(color):
            score -= 1.0
            
        # Avalia proteção de peões
        king_pos = king.position
        pawn_shield = 0
        for file_offset in [-1, 0, 1]:
            for rank_offset in [1] if color == Color.WHITE else [-1]:
                shield_pos = Position(
                    rank=king_pos.rank + rank_offset,
                    file=max(1, min(8, king_pos.file + file_offset))
                )
                piece = board.get_piece(shield_pos)
                if piece and piece.type == PieceType.PAWN and piece.color == color:
                    pawn_shield += 1
                    
        score += 0.2 * pawn_shield
        
        # Avalia exposição do rei
        attacking_pieces = 0
        for piece in board.piece_list:
            if piece.color != color:
                moves = board.get_valid_moves(piece.position)
                for move in moves:
                    if abs(move.rank - king_pos.rank) <= 2 and abs(move.file - king_pos.file) <= 2:
                        attacking_pieces += 1
                        break
                        
        score -= 0.1 * attacking_pieces
        
        return score
    
    def _evaluate_piece_coordination(self, board: Board, color: Color) -> float:
        """Avalia a coordenação entre as peças"""
        score = 0.0
        
        # Avalia peças defendidas
        for piece in board.piece_list:
            if piece.color == color:
                if board.is_square_attacked(piece.position, color):
                    score += 0.2  # Peça defendida
                    
        # Avalia pares de bispos
        bishops = [p for p in board.piece_list if p.type == PieceType.BISHOP and p.color == color]
        if len(bishops) >= 2:
            score += 0.5  # Bônus por par de bispos
            
        # Avalia torres dobradas
        rooks = [p for p in board.piece_list if p.type == PieceType.ROOK and p.color == color]
        for i, rook1 in enumerate(rooks):
            for rook2 in rooks[i+1:]:
                if rook1.position.file == rook2.position.file:
                    score += 0.3  # Bônus por torres na mesma coluna
                    
        return score
    
    def _evaluate_space(self, board: Board, color: Color) -> float:
        """Avalia a vantagem de espaço"""
        score = 0.0
        
        # Conta casas controladas no campo adversário
        enemy_half = range(1, 5) if color == Color.WHITE else range(5, 9)
        for rank in enemy_half:
            for file in range(1, 9):
                pos = Position(rank=rank, file=file)
                if board.is_square_attacked(pos, color):
                    score += 0.1
                    
        return score
    
    def _evaluate_development(self, board: Board, color: Color) -> float:
        """Avalia o desenvolvimento das peças"""
        score = 0.0
        
        # Peças desenvolvidas são aquelas que saíram da posição inicial
        back_rank = 1 if color == Color.WHITE else 8
        for piece in board.piece_list:
            if piece.color == color:
                if piece.type in [PieceType.KNIGHT, PieceType.BISHOP]:
                    if piece.position.rank != back_rank:
                        score += 0.3  # Peça menor desenvolvida
                elif piece.type == PieceType.QUEEN:
                    if piece.position.rank != back_rank:
                        score -= 0.1  # Penalidade por desenvolvimento prematuro da dama
                        
        return score
