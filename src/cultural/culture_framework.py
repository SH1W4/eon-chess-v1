from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from core.board.board import PieceType
from .adaptive_decision import CulturalBehavior, AdaptiveDecisionTree
from .cultural_evolution import CulturalEvolution, EvolutionMetrics
import random

@dataclass
class CulturalTheme:
    """Define um tema cultural específico com capacidade adaptativa"""
    name: str
    description: str
    weight: float
    narratives: List[str]
    historical_context: Optional[str] = None
    behavior_preferences: Dict[CulturalBehavior, float] = field(default_factory=lambda: {
        b: 1.0 for b in CulturalBehavior
    })
    
    def adapt_weight(self, performance: float):
        """Adapta o peso do tema baseado no desempenho"""
        self.weight += 0.1 * (performance - 0.5)
        self.weight = max(0.1, min(1.0, self.weight))
        
    def get_narrative(self, behavior: CulturalBehavior) -> str:
        """Retorna uma narrativa apropriada para o comportamento"""
        relevant = [n for n in self.narratives 
                   if any(k in n.lower() for k in CulturalBehavior.get_keywords()[behavior])]
        return random.choice(relevant) if relevant else random.choice(self.narratives)
    
@dataclass
class PieceCulturalIdentity:
    """Define a identidade cultural de uma peça com comportamento adaptativo"""
    name: str
    description: str
    piece_type: PieceType
    cultural_value: float
    special_moves: List[str] = field(default_factory=list)
    historical_significance: Optional[str] = None
    behavior_preferences: Dict[CulturalBehavior, float] = field(default_factory=lambda: {
        b: 1.0 for b in CulturalBehavior
    })
    
    def adapt_behavior(self, behavior: CulturalBehavior, success_rate: float):
        """Adapta as preferências comportamentais baseado no sucesso"""
        current = self.behavior_preferences.get(behavior, 1.0)
        self.behavior_preferences[behavior] = current + 0.1 * (success_rate - 0.5)
        self.behavior_preferences[behavior] = max(0.1, min(2.0, self.behavior_preferences[behavior]))

