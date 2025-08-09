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
        for piece in board.piece_list:
            piece_value = self.weights.piece_values[piece.type]
            if piece.color == color:
                score += piece_value
            else:
                score -= piece_value
        
        # Development evaluation
        white_starting_rank = {PieceType.PAWN: 6, PieceType.KNIGHT: 7, PieceType.BISHOP: 7, PieceType.ROOK: 7, PieceType.QUEEN: 7}
        black_starting_rank = {PieceType.PAWN: 1, PieceType.KNIGHT: 0, PieceType.BISHOP: 0, PieceType.ROOK: 0, PieceType.QUEEN: 0}
        development_score = 0.0
        
        for piece in board.piece_list:
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
    
    def get_best_move(self, board: Board, color: Optional[Color] = None, depth: int = 3) -> Optional[Move]:
        """Get best move using minimax with alpha-beta pruning"""
        if color is None:
            color = Color.WHITE
            
        best_score = float('-inf')
        best_move = None
        
        # Get all valid moves for the current position
        all_moves = []
        for piece in board.piece_list:
            if piece.color == color:
                for to_pos in board.get_valid_moves(piece.position):
                    move = Move(piece.position, to_pos, piece)
                    if board.get_piece(to_pos):
                        move.captured_piece = board.get_piece(to_pos)
                    all_moves.append(move)
        
        # Randomize move order slightly based on risk_taking profile
        if self.profile.risk_taking > 0.7:
            random.shuffle(all_moves)
        
        for move in all_moves:
            # Make copy of board for evaluation
            board_copy = Board()
            board_copy.squares = board.squares.copy()
            board_copy.piece_list = board.piece_list.copy()
            
            # Try move
            if board_copy.make_move(move):
            
                # Evaluate position recursively
                score = -self._minimax(board_copy, depth - 1, float('-inf'), float('inf'),
                                     Color.BLACK if color == Color.WHITE else Color.WHITE)
                
                # Add aggression bonus for captures
                if move.captured_piece:
                    capture_bonus = self.weights.piece_values[move.captured_piece.type] * self.profile.aggression
                    score += capture_bonus
                
                if score > best_score:
                    best_score = score
                    best_move = move
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, color: Color) -> float:
        # Verifica cache de transposição
        tt_entry = self.transposition_table.lookup(board)
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
            for piece in board.piece_list:
                if piece.color == color:
                    for to_pos in board.get_valid_moves(piece.position):
                        moves.append(Move(piece.position, to_pos, piece))
            
            # Order moves to improve alpha-beta pruning
            moves = self._order_moves(board, moves)
            
            for move in moves:
                # Make copy of board
                board_copy = Board()
                board_copy.squares = board.squares.copy()
                board_copy.piece_list = board.piece_list.copy()
                
                if board_copy.make_move(move):
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
            for piece in board.piece_list:
                if piece.color == color:
                    for to_pos in board.get_valid_moves(piece.position):
                        moves.append(Move(piece.position, to_pos, piece))
            
            # Order moves to improve alpha-beta pruning
            moves = self._order_moves(board, moves)
            
            for move in moves:
                # Make copy of board
                board_copy = Board()
                board_copy.squares = board.squares.copy()
                board_copy.piece_list = board.piece_list.copy()
                
                if board_copy.make_move(move):
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
            if 2 <= move.to_pos.rank <= 5 and 2 <= move.to_pos.file <= 5:
                score += 0.3
                if 3 <= move.to_pos.rank <= 4 and 3 <= move.to_pos.file <= 4:
                    score += 0.2
            
            move_scores.append((score, move))
        
        # Sort moves by score in descending order
        move_scores.sort(reverse=True)
        return [move for _, move in move_scores]
    
    def update_profile(self, board: Board, game_result: str):
        """Update AI profile based on board state and game result"""
        if not board or not game_result:
            return
            
        # Ajusta a taxa de aprendizado baseado no modo
        base_learning_rate = self.profile.learning_rate
        if self.profile.learning_mode == LearningMode.PASSIVE:
            self.learning_rate = base_learning_rate * 0.5
        elif self.profile.learning_mode == LearningMode.ACTIVE:
            self.learning_rate = base_learning_rate
        else:  # AGGRESSIVE
            self.learning_rate = base_learning_rate * 2.0
            
        # Analyze final position
        aggressive_moves = 0
        positional_moves = 0
        risky_moves = 0
        total_moves = len(board.move_history)
        
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
            
            # Evolução adicional baseada nos ciclos
            for _ in range(self.profile.evolution_cycles - 1):
                # Simula jogos usando o perfil atual
                simulated_profile = self._simulate_games()
                # Incorpora resultados da simulação
                self.profile.aggression = (self.profile.aggression + simulated_profile.aggression) / 2
                self.profile.positional = (self.profile.positional + simulated_profile.positional) / 2
                self.profile.risk_taking = (self.profile.risk_taking + simulated_profile.risk_taking) / 2
        
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
        for pos, piece in board.pieces.items():
            if piece.color == color:
                valid_moves = board.get_valid_moves(pos)
                mobility_score += len(valid_moves) * 0.1
                # Bonus for controlling center squares
                for move in valid_moves:
                    if 3 <= move.rank <= 6 and 3 <= move.file <= 6:
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
