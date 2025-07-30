"""
Configuração global dos testes
"""
import pytest
from typing import Dict
import json
import os
from pathlib import Path

# Configurações de teste
TEST_CONFIG = {
    'config_path': 'tests/fixtures/config.json',
    'patterns_path': 'tests/fixtures/patterns.json',
    'history_path': 'tests/fixtures/history.json'
}

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(tmp_path_factory):
    """Configura ambiente de testes"""
    base_dir = tmp_path_factory.mktemp("chess_test_data")
    
    # Criar diretórios de teste
    fixtures_dir = base_dir / "fixtures"
    fixtures_dir.mkdir(exist_ok=True)
    
    # Criar arquivos de configuração básicos
    config = {
        "evaluation_weights": {
            "material": 1.0,
            "position": 0.8,
            "mobility": 0.6,
            "king_safety": 0.9
        },
        "search_depth": 4,
        "cache_size": 1000000
    }
    
    patterns = {
        "openings": ["Sicilian", "Ruy Lopez", "Queen's Gambit"],
        "middlegame_patterns": ["fork", "pin", "skewer"],
        "endgame_patterns": ["mate_basic", "mate_advanced"]
    }
    
    history = {
        "games": [],
        "performance_metrics": {
            "wins": 0,
            "losses": 0,
            "draws": 0
        }
    }
    
    # Salvar arquivos
    (fixtures_dir / "config.json").write_text(json.dumps(config, indent=2))
    (fixtures_dir / "patterns.json").write_text(json.dumps(patterns, indent=2))
    (fixtures_dir / "history.json").write_text(json.dumps(history, indent=2))
    
    # Atualizar caminhos de teste
    for key in TEST_CONFIG:
        TEST_CONFIG[key] = str(fixtures_dir / Path(TEST_CONFIG[key]).name)
    
    return TEST_CONFIG

@pytest.fixture
def mock_board():
    """Fixture para tabuleiro limpo"""
    from src.core.board.board import Board
    return Board()

@pytest.fixture
def sample_game_position(mock_board):
    """Fixture para posição de jogo específica"""
    # Configurar uma posição interessante para testes
    from src.core.board.board import Position
    
    # Mover algumas peças para criar uma posição de teste
    mock_board.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
    mock_board.move_piece(Position.from_algebraic("e7"), Position.from_algebraic("e5"))
    mock_board.move_piece(Position.from_algebraic("d2"), Position.from_algebraic("d4"))
    
    return mock_board

@pytest.fixture
def ai_player():
    """Fixture para jogador IA"""
    from src.ai.pipeline.adaptive_ai import AdaptiveAI
    from src.ai.pipeline.player_profile import PlayerProfile
    
    profile = PlayerProfile(
        aggression=0.6,
        risk_taking=0.4,
        positional=0.7
    )
    
    return AdaptiveAI(profile=profile)

@pytest.fixture
def performance_monitor():
    """Fixture para monitoramento de performance"""
    class PerformanceMonitor:
        def __init__(self):
            self.move_times = []
            self.memory_usage = []
            self.nodes_explored = []
        
        def record_move(self, time_ms: float, memory_mb: float, nodes: int):
            self.move_times.append(time_ms)
            self.memory_usage.append(memory_mb)
            self.nodes_explored.append(nodes)
        
        @property
        def avg_move_time(self) -> float:
            return sum(self.move_times) / len(self.move_times) if self.move_times else 0
        
        @property
        def max_memory(self) -> float:
            return max(self.memory_usage) if self.memory_usage else 0
    
    return PerformanceMonitor()

def pytest_configure(config):
    """Configuração do pytest"""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers",
        "ai: mark test as AI-related"
    )
