"""Testes para o módulo board"""
import pytest
from src.core.board import Board, Position, Color, PieceType, Piece

def test_position_creation():
    """Testa a criação de posições no tabuleiro"""
    pos = Position(rank=1, file=1)
    assert pos.rank == 1
    assert pos.file == 1

def test_position_algebraic_notation():
    """Testa conversão de notação algébrica"""
    pos = Position.from_algebraic('e4')
    assert pos.rank == 4
    assert pos.file == 5
    assert pos.to_algebraic() == 'e4'

def test_piece_creation():
    """Testa a criação de peças"""
    pos = Position(rank=1, file=1)
    piece = Piece(type=PieceType.ROOK, color=Color.WHITE, position=pos)
    assert piece.type == PieceType.ROOK
    assert piece.color == Color.WHITE
    assert piece.position == pos
    assert not piece.has_moved

def test_board_initial_position():
    """Testa a posição inicial do tabuleiro"""
    board = Board()
    
    # Testa peças brancas
    assert board.get_piece(Position(1, 1)).type == PieceType.ROOK
    assert board.get_piece(Position(1, 2)).type == PieceType.KNIGHT
    assert board.get_piece(Position(1, 3)).type == PieceType.BISHOP
    assert board.get_piece(Position(1, 4)).type == PieceType.QUEEN
    assert board.get_piece(Position(1, 5)).type == PieceType.KING
    
    # Testa peões brancos
    for file in range(1, 9):
        piece = board.get_piece(Position(2, file))
        assert piece.type == PieceType.PAWN
        assert piece.color == Color.WHITE

    # Testa peças pretas
    assert board.get_piece(Position(8, 1)).type == PieceType.ROOK
    assert board.get_piece(Position(8, 2)).type == PieceType.KNIGHT
    assert board.get_piece(Position(8, 3)).type == PieceType.BISHOP
    assert board.get_piece(Position(8, 4)).type == PieceType.QUEEN
    assert board.get_piece(Position(8, 5)).type == PieceType.KING
    
    # Testa peões pretos
    for file in range(1, 9):
        piece = board.get_piece(Position(7, file))
        assert piece.type == PieceType.PAWN
        assert piece.color == Color.BLACK

def test_pawn_moves():
    """Testa movimentos válidos do peão"""
    board = Board()
    
    # Movimento simples do peão
    assert board.move_piece(Position(2, 1), Position(3, 1))
    
    # Movimento duplo inicial
    assert board.move_piece(Position(7, 1), Position(5, 1))
    
    # Movimento inválido de 3 casas
    assert not board.move_piece(Position(2, 2), Position(5, 2))
    
    # Movimento inválido para trás
    assert not board.move_piece(Position(3, 1), Position(2, 1))

def test_piece_capture():
    """Testa captura de peças"""
    board = Board()

    # Move peão branco para frente
    assert board.move_piece(Position(2, 1), Position(3, 1)), "Failed to move white pawn"
    print(board)

    # Move peão preto para diagonal
    assert board.move_piece(Position(7, 2), Position(5, 2)), "Failed to move black pawn"
    print(board)
    
    # Captura diagonal
    assert board.move_piece(Position(3, 1), Position(4, 2))
    assert len(board.captured_pieces) == 0  # Não houve captura ainda
    
    # Move peão preto para ser capturado
    board.move_piece(Position(5, 2), Position(4, 2))
    
    # Realiza a captura
    assert board.move_piece(Position(3, 1), Position(4, 2))
    assert len(board.captured_pieces) == 1
    assert board.captured_pieces[0].type == PieceType.PAWN
    assert board.captured_pieces[0].color == Color.BLACK

def test_check_detection():
    """Testa detecção de xeque"""
    board = Board()
    
    # Move peão branco
    board.move_piece(Position(2, 5), Position(3, 5))
    
    # Move peão preto
    board.move_piece(Position(7, 4), Position(5, 4))
    
    # Move rainha branca para xeque
    board.move_piece(Position(1, 4), Position(4, 7))
    
    assert board.is_in_check(Color.BLACK)
    assert not board.is_in_check(Color.WHITE)

def test_checkmate_detection():
    """Testa detecção de xeque-mate (Mate do pastor)"""
    board = Board()
    
    # Movimento do pastor
    board.move_piece(Position(2, 5), Position(3, 5))  # Peão branco
    board.move_piece(Position(7, 5), Position(5, 5))  # Peão preto
    board.move_piece(Position(1, 4), Position(4, 7))  # Rainha branca
    board.move_piece(Position(7, 6), Position(6, 6))  # Peão preto
    board.move_piece(Position(4, 7), Position(7, 4))  # Rainha branca para xeque-mate
    
    assert board.is_checkmate()

def test_stalemate_detection():
    """Testa detecção de afogamento"""
    board = Board()
    
    # Limpa o tabuleiro mantendo apenas reis e uma rainha
    board.pieces.clear()
    board._place_piece(PieceType.KING, Color.WHITE, Position(1, 1))
    board._place_piece(PieceType.KING, Color.BLACK, Position(8, 8))
    board._place_piece(PieceType.QUEEN, Color.WHITE, Position(7, 7))
    
    # Move a rainha para criar afogamento
    board.move_piece(Position(7, 7), Position(6, 7))
    
    assert board.is_stalemate()
