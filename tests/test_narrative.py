import pytest
from src.narrative.engine.engine import NarrativeEngine, NarrativeConfig
from src.core.board.board import Board, Position, Color, PieceType
from src.core.board.move import Move

@pytest.fixture
def narrative_engine():
    """Fixture que fornece uma instância configurada do motor narrativo."""
    config = NarrativeConfig(language="en", mode="standard")
    engine = NarrativeEngine(config)
    engine.initialize()
    return engine

def test_move_narrative(narrative_engine):
    """Testa geração de narrativa para um movimento"""
    context = {
        "type": "move",
        "piece": "pawn",
        "from": "e2",
        "to": "e4",
        "color": "white"
    }
    narrative = narrative_engine.generate_narrative(context)
    assert "narrativa" in narrative.lower() or "narrative" in narrative.lower()

def test_capture_narrative(narrative_engine):
    """Testa geração de narrativa para uma captura"""
    context = {
        "type": "capture",
        "piece": "pawn",
        "captured": "pawn",
        "from": "e4",
        "to": "d5",
        "color": "white"
    }
    narrative = narrative_engine.generate_narrative(context)
    assert "narrativa" in narrative.lower() or "narrative" in narrative.lower()

def test_check_narrative(narrative_engine):
    """Testa geração de narrativa para um xeque"""
    context = {
        "type": "check",
        "piece": "queen",
        "from": "d1",
        "to": "h5",
        "color": "white",
        "check": True
    }
    narrative = narrative_engine.generate_narrative(context)
    assert "narrativa" in narrative.lower() or "narrative" in narrative.lower()

def test_position_narrative(narrative_engine):
    """Testa geração de narrativa para uma posição"""
    context = {
        "type": "position",
        "phase": "opening",
        "center_control": "white",
        "development": "balanced"
    }
    narrative = narrative_engine.generate_narrative(context)
    assert "narrativa" in narrative.lower() or "narrative" in narrative.lower()

def test_culture_switching(narrative_engine):
    """Testa mudança de cultura nas narrativas"""
    # Narrativa padrão em inglês
    narrative_engine.config.language = "en"
    context = {
        "type": "move",
        "piece": "pawn",
        "from": "e2",
        "to": "e4"
    }
    narrative1 = narrative_engine.generate_narrative(context)
    
    # Narrativa em português
    narrative_engine.config.language = "pt-BR"
    narrative2 = narrative_engine.generate_narrative(context)
    
    # Verifica que ambas as narrativas foram geradas
    assert len(narrative1) > 0
    assert len(narrative2) > 0

