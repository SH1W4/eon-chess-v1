import pytest
from src.core.board.board import Board, Position, PieceType, Color, Piece
from src.ai.cache.transposition_table import TranspositionTable, TranspositionEntry

def test_table_initialization():
    """Testa inicialização da tabela"""
    table = TranspositionTable(max_size=1000)
    assert table.max_size == 1000
    assert len(table.table) == 0

def test_store_and_lookup(board_factory):
    """Testa armazenamento e busca de entradas"""
    table = TranspositionTable()
    
    # Cria um tabuleiro simples
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Armazena uma entrada
    table.store(board, depth=3, score=0.5, flag='exact')
    
    # Busca a entrada
    entry = table.lookup(board)
    assert entry is not None
    assert entry.depth == 3
    assert entry.score == 0.5
    assert entry.flag == 'exact'

def test_size_limit(board_factory):
    """Testa limite de tamanho da tabela"""
    table = TranspositionTable(max_size=2)
    
    # Cria três tabuleiros diferentes
    boards = []
    for i in range(3):
        pieces = {
            (i+1, i+1): (PieceType.PAWN, Color.WHITE),
            (7, 7): (PieceType.KING, Color.BLACK),
        }
        board = board_factory(pieces)
        boards.append(board)
        table.store(board, depth=i, score=float(i), flag='exact')
    
    # Verifica que o tamanho não excede o limite
    assert table.get_size() <= 2

def test_entry_flags(board_factory):
    """Testa diferentes flags das entradas"""
    table = TranspositionTable()
    
    # Cria um tabuleiro simples
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Armazena entradas com diferentes flags
    table.store(board, depth=3, score=0.5, flag='exact')
    entry1 = table.lookup(board)
    assert entry1.flag == 'exact'
    
    table.store(board, depth=2, score=0.3, flag='lowerbound')
    entry2 = table.lookup(board)
    assert entry2.flag == 'lowerbound'
    
    table.store(board, depth=4, score=0.7, flag='upperbound')
    entry3 = table.lookup(board)
    assert entry3.flag == 'upperbound'

def test_hash_collisions(board_factory):
    """Testa colisões de hash"""
    table = TranspositionTable()
    
    # Cria dois tabuleiros diferentes
    pieces1 = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board1 = board_factory(pieces1)
    
    pieces2 = {
        (4, 4): (PieceType.BISHOP, Color.WHITE),  # Diferente peça na mesma posição
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board2 = board_factory(pieces2)
    
    # Armazena entrada para o primeiro tabuleiro
    table.store(board1, depth=3, score=0.5, flag='exact')
    
    # Armazena entrada para o segundo tabuleiro
    table.store(board2, depth=4, score=0.7, flag='exact')
    
    # Verifica que as entradas são diferentes
    entry1 = table.lookup(board1)
    entry2 = table.lookup(board2)
    
    assert entry1.score != entry2.score
    assert entry1.depth != entry2.depth

def test_best_move_storage(board_factory):
    """Testa armazenamento do melhor movimento"""
    table = TranspositionTable()
    
    # Cria um tabuleiro simples
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Armazena uma entrada com melhor movimento
    best_move = (Position(rank=4, file=4), Position(rank=6, file=5))
    table.store(board, depth=3, score=0.5, flag='exact', best_move=best_move)
    
    # Busca a entrada
    entry = table.lookup(board)
    assert entry.best_move == best_move

def test_clear(board_factory):
    """Testa limpeza da tabela"""
    table = TranspositionTable()
    
    # Cria e armazena alguns tabuleiros diferentes
    for i in range(5):
        pieces = {
            (i+1, i+1): (PieceType.PAWN, Color.WHITE),
            (7, 7): (PieceType.KING, Color.BLACK),
        }
        board = board_factory(pieces)
        table.store(board, depth=i, score=float(i), flag='exact')
    
    # Limpa a tabela
    table.clear()
    assert table.get_size() == 0

def test_statistics(board_factory):
    """Testa coleta de estatísticas"""
    table = TranspositionTable()
    
    # Cria um tabuleiro base
    pieces = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
    }
    board = board_factory(pieces)
    
    # Armazena entradas com diferentes flags
    table.store(board, depth=3, score=0.5, flag='exact')
    
    # Modifica o tabuleiro para criar entradas diferentes
    pieces_mod1 = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
        (1, 1): (PieceType.PAWN, Color.WHITE),
    }
    board_mod1 = board_factory(pieces_mod1)
    table.store(board_mod1, depth=2, score=0.3, flag='lowerbound')
    
    pieces_mod2 = {
        (4, 4): (PieceType.KNIGHT, Color.WHITE),
        (7, 7): (PieceType.KING, Color.BLACK),
        (2, 2): (PieceType.PAWN, Color.WHITE),
    }
    board_mod2 = board_factory(pieces_mod2)
    table.store(board_mod2, depth=4, score=0.7, flag='upperbound')
    
    # Verifica estatísticas
    stats = table.get_statistics()
    assert stats['total_entries'] == 3
    assert stats['exact_scores'] == 1
    assert stats['lowerbound_scores'] == 1
    assert stats['upperbound_scores'] == 1
