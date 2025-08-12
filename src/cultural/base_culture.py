"""
AEON Chess - Base Culture Class
Classe base para todas as implementações culturais
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class CulturalTrait(Enum):
    """Enumeration of cultural traits"""
    HONOR = "honor"
    DISCIPLINE = "discipline"
    AGGRESSION = "aggression"
    PATIENCE = "patience"
    TACTICAL = "tactical"
    POSITIONAL = "positional"

@dataclass
class BaseCulture:
    """Base class for all cultural implementations"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.traits: Dict[str, float] = {}
        self.play_style: Dict[str, Any] = {}
        self.pieces_config: Dict[str, Dict[str, str]] = {}
        self.narratives: Dict[str, List[str]] = {}
        self.theme: Dict[str, Any] = {}
    
    def get_trait_value(self, trait: str) -> float:
        """Get the value of a specific trait"""
        return self.traits.get(trait, 0.5)
    
    def get_opening_move_weight(self, move: str) -> float:
        """Calculate cultural weight for an opening move"""
        return 1.0
    
    def get_position_evaluation_bonus(self, position_type: str) -> float:
        """Get evaluation bonus for position type"""
        return 0.0
    
    def get_narrative_for_context(self, context: str) -> str:
        """Get narrative text for game context"""
        return "Move executed."
    
    def adapt_to_opponent_style(self, opponent_aggression: float) -> Dict[str, float]:
        """Adapt playing style based on opponent"""
        return {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert culture to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "traits": self.traits,
            "play_style": self.play_style,
            "pieces_config": self.pieces_config,
            "narratives": self.narratives,
            "theme": self.theme
        }
