"""
AEON Chess - Persa Culture
Auto-generated culture implementation
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from ..base_culture import BaseCulture, CulturalTrait

@dataclass
class PersaCulture(BaseCulture):
    """Implementação da cultura Persa"""
    
    def __init__(self):
        super().__init__(
            name="Persa",
            description="Cultura persa baseada em estratégia elaborada, elegância e sofisticação"
        )
        
        # Características culturais
        self.traits = {
            "honor": 0.8,
            "discipline": 0.8,
            "aggression": 0.65,
            "patience": 0.85,
            "tactical": 0.75,
            "positional": 0.9
        }
        
        # Estilo de jogo
        self.play_style = {
            "opening_preference": "classical",
            "midgame_focus": "strategic",
            "endgame_strength": "calculation",
            "risk_tolerance": 0.5,
            "sacrifice_willingness": 0.6
        }
        
        # Configuração de peças
        self.pieces_config = {
            "king": {"model": "shah", "special": "royal_decree"},
            "queen": {"model": "vizier", "special": "court_intrigue"},
            "bishop": {"model": "mage", "special": "arcane_sight"},
            "knight": {"model": "immortal", "special": "elite_strike"},
            "rook": {"model": "citadel", "special": "empire_strength"},
            "pawn": {"model": "soldier", "special": "disciplined_march"}
        }
        
        # Narrativas contextuais
        self.narratives = {
            "opening": ["O xá contempla seu império no tabuleiro de mármore...", "Com a sabedoria de Cyrus, a partida se inicia...", "As pétalas de rosa marcam o início da dança estratégica..."],
            "midgame": ["A complexa teia persa se desenvolve elegantemente...", "Como um jardim de Isfahan, cada peça tem seu lugar...", "A paciência do deserto aguarda o momento certo..."],
            "endgame": ["Com a precisão de um relojoeiro, a vitória se aproxima...", "A geometria sagrada se revela nos movimentos finais...", "Elegância e eficiência coroam o triunfo persa..."]
        }
        
        # Configuração visual
        self.theme = {
            "colors": {
                "primary": "#800080",
                "secondary": "#FFD700",
                "accent": "#228B22"
            },
            "audio": {
                "ambient": "persian_garden.mp3",
                "move_sound": "silk_rustle.wav",
                "capture": "scimitar_ring.wav"
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
persian_culture = PersaCulture()

def get_culture():
    """Retorna a instância da cultura Persa"""
    return persian_culture
