"""
Implementação das regras tradicionais do xadrez.
"""

from typing import List, Optional, Tuple
from ..core.board import Board, Color, Piece, PieceType
from .movements import get_all_possible_moves

def is_check(board: Board, king_color: Color) -> bool:
    """Verifica se o rei da cor especificada está em xeque."""
    # Encontra a posição do rei
    king_pos = None
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if (piece is not None and 
                piece.type == PieceType.KING and 
                piece.color == king_color):
                king_pos = (row, col)
                break
        if king_pos is not None:
            break
    
    if king_pos is None:
        return False
    
    # Verifica se alguma peça adversária pode capturar o rei
    opponent_color = Color.BLACK if king_color == Color.WHITE else Color.WHITE
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None and piece.color == opponent_color:
                moves = get_all_possible_moves(board, (row, col))
                if king_pos in moves:
                    return True
    
    return False

def is_checkmate(board: Board, king_color: Color) -> bool:
    """Verifica se o rei da cor especificada está em xeque-mate."""
    if not is_check(board, king_color):
        return False
        
    # Verifica se há algum movimento legal que pode tirar do xeque
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None and piece.color == king_color:
                moves = get_all_possible_moves(board, (row, col))
                for move in moves:
                    # Tenta o movimento
                    original_piece = board.get_piece(*move)
                    board.move_piece((row, col), move)
                    
                    # Verifica se ainda está em xeque
                    still_in_check = is_check(board, king_color)
                    
                    # Desfaz o movimento
                    board.move_piece(move, (row, col))
                    board.squares[move[0]][move[1]] = original_piece
                    
                    if not still_in_check:
                        return False
    
    return True

def is_stalemate(board: Board, current_color: Color) -> bool:
    """Verifica se a posição atual é um empate por afogamento."""
    if is_check(board, current_color):
        return False
        
    # Verifica se há algum movimento legal disponível
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None and piece.color == current_color:
                moves = get_all_possible_moves(board, (row, col))
                for move in moves:
                    # Tenta o movimento
                    original_piece = board.get_piece(*move)
                    board.move_piece((row, col), move)
                    
                    # Verifica se o movimento é legal (não deixa em xeque)
                    legal_move = not is_check(board, current_color)
                    
                    # Desfaz o movimento
                    board.move_piece(move, (row, col))
                    board.squares[move[0]][move[1]] = original_piece
                    
                    if legal_move:
                        return False
    
    return True

def is_insufficient_material(board: Board) -> bool:
    """Verifica se há material insuficiente para mate."""
    pieces = {Color.WHITE: [], Color.BLACK: []}
    
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None:
                pieces[piece.color].append(piece.type)
    
    def has_only_king(pieces_list: List[PieceType]) -> bool:
        return len(pieces_list) == 1 and PieceType.KING in pieces_list
    
    def has_only_king_and_minor_piece(pieces_list: List[PieceType]) -> bool:
        if len(pieces_list) != 2:
            return False
        return (PieceType.KING in pieces_list and 
                (PieceType.BISHOP in pieces_list or PieceType.KNIGHT in pieces_list))
    
    # Rei contra rei
    if (has_only_king(pieces[Color.WHITE]) and 
        has_only_king(pieces[Color.BLACK])):
        return True
    
    # Rei contra rei e bispo/cavalo
    if ((has_only_king(pieces[Color.WHITE]) and 
         has_only_king_and_minor_piece(pieces[Color.BLACK])) or
        (has_only_king(pieces[Color.BLACK]) and 
         has_only_king_and_minor_piece(pieces[Color.WHITE]))):
        return True
    
    return False

def get_legal_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna todos os movimentos legais para uma peça (excluindo movimentos que deixam em xeque)."""
    piece = board.get_piece(*pos)
    if piece is None:
        return []
        
    moves = get_all_possible_moves(board, pos)
    legal_moves = []
    
    for move in moves:
        # Tenta o movimento
        original_piece = board.get_piece(*move)
        board.move_piece(pos, move)
        
        # Verifica se o movimento é legal
        if not is_check(board, piece.color):
            legal_moves.append(move)
        
        # Desfaz o movimento
        board.move_piece(move, pos)
        board.squares[move[0]][move[1]] = original_piece
    
    return legal_moves
