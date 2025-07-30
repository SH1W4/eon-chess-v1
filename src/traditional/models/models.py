from enum import Enum
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
    """Board position with rank (1-8, bottom to top) and file (1-8, a-h) coordinates"""
    rank: int
    file: int

    def __post_init__(self):
        """Validate coordinates after initialization"""
        if not isinstance(self.rank, int) or not (1 <= self.rank <= 8):
            raise ValueError(f"Invalid rank: {self.rank}. Must be an integer between 1 and 8")
        if not isinstance(self.file, int) or not (1 <= self.file <= 8):
            raise ValueError(f"Invalid file: {self.file}. Must be an integer between 1 and 8")

    def __hash__(self):
        return hash((self.rank, self.file))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.rank == other.rank and self.file == other.file

    def is_valid(self) -> bool:
        """Check if position is valid (within board bounds)"""
        return 1 <= self.rank <= 8 and 1 <= self.file <= 8
    
    def to_algebraic(self) -> str:
        """Convert to algebraic notation (e.g., 'e4')"""
        # Convert file number to letter (1=a, 2=b, etc)
        file_char = chr(ord('a') + self.file - 1)
        return f"{file_char}{self.rank}"

    @classmethod
    def from_algebraic(cls, notation: str) -> 'Position':
        """Create position from algebraic notation (e.g., 'e4')"""
        if not isinstance(notation, str) or len(notation) != 2:
            raise ValueError(f"Invalid algebraic notation: {notation}. Must be in format 'e4'")

        file_char = notation[0].lower()
        if not 'a' <= file_char <= 'h':
            raise ValueError(f"Invalid file: {file_char}. Must be between 'a' and 'h'")

        try:
            rank = int(notation[1])
            if not 1 <= rank <= 8:
                raise ValueError(f"Invalid rank: {rank}. Must be between 1 and 8")
        except ValueError:
            raise ValueError(f"Invalid rank: {notation[1]}. Must be between 1 and 8")

        # Convert file letter to number (a=1, b=2, etc)
        file = ord(file_char) - ord('a') + 1
        return cls(rank=rank, file=file)

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

