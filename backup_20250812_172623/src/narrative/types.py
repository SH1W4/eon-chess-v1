# Shims para satisfazer imports dos testes
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Tipos esperados pelos testes de narrativa
@dataclass
class ChessEvent:
    type: str
    piece: str
    position: str
    timestamp: float
    intensity: float = 0.0

@dataclass
class GameContext:
    game_phase: str
    move_count: int
    material_balance: int
    time_remaining: Dict[str, float]
    position_evaluation: float
    player_style: str
    tension_level: float
    last_moves: List[str]

@dataclass
class NarrativeResponse:
    narrative: str
    metadata: Optional[Dict[str, Any]] = None

