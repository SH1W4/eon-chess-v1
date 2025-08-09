# Package initializer for traditional.models
# Expose common chess model types for legacy imports
from .models import PieceType, Color, Position, Piece

__all__ = [
    'PieceType',
    'Color',
    'Position',
    'Piece',
]
