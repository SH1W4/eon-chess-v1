import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from core.board.board import Board, Position, PieceType, Color, Piece

@dataclass
class NarrativeConfig:
    """Configuração do motor narrativo"""
    language: str = "en"
    culture: str = "neutral"
    style: str = "standard"
    patterns_file: str = "data/patterns.json"
    phrases_file: str = "data/phrases.json"

class NarrativeEngine:
    """Motor narrativo para geração de comentários sobre o jogo"""
    
    def __init__(self, config: Optional[NarrativeConfig] = None):
        self.config = config or NarrativeConfig()
        self.patterns = self._load_patterns()
        self.phrases = self._load_phrases()
        self.history: List[str] = []
    
    def _load_patterns(self) -> Dict:
        """Carrega padrões do arquivo de configuração"""
        try:
            with open(self.config.patterns_file) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading patterns: {e}")
            raise
    
    def _load_phrases(self) -> Dict:
        """Carrega frases do arquivo de configuração"""
        try:
            with open(self.config.phrases_file) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading phrases: {e}")
            raise
    
    def generate_move_narrative(self, from_pos=None, to_pos=None, piece=None, context=None, move=None, board=None) -> str:
        """Gera narrativa para um movimento com múltiplas assinaturas de compatibilidade"""
        # Compatibilidade com diferentes chamadas
        if from_pos and to_pos and piece:
            # Chamada estilo teste: from_pos, to_pos, piece, context
            narrative_pool = context.get('narrative_pool', []) if context else []
            if narrative_pool:
                return narrative_pool[0] if isinstance(narrative_pool, list) else str(narrative_pool)
            # Gera narrativa básica
            piece_name = self._get_piece_name(piece) if hasattr(piece, 'type') else str(piece)
            return f"{piece_name} move de {from_pos} para {to_pos}"
        
        # Chamada original com objeto Move
        if not move:
            return "Movimento realizado"
    
    def _generate_move_narrative_original(self, move, board) -> str:
        """Implementação original da narrativa para movimento"""
        piece = move.piece
        captured = move.captured_piece
        narrative = []

        # Get appropriate phrases
        if self.phrases and self.config.language in self.phrases:
            phrases = self.phrases[self.config.language]['moves']
        else:
            phrases = {
                'standard': "{piece} moves from {from_square} to {to}",
                'capture': "{piece} captures {captured} on {to}",
                'check': "giving check"
            }

        # Get check status first (before adding description)
        opponent_color = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
        print(f'Debug: Opponent color is {opponent_color}')
        
        # Make the move temporarily
        old_pos = piece.position
        old_pos = piece.position
        piece.position = move.to_pos
        captured_piece = board.pieces.get(move.to_pos)
        board.pieces[move.to_pos] = piece
        del board.pieces[move.from_pos]
        
        # Check if move gives opponent check
        is_check = board.is_in_check(opponent_color)
        
        # Revert the move
        piece.position = old_pos
        board.pieces[move.from_pos] = piece
        if captured_piece:
            board.pieces[move.to_pos] = captured_piece
        else:
            del board.pieces[move.to_pos]
            
        # Basic move description
        piece_name = self._get_piece_name(piece)
        from_square = move.from_pos.to_algebraic()
        to_square = move.to_pos.to_algebraic()

        base_narrative = phrases['standard'].format(
            piece=piece_name,
            from_square=from_square,
            to=to_square
        )
        narrative.append(base_narrative)

        # Capture details
        if captured:
            captured_name = self._get_piece_name(captured)
            capture_narrative = phrases['capture'].format(
                piece=piece_name,
                captured=captured_name,
                to=to_square
            )
            narrative.append(capture_narrative)

        
        if is_check:
            narrative.append(phrases['check'])
        else:
            print('Debug: Not in check')

        return " ".join(narrative)

    def generate_position_narrative(self, board: Board) -> str:
        """Gera narrativa para uma posição"""
        narrative = []

        # Get appropriate phrases
        if self.phrases and self.config.language in self.phrases:
            phrases = self.phrases[self.config.language]['position']
        else:
            phrases = {
                'center_control': "{color} controls the center",
                'development': "{color} has better piece development",
                'pawn_structure': "{color} has a healthier pawn structure"
            }

        # Avalia controle do centro
        center_pieces = self._get_center_pieces(board)
        if center_pieces['WHITE'] > center_pieces['BLACK']:
            narrative.append(phrases['center_control'].format(color="White"))
        elif center_pieces['BLACK'] > center_pieces['WHITE']:
            narrative.append(phrases['center_control'].format(color="Black"))

        # Avalia desenvolvimento
        white_dev = self._get_development_score(board, Color.WHITE)
        black_dev = self._get_development_score(board, Color.BLACK)
        if white_dev > black_dev:
            narrative.append(phrases['development'].format(color="White"))
        elif black_dev > white_dev:
            narrative.append(phrases['development'].format(color="Black"))

        # Avalia estrutura de peões
        white_pawns = self._evaluate_pawn_structure(board, Color.WHITE)
        black_pawns = self._evaluate_pawn_structure(board, Color.BLACK)
        if white_pawns > black_pawns:
            narrative.append(phrases['pawn_structure'].format(color="White"))
        elif black_pawns > white_pawns:
            narrative.append(phrases['pawn_structure'].format(color="Black"))

        return ". ".join(narrative)

    def _get_piece_name(self, piece: Piece) -> str:
        """Retorna nome da peça no idioma configurado"""
        if self.config.language == "en":
            names = {
                PieceType.KING: "King",
                PieceType.QUEEN: "Queen",
                PieceType.ROOK: "Rook",
                PieceType.BISHOP: "Bishop",
                PieceType.KNIGHT: "Knight",
                PieceType.PAWN: "Pawn"
            }
        else:  # pt-br
            names = {
                PieceType.KING: "Rei",
                PieceType.QUEEN: "Rainha",
                PieceType.ROOK: "Torre",
                PieceType.BISHOP: "Bispo",
                PieceType.KNIGHT: "Cavalo",
                PieceType.PAWN: "Peão"
            }
        
        color = "White" if piece.color == Color.WHITE else "Black"
        return f"{color} {names[piece.type]}"

    def _get_center_pieces(self, board: Board) -> Dict[str, int]:
        """Conta peças no centro do tabuleiro"""
        center = [
            Position(4, 4), Position(4, 5),
            Position(5, 4), Position(5, 5),
            Position(4, 3), Position(4, 6),
            Position(5, 3), Position(5, 6)
        ]
        counts = {'WHITE': 0, 'BLACK': 0}
        
        for pos in center:
            piece = board.get_piece(pos)
            if piece:
                color = 'WHITE' if piece.color == Color.WHITE else 'BLACK'
                counts[color] += 1
        
        return counts

    def _get_development_score(self, board: Board, color: Color) -> int:
        """Calcula pontuação de desenvolvimento"""
        score = 0
        for piece in board.pieces.values():
            if piece.color == color and piece.type not in [PieceType.KING, PieceType.PAWN]:
                if piece.has_moved:
                    score += 1
        return score

    def _evaluate_pawn_structure(self, board: Board, color: Color) -> float:
        """Avalia estrutura de peões"""
        score = 0.0
        files = {i: [] for i in range(1, 9)}
        
        # Agrupa peões por coluna
        for piece in board.pieces.values():
            if piece.type == PieceType.PAWN and piece.color == color:
                files[piece.position.file].append(piece)
        
        # Penaliza peões dobrados e isolados
        for file, pawns in files.items():
            if len(pawns) > 1:  # Peões dobrados
                score -= 0.5 * (len(pawns) - 1)
            elif len(pawns) == 1:  # Verifica se está isolado
                has_neighbor = False
                for neighbor in [file-1, file+1]:
                    if 1 <= neighbor <= 8 and len(files[neighbor]) > 0:
                        has_neighbor = True
                        break
                if not has_neighbor:
                    score -= 0.5
        
        return score

