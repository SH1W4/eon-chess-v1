"""Testes para o sistema quântico de xadrez"""
import pytest
import numpy as np
from src.core.board.board import Position, Piece, PieceType, Color
from src.core.quantum.quantum_field import QuantumField

def test_quantum_field_initialization():
    """Testa inicialização do campo quântico"""
    field = QuantumField()
    assert isinstance(field.white_influence, np.ndarray)
    assert isinstance(field.black_influence, np.ndarray)
    assert field.white_influence.shape == (8, 8)
    assert field.black_influence.shape == (8, 8)
    assert np.all(field.white_influence == 0)
    assert np.all(field.black_influence == 0)

def test_pawn_field():
    """Testa campo de influência do peão"""
    field = QuantumField()
    pawn = Piece(
        type=PieceType.PAWN,
        color=Color.WHITE,
        position=Position(2, 4)  # d2
    )
    
    piece_field = field.calculate_piece_field(pawn)
    
    # Peão branco deve influenciar as casas diagonais à frente
    assert piece_field[2, 2] == 1.0  # d3
    assert piece_field[2, 4] == 1.0  # d3
    
    # Não deve influenciar outras casas
    assert piece_field[1, 3] == 0.0  # d2
    assert piece_field[2, 3] == 0.0  # Movimento frontal não é ataque

def test_knight_field():
    """Testa campo de influência do cavalo"""
    field = QuantumField()
    knight = Piece(
        type=PieceType.KNIGHT,
        color=Color.WHITE,
        position=Position(4, 4)  # d4
    )
    
    piece_field = field.calculate_piece_field(knight)
    
    # Verifica padrão em L
    expected_positions = [
        (2, 3), (2, 5),  # 2 acima, 1 lateral
        (6, 3), (6, 5),  # 2 abaixo, 1 lateral
        (3, 2), (3, 6),  # 1 acima, 2 lateral
        (5, 2), (5, 6)   # 1 abaixo, 2 lateral
    ]
    
    for rank, file in expected_positions:
        assert piece_field[rank-1, file-1] == 1.0

def test_sliding_piece_field():
    """Testa campo de influência de peças deslizantes (bispo, torre, rainha)"""
    field = QuantumField()
    queen = Piece(
        type=PieceType.QUEEN,
        color=Color.WHITE,
        position=Position(4, 4)  # d4
    )
    
    piece_field = field.calculate_piece_field(queen)
    
    # Verifica influência em todas as direções
    # Horizontal
    assert piece_field[3, 0:8].sum() > 3.0  # Rank 4
    # Vertical
    assert piece_field[0:8, 3].sum() > 3.0  # File d
    
    # Influência é constante ao longo da linha de ataque
    influence = 1.0
    
    # Horizontal (direita)
    assert piece_field[3, 4] == influence
    assert piece_field[3, 5] == influence
    
    # Vertical (cima)
    assert piece_field[4, 3] == influence
    assert piece_field[5, 3] == influence
    
    # Diagonal
    assert piece_field[4, 4] == influence
    assert piece_field[5, 5] == influence

def test_check_detection():
    """Testa detecção de xeque usando campo quântico"""
    field = QuantumField()
    
    # Rainha na mesma diagonal do rei
    pieces = {
        Position(1, 5): Piece(PieceType.KING, Color.WHITE, Position(1, 5)),
        Position(8, 5): Piece(PieceType.KING, Color.BLACK, Position(8, 5)),
        Position(5, 2): Piece(PieceType.QUEEN, Color.WHITE, Position(5, 2))
    }
    
    field.update_field(pieces)
    
    # Rainha na diagonal deve dar xeque no rei preto
    assert field.is_in_check(Color.BLACK, Position(8, 5))
    
    # Rei branco não deve estar em xeque
    assert not field.is_in_check(Color.WHITE, Position(1, 5))

def test_piece_mobility():
    """Testa cálculo de mobilidade das peças"""
    field = QuantumField()
    
    # Rainha no centro deve ter mais mobilidade que na borda
    queen_center = Piece(PieceType.QUEEN, Color.WHITE, Position(4, 4))
    queen_corner = Piece(PieceType.QUEEN, Color.WHITE, Position(1, 1))
    
    field.update_field({
        Position(4, 4): queen_center,
        Position(1, 1): queen_corner
    })
    
    center_mobility = field.get_piece_mobility(queen_center)
    corner_mobility = field.get_piece_mobility(queen_corner)
    
    assert center_mobility > corner_mobility

def test_control_score():
    """Testa cálculo de controle do tabuleiro"""
    field = QuantumField()
    
    # Setup com mais peças brancas controlando o centro
    pieces = {
        Position(4, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(4, 4)),
        Position(4, 5): Piece(PieceType.BISHOP, Color.WHITE, Position(4, 5)),
        Position(8, 1): Piece(PieceType.ROOK, Color.BLACK, Position(8, 1))
    }
    
    field.update_field(pieces)
    
    white_control = field.get_control_score(Color.WHITE)
    black_control = field.get_control_score(Color.BLACK)
    
    assert white_control > black_control

def test_move_simulation():
    """Testa simulação de movimentos"""
    field = QuantumField()
    
    initial_pieces = {
        Position(1, 5): Piece(PieceType.KING, Color.WHITE, Position(1, 5)),
        Position(8, 5): Piece(PieceType.KING, Color.BLACK, Position(8, 5)),
        Position(1, 2): Piece(PieceType.QUEEN, Color.WHITE, Position(1, 2))
    }
    
    # Simula movimento da rainha para a diagonal do rei preto
    from_pos = Position(1, 2)
    to_pos = Position(5, 2)
    
    new_field = field.simulate_move(from_pos, to_pos, initial_pieces)
    
    # Após mover a rainha para a diagonal, o rei preto deve estar em xeque
    assert new_field.is_in_check(Color.BLACK, Position(8, 5))
    
    # No campo original, o rei não deve estar em xeque
    field.update_field(initial_pieces)
    assert not field.is_in_check(Color.BLACK, Position(8, 5))
