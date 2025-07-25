"""
Integrações com bibliotecas externas para o sistema narrativo.
"""
import chess
import spacy
from typing import Dict, List, Optional
import chess.engine
from dataclasses import dataclass

@dataclass
class MoveAnalysis:
    """Análise de um movimento."""
    move: chess.Move
    evaluation: float
    best_moves: List[chess.Move]
    tactical_themes: List[str]
    positional_themes: List[str]

class ChessAnalyzer:
    """Analisador de xadrez usando python-chess e Stockfish."""
    
    def __init__(self, stockfish_path: str = None):
        """
        Inicializa analisador.
        
        Args:
            stockfish_path: Caminho para executável do Stockfish
        """
        self.board = chess.Board()
        self.engine = None
        if stockfish_path:
            self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    
    def analyze_move(self, move: chess.Move, depth: int = 20) -> MoveAnalysis:
        """
        Analisa um movimento.
        
        Args:
            move: Movimento a ser analisado
            depth: Profundidade de análise
        
        Returns:
            Análise do movimento
        """
        # Avalia posição antes do movimento
        if self.engine:
            info = self.engine.analyse(self.board, chess.engine.Limit(depth=depth))
            eval_before = info['score'].relative.score()
        else:
            eval_before = 0
        
        # Faz o movimento
        self.board.push(move)
        
        # Avalia posição após o movimento
        if self.engine:
            info = self.engine.analyse(self.board, chess.engine.Limit(depth=depth))
            eval_after = info['score'].relative.score()
            best_moves = [m.move for m in info['pv'][:3]]
        else:
            eval_after = 0
            best_moves = []
        
        # Desfaz o movimento
        self.board.pop()
        
        # Identifica temas
        tactical_themes = self._identify_tactical_themes(move)
        positional_themes = self._identify_positional_themes(move)
        
        return MoveAnalysis(
            move=move,
            evaluation=eval_after - eval_before,
            best_moves=best_moves,
            tactical_themes=tactical_themes,
            positional_themes=positional_themes
        )
    
    def _identify_tactical_themes(self, move: chess.Move) -> List[str]:
        """Identifica temas táticos do movimento."""
        themes = []
        
        # Verifica captura
        if self.board.is_capture(move):
            themes.append("capture")
        
        # Verifica xeque
        self.board.push(move)
        if self.board.is_check():
            themes.append("check")
        self.board.pop()
        
        # Verifica fork (ataque duplo)
        if self._is_fork(move):
            themes.append("fork")
        
        # Verifica pin (pregadura)
        if self._is_pin(move):
            themes.append("pin")
        
        return themes
    
    def _identify_positional_themes(self, move: chess.Move) -> List[str]:
        """Identifica temas posicionais do movimento."""
        themes = []
        
        # Verifica controle do centro
        if self._controls_center(move):
            themes.append("center_control")
        
        # Verifica desenvolvimento de peça
        if self._is_development(move):
            themes.append("development")
        
        # Verifica estrutura de peões
        if self._affects_pawn_structure(move):
            themes.append("pawn_structure")
        
        return themes
    
    def _is_fork(self, move: chess.Move) -> bool:
        """Verifica se o movimento cria um fork."""
        # Implementar lógica de detecção de fork
        return False
    
    def _is_pin(self, move: chess.Move) -> bool:
        """Verifica se o movimento cria uma pin."""
        # Implementar lógica de detecção de pin
        return False
    
    def _controls_center(self, move: chess.Move) -> bool:
        """Verifica se o movimento controla o centro."""
        center_squares = {chess.E4, chess.D4, chess.E5, chess.D5}
        return move.to_square in center_squares
    
    def _is_development(self, move: chess.Move) -> bool:
        """Verifica se é um movimento de desenvolvimento."""
        piece = self.board.piece_at(move.from_square)
        if not piece:
            return False
        
        # Peças menores saindo da posição inicial
        if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            rank = chess.square_rank(move.from_square)
            return (piece.color == chess.WHITE and rank == 0) or \
                   (piece.color == chess.BLACK and rank == 7)
        
        return False
    
    def _affects_pawn_structure(self, move: chess.Move) -> bool:
        """Verifica se o movimento afeta a estrutura de peões."""
        piece = self.board.piece_at(move.from_square)
        return piece and piece.piece_type == chess.PAWN

