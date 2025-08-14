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
    
    # Configura tema bizantino (brancas)
    elementos_bizantinos = [
        "Estratégia Imperial",
        "Diplomacia Bizantina",
        "Hierarquia Militar",
        "Ritual da Corte",
        "Simbolismo Ortodoxo"
    ]
    
    # Configura tema viking (pretas)
    elementos_vikings = [
        "Bravura Nórdica",
        "Batalha Naval",
        "Honra dos Guerreiros",
        "Sabedoria de Odin",
        "Força de Thor"
    ]
    
    # Adiciona temas vikings ao motor cultural
    cultural_metrics.themes.update({
        "Bravura Nórdica": {
            "weight": 0.8,
            "narratives": [
                "Com a força dos Vikings, {piece} avança sem medo",
                "Como um guerreiro nórdico, {piece} desafia seus inimigos",
                "Honrando a tradição viking, {piece} busca glória em batalha"
            ]
        },
        "Batalha Naval": {
            "weight": 0.7,
            "narratives": [
                "Como um navegante viking, {piece} conquista novo território",
                "Com a destreza de um capitão nórdico, {piece} traça seu curso",
                "Seguindo as rotas dos drakkar, {piece} explora novos horizontes"
            ]
        },
        "Honra dos Guerreiros": {
            "weight": 0.9,
            "narratives": [
                "Pela honra do clã, {piece} enfrenta o desafio",
                "Como um berserker em fúria, {piece} avança para a batalha",
                "Com o espírito de Valhalla, {piece} busca glória eterna"
            ]
        },
        "Sabedoria de Odin": {
            "weight": 0.6,
            "narratives": [
                "Guiado pela sabedoria do Pai de Todos, {piece} move-se com astúcia",
                "Com o conhecimento das runas, {piece} revela seu poder",
                "Sob o olhar de Odin, {piece} tece seu destino"
            ]
        },
        "Força de Thor": {
            "weight": 0.7,
            "narratives": [
                "Com a força do Deus do Trovão, {piece} golpeia como um raio",
                "Empunhando o poder de Mjolnir, {piece} domina o campo",
                "Como o trovão de Thor, {piece} ressoa pelo tabuleiro"
            ]
        }
    })
    
    # Analisa impacto cultural para ambos os lados
    impacto_bizantino = cultural_metrics.analyze_cultural_impact(elementos_bizantinos)
    impacto_viking = cultural_metrics.analyze_cultural_impact(elementos_vikings)
    
    # Inicia o jogo
    print("\nIniciando partida: Império Bizantino vs. Vikings")
    print(board.display())
    
    # Testa movimentos básicos
    moves_to_test = [
        ('e2', 'e4', impacto_bizantino),  # Peão branco (Bizantino)
        ('e7', 'e5', impacto_viking),     # Peão preto (Viking)
        ('g1', 'f3', impacto_bizantino),  # Cavalo branco (Bizantino)
        ('b8', 'c6', impacto_viking),     # Cavalo preto (Viking)
        ('f1', 'c4', impacto_bizantino),  # Bispo branco (Bizantino)
        ('f8', 'c5', impacto_viking),     # Bispo preto (Viking)
    ]
    
    for from_pos, to_pos, cultural_impact in moves_to_test:
        # Gera narrativa cultural para o movimento
        narrative = narrative_engine.generate_move_narrative(
            from_pos, 
            to_pos, 
            board.get_piece(from_pos),
            cultural_impact
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
    
    print("\nEstado do jogo:")
    print(f"Xeque: {board.is_in_check()}")
    print(f"Xeque-mate: {board.is_checkmate()}")
    print(f"Empate: {board.is_stalemate()}")

if __name__ == "__main__":
    main()
