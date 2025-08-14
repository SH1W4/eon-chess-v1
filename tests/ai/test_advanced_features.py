import pytest
from src.core.board.board import Board, Position, Piece, Color, PieceType
from src.ai.cache.transposition_table import TranspositionTable, TranspositionEntry
from src.ai.evaluation.position_evaluator import AdvancedEvaluator, PositionalFeatures

def test_transposition_table():
    """Testa a funcionalidade básica da tabela de transposição"""
    table = TranspositionTable(max_size=100)
    board = Board()
    
    # Testa inserção e busca
    table.store(board, depth=3, score=0.5, flag='exact')
    entry = table.lookup(board)
    assert entry is not None
    assert entry.depth == 3
    assert entry.score == 0.5
    assert entry.flag == 'exact'
    
    # Testa limite de tamanho
    for i in range(150):
        board.move_history.append((Position(rank=1, file=1), Position(rank=2, file=2)))
        table.store(board, depth=i, score=float(i), flag='exact')
    assert table.get_size() <= 100
    
    # Testa estatísticas
    table.clear()
    table.store(board, depth=3, score=0.5, flag='exact')
    table.store(board, depth=4, score=0.6, flag='lowerbound')
    stats = table.get_statistics()
    assert stats['total_entries'] == 1
    assert stats['exact_scores'] + stats['lowerbound_scores'] + stats['upperbound_scores'] == 1

def test_advanced_evaluator():
    """Testa o avaliador de posição avançado"""
    evaluator = AdvancedEvaluator()
    board = Board()
    
    # Configuração inicial para teste
    board.pieces = {
        # Peças brancas
        (4, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(rank=4, file=4)),
        (1, 1): Piece(PieceType.KING, Color.WHITE, Position(rank=1, file=1)),
        (2, 2): Piece(PieceType.BISHOP, Color.WHITE, Position(rank=2, file=2)),
        (2, 3): Piece(PieceType.BISHOP, Color.WHITE, Position(rank=2, file=3)),
        (3, 4): Piece(PieceType.PAWN, Color.WHITE, Position(rank=3, file=4)),
        (3, 5): Piece(PieceType.PAWN, Color.WHITE, Position(rank=3, file=5)),
        
        # Peças pretas
        (8, 8): Piece(PieceType.KING, Color.BLACK, Position(rank=8, file=8)),
        (7, 7): Piece(PieceType.PAWN, Color.BLACK, Position(rank=7, file=7)),
        (7, 8): Piece(PieceType.PAWN, Color.BLACK, Position(rank=7, file=8)),
        (6, 6): Piece(PieceType.KNIGHT, Color.BLACK, Position(rank=6, file=6))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia posição para brancas
    score, features = evaluator.evaluate(board, Color.WHITE)
    
    # Testa características individuais
    assert features.center_control > 0  # Brancas controlam mais o centro
    assert features.piece_mobility > 0  # Brancas têm mais mobilidade
    assert features.king_safety < 0  # Rei branco exposto
    assert features.piece_coordination > 0  # Par de bispos
    assert score > 0  # Vantagem geral para brancas

def test_evaluator_pawn_structure():
    """Testa avaliação específica de estrutura de peões"""
    evaluator = AdvancedEvaluator()
    board = Board()
    
    # Configuração com diferentes estruturas de peões
    board.pieces = {
        # Peões dobrados (ruim)
        (2, 4): Piece(PieceType.PAWN, Color.WHITE, Position(rank=2, file=4)),
        (3, 4): Piece(PieceType.PAWN, Color.WHITE, Position(rank=3, file=4)),
        
        # Peão isolado (ruim)
        (4, 1): Piece(PieceType.PAWN, Color.WHITE, Position(rank=4, file=1)),
        
        # Peão passado (bom)
        (6, 6): Piece(PieceType.PAWN, Color.WHITE, Position(rank=6, file=6)),
        
        # Estrutura normal
        (2, 2): Piece(PieceType.PAWN, Color.BLACK, Position(rank=2, file=2)),
        (2, 3): Piece(PieceType.PAWN, Color.BLACK, Position(rank=2, file=3))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia estrutura
    score = evaluator._evaluate_pawn_structure(board, Color.WHITE)
    
    # Score deve ser negativo devido aos peões dobrados e isolado
    assert score < 0

def test_evaluator_king_safety():
    """Testa avaliação específica de segurança do rei"""
    evaluator = AdvancedEvaluator()
    board = Board()
    
    # Rei protegido por peões
    board.pieces = {
        (1, 5): Piece(PieceType.KING, Color.WHITE, Position(rank=1, file=5)),
        (2, 4): Piece(PieceType.PAWN, Color.WHITE, Position(rank=2, file=4)),
        (2, 5): Piece(PieceType.PAWN, Color.WHITE, Position(rank=2, file=5)),
        (2, 6): Piece(PieceType.PAWN, Color.WHITE, Position(rank=2, file=6))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia segurança
    score_protected = evaluator._evaluate_king_safety(board, Color.WHITE)
    
    # Limpa o tabuleiro
    board.pieces.clear()
    board.piece_list.clear()
    
    # Rei exposto
    board.pieces = {
        (4, 5): Piece(PieceType.KING, Color.WHITE, Position(rank=4, file=5)),
        (6, 5): Piece(PieceType.QUEEN, Color.BLACK, Position(rank=6, file=5))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia segurança
    score_exposed = evaluator._evaluate_king_safety(board, Color.WHITE)
    
    # Rei protegido deve ter pontuação melhor
    assert score_protected > score_exposed

def test_evaluator_development():
    """Testa avaliação de desenvolvimento das peças"""
    evaluator = AdvancedEvaluator()
    board = Board()
    
    # Peças na posição inicial
    board.pieces = {
        (1, 1): Piece(PieceType.ROOK, Color.WHITE, Position(rank=1, file=1)),
        (1, 2): Piece(PieceType.KNIGHT, Color.WHITE, Position(rank=1, file=2)),
        (1, 3): Piece(PieceType.BISHOP, Color.WHITE, Position(rank=1, file=3)),
        (1, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(rank=1, file=4))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia desenvolvimento inicial
    score_initial = evaluator._evaluate_development(board, Color.WHITE)
    
    # Peças desenvolvidas
    board.pieces = {
        (1, 1): Piece(PieceType.ROOK, Color.WHITE, Position(rank=1, file=1)),
        (3, 3): Piece(PieceType.KNIGHT, Color.WHITE, Position(rank=3, file=3)),
        (4, 4): Piece(PieceType.BISHOP, Color.WHITE, Position(rank=4, file=4)),
        (1, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(rank=1, file=4))
    }
    board.piece_list = list(board.pieces.values())
    
    # Avalia desenvolvimento após movimentos
    score_developed = evaluator._evaluate_development(board, Color.WHITE)
    
    # Desenvolvimento deve melhorar a pontuação
    assert score_developed > score_initial
