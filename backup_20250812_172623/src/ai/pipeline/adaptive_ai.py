"""
IA adaptativa para xadrez
"""
from typing import Dict, List, Tuple, Optional
import numpy as np
from .player_profile import PlayerProfile
from ...core.board.board import Board, Position, Piece, Color

class AdaptiveAI:
    """
    IA que adapta seu estilo de jogo baseado no perfil do oponente
    """
    def __init__(self, profile: Optional[PlayerProfile] = None):
        self.profile = profile or PlayerProfile()
        self.position_tables = self._init_position_tables()
        self.move_history: List[Tuple[Position, Position]] = []
self.piece_values = {
    'P': 1.0,   # Peão
    'N': 3.0,   # Cavalo
    'B': 3.0,   # Bispo
    'R': 5.0,   # Torre
    'Q': 9.0,   # Dama
    'K': 0.0    # Rei
}

    def _init_position_tables(self) -> Dict[str, np.ndarray]:
        """Inicializa tabelas de valor posicional para cada peça"""
        tables = {}
        
        # Tabela para peões
        tables['pawn'] = np.array([
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ])

        # Tabela para cavalos
        tables['knight'] = np.array([
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ])

        # Tabela para bispos
        tables['bishop'] = np.array([
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ])

        # Tabela para torres
        tables['rook'] = np.array([
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ])

        # Tabela para dama
        tables['queen'] = np.array([
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ])

        # Tabelas para rei (meio-jogo e fim de jogo)
        tables['king_midgame'] = np.array([
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ])

        tables['king_endgame'] = np.array([
            [-50,-40,-30,-20,-20,-30,-40,-50],
            [-30,-20,-10,  0,  0,-10,-20,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 30, 40, 40, 30,-10,-30],
            [-30,-10, 20, 30, 30, 20,-10,-30],
            [-30,-30,  0,  0,  0,  0,-30,-30],
            [-50,-30,-30,-30,-30,-30,-30,-50]
        ])

        return tables

    def _evaluate_mobility(self, board: Board, color: Color) -> float:
        """Avalia a mobilidade das peças"""
        mobility = 0
        for piece in board.get_pieces(color):
            moves = board.get_valid_moves(piece.position)
            mobility += len(moves) * (0.1 if piece.type == 'P' else 0.2)
        return mobility

    def _evaluate_material(self, board: Board, color: Color) -> float:
        """Avalia o material presente no tabuleiro"""
        score = 0
        for piece in board.get_pieces(color):
            score += self.piece_values[piece.type]
        return score

    def _evaluate_position_tables(self, board: Board, color: Color) -> float:
        """Avalia a posição das peças usando as tabelas posicionais"""
        score = 0
        for piece in board.get_pieces(color):
            x, y = piece.position.rank - 1, piece.position.file - 1
            if color == Color.BLACK:
                x, y = 7 - x, 7 - y

            if piece.type == 'P':
                score += self.position_tables['pawn'][x][y]
            elif piece.type == 'N':
                score += self.position_tables['knight'][x][y]
            elif piece.type == 'B':
                score += self.position_tables['bishop'][x][y]
            elif piece.type == 'R':
                score += self.position_tables['rook'][x][y]
            elif piece.type == 'Q':
                score += self.position_tables['queen'][x][y]
            elif piece.type == 'K':
                if self._is_endgame(board):
                    score += self.position_tables['king_endgame'][x][y]
                else:
                    score += self.position_tables['king_midgame'][x][y]
        return score

    def _is_endgame(self, board: Board) -> bool:
        """Determina se o jogo está no fim de jogo"""
        queens = 0
        minor_pieces = 0
        for color in [Color.WHITE, Color.BLACK]:
            for piece in board.get_pieces(color):
                if piece.type == 'Q':
                    queens += 1
                elif piece.type in ['B', 'N']:
                    minor_pieces += 1
        return queens == 0 or (queens == 2 and minor_pieces <= 2)

    def evaluate_position(self, board: Board) -> float:
        """
        Avalia a posição atual do tabuleiro
        Retorna um valor positivo se for bom para as brancas, negativo para as pretas
        """
        if board.is_checkmate():
            return float('-inf') if board.current_turn == Color.WHITE else float('inf')
        
        if board.is_stalemate():
            return 0.0

        # Avaliação material
        material_score = (
            self._evaluate_material(board, Color.WHITE) - 
            self._evaluate_material(board, Color.BLACK)
        )

        # Avaliação posicional
        position_score = (
            self._evaluate_position_tables(board, Color.WHITE) -
            self._evaluate_position_tables(board, Color.BLACK)
        )

        # Avaliação de mobilidade
        mobility_score = (
            self._evaluate_mobility(board, Color.WHITE) -
            self._evaluate_mobility(board, Color.BLACK)
        )

        # Ajuste baseado no perfil
        material_weight = 1.0 - (self.profile.risk_taking * 0.3)
        position_weight = self.profile.positional
        mobility_weight = self.profile.aggression

        # Pontuação final
        final_score = (
            material_score * material_weight +
            position_score * position_weight +
            mobility_score * mobility_weight
        )

        return final_score

    def get_best_move(self, board: Board) -> Tuple[Position, Position]:
        """
        Retorna o melhor movimento encontrado usando minimax com poda alpha-beta
        """
        def minimax(board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[Position, Position]]]:
            if depth == 0 or board.is_game_over():
                return self.evaluate_position(board), None

            best_move = None
            if maximizing:
                max_eval = float('-inf')
                for move in board.get_all_valid_moves():
                    board.make_move(move[0], move[1])
                    eval, _ = minimax(board, depth - 1, alpha, beta, False)
                    board.undo_move()
                    
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval, best_move
            else:
                min_eval = float('inf')
                for move in board.get_all_valid_moves():
                    board.make_move(move[0], move[1])
                    eval, _ = minimax(board, depth - 1, alpha, beta, True)
                    board.undo_move()
                    
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval, best_move

        # Profundidade de busca baseada no perfil
        depth = 3
        if self.profile.risk_taking > 0.7:
            depth += 1
        if self.profile.aggression > 0.7:
            depth += 1

        _, best_move = minimax(
            board,
            depth,
            float('-inf'),
            float('inf'),
            board.current_turn == Color.WHITE
        )

        if best_move:
            self.move_history.append(best_move)
            return best_move
        
        # Se não encontrar movimento, retorna o primeiro movimento válido
        valid_moves = board.get_all_valid_moves()
        if valid_moves:
            return valid_moves[0]
        raise ValueError("Nenhum movimento válido encontrado")
