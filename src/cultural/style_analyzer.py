from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.board.board import Board, Piece, PieceType, Color
from cultural.culture_framework import ChessCulture
from cultural.memory import CulturalMemory

@dataclass
class PlayStyle:
    """Define um estilo de jogo"""
    name: str
    description: str
    characteristics: Dict[str, float]  # Ex: {"aggression": 0.8, "defense": 0.3}
    cultural_alignment: Dict[str, float]  # Alinhamento com diferentes culturas
    
    def __lt__(self, other) -> bool:
        """Implementa comparação para ordenação"""
        if not isinstance(other, PlayStyle):
            return NotImplemented
        
        # Compara baseado na média das características
        self_avg = sum(self.characteristics.values()) / len(self.characteristics)
        other_avg = sum(other.characteristics.values()) / len(other.characteristics)
        return self_avg < other_avg

@dataclass
class StyleAnalysis:
    """Resultado da análise de estilo"""
    primary_style: PlayStyle
    secondary_style: Optional[PlayStyle]
    cultural_expression: float  # 0-1, quão bem expressa a cultura
    style_consistency: float   # 0-1, consistência do estilo
    notable_patterns: List[str]
    recommendations: List[str]

class CulturalStyleAnalyzer:
    """Analisa o estilo de jogo em relação à cultura"""
    
    def __init__(self):
        self.play_styles = self._init_play_styles()
        
    def _init_play_styles(self) -> Dict[str, PlayStyle]:
        """Inicializa os estilos de jogo básicos"""
        return {
            "aggressive": PlayStyle(
                name="Agressivo",
                description="Focado em ataque e pressão constante",
                characteristics={
                    "aggression": 0.9,
                    "defense": 0.3,
                    "mobility": 0.8,
                    "development": 0.7
                },
                cultural_alignment={
                    "mongol": 0.9,    # Forte alinhamento com estilo mongol
                    "viking": 0.8,    # Bom alinhamento com vikings
                    "persian": 0.5,   # Alinhamento moderado
                    "chinese": 0.4,   # Baixo alinhamento
                    "byzantine": 0.5   # Alinhamento moderado
                }
            ),
            "defensive": PlayStyle(
                name="Defensivo",
                description="Focado em posições sólidas e contra-ataque",
                characteristics={
                    "aggression": 0.3,
                    "defense": 0.9,
                    "mobility": 0.5,
                    "development": 0.6
                },
                cultural_alignment={
                    "chinese": 0.8,    # Forte alinhamento
                    "byzantine": 0.7,  # Bom alinhamento
                    "persian": 0.6,    # Alinhamento moderado
                    "mongol": 0.3,     # Baixo alinhamento
                    "viking": 0.4      # Baixo alinhamento
                }
            ),
            "strategic": PlayStyle(
                name="Estratégico",
                description="Focado em planos de longo prazo e posição",
                characteristics={
                    "aggression": 0.5,
                    "defense": 0.7,
                    "mobility": 0.6,
                    "development": 0.9
                },
                cultural_alignment={
                    "persian": 0.9,    # Forte alinhamento
                    "chinese": 0.8,    # Bom alinhamento
                    "byzantine": 0.8,  # Bom alinhamento
                    "mongol": 0.5,     # Alinhamento moderado
                    "viking": 0.4      # Baixo alinhamento
                }
            ),
            "tactical": PlayStyle(
                name="Tático",
                description="Focado em combinações e táticas diretas",
                characteristics={
                    "aggression": 0.7,
                    "defense": 0.5,
                    "mobility": 0.8,
                    "development": 0.7
                },
                cultural_alignment={
                    "mongol": 0.8,     # Forte alinhamento
                    "viking": 0.7,     # Bom alinhamento
                    "persian": 0.7,    # Bom alinhamento
                    "chinese": 0.6,    # Alinhamento moderado
                    "byzantine": 0.6   # Alinhamento moderado
                }
            )
        }
    
    def analyze_game_style(self, memory: CulturalMemory, culture: ChessCulture) -> StyleAnalysis:
        """Analisa o estilo de jogo baseado no histórico"""
        # Calcula características do jogo
        game_characteristics = self._calculate_game_characteristics(memory)
        
        # Encontra os estilos mais próximos
        styles = self._find_matching_styles(game_characteristics, culture)
        
        # Analisa padrões notáveis
        patterns = self._analyze_patterns(memory, culture)
        
        # Gera recomendações
        recommendations = self._generate_recommendations(
            game_characteristics, 
            styles[0], 
            culture
        )
        
        return StyleAnalysis(
            primary_style=styles[0],
            secondary_style=styles[1] if len(styles) > 1 else None,
            cultural_expression=self._calculate_cultural_expression(
                game_characteristics, 
                culture
            ),
            style_consistency=self._calculate_style_consistency(memory),
            notable_patterns=patterns,
            recommendations=recommendations
        )
    
    def _calculate_game_characteristics(self, memory: CulturalMemory) -> Dict[str, float]:
        """Calcula características do jogo baseado no histórico"""
        moves = memory.moves_history
        
        # Inicializa métricas
        characteristics = {
            "aggression": 0.0,
            "defense": 0.0,
            "mobility": 0.0,
            "development": 0.0
        }
        
        if not moves:
            return characteristics
            
        # Análise de desenvolvimento
        unique_pieces = set()
        for m in moves:
            piece_key = (m['piece_type'], m['piece_color'])
            unique_pieces.add(piece_key)
        characteristics['development'] = min(len(unique_pieces) / 6, 1.0)  # 6 tipos de peças

        # Análise de mobilidade (baseada na distância das casas)
        total_distance = 0
        for m in moves:
            from_rank = int(m['from_pos'][1])
            from_file = ord(m['from_pos'][0]) - ord('a')
            to_rank = int(m['to_pos'][1])
            to_file = ord(m['to_pos'][0]) - ord('a')
            distance = abs(from_rank - to_rank) + abs(from_file - to_file)
            total_distance += distance
        characteristics['mobility'] = min(total_distance / (len(moves) * 2), 1.0)
        
        # Análise de agressão e defesa (simplificada)
        forward_moves = 0
        defensive_moves = 0
        for m in moves:
            if m['piece_color'] == Color.WHITE:
                if int(m['to_pos'][1]) > int(m['from_pos'][1]):
                    forward_moves += 1
                else:
                    defensive_moves += 1
            else:  # BLACK
                if int(m['to_pos'][1]) < int(m['from_pos'][1]):
                    forward_moves += 1
                else:
                    defensive_moves += 1
        
        characteristics['aggression'] = min(forward_moves / len(moves) * 1.5, 1.0)
        characteristics['defense'] = min(defensive_moves / len(moves) * 1.5, 1.0)
        
        return characteristics
    
    def _find_matching_styles(self, characteristics: Dict[str, float], culture: ChessCulture) -> List[PlayStyle]:
        """Encontra os estilos que melhor correspondem às características"""
        style_scores = []
        
        for style in self.play_styles.values():
            score = self._calculate_style_match(
                characteristics, 
                style.characteristics,
                style.cultural_alignment.get(culture.name.lower(), 0.5)
            )
            style_scores.append((score, style))
        
        # Ordena por pontuação
        style_scores.sort(reverse=True)
        
        return [style for _, style in style_scores[:2]]
    
    def _calculate_style_match(self, game_chars: Dict[str, float], 
                             style_chars: Dict[str, float],
                             cultural_alignment: float) -> float:
        """Calcula o quanto um estilo corresponde às características observadas"""
        base_score = sum(
            1 - abs(game_chars.get(k, 0) - v)
            for k, v in style_chars.items()
        ) / len(style_chars)
        
        return base_score * cultural_alignment
    
    def _analyze_patterns(self, memory: CulturalMemory, culture: ChessCulture) -> List[str]:
        """Identifica padrões notáveis no jogo"""
        patterns = []
        moves = memory.moves_history
        
        if not moves:
            return patterns
            
        # Análise de desenvolvimento
        early_moves = moves[:10]
        development_focus = len([m for m in early_moves if m['piece_type'] != PieceType.PAWN])
        if development_focus >= 5:
            patterns.append("Rápido desenvolvimento de peças")
        
        # Análise de controle central
        central_moves = [m for m in moves if self._is_central_square(m['to_pos'])]
        if len(central_moves) / len(moves) > 0.3:
            patterns.append("Forte foco no controle do centro")
        
        # Análise de formações
        if self._has_pawn_chain(moves):
            patterns.append("Formação de cadeia de peões")
        
        # Análise cultural
        cultural_moves = self._identify_cultural_patterns(moves, culture)
        patterns.extend(cultural_moves)
        
        return patterns
    
    def _is_central_square(self, position: str) -> bool:
        """Verifica se uma posição está no centro do tabuleiro"""
        central_squares = ['d4', 'd5', 'e4', 'e5']
        return position in central_squares
    
    def _has_pawn_chain(self, moves: List[Dict]) -> bool:
        """Verifica se existe uma cadeia de peões"""
        # Implementação simplificada
        return True
    
    def _identify_cultural_patterns(self, moves: List[Dict], culture: ChessCulture) -> List[str]:
        """Identifica padrões específicos da cultura"""
        patterns = []
        
        # Padrões específicos para cada cultura
        if culture.name.lower().startswith('persian'):
            if self._has_fianchetto(moves):
                patterns.append("Desenvolvimento em fianchetto (estilo persa)")
        elif culture.name.lower().startswith('mongol'):
            if self._has_knight_coordination(moves):
                patterns.append("Coordenação de cavalos (tática mongol)")
        elif culture.name.lower().startswith('chinese'):
            if self._has_balanced_formation(moves):
                patterns.append("Formação equilibrada (estilo chinês)")
        
        return patterns
    
    def _has_fianchetto(self, moves: List[Dict]) -> bool:
        """Verifica desenvolvimento em fianchetto"""
        # Implementação simplificada
        return True
    
    def _has_knight_coordination(self, moves: List[Dict]) -> bool:
        """Verifica coordenação de cavalos"""
        # Implementação simplificada
        return True
    
    def _has_balanced_formation(self, moves: List[Dict]) -> bool:
        """Verifica formação equilibrada"""
        # Implementação simplificada
        return True
    
    def _calculate_cultural_expression(self, characteristics: Dict[str, float], 
                                     culture: ChessCulture) -> float:
        """Calcula o quanto o jogo expressa a cultura"""
        # Calcula baseado nas características culturais específicas
        culture_name = culture.name.lower().split()[0]
        
        # Define pesos para diferentes culturas
        cultural_weights = {
            'persian': {'development': 0.8, 'defense': 0.6},
            'indian': {'mobility': 0.7, 'development': 0.7},
            'arabic': {'aggression': 0.6, 'mobility': 0.8},
            'japanese': {'defense': 0.8, 'coordination': 0.7},
            'mongol': {'mobility': 0.9, 'aggression': 0.7},
            'chinese': {'defense': 0.7, 'development': 0.7},
            'viking': {'aggression': 0.8, 'mobility': 0.7},
            'byzantine': {'defense': 0.7, 'development': 0.6}
        }
        
        weights = cultural_weights.get(culture_name, {'development': 0.5, 'defense': 0.5})
        score = sum(characteristics.get(attr, 0) * weight 
                   for attr, weight in weights.items())
        
        return min(score / len(weights), 1.0)
    
    def _calculate_style_consistency(self, memory: CulturalMemory) -> float:
        """Calcula a consistência do estilo ao longo do jogo"""
        # Implementação simplificada
        return 0.7
    
    def _generate_recommendations(self, characteristics: Dict[str, float],
                                style: PlayStyle,
                                culture: ChessCulture) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        # Recomendações gerais
        if characteristics['development'] < 0.6:
            recommendations.append("Foque mais no desenvolvimento de peças")
        
        # Recomendações culturais
        if culture.name.lower().startswith('persian'):
            if characteristics['mobility'] < 0.6:
                recommendations.append("Explore mais as diagonais para refletir o estilo persa")
        elif culture.name.lower().startswith('mongol'):
            if characteristics['aggression'] < 0.7:
                recommendations.append("Busque posições mais agressivas, típicas do estilo mongol")
        elif culture.name.lower().startswith('chinese'):
            if characteristics['defense'] < 0.6:
                recommendations.append("Fortaleça a estrutura defensiva, característica do estilo chinês")
        
        return recommendations
