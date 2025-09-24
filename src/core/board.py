"""
Implementação do tabuleiro de xadrez.
"""

from enum import Enum
from typing import List, Optional, Tuple

class PieceType(Enum):
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"
    EMPTY = "."

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color

    def __str__(self) -> str:
        return self.type.value if self.color == Color.WHITE else self.type.value.lower()

class Board:
    def __init__(self):
        self.squares: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        
    def initialize_board(self):
        """Inicializa o tabuleiro com as peças em suas posições padrão."""
        # Configura peças brancas
        self._setup_pieces(Color.WHITE, 7, 6)
        # Configura peças pretas
        self._setup_pieces(Color.BLACK, 0, 1)

    def _setup_pieces(self, color: Color, back_rank: int, pawn_rank: int):
        """Configura as peças para uma cor específica."""
        # Configura peões
        for file in range(8):
            self.squares[pawn_rank][file] = Piece(PieceType.PAWN, color)

        # Configura peças principais
        piece_types = [
            PieceType.ROOK,
            PieceType.KNIGHT,
            PieceType.BISHOP,
            PieceType.QUEEN,
            PieceType.KING,
            PieceType.BISHOP,
            PieceType.KNIGHT,
            PieceType.ROOK
        ]
        
        for file, piece_type in enumerate(piece_types):
            self.squares[back_rank][file] = Piece(piece_type, color)

    def is_valid_position(self, row: int, col: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro."""
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Retorna a peça em uma posição específica."""
        if not self.is_valid_position(row, col):
            return None
        return self.squares[row][col]

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Move uma peça de uma posição para outra.
        Retorna True se o movimento foi bem-sucedido, False caso contrário.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        if not (self.is_valid_position(from_row, from_col) and 
                self.is_valid_position(to_row, to_col)):
            return False

        piece = self.squares[from_row][from_col]
        if piece is None:
            return False

        # Realiza o movimento
        self.squares[to_row][to_col] = piece
        self.squares[from_row][from_col] = None
        return True

    def __str__(self) -> str:
        """Retorna uma representação string do tabuleiro."""
        board_str = []
        for row in self.squares:
            row_str = []
            for piece in row:
                if piece is None:
                    row_str.append(".")
                else:
                    row_str.append(str(piece))
            board_str.append(" ".join(row_str))
        return "\n".join(board_str)
