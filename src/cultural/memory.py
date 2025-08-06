from dataclasses import dataclass, field
from typing import List, Dict, Optional
from core.board.board import Piece, Color

@dataclass
class CulturalEvent:
    """Representa um evento cultural significativo no jogo"""
    turn: int
    piece: Piece
    event_type: str  # capture, check, promotion, etc
    description: str
    cultural_impact: float
    
@dataclass
class CaptureEvent(CulturalEvent):
    captured_piece: Piece
    
@dataclass
class PromotionEvent(CulturalEvent):
    new_piece_type: str
    
@dataclass
class CheckEvent(CulturalEvent):
    threatening_pieces: List[Piece]

@dataclass
class CulturalMemory:
    """Sistema de memória para manter o contexto cultural do jogo"""
    moves_history: List[Dict] = field(default_factory=list)
    captured_pieces: Dict[str, List[Piece]] = field(default_factory=lambda: {
        'white': [],
        'black': []
    })
    significant_events: List[CulturalEvent] = field(default_factory=list)
    cultural_tension: float = 0.0
    turn_count: int = 0
    
    def record_move(self, piece: Piece, from_pos: str, to_pos: str, cultural_impact: float):
        """Registra um movimento no histórico"""
        move_data = {
            'turn': self.turn_count,
            'piece_type': piece.type,
            'piece_color': piece.color,
            'from_pos': from_pos.to_algebraic() if hasattr(from_pos, 'to_algebraic') else str(from_pos),
            'to_pos': to_pos.to_algebraic() if hasattr(to_pos, 'to_algebraic') else str(to_pos),
            'impact': cultural_impact
        }
        self.moves_history.append(move_data)
        self.turn_count += 1
    
    def record_capture(self, capturing_piece: Piece, captured_piece: Piece, impact: float):
        """Registra uma captura"""
        color_key = captured_piece.color.value
        self.captured_pieces[color_key].append(captured_piece)
        event = CaptureEvent(
            turn=self.turn_count,
            piece=capturing_piece,
            event_type='capture',
            description=f'{capturing_piece.type.name} captures {captured_piece.type.name}',
            cultural_impact=impact,
            captured_piece=captured_piece
        )
        self.significant_events.append(event)
        self.cultural_tension += impact * 0.5
    
    def record_promotion(self, piece: Piece, new_type: str, impact: float):
        """Registra uma promoção"""
        event = PromotionEvent(
            turn=self.turn_count,
            piece=piece,
            event_type='promotion',
            description=f'{piece.type.name} promotes to {new_type}',
            cultural_impact=impact,
            new_piece_type=new_type
        )
        self.significant_events.append(event)
        self.cultural_tension += impact * 0.3
    
    def record_check(self, attacking_piece: Piece, threatening_pieces: List[Piece], impact: float):
        """Registra um xeque"""
        event = CheckEvent(
            turn=self.turn_count,
            piece=attacking_piece,
            event_type='check',
            description=f'{attacking_piece.type.name} puts king in check',
            cultural_impact=impact,
            threatening_pieces=threatening_pieces
        )
        self.significant_events.append(event)
        self.cultural_tension += impact * 0.7
    
    def get_recent_events(self, num_events: int = 5) -> List[CulturalEvent]:
        """Retorna os eventos mais recentes"""
        return self.significant_events[-num_events:]
    
    def get_cultural_context(self) -> Dict:
        """Retorna o contexto cultural atual do jogo"""
        return {
            'tension': self.cultural_tension,
            'moves': len(self.moves_history),
            'white_captures': len(self.captured_pieces['white']),
            'black_captures': len(self.captured_pieces['black']),
            'significant_events': len(self.significant_events)
        }
    
    def analyze_cultural_significance(self, piece: Piece) -> float:
        """Analisa a significância cultural de uma peça baseado no histórico"""
        piece_moves = [m for m in self.moves_history 
                     if m['piece_type'] == piece.type and m['piece_color'] == piece.color]
        piece_events = [e for e in self.significant_events if e.piece.type == piece.type 
                      and e.piece.color == piece.color]
        
        move_impact = len(piece_moves) * 0.1
        event_impact = len(piece_events) * 0.3
        
        return move_impact + event_impact
