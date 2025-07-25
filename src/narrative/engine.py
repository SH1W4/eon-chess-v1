"""
Motor principal do sistema narrativo de xadrez.
"""
from typing import List, Dict, Optional
import random
from dataclasses import dataclass
from .base import BaseNarrative, ChessPattern, GameState
from .patterns import PatternMatcher, Board, Position, Piece

@dataclass
class MoveContext:
    """Contexto de um movimento para narrativa."""
    piece: str
    from_square: str
    to_square: str
    is_capture: bool
    is_check: bool
    is_checkmate: bool
    captured_piece: Optional[str]
    promotion: Optional[str]
    is_castling: bool
    patterns: List[ChessPattern]

class NarrativeEngine:
    """Motor principal do sistema narrativo."""
    
    def __init__(self, 
                 config_path: str,
                 patterns_path: str,
                 history_path: str,
                 culture: str = 'medieval'):
        """
        Inicializa o motor narrativo.
        
        Args:
            config_path: Caminho para arquivo de configuração
            patterns_path: Caminho para arquivo de padrões
            history_path: Caminho para arquivo de história
            culture: Cultura inicial ('medieval' ou 'futuristic')
        """
        self.narrative = BaseNarrative(config_path)
        self.pattern_matcher = PatternMatcher(patterns_path)
        self.narrative.set_culture(culture)
        self.game_state = GameState(
            phase='opening',
            move_number=1,
            white_advantage=0.0,
            patterns=[],
            last_move=None
        )
    
    def generate_move_narrative(self, context: MoveContext) -> str:
        """
        Gera narrativa para um movimento.
        
        Args:
            context: Contexto do movimento
        
        Returns:
            Narrativa gerada
        """
        # Atualiza estado do jogo
        self._update_game_state(context)
        
        # Seleciona template base
        template = self._select_move_template(context)
        
        # Prepara dados para o template
        data = self._prepare_template_data(context)
        
        # Gera narrativa base
        narrative = template.format(**data)
        
        # Adiciona contexto de padrões
        pattern_narrative = self._generate_pattern_narrative(context.patterns)
        if pattern_narrative:
            narrative = f"{narrative} {pattern_narrative}"
        
        return narrative
    
    def _update_game_state(self, context: MoveContext) -> None:
        """Atualiza estado do jogo."""
        self.game_state.move_number += 1
        
        # Atualiza fase do jogo
        if self.game_state.move_number <= 10:
            self.game_state.phase = 'opening'
        elif self.game_state.move_number <= 30:
            self.game_state.phase = 'middlegame'
        else:
            self.game_state.phase = 'endgame'
        
        # Atualiza padrões
        self.game_state.patterns = context.patterns
        
        # Registra último movimento
        self.game_state.last_move = f"{context.from_square}-{context.to_square}"
    
    def _select_move_template(self, context: MoveContext) -> str:
        """Seleciona template apropriado para o movimento."""
        if context.is_checkmate:
            return self.narrative.get_move_template('checkmate')
        elif context.is_check:
            return self.narrative.get_move_template('check')
        elif context.is_capture:
            return self.narrative.get_move_template('capture')
        elif context.is_castling:
            return self.narrative.get_move_template('castle')
        else:
            return self.narrative.get_move_template('advance')
    
    def _prepare_template_data(self, context: MoveContext) -> Dict:
        """Prepara dados para o template."""
        data = {
            'piece': self.narrative.get_piece_description(context.piece),
            'from_square': context.from_square,
            'to_square': context.to_square
        }
        
        if context.is_capture:
            data['captured'] = self.narrative.get_piece_description(context.captured_piece)
        
        if context.promotion:
            data['promotion'] = self.narrative.get_piece_description(context.promotion)
        
        return data
    
    def _generate_pattern_narrative(self, patterns: List[ChessPattern]) -> Optional[str]:
        """Gera narrativa para padrões identificados."""
        if not patterns:
            return None
        
        # Ordena padrões por significância
        sorted_patterns = sorted(patterns, key=lambda p: p.significance, reverse=True)
        
        # Seleciona padrão mais significativo
        main_pattern = sorted_patterns[0]
        
        if main_pattern.type == 'tactical':
            templates = self.narrative.culture_config['tactical_templates']
        else:
            templates = self.narrative.culture_config['strategic_templates']
        
        pattern_template = random.choice(templates)
        return pattern_template.format(
            pattern=main_pattern.name,
            description=main_pattern.description
        )
    
    def generate_position_narrative(self, board: Board) -> str:
        """
        Gera narrativa para a posição atual.
        
        Args:
            board: Estado atual do tabuleiro
        
        Returns:
            Narrativa da posição
        """
# Atualiza último movimento no tabuleiro
        if board.move_stack:
            self.game_state.last_move = board.peek().uci()

        # Analisa padrões na posição
        patterns = self.pattern_matcher.analyze_position(board)

        # Seleciona template base na fase atual
        phase_template = self.narrative.culture_config['phases'][self.game_state.phase]
        
        # Gera narrativa base
        narrative = random.choice(phase_template)
        
        # Adiciona contexto de padrões
        pattern_narrative = self._generate_pattern_narrative(patterns)
        if pattern_narrative:
            narrative = f"{narrative} {pattern_narrative}"
        
        return narrative
    
    def generate_game_state_narrative(self) -> str:
        """
        Gera narrativa para o estado atual do jogo.
        
        Returns:
            Narrativa do estado do jogo
        """
        templates = self.narrative.culture_config['game_states']
        
        if self.game_state.white_advantage > 2.0:
            state = 'white_winning'
        elif self.game_state.white_advantage < -2.0:
            state = 'black_winning'
        else:
            state = 'equal'
        
        template = random.choice(templates[state])
        return template.format(
            phase=self.game_state.phase,
            move=self.game_state.move_number
        )
    
    def switch_culture(self, culture: str) -> None:
        """
        Alterna entre culturas narrativas.
        
        Args:
            culture: Nova cultura ('medieval' ou 'futuristic')
        """
        self.narrative.set_culture(culture)
