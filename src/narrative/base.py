"""
Módulo base para o sistema narrativo de xadrez.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml
import os

@dataclass
class NarrativeConfig:
    """Configuração do sistema narrativo."""
    version: str
    engine: str
    cultures: Dict[str, Dict]

@dataclass 
class ChessPattern:
    """Representa um padrão identificado no jogo."""
    name: str
    type: str  # tactical ou strategic
    description: str
    significance: float  # 0.0 a 1.0

@dataclass
class GameState:
    """Estado atual do jogo para contextualização."""
    phase: str  # opening, middlegame, endgame
    move_number: int
    white_advantage: float
    patterns: List[ChessPattern]
    last_move: Optional[str]

class BaseNarrative:
    """Classe base para narrativa do xadrez."""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.current_culture = None
        self.culture_config = None
    
    def _load_config(self, path: str) -> NarrativeConfig:
        """Carrega configuração do arquivo YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return NarrativeConfig(**data['chess_narrative'])
    
    def set_culture(self, culture: str) -> None:
        """Define a cultura atual para narrativa."""
        if culture not in self.config.cultures:
            raise ValueError(f"Cultura '{culture}' não encontrada")
        
        self.current_culture = culture
        self.culture_config = self.config.cultures[culture]
    
    def get_piece_description(self, piece: str) -> str:
        """Retorna descrição culturalmente apropriada da peça."""
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        piece_config = self.culture_config['piece_descriptions'].get(piece.lower())
        if not piece_config:
            return piece
        
        return piece_config['name']
    
    def get_move_template(self, move_type: str) -> str:
        """Retorna template narrativo para tipo de movimento."""
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        templates = self.culture_config['narrative_templates'][move_type]
        if not templates:
            return "{piece} move to {square}"
        
        import random
        return random.choice(templates)
