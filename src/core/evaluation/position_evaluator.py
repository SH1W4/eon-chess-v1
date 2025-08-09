from core.board.board import Board, PieceType, Color
from dataclasses import dataclass

@dataclass
class EvaluationResult:
    pontuacao_total: float
    pontuacao_material: float
    pontuacao_posicional: float
    influencia_quantica: float

class PositionEvaluator:
    def __init__(self):
        self.piece_values = {
            PieceType.PAWN: 1,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.ROOK: 5,
            PieceType.QUEEN: 9,
            PieceType.KING: 0  # O rei não tem valor material pois não pode ser capturado
        }

    def evaluate_position(self, board: Board) -> float:
        """Avalia a posição atual do tabuleiro.
        Retorna um valor positivo se as brancas estão melhor,
        negativo se as pretas estão melhor."""
        score = 0.0
        if not hasattr(board, 'pieces'):
            return score

        for piece in getattr(board, 'pieces', {}).values():
            if piece.type not in self.piece_values:
                continue
            value = self.piece_values[piece.type]
            if piece.color == Color.WHITE:
                score += value
            else:
                score -= value
        return score

    # Alias method for backward compatibility
    def avaliar(self, board: Board) -> EvaluationResult:
        """Compat wrapper expected by older tests (Portuguese naming).
        Returns an object with the fields used in legacy tests.
        """
        material = self.evaluate_position(board)
        # Simple placeholders; can be expanded to real positional/quantum metrics
        posicional = 0.0
        influencia = 0.0
        try:
            qf = getattr(board, 'quantum_field', None)
            if qf is not None:
                influencia = float(qf.get_control_score(Color.WHITE) - qf.get_control_score(Color.BLACK))
        except Exception:
            influencia = 0.0
        total = material + posicional + influencia
        return EvaluationResult(
            pontuacao_total=total,
            pontuacao_material=material,
            pontuacao_posicional=posicional,
            influencia_quantica=influencia,
        )

# Compat alias to satisfy tests referencing AvaliadorPosicao
AvaliadorPosicao = PositionEvaluator
