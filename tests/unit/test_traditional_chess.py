"""
Testes unitários para o sistema tradicional de xadrez.
"""

import pytest
from traditional.core.board import Board
from traditional.models import Position, Piece, PieceType, Color
from core.interfaces import Move, MoveType

@pytest.mark.asyncio
async def test_board_initialization(board):
    """Testa inicialização do tabuleiro."""
    assert board is not None
    assert len(board.pieces) > 0
    assert board.current_turn == Color.WHITE

@pytest.mark.asyncio
async def test_piece_movement(board):
    """Testa movimento básico de peças."""
    # Movimento de peão
    from_pos = Position(2, 4)  # e2
    to_pos = Position(4, 4)    # e4
    
    move = Move(from_pos, to_pos, MoveType.NORMAL)
    success = await board.make_move(move)
    
    assert success
    assert board.current_turn == Color.BLACK
    assert board.get_piece(to_pos) is not None
    assert board.get_piece(from_pos) is None

@pytest.mark.asyncio
async def test_invalid_moves(board):
    """Testa detecção de movimentos inválidos."""
    # Tentar mover peça inexistente
    from_pos = Position(3, 3)
    to_pos = Position(4, 4)
    
    move = Move(from_pos, to_pos, MoveType.NORMAL)
    success = await board.make_move(move)
    
    assert not success
    assert board.current_turn == Color.WHITE

@pytest.mark.asyncio
async def test_piece_capture(board):
    """Testa captura de peças."""
    # Setup para captura
    piece = Piece(PieceType.PAWN, Color.BLACK, Position(3, 4))
    board.set_piece(Position(3, 4), piece)
    
    # Movimento de captura
    from_pos = Position(2, 3)
    to_pos = Position(3, 4)
    
    move = Move(from_pos, to_pos, MoveType.CAPTURE)
    success = await board.make_move(move)
    
    assert success
    assert len(board.captured_pieces) == 1
    assert board.captured_pieces[0].color == Color.BLACK

@pytest.mark.asyncio
async def test_check_detection(board):
    """Testa detecção de xeque."""
    # Setup para xeque
    queen = Piece(PieceType.QUEEN, Color.WHITE, Position(4, 5))
    board.set_piece(Position(4, 5), queen)
    
    assert board.is_in_check(Color.BLACK)
    assert not board.is_in_check(Color.WHITE)

@pytest.mark.asyncio
async def test_checkmate_detection(board):
    """Testa detecção de xeque-mate."""
    # Setup para xeque-mate
    board.set_piece(Position(7, 5), Piece(PieceType.KING, Color.BLACK, Position(7, 5)))
    board.set_piece(Position(6, 4), Piece(PieceType.QUEEN, Color.WHITE, Position(6, 4)))
    board.set_piece(Position(6, 6), Piece(PieceType.ROOK, Color.WHITE, Position(6, 6)))
    
    assert board.is_checkmate()

@pytest.mark.asyncio
async def test_stalemate_detection(board):
    """Testa detecção de empate."""
    # Setup para empate
    board.pieces.clear()
    board.set_piece(Position(8, 8), Piece(PieceType.KING, Color.BLACK, Position(8, 8)))
    board.set_piece(Position(6, 7), Piece(PieceType.QUEEN, Color.WHITE, Position(6, 7)))
    board.set_piece(Position(7, 6), Piece(PieceType.KING, Color.WHITE, Position(7, 6)))
    
    assert board.is_stalemate()

@pytest.mark.asyncio
async def test_valid_moves_generation(board):
    """Testa geração de movimentos válidos."""
    # Peão inicial
    moves = await board.get_valid_moves(Position(2, 4))
    assert len(moves) == 2  # Movimento simples e duplo
    
    # Cavalo inicial
    moves = await board.get_valid_moves(Position(1, 2))
    assert len(moves) == 2  # f3 e h3

@pytest.mark.asyncio
async def test_special_moves(board):
    """Testa movimentos especiais."""
    # Setup para roque
    board.pieces.clear()
    board.set_piece(Position(1, 5), Piece(PieceType.KING, Color.WHITE, Position(1, 5)))
    board.set_piece(Position(1, 8), Piece(PieceType.ROOK, Color.WHITE, Position(1, 8)))
    
    # Roque
    from_pos = Position(1, 5)
    to_pos = Position(1, 7)
    move = Move(from_pos, to_pos, MoveType.CASTLE)
    
    success = await board.make_move(move)
    assert success
    assert board.get_piece(Position(1, 7)).type == PieceType.KING
    assert board.get_piece(Position(1, 6)).type == PieceType.ROOK

@pytest.mark.asyncio
async def test_move_validation(board):
    """Testa validação completa de movimentos."""
    # Movimento que deixaria próprio rei em xeque
    board.pieces.clear()
    board.set_piece(Position(1, 5), Piece(PieceType.KING, Color.WHITE, Position(1, 5)))
    board.set_piece(Position(2, 5), Piece(PieceType.ROOK, Color.WHITE, Position(2, 5)))
    board.set_piece(Position(8, 5), Piece(PieceType.QUEEN, Color.BLACK, Position(8, 5)))
    
    move = Move(Position(2, 5), Position(2, 1), MoveType.NORMAL)
    success = await board.make_move(move)
    
    assert not success  # Movimento bloqueado pois deixaria rei em xeque
