from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

class Color(Enum):
    WHITE = auto()
    BLACK = auto()

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Position:
    def __init__(self, file: str, rank: int):
        self.file = file
        self.rank = rank
    
    def __str__(self):
        return f"{self.file}{self.rank}"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False

class Board:
    def __init__(self):
        self.pieces: Dict[str, Piece] = {}
        self.setup_initial_position()
        self.current_turn = Color.WHITE
        self.last_move = None
        self._setup_piece_symbols()

    def _setup_piece_symbols(self):
        self.piece_symbols = {
            (PieceType.KING, Color.WHITE): "♔",
            (PieceType.QUEEN, Color.WHITE): "♕",
            (PieceType.ROOK, Color.WHITE): "♖",
            (PieceType.BISHOP, Color.WHITE): "♗",
            (PieceType.KNIGHT, Color.WHITE): "♘",
            (PieceType.PAWN, Color.WHITE): "♙",
            (PieceType.KING, Color.BLACK): "♚",
            (PieceType.QUEEN, Color.BLACK): "♛",
            (PieceType.ROOK, Color.BLACK): "♜",
            (PieceType.BISHOP, Color.BLACK): "♝",
            (PieceType.KNIGHT, Color.BLACK): "♞",
            (PieceType.PAWN, Color.BLACK): "♟"
        }

    def setup_initial_position(self):
        # Setup white pieces
        self.pieces["a1"] = Piece(PieceType.ROOK, Color.WHITE)
        self.pieces["b1"] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.pieces["c1"] = Piece(PieceType.BISHOP, Color.WHITE)
        self.pieces["d1"] = Piece(PieceType.QUEEN, Color.WHITE)
        self.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
        self.pieces["f1"] = Piece(PieceType.BISHOP, Color.WHITE)
        self.pieces["g1"] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.pieces["h1"] = Piece(PieceType.ROOK, Color.WHITE)
        
        # Setup black pieces
        self.pieces["a8"] = Piece(PieceType.ROOK, Color.BLACK)
        self.pieces["b8"] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.pieces["c8"] = Piece(PieceType.BISHOP, Color.BLACK)
        self.pieces["d8"] = Piece(PieceType.QUEEN, Color.BLACK)
        self.pieces["e8"] = Piece(PieceType.KING, Color.BLACK)
        self.pieces["f8"] = Piece(PieceType.BISHOP, Color.BLACK)
        self.pieces["g8"] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.pieces["h8"] = Piece(PieceType.ROOK, Color.BLACK)
        
        # Setup pawns
        for file in "abcdefgh":
            self.pieces[f"{file}2"] = Piece(PieceType.PAWN, Color.WHITE)
            self.pieces[f"{file}7"] = Piece(PieceType.PAWN, Color.BLACK)

    def get_piece(self, pos: str) -> Optional[Piece]:
        return self.pieces.get(pos)

    def display(self) -> str:
        board = []
        board.append("  a b c d e f g h")
        board.append("  ---------------")
        
        for rank in range(8, 0, -1):
            row = [f"{rank}|"]
            for file in "abcdefgh":
                pos = f"{file}{rank}"
                piece = self.pieces.get(pos)
                if piece:
                    symbol = self.piece_symbols.get((piece.type, piece.color), "?")
                    row.append(symbol)
                else:
                    row.append(".")
            row.append(f"|{rank}")
            board.append(" ".join(row))
        
        board.append("  ---------------")
        board.append("  a b c d e f g h")
        return "\n".join(board)

    def move_piece(self, from_pos: str, to_pos: str) -> dict:
        piece = self.pieces.get(from_pos)
        if not piece:
            return {"success": False, "error": "Não há peça na posição inicial"}
            
        if piece.color != self.current_turn:
            return {"success": False, "error": "Não é a vez desta cor"}
            
        # TODO: Implementar validação de movimento
        
        # Executa o movimento
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        piece.has_moved = True
        
        # Alterna o turno
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        self.last_move = (from_pos, to_pos)
        
        return {"success": True}

    def castle_kingside(self) -> dict:
        if self.current_turn == Color.WHITE:
            king_pos, rook_pos = "e1", "h1"
            king_target, rook_target = "g1", "f1"
        else:
            king_pos, rook_pos = "e8", "h8"
            king_target, rook_target = "g8", "f8"
            
        king = self.pieces.get(king_pos)
        rook = self.pieces.get(rook_pos)
        
        if not king or not rook:
            return {"success": False, "error": "Rei ou torre não encontrados"}
            
        if king.has_moved or rook.has_moved:
            return {"success": False, "error": "Rei ou torre já se moveram"}
            
        # TODO: Implementar verificação de caminho livre e xeque
        
        # Executa o roque
        self.pieces[king_target] = king
        self.pieces[rook_target] = rook
        del self.pieces[king_pos]
        del self.pieces[rook_pos]
        
        king.has_moved = True
        rook.has_moved = True
        
        return {"success": True}

    def is_en_passant_possible(self) -> bool:
        if not self.last_move:
            return False
            
        from_pos, to_pos = self.last_move
        piece = self.pieces.get(to_pos)
        
        if not piece or piece.type != PieceType.PAWN:
            return False
            
        # TODO: Implementar lógica completa de en passant
        return False

    def promote_pawn(self, from_pos: str, to_pos: str, promotion: str) -> dict:
        piece = self.pieces.get(from_pos)
        if not piece or piece.type != PieceType.PAWN:
            return {"success": False, "error": "Não há peão na posição inicial"}
            
        promotion_types = {
            "queen": PieceType.QUEEN,
            "rook": PieceType.ROOK,
            "bishop": PieceType.BISHOP,
            "knight": PieceType.KNIGHT
        }
        
        if promotion not in promotion_types:
            return {"success": False, "error": "Promoção inválida"}
            
        # Executa a promoção
        self.pieces[to_pos] = Piece(promotion_types[promotion], piece.color)
        del self.pieces[from_pos]
        
        return {"success": True}

    def is_in_check(self) -> bool:
        # TODO: Implementar verificação de xeque
        return False

    def is_checkmate(self) -> bool:
        # TODO: Implementar verificação de xeque-mate
        return False

    def is_stalemate(self) -> bool:
        # TODO: Implementar verificação de empate
        return False
