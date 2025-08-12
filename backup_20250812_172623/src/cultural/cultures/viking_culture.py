"""
AEON Chess - Viking Culture
Auto-generated culture implementation
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from ..base_culture import BaseCulture, CulturalTrait

@dataclass
class VikingCulture(BaseCulture):
    """Implementação da cultura Viking"""
    
    def __init__(self):
        super().__init__(
            name="Viking",
            description="Cultura nórdica baseada em agressividade, exploração e coragem"
        )
        
        # Características culturais
        self.traits = {
            "honor": 0.7,
            "discipline": 0.6,
            "aggression": 0.95,
            "patience": 0.4,
            "tactical": 0.9,
            "positional": 0.5
        }
        
        # Estilo de jogo
        self.play_style = {
            "opening_preference": "aggressive",
            "midgame_focus": "tactical",
            "endgame_strength": "material",
            "risk_tolerance": 0.8,
            "sacrifice_willingness": 0.9
        }
        
        # Configuração de peças
        self.pieces_config = {
            "king": {"model": "jarl", "special": "warrior_king"},
            "queen": {"model": "valkyrie", "special": "battle_fury"},
            "bishop": {"model": "skald", "special": "saga_vision"},
            "knight": {"model": "berserker", "special": "rage_charge"},
            "rook": {"model": "longship", "special": "raid_power"},
            "pawn": {"model": "warrior", "special": "shield_wall"}
        }
        
        # Narrativas contextuais
        self.narratives = {
            "opening": ["Os vikings partem para a batalha com sede de glória...", "O rugido de guerra ecoa pelo tabuleiro gelado...", "Com a força dos ancestrais, o primeiro golpe é desferido..."],
            "midgame": ["A fúria berserker se intensifica no campo de batalha...", "Como lobos famintos, os guerreiros avançam sem medo...", "O sangue ferve com a proximidade da vitória..."],
            "endgame": ["Com a força brutal dos martelos de Thor...", "A vitória é conquistada com honra e violência...", "Valhalla aguarda os corajosos, Hel recebe os covardes..."]
        }
        
        # Configuração visual
        self.theme = {
            "colors": {
                "primary": "#4169E1",
                "secondary": "#C0C0C0",
                "accent": "#8B0000"
            },
            "audio": {
                "ambient": "nordic_winds.mp3",
                "move_sound": "axe_swing.wav",
                "capture": "shield_clash.wav"
            }
        }
    
    def get_opening_move_weight(self, move: str) -> float:
        """Retorna peso cultural para um movimento de abertura"""
        if self.play_style["opening_preference"] == "aggressive":
            # Favorece aberturas agressivas
            aggressive_moves = ["e4", "f4", "Nf3", "d4"]
            if any(am in move for am in aggressive_moves):
                return 1.2
        elif self.play_style["opening_preference"] == "conservative":
            # Favorece aberturas posicionais
            positional_moves = ["d4", "Nf3", "c4", "g3"]
            if any(pm in move for pm in positional_moves):
                return 1.2
        elif self.play_style["opening_preference"] == "classical":
            # Favorece aberturas clássicas
            classical_moves = ["e4", "d4", "Nf3", "Nc3"]
            if any(cm in move for cm in classical_moves):
                return 1.1
                
        return 1.0
    
    def get_position_evaluation_bonus(self, position_type: str) -> float:
        """Retorna bônus de avaliação baseado no tipo de posição"""
        bonuses = {
            "tactical": self.traits["tactical"] * 0.1,
            "positional": self.traits["positional"] * 0.1,
            "aggressive": self.traits["aggression"] * 0.15,
            "defensive": (1.0 - self.traits["aggression"]) * 0.1
        }
        return bonuses.get(position_type, 0.0)
    
    def get_narrative_for_context(self, context: str) -> str:
        """Retorna narrativa apropriada para o contexto"""
        import random
        narratives = self.narratives.get(context, ["Movimento executado."])
        return random.choice(narratives)
    
    def adapt_to_opponent_style(self, opponent_aggression: float) -> Dict[str, float]:
        """Adapta estilo baseado no oponente"""
        adaptation = {}
        
        if opponent_aggression > 0.7:
            # Oponente agressivo - aumentar defesa
            adaptation["patience"] = min(1.0, self.traits["patience"] + 0.1)
            adaptation["aggression"] = max(0.0, self.traits["aggression"] - 0.05)
        elif opponent_aggression < 0.4:
            # Oponente passivo - aumentar agressão
            adaptation["aggression"] = min(1.0, self.traits["aggression"] + 0.1)
            adaptation["patience"] = max(0.0, self.traits["patience"] - 0.05)
        
        return adaptation

# Instância global da cultura
viking_culture = VikingCulture()

def get_culture():
    """Retorna a instância da cultura Viking"""
    return viking_culture
