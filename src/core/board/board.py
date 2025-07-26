"""Chess board implementation"""
from enum import Enum
import copy
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


class PieceType(Enum):
    """Chess piece types"""
    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"


class Color(Enum):
    """Chess piece colors"""
    WHITE = "white"
    BLACK = "black"


@dataclass(frozen=True)
class Position:
    """Board position"""
    rank: int  # 1-8
    file: int  # 1-8 (a-h)
    
    def __hash__(self):
        return hash((self.rank, self.file))

    @classmethod
    def from_algebraic(cls, notation: str) -> 'Position':
        """Create position from algebraic notation (e.g., 'e4')"""
        file = ord(notation[0].lower()) - ord('a') + 1
        rank = int(notation[1])
        return cls(rank=rank, file=file)
    
    def to_algebraic(self) -> str:
        """Convert to algebraic notation"""
        file = chr(self.file + ord('a') - 1)
        return f"{file}{self.rank}"


@dataclass
class Piece:
    """Chess piece"""
    type: PieceType
    color: Color
    position: Position
    has_moved: bool = False

    def symbol(self) -> str:
        """Return ASCII symbol for the piece"""
        symbols = {
            (PieceType.KING, Color.WHITE): "K",
            (PieceType.QUEEN, Color.WHITE): "Q",
            (PieceType.ROOK, Color.WHITE): "R",
            (PieceType.BISHOP, Color.WHITE): "B",
            (PieceType.KNIGHT, Color.WHITE): "N",
            (PieceType.PAWN, Color.WHITE): "P",
            (PieceType.KING, Color.BLACK): "k",
            (PieceType.QUEEN, Color.BLACK): "q",
            (PieceType.ROOK, Color.BLACK): "r",
            (PieceType.BISHOP, Color.BLACK): "b",
            (PieceType.KNIGHT, Color.BLACK): "n",
            (PieceType.PAWN, Color.BLACK): "p"
        }
        return symbols[(self.type, self.color)]


