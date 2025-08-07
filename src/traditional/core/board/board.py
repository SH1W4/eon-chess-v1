"""Chess board implementation"""
from typing import Dict, List, Optional, Tuple
from src.quantum.core.quantum.quantum_field import QuantumField
from src.traditional.models.models import Position, Color, PieceType, Piece

class Board:
    """Chess board implementation"""
    
    def __init__(self):
        self.pieces: Dict[Position, Piece] = {}
        self.captured_pieces: List[Piece] = []
        self.move_history: List[Tuple[Position, Position]] = []
        self.current_turn = Color.WHITE
        self.quantum_field = QuantumField()
        self._setup_initial_position()
        self.quantum_field.update_field(self.pieces)
    
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
        
    def _is_diagonal_move(self, from_pos: Position, to_pos: Position) -> bool:
        """Verifica se um movimento é diagonal"""
        dx = abs(to_pos.file - from_pos.file)
        dy = abs(to_pos.rank - from_pos.rank)
        return dx == dy
    
    def is_in_check(self, color: Color) -> bool:
        """Check if the king is in check"""
        # Find king position
        king_pos = None
        for pos, piece in self.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = pos
                break

        if not king_pos:
            print(f"King not found for {color}")
            return False

        # Check for attacks from enemy pieces
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        for pos, piece in self.pieces.items():
            if piece.color == enemy_color:
                moves = self._get_piece_moves_no_check(piece, include_castling=False)
                if king_pos in moves:
                    return True
        return False
    
    def _is_square_attacked_no_castling(self, pos: Position, color: Color) -> bool:
        """Check if a square is attacked by the opposite color (without considering castling)"""
        return self.quantum_field.is_square_attacked(pos, color)

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
            start_rank = 2 if piece.color == Color.WHITE else 7
            
            # Forward move
            try:
                forward = Position(piece.position.rank + direction, piece.position.file)
                if forward.is_valid() and not self.get_piece(forward):
                    moves.append(forward)
                    # Initial double move
                    if piece.position.rank == start_rank:
                        double_forward = Position(piece.position.rank + 2 * direction, piece.position.file)
                        if double_forward.is_valid() and not self.get_piece(double_forward):
                            moves.append(double_forward)
            except ValueError:
                pass
            
            # Diagonal captures
            for file_offset in [-1, 1]:
                try:
                    capture = Position(piece.position.rank + direction, piece.position.file + file_offset)
                    if capture.is_valid():
                        target = self.get_piece(capture)
                        # Adiciona o movimento se houver uma peça inimiga para capturar
                        if target is not None and target.color != piece.color:
                            moves.append(capture)
                            print(f"Valid pawn capture found at {capture.to_algebraic()}")
                except ValueError:
                    continue

        elif piece.type == PieceType.KNIGHT:
            for dr, df in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                try:
                    new_pos = Position(
                        piece.position.rank + dr,
                        piece.position.file + df
                    )
                    target = self.get_piece(new_pos)
                    if not target or target.color != piece.color:
                        moves.append(new_pos)
                except ValueError:
                    continue

        elif piece.type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
            directions = []
            if piece.type in [PieceType.QUEEN, PieceType.BISHOP]:
                directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            if piece.type in [PieceType.QUEEN, PieceType.ROOK]:
                directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])

            for dr, df in directions:
                for distance in range(1, 9):  # Mudando para 9 para cobrir todo o tabuleiro
                    try:
                        new_rank = piece.position.rank + dr * distance
                        new_file = piece.position.file + df * distance
                        new_pos = Position(new_rank, new_file)
                        
                        # Print debug info
                        dx = new_file - piece.position.file
                        dy = new_rank - piece.position.rank

