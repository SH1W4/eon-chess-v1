#!/usr/bin/env python3

import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.board.board import Board
from cultural.metrics import CulturalMetrics
from narrative.engine_simple import NarrativeEngine
from core.evaluation.position_evaluator import PositionEvaluator

def main():
    # Inicializa componentes
    board = Board()
    cultural_metrics = CulturalMetrics()
    narrative_engine = NarrativeEngine()
    evaluator = PositionEvaluator()
    
    # Configura tema bizantino
    elementos_bizantinos = [
        "Estratégia Imperial",
        "Diplomacia Bizantina",
        "Hierarquia Militar",
        "Ritual da Corte",
        "Simbolismo Ortodoxo"
    ]
    
    # Analisa impacto cultural
    impacto_bizantino = cultural_metrics.analyze_cultural_impact(elementos_bizantinos)
    
    # Inicia o jogo
    print("\nIniciando partida com tema Bizantino:")
    print(board.display())
    
    # Testa movimentos básicos
    moves_to_test = [
        ('e2', 'e4'),  # Peão branco
        ('e7', 'e5'),  # Peão preto
        ('g1', 'f3'),  # Cavalo branco
        ('b8', 'c6'),  # Cavalo preto
        ('f1', 'c4'),  # Bispo branco
        ('f8', 'c5'),  # Bispo preto
    ]
    
    for from_pos, to_pos in moves_to_test:
        # Gera narrativa cultural para o movimento
        narrative = narrative_engine.generate_move_narrative(
            from_pos, 
            to_pos, 
            board.get_piece(from_pos),
            impacto_bizantino
        )
        
        print(f"\nNarrativa: {narrative}")
        
        # Executa movimento
        result = board.move_piece(from_pos, to_pos)
        if result['success']:
            print(f"Movimento válido: {from_pos} -> {to_pos}")
            print(board.display())
            
            # Avalia posição
            evaluation = evaluator.evaluate_position(board)
            print(f"Avaliação da posição: {evaluation}")
        else:
            print(f"Movimento inválido: {result['error']}")
    
    # Testa regras especiais
    print("\nTestando regras especiais:")
    
    # Roque
    print("\nTentando roque:")
    result = board.castle_kingside()
    print("Roque curto:", "sucesso" if result['success'] else f"falha - {result['error']}")
    
    # En passant
    print("\nTentando en passant:")
    if board.is_en_passant_possible():
        result = board.move_piece('d5', 'e6')  # Exemplo de en passant
        print("En passant:", "sucesso" if result['success'] else f"falha - {result['error']}")
    else:
        print("En passant não disponível no momento")
    
    # Promoção
    print("\nTentando promoção:")
    result = board.promote_pawn('a7', 'a8', 'queen')
    print("Promoção:", "sucesso" if result['success'] else f"falha - {result['error']}")
    
    # Verifica xeque/xeque-mate
    print("\nEstado do jogo:")
    print(f"Xeque: {board.is_in_check()}")
    print(f"Xeque-mate: {board.is_checkmate()}")
    print(f"Empate: {board.is_stalemate()}")

if __name__ == "__main__":
    main()