class NarrativeGenerator:
    """Gerador de narrativas usando spaCy."""
    
    def __init__(self):
        """Inicializa gerador de narrativas."""
        self.nlp = spacy.load("pt_core_news_lg")
    
    def generate_move_description(self, analysis: MoveAnalysis, culture: str) -> str:
        """
        Gera descrição narrativa de um movimento.
        
        Args:
            analysis: Análise do movimento
            culture: Cultura atual
        
        Returns:
            Descrição narrativa
        """
        # Base description
        description = self._get_base_description(analysis)
        
        # Adiciona elementos culturais
        description = self._add_cultural_elements(description, culture)
        
        # Adiciona avaliação
        if abs(analysis.evaluation) > 100:
            description = self._add_evaluation(description, analysis.evaluation)
        
        # Adiciona temas
        if analysis.tactical_themes or analysis.positional_themes:
            description = self._add_themes(description, 
                                        analysis.tactical_themes,
                                        analysis.positional_themes)
        
        return description
    
    def _get_base_description(self, analysis: MoveAnalysis) -> str:
        """Gera descrição base do movimento."""
        move = analysis.move
        piece = chess.piece_name(chess.PIECE_TYPES.index(move.piece_type) + 1)
        from_square = chess.square_name(move.from_square)
        to_square = chess.square_name(move.to_square)
        
        return f"{piece} moves from {from_square} to {to_square}"
    
    def _add_cultural_elements(self, description: str, culture: str) -> str:
        """Adiciona elementos culturais à descrição."""
        doc = self.nlp(description)
        
        # Encontra substantivos principais
        nouns = [token for token in doc if token.pos_ == "NOUN"]
        
        # Adiciona adjetivos culturalmente apropriados
        if culture == "renaissance":
            adjectives = ["elegant", "harmonious", "masterful"]
        elif culture == "eastern":
            adjectives = ["flowing", "balanced", "precise"]
        elif culture == "nordic":
            adjectives = ["powerful", "brave", "fierce"]
        else:
            adjectives = ["strategic", "tactical", "skillful"]
        
        # Combina substantivos com adjetivos
        for noun in nouns:
            adj = random.choice(adjectives)
            description = description.replace(noun.text, f"{adj} {noun.text}")
        
        return description
    
    def _add_evaluation(self, description: str, evaluation: float) -> str:
        """Adiciona avaliação à descrição."""
        if evaluation > 200:
            return f"{description}, a brilliant move"
        elif evaluation > 100:
            return f"{description}, a strong move"
        elif evaluation < -200:
            return f"{description}, a serious mistake"
        elif evaluation < -100:
            return f"{description}, a questionable move"
        return description
    
    def _add_themes(self, description: str, 
                   tactical_themes: List[str],
                   positional_themes: List[str]) -> str:
        """Adiciona temas à descrição."""
        themes = []
        
        # Temas táticos
        if "check" in tactical_themes:
            themes.append("delivering check")
        if "capture" in tactical_themes:
            themes.append("winning material")
        if "fork" in tactical_themes:
            themes.append("creating a fork")
        if "pin" in tactical_themes:
            themes.append("establishing a pin")
        
        # Temas posicionais
        if "center_control" in positional_themes:
            themes.append("controlling the center")
        if "development" in positional_themes:
            themes.append("developing pieces")
        if "pawn_structure" in positional_themes:
            themes.append("improving pawn structure")
        
        if themes:
            theme_text = ", ".join(themes[:-1])
            if len(themes) > 1:
                theme_text += f" and {themes[-1]}"
            else:
                theme_text = themes[0]
            
            return f"{description}, {theme_text}"
        
        return description
