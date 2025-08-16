from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

import chess


class Color(Enum):
    WHITE = chess.WHITE
    BLACK = chess.BLACK


class PieceType(Enum):
    PAWN = chess.PAWN
    KNIGHT = chess.KNIGHT
    BISHOP = chess.BISHOP
    ROOK = chess.ROOK
    QUEEN = chess.QUEEN
    KING = chess.KING


@dataclass
class Piece:
    type: PieceType
    color: Color


@dataclass(frozen=True)
class Position:
    file: str
    rank: int

    def __str__(self) -> str:  # pragma: no cover - utility
        return f"{self.file}{self.rank}"


class Board:
    """Simple chess board wrapper backed by python-chess."""

    def __init__(self) -> None:
        self.pieces: Dict[str, Piece] = {}
        self.move_history: List[Tuple[str, str]] = []
        self.captured_pieces: List[Piece] = []
        self.current_turn: Color = Color.WHITE
        self.last_move: Optional[Tuple[str, str]] = None
        self.piece_symbols = {
            (PieceType.PAWN, Color.WHITE): "♙",
            (PieceType.KNIGHT, Color.WHITE): "♘",
            (PieceType.BISHOP, Color.WHITE): "♗",
            (PieceType.ROOK, Color.WHITE): "♖",
            (PieceType.QUEEN, Color.WHITE): "♕",
            (PieceType.KING, Color.WHITE): "♔",
            (PieceType.PAWN, Color.BLACK): "♟",
            (PieceType.KNIGHT, Color.BLACK): "♞",
            (PieceType.BISHOP, Color.BLACK): "♝",
            (PieceType.ROOK, Color.BLACK): "♜",
            (PieceType.QUEEN, Color.BLACK): "♛",
            (PieceType.KING, Color.BLACK): "♚",
        }
        self.setup_initial_position()

    # ------------------------------------------------------------------
    # Helpers
    def _to_chess_board(self) -> chess.Board:
        board = chess.Board(None)
        for pos, piece in self.pieces.items():
            square = chess.parse_square(pos)
            board.set_piece_at(square, chess.Piece(piece.type.value, piece.color.value))
        board.turn = self.current_turn == Color.WHITE
        board.castling_rights = chess.BB_ALL
        if self.last_move:
            from_sq, to_sq = self.last_move
            moved = self.pieces.get(to_sq)
            if moved and moved.type == PieceType.PAWN:
                r_from = chess.square_rank(chess.parse_square(from_sq))
                r_to = chess.square_rank(chess.parse_square(to_sq))
                if abs(r_from - r_to) == 2:
                    ep_rank = (r_from + r_to) // 2
                    file = chess.square_file(chess.parse_square(to_sq))
                    board.ep_square = chess.square(file, ep_rank)
        return board

    def _sync_from_chess_board(self, board: chess.Board) -> None:
        self.pieces.clear()
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                pos = chess.square_name(square)
                self.pieces[pos] = Piece(PieceType(piece.piece_type), Color(piece.color))
        self.current_turn = Color.WHITE if board.turn == chess.WHITE else Color.BLACK

    # ------------------------------------------------------------------
    def setup_initial_position(self) -> None:
        board = chess.Board()
        self._sync_from_chess_board(board)
        self.move_history.clear()
        self.captured_pieces.clear()
        self.last_move = None

    def display(self) -> str:
        return self._to_chess_board().unicode()

    def get_piece(self, pos: str) -> Optional[Piece]:
        return self.pieces.get(pos)

    # ------------------------------------------------------------------
    # Core move logic
    def _move_exposes_check(self, from_pos: str, to_pos: str) -> bool:
        board = self._to_chess_board()
        move = chess.Move.from_uci(from_pos + to_pos)
        return board.is_into_check(move)

    def _is_valid_move(self, piece: Piece, from_pos: str, to_pos: str) -> bool:
        board = self._to_chess_board()
        move = chess.Move.from_uci(from_pos + to_pos)
        return move in board.legal_moves

    def _has_legal_moves(self) -> bool:
        board = self._to_chess_board()
        return any(board.legal_moves)

    def _is_path_clear(self, from_pos: str, to_pos: str) -> bool:
        from_sq = chess.parse_square(from_pos)
        to_sq = chess.parse_square(to_pos)
        for sq in chess.SquareSet.between(from_sq, to_sq):
            if chess.square_name(sq) in self.pieces:
                return False
        return True

    def _is_en_passant_target(self, target: str) -> bool:
        if not self.last_move:
            return False
        from_pos, to_pos = self.last_move
        moved = self.pieces.get(to_pos)
        if not moved or moved.type != PieceType.PAWN:
            return False
        r_from = chess.square_rank(chess.parse_square(from_pos))
        r_to = chess.square_rank(chess.parse_square(to_pos))
        if abs(r_from - r_to) != 2:
            return False
        ep_rank = (r_from + r_to) // 2
        file = chess.square_file(chess.parse_square(to_pos))
        return chess.square_name(chess.square(file, ep_rank)) == target

    def move_piece(self, from_pos: str, to_pos: str) -> Dict[str, object]:
        board = self._to_chess_board()
        move = chess.Move.from_uci(from_pos + to_pos)
        if move not in board.legal_moves:
            if board.is_castling(move):
                return {"success": False, "error": "casa atacada durante o roque"}
            if self._move_exposes_check(from_pos, to_pos):
                return {"success": False, "error": "movimento expõe o rei ao xeque"}
            return {"success": False, "error": "movimento ilegal"}
        captured = board.piece_at(chess.parse_square(to_pos))
        moving_piece = self.pieces.get(from_pos)
        if not moving_piece:
            return {"success": False, "error": "sem peça na origem"}
        is_castle = board.is_castling(move)
        board.push(move)
        # update our representation
        self.pieces.pop(from_pos)
        self.pieces[to_pos] = moving_piece
        if is_castle:
            if to_pos == "g1":
                rook = self.pieces.pop("h1", None)
                if rook:
                    self.pieces["f1"] = rook
            elif to_pos == "c1":
                rook = self.pieces.pop("a1", None)
                if rook:
                    self.pieces["d1"] = rook
            elif to_pos == "g8":
                rook = self.pieces.pop("h8", None)
                if rook:
                    self.pieces["f8"] = rook
            elif to_pos == "c8":
                rook = self.pieces.pop("a8", None)
                if rook:
                    self.pieces["d8"] = rook
        if moving_piece.type == PieceType.PAWN and captured is None and from_pos[0] != to_pos[0]:
            # en passant capture
            captured_sq = to_pos[0] + from_pos[1]
            captured_piece = self.pieces.pop(captured_sq, None)
            if captured_piece:
                self.captured_pieces.append(captured_piece)
        if captured:
            self.captured_pieces.append(Piece(PieceType(captured.piece_type), Color(captured.color)))
        self.move_history.append((from_pos, to_pos))
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        self.last_move = (from_pos, to_pos)
        return {"success": True}

    # ------------------------------------------------------------------
    # Status helpers
    def is_in_check(self) -> bool:
        return self._to_chess_board().is_check()

    def is_checkmate(self) -> bool:
        return self._to_chess_board().is_checkmate()

    def is_stalemate(self) -> bool:
        board = self._to_chess_board()
        return board.is_stalemate() or board.is_insufficient_material()

