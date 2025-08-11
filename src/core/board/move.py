from dataclasses import dataclass
from typing import Optional
from .board import PieceType, Color, Piece, Position
from src.core.interfaces import MoveType

@dataclass
class Move:
    """Representa um movimento no jogo"""
    from_pos: Position
    to_pos: Position
    piece: Piece
    captured_piece: Optional[Piece] = None
    promotion_piece: Optional[Piece] = None
    is_castling: bool = False
    is_en_passant: bool = False
    is_check: bool = False
    
    @property
    def move_type(self) -> MoveType:
        """Retorna o tipo do movimento baseado nos flags booleanos"""
        if self.is_castling:
            return MoveType.CASTLE
        elif self.is_en_passant:
            return MoveType.EN_PASSANT
        elif self.promotion_piece is not None:
            return MoveType.PROMOTION
        else:
            return MoveType.NORMAL
    
    def __str__(self) -> str:
        """Retorna representação em string do movimento"""
        move_str = ""
        
        # Adiciona peça movida
        if self.piece.type != PieceType.PAWN:
            # Map piece types to their standard chess notation
            piece_notation = {
                PieceType.KNIGHT: 'N',
                PieceType.BISHOP: 'B',
                PieceType.ROOK: 'R',
                PieceType.QUEEN: 'Q',
                PieceType.KING: 'K'
            }
            move_str += piece_notation.get(self.piece.type, '')
            
        # Adiciona posição
        move_str += str(self.from_pos)
        
        # Adiciona captura
        if self.captured_piece:
            move_str += "x"
        else:
            move_str += "-"
            
        move_str += str(self.to_pos)
        
        # Adiciona promoção
        if self.promotion_piece:
            piece_notation = {
                PieceType.KNIGHT: 'N',
                PieceType.BISHOP: 'B',
                PieceType.ROOK: 'R',
                PieceType.QUEEN: 'Q'
            }
            move_str += "=" + piece_notation.get(self.promotion_piece.type, 'Q')
            
        # Adiciona xeque
        if self.is_check:
            move_str += "+"
            
        return move_str
