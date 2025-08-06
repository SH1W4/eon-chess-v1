from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import random
from core.board.board import PieceType
from .adaptive_decision import CulturalBehavior, AdaptiveDecisionTree

@dataclass
class EvolutionMetrics:
    """Métricas de evolução cultural"""
    success_rate: float = 0.0
    behavior_distribution: Dict[CulturalBehavior, float] = field(default_factory=dict)
    adaptation_score: float = 0.0
    cultural_coherence: float = 1.0
    
    def update(self, success: float, behavior: CulturalBehavior):
        """Atualiza as métricas com novos dados"""
        # Atualiza taxa de sucesso com média móvel ponderada por recência
        self.success_rate = 0.3 * self.success_rate + 0.7 * success
        
        # Atualiza distribuição de comportamentos com peso por sucesso
        weight = 1.0 + success  # Comportamentos bem-sucedidos têm mais peso
        if behavior in self.behavior_distribution:
            self.behavior_distribution[behavior] += weight
        else:
            self.behavior_distribution[behavior] = weight

        # Normaliza a distribuição
        total = sum(self.behavior_distribution.values())
        if total > 0:
            for b in self.behavior_distribution:
                self.behavior_distribution[b] = self.behavior_distribution[b] / total
            
        # Calcula score de adaptação
        self.adaptation_score = self.success_rate * max(self.behavior_distribution.values())
        
        # Atualiza coerência cultural
        # Calcula entropia comportamental para coerência
        behavior_probs = list(self.behavior_distribution.values())
        if len(behavior_probs) > 0:
            behavior_entropy = -sum(p * p for p in behavior_probs if p > 0.01)
            self.cultural_coherence = 1.0 / (1.0 + abs(behavior_entropy))
        else:
            self.cultural_coherence = 1.0

@dataclass
class CulturalEvolution:
    """Sistema de evolução cultural"""
    decision_tree: AdaptiveDecisionTree = field(default_factory=AdaptiveDecisionTree)
    metrics: EvolutionMetrics = field(default_factory=EvolutionMetrics)
    history: List[Dict[str, Any]] = field(default_factory=list)
    learning_rate: float = 0.1
    
    def evaluate_context(self, context: Dict[str, Any]) -> CulturalBehavior:
        """Avalia o contexto atual e retorna o comportamento mais apropriado"""
        return self.decision_tree.decide(context)
    
    def record_outcome(self, behavior: CulturalBehavior, success_rate: float, context: Dict[str, Any]):
        """Registra o resultado de uma decisão e adapta o sistema"""
        # Atualiza métricas
        self.metrics.update(success_rate, behavior)
        
        # Adapta a árvore de decisão
        self.decision_tree.adapt(success_rate)
        
        # Registra no histórico
        self.history.append({
            'behavior': behavior,
            'success_rate': success_rate,
            'context': context.copy(),
            'metrics': {
                'success_rate': self.metrics.success_rate,
                'adaptation_score': self.metrics.adaptation_score,
                'coherence': self.metrics.cultural_coherence
            }
        })
        
    def get_dominant_behavior(self) -> CulturalBehavior:
        """Retorna o comportamento mais bem-sucedido"""
        weights = self.decision_tree.get_behavior_weights()
        return max(weights.items(), key=lambda x: x[1])[0]
    
    def get_behavior_narrative(self, behavior: CulturalBehavior) -> str:
        """Gera uma narrativa para o comportamento"""
        success_rate = self.metrics.success_rate
        coherence = self.metrics.cultural_coherence
        
        narratives = {
            CulturalBehavior.AGGRESSIVE: [
                "Busca dominação total do tabuleiro",
                "Avança sem hesitação contra o inimigo",
                "Prioriza ataques diretos e conquistas"
            ],
            CulturalBehavior.DEFENSIVE: [
                "Mantém posições fortificadas",
                "Protege recursos estratégicos",
                "Prioriza segurança e estabilidade"
            ],
            CulturalBehavior.STRATEGIC: [
                "Planeja movimentos com precisão",
                "Controla pontos-chave do tabuleiro",
                "Desenvolve posições com paciência"
            ],
            CulturalBehavior.DIPLOMATIC: [
                "Busca equilíbrio nas trocas",
                "Estabelece presença sem confrontos",
                "Mantém flexibilidade posicional"
            ]
        }
        
        base_narrative = random.choice(narratives[behavior])
        
        if success_rate > 0.7:
            return f"{base_narrative}, com grande eficácia"
        elif success_rate < 0.3:
            return f"{base_narrative}, buscando adaptação"
        else:
            return base_narrative
    
    def get_evolution_summary(self) -> Dict[str, Any]:
        """Retorna um resumo do estado evolutivo atual"""
        return {
            'dominant_behavior': self.get_dominant_behavior(),
            'success_rate': self.metrics.success_rate,
            'cultural_coherence': self.metrics.cultural_coherence,
            'behavior_distribution': dict(self.metrics.behavior_distribution),
            'adaptation_score': self.metrics.adaptation_score,
            'historical_depth': len(self.history)
        }
