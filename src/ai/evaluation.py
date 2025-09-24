"""
Sistema de avaliação do tabuleiro para a IA de xadrez.
"""

from typing import Dict, Tuple
from ..core.board import Board, Color, Piece, PieceType

# Valores das peças
PIECE_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 20000
}

# Tabelas de posição para cada tipo de peça
PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

POSITION_TABLES = {
    PieceType.PAWN: PAWN_TABLE,
    PieceType.KNIGHT: KNIGHT_TABLE,
    PieceType.BISHOP: BISHOP_TABLE,
    PieceType.ROOK: ROOK_TABLE,
    PieceType.QUEEN: QUEEN_TABLE,
    PieceType.KING: KING_TABLE
}

def get_piece_position_value(piece: Piece, row: int, col: int) -> int:
    """Retorna o valor posicional de uma peça."""
    table = POSITION_TABLES[piece.type]
    if piece.color == Color.BLACK:
        # Inverte a tabela para peças pretas
        row = 7 - row
        return table[row][col]
    return table[row][col]

def evaluate_piece(piece: Piece, row: int, col: int) -> int:
    """Avalia uma peça individual considerando seu valor base e posição."""
    base_value = PIECE_VALUES[piece.type]
    position_value = get_piece_position_value(piece, row, col)
    return base_value + position_value

def evaluate_material(board: Board) -> Dict[Color, int]:
    """Avalia o material total para cada cor."""
    material = {Color.WHITE: 0, Color.BLACK: 0}
    
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is not None:
                material[piece.color] += evaluate_piece(piece, row, col)
                
    return material

def evaluate_mobility(board: Board) -> Dict[Color, int]:
    """Avalia a mobilidade das peças de cada cor."""
    # TODO: Implementar avaliação de mobilidade
    return {Color.WHITE: 0, Color.BLACK: 0}

def evaluate_pawn_structure(board: Board) -> Dict[Color, int]:
    """Avalia a estrutura de peões."""
    # TODO: Implementar avaliação de estrutura de peões
    return {Color.WHITE: 0, Color.BLACK: 0}

def evaluate_king_safety(board: Board) -> Dict[Color, int]:
    """Avalia a segurança do rei."""
    # TODO: Implementar avaliação de segurança do rei
    return {Color.WHITE: 0, Color.BLACK: 0}

def evaluate_position(board: Board) -> int:
    """
    Avalia a posição atual do tabuleiro.
    Retorna um valor positivo se as brancas estão melhor,
    negativo se as pretas estão melhor.
    """
    # Avalia diferentes aspectos da posição
    material = evaluate_material(board)
    mobility = evaluate_mobility(board)
    pawn_structure = evaluate_pawn_structure(board)
    king_safety = evaluate_king_safety(board)
    
    # Combina as avaliações com pesos
    white_score = (
        material[Color.WHITE] +
        mobility[Color.WHITE] +
        pawn_structure[Color.WHITE] +
        king_safety[Color.WHITE]
    )
    
    black_score = (
        material[Color.BLACK] +
        mobility[Color.BLACK] +
        pawn_structure[Color.BLACK] +
        king_safety[Color.BLACK]
    )
    
    return white_score - black_score
