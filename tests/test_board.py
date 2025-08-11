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
    
    # Move peão branco e2->e4
    board.move_piece("e2", "e4")
    
    # Move peão preto f7->f6
    board.move_piece("f7", "f6")
    
    # Move rainha branca para dar xeque (d1->h5)
    board.move_piece("d1", "h5")
    
    # Agora a rainha branca em h5 dá xeque no rei preto em e8
    assert board.is_in_check(Color.BLACK)
    assert not board.is_in_check(Color.WHITE)

def test_checkmate_detection():
    """Testa detecção de xeque-mate (Mate do tolo)"""
    board = Board()
    
    # Mate do tolo (Scholar's mate)
    board.move_piece("f2", "f3")  # Peão branco f2-f3
    board.move_piece("e7", "e5")  # Peão preto e7-e5
    board.move_piece("g2", "g4")  # Peão branco g2-g4
    board.move_piece("d8", "h4")  # Rainha preta dá xeque-mate
    
    # Agora deve ser xeque-mate para as brancas
    assert board.is_in_check(Color.WHITE)
    assert board.is_checkmate()

def test_castling():
    """Testa roque (castling)"""
    board = Board()
    
    # Prepara roque pequeno das brancas
    board.move_piece("e2", "e4")
    board.move_piece("e7", "e5")
    board.move_piece("g1", "f3")
    board.move_piece("b8", "c6")
    board.move_piece("f1", "c4")
    board.move_piece("g8", "f6")
    
    # Executa roque pequeno (O-O)
    result = board.castle_kingside(Color.WHITE)
    assert result.get('success', False), "Roque pequeno deveria ser permitido"
    
    # Verifica posições após roque
    king = board.get_piece_at("g1")
    rook = board.get_piece_at("f1")
    assert king and king.type == PieceType.KING
    assert rook and rook.type == PieceType.ROOK

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
