from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from src.core.board.board import Board, Position, PieceType, Color, Piece
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

@dataclass
class PlayerProfile:
    """Profile representing player characteristics"""
    aggression: float = 0.5  # 0.0 = defensive, 1.0 = aggressive
    positional: float = 0.5  # 0.0 = tactical, 1.0 = positional
    risk_taking: float = 0.5  # 0.0 = conservative, 1.0 = risky
    opening_preference: str = "balanced"  # e.g. "open", "closed", "balanced"
    learning_rate: float = 0.1  # Taxa de aprendizado para adaptação
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
        self.profile = profile or PlayerProfile()
        self.weights = weights or EvaluationWeights()
        self.position_history: List[Board] = []
        self.move_scores: Dict[Tuple[Position, Position], float] = {}
        self.position_tables = {
            'pawn': np.array(self.weights.positional_values[PieceType.PAWN]),
            'knight': np.zeros((8, 8)),
            'bishop': np.zeros((8, 8)),
            'rook': np.zeros((8, 8)),
            'queen': np.zeros((8, 8)),
            'king_midgame': np.zeros((8, 8)),
            'king_endgame': np.zeros((8, 8))
        }
        self.learning_rate = self.profile.learning_rate
        self.move_times: List[float] = []
        
    def evaluate_position(self, board: Board, color: Optional[Color] = None) -> float:
        """Evaluate board position from given color's perspective"""
        if color is None:
            color = Color.WHITE
            
        score = 0.0
        
        # Material evaluation
        for piece in board.pieces.values():
            piece_value = self.weights.piece_values[piece.type]
            if piece.color == color:
                score += piece_value
            else:
                score -= piece_value
        
        # Development evaluation
        white_starting_rank = {PieceType.PAWN: 6, PieceType.KNIGHT: 7, PieceType.BISHOP: 7, PieceType.ROOK: 7, PieceType.QUEEN: 7}
        black_starting_rank = {PieceType.PAWN: 1, PieceType.KNIGHT: 0, PieceType.BISHOP: 0, PieceType.ROOK: 0, PieceType.QUEEN: 0}
        development_score = 0.0
        
        for piece in board.pieces.values():
            if piece.type == PieceType.KING:
                continue
                
            # Center control
            center_value = 0.0
            if 3 <= piece.position.rank <= 6 and 3 <= piece.position.file <= 6:
                center_value = 0.3  # Outer center
                if 4 <= piece.position.rank <= 5 and 4 <= piece.position.file <= 5:
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
    
    def get_best_move(self, board: Board, color: Optional[Color] = None, depth: int = 3) -> Optional[Tuple[Position, Position]]:
        if color is None:
            color = Color.WHITE
        """Get best move using minimax with alpha-beta pruning"""
        best_score = float('-inf')
        best_move = None
        
        # Get all valid moves for the current position
        all_moves = []
        for piece in board.pieces.values():
            if piece.color == color:
                for move in board.get_valid_moves(piece.position):
                    all_moves.append((piece.position, move))
        
        # Randomize move order slightly based on risk_taking profile
        if self.profile.risk_taking > 0.7:
            random.shuffle(all_moves)
        
        for from_pos, to_pos in all_moves:
            # Try move
            piece = board.get_piece(from_pos)
            captured = board.get_piece(to_pos)
            
            # Make temporary move
            old_pos = piece.position
            piece.position = to_pos
            if captured:
                del board.pieces[to_pos]
            del board.pieces[from_pos]
            board.pieces[to_pos] = piece
            
            # Evaluate position recursively
            score = -self._minimax(board, depth - 1, float('-inf'), float('inf'),
                                 Color.BLACK if color == Color.WHITE else Color.WHITE)
            
            # Add aggression bonus for captures
            if captured:
                capture_bonus = self.weights.piece_values[captured.type] * self.profile.aggression
                score += capture_bonus
            
            # Revert move
            piece.position = old_pos
            board.pieces[old_pos] = piece
            if captured:
                board.pieces[to_pos] = captured
            else:
                del board.pieces[to_pos]
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, color: Color) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0:
            return self.evaluate_position(board, color)
        
        try:
            if color == Color.WHITE:
                max_score = float('-inf')
                for piece in board.pieces.values():
                    if piece.color == color:
                        for move in board.get_valid_moves(piece.position):
                            try:
                                # Try move
                                captured = board.get_piece(move)
                                old_pos = piece.position
                                piece.position = move
                                if captured:
                                    del board.pieces[move]
                                del board.pieces[old_pos]
                                board.pieces[move] = piece
                                
                                score = self._minimax(board, depth - 1, alpha, beta, Color.BLACK)
                                
                                # Revert move
                                piece.position = old_pos
                                board.pieces[old_pos] = piece
                                if captured:
                                    board.pieces[move] = captured
                                else:
                                    del board.pieces[move]
                                
                                max_score = max(max_score, score)
                                alpha = max(alpha, score)
                                if beta <= alpha:
                                    break
                            except Exception as e:
                                print(f"Error processing move in minimax: {str(e)}")
                                continue
                return max_score
            else:
                min_score = float('inf')
                for piece in board.pieces.values():
                    if piece.color == color:
                        for move in board.get_valid_moves(piece.position):
                            try:
                                # Try move
                                captured = board.get_piece(move)
                                old_pos = piece.position
                                piece.position = move
                                if captured:
                                    del board.pieces[move]
                                del board.pieces[old_pos]
                                board.pieces[move] = piece
                                
                                score = self._minimax(board, depth - 1, alpha, beta, Color.WHITE)
                                
                                # Revert move
                                piece.position = old_pos
                                board.pieces[old_pos] = piece
                                if captured:
                                    board.pieces[move] = captured
                                else:
                                    del board.pieces[move]
                                
                                min_score = min(min_score, score)
                                beta = min(beta, score)
                                if beta <= alpha:
                                    break
                            except Exception as e:
                                print(f"Error processing move in minimax: {str(e)}")
                                continue
                return min_score
        except Exception as e:
            print(f"Error in minimax: {str(e)}")
            return 0.0
    
    def update_profile(self, board: Board, game_result: str):
        """Update AI profile based on board state and game result"""
        if not board or not game_result:
            return
            
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
            self.profile.aggression = 0.8 * self.profile.aggression + \
                                    0.2 * (aggressive_moves / total_moves)
            self.profile.positional = 0.8 * self.profile.positional + \
                                  0.2 * (positional_moves / total_moves)
            self.profile.risk_taking = 0.8 * self.profile.risk_taking + \
                                     0.2 * (risky_moves / total_moves)
        
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
        """Save the AI profile to a file."""
        profile_data = {
            'aggression': self.profile.aggression,
            'positional': self.profile.positional,
            'risk_taking': self.profile.risk_taking,
            'learning_rate': self.profile.learning_rate,
            'wins': self.profile.wins,
            'losses': self.profile.losses,
            'draws': self.profile.draws,
            'games_played': self.profile.games_played
        }
        with open(path, 'w') as file:
            json.dump(profile_data, file)

    @classmethod
    def load_profile(cls, path: str) -> 'AdaptiveAI':
        """Load the AI profile from a file."""
        try:
            with open(path, 'r') as file:
                profile_data = json.load(file)
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
                
                return cls(profile=profile)
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