@dataclass
class ChessCulture:
    """Define uma cultura completa de xadrez com capacidade evolutiva"""
    name: str
    description: str
    themes: Dict[str, CulturalTheme]
    piece_identities: Dict[PieceType, PieceCulturalIdentity]
    historical_period: Optional[str] = None
    evolution_system: CulturalEvolution = field(default_factory=CulturalEvolution)
    
    def __post_init__(self):
        """Inicialização após criação"""
        if not hasattr(self, 'evolution_system'):
            self.evolution_system = CulturalEvolution()
    
    def get_piece_name(self, piece_type: PieceType) -> str:
        """Retorna o nome cultural de uma peça"""
        identity = self.piece_identities.get(piece_type)
        return identity.name if identity else 'Unknown'
    
    def get_theme_narratives(self, theme_name: str) -> List[str]:
        """Retorna as narrativas de um tema específico"""
        theme = self.themes.get(theme_name)
        if not theme:
            return []
        
        # Adapta narrativas baseado no comportamento dominante
        dominant_behavior = self.evolution_system.get_dominant_behavior()
        return [theme.get_narrative(dominant_behavior)]
    
    def calculate_cultural_weight(self, piece_type: PieceType, context: Dict[str, Any]) -> float:
        """Calcula o peso cultural de uma peça baseado no contexto e evolução"""
        identity = self.piece_identities.get(piece_type)
        if not identity:
            return 1.0
            
        # Avalia comportamento apropriado para o contexto
        behavior = self.evolution_system.evaluate_context(context)
        
        # Calcula peso base
        base_value = identity.cultural_value
        
        # Fatores contextuais
        if context.get('in_check', False) and piece_type == PieceType.KING:
            base_value *= 1.5
        if context.get('promotion_available', False) and piece_type == PieceType.PAWN:
            base_value *= 1.3
        if context.get('pieces_captured', 0) > 0:
            base_value *= 1.1
            
        # Modificador comportamental
        behavior_modifier = identity.behavior_preferences.get(behavior, 1.0)
        
        # Influência da evolução cultural
        evolution_metrics = self.evolution_system.get_evolution_summary()
        cultural_modifier = evolution_metrics['cultural_coherence']
        
        return base_value * behavior_modifier * cultural_modifier
    
    def record_move_outcome(self, piece_type: PieceType, context: Dict[str, Any], 
                          success_rate: float):
        """Registra o resultado de um movimento para evolução"""
        # Determina o comportamento usado
        behavior = self.evolution_system.evaluate_context(context)
        
        # Registra o resultado
        self.evolution_system.record_outcome(behavior, success_rate, context)
        
        # Adapta a identidade da peça
        identity = self.piece_identities.get(piece_type)
        if identity:
            identity.adapt_behavior(behavior, success_rate)
            
        # Adapta os temas relevantes
        for theme in self.themes.values():
            theme.adapt_weight(success_rate)
    
    def get_cultural_narrative(self, piece_type: PieceType, context: Dict[str, Any]) -> str:
        """Gera uma narrativa cultural para a situação atual"""
        behavior = self.evolution_system.evaluate_context(context)
        base_narrative = self.evolution_system.get_behavior_narrative(behavior)
        
        identity = self.piece_identities.get(piece_type)
        if identity:
            return f"{identity.name} {base_narrative}"
        return base_narrative
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Retorna o status atual da evolução cultural"""
        return {
            'summary': self.evolution_system.get_evolution_summary(),
            'piece_behaviors': {
                piece_type.name: {
                    'name': identity.name,
                    'preferences': dict(identity.behavior_preferences)
                }
                for piece_type, identity in self.piece_identities.items()
            },
            'theme_weights': {
                theme.name: theme.weight for theme in self.themes.values()
            }
        }

# Define a cultura Bizantina
byzantine_culture = ChessCulture(
    name="Império Bizantino",
    description="A cultura do Império Romano do Oriente, rica em tradição e cerimônia",
    historical_period="330-1453 D.C.",
    themes={
        "Estratégia Imperial": CulturalTheme(
            name="Estratégia Imperial",
            description="A arte da guerra bizantina, focada em táticas sofisticadas",
            weight=0.8,
            narratives=[
                "Como um estrategista bizantino, {piece} avança com precisão imperial",
                "Com a astúcia de um general bizantino, {piece} domina a posição",
                "Seguindo a tradição militar do império, {piece} executa uma manobra decisiva"
            ],
            historical_context="Baseado nos tratados militares bizantinos como o Strategikon"
        ),
        "Diplomacia Bizantina": CulturalTheme(
            name="Diplomacia Bizantina",
            description="A sutil arte da diplomacia e influência",
            weight=0.7,
            narratives=[
                "Em um movimento diplomático, {piece} estabelece sua influência",
                "Com a sutileza da corte bizantina, {piece} negocia sua posição",
                "Através de manobras políticas, {piece} assegura sua vantagem"
            ],
            historical_context="Reflete as complexas relações diplomáticas do império"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Basileus",
            description="O imperador bizantino, líder supremo do império",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="Título do imperador bizantino, sucessor dos césares romanos"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Augusta",
            description="A imperatriz, detentora de poder e influência",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Título da imperatriz bizantina"
        )
    }
)

# Define a cultura Viking
viking_culture = ChessCulture(
    name="Nórdico Viking",
    description="A cultura dos navegadores e guerreiros do norte",
    historical_period="793-1066 D.C.",
    themes={
        "Bravura Nórdica": CulturalTheme(
            name="Bravura Nórdica",
            description="A coragem e força dos guerreiros vikings",
            weight=0.8,
            narratives=[
                "Com a força dos Vikings, {piece} avança sem medo",
                "Como um guerreiro nórdico, {piece} desafia seus inimigos",
                "Honrando a tradição viking, {piece} busca glória em batalha"
            ],
            historical_context="Baseado nas sagas nórdicas e na cultura guerreira viking"
        ),
        "Batalha Naval": CulturalTheme(
            name="Batalha Naval",
            description="A maestria viking na navegação e batalhas marítimas",
            weight=0.7,
            narratives=[
                "Como um navegante viking, {piece} conquista novo território",
                "Com a destreza de um capitão nórdico, {piece} traça seu curso",
                "Seguindo as rotas dos drakkar, {piece} explora novos horizontes"
            ],
            historical_context="Reflete a importância dos navios e navegação na sociedade viking"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Jarl",
            description="O líder viking, comandante de guerreiros",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="Título dos líderes vikings e nobres escandinavos"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Valquíria",
            description="A poderosa guerreira mítica",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Baseado nas valquírias da mitologia nórdica"
        )
    }
)
