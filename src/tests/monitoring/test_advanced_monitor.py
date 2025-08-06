import pytest
import asyncio
from datetime import datetime, timedelta
from monitoring.advanced_monitor import (
    AdvancedMonitor, SystemHealth, ComponentMetrics, PerformanceMetrics
)

@pytest.fixture
def monitor():
    return AdvancedMonitor()

@pytest.mark.asyncio
async def test_system_health_monitoring(monitor):
    """Testa monitoramento de saúde do sistema"""
    # Simula monitoramento
    cpu_usage = await monitor._get_cpu_usage()
    memory_usage = await monitor._get_memory_usage()
    response_time = await monitor._get_response_time()
    
    assert 0 <= cpu_usage <= 1
    assert 0 <= memory_usage <= 1
    assert response_time > 0

@pytest.mark.asyncio
async def test_component_monitoring(monitor):
    """Testa monitoramento de componentes"""
    component = 'test_component'
    metrics = await monitor._get_component_metrics(component)
    
    assert isinstance(metrics, ComponentMetrics)
    assert metrics.component_name == component
    assert 0 <= metrics.success_rate <= 1
    assert metrics.error_count >= 0
    assert isinstance(metrics.last_execution, datetime)

@pytest.mark.asyncio
async def test_performance_monitoring(monitor):
    """Testa monitoramento de performance"""
    metrics = await monitor._collect_performance_metrics()
    
    assert isinstance(metrics, PerformanceMetrics)
    assert metrics.moves_analyzed >= 0
    assert metrics.patterns_recognized >= 0
    assert 0 <= metrics.adaptation_score <= 1

@pytest.mark.asyncio
async def test_alert_generation(monitor):
    """Testa geração de alertas"""
    # Simula condição de alerta
    monitor.system_health.cpu_usage = 0.9  # Acima do threshold
    await monitor._check_health_alerts()
    
    # Verifica se alerta foi registrado no log
    # Nota: Requer configuração adequada de logging para teste completo

@pytest.mark.asyncio
async def test_component_health_analysis(monitor):
    """Testa análise de saúde de componentes"""
    component = 'test_component'
    metrics = ComponentMetrics(
        component_name=component,
        execution_time=0.5,
        success_rate=0.85,  # Abaixo do threshold
        error_count=15,     # Acima do threshold
        last_execution=datetime.now()
    )
    
    await monitor._analyze_component_health(component, metrics)
    # Verifica se alertas foram gerados
    # Nota: Requer configuração adequada de logging para teste completo

@pytest.mark.asyncio
async def test_performance_analysis(monitor):
    """Testa análise de performance"""
    monitor.performance_metrics = PerformanceMetrics(
        moves_analyzed=500,
        patterns_recognized=25,
        learning_iterations=50,
        adaptation_score=0.5,  # Abaixo do threshold
        quantum_operations=5    # Abaixo do threshold
    )
    
    await monitor._analyze_performance()
    # Verifica se alertas foram gerados
    # Nota: Requer configuração adequada de logging para teste completo

@pytest.mark.asyncio
async def test_system_status(monitor):
    """Testa obtenção de status do sistema"""
    status = await monitor.get_system_status()
    
    assert 'health' in status
    assert 'components' in status
    assert 'performance' in status
    assert isinstance(status['health'], SystemHealth)

@pytest.mark.asyncio
async def test_component_status(monitor):
    """Testa obtenção de status de componente"""
    component = 'test_component'
    status = await monitor.get_component_status(component)
    
    assert isinstance(status, ComponentMetrics)
    assert status.component_name == component

@pytest.mark.asyncio
async def test_monitoring_startup(monitor):
    """Testa inicialização do monitoramento"""
    # Cria uma task para o monitoramento
    monitoring_task = asyncio.create_task(
        monitor.start_monitoring()
    )
    
    # Aguarda alguns ciclos de monitoramento
    await asyncio.sleep(1)
    
    # Cancela a task
    monitoring_task.cancel()
    try:
        await monitoring_task
    except asyncio.CancelledError:
        pass
    
    # Verifica se dados foram coletados
    assert monitor.system_health is not None
    assert len(monitor.component_metrics) > 0
    assert monitor.performance_metrics is not None