# Check if there is a piece on the new position
                        target = self.get_piece(new_pos)
                        
                        # Print debug info
                        dx = new_pos.file - piece.position.file
                        dy = new_pos.rank - piece.position.rank
                        print(f"Calculando coordenadas: {piece.position.to_algebraic()} -> {new_pos.to_algebraic()}")
                        print(f"Arquivo: {piece.position.file}->{new_pos.file} ({df})")
                        print(f"Rank: {piece.position.rank}->{new_pos.rank} ({dr})")
                        print(f"Diferenças dx={dx}, dy={dy}, abs_dx={abs(dx)}, abs_dy={abs(dy)}")
                        
                        # Verifica se é um movimento diagonal ou reto válido
                        # Para movimento diagonal, as diferenças absolutas em x e y devem ser iguais
                        is_diagonal = abs(dx) == abs(dy)
                        is_straight = dx == 0 or dy == 0
                        print(f"Rainha movendo de {piece.position.to_algebraic()} para {new_pos.to_algebraic()} -> diagonal? {is_diagonal}, straight? {is_straight}")
                        
                        # Adiciona o movimento se for válido
                        # Bispo pode mover apenas diagonalmente
                        # Torre pode mover apenas em linha reta
                        # Rainha pode mover tanto diagonalmente quanto em linha reta
                        if ((piece.type == PieceType.BISHOP and is_diagonal) or 
                            (piece.type == PieceType.ROOK and is_straight) or 
                            (piece.type == PieceType.QUEEN and (is_diagonal or is_straight))):
                            if target:
                                if target.color != piece.color:
                                    moves.append(new_pos)  # Captura possível
                                break  # Para a direção se encontrou uma peça
                            else:
                                moves.append(new_pos)  # Casa vazia, movimento válido
                    except ValueError:
                        break
                    except ValueError:
                        # Posição fora do tabuleiro
                        break

        elif piece.type == PieceType.KING:
            # Normal moves
            for dr, df in [(1, 0), (1, 1), (0, 1), (-1, 1),
                          (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                try:
                    new_pos = Position(
                        piece.position.rank + dr,
                        piece.position.file + df
                    )
                    target = self.get_piece(new_pos)
                    if not target or target.color != piece.color:
                        moves.append(new_pos)
                except ValueError:
                    continue

            # Castling
            if include_castling and not piece.has_moved:
                rank = piece.position.rank
                # Kingside castling
                try:
                    rook_pos = Position(rank, 8)
                    rook = self.get_piece(rook_pos)
                    if rook and rook.type == PieceType.ROOK and not rook.has_moved:
                        if not self.get_piece(Position(rank, 6)) and not self.get_piece(Position(rank, 7)):
                            # Check for check and attacks without recursion
                            if not self._is_square_attacked_no_castling(Position(rank, 5), piece.color) and \
                               not self._is_square_attacked_no_castling(Position(rank, 6), piece.color) and \
                               not self._is_square_attacked_no_castling(Position(rank, 7), piece.color):
                                moves.append(Position(rank, 7))
                except ValueError:
                    pass
                
                # Queenside castling
                try:
                    rook_pos = Position(rank, 1)
                    rook = self.get_piece(rook_pos)
                    if rook and rook.type == PieceType.ROOK and not rook.has_moved:
                        if not self.get_piece(Position(rank, 2)) and \
                           not self.get_piece(Position(rank, 3)) and \
                           not self.get_piece(Position(rank, 4)):
                            # Check for check and attacks without recursion
                            if not self._is_square_attacked_no_castling(Position(rank, 5), piece.color) and \
                               not self._is_square_attacked_no_castling(Position(rank, 3), piece.color) and \
                               not self._is_square_attacked_no_castling(Position(rank, 4), piece.color):
                                moves.append(Position(rank, 3))
                except ValueError:
                    pass

        return moves

    def _is_valid_pawn_capture(self, piece: Piece, to_pos: Position) -> bool:
        """Check if pawn can capture on given position"""
        target = self.get_piece(to_pos)
        if not target:
            return False
        if target.color == piece.color:
            return False
            
        # Verify diagonal capture
        file_diff = abs(piece.position.file - to_pos.file)
        rank_diff = to_pos.rank - piece.position.rank
        direction = 1 if piece.color == Color.WHITE else -1
        
        return file_diff == 1 and rank_diff == direction
    
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
            original_pieces = self.pieces.copy()
            
            # Make temporary move
            piece.position = move
            self.pieces = original_pieces.copy()
            if captured:
                del self.pieces[move]
            del self.pieces[old_pos]
            self.pieces[move] = piece
            
            # Update quantum field with temporary move
            self.quantum_field.update_field(self.pieces)
            
            # Check if king would be in check
            puts_king_in_check = self.is_in_check(piece.color)
            
            # Revert move and field
            piece.position = old_pos
            self.pieces = original_pieces
            self.quantum_field.update_field(self.pieces)
            
            if not puts_king_in_check:
                moves.append(move)
                
        return moves

    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Move a piece on the board"""
        # Get the piece at the source position
        piece = self.get_piece(from_pos)
        if not piece:
            return False
        
        # Verify it's the correct turn
        if piece.color != self.current_turn:
            return False
        
        # Get valid moves for the piece
        valid_moves = self.get_valid_moves(from_pos)
        if to_pos not in valid_moves:
            return False
        
        # Execute the move
        captured_piece = self.get_piece(to_pos)
        if captured_piece:
            self.captured_pieces.append(captured_piece)
        
        # Update piece position and status
        piece.position = to_pos
        piece.has_moved = True
        
        # Update board state
        del self.pieces[from_pos]
        self.pieces[to_pos] = piece
        
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
            else:  # Queenside
                rook = self.get_piece(Position(rank, 1))
                if rook:
                    del self.pieces[Position(rank, 1)]
                    rook.position = Position(rank, 4)
                    rook.has_moved = True
                    self.pieces[Position(rank, 4)] = rook

        # Record move and switch turns
        self.move_history.append((from_pos, to_pos))
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        
        # Update quantum field
        self.quantum_field.update_field(self.pieces)
        
        return True

    def _can_castle_kingside(self, king: Piece, to_pos: Position) -> bool:
        """Check if kingside castling is valid."""
        if king.has_moved or self.is_in_check(king.color):
            return False
            
        rank = king.position.rank
        rook_pos = Position(rank, 8)
        rook = self.get_piece(rook_pos)
        if not rook or rook.type != PieceType.ROOK or rook.has_moved:
            return False
            
        # Path must be clear
        if self.get_piece(Position(rank, 6)) or self.get_piece(Position(rank, 7)):
            return False
            
        # Path must not be under attack
        enemy_color = Color.BLACK if king.color == Color.WHITE else Color.WHITE
        if (self.is_square_attacked(Position(rank, 5), enemy_color) or
            self.is_square_attacked(Position(rank, 6), enemy_color) or
            self.is_square_attacked(Position(rank, 7), enemy_color)):
            return False
            
        return True

    def _can_castle_queenside(self, king: Piece, to_pos: Position) -> bool:
        """Check if queenside castling is valid."""
        if king.has_moved or self.is_in_check(king.color):
            return False
            
        rank = king.position.rank
        rook_pos = Position(rank, 1)
        rook = self.get_piece(rook_pos)
        if not rook or rook.type != PieceType.ROOK or rook.has_moved:
            return False
            
        # Path must be clear
        if (self.get_piece(Position(rank, 2)) or
            self.get_piece(Position(rank, 3)) or
            self.get_piece(Position(rank, 4))):
            return False
            
        # Path must not be under attack
        enemy_color = Color.BLACK if king.color == Color.WHITE else Color.WHITE
        if (self.is_square_attacked(Position(rank, 3), enemy_color) or
            self.is_square_attacked(Position(rank, 4), enemy_color)):
            return False
            
        return True
    
    def is_checkmate(self) -> bool:
        """Check if it's checkmate"""
        color = self.current_turn

        # Must be in check first
        if not self.is_in_check(color):
            return False

        # Try every possible move to get out of check
        for pos, piece in self.pieces.items():
            if piece.color == color:
                for move_pos in self._get_piece_moves_no_check(piece):
                    # Try the move
                    old_pos = piece.position
                    captured = self.get_piece(move_pos)
                    original_pieces = self.pieces.copy()
                    
                    # Make temporary move
                    piece.position = move_pos
                    self.pieces = original_pieces.copy()
                    if captured:
                        del self.pieces[move_pos]
                    del self.pieces[old_pos]
                    self.pieces[move_pos] = piece
                    
                    # Check if still in check
                    still_in_check = self.is_in_check(color)
                    
                    # Revert move
                    piece.position = old_pos
                    self.pieces = original_pieces
                    
                    if not still_in_check:
                        return False
        
        return True

    def is_stalemate(self) -> bool:
        """Check if it's a stalemate"""
        if self.is_in_check(self.current_turn):
            return False

        # Check if any piece has valid moves
        for pos, piece in list(self.pieces.items()):
            if piece.color == self.current_turn:
                if self.get_valid_moves(pos):
                    return False

        return True
    
    def get_pieces(self, color: Color) -> List[Piece]:
        """Get all pieces of a specific color"""
        return [piece for piece in self.pieces.values() if piece.color == color]
    
    def get_all_pieces(self) -> List[Piece]:
        """Get all pieces on the board"""
        return list(self.pieces.values())
    
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
