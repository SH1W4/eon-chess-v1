import pytest
from src.core.board.board import Board, Position, PieceType, Color, Piece

@pytest.fixture
def board_factory():
    def _create_board(pieces_dict):
        board = Board()
        for pos, (piece_type, color) in pieces_dict.items():
            piece = Piece(piece_type, color)
            board.pieces[pos] = piece
            piece._position = Position(rank=pos[0], file=pos[1])
        return board
    return _create_board
