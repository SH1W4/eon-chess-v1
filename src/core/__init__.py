"""Core module for chess game"""

# Prefer built-in shims for tests; fallback to traditional models if available
try:
    from src.traditional.models import Position, Color, PieceType, Piece  # our shim
except Exception:
    from src.traditional.models.models import Position, Color, PieceType, Piece
from src.traditional.core.board.board import Board

__all__ = ["Board", "Position", "Color", "PieceType", "Piece"]
