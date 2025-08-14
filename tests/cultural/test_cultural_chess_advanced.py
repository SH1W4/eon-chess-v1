#!/usr/bin/env python3

import sys
import os
from typing import Dict, List, Tuple

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.board.board import Board
from cultural.metrics import CulturalMetrics
from cultural.memory import CulturalMemory
from cultural.events import CulturalEventSystem
from cultural.style_analyzer import CulturalStyleAnalyzer
from cultural.cultures import persian_culture, viking_culture, samurai_culture
from narrative.engine_simple import NarrativeEngine
from core.evaluation.position_evaluator import PositionEvaluator

def print_cultural_report(culture_name: str, analysis_results: Dict):
    """Imprime um relatório cultural detalhado"""
    print(f"\n=== Relatório Cultural: {culture_name} ===")
    print("\nEstilo de Jogo:")
    print(f"- Primário: {analysis_results['primary_style'].name}")
    if analysis_results.get('secondary_style'):
        print(f"- Secundário: {analysis_results['secondary_style'].name}")
    
    print("\nExpressão Cultural:")
    print(f"- Nível: {analysis_results['cultural_expression']:.2f}")
    print(f"- Consistência: {analysis_results['style_consistency']:.2f}")
    
    print("\nPadrões Notáveis:")
    for pattern in analysis_results['notable_patterns']:
        print(f"- {pattern}")
    
    print("\nRecomendações:")
    for rec in analysis_results['recommendations']:
        print(f"- {rec}")

def print_event_report(event):
    """Imprime detalhes de um evento cultural"""
    print(f"\n=== Evento Cultural: {event.name} ===")
    print(f"Descrição: {event.description}")
    print(f"Impacto Cultural: {event.cultural_impact:.2f}")
    print("Bônus Ativos:")
    for bonus_type, value in event.bonuses.items():
        print(f"- {bonus_type}: x{value}")

def main():
    # Inicializa componentes
    board = Board()
    memory = CulturalMemory()
    narrative_engine = NarrativeEngine()
    evaluator = PositionEvaluator()
    event_system = CulturalEventSystem()
    style_analyzer = CulturalStyleAnalyzer()
    
    # Define o confronto cultural
    print("\n=== Confronto Cultural: Império Persa vs. Guerreiros Viking ===")
    
    # Sequência de movimentos para teste
    moves_to_test = [
        ('e2', 'e4', persian_culture),  # Peão persa
        ('e7', 'e5', viking_culture),   # Peão viking
        ('g1', 'f3', persian_culture),  # Cavalo persa
        ('b8', 'c6', viking_culture),   # Cavalo viking
        ('f1', 'c4', persian_culture),  # Bispo persa
        ('f8', 'c5', viking_culture),   # Bispo viking
        ('d2', 'd3', persian_culture),  # Peão persa
        ('d7', 'd6', viking_culture),   # Peão viking
    ]
    
    print(board.display())
    
    # Executa os movimentos
    for from_pos, to_pos, culture in moves_to_test:
        piece = board.get_piece(from_pos)
        if not piece:
            continue
            
        # Verifica eventos culturais
        board_state = {
            'position': board.display(),
            'current_move': (from_pos, to_pos),
            'piece': piece
        }
        
        events = event_system.check_event_triggers(board_state, culture)
        
        # Gera narrativa cultural
        context = memory.get_cultural_context()
        cultural_weight = culture.calculate_cultural_weight(piece.type, context)
        
        # Seleciona tema baseado no contexto e eventos
        theme_name = list(culture.themes.keys())[0]
        narratives = culture.get_theme_narratives(theme_name)
        
        # Gera e exibe narrativa
        narrative = narrative_engine.generate_move_narrative(
            from_pos, to_pos, piece, {'narrative_pool': narratives}
        )
        print(f"\nNarrativa: {narrative}")
        
        # Exibe eventos ativos
        for event in events:
            print_event_report(event)
            board_state = event_system.apply_event_effects(event, board_state)
        
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
    
    # Análise final
    print("\n=== Análise Final ===")
    
    # Analisa estilo Persa
    persian_analysis = style_analyzer.analyze_game_style(memory, persian_culture)
    print_cultural_report("Império Persa", {
        'primary_style': persian_analysis.primary_style,
        'secondary_style': persian_analysis.secondary_style,
        'cultural_expression': persian_analysis.cultural_expression,
        'style_consistency': persian_analysis.style_consistency,
        'notable_patterns': persian_analysis.notable_patterns,
        'recommendations': persian_analysis.recommendations
    })
    
    # Analisa estilo Viking
    viking_analysis = style_analyzer.analyze_game_style(memory, viking_culture)
    print_cultural_report("Guerreiros Viking", {
        'primary_style': viking_analysis.primary_style,
        'secondary_style': viking_analysis.secondary_style,
        'cultural_expression': viking_analysis.cultural_expression,
        'style_consistency': viking_analysis.style_consistency,
        'notable_patterns': viking_analysis.notable_patterns,
        'recommendations': viking_analysis.recommendations
    })
    
    # Exibe eventos significativos
    print("\nEventos Significativos:")
    for event in memory.get_recent_events():
        print(f"- {event.description} (Impacto: {event.cultural_impact:.2f})")

if __name__ == "__main__":
    main()
