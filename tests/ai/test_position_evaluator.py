import pytest
from typing import Tuple
from src.core.board.board import Board, Position, Move, PieceType, Color, Piece
from src.ai.evaluation.position_evaluator import AdvancedEvaluator

def coord_to_san(pos: Tuple[int, int]) -> str:
    """Convert numeric coordinates to algebraic notation (e.g. (1,1) -> 'a1')"""
    rank, file = pos
    # Return algebraic notation with correct file offset
    return f"{chr(ord('a') + file - 1)}{rank}"

@pytest.fixture
def board_factory():
    """Create a board with given pieces"""
    def _create_board(pieces):
        board = Board()
        board.pieces.clear()
        
        # Convert numeric coords to algebraic notation
        for pos, (piece_type, color) in pieces.items():
            pos_san = coord_to_san(pos)
            board.pieces[pos_san] = Piece(piece_type, color)
            
        return board
    return _create_board

@pytest.fixture
def start_position() -> Board:
    """Create a board in the initial position"""
    board = Board()
    board.setup_initial_position()
    return board

def test_evaluator_initialization():
    """Testa inicialização do avaliador"""
    evaluator = AdvancedEvaluator()
    assert 'pawn_structure' in evaluator.weights
    assert 'king_safety' in evaluator.weights
    assert 'center_control' in evaluator.weights
    assert 'development' in evaluator.weights

def test_center_control_evaluation(board_factory):
    """Testa avaliação do controle do centro"""
    evaluator = AdvancedEvaluator()
    
    # Cria um tabuleiro com peças no centro
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),  # Cavalo branco no centro
        (4, 3): (PieceType.PAWN, Color.WHITE),    # Peão branco no centro
        (7, 7): (PieceType.KING, Color.BLACK),    # Rei preto no canto
    }
    board = board_factory(pieces)
    
    # Avalia a posição
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pelo controle do centro

def test_pawn_structure_evaluation(board_factory):
    """Testa avaliação da estrutura de peões"""
    evaluator = AdvancedEvaluator()
    
    # Cria um tabuleiro com estrutura de peões
    pieces = {
        (2, 4): (PieceType.PAWN, Color.WHITE),  # Peão branco central
        (2, 3): (PieceType.PAWN, Color.WHITE),  # Peão branco protegendo
        (7, 7): (PieceType.KING, Color.BLACK),  # Rei preto
        (6, 4): (PieceType.PAWN, Color.BLACK),  # Peão preto isolado
    }
    board = board_factory(pieces)
    
    # Avalia a posição
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pela melhor estrutura

def test_king_safety_evaluation(board_factory):
    """Testa avaliação da segurança do rei"""
    evaluator = AdvancedEvaluator()
    
    # Cria um tabuleiro com reis em diferentes situações
    pieces = {
        (1, 1): (PieceType.KING, Color.WHITE),  # Rei branco no canto com proteção
        (1, 2): (PieceType.PAWN, Color.WHITE),  # Peão protegendo rei branco
        (4, 4): (PieceType.KING, Color.BLACK),  # Rei preto exposto no centro
    }
    board = board_factory(pieces)
    
    # Avalia a posição
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pela melhor segurança do rei

def test_development_evaluation(board_factory):
    """Testa avaliação do desenvolvimento de peças"""
    evaluator = AdvancedEvaluator()
    
    # Cria um tabuleiro com diferentes níveis de desenvolvimento
    pieces = {
        (1, 1): (PieceType.KING, Color.WHITE),
        (2, 2): (PieceType.KNIGHT, Color.WHITE),  # Cavalo branco desenvolvido
        (2, 5): (PieceType.BISHOP, Color.WHITE),  # Bispo branco desenvolvido
        (8, 8): (PieceType.KING, Color.BLACK),
        (8, 2): (PieceType.KNIGHT, Color.BLACK),  # Cavalo preto não desenvolvido
        (8, 5): (PieceType.BISHOP, Color.BLACK),  # Bispo preto não desenvolvido
    }
    board = board_factory(pieces)
    
    # Avalia a posição
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pelo melhor desenvolvimento

