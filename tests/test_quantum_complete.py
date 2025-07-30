"""Testes completos para o sistema de xadrez quântico"""
import pytest
import numpy as np
from src.traditional.models.models import Position, Piece, Color, PieceType
from src.quantum.core.quantum.quantum_enhancements import EnhancedQuantumField, PositionEvaluation

def create_test_position(pieces_config):
    """Cria uma posição de teste a partir de uma configuração"""
    pieces = {}
    for pos, (piece_type, color) in pieces_config.items():
        pieces[Position(*pos)] = Piece(PieceType(piece_type), Color[color], Position(*pos))
    return pieces

def test_pawn_structure_basic():
    """Testa avaliação básica da estrutura de peões"""
    field = EnhancedQuantumField()
    
    # Posição com peões brancos em formação ideal
    pieces = create_test_position({
        (2, 4): ('P', 'WHITE'),  # Peão central
        (2, 3): ('P', 'WHITE'),  # Peão suporte
        (2, 5): ('P', 'WHITE'),  # Peão suporte
        (7, 4): ('P', 'BLACK'),  # Peão preto isolado
    })
    
    field.update_field(pieces)
    white_structure = field.analyze_pawn_structure(Color.WHITE)
    black_structure = field.analyze_pawn_structure(Color.BLACK)
    
    assert white_structure > black_structure
    assert white_structure > 0.5  # Estrutura branca deve ser bem avaliada

def test_pawn_structure_advanced():
    """Testa avaliação avançada da estrutura de peões"""
    field = EnhancedQuantumField()
    
    # Posição com diferentes formações de peões
    pieces = create_test_position({
        (2, 4): ('P', 'WHITE'),  # Peão central branco
        (3, 4): ('P', 'WHITE'),  # Peão dobrado branco
        (2, 6): ('P', 'WHITE'),  # Peão isolado branco
        (7, 3): ('P', 'BLACK'),  # Peão preto
        (6, 4): ('P', 'BLACK'),  # Peão preto avançado
    })
    
    field.update_field(pieces)
    white_structure = field.analyze_pawn_structure(Color.WHITE)
    black_structure = field.analyze_pawn_structure(Color.BLACK)
    
    # Verifica penalidades por peões dobrados e isolados
    assert white_structure < 1.0  # Deve haver penalidade por peões dobrados
    assert black_structure > 0  # Estrutura preta não deve ser péssima

def test_king_safety():
    """Testa avaliação da segurança do rei"""
    field = EnhancedQuantumField()
    
    # Posição com rei branco bem protegido e rei preto exposto
    pieces = create_test_position({
        (1, 5): ('K', 'WHITE'),  # Rei branco
        (2, 4): ('P', 'WHITE'),  # Peão protetor
        (2, 5): ('P', 'WHITE'),  # Peão protetor
        (2, 6): ('P', 'WHITE'),  # Peão protetor
        (1, 4): ('Q', 'WHITE'),  # Dama protetora
        (8, 5): ('K', 'BLACK'),  # Rei preto exposto
    })
    
    field.update_field(pieces)
    white_safety = field.analyze_king_safety(Color.WHITE, Position(1, 5))
    black_safety = field.analyze_king_safety(Color.BLACK, Position(8, 5))
    
    assert white_safety > black_safety
    assert white_safety > 0  # Segurança positiva para rei branco
    assert black_safety < 0  # Segurança negativa para rei preto exposto

def test_position_evaluation():
    """Testa avaliação completa da posição"""
    field = EnhancedQuantumField()
    
    # Posição com vantagem branca clara
    pieces = create_test_position({
        (1, 5): ('K', 'WHITE'),  # Rei branco
        (2, 5): ('P', 'WHITE'),  # Peão protetor
        (1, 4): ('Q', 'WHITE'),  # Dama branca
        (3, 3): ('B', 'WHITE'),  # Bispo branco
        (8, 5): ('K', 'BLACK'),  # Rei preto
        (7, 5): ('P', 'BLACK'),  # Peão preto
    })
    
    field.update_field(pieces)
    evaluation = field.evaluate_position(pieces)
    
    assert isinstance(evaluation, PositionEvaluation)
    assert evaluation.total_score > 0  # Vantagem branca
    assert evaluation.material_score > 0  # Vantagem material branca
    assert evaluation.king_safety_score > 0  # Rei branco mais seguro

