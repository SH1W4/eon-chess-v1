from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable
from enum import Enum, auto
import random

class CulturalBehavior(Enum):
    """Comportamentos culturais possíveis"""
    AGGRESSIVE = auto()
    DEFENSIVE = auto()
    STRATEGIC = auto()
    DIPLOMATIC = auto()
    
    @classmethod
    def get_keywords(cls) -> Dict['CulturalBehavior', List[str]]:
        """Retorna palavras-chave associadas a cada comportamento"""
        return {
            cls.AGGRESSIVE: ['ataque', 'conquista', 'domina', 'avança', 'subjuga'],
            cls.DEFENSIVE: ['protege', 'defende', 'resguarda', 'fortalece', 'mantém'],
            cls.STRATEGIC: ['planeja', 'posiciona', 'controla', 'calcula', 'prevê'],
            cls.DIPLOMATIC: ['influencia', 'negocia', 'estabelece', 'harmoniza', 'media']
        }

@dataclass
class DecisionNode:
    """Nó da árvore de decisão cultural"""
    condition: Callable[[Dict[str, Any]], bool]
    behavior: CulturalBehavior
    weight: float = 1.0
    children: List['DecisionNode'] = field(default_factory=list)
    adaptation_rate: float = 0.1
    
    def adapt(self, success_rate: float):
        """Adapta o peso do nó baseado no sucesso"""
        # Ajuste mais agressivo para comportamentos bem-sucedidos
        adaptation_factor = 2.0 if success_rate > 0.7 else 1.0
        self.weight += (self.adaptation_rate * adaptation_factor) * (success_rate - 0.4)
        self.weight = max(0.2, min(3.0, self.weight))  # Limites mais amplos
        
        # Propaga a adaptação para os filhos com menor decaimento
        for child in self.children:
            child.adapt(success_rate * 0.95)  # Efeito reduzido mais suave
            
    def evaluate(self, context: Dict[str, Any]) -> CulturalBehavior:
        """Avalia o contexto e retorna o comportamento mais apropriado.
        Regra: determinístico e estável. Se o nó atual atende, procura o primeiro
        filho (em ordem de declaração) que também atende e avalia recursivamente.
        Isso garante previsibilidade para cenários de teste e priorização explícita.
        """
        if not self.condition(context):
            return self.behavior

        for child in self.children:
            if child.condition(context):
                return child.evaluate(context)

        return self.behavior

class AdaptiveDecisionTree:
    """Árvore de decisão adaptativa para comportamentos culturais"""
    def __init__(self):
        self.root = self._create_base_tree()
        
    def _create_base_tree(self) -> DecisionNode:
        """Cria a estrutura base da árvore de decisão"""
        return DecisionNode(
            condition=lambda ctx: True,  # Root sempre avalia
            behavior=CulturalBehavior.STRATEGIC,  # Comportamento padrão
            children=[
            # Situações de ataque/defesa
                DecisionNode(
                    condition=lambda ctx: ctx.get('under_attack', False),
                    behavior=CulturalBehavior.DEFENSIVE,
                    weight=2.0,  # Peso maior para defesa quando sob ataque
                    children=[
                        DecisionNode(
                            condition=lambda ctx: ctx.get('material_advantage', 0) > 2,
                            behavior=CulturalBehavior.AGGRESSIVE,
                            weight=1.5
                        )
                    ]
                ),
                # Situações de vantagem
                DecisionNode(
                    condition=lambda ctx: ctx.get('material_advantage', 0) > 1,
                    behavior=CulturalBehavior.AGGRESSIVE,
                    children=[
                        DecisionNode(
                            condition=lambda ctx: ctx.get('opponent_king_exposed', False),
                            behavior=CulturalBehavior.AGGRESSIVE
                        )
                    ]
                ),
                # Situações de desenvolvimento
                DecisionNode(
                    condition=lambda ctx: ctx.get('early_game', True),
                    behavior=CulturalBehavior.STRATEGIC,
                    children=[
                        DecisionNode(
                            condition=lambda ctx: ctx.get('center_control', 0) < 0.3,
                            behavior=CulturalBehavior.STRATEGIC
                        )
                    ]
                ),
                # Situações diplomáticas
                DecisionNode(
                    condition=lambda ctx: ctx.get('equal_position', True),
                    behavior=CulturalBehavior.DIPLOMATIC,
                    children=[
                        DecisionNode(
                            condition=lambda ctx: ctx.get('piece_coordination', 0) < 0.5,
                            behavior=CulturalBehavior.STRATEGIC
                        )
                    ]
                )
            ]
        )
        
    def decide(self, context: Dict[str, Any]) -> CulturalBehavior:
        """Decide o comportamento baseado no contexto atual"""
        return self.root.evaluate(context)
        
    def adapt(self, success_rate: float):
        """Adapta a árvore baseado no sucesso da última decisão"""
        self.root.adapt(success_rate)
        
    def get_behavior_weights(self) -> Dict[CulturalBehavior, float]:
        """Retorna os pesos atuais para cada comportamento"""
        weights = {behavior: 0.0 for behavior in CulturalBehavior}
        
        def accumulate_weights(node: DecisionNode, depth: int = 0):
            weight_factor = 1.0 / (depth + 1)  # Pesos diminuem com a profundidade
            weights[node.behavior] += node.weight * weight_factor
            for child in node.children:
                accumulate_weights(child, depth + 1)
                
        accumulate_weights(self.root)
        return weights
