from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from core.board.board import Piece, PieceType, Color
from cultural.culture_framework import ChessCulture

@dataclass
class CulturalEventTrigger:
    """Define quando um evento cultural deve ser ativado"""
    name: str
    description: str
    conditions: Dict[str, any]  # Ex: {"piece_type": PieceType.KING, "position": "e4"}
    weight: float = 1.0

@dataclass
class CulturalEvent:
    """Define um evento cultural especial"""
    name: str
    description: str
    trigger: CulturalEventTrigger
    cultural_impact: float
    narratives: List[str]
    bonuses: Dict[str, float] = field(default_factory=dict)

class CulturalEventSystem:
    """Sistema para gerenciar eventos culturais especiais"""
    
    def __init__(self):
        self.events = self._init_events()
        self.active_events = []
        self.event_history = []
        
    def _init_events(self) -> Dict[str, Dict[str, CulturalEvent]]:
        """Inicializa eventos culturais para cada cultura"""
        return {
            "persian": {
                "silk_road": CulturalEvent(
                    name="Rota da Seda",
                    description="Conexão das rotas comerciais",
                    trigger=CulturalEventTrigger(
                        name="diagonal_control",
                        description="Controle de uma diagonal principal",
                        conditions={"diagonal_control": True}
                    ),
                    cultural_impact=0.8,
                    narratives=[
                        "As rotas comerciais se abrem como a Rota da Seda",
                        "O comércio floresce através das terras persas",
                        "As caravanas estabelecem novas conexões"
                    ],
                    bonuses={"mobility": 1.2, "influence": 1.1}
                ),
                "immortal_guard": CulturalEvent(
                    name="Guarda Imortal",
                    description="Formação da elite persa",
                    trigger=CulturalEventTrigger(
                        name="pawn_formation",
                        description="Formação específica de peões",
                        conditions={"pawns_aligned": 3}
                    ),
                    cultural_impact=0.9,
                    narratives=[
                        "Os Imortais formam sua linha de batalha",
                        "A guarda de elite assume sua posição",
                        "A formação persa intimida seus inimigos"
                    ],
                    bonuses={"defense": 1.3, "morale": 1.2}
                )
            },
            "mongol": {
                "cavalry_charge": CulturalEvent(
                    name="Carga da Cavalaria",
                    description="Ataque coordenado da cavalaria mongol",
                    trigger=CulturalEventTrigger(
                        name="knight_coordination",
                        description="Cavalos em posição de ataque",
                        conditions={"knights_attacking": 2}
                    ),
                    cultural_impact=0.9,
                    narratives=[
                        "A cavalaria mongol inicia sua carga devastadora",
                        "Os arqueiros montados coordenam seu ataque",
                        "O trovão dos cascos ecoa pelo campo de batalha"
                    ],
                    bonuses={"attack": 1.4, "mobility": 1.3}
                ),
                "tribal_unity": CulturalEvent(
                    name="União Tribal",
                    description="Unificação das tribos mongóis",
                    trigger=CulturalEventTrigger(
                        name="piece_coordination",
                        description="Peças em formação de suporte",
                        conditions={"pieces_supporting": 3}
                    ),
                    cultural_impact=0.8,
                    narratives=[
                        "As tribos se unem sob a bandeira do Khan",
                        "A força da união mongol se manifesta",
                        "Como um só povo, os mongóis avançam"
                    ],
                    bonuses={"coordination": 1.3, "morale": 1.2}
                )
            },
            "chinese": {
                "heavenly_mandate": CulturalEvent(
                    name="Mandato Celestial",
                    description="Manifestação do poder imperial",
                    trigger=CulturalEventTrigger(
                        name="king_position",
                        description="Rei em posição de poder",
                        conditions={"king_protected": True, "center_control": True}
                    ),
                    cultural_impact=1.0,
                    narratives=[
                        "O Mandato do Céu se manifesta através do Imperador",
                        "A harmonia celestial favorece o Filho do Céu",
                        "O poder imperial resplandece sobre o reino"
                    ],
                    bonuses={"authority": 1.5, "influence": 1.3}
                ),
                "silk_army": CulturalEvent(
                    name="Exército de Seda",
                    description="Formação militar refinada",
                    trigger=CulturalEventTrigger(
                        name="piece_formation",
                        description="Formação militar clássica",
                        conditions={"formation_complete": True}
                    ),
                    cultural_impact=0.8,
                    narratives=[
                        "O exército se move com a fluidez da seda",
                        "A formação militar reflete a harmonia celestial",
                        "Como ensinou Sun Tzu, a vitória vem da ordem"
                    ],
                    bonuses={"coordination": 1.2, "discipline": 1.3}
                )
            }
        }
    
    def check_event_triggers(self, board_state: Dict, culture: ChessCulture) -> List[CulturalEvent]:
        """Verifica se algum evento cultural deve ser ativado"""
        triggered_events = []
        culture_events = self.events.get(culture.name.lower().split()[0], {})
        
        for event in culture_events.values():
            if self._check_conditions(event.trigger.conditions, board_state):
                triggered_events.append(event)
                
        return triggered_events
    
    def _check_conditions(self, conditions: Dict, board_state: Dict) -> bool:
        """Verifica se as condições para um evento foram satisfeitas"""
        for condition, value in conditions.items():
            if condition == "diagonal_control":
                if not self._check_diagonal_control(board_state):
                    return False
            elif condition == "pawns_aligned":
                if not self._check_pawn_formation(board_state, value):
                    return False
            elif condition == "knights_attacking":
                if not self._check_knight_coordination(board_state, value):
                    return False
            elif condition == "pieces_supporting":
                if not self._check_piece_support(board_state, value):
                    return False
            elif condition == "king_protected":
                if not self._check_king_protection(board_state):
                    return False
            elif condition == "center_control":
                if not self._check_center_control(board_state):
                    return False
            elif condition == "formation_complete":
                if not self._check_formation(board_state):
                    return False
        return True
    
    def _check_diagonal_control(self, board_state: Dict) -> bool:
        """Verifica controle de diagonal"""
        # Implementação específica para verificar controle de diagonal
        return True  # Simplificado para exemplo
    
    def _check_pawn_formation(self, board_state: Dict, num_pawns: int) -> bool:
        """Verifica formação de peões"""
        # Implementação específica para verificar formação de peões
        return True  # Simplificado para exemplo
    
    def _check_knight_coordination(self, board_state: Dict, num_knights: int) -> bool:
        """Verifica coordenação de cavalos"""
        # Implementação específica para verificar coordenação de cavalos
        return True  # Simplificado para exemplo
    
    def _check_piece_support(self, board_state: Dict, num_pieces: int) -> bool:
        """Verifica suporte entre peças"""
        # Implementação específica para verificar suporte entre peças
        return True  # Simplificado para exemplo
    
    def _check_king_protection(self, board_state: Dict) -> bool:
        """Verifica proteção do rei"""
        # Implementação específica para verificar proteção do rei
        return True  # Simplificado para exemplo
    
    def _check_center_control(self, board_state: Dict) -> bool:
        """Verifica controle do centro"""
        # Implementação específica para verificar controle do centro
        return True  # Simplificado para exemplo
    
    def _check_formation(self, board_state: Dict) -> bool:
        """Verifica formação militar completa"""
        # Implementação específica para verificar formação militar
        return True  # Simplificado para exemplo
    
    def apply_event_effects(self, event: CulturalEvent, game_state: Dict) -> Dict:
        """Aplica os efeitos de um evento cultural"""
        effects = game_state.copy()
        
        for bonus_type, multiplier in event.bonuses.items():
            if bonus_type in effects:
                effects[bonus_type] *= multiplier
            else:
                effects[bonus_type] = multiplier
        
        self.active_events.append(event)
        self.event_history.append((len(self.event_history) + 1, event))
        
        return effects
    
    def get_event_narrative(self, event: CulturalEvent) -> str:
        """Retorna uma narrativa para o evento cultural"""
        return random.choice(event.narratives)
