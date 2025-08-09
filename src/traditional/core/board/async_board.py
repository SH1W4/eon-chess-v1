"""Wrapper assíncrono para o Board tradicional - Versão corrigida pelo ARKITECT"""
import asyncio
from typing import List, Optional
from .board import Board as SyncBoard
from src.traditional.models.models import Position, Piece, PieceType, Color
from core.interfaces import Move, MoveType


class Board(SyncBoard):
    """Board com métodos assíncronos para compatibilidade com testes"""
    
    def __init__(self):
        super().__init__()
    
    def is_in_check(self, color: Color) -> bool:
        """Check if the king is in check - versão melhorada pelo ARKITECT"""
        # Find king position
        king_pos = None
        for pos, piece in self.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = pos
                break
        
        if not king_pos:
            return False
        
        # Check for attacks from enemy pieces
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        # Check for pawn attacks
        pawn_direction = 1 if enemy_color == Color.WHITE else -1
        for file_offset in [-1, 1]:
            try:
                attack_pos = Position(king_pos.rank - pawn_direction, king_pos.file + file_offset)
                piece = self.get_piece(attack_pos)
                if piece and piece.color == enemy_color and piece.type == PieceType.PAWN:
                    return True
            except:
                pass
        
        # Check for knight attacks
        knight_moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dr, df in knight_moves:
            try:
                attack_pos = Position(king_pos.rank + dr, king_pos.file + df)
                piece = self.get_piece(attack_pos)
                if piece and piece.color == enemy_color and piece.type == PieceType.KNIGHT:
                    return True
            except:
                pass
        
        # Check for sliding piece attacks (Queen, Rook, Bishop)
        directions = [
            (1,0), (-1,0), (0,1), (0,-1),  # Rook/Queen
            (1,1), (1,-1), (-1,1), (-1,-1)  # Bishop/Queen
        ]
        
        for dr, df in directions:
            for distance in range(1, 9):
                try:
                    check_pos = Position(king_pos.rank + dr*distance, king_pos.file + df*distance)
                    piece = self.get_piece(check_pos)
                    if piece:
                        if piece.color == enemy_color:
                            is_diagonal = dr != 0 and df != 0
                            is_straight = dr == 0 or df == 0
                            if piece.type == PieceType.QUEEN:
                                return True
                            elif piece.type == PieceType.BISHOP and is_diagonal:
                                return True
                            elif piece.type == PieceType.ROOK and is_straight:
                                return True
                            elif piece.type == PieceType.KING and distance == 1:
                                return True
                        break  # Piece blocks line
                except:
                    break
        
        return False
    
    async def make_move(self, move: Move) -> bool:
        """Executa um movimento de forma assíncrona com validação completa"""
        # Converte Move para chamada síncrona
        from_pos = move.from_pos if isinstance(move.from_pos, Position) else Position(move.from_pos.rank, move.from_pos.file)
        to_pos = move.to_pos if isinstance(move.to_pos, Position) else Position(move.to_pos.rank, move.to_pos.file)
        
        # Verifica se o movimento é válido
        piece = self.get_piece(from_pos)
        if not piece:
            return False
        
        if piece.color != self.current_turn:
            return False
        
        # Salva estado original para validação
        original_target = self.get_piece(to_pos)
        original_pos = piece.position
        
        # Faz o movimento temporariamente
        self.pieces[to_pos] = piece
        piece.position = to_pos
        if from_pos in self.pieces:
            del self.pieces[from_pos]
        
        # Verifica se o movimento deixaria o rei em xeque
        would_be_in_check = self.is_in_check(piece.color)
        
        # Se deixaria em xeque, desfaz o movimento
        if would_be_in_check:
            # Restaura estado original
            self.pieces[from_pos] = piece
            piece.position = original_pos
            if original_target:
                self.pieces[to_pos] = original_target
            elif to_pos in self.pieces:
                del self.pieces[to_pos]
            return False  # Movimento ilegal
        
        # Movimento é válido, mantém as mudanças
        # Adiciona peça capturada se houver
        if original_target:
            self.captured_pieces.append(original_target)
        
        # Handle castling - move a torre também
        if move.move_type == MoveType.CASTLE:
            # King side castling
            if to_pos.file == 7:
                rook_from = Position(from_pos.rank, 8)
                rook_to = Position(from_pos.rank, 6)
            # Queen side castling
            elif to_pos.file == 3:
                rook_from = Position(from_pos.rank, 1)
                rook_to = Position(from_pos.rank, 4)
            else:
                # Invalid castling position
                rook_from = None
                rook_to = None
            
            if rook_from and rook_to:
                rook = self.get_piece(rook_from)
                if rook and rook.type == PieceType.ROOK:
                    self.pieces[rook_to] = rook
                    rook.position = rook_to
                    if rook_from in self.pieces:
                        del self.pieces[rook_from]
        
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
        moves = self._get_piece_moves_no_check(piece)
        
        # Filtra movimentos que deixariam rei em xeque
        valid_moves = []
        for move_pos in moves:
            # Simula o movimento
            original_target = self.get_piece(move_pos)
            original_pos = piece.position
            
            self.pieces[move_pos] = piece
            piece.position = move_pos
            if position in self.pieces:
                del self.pieces[position]
            
            # Verifica se deixaria em xeque
            in_check = self.is_in_check(piece.color)
            
            # Desfaz o movimento
            self.pieces[position] = piece
            piece.position = original_pos
            if original_target:
                self.pieces[move_pos] = original_target
            elif move_pos in self.pieces:
                del self.pieces[move_pos]
            
            if not in_check:
                valid_moves.append(move_pos)
        
        return valid_moves
    
    def set_piece(self, position: Position, piece: Piece):
        """Define uma peça em uma posição"""
        self.pieces[position] = piece
        piece.position = position
    
    def is_checkmate(self) -> bool:
        """Verifica xeque-mate - versão melhorada"""
        if not self.is_in_check(self.current_turn):
            return False
        
        # Verifica se há algum movimento que tira do xeque
        for pos, piece in list(self.pieces.items()):
            if piece.color == self.current_turn:
                moves = self._get_piece_moves_no_check(piece)
                for move_pos in moves:
                    # Simula o movimento
                    original_target = self.get_piece(move_pos)
                    original_pos = piece.position
                    
                    self.pieces[move_pos] = piece
                    piece.position = move_pos
                    if pos in self.pieces:
                        del self.pieces[pos]
                    
                    # Verifica se ainda está em xeque
                    still_in_check = self.is_in_check(self.current_turn)
                    
                    # Desfaz o movimento
                    self.pieces[pos] = piece
                    piece.position = original_pos
                    if original_target:
                        self.pieces[move_pos] = original_target
                    elif move_pos in self.pieces:
                        del self.pieces[move_pos]
                    
                    if not still_in_check:
                        return False  # Encontrou movimento que salva do xeque
        
        return True  # Nenhum movimento salva do xeque = xeque-mate
    
    def is_stalemate(self) -> bool:
        """Verifica empate por afogamento - versão melhorada"""
        if self.is_in_check(self.current_turn):
            return False  # Se está em xeque, não é stalemate
        
        # Verifica se há algum movimento válido
        for pos, piece in list(self.pieces.items()):
            if piece.color == self.current_turn:
                moves = self._get_piece_moves_no_check(piece)
                for move_pos in moves:
                    # Simula o movimento
                    original_target = self.get_piece(move_pos)
                    original_pos = piece.position
                    
                    self.pieces[move_pos] = piece
                    piece.position = move_pos
                    if pos in self.pieces:
                        del self.pieces[pos]
                    
                    # Verifica se o movimento é legal (não deixa em xeque)
                    would_be_in_check = self.is_in_check(self.current_turn)
                    
                    # Desfaz o movimento
                    self.pieces[pos] = piece
                    piece.position = original_pos
                    if original_target:
                        self.pieces[move_pos] = original_target
                    elif move_pos in self.pieces:
                        del self.pieces[move_pos]
                    
                    if not would_be_in_check:
                        return False  # Encontrou movimento válido
        
        return True  # Nenhum movimento válido = stalemate
