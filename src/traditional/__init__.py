"""
Traditional chess components package.
"""

from .movements import (
    get_pawn_moves,
    get_rook_moves,
    get_knight_moves,
    get_bishop_moves,
    get_queen_moves,
    get_king_moves,
    get_all_possible_moves
)
from .rules import (
    is_check,
    is_checkmate,
    is_stalemate,
    is_insufficient_material,
    get_legal_moves
)

__all__ = [
    'get_pawn_moves',
    'get_rook_moves',
    'get_knight_moves',
    'get_bishop_moves',
    'get_queen_moves',
    'get_king_moves',
    'get_all_possible_moves',
    'is_check',
    'is_checkmate',
    'is_stalemate',
    'is_insufficient_material',
    'get_legal_moves'
]
