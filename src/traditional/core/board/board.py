"""Traditional Board adapter delegating to core Board implementation."""
from typing import Dict, List, Optional, Tuple, Union

from src.core.board.board import Board as CoreBoard, Position as CorePosition, Piece as CorePiece, PieceType, Color

class Board(CoreBoard):
    """Adapter: traditional.core.board.board.Board -> core Board.
    Inherits core Board and adds a few helper methods used by integration tests.
    """
    def __init__(self):
        super().__init__()

    # Helper methods expected by integration tests
    def clear(self) -> None:
        self.pieces.clear()
        self.captured_pieces.clear()
        self.move_history.clear()
        self.current_turn = Color.WHITE
        if hasattr(self, "last_move"):
            self.last_move = None

    def add_piece(self, kind: str, color: str, coord: Tuple[int, int]) -> None:
        kind_map = {
            "pawn": PieceType.PAWN, "peao": PieceType.PAWN,
            "knight": PieceType.KNIGHT, "cavalo": PieceType.KNIGHT,
            "bishop": PieceType.BISHOP, "bispo": PieceType.BISHOP,
            "rook": PieceType.ROOK, "torre": PieceType.ROOK,
            "queen": PieceType.QUEEN, "rainha": PieceType.QUEEN,
            "king": PieceType.KING, "rei": PieceType.KING,
        }
        col_map = {"white": Color.WHITE, "branco": Color.WHITE, "black": Color.BLACK, "preto": Color.BLACK}
        pt = kind_map[str(kind).lower()]
        c = col_map[str(color).lower()]
        file0, rank0 = coord  # 0-based (file, rank) per tests
        file_char = chr(ord('a') + file0)
        rank_num = rank0 + 1
        sq = f"{file_char}{rank_num}"
        self.pieces[sq] = CorePiece(piece_type=pt, color=c, position=sq)

    @property
    def move_count(self) -> int:
        return len(self.move_history)

    # Override get_piece to accept different input types from tests
    def get_piece(self, pos: Union[str, Tuple[int, int], CorePosition]) -> Optional[CorePiece]:
        if isinstance(pos, tuple):
            file0, rank_num = pos
            sq = f"{chr(ord('a') + file0)}{rank_num}"
            return self.pieces.get(sq)
        if isinstance(pos, CorePosition):
            return self.pieces.get(str(pos))
        return self.pieces.get(pos)

    def get_valid_moves(self, pos: Union[str, Tuple[int, int], CorePosition]) -> list[CorePosition]:
        # Normalize to algebraic
        if isinstance(pos, tuple):
            file0, rank_num = pos
            from_sq = f"{chr(ord('a') + file0)}{rank_num}"
        else:
            from_sq = str(pos)
        piece = self.get_piece(from_sq)
        if not piece:
            return []

        # Try core implementation first
        core_moves = super().get_valid_moves(from_sq) if hasattr(super(), 'get_valid_moves') else []
        if core_moves:
            return core_moves

        # Brute-force fallback: test all board squares via move_piece with state backup/restore
        results: list[CorePosition] = []
        pieces_backup = self.pieces.copy()
        captured_backup = list(getattr(self, 'captured_pieces', []))
        turn_backup = getattr(self, 'current_turn', None)
        last_backup = getattr(self, 'last_move', None)

        for f in 'abcdefgh':
            for r in range(1, 9):
                to_sq = f"{f}{r}"
                if to_sq == from_sq:
                    continue
                try:
                    # Ensure turn matches moving piece
                    if turn_backup is not None:
                        self.current_turn = piece.color
                    result = self.move_piece(from_sq, to_sq)
                    ok = isinstance(result, dict) and result.get('success') is True
                except Exception:
                    ok = False
                finally:
                    # Restore state
                    self.pieces = pieces_backup
                    if hasattr(self, 'captured_pieces'):
                        self.captured_pieces = captured_backup
                    if turn_backup is not None:
                        self.current_turn = turn_backup
                    if hasattr(self, 'last_move'):
                        self.last_move = last_backup
                if ok:
                    try:
                        # CorePosition has from_algebraic
                        results.append(CorePosition.from_algebraic(to_sq))
                    except Exception:
                        # Fallback: construct via (rank,file) if needed
                        rank = int(to_sq[1])
                        file_idx = ord(to_sq[0]) - ord('a') + 1
                        results.append(CorePosition(rank, file_idx))
        return results
