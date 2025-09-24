"""
Sistema de narrativas culturais para xadrez.
"""

from typing import Dict, List, Optional, Union
import json
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from ..core.board import Board, Color, PieceType

class NarrativeStyle(Enum):
    """Estilos de narrativa disponíveis."""
    HISTORICAL = "historical"  # Baseado em eventos históricos reais
    MYTHOLOGICAL = "mythological"  # Baseado em mitos e lendas
    DRAMATIC = "dramatic"  # Foco em drama e conflito
    STRATEGIC = "strategic"  # Foco em aspectos táticos e estratégicos
    EDUCATIONAL = "educational"  # Foco em ensino e aprendizado

@dataclass
class CulturalContext:
    """Contexto cultural para a narrativa."""
    region: str  # Região cultural (ex: "europeu", "persa", "indiano")
    era: str  # Era histórica (ex: "medieval", "renascimento", "moderno")
    style: NarrativeStyle  # Estilo da narrativa
    language: str  # Idioma principal para narrativas

@dataclass
class NarrativeEvent:
    """Representa um evento narrativo no jogo."""
    move_number: int
    piece_type: PieceType
    color: Color
    event_type: str  # ex: "capture", "check", "promote", "castle"
    description: str
    cultural_significance: Optional[str] = None

class CulturalNarrativeManager:
    """Gerencia narrativas culturais durante o jogo."""
    
    def __init__(self, context: CulturalContext):
        self.context = context
        self.narrative_history: List[NarrativeEvent] = []
        self.cultural_database: Dict[str, Dict] = {}
        self.templates: Dict[str, str] = {}
        
    def load_cultural_database(self, filepath: str) -> bool:
        """
        Carrega banco de dados de referências culturais.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r') as f:
                self.cultural_database = json.load(f)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def load_narrative_templates(self, filepath: str) -> bool:
        """
        Carrega templates de narrativa.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r') as f:
                self.templates = json.load(f)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
            
    def _get_piece_cultural_name(self, piece_type: PieceType) -> str:
        """Retorna o nome cultural da peça baseado no contexto."""
        cultural_names = {
            "europeu": {
                PieceType.KING: "Rei",
                PieceType.QUEEN: "Rainha",
                PieceType.BISHOP: "Bispo",
                PieceType.KNIGHT: "Cavaleiro",
                PieceType.ROOK: "Torre",
                PieceType.PAWN: "Peão"
            },
            "persa": {
                PieceType.KING: "Shah",
                PieceType.QUEEN: "Vizir",
                PieceType.BISHOP: "Alfil",
                PieceType.KNIGHT: "Aspa",
                PieceType.ROOK: "Rukh",
                PieceType.PAWN: "Piyadah"
            },
            "indiano": {
                PieceType.KING: "Raja",
                PieceType.QUEEN: "Mantri",
                PieceType.BISHOP: "Gaja",
                PieceType.KNIGHT: "Ashva",
                PieceType.ROOK: "Ratha",
                PieceType.PAWN: "Bhata"
            }
        }
        
        return cultural_names.get(self.context.region, {}).get(piece_type, str(piece_type))
        
    def generate_move_narrative(self, 
                              move_number: int,
                              piece_type: PieceType,
                              color: Color,
                              from_pos: tuple,
                              to_pos: tuple,
                              is_capture: bool,
                              is_check: bool,
                              is_checkmate: bool) -> str:
        """Gera uma narrativa cultural para um movimento."""
        piece_name = self._get_piece_cultural_name(piece_type)
        color_name = "branco" if color == Color.WHITE else "preto"
        
        # Gera descrição base
        if self.context.style == NarrativeStyle.HISTORICAL:
            template = "O {piece} {color} avança como um comandante em batalha"
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            template = "O poderoso {piece} {color} move-se com propósito divino"
        elif self.context.style == NarrativeStyle.DRAMATIC:
            template = "Em um movimento audacioso, o {piece} {color} desafia seu destino"
        elif self.context.style == NarrativeStyle.STRATEGIC:
            template = "O {piece} {color} executa uma manobra estratégica"
        else:  # EDUCATIONAL
            template = "O {piece} {color} demonstra um movimento clássico"
            
        narrative = template.format(piece=piece_name, color=color_name)
        
        # Adiciona contexto adicional
        if is_capture:
            narrative += " e captura uma peça inimiga"
        if is_check:
            narrative += ", ameaçando o rei adversário"
        if is_checkmate:
            narrative += " e conquista a vitória!"
            
        # Adiciona significado cultural se disponível
        cultural_ref = self.cultural_database.get(str(piece_type), {}).get(self.context.region)
        if cultural_ref:
            narrative += f"\n{cultural_ref}"
            
        # Registra o evento
        event = NarrativeEvent(
            move_number=move_number,
            piece_type=piece_type,
            color=color,
            event_type="move",
            description=narrative,
            cultural_significance=cultural_ref
        )
        self.narrative_history.append(event)
        
        return narrative
        
    def generate_game_story(self) -> str:
        """Gera uma história completa do jogo baseada nos eventos registrados."""
        if not self.narrative_history:
            return "Nenhuma história para contar ainda."
            
        story = f"Uma épica batalha de {self.context.era} se desenrola...\n\n"
        
        for event in self.narrative_history:
            story += f"Movimento {event.move_number}: {event.description}\n"
            if event.cultural_significance:
                story += f"Nota cultural: {event.cultural_significance}\n"
            story += "\n"
            
        return story
        
    def save_narrative_history(self, filepath: str):
        """Salva o histórico de narrativas em disco."""
        history_data = {
            'context': {
                'region': self.context.region,
                'era': self.context.era,
                'style': self.context.style.value,
                'language': self.context.language
            },
            'events': [
                {
                    'move_number': event.move_number,
                    'piece_type': event.piece_type.value,
                    'color': event.color.value,
                    'event_type': event.event_type,
                    'description': event.description,
                    'cultural_significance': event.cultural_significance
                }
                for event in self.narrative_history
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2)
            
    def load_narrative_history(self, filepath: str) -> bool:
        """
        Carrega histórico de narrativas do disco.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r') as f:
                history_data = json.load(f)
                
            self.context = CulturalContext(
                region=history_data['context']['region'],
                era=history_data['context']['era'],
                style=NarrativeStyle(history_data['context']['style']),
                language=history_data['context']['language']
            )
            
            self.narrative_history = [
                NarrativeEvent(
                    move_number=event['move_number'],
                    piece_type=PieceType(event['piece_type']),
                    color=Color(event['color']),
                    event_type=event['event_type'],
                    description=event['description'],
                    cultural_significance=event.get('cultural_significance')
                )
                for event in history_data['events']
            ]
            
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
