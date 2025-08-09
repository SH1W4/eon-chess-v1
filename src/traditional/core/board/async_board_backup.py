"""Wrapper assíncrono para o Board tradicional"""
import asyncio
from typing import List, Optional
from .board import Board as SyncBoard
from src.traditional.models.models import Position, Piece, PieceType, Color
from core.interfaces import Move, MoveType


class Board(SyncBoard):
    """Board com métodos assíncronos para compatibilidade com testes"""
    
    def __init__(self):
        super().__init__()
    
    async def make_move(self, move: Move) -> bool:
        """Executa um movimento de forma assíncrona"""
        # Converte Move para chamada síncrona
        from_pos = move.from_pos if isinstance(move.from_pos, Position) else Position(move.from_pos.rank, move.from_pos.file)
        to_pos = move.to_pos if isinstance(move.to_pos, Position) else Position(move.to_pos.rank, move.to_pos.file)
        
        # Verifica se o movimento é válido
        piece = self.get_piece(from_pos)
        if not piece:
            return False
        
        if piece.color != self.current_turn:
            return False
        
        # Executa o movimento
        target = self.get_piece(to_pos)
        if target:
            self.captured_pieces.append(target)
        
        # Move a peça
        self.pieces[to_pos] = piece
        piece.position = to_pos
        del self.pieces[from_pos]
        
        # Atualiza o turno
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        self.move_history.append((from_pos, to_pos))
        
        return True
    
    async def get_valid_moves(self, position: Position) -> List[Position]:
        """Retorna movimentos válidos de forma assíncrona"""
        piece = self.get_piece(position)
        if not piece:
            return []
        
        # Usa o método síncrono existente
        return self._get_piece_moves_no_check(piece)
    
    def set_piece(self, position: Position, piece: Piece):
        """Define uma peça em uma posição"""
        self.pieces[position] = piece
        piece.position = position
    
    def is_checkmate(self) -> bool:
        """Verifica xeque-mate"""
        if not self.is_in_check(self.current_turn):
            return False
        
        # Verifica se há movimentos válidos
        for pos, piece in self.pieces.items():
            if piece.color == self.current_turn:
                moves = self._get_piece_moves_no_check(piece)
                if moves:
                    return False
        return True
    
    def is_stalemate(self) -> bool:
        """Verifica empate por afogamento"""
        if self.is_in_check(self.current_turn):
            return False
        
        # Verifica se há movimentos válidos
        for pos, piece in self.pieces.items():
            if piece.color == self.current_turn:
                moves = self._get_piece_moves_no_check(piece)
                if moves:
                    return False
        return True
