import pytest
from typing import Dict, List
from dataclasses import dataclass
from traditional.models.models import Position, Color, PieceType, Piece
from traditional.core.board.board import Board
from cultural.memory import CulturalMemory, CulturalEvent
from cultural.events import CulturalEventSystem
from cultural.style_analyzer import CulturalStyleAnalyzer
from cultural.cultures import persian_culture, mongol_culture, chinese_culture
from cultural.culture_framework import ChessCulture, CulturalTheme, PieceCulturalIdentity

@dataclass
class TestPiece:
    """Mock da classe Piece para testes"""
    type: PieceType
    color: Color
    position: Position = None
    has_moved: bool = False
    
    def __hash__(self):
        return hash((self.type, self.color))
    
    def __str__(self):
        return f"{self.color.name} {self.type.name}"
    
    def __eq__(self, other):
        if not isinstance(other, TestPiece):
            return False
        return self.type == other.type and self.color == other.color
    
    def to_algebraic(self) -> str:
        return self.position.to_algebraic() if self.position else ""

class TestCulturalMemory:
    def test_record_move(self):
        memory = CulturalMemory()
        pos = Position.from_algebraic('e2')
        piece = TestPiece(PieceType.PAWN, Color.WHITE)
        
        memory.record_move(piece, "e2", "e4", 0.5)
        assert len(memory.moves_history) == 1
        assert memory.moves_history[0]['from_pos'] == "e2"
        assert memory.moves_history[0]['to_pos'] == "e4"
        
    def test_record_capture(self):
        memory = CulturalMemory()
        pos1 = Position.from_algebraic('g1')
        pos2 = Position.from_algebraic('e5')
        capturing_piece = TestPiece(PieceType.KNIGHT, Color.WHITE)
        captured_piece = TestPiece(PieceType.PAWN, Color.BLACK)
        
        memory.record_capture(capturing_piece, captured_piece, 0.8)
        assert len(memory.captured_pieces['black']) == 1
        assert len(memory.significant_events) == 1
        
    def test_cultural_context(self):
        memory = CulturalMemory()
        context = memory.get_cultural_context()
        
        assert 'tension' in context
        assert 'moves' in context
        assert 'white_captures' in context
        assert 'black_captures' in context

class TestCulturalEvents:
    def test_event_triggers(self):
        event_system = CulturalEventSystem()
        board_state = {
            'position': 'test position',
            'current_move': ('e2', 'e4'),
            'piece': TestPiece(PieceType.PAWN, Color.WHITE)
        }
        
        events = event_system.check_event_triggers(board_state, persian_culture)
        assert isinstance(events, list)
        
    def test_event_effects(self):
        event_system = CulturalEventSystem()
        game_state = {'attack': 1.0, 'defense': 1.0}
        
        # Testa um evento persa
        events = event_system.events['persian']
        first_event = list(events.values())[0]
        
        new_state = event_system.apply_event_effects(first_event, game_state)
        assert new_state != game_state
        assert len(event_system.active_events) == 1

class TestStyleAnalyzer:
    def test_style_matching(self):
        analyzer = CulturalStyleAnalyzer()
        memory = CulturalMemory()
        
        # Registra alguns movimentos para teste
        pos = Position.from_algebraic('e2')
        piece = TestPiece(PieceType.PAWN, Color.WHITE)
        memory.record_move(piece, "e2", "e4", 0.5)
        
        analysis = analyzer.analyze_game_style(memory, persian_culture)
        assert analysis.primary_style is not None
        assert isinstance(analysis.cultural_expression, float)
        assert isinstance(analysis.style_consistency, float)
        
    def test_pattern_recognition(self):
        analyzer = CulturalStyleAnalyzer()
        memory = CulturalMemory()
        
        # Simula uma sequência de movimentos
        moves = [
            (TestPiece(PieceType.PAWN, Color.WHITE), "e2", "e4"),
            (TestPiece(PieceType.KNIGHT, Color.WHITE), "g1", "f3"),
            (TestPiece(PieceType.BISHOP, Color.WHITE), "f1", "c4")
        ]
        
        for piece, from_pos, to_pos in moves:
            memory.record_move(piece, from_pos, to_pos, 0.5)
        
        patterns = analyzer._analyze_patterns(memory, persian_culture)
        assert isinstance(patterns, list)

