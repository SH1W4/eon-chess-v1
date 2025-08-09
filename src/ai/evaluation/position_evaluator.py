from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
from src.core.board.board import Board, Position, Piece, Color, PieceType

def coord_to_san(pos: Union[str, Position, tuple]) -> str:
    """Convert various position formats to algebraic notation (e.g. 'd4' -> 'd4')"""
    if isinstance(pos, str):
        return pos
    elif isinstance(pos, Position):
        return str(pos)
    else:
        rank, file = pos
        # Convert to algebraic with correct file offset
        return f"{chr(ord('a') + file - 1)}{rank}"

def san_to_coords(san: str) -> Tuple[int, int]:
    """Convert algebraic notation to rank, file coordinates (e.g. 'd4' -> (4, 4))"""
    file = ord(san[0]) - ord('a') + 1  # a=1, b=2, etc.
    rank = int(san[1])
    return (rank, file)

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
            'material': 10.0,       # Base material value scale
            'center_control': 5.0,   # Important for center control
            'mobility': 3.0,        # Moderate for piece activity
            'pawn_structure': 4.0,  # Important for structure
            'king_safety': 6.0,     # Critical for king safety
            'piece_coordination': 2.0, # Modest tactical strength
            'space': 1.0,           # Minor territorial advantage
            'development': 2.0      # Early game activity
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
        
        # Strong weights for different pieces in the center
        piece_weights = {
            PieceType.PAWN: 3.0,    # Critical in center but not overwhelming
            PieceType.KNIGHT: 3.5,  # Strong in center
            PieceType.BISHOP: 2.5,  # Good in center
            PieceType.ROOK: 2.0,    # Decent in center
            PieceType.QUEEN: 1.5    # Avoid early development
        }
        
        # Evaluate only center and extended center
        for rank in range(2, 6):
            for file in range(2, 6):
                pos = (rank, file)
                is_center = pos in self.center_squares
                base_weight = 2.0 if is_center else 1.0  # Center square bonus
                
                piece = board.pieces.get(pos)
                if piece:
                    piece_weight = piece_weights.get(piece.type, 1.0)
                    if piece.color == color:
                        # Bonus for piece placement and control
                        score += base_weight * piece_weight
                        if is_center:
                            score += 2.0  # Center piece bonus
                            # Extra bonus for centralized knights
                            if piece.type == PieceType.KNIGHT:
                                score += 1.5
                    else:
                        # Smaller penalty for enemy pieces
                        score -= base_weight * piece_weight * 0.4
                
                # Evaluate square control in center
                if is_center:
                    pos_san = coord_to_san(pos)
                    if board.is_square_attacked(pos_san, color):
                        score += 1.0  # Moderate bonus for controlling central square
                        if piece and piece.color == color:
                            score += 0.5  # Small bonus for piece attacking its square
                    if board.is_square_attacked(pos_san, Color.BLACK if color == Color.WHITE else Color.WHITE):
                        score -= 0.5  # Small penalty for enemy control
                    
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
        
        for piece_pos, piece in board.pieces.items():
            if piece.type == PieceType.KING:
                continue
                
            moves = board.get_valid_moves(piece_pos)
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
        enemy_pawns_by_file = {i: [] for i in range(1, 9)}
        
        # Mapeia peões por coluna
        for piece_pos, piece in board.pieces.items():
                if piece.type == PieceType.PAWN:
                    # Handle tuple or string position
                    if isinstance(piece_pos, tuple):
                        rank, file = piece_pos
                    else:
                        rank, file = san_to_coords(piece_pos)
                    if 1 <= file <= 8:  # Validate file index
                        if piece.color == color:
                            pawns_by_file[file].append((piece, rank))
                        else:
                            enemy_pawns_by_file[file].append((piece, rank))
        
        # Avalia estrutura de peões para cada coluna
        for file in range(1, 9):
            pawns = pawns_by_file[file]
            enemy_pawns = enemy_pawns_by_file[file]
            
            # Doubled pawns (bad)
            if len(pawns) > 1:
                score -= 8.0 * (len(pawns) - 1)  # Moderate penalty for doubled pawns
            if len(enemy_pawns) > 1:
                score += 6.0 * (len(enemy_pawns) - 1)  # Small bonus for enemy doubled pawns
            
            # Connected pawns (very good)
            if len(pawns) > 0:
                has_neighbor = False
                if file > 1 and pawns_by_file[file-1]:
                    has_neighbor = True
                    score += 10.0  # Moderate bonus for connected pawns
                if file < 8 and pawns_by_file[file+1]:
                    has_neighbor = True
                    score += 10.0  # Moderate bonus for connected pawns
                
                # Isolated pawns (very bad)
                if not has_neighbor and len(pawns) > 0:
                    score -= 15.0  # Moderate penalty for isolated pawns
            
            # Enemy isolated pawns (good for us)
            if len(enemy_pawns) > 0:
                enemy_has_neighbor = False
                if file > 1 and enemy_pawns_by_file[file-1]:
                    enemy_has_neighbor = True
                if file < 8 and enemy_pawns_by_file[file+1]:
                    enemy_has_neighbor = True
                if not enemy_has_neighbor:
                    score += 8.0  # Moderate bonus for enemy isolated pawns
            
            # Avalia peões passados e avançados
            for pawn_info in pawns:
                pawn, rank = pawn_info
                is_passed = True
                # Verifica se há peões inimigos que podem bloquear
                target_rank = range(rank - 1, 0, -1) if color == Color.WHITE else range(rank + 1, 9)
                
                for r in target_rank:
                    if any(p for pos, p in board.pieces.items() 
                          if p.type == PieceType.PAWN 
                          and p.color != color
                          and abs(san_to_coords(pos)[1] - file) <= 1
                          and ((color == Color.WHITE and san_to_coords(pos)[0] < rank)
                              or (color == Color.BLACK and san_to_coords(pos)[0] > rank))):
                        is_passed = False
                        break
                
                if is_passed:
                    # Strong bonuses for passed pawns
                    base_weight = 5.0  # Moderate base bonus
                    # Reasonable rank advancement bonus
                    rank_bonus = 1.0 * (rank - 2 if color == Color.WHITE else 7 - rank)
                    # Support bonus
                    support_bonus = 2.0 if has_neighbor else 0.0
                    score += base_weight + rank_bonus + support_bonus
                
                # Enhanced bonus for pawn advancement
                    advance_bonus = 1.0 * (rank - 2 if color == Color.WHITE else 7 - rank)
                score += advance_bonus
                        
        return score
    
    def _evaluate_king_safety(self, board: Board, color: Color) -> float:
        """Avalia a segurança do rei"""
        score = 0.0
        
        # Encontra o rei
        king_pos = None
        for pos, piece in board.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = pos
                break
                
        if not king_pos:
            return -999.0  # Rei não encontrado (não deve acontecer em jogo normal)
            
        # Check penalty
        original_turn = board.current_turn
        board.current_turn = color
        if board.is_in_check():
                score -= 2.5  # Check penalty
        board.current_turn = original_turn
            
        # Evaluate king position and pawn protection
        rank, file = san_to_coords(king_pos)
        pawn_shield = 0
        
        # Very large bonus for corner positions
        if (rank == 1 or rank == 8) and (file == 1 or file == 8):
            score += 35.0  # Strong corner bonus
            if (rank == 1 and color == Color.WHITE) or (rank == 8 and color == Color.BLACK):
                score += 25.0  # Strong bonus for correct back rank
        
        # Heavy central penalty
        if 3 <= rank <= 6 and 3 <= file <= 6:
            central_exposure = -25.0 * (5 - abs(4.5 - rank) - abs(4.5 - file))
            score += central_exposure  # Severe central penalty
        
        # Evaluate pawn protection
        pawn_direction = 1 if color == Color.WHITE else -1
        for file_offset in [-1, 0, 1]:
            shield_file = max(1, min(8, file + file_offset))
            shield_rank = rank + pawn_direction
            if 1 <= shield_rank <= 8:
                shield_pos = coord_to_san((shield_rank, shield_file))
                piece = board.pieces.get(shield_pos)
                if piece and piece.type == PieceType.PAWN and piece.color == color:
                    if file_offset == 0:  # Pawn directly in front
                        pawn_shield += 25.0  # Strong bonus for direct protection
                    else:  # Diagonal pawns
                        pawn_shield += 15.0  # Significant diagonal protection

        # Bonus for pawns on king's file
        king_file_pawns = sum(1 for pos, piece in board.pieces.items()
                             if piece.type == PieceType.PAWN
                             and piece.color == color
                             and san_to_coords(pos)[1] == file)
        score += 5.0 * king_file_pawns
        
        # Evaluate enemy piece proximity
        king_tropism = 0
        for pos, piece in board.pieces.items():
            if piece.color != color:
                # Calculate Manhattan distance to king
                enemy_rank, enemy_file = san_to_coords(pos)
                distance = abs(enemy_rank - rank) + abs(enemy_file - file)
                
                # Different weights by piece type
                if distance <= 3:  # Only consider nearby pieces
                    piece_danger = {
                        PieceType.QUEEN: 15.0,
                        PieceType.ROOK: 10.0,
                        PieceType.BISHOP: 8.0,
                        PieceType.KNIGHT: 8.0,
                        PieceType.PAWN: 3.0
                    }.get(piece.type, 0.0)
                    
                    king_tropism -= piece_danger / (distance + 1)  # Closer = more dangerous
        
        # Apply all factors with appropriate weights
        score += 2.0 * pawn_shield  # Pawn protection is very important
        score += king_tropism      # Penalty for nearby enemy pieces
                        
        return score
    
    def _evaluate_piece_coordination(self, board: Board, color: Color) -> float:
        """Avalia a coordenação entre as peças"""
        score = 0.0
        
        # Avalia peças defendidas
        for pos, piece in board.pieces.items():
            if piece.color == color:
                pos_san = coord_to_san(pos)
                if board.is_square_attacked(pos_san, color):
                    score += 0.2  # Peça defendida
                    
        # Avalia pares de bispos
        bishops = [p for pos, p in board.pieces.items() if p.type == PieceType.BISHOP and p.color == color]
        if len(bishops) >= 2:
            score += 0.5  # Bônus por par de bispos
            
        # Avalia torres dobradas
        rooks = [pos for pos, p in board.pieces.items() if p.type == PieceType.ROOK and p.color == color]
        for i, rook1_pos in enumerate(rooks):
            for rook2_pos in rooks[i+1:]:
                if rook1_pos[1] == rook2_pos[1]:  # Mesma coluna
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
                pos_san = coord_to_san((rank, file))
                if board.is_square_attacked(pos_san, color):
                    score += 0.1
                    
        return score
    
    def _evaluate_development(self, board: Board, color: Color) -> float:
        """Avalia o desenvolvimento das peças"""
        score = 0.0
        
        # Peças desenvolvidas são aquelas que saíram da posição inicial
        back_rank = 1 if color == Color.WHITE else 8
        for pos, piece in board.pieces.items():
            if piece.color == color:
                rank, file = san_to_coords(pos)
                if piece.type in [PieceType.KNIGHT, PieceType.BISHOP]:
                    if rank != back_rank:
                        score += 0.3  # Peça menor desenvolvida
                elif piece.type == PieceType.QUEEN:
                    if rank != back_rank:
                        score -= 0.1  # Penalidade por desenvolvimento prematuro da dama
                        
        return score
