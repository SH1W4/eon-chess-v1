"""
Implementação dos movimentos tradicionais das peças de xadrez.
"""

from typing import List, Tuple
from ..core.board import Board, Color, Piece, PieceType

def get_pawn_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para um peão."""
    row, col = pos
    piece = board.get_piece(row, col)
    if piece is None or piece.type != PieceType.PAWN:
        return []

    moves = []
    direction = -1 if piece.color == Color.WHITE else 1
    
    # Movimento básico para frente
    next_row = row + direction
    if board.is_valid_position(next_row, col) and board.get_piece(next_row, col) is None:
        moves.append((next_row, col))
        
        # Movimento duplo inicial
        if ((piece.color == Color.WHITE and row == 6) or 
            (piece.color == Color.BLACK and row == 1)):
            next_row = row + 2 * direction
            if board.get_piece(next_row, col) is None:
                moves.append((next_row, col))
    
    # Capturas diagonais
    for col_offset in [-1, 1]:
        capture_col = col + col_offset
        if board.is_valid_position(next_row, capture_col):
            target = board.get_piece(next_row, capture_col)
            if target is not None and target.color != piece.color:
                moves.append((next_row, capture_col))
    
    return moves

def get_rook_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para uma torre."""
    row, col = pos
    piece = board.get_piece(row, col)
    if piece is None or piece.type != PieceType.ROOK:
        return []

    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Direções: direita, esquerda, baixo, cima
    
    for row_dir, col_dir in directions:
        current_row, current_col = row + row_dir, col + col_dir
        while board.is_valid_position(current_row, current_col):
            target = board.get_piece(current_row, current_col)
            if target is None:
                moves.append((current_row, current_col))
            else:
                if target.color != piece.color:
                    moves.append((current_row, current_col))
                break
            current_row += row_dir
            current_col += col_dir
    
    return moves

def get_knight_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para um cavalo."""
    row, col = pos
    piece = board.get_piece(row, col)
    if piece is None or piece.type != PieceType.KNIGHT:
        return []

    moves = []
    offsets = [
        (-2, -1), (-2, 1),  # Movimentos em L para cima
        (-1, -2), (-1, 2),  # Movimentos em L para os lados (cima)
        (1, -2), (1, 2),    # Movimentos em L para os lados (baixo)
        (2, -1), (2, 1)     # Movimentos em L para baixo
    ]
    
    for row_offset, col_offset in offsets:
        new_row, new_col = row + row_offset, col + col_offset
        if board.is_valid_position(new_row, new_col):
            target = board.get_piece(new_row, new_col)
            if target is None or target.color != piece.color:
                moves.append((new_row, new_col))
    
    return moves

def get_bishop_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para um bispo."""
    row, col = pos
    piece = board.get_piece(row, col)
    if piece is None or piece.type != PieceType.BISHOP:
        return []

    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Direções diagonais
    
    for row_dir, col_dir in directions:
        current_row, current_col = row + row_dir, col + col_dir
        while board.is_valid_position(current_row, current_col):
            target = board.get_piece(current_row, current_col)
            if target is None:
                moves.append((current_row, current_col))
            else:
                if target.color != piece.color:
                    moves.append((current_row, current_col))
                break
            current_row += row_dir
            current_col += col_dir
    
    return moves

def get_queen_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para uma rainha."""
    # A rainha combina os movimentos da torre e do bispo
    return get_rook_moves(board, pos) + get_bishop_moves(board, pos)

def get_king_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna os movimentos possíveis para um rei."""
    row, col = pos
    piece = board.get_piece(row, col)
    if piece is None or piece.type != PieceType.KING:
        return []

    moves = []
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for row_offset, col_offset in directions:
        new_row, new_col = row + row_offset, col + col_offset
        if board.is_valid_position(new_row, new_col):
            target = board.get_piece(new_row, new_col)
            if target is None or target.color != piece.color:
                moves.append((new_row, new_col))
    
    # TODO: Implementar roque (castling)
    return moves

def get_all_possible_moves(board: Board, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Retorna todos os movimentos possíveis para uma peça na posição dada."""
    piece = board.get_piece(*pos)
    if piece is None:
        return []
        
    move_functions = {
        PieceType.PAWN: get_pawn_moves,
        PieceType.ROOK: get_rook_moves,
        PieceType.KNIGHT: get_knight_moves,
        PieceType.BISHOP: get_bishop_moves,
        PieceType.QUEEN: get_queen_moves,
        PieceType.KING: get_king_moves
    }
    
    return move_functions[piece.type](board, pos)