class TestCultureFramework:
    def test_persian_culture(self):
        assert persian_culture.name == "Império Persa"
        assert len(persian_culture.themes) > 0
        assert len(persian_culture.piece_identities) > 0
        
        # Testa cálculo de peso cultural
        context = {'in_check': False, 'promotion_available': False}
        weight = persian_culture.calculate_cultural_weight(PieceType.KING, context)
        assert isinstance(weight, float)
        
    def test_mongol_culture(self):
        assert mongol_culture.name == "Império Mongol"
        assert len(mongol_culture.themes) > 0
        assert len(mongol_culture.piece_identities) > 0
        
        # Testa narrativas
        narratives = mongol_culture.get_theme_narratives("Conquista")
        assert len(narratives) > 0
        
    def test_chinese_culture(self):
        assert chinese_culture.name == "Império Chinês"
        assert len(chinese_culture.themes) > 0
        assert len(chinese_culture.piece_identities) > 0
        
        # Testa nomes de peças
        king_name = chinese_culture.get_piece_name(PieceType.KING)
        assert king_name == "Imperador"

class TestCulturalIntegration:
    def test_full_move_sequence(self):
        board = Board()
        memory = CulturalMemory()
        event_system = CulturalEventSystem()
        analyzer = CulturalStyleAnalyzer()
        
        # Executa uma sequência de movimentos
        moves = [
            (Position.from_algebraic("e2"), Position.from_algebraic("e4"), persian_culture),
            (Position.from_algebraic("e7"), Position.from_algebraic("e5"), mongol_culture),
            (Position.from_algebraic("g1"), Position.from_algebraic("f3"), persian_culture),
            (Position.from_algebraic("b8"), Position.from_algebraic("c6"), mongol_culture)
        ]
        
        for from_pos, to_pos, culture in moves:
            piece = board.get_piece(from_pos)
            if piece:
                # Verifica eventos
                board_state = {
                    'position': board.display(),
                    'current_move': (from_pos, to_pos),
                    'piece': piece
                }
                events = event_system.check_event_triggers(board_state, culture)
                
                # Executa movimento
                result = board.move_piece(from_pos, to_pos)
                assert result['success']
                
                # Registra na memória
                # Registra na memória
                memory.record_move(piece, str(from_pos), str(to_pos), 0.5)
        
        # Analisa resultados
        persian_analysis = analyzer.analyze_game_style(memory, persian_culture)
        mongol_analysis = analyzer.analyze_game_style(memory, mongol_culture)
        
        assert persian_analysis.primary_style is not None
        assert mongol_analysis.primary_style is not None
        assert len(memory.moves_history) == 4

def test_all():
    """Executa todos os testes"""
    # Testes de Memória Cultural
    memory_tests = TestCulturalMemory()
    memory_tests.test_record_move()
    memory_tests.test_record_capture()
    memory_tests.test_cultural_context()
    
    # Testes de Eventos
    event_tests = TestCulturalEvents()
    event_tests.test_event_triggers()
    event_tests.test_event_effects()
    
    # Testes de Análise de Estilo
    style_tests = TestStyleAnalyzer()
    style_tests.test_style_matching()
    style_tests.test_pattern_recognition()
    
    # Testes do Framework Cultural
    culture_tests = TestCultureFramework()
    culture_tests.test_persian_culture()
    culture_tests.test_mongol_culture()
    culture_tests.test_chinese_culture()
    
    # Testes de Integração
    integration_tests = TestCulturalIntegration()
    integration_tests.test_full_move_sequence()
    
    print("Todos os testes executados com sucesso!")
