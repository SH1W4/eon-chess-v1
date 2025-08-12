"""Chess board implementation"""
# Prefer shim if available
try:
    from src.traditional.models import Position, Color, PieceType, Piece
except Exception:
    from src.traditional.models.models import Position, Color, PieceType, Piece
from .board import Board
