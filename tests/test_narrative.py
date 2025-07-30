import pytest
from src.narrative.engine import NarrativeEngine, NarrativeConfig
from src.core.board.board import Board, Position, Color, PieceType
from src.core.engine import Move

@pytest.fixture
def narrative_engine():
    """Fixture que fornece uma instância configurada do motor narrativo."""
    return NarrativeEngine(NarrativeConfig(language="en", culture="standard", style="standard"))

def test_move_narrative(narrative_engine):
    """Testa geração de narrativa para um movimento"""
    board = Board()
    # e4
    move = Move(
        from_pos=Position(2, 5),  # e2
        to_pos=Position(4, 5),     # e4
        piece=board.get_piece(Position(2, 5))
    )
    narrative = narrative_engine.generate_move_narrative(move, board)
    assert "White Pawn moves from e2 to e4" in narrative

def test_capture_narrative(narrative_engine):
    """Testa geração de narrativa para uma captura"""
    board = Board()
    # Simula um movimento para criar uma posição de captura
    board.move_piece(Position(2, 5), Position(4, 5))  # e4
    board.move_piece(Position(7, 4), Position(5, 4))  # d5
    
    # exd5
    move = Move(
        from_pos=Position(4, 5),  # e4
        to_pos=Position(5, 4),     # d5
        piece=board.get_piece(Position(4, 5)),
        captured_piece=board.get_piece(Position(5, 4))
    )
    narrative = narrative_engine.generate_move_narrative(move, board)
    assert "captures Black Pawn on d5" in narrative

def test_check_narrative(narrative_engine):
    """Testa geração de narrativa para um xeque"""
    board = Board()
    # Mate do pastor
    board.move_piece(Position(2, 5), Position(4, 5))  # e4
    board.move_piece(Position(7, 5), Position(5, 5))  # e5
    board.move_piece(Position(1, 6), Position(4, 3))  # Bc4
    board.move_piece(Position(8, 2), Position(6, 3))  # Nc6
    
    # Qh5+ (xeque)
    move = Move(
        from_pos=Position(1, 4),  # d1
        to_pos=Position(5, 8),     # h5
        piece=board.get_piece(Position(1, 4))
    )
    board.move_piece(move.from_pos, move.to_pos)
    
    narrative = narrative_engine.generate_move_narrative(move, board)
    assert "giving check" in narrative.lower()

def test_position_narrative(narrative_engine):
    """Testa geração de narrativa para uma posição"""
    board = Board()
    # Abertura padrão
    board.move_piece(Position(2, 5), Position(4, 5))  # e4
    board.move_piece(Position(7, 5), Position(5, 5))  # e5
    board.move_piece(Position(1, 6), Position(4, 3))  # Bc4
    
    narrative = narrative_engine.generate_position_narrative(board)
    assert "center" in narrative.lower()
    assert "development" in narrative.lower()

def test_culture_switching(narrative_engine):
    """Testa mudança de cultura nas narrativas"""
    board = Board()
    
    # Narrativa padrão
    narrative_engine.config.culture = "standard"
    move = Move(
        from_pos=Position(2, 5),  # e2
        to_pos=Position(4, 5),     # e4
        piece=board.get_piece(Position(2, 5))
    )
    narrative = narrative_engine.generate_move_narrative(move, board)
    assert "moves from" in narrative
    
    # Narrativa em português
    narrative_engine.config.language = "pt-br"
    narrative = narrative_engine.generate_move_narrative(move, board)
    assert "Peão" in narrative

