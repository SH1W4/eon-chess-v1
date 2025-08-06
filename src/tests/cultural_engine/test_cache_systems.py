import pytest
from cultural.cache import (
    CulturalAnalysisCache, CulturalEventCache, NarrativeCache
)

@pytest.fixture
def board_state():
    return {'position': 'some_position'}

@pytest.fixture
def analysis_cache():
    return CulturalAnalysisCache()

@pytest.fixture
def event_cache():
    return CulturalEventCache()

@pytest.fixture
def narrative_cache():
    return NarrativeCache()


def test_cache_patterns(analysis_cache, board_state):
    """Testa o cache de padrões"""
    analysis_cache.cache_pattern('spiral', board_state)
    patterns = analysis_cache.get_patterns(board_state)
    assert 'spiral' in patterns


def test_cache_events(event_cache, board_state):
    """Testa o cache de eventos culturais"""
    event_cache.cache_event('indian', 'chakravyuha', board_state)
    events = event_cache.get_active_events('indian')
    assert 'chakravyuha' in events


def test_cache_narratives(narrative_cache, board_state):
    """Testa o armazenamento e recuperação de narrativas"""
    narrative_cache.cache_narrative('arabic', 'Uma narrativa poética', board_state)
    narratives = narrative_cache.get_recent_narratives('arabic')
    assert 'Uma narrativa poética' in narratives

