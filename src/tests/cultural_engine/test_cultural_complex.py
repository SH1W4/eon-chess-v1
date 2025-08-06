import pytest
from typing import Dict, List, Tuple
from core.board.board import Board, PieceType, Color, Piece
from cultural.memory import CulturalMemory
from cultural.events import CulturalEventSystem
from cultural.events_extended import (
    get_cultural_events,
    check_culture_specific_conditions,
    indian_events,
    arabic_events,
    japanese_events
)
from cultural.cultures_extended import indian_culture, arabic_culture, japanese_culture
from cultural.style_analyzer import CulturalStyleAnalyzer
from narrative.engine_simple import NarrativeEngine

class TestExtendedCultures:
    """Testes complexos para as culturas estendidas"""
    
    def setup_method(self):
        self.board = Board()
        self.memory = CulturalMemory()
        self.event_system = CulturalEventSystem()
        self.analyzer = CulturalStyleAnalyzer()
        self.narrative_engine = NarrativeEngine()
        
    def test_indian_culture_themes(self):
        """Testa temas da cultura indiana"""
        themes = indian_culture.themes
        
        # Verifica temas específicos
        assert "Dharma" in themes
        assert "Quatro Braços" in themes
        assert "Karma" in themes
        
        # Verifica narrativas específicas
        dharma_narratives = themes["Dharma"].narratives
        assert any("dharma" in n.lower() for n in dharma_narratives)
        assert any("ordem cósmica" in n.lower() for n in dharma_narratives)
        
    def test_arabic_culture_pieces(self):
        """Testa peças da cultura árabe"""
        pieces = arabic_culture.piece_identities
        
        # Verifica nomes históricos
        assert pieces[PieceType.KING].name == "Califa"
        assert pieces[PieceType.QUEEN].name == "Vizir"
        assert pieces[PieceType.BISHOP].name == "Al-Fil"
        
        # Verifica valores culturais
        assert pieces[PieceType.KING].cultural_value == 1.0
        assert pieces[PieceType.QUEEN].cultural_value == 0.9
        
    def test_japanese_culture_events(self):
        """Testa eventos da cultura japonesa"""
        events = japanese_events
        
        # Verifica eventos específicos
        assert "kiai" in events
        assert "tenchi" in events
        
        # Verifica narrativas e impactos
        kiai_event = events["kiai"]
        assert kiai_event.cultural_impact >= 0.8
        assert any("samurai" in n.lower() for n in kiai_event.narratives)
        
    def test_cultural_interaction(self):
        """Testa interação entre culturas diferentes"""
        # Configura sequência de movimentos
        moves = [
            ("e2", "e4", indian_culture),   # Peão indiano
            ("e7", "e5", arabic_culture),   # Peão árabe
            ("g1", "f3", indian_culture),   # Cavalo indiano
            ("b8", "c6", arabic_culture)    # Cavalo árabe
        ]
        
        narratives = []
        for from_pos, to_pos, culture in moves:
            piece = self.board.get_piece(from_pos)
            if piece:
                # Gera narrativa
                narrative = self.narrative_engine.generate_move_narrative(
                    from_pos, to_pos, piece,
                    {'narrative_pool': culture.get_theme_narratives(list(culture.themes.keys())[0])}
                )
                narratives.append(narrative)
                
                # Executa movimento
                self.board.move_piece(from_pos, to_pos)
                self.memory.record_move(piece, from_pos, to_pos, 0.5)
        
        # Verifica distinção cultural nas narrativas
        indian_narratives = narratives[::2]  # Narrativas indianas
        arabic_narratives = narratives[1::2]  # Narrativas árabes
        
        assert any("dharma" in n.lower() or "karma" in n.lower() for n in indian_narratives)
        assert any("califa" in n.lower() or "deserto" in n.lower() for n in arabic_narratives)
        
    def test_event_triggers(self):
        """Testa gatilhos de eventos culturais"""
        # Prepara estado do tabuleiro para teste
        board_state = {
            'position': self.board.display(),
            'pieces_in_spiral': True,
            'center_control': True,
            'symmetric_pattern': True,
            'critical_position': True,
            'piece_sacrifice': True
        }
        
        # Testa eventos indianos
        chakravyuha = indian_events["chakravyuha"]
        assert check_culture_specific_conditions(chakravyuha, board_state)
        
        # Testa eventos japoneses
        kiai = japanese_events["kiai"]
        assert check_culture_specific_conditions(kiai, board_state)
        
    def test_style_analysis(self):
        """Testa análise de estilo para diferentes culturas"""
        # Prepara movimentos de teste
        piece = Piece(PieceType.PAWN, Color.WHITE)
        moves = [
            ("e2", "e4"),
            ("g1", "f3"),
            ("f1", "c4")
        ]
        
        for from_pos, to_pos in moves:
            self.memory.record_move(piece, from_pos, to_pos, 0.5)
        
        # Analisa estilo para cada cultura
        indian_analysis = self.analyzer.analyze_game_style(self.memory, indian_culture)
        arabic_analysis = self.analyzer.analyze_game_style(self.memory, arabic_culture)
        japanese_analysis = self.analyzer.analyze_game_style(self.memory, japanese_culture)
        
        # Verifica diferenças culturais na análise
        assert indian_analysis.cultural_expression != arabic_analysis.cultural_expression
        assert japanese_analysis.cultural_expression != arabic_analysis.cultural_expression
        
    def test_complex_scenario(self):
        """Testa cenário complexo com múltiplas culturas e eventos"""
        # Configura um cenário complexo
        board_states = [
            {
                'position': 'initial',
                'pieces_in_spiral': True,
                'center_control': True,
                'movement_pattern': 'rhythmic',
                'attacking_pieces': 3,
                'directional_pattern': True
            },
            {
                'position': 'midgame',
                'critical_position': True,
                'piece_sacrifice': True,
                'position_balance': True,
                'energy_flow': True
            }
        ]
        
        cultures = [indian_culture, arabic_culture, japanese_culture]
        all_events = []
        
        # Testa eventos em diferentes estados
        for state in board_states:
            for culture in cultures:
                culture_events = get_cultural_events(culture.name.split()[0].lower())
                for event in culture_events.values():
                    if check_culture_specific_conditions(event, state):
                        all_events.append(event)
        
        # Verifica diversidade de eventos
        event_types = set(event.name for event in all_events)
        assert len(event_types) >= 3
        
        # Verifica impacto cultural
        total_impact = sum(event.cultural_impact for event in all_events)
        assert total_impact > 0

    def test_cultural_cache(self):
        """Testa sistema de cache para operações culturais"""
        # Implementar depois que o sistema de cache estiver pronto
        pass

def test_all():
    """Executa todos os testes complexos"""
    test_suite = TestExtendedCultures()
    test_suite.setup_method()
    
    # Testes de culturas individuais
    test_suite.test_indian_culture_themes()
    test_suite.test_arabic_culture_pieces()
    test_suite.test_japanese_culture_events()
    
    # Testes de interação
    test_suite.test_cultural_interaction()
    test_suite.test_event_triggers()
    test_suite.test_style_analysis()
    
    # Teste complexo
    test_suite.test_complex_scenario()
    
    print("Todos os testes complexos executados com sucesso!")

if __name__ == "__main__":
    test_all()
