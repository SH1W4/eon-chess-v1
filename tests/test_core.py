"""Testes para o núcleo do jogo de xadrez"""
import pytest
from src.core.board import Board, Position, Color, PieceType, Piece

def test_board_initialization():
    """Testa inicialização do tabuleiro"""
    board = Board()
    
    # Verifica peças brancas (rank 1)
    assert board.get_piece(Position.from_algebraic("a1")).type == PieceType.ROOK
    assert board.get_piece(Position.from_algebraic("b1")).type == PieceType.KNIGHT
    assert board.get_piece(Position.from_algebraic("c1")).type == PieceType.BISHOP
    assert board.get_piece(Position.from_algebraic("d1")).type == PieceType.QUEEN
    assert board.get_piece(Position.from_algebraic("e1")).type == PieceType.KING
    assert board.get_piece(Position.from_algebraic("f1")).type == PieceType.BISHOP
    assert board.get_piece(Position.from_algebraic("g1")).type == PieceType.KNIGHT
    assert board.get_piece(Position.from_algebraic("h1")).type == PieceType.ROOK
    
    # Verifica peões brancos (rank 2)
    for file in "abcdefgh":
        pos = f"{file}2"
        assert board.get_piece(Position.from_algebraic(pos)).type == PieceType.PAWN
        assert board.get_piece(Position.from_algebraic(pos)).color == Color.WHITE
    
    # Verifica peças pretas (rank 8)
    assert board.get_piece(Position.from_algebraic("a8")).type == PieceType.ROOK
    assert board.get_piece(Position.from_algebraic("b8")).type == PieceType.KNIGHT
    assert board.get_piece(Position.from_algebraic("c8")).type == PieceType.BISHOP
    assert board.get_piece(Position.from_algebraic("d8")).type == PieceType.QUEEN
    assert board.get_piece(Position.from_algebraic("e8")).type == PieceType.KING
    assert board.get_piece(Position.from_algebraic("f8")).type == PieceType.BISHOP
    assert board.get_piece(Position.from_algebraic("g8")).type == PieceType.KNIGHT
    assert board.get_piece(Position.from_algebraic("h8")).type == PieceType.ROOK
    
    # Verifica peões pretos (rank 7)
    for file in "abcdefgh":
        pos = f"{file}7"
        assert board.get_piece(Position.from_algebraic(pos)).type == PieceType.PAWN
        assert board.get_piece(Position.from_algebraic(pos)).color == Color.BLACK

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
    result = board.move_piece("e2", "e4")
    assert result["success"]
    assert board.get_piece(Position.from_algebraic("e4")).type == PieceType.PAWN
    assert board.get_piece(Position.from_algebraic("e4")).color == Color.WHITE
    
    # Verifica troca de turno
    assert board.current_turn == Color.BLACK
    
    # Move peão preto
    result = board.move_piece("e7", "e5")
    assert result["success"]
    assert board.get_piece(Position.from_algebraic("e5")).type == PieceType.PAWN
    assert board.get_piece(Position.from_algebraic("e5")).color == Color.BLACK
    
    # Verifica histórico de movimentos
    assert len(board.move_history) == 2

def test_invalid_moves():
    """Testa movimentos inválidos"""
    board = Board()
    
    # Tenta mover peça errada no turno
    result = board.move_piece("e7", "e5")  # Peça preta
    assert not result["success"]
    
    # Tenta mover de casa vazia
    result = board.move_piece("e4", "e5")
    assert not result["success"]
    
    # Movimento válido não deve afetar estado do jogo
    assert board.current_turn == Color.WHITE
    assert len(board.move_history) == 0

def test_piece_capture():
    """Testa captura de peças"""
    board = Board()
    
    # Move peão branco para perto do preto
    board.move_piece("e2", "e4")
    board.move_piece("d7", "d5")
    
    # Captura
    result = board.move_piece("e4", "d5")
    assert result["success"]
    
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
    board.move_piece("e2", "e4")
    print("Move Black Pawn: e7 to e5")
    board.move_piece("e7", "e5")
    print("Move White Queen: d1 to h5")
    board.move_piece("d1", "h5")
    
    # Verifica que não há xeque ainda
    assert not board.is_in_check(Color.BLACK)
    print("Check failed initially as expected")
    
    # Move a dama para dar xeque
    print("Move White Queen: h5 to f7 for Check")
    board.move_piece("h5", "f7")
    
    # Verifica xeque
    assert board.is_in_check(Color.BLACK)
    print("Check passed as expected")
    assert not board.is_in_check(Color.WHITE)

def test_checkmate_detection():
    """Testa detecção de xeque-mate"""
    board = Board()
    
    # Executa o mate do pastor
    board.move_piece("e2", "e4")
    board.move_piece("e7", "e5")
    board.move_piece("d1", "h5")
    board.move_piece("f7", "f6")
    board.move_piece("h5", "f7")
    
    # Verifica xeque-mate
    assert board.is_in_check(Color.BLACK)
    assert board.is_checkmate()

def test_castling():
    """Testa o roque"""
    board = Board()
    
    # Move peças para liberar caminho do roque pequeno
    board.move_piece("e2", "e4")
    board.move_piece("e7", "e5")
    board.move_piece("f1", "c4")
    board.move_piece("d7", "d6")
    board.move_piece("g1", "f3")
    
    # Executa roque pequeno
    result = board.move_piece("e1", "g1")
    assert result["success"]
    
    # Verifica posições após o roque
    king = board.get_piece(Position.from_algebraic("g1"))
    rook = board.get_piece(Position.from_algebraic("f1"))
    
    assert king.type == PieceType.KING
    assert rook.type == PieceType.ROOK
    assert king.has_moved
    assert rook.has_moved
