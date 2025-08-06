from dataclasses import dataclass
from enum import Enum, auto
from .board import PieceType, Color

@dataclass
class Move:
    """Representa um movimento no jogo"""
    piece_type: PieceType
    piece_color: Color
    from_pos: str
    to_pos: str
    is_capture: bool = False
    is_check: bool = False
    promoted_to: PieceType = None
    
    def __str__(self) -> str:
        """Retorna representação em string do movimento"""
        move_str = ""
        
        # Adiciona peça movida
        if self.piece_type != PieceType.PAWN:
            move_str += self.piece_type.value[0].upper()
            
        # Adiciona posição
        move_str += self.from_pos
        
        # Adiciona captura
        if self.is_capture:
            move_str += "x"
        else:
            move_str += "-"
            
        move_str += self.to_pos
        
        # Adiciona promoção
        if self.promoted_to:
            move_str += "=" + self.promoted_to.value[0].upper()
            
        # Adiciona xeque
        if self.is_check:
            move_str += "+"
            
        return move_str
