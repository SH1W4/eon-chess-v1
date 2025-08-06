import pytest
from cultural.adaptive_decision import CulturalBehavior, AdaptiveDecisionTree
from cultural.cultural_evolution import CulturalEvolution, EvolutionMetrics
from cultural.culture_framework import ChessCulture, CulturalTheme, PieceCulturalIdentity
from traditional.models.models import PieceType

def test_adaptive_decision_tree():
    """Testa a árvore de decisão adaptativa"""
    tree = AdaptiveDecisionTree()
    
    # Testa comportamento inicial
    context = {'under_attack': True, 'material_advantage': 0}
    behavior = tree.decide(context)
    assert behavior == CulturalBehavior.DEFENSIVE
    
    # Testa adaptação
    tree.adapt(0.8)  # Bom resultado
    new_behavior = tree.decide(context)
    assert new_behavior == CulturalBehavior.DEFENSIVE
    
    # Testa comportamento em contexto diferente
    context = {'early_game': True, 'center_control': 0.2}
    behavior = tree.decide(context)
    assert behavior == CulturalBehavior.STRATEGIC

def test_evolution_metrics():
    """Testa as métricas de evolução"""
    metrics = EvolutionMetrics()
    
    # Testa atualização de métricas
    metrics.update(0.8, CulturalBehavior.AGGRESSIVE)
    assert metrics.success_rate > 0
    assert CulturalBehavior.AGGRESSIVE in metrics.behavior_distribution
    
    # Testa múltiplas atualizações
    metrics.update(0.6, CulturalBehavior.STRATEGIC)
    metrics.update(0.7, CulturalBehavior.AGGRESSIVE)
    
    assert metrics.success_rate > 0.6
    assert metrics.cultural_coherence <= 1.0
    assert metrics.cultural_coherence > 0

def test_cultural_evolution():
    """Testa o sistema de evolução cultural"""
    evolution = CulturalEvolution()
    
    # Testa avaliação de contexto
    context = {'under_attack': True}
    behavior = evolution.evaluate_context(context)
    assert isinstance(behavior, CulturalBehavior)
    
    # Testa registro de resultados
    evolution.record_outcome(behavior, 0.7, context)
    assert len(evolution.history) == 1
    
    # Testa adaptação
    summary = evolution.get_evolution_summary()
    assert summary['success_rate'] > 0
    assert isinstance(summary['dominant_behavior'], CulturalBehavior)

def test_theme_adaptation():
    """Testa adaptação de temas culturais"""
    theme = CulturalTheme(
        name="Test Theme",
        description="Test Description",
        weight=0.5,
        narratives=[
            "Avança para atacar o inimigo",
            "Defende sua posição com vigor",
            "Planeja sua estratégia com cuidado"
        ]
    )
    
    # Testa adaptação de peso
    initial_weight = theme.weight
    theme.adapt_weight(0.8)
    assert theme.weight > initial_weight
    
    # Testa seleção de narrativa
    narrative = theme.get_narrative(CulturalBehavior.AGGRESSIVE)
    assert "atac" in narrative.lower()

def test_piece_identity_adaptation():
    """Testa adaptação de identidade cultural de peça"""
    identity = PieceCulturalIdentity(
        name="Test Piece",
        description="Test Description",
        piece_type=PieceType.KING,
        cultural_value=1.0
    )
    
    # Testa adaptação de comportamento
    initial_pref = identity.behavior_preferences[CulturalBehavior.AGGRESSIVE]
    identity.adapt_behavior(CulturalBehavior.AGGRESSIVE, 0.8)
    assert identity.behavior_preferences[CulturalBehavior.AGGRESSIVE] > initial_pref

def test_culture_evolution():
    """Testa evolução cultural completa"""
    culture = ChessCulture(
        name="Test Culture",
        description="Test Description",
        themes={
            "Test Theme": CulturalTheme(
                name="Test Theme",
                description="Test Description",
                weight=0.5,
                narratives=[
                    "Avança para atacar o inimigo",
                    "Defende sua posição com vigor",
                    "Planeja sua estratégia com cuidado"
                ]
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Test King",
                description="Test Description",
                piece_type=PieceType.KING,
                cultural_value=1.0
            )
        }
    )
    
    # Testa registro de movimento
    context = {'under_attack': True, 'material_advantage': 1}
    culture.record_move_outcome(PieceType.KING, context, 0.8)
    
    # Verifica evolução
    status = culture.get_evolution_status()
    assert status['summary']['success_rate'] > 0
    assert 'piece_behaviors' in status
    assert 'theme_weights' in status
    
    # Testa narrativa cultural
    narrative = culture.get_cultural_narrative(PieceType.KING, context)
    assert "Test King" in narrative

def test_behavioral_consistency():
    """Testa consistência de comportamentos ao longo do tempo"""
    evolution = CulturalEvolution()
    context = {'under_attack': True, 'material_advantage': 0}
    
    # Registra série de resultados positivos para comportamento defensivo
    for _ in range(5):
        behavior = evolution.evaluate_context(context)
        evolution.record_outcome(behavior, 0.9, context)
    
    # Verifica se o comportamento se mantém consistente
    dominant = evolution.get_dominant_behavior()
    for _ in range(3):
        new_behavior = evolution.evaluate_context(context)
        assert new_behavior == dominant

def test_cultural_adaptation_to_success():
    """Testa adaptação cultural baseada em sucesso"""
    culture = ChessCulture(
        name="Test Culture",
        description="Test Description",
        themes={
            "Test Theme": CulturalTheme(
                name="Test Theme",
                description="Test Description",
                weight=0.5,
                narratives=[
                    "Avança para atacar o inimigo",
                    "Defende sua posição com vigor",
                    "Planeja sua estratégia com cuidado"
                ]
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Test King",
                description="Test Description",
                piece_type=PieceType.KING,
                cultural_value=1.0
            )
        }
    )
    
    # Simula série de movimentos bem-sucedidos
    context = {'under_attack': False, 'material_advantage': 2}
    for _ in range(5):
        culture.record_move_outcome(PieceType.KING, context, 0.9)
    
    # Verifica adaptação
    status = culture.get_evolution_status()
    assert status['summary']['success_rate'] > 0.8
    assert status['summary']['cultural_coherence'] > 0.5

def test_narrative_evolution():
    """Testa evolução das narrativas culturais"""
    culture = ChessCulture(
        name="Test Culture",
        description="Test Description",
        themes={
            "Test Theme": CulturalTheme(
                name="Test Theme",
                description="Test Description",
                weight=0.5,
                narratives=[
                    "Avança para atacar o inimigo",
                    "Defende sua posição com vigor",
                    "Planeja sua estratégia com cuidado"
                ]
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Test King",
                description="Test Description",
                piece_type=PieceType.KING,
                cultural_value=1.0
            )
        }
    )
    
    # Registra sucesso em comportamento agressivo
    context = {'material_advantage': 2, 'opponent_king_exposed': True}
    for _ in range(5):
        culture.record_move_outcome(PieceType.KING, context, 0.9)
    
    # Verifica se as narrativas refletem o comportamento bem-sucedido
    narrative = culture.get_cultural_narrative(PieceType.KING, context)
    assert any(word in narrative.lower() for word in ['atac', 'avanç', 'domin'])
