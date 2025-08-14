import pytest
from src.core.board.board import Board, Position, PieceType, Color, Piece
from src.ai.evaluation.position_evaluator import AdvancedEvaluator, PositionalFeatures
from typing import Dict, Tuple

@pytest.fixture
def board_factory():
    def _create_board(pieces_dict: Dict[Tuple[int, int], Tuple[PieceType, Color]]):
        board = Board()
        for (rank, file), (piece_type, color) in pieces_dict.items():
            # Converte coordenadas para notação algébrica
            pos = f"{chr(file + ord('a'))}{rank+1}"
            # Cria a peça e define sua posição
            piece = Piece(piece_type, color, pos)
            board.pieces[pos] = piece
        return board
    return _create_board

def test_evaluator_initialization():
    """Testa inicialização do avaliador"""
    evaluator = AdvancedEvaluator()
    assert evaluator.weights['material'] == 1.0
    assert evaluator.weights['center_control'] == 0.3
    assert evaluator.weights['king_safety'] == 0.25
    assert evaluator.weights['pawn_structure'] == 0.15
    assert evaluator.weights['development'] == 0.2

def test_center_control(board_factory):
    """Testa avaliação do controle do centro"""
    evaluator = AdvancedEvaluator()
    
    # Cria tabuleiro com peças controlando o centro
    pieces = {
        (3, 3): (PieceType.KNIGHT, Color.WHITE),  # d4
        (3, 4): (PieceType.BISHOP, Color.WHITE),  # e4
        (7, 7): (PieceType.KING, Color.BLACK),    # h8
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.center_control > 0  # Brancas controlam mais o centro
    
    # Adiciona peça preta controlando o centro
    pieces[(5, 4)] = (PieceType.QUEEN, Color.BLACK)  # e6
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.center_control < features.center_control  # Menos controle do centro

def test_pawn_structure(board_factory):
    """Testa avaliação da estrutura de peões"""
    evaluator = AdvancedEvaluator()
    
    # Peões dobrados (ruim)
    pieces = {
        (1, 3): (PieceType.PAWN, Color.WHITE),  # d2
        (2, 3): (PieceType.PAWN, Color.WHITE),  # d3
        (7, 4): (PieceType.KING, Color.BLACK),  # e8
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.pawn_structure < 0  # Estrutura ruim
    
    # Peões conectados (bom)
    pieces = {
        (1, 3): (PieceType.PAWN, Color.WHITE),  # d2
        (1, 4): (PieceType.PAWN, Color.WHITE),  # e2
        (7, 4): (PieceType.KING, Color.BLACK),  # e8
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.pawn_structure > features.pawn_structure  # Melhor estrutura

def test_king_safety(board_factory):
    """Testa avaliação da segurança do rei"""
    evaluator = AdvancedEvaluator()
    
    # Rei protegido por peões
    pieces = {
        (0, 4): (PieceType.KING, Color.WHITE),   # e1
        (1, 3): (PieceType.PAWN, Color.WHITE),   # d2
        (1, 4): (PieceType.PAWN, Color.WHITE),   # e2
        (1, 5): (PieceType.PAWN, Color.WHITE),   # f2
        (7, 4): (PieceType.KING, Color.BLACK),   # e8
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.king_safety > 0  # Rei bem protegido
    
    # Rei exposto
    pieces = {
        (3, 4): (PieceType.KING, Color.WHITE),   # e4
        (5, 4): (PieceType.QUEEN, Color.BLACK),  # e6
        (7, 4): (PieceType.KING, Color.BLACK),   # e8
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.king_safety < features.king_safety  # Rei menos seguro

def test_piece_coordination(board_factory):
    """Testa avaliação da coordenação das peças"""
    evaluator = AdvancedEvaluator()
    
    # Par de bispos
    pieces = {
        (0, 0): (PieceType.KING, Color.WHITE),   # a1
        (2, 2): (PieceType.BISHOP, Color.WHITE), # c3
        (3, 3): (PieceType.BISHOP, Color.WHITE), # d4
        (7, 7): (PieceType.KING, Color.BLACK),   # h8
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.piece_coordination > 0  # Boa coordenação
    
    # Torres dobradas
    pieces = {
        (0, 0): (PieceType.KING, Color.WHITE),   # a1
        (2, 0): (PieceType.ROOK, Color.WHITE),   # a3
        (4, 0): (PieceType.ROOK, Color.WHITE),   # a5
        (7, 7): (PieceType.KING, Color.BLACK),   # h8
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.piece_coordination > 0  # Boa coordenação

def test_development(board_factory):
    """Testa avaliação do desenvolvimento das peças"""
    evaluator = AdvancedEvaluator()
    
    # Posição inicial
    pieces = {
        (0, 0): (PieceType.ROOK, Color.WHITE),    # a1
        (0, 1): (PieceType.KNIGHT, Color.WHITE),  # b1
        (0, 2): (PieceType.BISHOP, Color.WHITE),  # c1
        (0, 3): (PieceType.QUEEN, Color.WHITE),   # d1
        (7, 7): (PieceType.KING, Color.BLACK),    # h8
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.development == 0  # Nenhuma peça desenvolvida
    
    # Peças desenvolvidas
    pieces = {
        (0, 0): (PieceType.ROOK, Color.WHITE),    # a1
        (2, 2): (PieceType.KNIGHT, Color.WHITE),  # c3
        (3, 3): (PieceType.BISHOP, Color.WHITE),  # d4
        (0, 3): (PieceType.QUEEN, Color.WHITE),   # d1
        (7, 7): (PieceType.KING, Color.BLACK),    # h8
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.development > features.development  # Melhor desenvolvimento

def test_complete_position(board_factory):
    """Testa avaliação de uma posição completa"""
    evaluator = AdvancedEvaluator()
    
    # Posição típica de meio-jogo
    pieces = {
        # Brancas
        (0, 4): (PieceType.KING, Color.WHITE),    # e1
        (1, 3): (PieceType.PAWN, Color.WHITE),    # d2
        (1, 4): (PieceType.PAWN, Color.WHITE),    # e2
        (3, 3): (PieceType.KNIGHT, Color.WHITE),  # d4
        (4, 4): (PieceType.BISHOP, Color.WHITE),  # e5
        
        # Pretas
        (7, 4): (PieceType.KING, Color.BLACK),    # e8
        (6, 3): (PieceType.PAWN, Color.BLACK),    # d7
        (6, 4): (PieceType.PAWN, Color.BLACK),    # e7
        (5, 3): (PieceType.KNIGHT, Color.BLACK),  # d6
        (4, 2): (PieceType.BISHOP, Color.BLACK),  # c5
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    
    # A posição deve estar aproximadamente igual
    assert abs(score) < 0.5
    assert features.material == 0  # Material igual
    assert features.king_safety > 0  # Brancas tem rei mais seguro
    assert features.center_control != 0  # Algum lado controla mais o centro
    assert features.development != 0  # Algum lado está mais desenvolvido
