import pytest
import asyncio
from unittest.mock import Mock, patch
import numpy as np
import time
from datetime import datetime

from core.models import Position, Color, PieceType, Piece
from core.board.board import Board
from core.orchestration.aeon_orchestrator import AEONOrchestrator
from arquimax.chess_integration import ARQUIMAXChessIntegrator, PositionAnalysis
from learning.symbiotic_learner import SymbioticLearner, LearningMetrics
from monitoring.advanced_monitor import AdvancedMonitor

# Fixtures
@pytest.fixture
def board():
    """Cria um tabuleiro de teste"""
    board = Board()
    return board

@pytest.fixture
def orchestrator():
    """Cria um orquestrador de teste"""
    return AEONOrchestrator()

@pytest.fixture
def arquimax():
    """Cria um integrador ARQUIMAX de teste"""
    return ARQUIMAXChessIntegrator()

@pytest.fixture
def learner():
    """Cria um learner simbiótico de teste"""
    return SymbioticLearner()

@pytest.fixture
def monitor():
    """Cria um monitor avançado de teste"""
    return AdvancedMonitor()

# Testes do Sistema Base
@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    """Testa inicialização do orquestrador"""
    success = await orchestrator.initialize_symbiotic_mode()
    assert success == True
    assert orchestrator.current_phase.value == "bootstrap"

@pytest.mark.asyncio
async def test_orchestrator_workflow(orchestrator):
    """Testa workflow completo do orquestrador"""
    success = await orchestrator.execute_full_workflow()
    assert success == True
    assert orchestrator.current_phase.value == "autonomous"

# Testes da Integração ARQUIMAX
@pytest.mark.asyncio
async def test_arquimax_position_analysis(arquimax, board):
    """Testa análise de posição ARQUIMAX"""
    analysis = await arquimax.analyze_position(board)
    assert isinstance(analysis, PositionAnalysis)
    assert -100 <= analysis.score <= 100
    assert 0 <= analysis.winning_chances <= 1
    assert 0 <= analysis.complexity <= 1
    assert 0 <= analysis.quantum_influence <= 1.5

@pytest.mark.asyncio
async def test_arquimax_best_move(arquimax, board):
    """Testa busca do melhor movimento"""
    analysis = await arquimax.analyze_position(board)
    assert analysis.best_move is not None
    from_pos, to_pos = analysis.best_move
    assert isinstance(from_pos, Position)
    assert isinstance(to_pos, Position)

# Testes do Sistema de Aprendizado
@pytest.mark.asyncio
async def test_symbiotic_learning(learner, board):
    """Testa aprendizado simbiótico"""
    analysis = await learner.arquimax.analyze_position(board)
    metrics = await learner.learn_from_position(board, analysis)
    
    assert isinstance(metrics, LearningMetrics)
    assert 0 <= metrics.adaptation_rate <= 1
    assert 0 <= metrics.pattern_recognition <= 1
    assert 0 <= metrics.evolution_score <= 1
    assert 0 <= metrics.convergence_rate <= 1

@pytest.mark.asyncio
async def test_pattern_recognition(learner, board):
    """Testa reconhecimento de padrões"""
    analysis = await learner.arquimax.analyze_position(board)
    await learner.learn_from_position(board, analysis)
    
    # Testa com a mesma posição
    metrics = await learner.learn_from_position(board, analysis)
    assert metrics.pattern_recognition > 0
    assert len(learner.position_patterns) > 0

# Testes do Sistema de Monitoramento
@pytest.mark.asyncio
async def test_system_health_monitoring(monitor):
    """Testa monitoramento de saúde do sistema"""
    status = await monitor.get_system_status()
    
    assert 'health' in status
    assert 0 <= status['health'].cpu_usage <= 1
    assert 0 <= status['health'].memory_usage <= 1
    assert status['health'].response_time >= 0
    assert 0 <= status['health'].error_rate <= 1

@pytest.mark.asyncio
async def test_component_monitoring(monitor):
    """Testa monitoramento de componentes"""
    component = 'arquimax'
    metrics = await monitor.get_component_status(component)
    
    assert metrics is not None
    assert metrics.component_name == component
    assert 0 <= metrics.success_rate <= 1
    assert metrics.error_count >= 0
    assert isinstance(metrics.last_execution, datetime)

# Testes de Integração
@pytest.mark.asyncio
async def test_full_system_integration(orchestrator, board, monitor):
    """Testa integração completa do sistema"""
    # Inicializa sistema
    await orchestrator.initialize_symbiotic_mode()
    
    # Inicia monitoramento
    monitoring_task = asyncio.create_task(monitor.start_monitoring())
    
    # Executa workflow
    success = await orchestrator.execute_full_workflow()
    assert success == True
    
    # Verifica status
    status = await monitor.get_system_status()
    assert status['health'].error_rate < 0.1
    
    # Cancela monitoramento
    monitoring_task.cancel()
    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass

# Testes de Performance
@pytest.mark.asyncio
async def test_system_performance(orchestrator, board, monitor):
    """Testa performance do sistema"""
    start_time = time.time()
    
    # Executa operações
    await orchestrator.initialize_symbiotic_mode()
    await orchestrator.execute_adaptation_phase()
    
    # Verifica tempo de execução
    execution_time = time.time() - start_time
    assert execution_time < 5.0  # Deve executar em menos de 5 segundos
    
    # Coleta e verifica métricas de performance
    metrics = await monitor._collect_performance_metrics()
    assert metrics.moves_analyzed > 0
    assert metrics.patterns_recognized > 0
    assert metrics.adaptation_score > 0

if __name__ == '__main__':
    pytest.main(['-v'])
