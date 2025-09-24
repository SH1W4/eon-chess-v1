"""
Módulo de IA do xadrez.
"""

from .evaluation import (
    evaluate_position,
    evaluate_material,
    evaluate_mobility,
    evaluate_pawn_structure,
    evaluate_king_safety
)
from .cache import (
    PositionCache,
    OpeningBookCache,
    EndgameTablebaseCache
)

__all__ = [
    'evaluate_position',
    'evaluate_material',
    'evaluate_mobility',
    'evaluate_pawn_structure',
    'evaluate_king_safety',
    'PositionCache',
    'OpeningBookCache',
    'EndgameTablebaseCache'
]
