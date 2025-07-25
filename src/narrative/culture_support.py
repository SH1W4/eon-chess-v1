"""
Módulo de suporte para culturas expandidas do sistema narrativo.
"""
from typing import Dict, List, Optional
import random
from dataclasses import dataclass
import yaml

@dataclass
class CulturalTheme:
    """Tema cultural com seus elementos."""
    name: str
    weight: float
    keywords: List[str]

@dataclass
class PieceRole:
    """Papel cultural de uma peça."""
    name: str
    roles: List[str]

class CultureManager:
    """Gerenciador de aspectos culturais do sistema."""
    
    def __init__(self, culture_path: str):
        """
        Inicializa gerenciador cultural.
        
        Args:
            culture_path: Caminho para arquivo de configuração cultural
        """
        self.cultures = self._load_cultures(culture_path)
        self.current_culture = None
        self.themes = {}
        self.narrative_patterns = {}
    
    def _load_cultures(self, path: str) -> Dict:
        """Carrega configurações culturais."""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)['chess_cultures']
    
    def set_culture(self, culture_name: str) -> None:
        """
        Define cultura ativa.
        
        Args:
            culture_name: Nome da cultura ('renaissance', 'eastern', 'nordic', etc)
        """
        if culture_name not in self.cultures:
            raise ValueError(f"Cultura '{culture_name}' não encontrada")
        
        self.current_culture = culture_name
        self._load_cultural_elements()
    
    def _load_cultural_elements(self) -> None:
        """Carrega elementos da cultura atual."""
        culture = self.cultures[self.current_culture]
        
        # Carrega temas
        self.themes = {
            theme['name']: CulturalTheme(
                name=theme['name'],
                weight=theme['weight'],
                keywords=theme['keywords']
            )
            for theme in culture['themes']
        }
        
        # Carrega padrões narrativos
        self.narrative_patterns = culture.get('narrative_patterns', {})
    
    def get_piece_description(self, piece_type: str) -> PieceRole:
        """
        Retorna descrição cultural de uma peça.
        
        Args:
            piece_type: Tipo da peça ('pawn', 'knight', etc)
        
        Returns:
            Papel cultural da peça
        """
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        piece_data = self.cultures[self.current_culture]['piece_metaphors'].get(piece_type)
        if not piece_data:
            return PieceRole(piece_type, [piece_type])
        
        return PieceRole(
            name=piece_data['name'],
            roles=piece_data['roles']
        )
    
    def get_narrative_template(self, context: str) -> str:
        """
        Retorna template narrativo culturalmente apropriado.
        
        Args:
            context: Contexto do template ('advance', 'capture', etc)
        
        Returns:
            Template narrativo
        """
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        patterns = self.cultures[self.current_culture]['narrative_patterns']
        if context not in patterns:
            return "{piece} move to {square}"
        
        return random.choice(patterns[context])
    
    def get_cultural_flavor(self, text: str) -> str:
        """
        Adiciona elementos culturais a um texto.
        
        Args:
            text: Texto base
        
        Returns:
            Texto com elementos culturais
        """
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        # Seleciona tema relevante
        theme = random.choice(list(self.themes.values()))
        
        # Adiciona palavra-chave do tema
        keyword = random.choice(theme.keywords)
        
        return f"{text} com {keyword}"
    
    def get_phase_description(self, phase: str) -> str:
        """
        Retorna descrição cultural para fase do jogo.
        
        Args:
            phase: Fase do jogo ('opening', 'middlegame', 'endgame')
        
        Returns:
            Descrição da fase
        """
        if not self.current_culture:
            raise ValueError("Cultura não definida")
        
        patterns = self.cultures[self.current_culture]['narrative_patterns']
        if phase not in patterns.get('phases', {}):
            return f"Fase: {phase}"
        
        return random.choice(patterns['phases'][phase])

class NarrativeEnhancer:
    """Aprimorador de narrativas com elementos culturais."""
    
    def __init__(self, culture_manager: CultureManager):
        """
        Inicializa aprimorador.
        
        Args:
            culture_manager: Gerenciador cultural
        """
        self.culture = culture_manager
    
    def enhance_move_description(self, description: str, context: Dict) -> str:
        """
        Aprimora descrição de movimento.
        
        Args:
            description: Descrição base
            context: Contexto do movimento
        
        Returns:
            Descrição aprimorada
        """
        # Adiciona elemento cultural
        enhanced = self.culture.get_cultural_flavor(description)
        
        # Adiciona referência a tema se apropriado
        if context.get('significance', 0) > 0.7:
            theme = random.choice(list(self.culture.themes.values()))
            enhanced = f"{enhanced}, demonstrando {theme.name}"
        
        return enhanced
    
    def enhance_pattern_description(self, pattern: str, significance: float) -> str:
        """
        Aprimora descrição de padrão.
        
        Args:
            pattern: Descrição do padrão
            significance: Significância do padrão
        
        Returns:
            Descrição aprimorada
        """
        # Base enhancement
        enhanced = self.culture.get_cultural_flavor(pattern)
        
        # Adiciona ênfase baseada na significância
        if significance > 0.8:
            theme = random.choice(list(self.culture.themes.values()))
            enhanced = f"{enhanced}, um momento de {theme.name}"
        
        return enhanced
    
    def generate_cultural_commentary(self, position_evaluation: float) -> str:
        """
        Gera comentário cultural sobre a posição.
        
        Args:
            position_evaluation: Avaliação da posição (-1.0 a 1.0)
        
        Returns:
            Comentário cultural
        """
        themes = list(self.culture.themes.values())
        
        if position_evaluation > 0.5:
            theme = max(themes, key=lambda t: t.weight)
            return f"A posição reflete {theme.name} supremo"
        elif position_evaluation < -0.5:
            theme = min(themes, key=lambda t: t.weight)
            return f"A posição carece de {theme.name}"
        else:
            theme = random.choice(themes)
            return f"A posição mantém {theme.name} em equilíbrio"
