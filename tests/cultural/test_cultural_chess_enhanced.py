#!/usr/bin/env python3

import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.board.board import Board
from cultural.metrics import CulturalMetrics
from cultural.memory import CulturalMemory
from cultural.culture_framework import byzantine_culture, viking_culture
from narrative.engine_simple import NarrativeEngine
from core.evaluation.position_evaluator import PositionEvaluator
from tests.cultural_engine.test_cultural_framework import CulturalTestFramework

def main():
    print("\n=== Teste Cultural Avançado: Bizantinos vs Vikings ===\n")
    
    # Inicializa o framework de teste
    framework = CulturalTestFramework()
    
    # Gera e exibe o relatório de teste
    report = framework.generate_test_report(byzantine_culture, viking_culture)
    print(report)
    
    # Executa uma partida com acompanhamento cultural
    print("\n=== Iniciando Partida Cultural ===\n")
    
    board = Board()
    memory = CulturalMemory()
    narrative_engine = NarrativeEngine()
    evaluator = PositionEvaluator()
    
    # Movimentos de teste
    moves_to_test = [
        ('e2', 'e4', byzantine_culture),  # Peão branco (Bizantino)
        ('e7', 'e5', viking_culture),     # Peão preto (Viking)
        ('g1', 'f3', byzantine_culture),  # Cavalo branco (Bizantino)
        ('b8', 'c6', viking_culture),     # Cavalo preto (Viking)
        ('f1', 'c4', byzantine_culture),  # Bispo branco (Bizantino)
        ('f8', 'c5', viking_culture),     # Bispo preto (Viking)
    ]
    
    print(board.display())
    
    for from_pos, to_pos, culture in moves_to_test:
        piece = board.get_piece(from_pos)
        if not piece:
            continue
            
        # Gera narrativa cultural
        context = memory.get_cultural_context()
        cultural_weight = culture.calculate_cultural_weight(piece.type, context)
        
        # Seleciona tema baseado no contexto
        theme_name = list(culture.themes.keys())[0]  # Simplificado para exemplo
        narratives = culture.get_theme_narratives(theme_name)
        
        # Gera e exibe narrativa
        narrative = narrative_engine.generate_move_narrative(
            from_pos, to_pos, piece, {'narrative_pool': narratives}
        )
        print(f"\nNarrativa: {narrative}")
        
        # Executa movimento
        result = board.move_piece(from_pos, to_pos)
        if result['success']:
            print(f"Movimento válido: {from_pos} -> {to_pos}")
            print(board.display())
            
            # Registra movimento na memória cultural
            memory.record_move(piece, from_pos, to_pos, cultural_weight)
            
            # Avalia posição
            evaluation = evaluator.evaluate_position(board)
            print(f"Avaliação da posição: {evaluation}")
            
            # Exibe contexto cultural atual
            context = memory.get_cultural_context()
            print("\nContexto Cultural:")
            print(f"- Tensão: {context['tension']:.2f}")
            print(f"- Movimentos: {context['moves']}")
            print(f"- Capturas (B/P): {context['white_captures']}/{context['black_captures']}")
        else:
            print(f"Movimento inválido: {result['error']}")
    
    # Exibe estado final do jogo
    print("\nEstado do jogo:")
    print(f"Xeque: {board.is_in_check()}")
    print(f"Xeque-mate: {board.is_checkmate()}")
    print(f"Empate: {board.is_stalemate()}")
    
    # Exibe eventos significativos
    print("\nEventos Significativos:")
    for event in memory.get_recent_events():
        print(f"- {event.description} (Impacto: {event.cultural_impact:.2f})")

if __name__ == "__main__":
    main()
