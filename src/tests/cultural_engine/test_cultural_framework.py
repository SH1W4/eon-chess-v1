import pytest
from typing import Dict, List, Tuple
from dataclasses import dataclass
from core.board.board import Board, PieceType, Color, Piece
from cultural.memory import CulturalMemory
from cultural.culture_framework import ChessCulture, byzantine_culture, viking_culture
from narrative.engine_simple import NarrativeEngine

@dataclass
class CulturalTestResult:
    """Resultados dos testes culturais"""
    culture_name: str
    narrative_diversity: float  # 0-1, mede a variedade de narrativas
    theme_consistency: float   # 0-1, mede a consistência dos temas
    historical_accuracy: float # 0-1, mede a precisão histórica
    cultural_depth: float     # 0-1, mede a profundidade cultural
    engagement_score: float   # 0-1, mede o engajamento geral

class CulturalTestFramework:
    def __init__(self):
        self.board = Board()
        self.memory = CulturalMemory()
        self.narrative_engine = NarrativeEngine()
        
    def setup_test_scenario(self, moves: List[Tuple[str, str]]):
        """Configura um cenário de teste com movimentos específicos"""
        for from_pos, to_pos in moves:
            self.board.move_piece(from_pos, to_pos)
            piece = self.board.get_piece(to_pos)
            if piece:
                self.memory.record_move(piece, from_pos, to_pos, 0.5)
    
    def evaluate_cultural_narrative(self, culture: ChessCulture, move_sequence: List[Tuple[str, str]]) -> Dict:
        """Avalia a qualidade das narrativas culturais"""
        narratives = []
        theme_usage = {}
        historical_refs = 0
        
        for from_pos, to_pos in move_sequence:
            piece = self.board.get_piece(from_pos)
            if not piece:
                continue
                
            # Gera narrativa
            context = self.memory.get_cultural_context()
            cultural_weight = culture.calculate_cultural_weight(piece.type, context)
            
            # Registra uso de temas
            for theme in culture.themes.values():
                if any(narrative in theme.narratives for narrative in narratives):
                    theme_usage[theme.name] = theme_usage.get(theme.name, 0) + 1
                if theme.historical_context:
                    historical_refs += 1
            
            narratives.append(self.narrative_engine.generate_move_narrative(
                from_pos, to_pos, piece, {'narrative_pool': culture.get_theme_narratives('Estratégia Imperial')}
            ))
        
        # Calcula métricas
        narrative_diversity = len(set(narratives)) / len(narratives) if narratives else 0
        theme_consistency = len(theme_usage) / len(culture.themes) if culture.themes else 0
        historical_depth = historical_refs / len(move_sequence)
        
        return {
            'narrative_diversity': narrative_diversity,
            'theme_consistency': theme_consistency,
            'historical_depth': historical_depth,
            'narratives': narratives
        }
    
    def test_cultural_interaction(self, culture1: ChessCulture, culture2: ChessCulture) -> Dict:
        """Testa a interação entre duas culturas"""
        # Configura um cenário de teste
        test_moves = [
            ('e2', 'e4'),  # Brancas (Cultura 1)
            ('e7', 'e5'),  # Pretas (Cultura 2)
            ('g1', 'f3'),  # Brancas
            ('b8', 'c6'),  # Pretas
        ]
        
        self.setup_test_scenario(test_moves)
        
        # Avalia cada cultura
        culture1_eval = self.evaluate_cultural_narrative(culture1, test_moves[::2])  # Moves pares (Brancas)
        culture2_eval = self.evaluate_cultural_narrative(culture2, test_moves[1::2]) # Moves ímpares (Pretas)
        
        # Calcula métricas de interação
        cultural_tension = self.memory.cultural_tension
        interaction_depth = (culture1_eval['theme_consistency'] + culture2_eval['theme_consistency']) / 2
        narrative_contrast = abs(culture1_eval['narrative_diversity'] - culture2_eval['narrative_diversity'])
        
        return {
            'cultural_tension': cultural_tension,
            'interaction_depth': interaction_depth,
            'narrative_contrast': narrative_contrast,
            'culture1_metrics': culture1_eval,
            'culture2_metrics': culture2_eval
        }
    
    def generate_test_report(self, culture1: ChessCulture, culture2: ChessCulture) -> str:
        """Gera um relatório detalhado dos testes culturais"""
        results = self.test_cultural_interaction(culture1, culture2)
        
        report = f"""
=== Relatório de Teste Cultural: {culture1.name} vs {culture2.name} ===

Períodos Históricos:
- {culture1.name}: {culture1.historical_period}
- {culture2.name}: {culture2.historical_period}

Métricas de Interação:
- Tensão Cultural: {results['cultural_tension']:.2f}
- Profundidade de Interação: {results['interaction_depth']:.2f}
- Contraste Narrativo: {results['narrative_contrast']:.2f}

{culture1.name} (Brancas):
- Diversidade Narrativa: {results['culture1_metrics']['narrative_diversity']:.2f}
- Consistência Temática: {results['culture1_metrics']['theme_consistency']:.2f}
- Profundidade Histórica: {results['culture1_metrics']['historical_depth']:.2f}

{culture2.name} (Pretas):
- Diversidade Narrativa: {results['culture2_metrics']['narrative_diversity']:.2f}
- Consistência Temática: {results['culture2_metrics']['theme_consistency']:.2f}
- Profundidade Histórica: {results['culture2_metrics']['historical_depth']:.2f}

Exemplos de Narrativas:
{culture1.name}:
""" + "\n".join(f"- {n}" for n in results['culture1_metrics']['narratives'][:3]) + f"""

{culture2.name}:
""" + "\n".join(f"- {n}" for n in results['culture2_metrics']['narratives'][:3])
        
        return report

def test_byzantine_vs_viking():
    """Teste específico: Bizantinos vs Vikings"""
    framework = CulturalTestFramework()
    report = framework.generate_test_report(byzantine_culture, viking_culture)
    print(report)
    
    # Assertions para garantir qualidade mínima
    results = framework.test_cultural_interaction(byzantine_culture, viking_culture)
    assert results['cultural_tension'] > 0, "Deve haver tensão cultural entre as culturas"
    assert results['interaction_depth'] > 0.5, "Deve haver profundidade significativa na interação"
    assert results['narrative_contrast'] < 0.5, "O contraste narrativo não deve ser muito extremo"

if __name__ == "__main__":
    # Executa o teste
    test_byzantine_vs_viking()
