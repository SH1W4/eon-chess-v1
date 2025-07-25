import pytest
from src.core.engine import ChessEngine, Position, Piece, Move

def test_initial_board_setup():
    engine = ChessEngine()
    
    # Test pawns
    for col in range(8):
        assert isinstance(engine.get_piece(Position(1, col)), Piece)
        assert engine.get_piece(Position(1, col)).type == 'pawn'
        assert engine.get_piece(Position(1, col)).color == 'black'
        
        assert isinstance(engine.get_piece(Position(6, col)), Piece)
        assert engine.get_piece(Position(6, col)).type == 'pawn'
        assert engine.get_piece(Position(6, col)).color == 'white'
    
    # Test other pieces
    pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    for col, piece_type in enumerate(pieces):
        # Black pieces
        assert isinstance(engine.get_piece(Position(0, col)), Piece)
        assert engine.get_piece(Position(0, col)).type == piece_type
        assert engine.get_piece(Position(0, col)).color == 'black'
        
        # White pieces
        assert isinstance(engine.get_piece(Position(7, col)), Piece)
        assert engine.get_piece(Position(7, col)).type == piece_type
        assert engine.get_piece(Position(7, col)).color == 'white'

def test_pawn_moves():
    engine = ChessEngine()
    
    # Test initial white pawn moves
    moves = engine.get_legal_moves(Position(6, 0))
    assert len(moves) == 2
    assert Position(5, 0) in moves  # One square forward
    assert Position(4, 0) in moves  # Two squares forward
    
    # Test black pawn moves
    moves = engine.get_legal_moves(Position(1, 0))
    assert len(moves) == 2
    assert Position(2, 0) in moves  # One square forward
    assert Position(3, 0) in moves  # Two squares forward

def test_knight_moves():
    engine = ChessEngine()
    
    # Test initial knight moves
    moves = engine.get_legal_moves(Position(7, 1))  # White knight
    assert len(moves) == 2
    assert Position(5, 0) in moves
    assert Position(5, 2) in moves

def test_invalid_moves():
    engine = ChessEngine()
    
    # Try to move opponent's piece
    moves = engine.get_legal_moves(Position(0, 0))  # Black rook
    assert len(moves) == 0
    
    # Try to move empty square
    moves = engine.get_legal_moves(Position(4, 4))
    assert len(moves) == 0

def test_make_move():
    engine = ChessEngine()
    
    # Make a valid pawn move
    from_pos = Position(6, 0)
    to_pos = Position(4, 0)
    piece = engine.get_piece(from_pos)
    move = Move(from_pos, to_pos, piece)
    
    assert engine.make_move(move)
    assert engine.get_piece(to_pos) == piece
    assert engine.get_piece(from_pos) is None
    assert engine.current_player == 'black'

def test_invalid_move():
    engine = ChessEngine()
    
    # Try to make an invalid pawn move
    from_pos = Position(6, 0)
    to_pos = Position(3, 0)  # Too far
    piece = engine.get_piece(from_pos)
    move = Move(from_pos, to_pos, piece)
    
    assert not engine.make_move(move)
    assert engine.get_piece(from_pos) == piece
    assert engine.get_piece(to_pos) is None
    assert engine.current_player == 'white'

def test_pawn_capture():
    engine = ChessEngine()
    
    # Setup a capture scenario
    engine.make_move(Move(Position(6, 0), Position(4, 0), engine.get_piece(Position(6, 0))))
    engine.make_move(Move(Position(1, 1), Position(3, 1), engine.get_piece(Position(1, 1))))
    
    # Test capture move
    from_pos = Position(4, 0)
    to_pos = Position(3, 1)
    piece = engine.get_piece(from_pos)
    captured = engine.get_piece(to_pos)
    move = Move(from_pos, to_pos, piece, captured_piece=captured)
    
    assert engine.make_move(move)
    assert engine.get_piece(to_pos) == piece
    assert engine.get_piece(from_pos) is None

def test_check_detection():
    engine = ChessEngine()
    
    # Setup a check scenario
    engine.make_move(Move(Position(6, 5), Position(4, 5), engine.get_piece(Position(6, 5))))
    engine.make_move(Move(Position(1, 4), Position(3, 4), engine.get_piece(Position(1, 4))))
    engine.make_move(Move(Position(7, 3), Position(3, 7), engine.get_piece(Position(7, 3))))  # White queen attacks
    
    assert engine._is_in_check('black')
    assert not engine._is_in_check('white')

def test_checkmate_detection():
    engine = ChessEngine()
    
    # Scholar's mate setup
    moves = [
        (Position(6, 4), Position(4, 4)),  # e4
        (Position(1, 4), Position(3, 4)),  # e5
        (Position(7, 5), Position(4, 2)),  # Bc4
        (Position(1, 6), Position(2, 6)),  # f6
        (Position(7, 3), Position(3, 7)),  # Qh5
        (Position(1, 5), Position(2, 5)),  # g6
        (Position(3, 7), Position(1, 5)),  # Qxf7#
    ]
    
    for from_pos, to_pos in moves:
        piece = engine.get_piece(from_pos)
        captured = engine.get_piece(to_pos)
        engine.make_move(Move(from_pos, to_pos, piece, captured_piece=captured))
    
    assert engine.is_checkmate()

def test_stalemate_detection():
    engine = ChessEngine()
    
    # Setup a stalemate scenario
    # Clear the board except for kings and a queen
    for row in range(8):
        for col in range(8):
            if engine.get_piece(Position(row, col)):
                engine.set_piece(Position(row, col), None)
    
    # Place pieces for stalemate
    engine.set_piece(Position(0, 0), Piece('king', 'black'))
    engine.set_piece(Position(2, 1), Piece('queen', 'white'))
    engine.set_piece(Position(2, 0), Piece('king', 'white'))
    engine.current_player = 'black'
    
    assert engine.is_stalemate()
    assert not engine.is_checkmate()

def test_algebraic_notation():
    # Test conversion to algebraic notation
    pos = Position(4, 4)
    assert pos.to_algebraic() == 'e4'
    
    # Test conversion from algebraic notation
    pos = Position.from_algebraic('e4')
    assert pos.row == 4
    assert pos.col == 4

def test_castling():
    engine = ChessEngine()
    
    # Clear pieces between king and rook
    engine.set_piece(Position(7, 5), None)
    engine.set_piece(Position(7, 6), None)
    
    # Test kingside castling
    moves = engine.get_legal_moves(Position(7, 4))
    assert Position(7, 6) in moves  # Kingside castling should be possible
    
    # Execute castling move
    king = engine.get_piece(Position(7, 4))
    move = Move(Position(7, 4), Position(7, 6), king, is_castling=True)
    assert engine.make_move(move)
    
    # Verify king and rook positions after castling
    assert engine.get_piece(Position(7, 6)).type == 'king'
    assert engine.get_piece(Position(7, 5)).type == 'rook'
