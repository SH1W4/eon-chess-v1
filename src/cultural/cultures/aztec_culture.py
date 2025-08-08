"""
Aztec cultural definitions and rules for chess gameplay.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

@dataclass
class AztecTheme:
    name: str
    description: str
    narratives: List[str]
    piece_names: Dict[str, str]
    cultural_weight: float

AZTEC_PIECES = {
    'king': 'Tlatoani',
    'queen': 'Cihuacóatl',
    'bishop': 'Sacerdote Guerreiro',
    'knight': 'Guerreiro Águia',
    'rook': 'Templo Fortificado',
    'pawn': 'Guerreiro Jaguar'
}

AZTEC_NARRATIVES = {
    'move': [
        "O {piece} avança como nas guerras floridas",
        "Seguindo os rituais sagrados, {piece} se move",
        "Com a bênção dos deuses, {piece} toma sua posição",
        "Como nas batalhas ancestrais, {piece} assume o comando"
    ],
    'capture': [
        "Um sacrifício sagrado é feito quando {piece} captura {target}",
        "Os deuses aceitam a oferenda de {target} por {piece}",
        "Na guerra florida, {piece} oferece {target} aos céus",
        "O sangue de {target} alimenta os deuses através de {piece}"
    ],
    'check': [
        "O Tlatoani está ameaçado, como previsto nos presságios",
        "Os oráculos alertam sobre o perigo ao líder supremo",
        "A ordem cósmica está em risco com o Tlatoani em perigo"
    ],
    'victory': [
        "A vitória é alcançada, e os deuses são honrados",
        "O ciclo sagrado se completa com este triunfo",
        "As profecias se cumprem nesta conquista divina"
    ]
}

CULTURAL_EVENTS = {
    'sacrificio_ritual': {
        'description': "Um sacrifício ritual fortalece o sol",
        'impact': 0.8,
        'triggers': ['capture']
    },
    'guerra_florida': {
        'description': "Uma batalha ritual honra os deuses",
        'impact': 0.7,
        'triggers': ['strategic_position']
    },
    'profecia_cumprida': {
        'description': "Os presságios dos sacerdotes se realizam",
        'impact': 0.9,
        'triggers': ['checkmate', 'victory']
    }
}

class AztecCulture:
    def __init__(self):
        self.pieces = AZTEC_PIECES
        self.narratives = AZTEC_NARRATIVES
        self.events = CULTURAL_EVENTS
        
    def get_piece_name(self, piece_type: str) -> str:
        return self.pieces.get(piece_type.lower(), piece_type)
        
    def get_narrative(self, context: str, **kwargs) -> str:
        if context not in self.narratives:
            return ""
        import random
        template = random.choice(self.narratives[context])
        return template.format(**kwargs)
        
    def trigger_event(self, event_type: str) -> Optional[Dict]:
        if event_type not in self.events:
            return None
        return self.events[event_type]
        
    def calculate_cultural_weight(self, piece_type: str, context: Dict) -> float:
        """Calculate cultural importance weight of a piece in current context."""
        base_weights = {
            'king': 1.0,    # Tlatoani - máxima autoridade
            'queen': 0.9,   # Cihuacóatl - poder feminino
            'bishop': 0.8,  # Sacerdote - conexão divina
            'knight': 0.7,  # Guerreiro Águia - elite militar
            'rook': 0.6,    # Templo - estrutura sagrada
            'pawn': 0.5     # Guerreiro Jaguar - força básica
        }
        
        weight = base_weights.get(piece_type.lower(), 0.5)
        
        # Adjust weight based on context
        if context.get('is_capture'):
            weight *= 1.2  # Sacrifício ritual aumenta peso
        if context.get('is_check'):
            weight *= 1.3  # Ameaça ao líder é significativa
        if context.get('is_promotion'):
            weight *= 1.4  # Ascensão hierárquica é importante
            
        return min(weight, 1.0)  # Cap at 1.0

aztec_culture = AztecCulture()
