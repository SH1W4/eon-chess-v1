"""Testes para o núcleo do jogo de xadrez"""
import pytest
from src.core.board import Board, Position, Color, PieceType, Piece

def test_board_initialization():
    """Testa inicialização do tabuleiro"""
    board = Board()
    
    # Verifica peças brancas
    assert board.get_piece(Position(1, 1)).type == PieceType.ROOK
    assert board.get_piece(Position(1, 2)).type == PieceType.KNIGHT
    assert board.get_piece(Position(1, 3)).type == PieceType.BISHOP
    assert board.get_piece(Position(1, 4)).type == PieceType.QUEEN
    assert board.get_piece(Position(1, 5)).type == PieceType.KING
    assert board.get_piece(Position(1, 6)).type == PieceType.BISHOP
    assert board.get_piece(Position(1, 7)).type == PieceType.KNIGHT
    assert board.get_piece(Position(1, 8)).type == PieceType.ROOK
    
    # Verifica peões brancos
    for file in range(1, 9):
        assert board.get_piece(Position(2, file)).type == PieceType.PAWN
        assert board.get_piece(Position(2, file)).color == Color.WHITE
    
    # Verifica peças pretas
    assert board.get_piece(Position(8, 1)).type == PieceType.ROOK
    assert board.get_piece(Position(8, 2)).type == PieceType.KNIGHT
    assert board.get_piece(Position(8, 3)).type == PieceType.BISHOP
    assert board.get_piece(Position(8, 4)).type == PieceType.QUEEN
    assert board.get_piece(Position(8, 5)).type == PieceType.KING
    assert board.get_piece(Position(8, 6)).type == PieceType.BISHOP
    assert board.get_piece(Position(8, 7)).type == PieceType.KNIGHT
    assert board.get_piece(Position(8, 8)).type == PieceType.ROOK
    
    # Verifica peões pretos
    for file in range(1, 9):
        assert board.get_piece(Position(7, file)).type == PieceType.PAWN
        assert board.get_piece(Position(7, file)).color == Color.BLACK

def test_position_algebraic():
    """Testa conversão de notação algébrica"""
    # De algébrica para Position
    pos = Position.from_algebraic("e4")
    assert pos.rank == 4
    assert pos.file == 5
    
    pos = Position.from_algebraic("a1")
    assert pos.rank == 1
    assert pos.file == 1
    
    pos = Position.from_algebraic("h8")
    assert pos.rank == 8
    assert pos.file == 8
    
    # De Position para algébrica
    assert Position(4, 5).to_algebraic() == "e4"
    assert Position(1, 1).to_algebraic() == "a1"
    assert Position(8, 8).to_algebraic() == "h8"

def test_piece_movement():
    """Testa movimento básico de peças"""
    board = Board()
    
    # Move peão branco
    assert board.move_piece(
        Position.from_algebraic("e2"),
        Position.from_algebraic("e4")
    )
    assert board.get_piece(Position.from_algebraic("e4")).type == PieceType.PAWN
    assert board.get_piece(Position.from_algebraic("e4")).color == Color.WHITE
    
    # Verifica troca de turno
    assert board.current_turn == Color.BLACK
    
    # Move peão preto
    assert board.move_piece(
        Position.from_algebraic("e7"),
        Position.from_algebraic("e5")
    )
    assert board.get_piece(Position.from_algebraic("e5")).type == PieceType.PAWN
    assert board.get_piece(Position.from_algebraic("e5")).color == Color.BLACK
    
    # Verifica histórico de movimentos
    assert len(board.move_history) == 2

def test_invalid_moves():
    """Testa movimentos inválidos"""
    board = Board()
    
    # Tenta mover peça errada no turno
    assert not board.move_piece(
        Position.from_algebraic("e7"),  # Peça preta
        Position.from_algebraic("e5")
    )
    
    # Tenta mover de casa vazia
    assert not board.move_piece(
        Position.from_algebraic("e4"),
        Position.from_algebraic("e5")
    )
    
    # Movimento válido não deve afetar estado do jogo
    assert board.current_turn == Color.WHITE
    assert len(board.move_history) == 0

def test_piece_capture():
    """Testa captura de peças"""
    board = Board()
    
    # Move peão branco para perto do preto
    board.move_piece(
        Position.from_algebraic("e2"),
        Position.from_algebraic("e4")
    )
    board.move_piece(
        Position.from_algebraic("d7"),
        Position.from_algebraic("d5")
    )
    
    # Captura
    assert board.move_piece(
        Position.from_algebraic("e4"),
        Position.from_algebraic("d5")
    )
    
    # Verifica captura
    assert len(board.captured_pieces) == 1
    assert board.captured_pieces[0].type == PieceType.PAWN
    assert board.captured_pieces[0].color == Color.BLACK
    
    # Verifica nova posição
    piece = board.get_piece(Position.from_algebraic("d5"))
    assert piece.type == PieceType.PAWN
    assert piece.color == Color.WHITE

def test_check_detection():
    """Testa detecção de xeque"""
    board = Board()
    
    # Mate do pastor (sem o mate)
    print("Move White Pawn: e2 to e4")
    board.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
    print("Move Black Pawn: e7 to e5")
    board.move_piece(Position.from_algebraic("e7"), Position.from_algebraic("e5"))
    print("Move White Queen: d1 to h5")
    board.move_piece(Position.from_algebraic("d1"), Position.from_algebraic("h5"))
    
    # Verifica que não há xeque ainda
    assert not board.is_in_check(Color.BLACK)
    print("Check failed initially as expected")
    
    # Move a dama para dar xeque
    print("Move White Queen: h5 to f7 for Check")
    board.move_piece(Position.from_algebraic("h5"), Position.from_algebraic("f7"))
    
    # Verifica xeque
    assert board.is_in_check(Color.BLACK)
    print("Check passed as expected")
    assert not board.is_in_check(Color.WHITE)

def test_checkmate_detection():
    """Testa detecção de xeque-mate"""
    board = Board()
    
    # Executa o mate do pastor
    board.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
    board.move_piece(Position.from_algebraic("e7"), Position.from_algebraic("e5"))
    board.move_piece(Position.from_algebraic("d1"), Position.from_algebraic("h5"))
    board.move_piece(Position.from_algebraic("f7"), Position.from_algebraic("f6"))
    board.move_piece(Position.from_algebraic("h5"), Position.from_algebraic("f7"))
    
    # Verifica xeque-mate
    assert board.is_in_check(Color.BLACK)
    assert board.is_checkmate()

def test_castling():
    """Testa o roque"""
    board = Board()
    
    # Move peças para liberar caminho do roque pequeno
    board.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
    board.move_piece(Position.from_algebraic("e7"), Position.from_algebraic("e5"))
    board.move_piece(Position.from_algebraic("f1"), Position.from_algebraic("c4"))
    board.move_piece(Position.from_algebraic("d7"), Position.from_algebraic("d6"))
    board.move_piece(Position.from_algebraic("g1"), Position.from_algebraic("f3"))
    
    # Executa roque pequeno
    assert board.move_piece(Position.from_algebraic("e1"), Position.from_algebraic("g1"))
    
    # Verifica posições após o roque
    king = board.get_piece(Position.from_algebraic("g1"))
    rook = board.get_piece(Position.from_algebraic("f1"))
    
    assert king.type == PieceType.KING
    assert rook.type == PieceType.ROOK
    assert king.has_moved
    assert rook.has_moved
