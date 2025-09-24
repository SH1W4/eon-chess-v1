"""
Gerenciamento do estado do jogo de xadrez.
"""

from enum import Enum
from typing import List, Optional, Tuple
from .board import Board, Color, Piece

class GameState(Enum):
    ACTIVE = "active"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_player = Color.WHITE
        self.state = GameState.ACTIVE
        self.move_history: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        
    def switch_player(self):
        """Alterna o jogador atual."""
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Realiza um movimento no jogo.
        Retorna True se o movimento foi válido e bem-sucedido.
        """
        if not self._is_valid_move(from_pos, to_pos):
            return False
            
        # Executa o movimento
        if self.board.move_piece(from_pos, to_pos):
            self.move_history.append((from_pos, to_pos))
            self.switch_player()
            self._update_game_state()
            return True
            
        return False
        
    def _is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Verifica se um movimento é válido."""
        from_row, from_col = from_pos
        piece = self.board.get_piece(from_row, from_col)
        
        if piece is None or piece.color != self.current_player:
            return False
            
        # TODO: Implementar regras específicas de movimento para cada tipo de peça
        return True
        
    def _update_game_state(self):
        """Atualiza o estado do jogo após cada movimento."""
        # TODO: Implementar lógica para detectar check, checkmate, stalemate e draw
        pass
        
    def get_possible_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retorna todos os movimentos possíveis para uma peça."""
        # TODO: Implementar lógica para cada tipo de peça
        return []
        
    def is_game_over(self) -> bool:
        """Verifica se o jogo acabou."""
        return self.state in [GameState.CHECKMATE, GameState.STALEMATE, GameState.DRAW]
        
    def get_winner(self) -> Optional[Color]:
        """Retorna o vencedor do jogo, se houver."""
        if self.state == GameState.CHECKMATE:
            return Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        return None
