"""
Integração avançada para análise de xadrez com conceitos NEXUS/ARQUIMAX.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
import chess
import chess.engine
from .integrations import ChessAnalyzer, NarrativeGenerator
from .culture_support import CultureManager

@dataclass
class PositionalAnalysis:
    """Análise posicional detalhada."""
    space_control: float  # 0.0 a 1.0
    piece_coordination: float
    king_safety: float
    pawn_structure: float
    center_control: float
    tactical_opportunities: float

@dataclass
class StrategicContext:
    """Contexto estratégico da posição."""
    phase: str  # opening, middlegame, endgame
    initiative: float  # -1.0 (black) a 1.0 (white)
    tension: float  # 0.0 a 1.0
    dynamics: float  # 0.0 (static) a 1.0 (dynamic)
    complexity: float  # 0.0 (simple) a 1.0 (complex)

class AdvancedChessAnalyzer:
    """Analisador avançado de xadrez com integração NEXUS/ARQUIMAX."""
    
    def __init__(self,
                 stockfish_path: str,
                 culture_path: str,
                 learning_mode: str = "passive",
                 evolution_cycles: int = 1):
        """
        Inicializa analisador avançado.
        
        Args:
            stockfish_path: Caminho para Stockfish
            culture_path: Caminho para configurações culturais
            learning_mode: Modo de aprendizado (passive, active, aggressive)
            evolution_cycles: Número de ciclos evolutivos
        """
        self.analyzer = ChessAnalyzer(stockfish_path)
        self.narrator = NarrativeGenerator()
        self.culture = CultureManager(culture_path)
        self.learning_mode = learning_mode
        self.evolution_cycles = evolution_cycles
        self.position_cache = {}
    
    def analyze_position(self, board: chess.Board) -> Dict:
        """
        Realiza análise profunda da posição.
        
        Args:
            board: Tabuleiro atual
        
        Returns:
            Análise completa da posição
        """
        # Cache key
        fen = board.fen()
        if fen in self.position_cache:
            return self.position_cache[fen]
        
        # Análise posicional
        positional = self._analyze_positional_factors(board)
        
        # Contexto estratégico
        context = self._determine_strategic_context(board)
        
        # Análise de engine
        engine_analysis = self._get_engine_analysis(board)
        
        # Integra resultados
        analysis = {
            'positional': positional,
            'strategic': context,
            'engine': engine_analysis,
            'evaluation': self._calculate_final_evaluation(
                positional, context, engine_analysis
            )
        }
        
        # Cache result
        self.position_cache[fen] = analysis
        return analysis
    
    def generate_narrative(self, 
                         board: chess.Board,
                         move: chess.Move,
                         culture: str) -> str:
        """
        Gera narrativa avançada para um movimento.
        
        Args:
            board: Tabuleiro atual
            move: Movimento a analisar
            culture: Cultura narrativa
        
        Returns:
            Narrativa culturalmente apropriada
        """
        # Análise básica
        basic_analysis = self.analyzer.analyze_move(move)
        
        # Análise avançada
        advanced_analysis = self.analyze_position(board)
        
        # Prepara contexto cultural
        self.culture.set_culture(culture)
        
        # Gera narrativa base
        base_narrative = self.narrator.generate_move_description(
            basic_analysis, culture
        )
        
        # Enriquece com contexto estratégico
        enriched = self._enrich_narrative(
            base_narrative,
            advanced_analysis,
            culture
        )
        
        return enriched
    
    def _analyze_positional_factors(self, board: chess.Board) -> PositionalAnalysis:
        """Analisa fatores posicionais."""
        return PositionalAnalysis(
            space_control=self._calculate_space_control(board),
            piece_coordination=self._calculate_coordination(board),
            king_safety=self._calculate_king_safety(board),
            pawn_structure=self._analyze_pawn_structure(board),
            center_control=self._calculate_center_control(board),
            tactical_opportunities=self._find_tactical_opportunities(board)
        )
    
    def _determine_strategic_context(self, board: chess.Board) -> StrategicContext:
        """Determina contexto estratégico."""
        return StrategicContext(
            phase=self._determine_game_phase(board),
            initiative=self._calculate_initiative(board),
            tension=self._calculate_tension(board),
            dynamics=self._calculate_dynamics(board),
            complexity=self._calculate_complexity(board)
        )
    
    def _get_engine_analysis(self, board: chess.Board) -> Dict:
        """Obtém análise da engine."""
        info = self.analyzer.engine.analyse(
            board,
            chess.engine.Limit(depth=20, time=1.0)
        )
        return {
            'score': info['score'].relative.score(),
            'depth': info['depth'],
            'pv': [move.uci() for move in info.get('pv', [])]
        }
    
    def _calculate_final_evaluation(self,
                                  positional: PositionalAnalysis,
                                  strategic: StrategicContext,
                                  engine: Dict) -> float:
        """Calcula avaliação final combinando todos os fatores."""
        # Peso base da engine
        base_eval = engine['score'] / 100.0 if engine['score'] else 0.0
        
        # Ajuste posicional
        positional_factor = (
            positional.space_control * 0.2 +
            positional.piece_coordination * 0.2 +
            positional.king_safety * 0.3 +
            positional.center_control * 0.2 +
            positional.tactical_opportunities * 0.1
        )
        
        # Ajuste estratégico
        strategic_factor = (
            abs(strategic.initiative) * 0.3 +
            strategic.tension * 0.3 +
            strategic.dynamics * 0.2 +
            strategic.complexity * 0.2
        )
        
        # Combinação final
        return base_eval * (1.0 + positional_factor) * strategic_factor
    
    def _enrich_narrative(self,
                         base_narrative: str,
                         analysis: Dict,
                         culture: str) -> str:
        """Enriquece narrativa com contexto estratégico."""
        strategic = analysis['strategic']
        positional = analysis['positional']
        
        # Adiciona contexto de fase
        phase_context = self.culture.get_phase_description(strategic.phase)
        
        # Adiciona elementos posicionais relevantes
        if positional.tactical_opportunities > 0.7:
            tactical = self.culture.get_cultural_flavor("oportunidades táticas surgem")
            base_narrative = f"{base_narrative} enquanto {tactical}"
        
        # Adiciona tensão estratégica
        if strategic.tension > 0.8:
            tension = self.culture.get_cultural_flavor("a tensão aumenta")
            base_narrative = f"{base_narrative}; {tension}"
        
        return f"{phase_context}. {base_narrative}"
    
    # Métodos auxiliares de análise
    def _calculate_space_control(self, board: chess.Board) -> float:
        """Calcula controle de espaço."""
        # Implementar cálculo de controle de espaço
        return 0.5
    
    def _calculate_coordination(self, board: chess.Board) -> float:
        """Calcula coordenação de peças."""
        # Implementar cálculo de coordenação
        return 0.5
    
    def _calculate_king_safety(self, board: chess.Board) -> float:
        """Calcula segurança do rei."""
        # Implementar cálculo de segurança
        return 0.5
    
    def _analyze_pawn_structure(self, board: chess.Board) -> float:
        """Analisa estrutura de peões."""
        # Implementar análise de peões
        return 0.5
    
    def _calculate_center_control(self, board: chess.Board) -> float:
        """Calcula controle do centro."""
        # Implementar cálculo de controle central
        return 0.5
    
    def _find_tactical_opportunities(self, board: chess.Board) -> float:
        """Encontra oportunidades táticas."""
        # Implementar busca de táticas
        return 0.5
    
    def _determine_game_phase(self, board: chess.Board) -> str:
        """Determina fase do jogo."""
        # Implementar determinação de fase
        return "middlegame"
    
    def _calculate_initiative(self, board: chess.Board) -> float:
        """Calcula iniciativa."""
        # Implementar cálculo de iniciativa
        return 0.0
    
    def _calculate_tension(self, board: chess.Board) -> float:
        """Calcula tensão posicional."""
        # Implementar cálculo de tensão
        return 0.5
    
    def _calculate_dynamics(self, board: chess.Board) -> float:
        """Calcula dinamismo da posição."""
        # Implementar cálculo de dinamismo
        return 0.5
    
    def _calculate_complexity(self, board: chess.Board) -> float:
        """Calcula complexidade da posição."""
        # Implementar cálculo de complexidade
        return 0.5
