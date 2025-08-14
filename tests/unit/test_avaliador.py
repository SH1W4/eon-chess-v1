import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.traditional.core.board.board import Board
from src.core.evaluation.position_evaluator import AvaliadorPosicao

# Exemplo de uso
board = Board()
avaliador = AvaliadorPosicao()
avaliacao = avaliador.avaliar(board)

# Acessar componentes individuais
print(f"Pontuação total: {avaliacao.pontuacao_total}")
print(f"Material: {avaliacao.pontuacao_material}")
print(f"Posicional: {avaliacao.pontuacao_posicional}")
print(f"Influência quântica: {avaliacao.influencia_quantica}")
