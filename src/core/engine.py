from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
import json

@dataclass
class Position:
    row: int
    col: int

    def to_algebraic(self) -> str:
        """Convert position to algebraic notation (e.g. e4)"""
        return f"{chr(97 + self.col)}{8 - self.row}"

    @staticmethod
    def from_algebraic(algebraic: str) -> 'Position':
        """Create position from algebraic notation"""
        col = ord(algebraic[0]) - 97
        row = 8 - int(algebraic[1])
        return Position(row, col)

@dataclass
class Piece:
    type: str  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
    color: str  # 'white', 'black'
    has_moved: bool = False

@dataclass
class Move:
    from_pos: Position
    to_pos: Position
    piece: Piece
    captured_piece: Optional[Piece] = None
    is_castling: bool = False
    is_en_passant: bool = False
    promotion_piece: Optional[str] = None

class ChessEngine:
    def __init__(self):
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.current_player: str = 'white'
        self.move_history: List[Move] = []
        self.initialize_board()

    def initialize_board(self):
        """Set up the initial chess board configuration"""
        # Setup pawns
        for col in range(8):
            self.board[1][col] = Piece('pawn', 'black')
            self.board[6][col] = Piece('pawn', 'white')

        # Setup other pieces
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col, piece_type in enumerate(pieces):
            self.board[0][col] = Piece(piece_type, 'black')
            self.board[7][col] = Piece(piece_type, 'white')

    def get_piece(self, pos: Position) -> Optional[Piece]:
        """Get piece at given position"""
        return self.board[pos.row][pos.col]

    def set_piece(self, pos: Position, piece: Optional[Piece]):
        """Set or remove piece at given position"""
        self.board[pos.row][pos.col] = piece

    def is_valid_position(self, pos: Position) -> bool:
        """Check if position is within board boundaries"""
        return 0 <= pos.row < 8 and 0 <= pos.col < 8

    def get_legal_moves(self, pos: Position) -> List[Position]:
        """Get all legal moves for piece at given position"""
        piece = self.get_piece(pos)
        if not piece or piece.color != self.current_player:
            return []

        moves = []
        if piece.type == 'pawn':
            moves.extend(self._get_pawn_moves(pos))
        elif piece.type == 'knight':
            moves.extend(self._get_knight_moves(pos))
        elif piece.type == 'bishop':
            moves.extend(self._get_bishop_moves(pos))
        elif piece.type == 'rook':
            moves.extend(self._get_rook_moves(pos))
        elif piece.type == 'queen':
            moves.extend(self._get_queen_moves(pos))
        elif piece.type == 'king':
            moves.extend(self._get_king_moves(pos))

        # Filter moves that would leave king in check
        return [move for move in moves if not self._would_be_in_check(pos, move)]

    def _get_pawn_moves(self, pos: Position) -> List[Position]:
        moves = []
        piece = self.get_piece(pos)
        direction = -1 if piece.color == 'white' else 1
        
        # Forward move
        next_pos = Position(pos.row + direction, pos.col)
        if self.is_valid_position(next_pos) and not self.get_piece(next_pos):
            moves.append(next_pos)
            # Initial two-square move
            if not piece.has_moved:
                double_pos = Position(pos.row + 2 * direction, pos.col)
                if not self.get_piece(double_pos):
                    moves.append(double_pos)

        # Captures
        for col_offset in [-1, 1]:
            capture_pos = Position(pos.row + direction, pos.col + col_offset)
            if self.is_valid_position(capture_pos):
                target = self.get_piece(capture_pos)
                if target and target.color != piece.color:
                    moves.append(capture_pos)

        return moves

    def _get_knight_moves(self, pos: Position) -> List[Position]:
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for row_offset, col_offset in offsets:
            new_pos = Position(pos.row + row_offset, pos.col + col_offset)
            if self.is_valid_position(new_pos):
                target = self.get_piece(new_pos)
                if not target or target.color != self.current_player:
                    moves.append(new_pos)
        
        return moves

    def _get_bishop_moves(self, pos: Position) -> List[Position]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for row_dir, col_dir in directions:
            current = Position(pos.row + row_dir, pos.col + col_dir)
            while self.is_valid_position(current):
                target = self.get_piece(current)
                if not target:
                    moves.append(current)
                elif target.color != self.current_player:
                    moves.append(current)
                    break
                else:
                    break
                current = Position(current.row + row_dir, current.col + col_dir)
        
        return moves

    def _get_rook_moves(self, pos: Position) -> List[Position]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for row_dir, col_dir in directions:
            current = Position(pos.row + row_dir, pos.col + col_dir)
            while self.is_valid_position(current):
                target = self.get_piece(current)
                if not target:
                    moves.append(current)
                elif target.color != self.current_player:
                    moves.append(current)
                    break
                else:
                    break
                current = Position(current.row + row_dir, current.col + col_dir)
        
        return moves

    def _get_queen_moves(self, pos: Position) -> List[Position]:
        return self._get_bishop_moves(pos) + self._get_rook_moves(pos)

    def _get_king_moves(self, pos: Position) -> List[Position]:
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for row_dir, col_dir in directions:
            new_pos = Position(pos.row + row_dir, pos.col + col_dir)
            if self.is_valid_position(new_pos):
                target = self.get_piece(new_pos)
                if not target or target.color != self.current_player:
                    moves.append(new_pos)
        
        # Add castling moves if available
        if not self._is_in_check(self.current_player):
            moves.extend(self._get_castling_moves(pos))
        
        return moves

    def _get_castling_moves(self, pos: Position) -> List[Position]:
        moves = []
        piece = self.get_piece(pos)
        if piece.type != 'king' or piece.has_moved:
            return moves

        row = pos.row
        # Kingside castling
        if (not self.get_piece(Position(row, 5)) and 
            not self.get_piece(Position(row, 6)) and 
            isinstance(self.get_piece(Position(row, 7)), Piece) and 
            not self.get_piece(Position(row, 7)).has_moved):
            moves.append(Position(row, 6))

        # Queenside castling
        if (not self.get_piece(Position(row, 3)) and 
            not self.get_piece(Position(row, 2)) and 
            not self.get_piece(Position(row, 1)) and 
            isinstance(self.get_piece(Position(row, 0)), Piece) and 
            not self.get_piece(Position(row, 0)).has_moved):
            moves.append(Position(row, 2))

        return moves

    def make_move(self, move: Move) -> bool:
        """Execute a move on the board"""
        if not self._is_legal_move(move):
            return False

        # Store the move
        self.move_history.append(move)

        # Update pieces
        piece = self.get_piece(move.from_pos)
        self.set_piece(move.from_pos, None)
        self.set_piece(move.to_pos, piece)
        piece.has_moved = True

        # Handle castling
        if move.is_castling:
            if move.to_pos.col == 6:  # Kingside
                rook_from = Position(move.from_pos.row, 7)
                rook_to = Position(move.from_pos.row, 5)
            else:  # Queenside
                rook_from = Position(move.from_pos.row, 0)
                rook_to = Position(move.from_pos.row, 3)
            rook = self.get_piece(rook_from)
            self.set_piece(rook_from, None)
            self.set_piece(rook_to, rook)
            rook.has_moved = True

        # Handle promotion
        if move.promotion_piece:
            self.set_piece(move.to_pos, Piece(move.promotion_piece, self.current_player))

        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def _is_legal_move(self, move: Move) -> bool:
        """Check if move is legal"""
        piece = self.get_piece(move.from_pos)
        if not piece or piece.color != self.current_player:
            return False

        legal_moves = self.get_legal_moves(move.from_pos)
        return move.to_pos in legal_moves

    def _is_in_check(self, color: str) -> bool:
        """Determine if the given color's king is in check"""
        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.type == 'king' and piece.color == color:
                    king_pos = Position(row, col)
                    break
            if king_pos:
                break

        # Check if any opponent piece can capture king
        opponent = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = self.get_piece(pos)
                if piece and piece.color == opponent:
                    moves = self.get_legal_moves(pos)
                    if king_pos in moves:
                        return True
        return False

    def _would_be_in_check(self, from_pos: Position, to_pos: Position) -> bool:
        """Check if moving piece would leave/put own king in check"""
        # Make temporary move
        piece = self.get_piece(from_pos)
        captured = self.get_piece(to_pos)
        self.set_piece(to_pos, piece)
        self.set_piece(from_pos, None)

        # Check if in check
        in_check = self._is_in_check(self.current_player)

        # Undo move
        self.set_piece(from_pos, piece)
        self.set_piece(to_pos, captured)

        return in_check

    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate"""
        if not self._is_in_check(self.current_player):
            return False

        # Check if any piece has legal moves
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = self.get_piece(pos)
                if piece and piece.color == self.current_player:
                    if self.get_legal_moves(pos):
                        return False
        return True

    def is_stalemate(self) -> bool:
        """Check if current player is in stalemate"""
        if self._is_in_check(self.current_player):
            return False

        # Check if any piece has legal moves
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                piece = self.get_piece(pos)
                if piece and piece.color == self.current_player:
                    if self.get_legal_moves(pos):
                        return False
        return True

    def get_game_state(self) -> Dict:
        """Get current game state"""
        return {
            'board': [[piece.__dict__ if piece else None for piece in row] 
                     for row in self.board],
            'current_player': self.current_player,
            'move_history': [move.__dict__ for move in self.move_history],
            'is_check': self._is_in_check(self.current_player),
            'is_checkmate': self.is_checkmate(),
            'is_stalemate': self.is_stalemate()
        }
    
    def _undo_move(self) -> None:
        """Desfaz o último movimento realizado"""
        if not self.move_history:
            return
            
        # Recuperar último movimento
        move = self.move_history.pop()
        
        # Retornar a peça para a posição original
        piece = self.get_piece(move.to_pos)
        if piece:
            self.set_piece(move.from_pos, piece)
            piece.has_moved = False  # Resetar flag de movimento
        
        # Restaurar peça capturada, se houver
        self.set_piece(move.to_pos, move.captured_piece)
        
        # Desfazer roque, se necessário
        if move.is_castling:
            if move.to_pos.col == 6:  # Roque curto
                rook = self.get_piece(Position(move.from_pos.row, 5))
                if rook:
                    self.set_piece(Position(move.from_pos.row, 7), rook)
                    self.set_piece(Position(move.from_pos.row, 5), None)
                    rook.has_moved = False
            else:  # Roque longo
                rook = self.get_piece(Position(move.from_pos.row, 3))
                if rook:
                    self.set_piece(Position(move.from_pos.row, 0), rook)
                    self.set_piece(Position(move.from_pos.row, 3), None)
                    rook.has_moved = False
        
        # Trocar jogador
        self.current_player = 'black' if self.current_player == 'white' else 'white'
