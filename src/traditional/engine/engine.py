from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
from src.core.board.board import Board, Position, Piece, PieceType, Color

@dataclass
class Move:
    """Represents a chess move"""
    from_pos: Position
    to_pos: Position
    piece: Piece
    captured_piece: Optional[Piece] = None
    is_castling: bool = False
    is_en_passant: bool = False
    promotion_piece_type: Optional[PieceType] = None

class ChessEngine:
    """Chess game engine implementation"""
    
    def __init__(self):
        self.board = Board()
        self.move_history: List[Move] = []
        self.current_position = self.board  # Reference to current board state
    
    def get_piece(self, position: Position) -> Optional[Piece]:
        """Get piece at the given position"""
        return self.board.get_piece(position)
    
    def set_piece(self, position: Position, piece: Optional[Piece]) -> None:
        """Set or remove a piece at the given position"""
        if piece is None:
            if position in self.board.pieces:
                del self.board.pieces[position]
        else:
            self.board.pieces[position] = piece
    
    def make_move(self, move: Move) -> bool:
        """Make a move on the board"""
        # Get pieces involved
        piece = self.get_piece(move.from_pos)
        if not piece:
            return False
            
        # Validate turn
        if piece.color != self.board.current_turn:
            return False
            
        # Check if move is legal
        if move.to_pos not in self.board.get_valid_moves(move.from_pos):
            return False

        # Get captured piece if any
        captured = self.get_piece(move.to_pos)
        
        # Detect castling
        is_castling = (piece.type == PieceType.KING and 
                      abs(move.from_pos.file - move.to_pos.file) == 2)
        
        if is_castling:
            # Execute castling move
            rank = move.from_pos.rank
            if move.to_pos.file == 7:  # Kingside
                rook_from = Position(rank, 8)
                rook_to = Position(rank, 6)
                rook = self.get_piece(rook_from)
                if not rook or rook.has_moved or piece.has_moved:
                    return False
                    
                # Move both pieces
                self.set_piece(rook_from, None)
                self.set_piece(rook_to, rook)
                rook.position = rook_to
                rook.has_moved = True
                
            else:  # Queenside
                rook_from = Position(rank, 1)
                rook_to = Position(rank, 4)
                rook = self.get_piece(rook_from)
                if not rook or rook.has_moved or piece.has_moved:
                    return False
                    
                # Move both pieces
                self.set_piece(rook_from, None)
                self.set_piece(rook_to, rook)
                rook.position = rook_to
                rook.has_moved = True
            
            # Move the king
            self.set_piece(move.from_pos, None)
            self.set_piece(move.to_pos, piece)
            piece.position = move.to_pos
            piece.has_moved = True
            move.is_castling = True
            
        # Handle promotion
        elif move.promotion_piece_type and piece.type == PieceType.PAWN:
            if (piece.color == Color.WHITE and move.to_pos.rank == 8) or \
               (piece.color == Color.BLACK and move.to_pos.rank == 1):
                # Execute promotion
                if captured:
                    del self.board.pieces[move.to_pos]
                del self.board.pieces[move.from_pos]
                new_piece = Piece(
                    type=move.promotion_piece_type,
                    color=piece.color,
                    position=move.to_pos,
                    has_moved=True
                )
                self.board.pieces[move.to_pos] = new_piece
                
        else:
            # Normal move
            if captured:
                self.board.captured_pieces.append(captured)
                
            self.set_piece(move.from_pos, None)
            self.set_piece(move.to_pos, piece)
            piece.position = move.to_pos
            piece.has_moved = True
            
        # Update game state
        self.board.current_turn = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
        self.move_history.append(move)
        
        return True
    
    def get_legal_moves(self, position: Position) -> List[Position]:
        """Get all legal moves for a piece at the given position"""
        return self.board.get_valid_moves(position)
    
    def is_checkmate(self) -> bool:
        """Check if the game is in checkmate state"""
        return self.board.is_checkmate()

    def is_stalemate(self) -> bool:
        """Check if the game is in stalemate state"""
        return self.board.is_stalemate()

    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """Check if the game is over and return the result"""
        if self.is_checkmate():
            winner = "Black" if self.board.current_turn == Color.WHITE else "White"
            return True, f"Checkmate - {winner} wins"
            
        if self.is_stalemate():
            return True, "Stalemate - Draw"
            
        # TODO: Implement other draw conditions
        # - Insufficient material
        # - Threefold repetition
        # - Fifty-move rule
        
        return False, None
    
    def get_game_state(self) -> Dict:
        """Get current game state"""
        return {
            'board': str(self.board),
            'current_turn': self.board.current_turn,
            'white_captured': [p for p in self.board.captured_pieces if p.color == Color.WHITE],
            'black_captured': [p for p in self.board.captured_pieces if p.color == Color.BLACK],
            'move_history': self.move_history,
            'is_check': self.board.is_in_check(self.board.current_turn),
            'legal_moves': sum(1 for p in self.board.pieces.values() 
                             if p.color == self.board.current_turn 
                             for _ in self.board.get_valid_moves(p.position))
        }
    
    def undo_last_move(self) -> bool:
        """Undo the last move made"""
        if not self.move_history:
            return False
            
        last_move = self.move_history.pop()
        piece = self.get_piece(last_move.to_pos)
        if not piece:
            return False
            
        # Restore piece to original position
        piece.position = last_move.from_pos
        piece.has_moved = False  # This might need to track previous state
        self.board.pieces[last_move.from_pos] = piece
        del self.board.pieces[last_move.to_pos]
        
        # Restore captured piece if any
        if last_move.captured_piece:
            self.board.pieces[last_move.to_pos] = last_move.captured_piece
            if last_move.captured_piece in self.board.captured_pieces:
                self.board.captured_pieces.remove(last_move.captured_piece)
                
        # Handle castling undo
        if last_move.is_castling:
            rank = last_move.from_pos.rank
            if last_move.to_pos.file == 7:  # Kingside
                rook = self.get_piece(Position(rank, 6))
                if rook:
                    del self.board.pieces[Position(rank, 6)]
                    rook.position = Position(rank, 8)
                    rook.has_moved = False
                    self.board.pieces[Position(rank, 8)] = rook
            else:  # Queenside
                rook = self.get_piece(Position(rank, 4))
                if rook:
                    del self.board.pieces[Position(rank, 4)]
                    rook.position = Position(rank, 1)
                    rook.has_moved = False
                    self.board.pieces[Position(rank, 1)] = rook
        
        # Restore turn
        self.board.current_turn = Color.BLACK if self.board.current_turn == Color.WHITE else Color.WHITE
        
        return True
