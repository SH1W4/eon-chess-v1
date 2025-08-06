import pytest
from cultural_evolution import EvolutionMetrics, CulturalEvolution
from adaptive_decision import CulturalBehavior

def test_evolution_metrics_initialization():
    """Testa a inicialização correta das métricas"""
    metrics = EvolutionMetrics()
    assert metrics.success_rate == 0.0
    assert metrics.behavior_distribution == {}
    assert metrics.adaptation_score == 0.0
    assert metrics.cultural_coherence == 1.0

def test_behavior_distribution_normalization():
    """Testa a normalização da distribuição de comportamentos"""
    metrics = EvolutionMetrics()
    
    # Primeiro comportamento
    metrics.update(1.0, CulturalBehavior.AGGRESSIVE)
    assert CulturalBehavior.AGGRESSIVE in metrics.behavior_distribution
    assert metrics.behavior_distribution[CulturalBehavior.AGGRESSIVE] > 0
    
    # Total das probabilidades deve ser aproximadamente 1
    total = sum(metrics.behavior_distribution.values())
    assert abs(total - 1.0) < 1e-6

def test_multiple_behaviors():
    """Testa a atualização com múltiplos comportamentos"""
    metrics = EvolutionMetrics()
    
    # Adiciona vários comportamentos
    behaviors = [
        CulturalBehavior.AGGRESSIVE,
        CulturalBehavior.DEFENSIVE,
        CulturalBehavior.STRATEGIC
    ]
    
    for behavior in behaviors:
        metrics.update(1.0, behavior)
    
    # Verifica se todos os comportamentos estão presentes
    for behavior in behaviors:
        assert behavior in metrics.behavior_distribution
        assert metrics.behavior_distribution[behavior] > 0
    
    # Total ainda deve ser aproximadamente 1
    total = sum(metrics.behavior_distribution.values())
    assert abs(total - 1.0) < 1e-6

def test_cultural_coherence():
    """Testa o cálculo da coerência cultural"""
    metrics = EvolutionMetrics()
    
    # Inicialmente deve ser 1.0
    assert metrics.cultural_coherence == 1.0
    
    # Após adicionar comportamentos, deve mudar
    metrics.update(1.0, CulturalBehavior.AGGRESSIVE)
    metrics.update(1.0, CulturalBehavior.DEFENSIVE)
    
    # Coerência deve estar entre 0 e 1
    assert 0 < metrics.cultural_coherence <= 1.0

def test_adaptation_score():
    """Testa o cálculo do score de adaptação"""
    metrics = EvolutionMetrics()
    
    # Adiciona comportamento com alta taxa de sucesso
    metrics.update(0.9, CulturalBehavior.STRATEGIC)
    
    # Score de adaptação deve ser positivo e menor que 1
    assert 0 < metrics.adaptation_score < 1.0

def test_cultural_evolution_behavior_weights():
    """Testa os pesos dos comportamentos na evolução cultural"""
    evolution = CulturalEvolution()
    
    # Registra alguns resultados
    context = {"under_attack": True}
    evolution.record_outcome(CulturalBehavior.DEFENSIVE, 0.8, context)
    evolution.record_outcome(CulturalBehavior.AGGRESSIVE, 0.6, context)
    
    # Verifica se os pesos foram atualizados
    weights = evolution.decision_tree.get_behavior_weights()
    assert CulturalBehavior.DEFENSIVE in weights
    assert CulturalBehavior.AGGRESSIVE in weights

def test_behavior_narrative():
    """Testa a geração de narrativas de comportamento"""
    evolution = CulturalEvolution()
    
    # Gera narrativa para comportamento
    narrative = evolution.get_behavior_narrative(CulturalBehavior.STRATEGIC)
    assert isinstance(narrative, str)
    assert len(narrative) > 0

def test_evolution_summary():
    """Testa o resumo da evolução"""
    evolution = CulturalEvolution()
    
    # Registra alguns resultados
    context = {"under_attack": False}
    evolution.record_outcome(CulturalBehavior.STRATEGIC, 0.7, context)
    
    # Obtém resumo
    summary = evolution.get_evolution_summary()
    
    # Verifica campos essenciais
    assert 'dominant_behavior' in summary
    assert 'success_rate' in summary
    assert 'cultural_coherence' in summary
    assert 'behavior_distribution' in summary
    assert 'adaptation_score' in summary
    assert 'historical_depth' in summary
