from core.board.board import Board, PieceType, Color

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
            
        for piece in board.pieces.values():
            if piece.type not in self.piece_values:
                continue
            
            value = self.piece_values[piece.type]
            if piece.color == Color.WHITE:
                score += value
            else:
                score -= value
                
        return score
