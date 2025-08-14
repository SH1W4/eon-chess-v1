import pytest
from dataclasses import dataclass
from typing import Dict, List
from cultural.style_analyzer import CulturalStyleAnalyzer
from cultural.memory import CulturalMemory
from cultural.culture_framework import ChessCulture
from core.board.board import PieceType, Color
from core.board.move import Move

# Fixtures
@pytest.fixture
def culture():
    return ChessCulture("Persian Classical", "Description", [], [])

@pytest.fixture
def memory():
    mem = CulturalMemory()
    # Simula alguns movimentos
    moves = [
        {'piece_type': PieceType.PAWN, 'piece_color': Color.WHITE, 
         'from_pos': 'e2', 'to_pos': 'e4'},
        {'piece_type': PieceType.KNIGHT, 'piece_color': Color.WHITE,
         'from_pos': 'g1', 'to_pos': 'f3'},
        {'piece_type': PieceType.BISHOP, 'piece_color': Color.WHITE,
         'from_pos': 'f1', 'to_pos': 'c4'}
    ]
    mem.moves_history.extend(moves)
    return mem

def test_cultural_style_analysis(culture, memory):
    """Testa a análise cultural do estilo"""
    analyzer = CulturalStyleAnalyzer()
    analysis = analyzer.analyze_game_style(memory, culture)
    
    # Verifica a estrutura da análise
    assert analysis.primary_style is not None
    assert hasattr(analysis, 'cultural_expression')
    assert hasattr(analysis, 'style_consistency')
    assert isinstance(analysis.notable_patterns, list)
    assert isinstance(analysis.recommendations, list)
    
    # Verifica expressão cultural
    assert 0 <= analysis.cultural_expression <= 1
    assert 0 <= analysis.style_consistency <= 1

def test_pattern_recognition(culture, memory):
    """Testa o reconhecimento de padrões culturais"""
    analyzer = CulturalStyleAnalyzer()
    patterns = analyzer._analyze_patterns(memory, culture)
    
    # Verifica se retorna uma lista de padrões
    assert isinstance(patterns, list)
    assert all(isinstance(pattern, str) for pattern in patterns)

def test_style_description(culture, memory):
    """Testa a geração de descrições de estilo"""
    analyzer = CulturalStyleAnalyzer()
    analysis = analyzer.analyze_game_style(memory, culture)
    
    # Verifica descrição
    assert analysis.primary_style is not None
    assert analysis.primary_style.name in ['Estratégico', 'Agressivo', 'Defensivo', 'Tático']
    assert isinstance(analysis.primary_style.description, str)
    assert len(analysis.primary_style.description) > 0

def test_recommendation_generation(culture, memory):
    """Testa a geração de recomendações"""
    analyzer = CulturalStyleAnalyzer()
    analysis = analyzer.analyze_game_style(memory, culture)
    
    # Verifica recomendações
    assert isinstance(analysis.recommendations, list)
    assert len(analysis.recommendations) > 0
    assert all(isinstance(rec, str) for rec in analysis.recommendations)

def test_style_consistency(memory):
    """Testa o cálculo de consistência de estilo"""
    analyzer = CulturalStyleAnalyzer()
    consistency = analyzer._calculate_style_consistency(memory)
    
    # Verifica valor de consistência
    assert 0 <= consistency <= 1