def test_complex_position_evaluation(board_factory):
    """Testa avaliação de posição complexa"""
    evaluator = AdvancedEvaluator()
    
    # Cria um tabuleiro com posição complexa
    pieces = {
        # Posição branca
        (1, 1): (PieceType.KING, Color.WHITE),
        (2, 2): (PieceType.PAWN, Color.WHITE),
        (2, 3): (PieceType.PAWN, Color.WHITE),
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (5, 5): (PieceType.BISHOP, Color.WHITE),
        
        # Posição preta
        (8, 8): (PieceType.KING, Color.BLACK),
        (7, 7): (PieceType.PAWN, Color.BLACK),
        (7, 4): (PieceType.PAWN, Color.BLACK),
        (8, 2): (PieceType.KNIGHT, Color.BLACK),
        (8, 3): (PieceType.BISHOP, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Avalia a posição
    score, _ = evaluator.evaluate(board, Color.WHITE)
    # Não testamos valor específico, apenas que é um número
    assert isinstance(score, (int, float))

def test_isolated_pawns_penalty(board_factory):
    """Testa penalidade para peões isolados"""
    evaluator = AdvancedEvaluator()
    
    # Tabuleiro com peões isolados vs. conectados
    pieces = {
        (2, 1): (PieceType.PAWN, Color.WHITE),  # Peão branco isolado
        (2, 7): (PieceType.PAWN, Color.WHITE),  # Peão branco isolado
        (7, 3): (PieceType.PAWN, Color.BLACK),  # Peões pretos conectados
        (7, 4): (PieceType.PAWN, Color.BLACK),
        (1, 1): (PieceType.KING, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score < 0  # Pretas devem ter vantagem pela melhor estrutura de peões

def test_piece_mobility(board_factory):
    """Testa avaliação da mobilidade das peças"""
    evaluator = AdvancedEvaluator()
    
    # Tabuleiro com diferença na mobilidade das peças
    pieces = {
        (4, 4): (PieceType.BISHOP, Color.WHITE),  # Bispo branco com boa mobilidade
        (1, 1): (PieceType.BISHOP, Color.BLACK),  # Bispo preto bloqueado
        (1, 2): (PieceType.PAWN, Color.BLACK),    # Peão bloqueando bispo preto
        (1, 8): (PieceType.KING, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pela melhor mobilidade

def test_attacking_potential(board_factory):
    """Testa avaliação do potencial de ataque"""
    evaluator = AdvancedEvaluator()
    
    # Tabuleiro com peças atacando posições importantes
    pieces = {
        (3, 7): (PieceType.QUEEN, Color.WHITE),   # Rainha branca atacando
        (3, 4): (PieceType.KNIGHT, Color.WHITE),  # Cavalo branco em boa posição
        (8, 8): (PieceType.KING, Color.BLACK),    # Rei preto exposto
        (1, 1): (PieceType.KING, Color.WHITE),    # Rei branco seguro
    }
    board = board_factory(pieces)
    
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pelo potencial de ataque

def test_endgame_evaluation(board_factory):
    """Testa avaliação de final de jogo"""
    evaluator = AdvancedEvaluator()
    
    # Posição de final de jogo
    pieces = {
        (2, 2): (PieceType.KING, Color.WHITE),
        (2, 4): (PieceType.PAWN, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Avalia posição de final de jogo
    score, _ = evaluator.evaluate(board, Color.WHITE)
    assert score > 0  # Brancas devem ter vantagem pelo peão passado

    """Testa inicialização do avaliador"""
    evaluator = AdvancedEvaluator()
    
    # Verifica pesos padrão
    assert evaluator.weights['material'] == 1.0
    assert evaluator.weights['center_control'] == 0.3
    assert evaluator.weights['mobility'] == 0.2
    assert evaluator.weights['pawn_structure'] == 0.15
    assert evaluator.weights['king_safety'] == 0.25
    
    # Verifica definição das casas centrais
    assert len(evaluator.center_squares) == 4
    assert (3,3) in evaluator.center_squares
    assert (4,4) in evaluator.center_squares

def test_center_control(board_factory):
    """Testa avaliação do controle do centro"""
    evaluator = AdvancedEvaluator()
    
    # Cria tabuleiro com peças controlando o centro
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),  # Cavalo branco no centro
        (3, 3): (PieceType.BISHOP, Color.WHITE),  # Bispo branco no centro
        (7, 7): (PieceType.KING, Color.BLACK),    # Rei preto na ala do rei
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.center_control > 0  # Brancas controlam mais o centro
    
    # Adiciona peça preta controlando o centro
    pieces[(5, 5)] = (PieceType.QUEEN, Color.BLACK)
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.center_control < features.center_control  # Menos controle do centro

def test_pawn_structure(board_factory):
    """Testa avaliação da estrutura de peões"""
    evaluator = AdvancedEvaluator()
    
    # Peões dobrados (ruim)
    pieces = {
        (2, 4): (PieceType.PAWN, Color.WHITE),
        (3, 4): (PieceType.PAWN, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.pawn_structure < 0  # Estrutura ruim
    
    # Peões conectados (bom)
    pieces = {
        (2, 4): (PieceType.PAWN, Color.WHITE),
        (2, 5): (PieceType.PAWN, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.pawn_structure > features.pawn_structure  # Melhor estrutura

def test_king_safety(board_factory):
    """Testa avaliação da segurança do rei"""
    evaluator = AdvancedEvaluator()
    
    # Rei protegido por peões
    pieces = {
        (1, 5): (PieceType.KING, Color.WHITE),
        (2, 4): (PieceType.PAWN, Color.WHITE),
        (2, 5): (PieceType.PAWN, Color.WHITE),
        (2, 6): (PieceType.PAWN, Color.WHITE),
        (8, 5): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.king_safety > 0  # Rei bem protegido
    
    # Rei exposto
    pieces = {
        (4, 5): (PieceType.KING, Color.WHITE),
        (6, 5): (PieceType.QUEEN, Color.BLACK),
        (8, 5): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.king_safety < features.king_safety  # Rei menos seguro

def test_piece_coordination(board_factory):
    """Testa avaliação da coordenação das peças"""
    evaluator = AdvancedEvaluator()
    
    # Par de bispos
    pieces = {
        (1, 1): (PieceType.KING, Color.WHITE),
        (3, 3): (PieceType.BISHOP, Color.WHITE),
        (4, 4): (PieceType.BISHOP, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.piece_coordination > 0  # Boa coordenação
    
    # Torres dobradas
    pieces = {
        (1, 1): (PieceType.KING, Color.WHITE),
        (3, 1): (PieceType.ROOK, Color.WHITE),
        (5, 1): (PieceType.ROOK, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.piece_coordination > 0  # Boa coordenação

def test_development(board_factory):
    """Testa avaliação do desenvolvimento das peças"""
    evaluator = AdvancedEvaluator()
    
    # Posição inicial
    pieces = {
        (1, 1): (PieceType.ROOK, Color.WHITE),
        (1, 2): (PieceType.KNIGHT, Color.WHITE),
        (1, 3): (PieceType.BISHOP, Color.WHITE),
        (1, 4): (PieceType.QUEEN, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score, features = evaluator.evaluate(board, Color.WHITE)
    assert features.development == 0  # Nenhuma peça desenvolvida
    
    # Peças desenvolvidas
    pieces = {
        (1, 1): (PieceType.ROOK, Color.WHITE),
        (3, 3): (PieceType.KNIGHT, Color.WHITE),
        (4, 4): (PieceType.BISHOP, Color.WHITE),
        (1, 4): (PieceType.QUEEN, Color.WHITE),
        (8, 8): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    assert features2.development > features.development  # Melhor desenvolvimento

def test_complete_evaluation(start_position):
    """Testa avaliação completa em posição real"""
    evaluator = AdvancedEvaluator()
    
    # Avalia posição inicial
    score, features = evaluator.evaluate(start_position, Color.WHITE)
    
    # Posição inicial deve ser equilibrada
    assert abs(score) < 0.1
    assert features.center_control == 0
    assert features.development == 0
    assert features.king_safety > 0
    
    # Simula alguns movimentos
    board = start_position
    
    # 1. e4
    board.make_move(Move(
        Position(rank=2, file=4),
        Position(rank=4, file=4),
        board.get_piece(Position(rank=2, file=4))
    ))
    
    # 1...e5
    board.make_move(Move(
        Position(rank=7, file=4),
        Position(rank=5, file=4),
        board.get_piece(Position(rank=7, file=4))
    ))
    
    # Avalia nova posição
    score2, features2 = evaluator.evaluate(board, Color.WHITE)
    
    # Posição deve continuar equilibrada
    assert abs(score2) < 0.1
    assert features2.center_control != 0  # Agora há luta pelo centro
    assert features2.development > 0  # Peças foram desenvolvidas
