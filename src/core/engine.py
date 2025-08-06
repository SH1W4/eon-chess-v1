from typing import List, Optional
from .board.board import Board, Position, PieceType, Color, Piece
from .board.move import Move

class ChessEngine:
    def __init__(self):
        self.board = Board()
        self.current_player = Color.WHITE
        self.move_history = []
        
    def get_piece(self, pos: Position) -> Optional[Piece]:
        """Get piece at given position"""
        return self.board.get_piece(pos)
        
    def make_move(self, move: Move) -> bool:
        """Make a move on the board
        
        Args:
            move: The move to make
            
        Returns:
            bool: True if move was valid and executed, False otherwise
        """
        if self._is_legal_move(move):
            # Make the move on the board
            from_piece = self.board.get_piece(move.from_pos)
            to_piece = self.board.get_piece(move.to_pos)
            
            # Update board state
            self.board.squares[(move.from_pos.file, move.from_pos.rank)] = None
            self.board.squares[(move.to_pos.file, move.to_pos.rank)] = from_piece
            if from_piece:
                from_piece.position = move.to_pos
            
            # If there was a piece captured, update piece list
            if to_piece:
                if to_piece in self.board.piece_list:
                    self.board.piece_list.remove(to_piece)
            
            # Add move to history
            self.move_history.append(move)
            return True
            
        return False
        
    def get_legal_moves(self, pos: Position) -> List[Position]:
        """Get list of legal moves from given position
        
        Args:
            pos: Starting position
            
        Returns:
            list[Position]: List of valid destination positions
        """
        piece = self.board.get_piece(pos)
        if not piece:
            return []
        
        moves = []
        for rank in range(8):
            for file in range(8):
                to_pos = Position(file=file, rank=rank)
                move = Move(from_pos=pos, to_pos=to_pos, piece=piece)
                if self._is_legal_move(move):
                    moves.append(to_pos)
        return moves
        
    def _is_legal_move(self, move: Move) -> bool:
        """Check if a move is legal
        
        Args:
            move: The move to check
            
        Returns:
            bool: True if move is legal, False otherwise
        """
        # Basic validation
        if not self._is_valid_position(move.from_pos) or not self._is_valid_position(move.to_pos):
            return False
            
        # Get piece at starting position
        piece = self.board.get_piece(move.from_pos)
        if not piece or piece != move.piece:
            return False
            
        # Validate move follows piece rules (use board's validation)
        return self.board._is_valid_piece_move(move)
        
    def _is_valid_position(self, pos: Position) -> bool:
        """Check if position is within board bounds"""
        return 0 <= pos.file < 8 and 0 <= pos.rank < 8
