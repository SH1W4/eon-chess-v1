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

    @property
    def is_castle(self) -> bool:
        return bool(self.is_castling)

class ChessEngine:
    """Chess game engine implementation"""
    
    def __init__(self, board: Optional[Board] = None):
        self.board = board if board is not None else Board()
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

    def make_move(self, move: Move) -> Dict[str, object]:
        """Make a move on the board. Returns a result dict with {'success': bool}.
        Prefer delegating to the board's own move validation/execution to stay consistent.
        """
        # Convert positions to algebraic strings when needed
        def to_sq(p):
            try:
                return str(p)
            except Exception:
                return p
        from_sq = to_sq(move.from_pos)
        to_sq = to_sq(move.to_pos)

        # Attempt to ensure the board's turn matches the mover
        mover_piece = None
        try:
            mover_piece = self.get_piece(move.from_pos)
        except Exception:
            mover_piece = None
        if mover_piece is not None and hasattr(self.board, 'current_turn'):
            self.board.current_turn = mover_piece.color

        # Delegate to board if it implements move_piece(from: str, to: str)
        if hasattr(self.board, "move_piece"):
            try:
                # Debug: show piece at from_sq before delegating
                try:
                    present_piece = self.board.pieces.get(from_sq)
                    print(f"DEBUG(engine): attempting {from_sq}->{to_sq}, present_piece={present_piece}")
                except Exception:
                    pass
                result = self.board.move_piece(from_sq, to_sq)
                if isinstance(result, dict):
                    if result.get("success"):
                        self.move_history.append(move)
                        return result
                    else:
                        # Minimal debug to help diagnose illegal AI moves
                        print(f"DEBUG(engine): move_piece failed for {from_sq}->{to_sq} reason={result}")
                        return result
            except TypeError as e:
                # Fallback to core signature if adapter differs
                print(f"DEBUG(engine): TypeError delegating move: {e}")
                pass

        # Fallback: minimal internal execution with legality check
        piece = mover_piece or self.get_piece(move.from_pos)
        if not piece:
            return {"success": False, "reason": "no_piece"}
        if piece.color != self.board.current_turn:
            return {"success": False, "reason": "wrong_turn"}
        if move.to_pos not in self.board.get_valid_moves(move.from_pos):
            return {"success": False, "reason": "illegal_move"}
        captured = self.get_piece(move.to_pos)
        if captured:
            self.board.captured_pieces.append(captured)
        self.set_piece(move.from_pos, None)
        self.set_piece(move.to_pos, piece)
        try:
            piece.position = move.to_pos
        except Exception:
            pass
        piece.has_moved = True
        self.board.current_turn = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
        self.move_history.append(move)
        return {"success": True}
    
    def get_legal_moves(self, position: Position) -> List[Position]:
        """Get all legal moves for a piece at the given position"""
        return self.board.get_valid_moves(position)

    def _can_execute_move(self, from_sq: str, to_sq: str) -> bool:
        # Backup minimal board state
        pieces_backup = self.board.pieces.copy()
        captured_backup = list(getattr(self.board, 'captured_pieces', []))
        turn_backup = getattr(self.board, 'current_turn', None)
        last_backup = getattr(self.board, 'last_move', None)
        try:
            result = self.board.move_piece(from_sq, to_sq)
            return isinstance(result, dict) and result.get('success') is True
        finally:
            # Restore state
            self.board.pieces = pieces_backup
            if hasattr(self.board, 'captured_pieces'):
                self.board.captured_pieces = captured_backup
            if turn_backup is not None:
                self.board.current_turn = turn_backup
            if hasattr(self.board, 'last_move'):
                self.board.last_move = last_backup

    def get_valid_moves(self, color: str) -> List[Move]:
        """Retorna lista de Moves legais para a cor fornecida, validando via board.move_piece."""
        color_enum = Color.WHITE if str(color).lower().startswith("w") else Color.BLACK
        moves: List[Move] = []
        for pos, piece in list(self.board.pieces.items()):
            if piece.color != color_enum:
                continue
            candidates = self.board.get_valid_moves(pos)
            for to_pos in candidates:
                from_sq = str(pos)
                to_sq = str(to_pos)
                if self._can_execute_move(from_sq, to_sq):
                    moves.append(Move(from_pos=pos, to_pos=to_pos, piece=piece))
        # Se por alguma razão não houver movimentos (ex. implementação parcial), pequeno fallback de peões
        if not moves:
            for pos, piece in list(self.board.pieces.items()):
                if piece.color != color_enum or piece.type != PieceType.PAWN:
                    continue
                try:
                    from_sq = str(pos)  # pos já é string
                    file_char = from_sq[0]
                    rank = int(from_sq[1])
                    # Direção por cor
                    dir_step = 1 if color_enum == Color.WHITE else -1
                    one_step_sq = f"{file_char}{rank + dir_step}"
                    # Casa livre para um passo
                    if self.board.pieces.get(one_step_sq) is None and self._can_execute_move(from_sq, one_step_sq):
                        to_pos = Position.from_algebraic(one_step_sq)
                        moves.append(Move(from_pos=pos, to_pos=to_pos, piece=piece))
                        continue
                except Exception:
                    continue
        return moves
    
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