class Board:
    """Chess board implementation"""
    
    def __init__(self):
        self.pieces: Dict[Position, Piece] = {}
        self.captured_pieces: List[Piece] = []
        self.move_history: List[Tuple[Position, Position]] = []
        self.current_turn = Color.WHITE
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        """Setup initial piece positions"""
        # White pieces
        self._place_piece(PieceType.ROOK, Color.WHITE, Position(1, 1))
        self._place_piece(PieceType.KNIGHT, Color.WHITE, Position(1, 2))
        self._place_piece(PieceType.BISHOP, Color.WHITE, Position(1, 3))
        self._place_piece(PieceType.QUEEN, Color.WHITE, Position(1, 4))
        self._place_piece(PieceType.KING, Color.WHITE, Position(1, 5))
        self._place_piece(PieceType.BISHOP, Color.WHITE, Position(1, 6))
        self._place_piece(PieceType.KNIGHT, Color.WHITE, Position(1, 7))
        self._place_piece(PieceType.ROOK, Color.WHITE, Position(1, 8))
        for file in range(1, 9):
            self._place_piece(PieceType.PAWN, Color.WHITE, Position(2, file))

        # Black pieces
        self._place_piece(PieceType.ROOK, Color.BLACK, Position(8, 1))
        self._place_piece(PieceType.KNIGHT, Color.BLACK, Position(8, 2))
        self._place_piece(PieceType.BISHOP, Color.BLACK, Position(8, 3))
        self._place_piece(PieceType.QUEEN, Color.BLACK, Position(8, 4))
        self._place_piece(PieceType.KING, Color.BLACK, Position(8, 5))
        self._place_piece(PieceType.BISHOP, Color.BLACK, Position(8, 6))
        self._place_piece(PieceType.KNIGHT, Color.BLACK, Position(8, 7))
        self._place_piece(PieceType.ROOK, Color.BLACK, Position(8, 8))
        for file in range(1, 9):
            self._place_piece(PieceType.PAWN, Color.BLACK, Position(7, file))
    
    def _place_piece(self, piece_type: PieceType, color: Color, position: Position):
        """Place a piece on the board"""
        piece = Piece(type=piece_type, color=color, position=position)
        self.pieces[position] = piece
    
    def get_piece(self, position: Position) -> Optional[Piece]:
        """Get piece at a position"""
        return self.pieces.get(position)
    
    def is_in_check(self, color: Color) -> bool:
        """Check if the king is in check"""
        # Find king position
        king_pos = None
        for piece in self.pieces.values():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = piece.position
                break

        if not king_pos:
            print(f"King not found for {color}")
            return False
        
        print(f"Checking if {color} king at {king_pos.to_algebraic()} is in check")
        
        # Determine attacking color
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        # Check if any opponent piece can attack the king
        for piece in self.pieces.values():
            if piece.color != color:  # Any opponent piece
                # Check based on piece type
                print(f"Checking piece {piece.type} at {piece.position.to_algebraic()}")
                if piece.type == PieceType.PAWN:
                    # Pawns only attack diagonally forward
                    attack_direction = 1 if piece.color == Color.WHITE else -1
                    for file_offset in [-1, 1]:
                        attack_pos = Position(
                            piece.position.rank + attack_direction,
                            piece.position.file + file_offset
                        )
                        if (1 <= attack_pos.rank <= 8 and 
                            1 <= attack_pos.file <= 8 and
                            attack_pos == king_pos):
                            print(f"FOUND CHECK: King at {king_pos.to_algebraic()} is in check by pawn at {piece.position.to_algebraic()}")
                            return True
                            
                elif piece.type == PieceType.KNIGHT:
                    # Knights have fixed attack pattern
                    for dr, df in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                  (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        attack_pos = Position(
                            piece.position.rank + dr,
                            piece.position.file + df
                        )
                        if (1 <= attack_pos.rank <= 8 and 
                            1 <= attack_pos.file <= 8 and
                            attack_pos == king_pos):
                            print(f"FOUND CHECK: King at {king_pos.to_algebraic()} is in check by knight at {piece.position.to_algebraic()}")
                            return True
                            
                elif piece.type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
                    # These pieces attack along lines
                    directions = []
                    if piece.type in [PieceType.BISHOP, PieceType.QUEEN]:
                        directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
                    if piece.type in [PieceType.ROOK, PieceType.QUEEN]:
                        directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
                    
                    for dr, df in directions:
                        for distance in range(1, 8):
                            attack_pos = Position(
                                piece.position.rank + dr * distance,
                                piece.position.file + df * distance
                            )
                            # Stop at board edge
                            if not (1 <= attack_pos.rank <= 8 and 1 <= attack_pos.file <= 8):
                                break
                                
                            # Found the king in this direction
                            if attack_pos == king_pos:
                                print(f"FOUND CHECK: King at {king_pos.to_algebraic()} is in check by {piece.type} at {piece.position.to_algebraic()}")
                                return True
                                
                            # Stop scanning if we hit any piece that isn't the target
                            target = self.get_piece(attack_pos)
                            if target and target.position != king_pos:
                                break

        return False
    
    def _is_square_attacked_no_castling(self, pos: Position, color: Color) -> bool:
        """Check if a square is attacked by the opposite color (without considering castling)"""
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for piece in self.pieces.values():
            if piece.color == opponent_color:  # Any opponent piece
                # Check based on piece type
                if piece.type == PieceType.PAWN:
                    # Pawns only attack diagonally forward
                    attack_direction = 1 if piece.color == Color.WHITE else -1
                    for file_offset in [-1, 1]:
                        attack_pos = Position(
                            piece.position.rank + attack_direction,
                            piece.position.file + file_offset
                        )
                        if (1 <= attack_pos.rank <= 8 and 
                            1 <= attack_pos.file <= 8 and
                            attack_pos == pos):
                            return True
                            
                elif piece.type == PieceType.KNIGHT:
                    # Knights have fixed attack pattern
                    for dr, df in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                  (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        attack_pos = Position(
                            piece.position.rank + dr,
                            piece.position.file + df
                        )
                        if (1 <= attack_pos.rank <= 8 and 
                            1 <= attack_pos.file <= 8 and
                            attack_pos == pos):
                            return True
                            
                elif piece.type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
                    # These pieces attack along lines
                    directions = []
                    if piece.type in [PieceType.BISHOP, PieceType.QUEEN]:
                        directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
                    if piece.type in [PieceType.ROOK, PieceType.QUEEN]:
                        directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
                    
                    for dr, df in directions:
                        for distance in range(1, 8):
                            attack_pos = Position(
                                piece.position.rank + dr * distance,
                                piece.position.file + df * distance
                            )
                            # Stop at board edge
                            if not (1 <= attack_pos.rank <= 8 and 1 <= attack_pos.file <= 8):
                                break
                                
                            # Found the target square in this direction
                            if attack_pos == pos:
                                return True
                                
                            # Stop scanning if we hit any piece that isn't the target
                            target = self.get_piece(attack_pos)
                            if target and target.position != pos:
                                break

        return False

    def is_square_attacked(self, pos: Position, color: Color) -> bool:
        """Check if a square is attacked by the opposite color"""
        return self._is_square_attacked_no_castling(pos, color)

    def _get_piece_moves_no_check(self, piece: Piece, include_castling: bool = True, calc_check: bool = True) -> List[Position]:
        """Get possible moves for a piece without checking for check"""
        moves = []
        
        # Log piece being evaluated
        print(f"Getting moves for {piece.type} at {piece.position.to_algebraic()}")

        if piece.type == PieceType.PAWN:
            direction = 1 if piece.color == Color.WHITE else -1
            
            # Forward move
            forward = Position(piece.position.rank + direction, piece.position.file)
            if 1 <= forward.rank <= 8 and not self.get_piece(forward):
                moves.append(forward)
                # Initial double move
                if not piece.has_moved:
                    double_forward = Position(piece.position.rank + 2 * direction, piece.position.file)
                    if 1 <= double_forward.rank <= 8 and not self.get_piece(double_forward):
                        middle_pos = Position(piece.position.rank + direction, piece.position.file)
                        if not self.get_piece(middle_pos):
                            moves.append(double_forward)
            
            # Diagonal captures
            for file_offset in [-1, 1]:
                capture = Position(piece.position.rank + direction, piece.position.file + file_offset)
                if 1 <= capture.rank <= 8 and 1 <= capture.file <= 8:
                    target = self.get_piece(capture)
                    if target and target.color != piece.color:
                        moves.append(capture)

        elif piece.type == PieceType.KNIGHT:
            for dr, df in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                new_pos = Position(
                    piece.position.rank + dr,
                    piece.position.file + df
                )
                if 1 <= new_pos.rank <= 8 and 1 <= new_pos.file <= 8:
                    target = self.get_piece(new_pos)
                    if not target or target.color != piece.color:
                        moves.append(new_pos)

        elif piece.type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
            directions = []
            if piece.type in [PieceType.BISHOP, PieceType.QUEEN]:
                directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            if piece.type in [PieceType.ROOK, PieceType.QUEEN]:
                directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])

            for dr, df in directions:
                # Keep moving in the direction until we hit a piece or the edge of the board
                for distance in range(1, 9):
                    new_pos = Position(
                        piece.position.rank + dr * distance,
                        piece.position.file + df * distance
                    )
                    # Stop if we hit the edge of the board
                    if not (1 <= new_pos.rank <= 8 and 1 <= new_pos.file <= 8):
                        break
                    # Check if there's a piece on this square
                    target = self.get_piece(new_pos)
                    # If we hit a piece:
                    # - Add the square if it's an enemy piece
                    # - Stop searching this direction
                    if target:
                        if target.color != piece.color:
                            moves.append(new_pos)
                        break
                    # No piece on this square, keep searching this direction
                    moves.append(new_pos)

        elif piece.type == PieceType.KING:
            # Normal moves
            for dr, df in [(1, 0), (1, 1), (0, 1), (-1, 1),
                          (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                new_pos = Position(
                    piece.position.rank + dr,
                    piece.position.file + df
                )
                if 1 <= new_pos.rank <= 8 and 1 <= new_pos.file <= 8:
                    target = self.get_piece(new_pos)
                    if not target or target.color != piece.color:
                        moves.append(new_pos)

            # Castling
            if include_castling and not piece.has_moved:
                rank = piece.position.rank
                # Kingside castling
                rook_pos = Position(rank, 8)
                rook = self.get_piece(rook_pos)
                if rook and rook.type == PieceType.ROOK and not rook.has_moved:
                    if not self.get_piece(Position(rank, 6)) and not self.get_piece(Position(rank, 7)):
                        # Verificar xeque e ataques sem recursão
                        if not self._is_square_attacked_no_castling(Position(rank, 5), piece.color) and \
                           not self._is_square_attacked_no_castling(Position(rank, 6), piece.color) and \
                           not self._is_square_attacked_no_castling(Position(rank, 7), piece.color):
                            moves.append(Position(rank, 7))
                
                # Queenside castling
                rook_pos = Position(rank, 1)
                rook = self.get_piece(rook_pos)
                if rook and rook.type == PieceType.ROOK and not rook.has_moved:
                    if not self.get_piece(Position(rank, 2)) and \
                       not self.get_piece(Position(rank, 3)) and \
                       not self.get_piece(Position(rank, 4)):
                        # Verificar xeque e ataques sem recursão
                        if not self._is_square_attacked_no_castling(Position(rank, 5), piece.color) and \
                           not self._is_square_attacked_no_castling(Position(rank, 3), piece.color) and \
                           not self._is_square_attacked_no_castling(Position(rank, 4), piece.color):
                            moves.append(Position(rank, 3))

        return moves

    def _is_valid_pawn_capture(self, piece: Piece, to_pos: Position) -> bool:
        """Check if pawn can capture on given position"""
        target = self.get_piece(to_pos)
        if not target:
            return False
        if target.color == piece.color:
            return False
        return True
    
    def get_valid_moves(self, position: Position) -> List[Position]:
        """Get all valid moves for a piece at the given position."""
        piece = self.get_piece(position)
        if not piece:
            return []

        moves = []
        for move in self._get_piece_moves_no_check(piece):
            # Try move
            old_pos = piece.position
            captured = self.get_piece(move)
            
            # Make temporary move
            piece.position = move
            if captured:
                del self.pieces[move]
            del self.pieces[old_pos]
            self.pieces[move] = piece
            
            # Check if king would be in check
            puts_king_in_check = self.is_in_check(piece.color)
            
            # Revert move
            piece.position = old_pos
            self.pieces[old_pos] = piece
            if captured:
                self.pieces[move] = captured
            else:
                del self.pieces[move]
                
            if not puts_king_in_check:
                moves.append(move)
                
        return moves

    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Move a piece on the board"""
        piece = self.get_piece(from_pos)
        if not piece or piece.color != self.current_turn:
            return False
        
        # Check if move is in valid moves list
        valid_moves = self.get_valid_moves(from_pos)
        if to_pos not in valid_moves:
            return False
        
        # Get captured piece if any
        captured = self.get_piece(to_pos)
        
        # Update piece position
        old_pos = piece.position
        piece.position = to_pos
        if captured:
            del self.pieces[to_pos]
        del self.pieces[from_pos]
        self.pieces[to_pos] = piece
        
        if piece.type == PieceType.KING:
            self.current_turn = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
            return not self.is_in_check(piece.color)

        # Handle castling
        if piece.type == PieceType.KING and abs(from_pos.file - to_pos.file) == 2:
            rank = piece.position.rank
            if to_pos.file == 7:  # Kingside
                rook = self.get_piece(Position(rank, 8))
                if rook:
                    del self.pieces[Position(rank, 8)]
                    rook.position = Position(rank, 6)
                    rook.has_moved = True
                    self.pieces[Position(rank, 6)] = rook
            elif to_pos.file == 3:  # Queenside
                rook = self.get_piece(Position(rank, 1))
                if rook:
                    del self.pieces[Position(rank, 1)]
                    rook.position = Position(rank, 4)
                    rook.has_moved = True
                    self.pieces[Position(rank, 4)] = rook

        # Move is valid, make it permanent
        if captured:
            self.captured_pieces.append(captured)
        piece.has_moved = True
        self.move_history.append((from_pos, to_pos))
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        
        return True
    
    def is_checkmate(self) -> bool:
        """Check if it's checkmate"""
        if not self.is_in_check(self.current_turn):
            return False

        # Test all possible moves to escape check
        for piece in self.pieces.values():
            if piece.color == self.current_turn:
                for move_pos in self._get_piece_moves_no_check(piece):
                    # Try move
                    old_pos = piece.position
                    captured = self.get_piece(move_pos)
                    
                    # Make temporary move
                    piece.position = move_pos
                    if captured:
                        del self.pieces[move_pos]
                    del self.pieces[old_pos]
                    self.pieces[move_pos] = piece
                    
                    # Check if king is still in check
                    still_in_check = self.is_in_check(self.current_turn)
                    
                    # Revert move
                    piece.position = old_pos
                    self.pieces[old_pos] = piece
                    if captured:
                        self.pieces[move_pos] = captured
                    else:
                        del self.pieces[move_pos]
                    
                    if not still_in_check:
                        return False

        return True

    def is_stalemate(self) -> bool:
        """Check if it's a stalemate"""
        if self.is_in_check(self.current_turn):
            return False

        # Check if any piece has valid moves
        for piece in self.pieces.values():
            if piece.color == self.current_turn:
                for move_pos in self._get_piece_moves_no_check(piece):
                    # Try move
                    old_pos = piece.position
                    captured = self.get_piece(move_pos)
                    
                    # Make temporary move
                    piece.position = move_pos
                    if captured:
                        del self.pieces[move_pos]
                    del self.pieces[old_pos]
                    self.pieces[move_pos] = piece
                    
                    # Check if king would be in check
                    valid_move = not self.is_in_check(self.current_turn)
                    
                    # Revert move
                    piece.position = old_pos
                    self.pieces[old_pos] = piece
                    if captured:
                        self.pieces[move_pos] = captured
                    else:
                        del self.pieces[move_pos]
                    
                    if valid_move:
                        return False

        return True
    
    def __str__(self) -> str:
        """Return ASCII representation of the board"""
        output = []
        output.append("  a b c d e f g h")
        output.append("  ---------------")
        for rank in range(8, 0, -1):
            row = f"{rank}|"
            for file in range(1, 9):
                piece = self.get_piece(Position(rank, file))
                if piece:
                    row += piece.symbol() + " "
                else:
                    row += ". "
            output.append(row.rstrip())
        return "\n".join(output)
