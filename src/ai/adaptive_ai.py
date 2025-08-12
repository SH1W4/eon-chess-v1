from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from src.core.board.board import Board, Position, PieceType, Color, Piece
from src.core.board.move import Move
from src.ai.transposition_table import TranspositionTable, AdvancedEvaluator
import random
import json
import numpy as np

@dataclass
class EvaluationWeights:
    """Weights used for position evaluation"""
    piece_values: Dict[PieceType, float] = None
    positional_values: Dict[PieceType, List[List[float]]] = None
    mobility_weight: float = 0.1
    pawn_structure_weight: float = 0.1
    king_safety_weight: float = 0.2
    
    def __post_init__(self):
        if self.piece_values is None:
            self.piece_values = {
                PieceType.PAWN: 1.0,
                PieceType.KNIGHT: 3.0,
                PieceType.BISHOP: 3.0,
                PieceType.ROOK: 5.0,
                PieceType.QUEEN: 9.0,
                PieceType.KING: 0.0  # King's value is not used in evaluation
            }
        
        # Initialize position tables if not provided
        if self.positional_values is None:
            self.positional_values = self._default_position_tables()
    
    @staticmethod
    def _default_position_tables() -> Dict[PieceType, List[List[float]]]:
        """Default piece-square tables for positional evaluation"""
        return {
            PieceType.PAWN: [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],      # 8th rank
                [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9],      # 7th rank
                [0.5, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.5],      # 6th rank
                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],      # 5th rank
                [0.2, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.2],      # 4th rank
                [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],      # 3rd rank
                [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1], # 2nd rank (starting)
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]       # 1st rank
            ],
            PieceType.KNIGHT: [
                [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
                [-0.4, -0.2, 0.0, 0.0, 0.0, 0.0, -0.2, -0.4],
                [-0.3, 0.0, 0.1, 0.15, 0.15, 0.1, 0.0, -0.3],
                [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
                [-0.3, 0.0, 0.15, 0.2, 0.2, 0.15, 0.0, -0.3],
                [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
                [-0.4, -0.2, 0.0, 0.05, 0.05, 0.0, -0.2, -0.4],
                [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
            ],
            PieceType.BISHOP: [
                [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.05, 0.1, 0.1, 0.05, 0.0, -0.1],
                [-0.1, 0.05, 0.05, 0.2, 0.2, 0.05, 0.05, -0.1],
                [-0.1, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0, -0.1],
                [-0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1],
                [-0.1, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, -0.1],
                [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
            ],
            PieceType.ROOK: [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05],
                [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
                [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
                [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
                [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
                [-0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05],
                [0.0, 0.0, 0.0, 0.05, 0.05, 0.0, 0.0, 0.0]
            ],
            PieceType.QUEEN: [
                [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
                [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.1, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
                [-0.05, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
                [0.0, 0.0, 0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
                [-0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
                [-0.1, 0.0, 0.05, 0.0, 0.0, 0.0, 0.0, -0.1],
                [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
            ],
            PieceType.KING: [
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
                [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
                [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
                [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
                [0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2]
            ]
        }

class LearningMode(Enum):
    """Modos de aprendizado da IA"""
    PASSIVE = "passive"      # Aprende lentamente, mantém estabilidade
    ACTIVE = "active"       # Aprende moderadamente, equilibra adaptação
    AGGRESSIVE = "aggressive" # Aprende rapidamente, adapta-se muito

@dataclass
class PlayerProfile:
    """Profile representing player characteristics"""
    aggression: float = 0.5  # 0.0 = defensive, 1.0 = aggressive
    positional: float = 0.5  # 0.0 = tactical, 1.0 = positional
    risk_taking: float = 0.5  # 0.0 = conservative, 1.0 = risky
    opening_preference: str = "balanced"  # e.g. "open", "closed", "balanced"
    learning_rate: float = 0.1  # Taxa de aprendizado para adaptação
    learning_mode: LearningMode = LearningMode.PASSIVE  # Modo de aprendizado
    evolution_cycles: int = 1  # Número de ciclos evolutivos
    wins: int = 0
    losses: int = 0
    draws: int = 0
    games_played: int = 0
    piece_preferences: Dict[PieceType, float] = None
    favorite_openings: List[str] = None
    
    def __post_init__(self):
        self.position_tables = {}
        self.move_history = []
        if self.piece_preferences is None:
            self.piece_preferences = {
                PieceType.PAWN: 1.0,
                PieceType.KNIGHT: 1.0,
                PieceType.BISHOP: 1.0,
                PieceType.ROOK: 1.0,
                PieceType.QUEEN: 1.0
            }
        if self.favorite_openings is None:
            self.favorite_openings = []
    
    def adjust_for_game_phase(self, phase: str):
        """Adjust profile based on game phase"""
        if phase == "opening":
            self.aggression *= 0.8  # More conservative in opening
            self.positional *= 1.2  # More positional play
        elif phase == "endgame":
            self.aggression *= 1.2  # More aggressive in endgame
            self.risk_taking *= 1.1  # Slightly more risky
    
    def update_stats(self, result: str):
        """Update player statistics"""
        self.games_played += 1
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        else:
            self.draws += 1
            
    def calculate_win_rate(self) -> float:
        """Calculate win rate"""
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played

class AdaptiveAI:
    """Adaptive chess AI that learns from opponent's play style"""
    
    def __init__(self, profile: Optional[PlayerProfile] = None, 
                 weights: Optional[EvaluationWeights] = None):
        # Inicialização básica
        self.profile = profile or PlayerProfile()
        self.weights = weights or EvaluationWeights()
        self.position_history: List[Board] = []
        self.move_scores: Dict[Tuple[Position, Position], float] = {}
        self.game_memory: List[Dict] = []  # Lista de jogos anteriores
        self.learning_rate = self.profile.learning_rate
        self.move_times: List[float] = []
        
        # Inicializa recursos avançados
        self.transposition_table = TranspositionTable()
        self.advanced_evaluator = AdvancedEvaluator()
        
        # Inicializar tabelas de posição
        self.position_tables = {}
        for piece_type in PieceType:
            if piece_type in self.weights.positional_values:
                self.position_tables[piece_type] = np.array(self.weights.positional_values[piece_type])
        
        # Tabelas especiais para o rei
        self.position_tables['king_midgame'] = np.array(self.weights.positional_values[PieceType.KING])
        self.position_tables['king_endgame'] = np.array([
            [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
            [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
            [0.2, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.2],
            [0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1],
            [0.0, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.0],
            [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
            [-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.3]
        ])
        self.profile = profile or PlayerProfile()
        self.weights = weights or EvaluationWeights()
        self.position_history: List[Board] = []
        self.move_scores: Dict[Tuple[Position, Position], float] = {}
        self.game_memory: List[Dict] = []  # Lista de jogos anteriores
        self.learning_rate = self.profile.learning_rate
        self.move_times: List[float] = []
        
        # Inicializar tabelas de posição com os valores padrão
        self.position_tables = {}
        for piece_type in PieceType:
            if piece_type in self.weights.positional_values:
                self.position_tables[piece_type] = np.array(self.weights.positional_values[piece_type])
        
        # Tabelas especiais para o rei em diferentes fases do jogo
        self.position_tables['king_midgame'] = np.array(self.weights.positional_values[PieceType.KING])
        self.position_tables['king_endgame'] = np.array([
            [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
            [0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3],
            [0.2, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.2],
            [0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1],
            [0.0, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.0],
            [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1],
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
            [-0.3, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.3]
        ])
        
    def evaluate_position(self, board: Board, color: Optional[Color] = None) -> float:
        # Usa avaliador avançado
        score, features = self.advanced_evaluator.evaluate(board, color or Color.WHITE)
        return score
        """Evaluate board position from given color's perspective"""
        if color is None:
            color = Color.WHITE
            
        score = 0.0
        
        # Material evaluation
        for pos, piece in board.pieces.items():
            # Garante que a peça tem position configurado
            if not hasattr(piece, 'position') or piece.position is None:
                if isinstance(pos, tuple):
                    file_char = chr(ord('a') + pos[0])
                    # NOTA: Board usa rank direto da tupla, sem +1
                    piece.position = Position(file_char, pos[1])
            piece_value = self.weights.piece_values[piece.type]
            if piece.color == color:
                score += piece_value
            else:
                score -= piece_value
        
        # Development evaluation
        white_starting_rank = {PieceType.PAWN: 6, PieceType.KNIGHT: 7, PieceType.BISHOP: 7, PieceType.ROOK: 7, PieceType.QUEEN: 7}
        black_starting_rank = {PieceType.PAWN: 1, PieceType.KNIGHT: 0, PieceType.BISHOP: 0, PieceType.ROOK: 0, PieceType.QUEEN: 0}
        development_score = 0.0
        
        for pos, piece in board.pieces.items():
            # Garante que a peça tem position configurado
            if not hasattr(piece, 'position') or piece.position is None:
                if isinstance(pos, tuple):
                    file_char = chr(ord('a') + pos[0])
                    # NOTA: Board usa rank direto da tupla, sem +1
                    piece.position = Position(file_char, pos[1])
            if piece.type == PieceType.KING:
                continue
                
            # Center control
            center_value = 0.0
            if 2 <= piece.position.rank <= 5 and 2 <= piece.position.file <= 5:
                center_value = 0.3  # Outer center
                if 3 <= piece.position.rank <= 4 and 3 <= piece.position.file <= 4:
                    center_value = 0.5  # Inner center
                    
            # Development evaluation
            if piece.color == Color.WHITE:
                if piece.position.rank < white_starting_rank[piece.type]:
                    if piece.type == PieceType.PAWN:
                        # Larger bonus for central pawns
                        if 3 <= piece.position.file <= 6:
                            development_score += 0.4
                        else:
                            development_score += 0.2
                    else:
                        development_score += 0.3
                development_score += center_value
            else:
                if piece.position.rank > black_starting_rank[piece.type]:
                    if piece.type == PieceType.PAWN:
                        # Larger bonus for central pawns
                        if 3 <= piece.position.file <= 6:
                            development_score -= 0.4
                        else:
                            development_score -= 0.2
                    else:
                        development_score -= 0.3
                development_score -= center_value
        
        # Adjust score based on color perspective
        if color == Color.WHITE:
            score += development_score
        else:
            score -= development_score
            
        # Positional evaluation using piece-square tables
        for piece in board.pieces.values():
            if piece.type in self.weights.positional_values:
                pos_table = self.weights.positional_values[piece.type]
                rank_idx = piece.position.rank - 1
                if piece.color == Color.BLACK:
                    rank_idx = 7 - rank_idx  # Flip rank for black pieces
                pos_value = pos_table[rank_idx][piece.position.file - 1]
                
                if piece.color == color:
                    score += pos_value * self.profile.positional
                else:
                    score -= pos_value * self.profile.positional
        
        # Mobility evaluation
        mobility_score = 0.0
        for piece in board.pieces.values():
            if piece.color == color:
                moves = board.get_valid_moves(piece.position)
                mobility_score += len(moves) * 0.05  # Reduced base mobility weight
                # Bonus for moves that control important squares
                for move in moves:
                    if 3 <= move.rank <= 6 and 3 <= move.file <= 6:
                        mobility_score += 0.1  # Center control
                    elif piece.type == PieceType.PAWN and (move.rank == 3 or move.rank == 4):
                        mobility_score += 0.15  # Pawn advances in opening
            else:
                moves = board.get_valid_moves(piece.position)
                mobility_score -= len(moves) * 0.05
                for move in moves:
                    if 3 <= move.rank <= 6 and 3 <= move.file <= 6:
                        mobility_score -= 0.1
                    elif piece.type == PieceType.PAWN and (move.rank == 3 or move.rank == 4):
                        mobility_score -= 0.15
                        
        score += mobility_score * self.weights.mobility_weight
        
        # King safety
        if board.is_in_check(color):
            score -= 0.5 * self.weights.king_safety_weight
        if board.is_in_check(Color.BLACK if color == Color.WHITE else Color.WHITE):
            score += 0.3 * self.weights.king_safety_weight
            
        return score
    def get_best_move(self, board: Board, color: Optional[Color] = None, depth: int = 1) -> Optional[Move]:
        """Get best move using minimax with alpha-beta pruning"""
        # Normaliza cor (aceita enum ou string)
        if isinstance(color, str):
            color = Color.WHITE if color.lower().startswith('w') else Color.BLACK
        if color is None:
            color = Color.WHITE
            
        best_score = float('-inf')
        best_move = None
        
        # Get all valid moves for the current position
        all_moves = []
        
        # Verifica se board.pieces existe e tem itens
        if not hasattr(board, 'pieces') or not board.pieces:
            return None
            
        for pos, piece in board.pieces.items():
            # Garante que a peça tem position configurado
            if not hasattr(piece, 'position') or piece.position is None:
                if isinstance(pos, tuple):
                    file_char = chr(ord('a') + pos[0])
                    # NOTA: Board usa rank direto da tupla, sem +1
                    piece.position = Position(file_char, pos[1])
            if piece.color == color:
                # Get valid moves for this piece
                valid_moves = board.get_valid_moves(pos)
                for to_pos in valid_moves:
                    move = Move(pos, to_pos, piece)
                    # Check for captures
                    captured = board.get_piece(to_pos)
                    if captured:
                        move.captured_piece = captured
                    all_moves.append(move)
        
        # Se não há movimentos válidos, tenta um fallback simples gerando do tabuleiro
        if not all_moves:
            try:
                for pos, piece in list(board.pieces.items()):
                    if piece.color == color:
                        for to_pos in board.get_valid_moves(pos):
                            mv = Move(pos, to_pos, piece)
                            all_moves.append(mv)
            except Exception:
                pass
        if not all_moves:
            return None
        
        # Randomize move order slightly based on risk_taking profile
        if self.profile.risk_taking > 0.7:
            import random
            random.shuffle(all_moves)
        
        for move in all_moves:
            # Make copy of board for evaluation
            board_copy = Board()
            # Copia o estado do tabuleiro
            if hasattr(board, 'squares'):
                board_copy.squares = board.squares.copy()
            if hasattr(board, 'pieces'):
                board_copy.pieces = board.pieces.copy()
            
            # Try move (make_move pode ser síncrono em Board básico)
            piece_backup = board_copy.pieces.get(move.to_pos)
            board_copy.pieces[move.to_pos] = move.piece
            if move.from_pos in board_copy.pieces:
                del board_copy.pieces[move.from_pos]
            
            # Evaluate position recursively
            opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
            minimax_score = self._minimax(board_copy, depth - 1, float('-inf'), float('inf'), opponent_color)
            score = -minimax_score
            
            # Restore board state
            if move.from_pos != move.to_pos:
                board_copy.pieces[move.from_pos] = move.piece
                if piece_backup:
                    board_copy.pieces[move.to_pos] = piece_backup
                elif move.to_pos in board_copy.pieces:
                    del board_copy.pieces[move.to_pos]
            
            # Add aggression bonus for captures
            if move.captured_piece:
                capture_bonus = self.weights.piece_values[move.captured_piece.type] * self.profile.aggression
                score += capture_bonus
            
            if score > best_score:
                best_score = score
                best_move = move
        
        # Antes de devolver, verifique se o movimento é executável pelo board
        def _can_execute(mv: Move) -> bool:
            try:
                from_sq = str(mv.from_pos)
                to_sq = str(mv.to_pos)
            except Exception:
                from_sq = mv.from_pos
                to_sq = mv.to_pos
            # Backup estado mínimo
            pieces_backup = board.pieces.copy() if hasattr(board, 'pieces') else None
            captured_backup = list(getattr(board, 'captured_pieces', [])) if hasattr(board, 'captured_pieces') else None
            turn_backup = getattr(board, 'current_turn', None)
            last_backup = getattr(board, 'last_move', None)
            try:
                # Garante que a vez esteja coerente com a peça que vai se mover
                mover_color = None
                try:
                    mover_color = mv.piece.color if hasattr(mv, 'piece') and mv.piece else board.get_piece(from_sq).color
                except Exception:
                    pass
                if mover_color is not None and hasattr(board, 'current_turn'):
                    board.current_turn = mover_color
                # Snapshot flags/positions to avoid side effects
                flags_backup = {}
                pos_backup = {}
                try:
                    for p in board.pieces.values():
                        flags_backup[id(p)] = getattr(p, 'has_moved', False)
                        pos_backup[id(p)] = getattr(p, 'position', None)
                except Exception:
                    pass
                # Se não há peça na casa de origem, nem tenta
                try:
                    if hasattr(board, 'pieces') and board.pieces.get(from_sq) is None:
                        return False
                except Exception:
                    pass
                if hasattr(board, 'move_piece'):
                    res = board.move_piece(from_sq, to_sq)
                    ok = isinstance(res, dict) and res.get('success') is True
                else:
                    ok = False
                # Restore per-piece flags/positions possibly mutated during simulation
                try:
                    for p in board.pieces.values():
                        pid = id(p)
                        if pid in flags_backup:
                            p.has_moved = flags_backup[pid]
                        if pid in pos_backup:
                            p.position = pos_backup[pid]
                except Exception:
                    pass
                return ok
            finally:
                # Restore
                if pieces_backup is not None:
                    board.pieces = pieces_backup
                if captured_backup is not None and hasattr(board, 'captured_pieces'):
                    board.captured_pieces = captured_backup
                if turn_backup is not None and hasattr(board, 'current_turn'):
                    board.current_turn = turn_backup
                if hasattr(board, 'last_move'):
                    board.last_move = last_backup
        
        # Se o melhor movimento não é válido, tenta o primeiro executável
        if best_move is None or not _can_execute(best_move):
            for mv in all_moves:
                if _can_execute(mv):
                    return mv
            # Último fallback: tenta um avanço simples de peão válido
            try:
                for pos, piece in list(board.pieces.items()):
                    try:
                        is_black = (color == Color.BLACK)
                    except Exception:
                        is_black = False
                    if piece.type == PieceType.PAWN and ((is_black and piece.color == Color.BLACK) or (not is_black and piece.color == Color.WHITE)):
                        from_sq = str(pos)
                        file_char = from_sq[0]
                        rank = int(from_sq[1])
                        dir_step = -1 if is_black else 1
                        one_step = f"{file_char}{rank + dir_step}"
                        if board.pieces.get(one_step) is None and _can_execute(Move(pos, Position.from_algebraic(one_step), piece)):
                            return Move(pos, Position.from_algebraic(one_step), piece)
            except Exception:
                pass
        
        # Fallback final: se não escolheu, devolve primeiro movimento disponível
        return best_move or (all_moves[0] if all_moves else None)
    
    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, color: Color) -> float:
        # Verifica cache de transposição
        tt_entry = self.transposition_table.lookup(board, depth)
        if tt_entry and tt_entry.depth >= depth:
            if tt_entry.flag == 'exact':
                return tt_entry.score
            elif tt_entry.flag == 'lowerbound':
                alpha = max(alpha, tt_entry.score)
            elif tt_entry.flag == 'upperbound':
                beta = min(beta, tt_entry.score)
            if alpha >= beta:
                return tt_entry.score
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0:
            return self.evaluate_position(board, color)
        
        if color == Color.WHITE:
            max_score = float('-inf')
            
            # Get all valid moves for white pieces
            moves = []
            for pos, piece in board.pieces.items():
                # Garante que a peça tem position configurado
                if not hasattr(piece, 'position') or piece.position is None:
                    if isinstance(pos, tuple):
                        file_char = chr(ord('a') + pos[0])
                        # NOTA: Board usa rank direto da tupla, sem +1
                        piece.position = Position(file_char, pos[1])
                if piece.color == color:
                    for to_pos in board.get_valid_moves(pos):
                        moves.append(Move(pos, to_pos, piece))
            
            # Order moves to improve alpha-beta pruning
            moves = self._order_moves(board, moves)
            
            for move in moves:
                # Make copy of board
                board_copy = Board()
                if hasattr(board, 'squares'):
                    board_copy.squares = board.squares.copy()
                if hasattr(board, 'pieces'):
                    board_copy.pieces = board.pieces.copy()
                
                # Manually make the move
                piece_backup = board_copy.pieces.get(move.to_pos)
                board_copy.pieces[move.to_pos] = move.piece
                if move.from_pos in board_copy.pieces:
                    del board_copy.pieces[move.from_pos]
                    
                score = self._minimax(board_copy, depth - 1, alpha, beta, Color.BLACK)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            return max_score
        else:
            min_score = float('inf')
            
            # Get all valid moves for black pieces
            moves = []
            for pos, piece in board.pieces.items():
                # Garanta que a peça tem position configurado
                if not hasattr(piece, 'position') or piece.position is None:
                    if isinstance(pos, tuple):
                        file_char = chr(ord('a') + pos[0])
                        # NOTA: Board usa rank direto da tupla, sem +1
                        piece.position = Position(file_char, pos[1])
                if piece.color == color:
                    for to_pos in board.get_valid_moves(pos):
                        moves.append(Move(pos, to_pos, piece))
            
            # Order moves to improve alpha-beta pruning
            moves = self._order_moves(board, moves)
            
            if not moves:
                return min_score
            
            for move in moves:
                # Make copy of board
                board_copy = Board()
                if hasattr(board, 'squares'):
                    board_copy.squares = board.squares.copy()
                if hasattr(board, 'pieces'):
                    board_copy.pieces = board.pieces.copy()
                
                # Manually make the move
                piece_backup = board_copy.pieces.get(move.to_pos)
                board_copy.pieces[move.to_pos] = move.piece
                if move.from_pos in board_copy.pieces:
                    del board_copy.pieces[move.from_pos]
                    
                score = self._minimax(board_copy, depth - 1, alpha, beta, Color.WHITE)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            return min_score
            
    def _order_moves(self, board: Board, moves: List[Move]) -> List[Move]:
        """Order moves to improve alpha-beta pruning efficiency"""
        move_scores = []
        
        for move in moves:
            score = 0
            
            # Captures are likely good moves
            if move.captured_piece:
                score += self.weights.piece_values[move.captured_piece.type]
            
            # Check if move was successful in past games
            move_key = (str(move.from_pos), str(move.to_pos))
            if move_key in self.move_scores:
                score += self.move_scores[move_key]
            
            # Center control is generally good
            # Handle both Position objects and tuples
            if hasattr(move.to_pos, 'rank') and hasattr(move.to_pos, 'file'):
                # Position object - file is already 0-7 index
                if 2 <= move.to_pos.rank <= 5 and 2 <= move.to_pos.file <= 5:
                    score += 0.3
                    if 3 <= move.to_pos.rank <= 4 and 3 <= move.to_pos.file <= 4:
                        score += 0.2
            elif isinstance(move.to_pos, tuple) and len(move.to_pos) == 2:
                # Tuple (file_idx, rank)
                file_idx, rank = move.to_pos
                if 2 <= rank <= 5 and 2 <= file_idx <= 5:
                    score += 0.3
                    if 3 <= rank <= 4 and 3 <= file_idx <= 4:
                        score += 0.2
            
            move_scores.append((score, move))
        
        # Sort moves by score in descending order (sort by key to avoid comparing Move objects)
        move_scores.sort(key=lambda x: x[0], reverse=True)
        return [move for _, move in move_scores]
    
    def update_profile(self, board: Board, game_result: str):
        """Update AI profile based on board state and game result"""
        if not board or not game_result:
            return
            
        # Ajusta a taxa de aprendizado baseado no modo
        base_learning_rate = self.profile.learning_rate
        if self.profile.learning_mode == LearningMode.PASSIVE:
            learning_rate = base_learning_rate * 0.5
        elif self.profile.learning_mode == LearningMode.ACTIVE:
            learning_rate = base_learning_rate * 1.0
        else:  # AGGRESSIVE
            learning_rate = base_learning_rate * 2.0
            
        # Sempre adiciona o jogo atual à memória antes de processar
        current_game = {
            'result': game_result,
            'aggression': self.profile.aggression,
            'positional': self.profile.positional,
            'risk_taking': self.profile.risk_taking
        }
        self.game_memory.append(current_game)
        
        # Analyze final position
        aggressive_moves = 0
        positional_moves = 0
        risky_moves = 0
        total_moves = len(board.move_history) if hasattr(board, 'move_history') and board.move_history else 0
        
        # Só processa move_history se existir
        if hasattr(board, 'move_history') and board.move_history:
            for move in board.move_history:
                from_pos, to_pos = move
                # Count captures as aggressive moves
                if to_pos in board.captured_pieces:
                    aggressive_moves += 1
                
                # Simple positional analysis
                piece = board.get_piece(to_pos)
                if piece and piece.type != PieceType.PAWN:
                    # Center control is positional
                    if 3 <= to_pos.rank <= 6 and 3 <= to_pos.file <= 6:
                        positional_moves += 1
                        
                # Consider moves that put pieces at risk as risky
                if piece and board.is_square_attacked(to_pos, 
                    Color.BLACK if piece.color == Color.WHITE else Color.WHITE):
                    risky_moves += 1
        
        # Update profile based on move analysis
        if total_moves > 0:
            # Base weights dependem do modo de aprendizado
            if self.profile.learning_mode == LearningMode.PASSIVE:
                memory_weight = 0.9
                new_weight = 0.1
            elif self.profile.learning_mode == LearningMode.ACTIVE:
                memory_weight = 0.8
                new_weight = 0.2
            else:  # AGGRESSIVE
                memory_weight = 0.6
                new_weight = 0.4
            
            # Aplica os pesos na atualização
            self.profile.aggression = memory_weight * self.profile.aggression + \
                                    new_weight * (aggressive_moves / total_moves)
            self.profile.positional = memory_weight * self.profile.positional + \
                                    new_weight * (positional_moves / total_moves)
            self.profile.risk_taking = memory_weight * self.profile.risk_taking + \
                                     new_weight * (risky_moves / total_moves)
        
        # Evolução adicional baseada nos ciclos (independente de move_history)
        if self.profile.evolution_cycles > 0:
            # Para o primeiro jogo ou modo AGGRESSIVE, força mudanças
            if len(self.game_memory) == 1 and self.profile.learning_mode == LearningMode.AGGRESSIVE:
                # Primeiro jogo com modo agressivo - força evolução
                change = 0.05 * self.profile.evolution_cycles * learning_rate
                self.profile.aggression = min(1.0, self.profile.aggression + change)
                self.profile.risk_taking = min(1.0, self.profile.risk_taking + change)
            elif len(self.game_memory) > 1:
                # Usa memória de jogos para aprendizado
                memory_stats = {
                    'aggression': sum(g.get('aggression', 0.5) for g in self.game_memory[-5:]) / min(5, len(self.game_memory)),
                    'positional': sum(g.get('positional', 0.5) for g in self.game_memory[-5:]) / min(5, len(self.game_memory)),
                    'risk_taking': sum(g.get('risk_taking', 0.5) for g in self.game_memory[-5:]) / min(5, len(self.game_memory))
                }
                
                # Aplica aprendizado baseado na memória com taxa de aprendizado
                evolution_rate = learning_rate * self.profile.evolution_cycles
                self.profile.aggression += evolution_rate * (memory_stats['aggression'] - self.profile.aggression)
                self.profile.positional += evolution_rate * (memory_stats['positional'] - self.profile.positional)
                self.profile.risk_taking += evolution_rate * (memory_stats['risk_taking'] - self.profile.risk_taking)
            elif self.profile.learning_mode == LearningMode.AGGRESSIVE:
                # Se não há memória mas há evolution_cycles e modo agressivo
                change = 0.05 * self.profile.evolution_cycles * learning_rate
                self.profile.aggression = min(1.0, self.profile.aggression + change)
                self.profile.risk_taking = min(1.0, self.profile.risk_taking + change)
            elif self.profile.learning_mode == LearningMode.ACTIVE:
                self.profile.aggression += random.uniform(-0.05, 0.05)
                self.profile.positional += random.uniform(-0.05, 0.05)
                self.profile.risk_taking += random.uniform(-0.05, 0.05)
                
            # Garante que valores fiquem no intervalo [0, 1]
            self.profile.aggression = max(0.0, min(1.0, self.profile.aggression))
            self.profile.positional = max(0.0, min(1.0, self.profile.positional))
            self.profile.risk_taking = max(0.0, min(1.0, self.profile.risk_taking))
        
        # Adjust based on game result
        if game_result == "win":
            # Reinforce current strategy
            self.profile.wins += 1
        elif game_result == "loss":
            # Slightly adjust strategy
            self.profile.aggression = (self.profile.aggression + 0.5) / 2
            self.profile.risk_taking = (self.profile.risk_taking + 0.5) / 2
            self.profile.losses += 1
        else:
            self.profile.draws += 1
            
        self.profile.games_played += 1

    def save_profile(self, path: str) -> None:
        """Save the AI profile and game memory to a file."""
        data = {
            'profile': {
                'aggression': self.profile.aggression,
                'positional': self.profile.positional,
                'risk_taking': self.profile.risk_taking,
                'learning_rate': self.profile.learning_rate,
                'wins': self.profile.wins,
                'losses': self.profile.losses,
                'draws': self.profile.draws,
                'games_played': self.profile.games_played,
                'piece_preferences': {str(k): v for k, v in self.profile.piece_preferences.items()},
                'favorite_openings': self.profile.favorite_openings
            },
            'game_memory': self.game_memory,
            'move_scores': {str(k): v for k, v in self.move_scores.items()},
            'position_tables': {str(k): v.tolist() for k, v in self.position_tables.items()}
        }
        with open(path, 'w') as file:
            json.dump(data, file)

    @classmethod
    def load_profile(cls, path: str) -> 'AdaptiveAI':
        """Load the AI profile and game memory from a file."""
        try:
            with open(path, 'r') as file:
                data = json.load(file)
                profile_data = data['profile']
                
                # Create profile
                profile = PlayerProfile(
                    aggression=profile_data.get('aggression', 0.5),
                    positional=profile_data.get('positional', 0.5),
                    risk_taking=profile_data.get('risk_taking', 0.5),
                    learning_rate=profile_data.get('learning_rate', 0.1)
                )
                profile.wins = profile_data.get('wins', 0)
                profile.losses = profile_data.get('losses', 0)
                profile.draws = profile_data.get('draws', 0)
                profile.games_played = profile_data.get('games_played', 0)
                
                # Create AI instance
                ai = cls(profile=profile)
                
                # Load additional data
                ai.game_memory = data.get('game_memory', [])
                ai.move_scores = {tuple(eval(k)): v for k, v in data.get('move_scores', {}).items()}
                
                # Load position tables
                for k, v in data.get('position_tables', {}).items():
                    piece_type = None
                    if k in ['king_midgame', 'king_endgame']:
                        ai.position_tables[k] = np.array(v)
                    else:
                        for pt in PieceType:
                            if str(pt) == k:
                                piece_type = pt
                                break
                        if piece_type:
                            ai.position_tables[piece_type] = np.array(v)
                
                return ai
        except Exception as e:
            print(f"Error loading profile: {str(e)}")
            return cls()
    
    def _evaluate_mobility(self, board: Board, color: Color) -> float:
        """Evaluate the mobility of pieces for a given color."""
        mobility_score = 0.0
        
        if not hasattr(board, 'pieces') or not board.pieces:
            return 0.0
            
        for pos, piece in board.pieces.items():
            # Garante que a peça tem position configurado
            if not hasattr(piece, 'position') or piece.position is None:
                if isinstance(pos, tuple):
                    file_char = chr(ord('a') + pos[0])
                    # NOTA: Board usa rank direto da tupla, sem +1
                    piece.position = Position(file_char, pos[1])
            if piece.color == color:
                # get_valid_moves retorna uma lista de posições (Position)
                valid_moves = board.get_valid_moves(pos)
                # Cada movimento válido contribui para a mobilidade
                mobility_score += len(valid_moves) * 0.1
                # Bonus for controlling center squares
                for move_pos in valid_moves:
                    # move_pos é uma Position
                    if hasattr(move_pos, 'rank') and hasattr(move_pos, 'file'):
                        if 3 <= move_pos.rank <= 4 and 3 <= move_pos.file <= 4:
                            mobility_score += 0.05
                    elif isinstance(move_pos, tuple) and len(move_pos) == 2:
                        # Se for uma tupla (rank, file)
                        if 3 <= move_pos[0] <= 4 and 3 <= move_pos[1] <= 4:
                            mobility_score += 0.05
        return mobility_score
        
    def _simulate_games(self) -> PlayerProfile:
        """Simula jogos para evolução do perfil"""
        simulated_profile = PlayerProfile(
            aggression=self.profile.aggression,
            positional=self.profile.positional,
            risk_taking=self.profile.risk_taking
        )
        
        # Usa memória de jogos para simulação
        if self.game_memory:
            wins = 0
            total = min(10, len(self.game_memory))  # Limita a 10 jogos recentes
            
            for game in self.game_memory[-total:]:
                if game.get('result') == 'win':
                    wins += 1
                    # Reforça características bem sucedidas
                    simulated_profile.aggression += 0.1 * (game.get('aggression', 0) - simulated_profile.aggression)
                    simulated_profile.positional += 0.1 * (game.get('positional', 0) - simulated_profile.positional)
                    simulated_profile.risk_taking += 0.1 * (game.get('risk_taking', 0) - simulated_profile.risk_taking)
            
            # Ajusta baseado no sucesso geral
            if wins >= total * 0.6:  # Se ganhou 60% ou mais
                pass  # Mantém a direção atual
            else:
                # Reverte um pouco em direção à média
                simulated_profile.aggression = (simulated_profile.aggression + 0.5) / 2
                simulated_profile.positional = (simulated_profile.positional + 0.5) / 2
                simulated_profile.risk_taking = (simulated_profile.risk_taking + 0.5) / 2
        
        return simulated_profile
    
    def _evaluate_components(self, board: Board, color: Color) -> Tuple[float, float, float]:
        """Evaluate various components such as material, position, and king safety."""
        material_score = 0.0
        positional_score = 0.0
        king_safety_score = 0.0

        for piece in board.pieces.values():
            if piece.color == color:
                material_score += self.weights.piece_values[piece.type]
                positional_score += self.weights.positional_values[piece.type][piece.position.rank - 1][piece.position.file - 1]
            else:
                material_score -= self.weights.piece_values[piece.type]
                positional_score -= self.weights.positional_values[piece.type][piece.position.rank - 1][piece.position.file - 1]

        if board.is_in_check(color):
            king_safety_score -= 0.5 * self.weights.king_safety_weight
        if board.is_in_check(Color.BLACK if color == Color.WHITE else Color.WHITE):
            king_safety_score += 0.3 * self.weights.king_safety_weight

        return material_score, positional_score, king_safety_score
