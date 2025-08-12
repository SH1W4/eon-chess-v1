"""Core module for chess game

Exports the core board and model classes without importing the traditional adapter
to avoid circular imports during test collection.
"""

from src.core.board.board import Board, Position, Color, PieceType, Piece

__all__ = ["Board", "Position", "Color", "PieceType", "Piece"]
