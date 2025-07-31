"""
Testes para o sistema unificado de avaliação de posição
"""
import pytest
from src.core.board.board import Board, Position, PieceType, Color
from src.core.evaluation.position_evaluator import AvaliadorPosicao, AvaliacaoPosicao

def test_avaliacao_posicao_inicial():
    """Testa a avaliação da posição inicial"""
    board = Board()  # Posição inicial
    avaliador = AvaliadorPosicao()
    
    avaliacao = avaliador.avaliar(board)
    
    # Na posição inicial, a pontuação deve ser próxima de zero
    assert abs(avaliacao.pontuacao_total) < 0.1
    assert abs(avaliacao.pontuacao_material) == 0.0  # Material igual
    assert abs(avaliacao.pontuacao_posicional) < 0.1  # Posições simétricas

def test_avaliacao_vantagem_material():
    """Testa a avaliação quando há vantagem material"""
    board = Board()
    # Remove uma torre preta
    board.remove_piece(Position(8, 1))  # a8
    
    avaliador = AvaliadorPosicao()
    avaliacao = avaliador.avaliar(board)
    
    # Brancas devem ter vantagem de aproximadamente 5 pontos (valor da torre)
    assert 4.5 <= avaliacao.pontuacao_material <= 5.5
    assert avaliacao.pontuacao_total > 0  # Vantagem para as brancas

def test_avaliacao_desenvolvimento():
    """Testa a avaliação do desenvolvimento das peças"""
    board = Board()
    
    # Desenvolve algumas peças brancas
    board.move_piece(Position(2, 5), Position(4, 5))  # e2-e4
    board.move_piece(Position(1, 6), Position(3, 5))  # Nf3
    
    avaliador = AvaliadorPosicao()
    avaliacao = avaliador.avaliar(board)
    
    # Brancas devem ter vantagem no desenvolvimento
    assert avaliacao.pontuacao_desenvolvimento > 0
    assert avaliacao.pontuacao_controle_centro > 0

def test_avaliacao_estrutura_peoes():
    """Testa a avaliação da estrutura de peões"""
    board = Board()
    
    # Cria peões dobrados para as pretas
    board.move_piece(Position(7, 4), Position(5, 4))  # d7-d5
    board.move_piece(Position(7, 5), Position(5, 4))  # e7-d5
    
    avaliador = AvaliadorPosicao()
    avaliacao = avaliador.avaliar(board)
    
    # Estrutura de peões das brancas deve ser melhor
    assert avaliacao.pontuacao_estrutura_peoes > 0

def test_avaliacao_seguranca_rei():
    """Testa a avaliação da segurança do rei"""
    board = Board()
    
    # Expõe o rei preto
    board.move_piece(Position(7, 6), Position(6, 6))  # f7-f6
    board.move_piece(Position(7, 7), Position(6, 7))  # g7-g6
    board.move_piece(Position(8, 6), Position(6, 8))  # Rei preto se move
    
    avaliador = AvaliadorPosicao()
    avaliacao = avaliador.avaliar(board)
    
    # Rei preto deve estar menos seguro
    assert avaliacao.pontuacao_seguranca_rei > 0

def test_avaliacao_mobilidade():
    """Testa a avaliação da mobilidade das peças"""
    board = Board()
    
    # Desenvolve peças brancas para aumentar mobilidade
    board.move_piece(Position(2, 4), Position(4, 4))  # d2-d4
    board.move_piece(Position(2, 5), Position(4, 5))  # e2-e4
    board.move_piece(Position(1, 3), Position(3, 4))  # Bispo para d3
    
    avaliador = AvaliadorPosicao()
    avaliacao = avaliador.avaliar(board)
    
    # Brancas devem ter mais mobilidade
    assert avaliacao.pontuacao_mobilidade > 0

def test_avaliacao_fase_jogo():
    """Testa a detecção correta da fase do jogo"""
    board = Board()
    avaliador = AvaliadorPosicao()
    
    # Posição inicial - meio jogo
    assert not avaliador._is_endgame(board)
    
    # Remove várias peças para simular final
    for file in range(1, 9):
        if file not in [4, 5]:  # Mantém apenas os reis e algumas peças
            board.remove_piece(Position(1, file))
            board.remove_piece(Position(2, file))
            board.remove_piece(Position(7, file))
            board.remove_piece(Position(8, file))
    
    # Deve detectar final de jogo
    assert avaliador._is_endgame(board)

def test_influencia_quantica():
    """Testa a avaliação da influência quântica"""
    board = Board()
    avaliador = AvaliadorPosicao()
    
    # Na posição inicial
    avaliacao_inicial = avaliador.avaliar(board)
    
    # Move algumas peças para criar mais dinâmica
    board.move_piece(Position(2, 5), Position(4, 5))  # e2-e4
    board.move_piece(Position(7, 5), Position(5, 5))  # e7-e5
    board.move_piece(Position(1, 6), Position(3, 5))  # Nf3
    
    avaliacao_dinamica = avaliador.avaliar(board)
    
    # Posição mais dinâmica deve ter maior influência quântica
    assert abs(avaliacao_dinamica.influencia_quantica) > abs(avaliacao_inicial.influencia_quantica)