def test_position_dynamics():
    """Testa análise da dinâmica da posição"""
    field = EnhancedQuantumField()
    
    # Posição com peças em desenvolvimento
    pieces = create_test_position({
        (1, 5): ('K', 'WHITE'),
        (4, 4): ('P', 'WHITE'),  # Peão central
        (4, 5): ('P', 'WHITE'),  # Peão central
        (3, 3): ('B', 'WHITE'),  # Bispo desenvolvido
        (3, 6): ('N', 'WHITE'),  # Cavalo desenvolvido
        (8, 5): ('K', 'BLACK'),
        (5, 4): ('P', 'BLACK'),
        (7, 6): ('N', 'BLACK'),
    })
    
    field.update_field(pieces)
    dynamics = field.get_position_dynamics(pieces)
    
    assert isinstance(dynamics, dict)
    assert 'center_control' in dynamics
    assert 'piece_coordination' in dynamics
    assert dynamics['center_control'] > 0  # Brancas controlam mais o centro

def test_special_cases():
    """Testa casos especiais e bordas"""
    field = EnhancedQuantumField()
    
    # Posição com casos especiais
    pieces = create_test_position({
        (1, 1): ('K', 'WHITE'),  # Rei no canto
        (1, 2): ('P', 'WHITE'),  # Peão na borda
        (4, 8): ('B', 'WHITE'),  # Bispo na borda direita
        (8, 8): ('K', 'BLACK'),  # Rei preto no canto
        (8, 1): ('R', 'BLACK'),  # Torre na borda
    })
    
    field.update_field(pieces)
    
    # Testa segurança do rei no canto
    white_safety = field.analyze_king_safety(Color.WHITE, Position(1, 1))
    black_safety = field.analyze_king_safety(Color.BLACK, Position(8, 8))
    
    # Reis no canto devem ter avaliações especiais
    assert white_safety != 0
    assert black_safety != 0

def test_quantum_field_influence():
    """Testa cálculos de influência do campo quântico"""
    field = EnhancedQuantumField()
    
    # Posição para testar influência
    pieces = create_test_position({
        (4, 4): ('Q', 'WHITE'),  # Dama central
        (5, 5): ('B', 'BLACK'),  # Bispo preto
    })
    
    field.update_field(pieces)
    
    # Verifica se a influência da dama é maior no centro
    assert np.sum(field.white_influence) > np.sum(field.black_influence)
    assert field.white_influence[3:6, 3:6].mean() > 0.5  # Alta influência central

def test_comprehensive():
    """Teste abrangente com posição complexa"""
    field = EnhancedQuantumField()
    
    # Posição complexa com múltiplos aspectos
    pieces = create_test_position({
        (1, 5): ('K', 'WHITE'),
        (2, 4): ('P', 'WHITE'),
        (2, 5): ('P', 'WHITE'),
        (2, 6): ('P', 'WHITE'),
        (1, 4): ('Q', 'WHITE'),
        (3, 3): ('B', 'WHITE'),
        (3, 6): ('N', 'WHITE'),
        (8, 5): ('K', 'BLACK'),
        (7, 4): ('P', 'BLACK'),
        (7, 5): ('P', 'BLACK'),
        (7, 6): ('P', 'BLACK'),
        (8, 4): ('Q', 'BLACK'),
        (6, 3): ('B', 'BLACK'),
        (6, 6): ('N', 'BLACK'),
    })
    
    field.update_field(pieces)
    evaluation = field.evaluate_position(pieces)
    dynamics = field.get_position_dynamics(pieces)
    
    # Avaliação deve ser equilibrada mas não exatamente igual
    assert abs(evaluation.total_score) < 1.0
    assert 'center_control' in dynamics
    assert 'piece_coordination' in dynamics
    assert 'attacking_potential' in dynamics
    assert 'defensive_solidity' in dynamics

if __name__ == '__main__':
    pytest.main(['-v', __file__])
