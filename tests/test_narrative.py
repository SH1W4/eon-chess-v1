"""
Testes para o sistema narrativo de xadrez.
"""
import os
import pytest
from src.narrative.base import BaseNarrative, ChessPattern, GameState
from src.narrative.patterns import PatternMatcher, Board, Position, Piece
from src.narrative.engine import NarrativeEngine, MoveContext

# Configurações para testes
TEST_CONFIG = {
    'config_path': 'src/narrative/chess_config.yaml',
    'patterns_path': 'src/narrative/chess_patterns.yaml',
    'history_path': 'src/narrative/chess_tactics_history.yaml'
}

@pytest.fixture
def narrative_engine():
    """Fixture para o motor narrativo."""
    return NarrativeEngine(
        config_path=TEST_CONFIG['config_path'],
        patterns_path=TEST_CONFIG['patterns_path'],
        history_path=TEST_CONFIG['history_path']
    )

@pytest.fixture
def sample_board():
    """Fixture para um tabuleiro de teste."""
    pieces = {
        ('e', 1): Piece('king', 'white', Position('e', 1)),
        ('d', 1): Piece('queen', 'white', Position('d', 1)),
        ('e', 8): Piece('king', 'black', Position('e', 8)),
        ('d', 7): Piece('queen', 'black', Position('d', 7))
    }
    return Board(pieces=pieces, last_move=None, move_number=1)

@pytest.fixture
def sample_pattern():
    """Fixture para um padrão de teste."""
    return ChessPattern(
        name="fork",
        type="tactical",
        description="Ataque duplo com cavalo",
        significance=0.9
    )

def test_narrative_initialization(narrative_engine):
    """Testa inicialização do motor narrativo."""
    assert narrative_engine is not None
    assert narrative_engine.game_state.phase == 'opening'
    assert narrative_engine.game_state.move_number == 1

def test_culture_switching(narrative_engine):
    """Testa mudança de cultura."""
    # Cultura inicial deve ser medieval
    piece_desc = narrative_engine.narrative.get_piece_description('king')
    assert piece_desc == "Rei"
    
    # Muda para futurista
    narrative_engine.switch_culture('futuristic')
    piece_desc = narrative_engine.narrative.get_piece_description('king')
    assert piece_desc == "Núcleo"

def test_move_narrative_generation(narrative_engine):
    """Testa geração de narrativa para movimento."""
    context = MoveContext(
        piece="knight",
        from_square="b1",
        to_square="c3",
        is_capture=False,
        is_check=False,
        is_checkmate=False,
        captured_piece=None,
        promotion=None,
        is_castling=False,
        patterns=[]
    )
    
    narrative = narrative_engine.generate_move_narrative(context)
    assert narrative is not None
    assert len(narrative) > 0

def test_capture_narrative(narrative_engine):
    """Testa narrativa de captura."""
    context = MoveContext(
        piece="queen",
        from_square="d1",
        to_square="d7",
        is_capture=True,
        is_check=False,
        is_checkmate=False,
        captured_piece="pawn",
        promotion=None,
        is_castling=False,
        patterns=[]
    )
    
    narrative = narrative_engine.generate_move_narrative(context)
    assert narrative is not None
    assert "conquista" in narrative.lower() or "neutraliza" in narrative.lower()

def test_checkmate_narrative(narrative_engine):
    """Testa narrativa de xeque-mate."""
    context = MoveContext(
        piece="queen",
        from_square="d1",
        to_square="d8",
        is_capture=False,
        is_check=True,
        is_checkmate=True,
        captured_piece=None,
        promotion=None,
        is_castling=False,
        patterns=[]
    )
    
    narrative = narrative_engine.generate_move_narrative(context)
    assert narrative is not None
    assert "xeque-mate" in narrative.lower() or "vitória" in narrative.lower()

def test_pattern_identification(narrative_engine, sample_board):
    """Testa identificação de padrões."""
    patterns = narrative_engine.pattern_matcher.analyze_position(sample_board)
    assert patterns is not None
    assert isinstance(patterns, list)

def test_game_state_narrative(narrative_engine):
    """Testa narrativa do estado do jogo."""
    narrative = narrative_engine.generate_game_state_narrative()
    assert narrative is not None
    assert narrative_engine.game_state.phase in ['opening', 'middlegame', 'endgame']

def test_position_narrative(narrative_engine, sample_board):
    """Testa narrativa da posição."""
    narrative = narrative_engine.generate_position_narrative(sample_board)
    assert narrative is not None
    assert len(narrative) > 0

def test_pattern_narrative(narrative_engine, sample_pattern):
    """Testa narrativa de padrão."""
    narrative = narrative_engine._generate_pattern_narrative([sample_pattern])
    assert narrative is not None
    assert "fork" in narrative.lower() or "garfo" in narrative.lower()

def test_phase_transitions(narrative_engine):
    """Testa transições de fase do jogo."""
    # Início do jogo
    assert narrative_engine.game_state.phase == 'opening'
    
    # Meio-jogo
    for _ in range(15):
        context = MoveContext(
            piece="pawn",
            from_square="e2",
            to_square="e4",
            is_capture=False,
            is_check=False,
            is_checkmate=False,
            captured_piece=None,
            promotion=None,
            is_castling=False,
            patterns=[]
        )
        narrative_engine.generate_move_narrative(context)
    
    assert narrative_engine.game_state.phase == 'middlegame'
    
    # Final
    for _ in range(20):
        narrative_engine.generate_move_narrative(context)
    
    assert narrative_engine.game_state.phase == 'endgame'
