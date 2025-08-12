"""
AEON Chess - Samurai Culture
Auto-generated culture implementation
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from ..base_culture import BaseCulture, CulturalTrait

@dataclass
class SamuraiCulture(BaseCulture):
    """Implementação da cultura Samurai"""
    
    def __init__(self):
        super().__init__(
            name="Samurai",
            description="Cultura japonesa baseada em honra, disciplina e estratégia refinada"
        )
        
        # Características culturais
        self.traits = {
            "honor": 0.9,
            "discipline": 0.95,
            "aggression": 0.6,
            "patience": 0.9,
            "tactical": 0.8,
            "positional": 0.85
        }
        
        # Estilo de jogo
        self.play_style = {
            "opening_preference": "conservative",
            "midgame_focus": "positional",
            "endgame_strength": "technique",
            "risk_tolerance": 0.4,
            "sacrifice_willingness": 0.7
        }
        
        # Configuração de peças
        self.pieces_config = {
            "king": {"model": "emperor", "special": "bushido_defense"},
            "queen": {"model": "shogun", "special": "strategic_vision"},
            "bishop": {"model": "monk", "special": "distant_wisdom"},
            "knight": {"model": "samurai", "special": "honor_leap"},
            "rook": {"model": "castle", "special": "fortress_power"},
            "pawn": {"model": "ashigaru", "special": "loyal_advance"}
        }
        
        # Narrativas contextuais
        self.narratives = {
            "opening": ["O mestre samurai contempla o campo de batalha com serenidade...", "Com a disciplina de mil anos, a primeira jogada é executada...", "O bushido guia cada movimento, honra acima da vitória..."],
            "midgame": ["A estratégia samurai se revela, cada peça em harmonia...", "Como folhas de cerejeira ao vento, as peças dançam em formação...", "A paciência do guerreiro aguarda o momento perfeito..."],
            "endgame": ["Com precisão cirúrgica, o samurai finaliza com honra...", "A técnica ancestral se manifesta nos movimentos finais...", "Vitória com dignidade, derrota com honor - o caminho samurai..."]
        }
        
        # Configuração visual
        self.theme = {
            "colors": {
                "primary": "#8B0000",
                "secondary": "#FFD700",
                "accent": "#000000"
            },
            "audio": {
                "ambient": "japanese_garden.mp3",
                "move_sound": "bamboo_strike.wav",
                "capture": "katana_slash.wav"
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
samurai_culture = SamuraiCulture()

def get_culture():
    """Retorna a instância da cultura Samurai"""
    return samurai_culture
