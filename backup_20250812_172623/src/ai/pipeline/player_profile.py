"""
Perfil do jogador para IA adaptativa
"""
from dataclasses import dataclass
from typing import Dict, Optional
import json

@dataclass
class PlayerProfile:
    """
    Perfil do jogador contendo características de jogo e métricas
    """
    aggression: float = 0.5  # Nível de agressividade (0-1)
    risk_taking: float = 0.5  # Propensão a riscos (0-1)
    positional: float = 0.5  # Preferência por jogo posicional (0-1)
    wins: int = 0
    losses: int = 0
    draws: int = 0
    avg_move_time: float = 0.0  # Tempo médio por movimento em segundos
    preferred_openings: Dict[str, int] = None  # Contagem de aberturas usadas

    def __post_init__(self):
        if self.preferred_openings is None:
            self.preferred_openings = {}

    @property
    def win_rate(self) -> float:
        """Calcula taxa de vitórias"""
        total_games = self.wins + self.losses + self.draws
        return self.wins / total_games if total_games > 0 else 0.0

    def update_metrics(self, game_result: str, move_time: float, opening: str):
        """Atualiza métricas após uma partida"""
        if game_result == "win":
            self.wins += 1
        elif game_result == "loss":
            self.losses += 1
        else:
            self.draws += 1

        # Atualiza tempo médio
        total_games = self.wins + self.losses + self.draws
        self.avg_move_time = ((self.avg_move_time * (total_games - 1)) + move_time) / total_games

        # Atualiza contagem de aberturas
        self.preferred_openings[opening] = self.preferred_openings.get(opening, 0) + 1

    def adapt_style(self, opponent_profile: 'PlayerProfile'):
        """Adapta estilo baseado no oponente"""
        # Ajusta agressividade como contra-medida
        self.aggression = min(1.0, max(0.0, 1.0 - opponent_profile.aggression))
        
        # Ajusta tomada de risco baseado no histórico
        if opponent_profile.win_rate > 0.6:  # Oponente forte
            self.risk_taking = max(0.2, self.risk_taking - 0.1)  # Mais conservador
        else:
            self.risk_taking = min(0.8, self.risk_taking + 0.1)  # Mais arriscado

    def to_dict(self) -> dict:
        """Converte perfil para dicionário"""
        return {
            "aggression": self.aggression,
            "risk_taking": self.risk_taking,
            "positional": self.positional,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "avg_move_time": self.avg_move_time,
            "preferred_openings": self.preferred_openings
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProfile':
        """Cria perfil a partir de dicionário"""
        return cls(**data)

    def save_to_file(self, filepath: str):
        """Salva perfil em arquivo"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'PlayerProfile':
        """Carrega perfil de arquivo"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)
