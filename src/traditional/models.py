# Shims para traditional.models conforme esperado nos testes
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class Color(Enum):
    WHITE = auto()
    BLACK = auto()

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

@dataclass(frozen=True)
class Position:
    rank: int
    file: int

@dataclass
class Piece:
    type: PieceType
    color: Color
    position: Optional[Position] = None

# Ensure imports like `src.traditional.models.models` resolve to this module if needed
import sys as _sys
_sys.modules['src.traditional.models.models'] = _sys.modules[__name__]

