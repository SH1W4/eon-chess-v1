import pytest
from src.core.engine import ChessEngine, Position, Piece, Move
from src.core.board.board import PieceType, Color

def test_initial_board_setup():
    engine = ChessEngine()
    
    # Test pawns
    for file in range(1, 9):
        # Black pawns on rank 7
        piece = engine.get_piece(Position(7, file))
        assert isinstance(piece, Piece)
        assert piece.type == PieceType.PAWN
        assert piece.color == Color.BLACK
        
        # White pawns on rank 2
        piece = engine.get_piece(Position(2, file))
        assert isinstance(piece, Piece)
        assert piece.type == PieceType.PAWN
        assert piece.color == Color.WHITE
    
    # Test other pieces
    pieces = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
              PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
    for file, piece_type in enumerate(pieces, start=1):
        # Black pieces on rank 8
        piece = engine.get_piece(Position(8, file))
        assert isinstance(piece, Piece)
        assert piece.type == piece_type
        assert piece.color == Color.BLACK
        
        # White pieces on rank 1
        piece = engine.get_piece(Position(1, file))
        assert isinstance(piece, Piece)
        assert piece.type == piece_type
        assert piece.color == Color.WHITE

def test_pawn_moves():
    engine = ChessEngine()
    
    # Test initial white pawn moves
    moves = engine.get_legal_moves(Position(2, 1))  # a2 pawn
    assert len(moves) == 2
    assert Position(3, 1) in moves  # One square forward
    assert Position(4, 1) in moves  # Two squares forward
    
    # Test black pawn moves
    moves = engine.get_legal_moves(Position(7, 1))  # a7 pawn
    assert len(moves) == 2
    assert Position(6, 1) in moves  # One square forward
    assert Position(5, 1) in moves  # Two squares forward

def test_knight_moves():
    engine = ChessEngine()
    
    # Test initial knight moves
    moves = engine.get_legal_moves(Position(1, 2))  # White knight on b1
    assert len(moves) == 2
    assert Position(3, 1) in moves  # a3
    assert Position(3, 3) in moves  # c3

def test_invalid_moves():
    engine = ChessEngine()
    
    # Try to move opponent's piece
    moves = engine.get_legal_moves(Position(8, 1))  # Black rook on a8
    assert len(moves) == 0
    
    # Try to move empty square
    moves = engine.get_legal_moves(Position(4, 4))  # Empty square e4
    assert len(moves) == 0

def test_make_move():
    engine = ChessEngine()
    
    # Make a valid pawn move
    from_pos = Position(2, 5)  # e2
    to_pos = Position(4, 5)    # e4
    piece = engine.get_piece(from_pos)
    move = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    
    assert engine.make_move(move)
    assert engine.get_piece(to_pos) == piece
    assert engine.get_piece(from_pos) is None
    assert engine.board.current_turn == Color.BLACK

def test_invalid_move():
    engine = ChessEngine()
    
    # Try to make an invalid pawn move
    from_pos = Position(2, 1)  # a2
    to_pos = Position(5, 1)    # a5 (too far)
    piece = engine.get_piece(from_pos)
    move = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    
    assert not engine.make_move(move)
    assert engine.get_piece(from_pos) == piece
    assert engine.get_piece(to_pos) is None
    assert engine.board.current_turn == Color.WHITE

def test_pawn_capture():
    engine = ChessEngine()
    
    # Setup a capture scenario (e4 d5 exd5)
    from_pos = Position(2, 5)  # e2
    to_pos = Position(4, 5)    # e4
    piece = engine.get_piece(from_pos)
    move1 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    assert engine.make_move(move1)
    
    from_pos = Position(7, 4)  # d7
    to_pos = Position(5, 4)    # d5
    piece = engine.get_piece(from_pos)
    move2 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    assert engine.make_move(move2)
    
    # Capture move
    from_pos = Position(4, 5)  # e4
    to_pos = Position(5, 4)    # d5
    piece = engine.get_piece(from_pos)
    captured = engine.get_piece(to_pos)
    move3 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece, captured_piece=captured)
    
    assert engine.make_move(move3)
    assert engine.get_piece(to_pos) == piece
    assert engine.get_piece(from_pos) is None

def test_check_detection():
    engine = ChessEngine()
    
    # Setup a check scenario
    # 1. e4 e5 2. Qh5 (check)
    from_pos = Position(2, 5)  # e2
    to_pos = Position(4, 5)    # e4
    piece = engine.get_piece(from_pos)
    move1 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    assert engine.make_move(move1)
    
    from_pos = Position(7, 5)  # e7
    to_pos = Position(5, 5)    # e5
    piece = engine.get_piece(from_pos)
    move2 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    assert engine.make_move(move2)
    
    from_pos = Position(1, 4)  # d1 (queen)
    to_pos = Position(5, 8)    # h5
    piece = engine.get_piece(from_pos)
    move3 = Move(from_pos=from_pos, to_pos=to_pos, piece=piece)
    assert engine.make_move(move3)
    
    assert engine.board.is_in_check(Color.BLACK)
    assert not engine.board.is_in_check(Color.WHITE)

def test_checkmate_detection():
    engine = ChessEngine()
    
    # Scholar's mate setup
    # 1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6?? 4. Qxf7#
    moves = [
        (Position(2, 5), Position(4, 5)),  # e4
        (Position(7, 5), Position(5, 5)),  # e5
        (Position(1, 6), Position(4, 3)),  # Bc4
        (Position(8, 2), Position(6, 3)),  # Nc6
        (Position(1, 4), Position(5, 8)),  # Qh5
        (Position(8, 7), Position(6, 6)),  # Nf6
        (Position(5, 8), Position(6, 6)),  # Qxf7#
    ]
    
    for from_pos, to_pos in moves:
        piece = engine.get_piece(from_pos)
        captured = engine.get_piece(to_pos)
        move = Move(from_pos=from_pos, to_pos=to_pos, piece=piece, captured_piece=captured)
        engine.make_move(move)
    
    assert engine.is_checkmate()

def test_stalemate_detection():
    engine = ChessEngine()
    
    # Setup a stalemate scenario
    # Clear the board except for kings and a queen
    for rank in range(1, 9):
        for file in range(1, 9):
            if engine.get_piece(Position(rank, file)):
                engine.set_piece(Position(rank, file), None)
    
    # Place pieces for stalemate
    engine.set_piece(Position(8, 1),  # a8
                    Piece(type=PieceType.KING, color=Color.BLACK,
                         position=Position(8, 1)))
    
    engine.set_piece(Position(7, 2),  # b7
                    Piece(type=PieceType.QUEEN, color=Color.WHITE,
                         position=Position(7, 2)))
    
    engine.set_piece(Position(7, 1),  # a7
                    Piece(type=PieceType.KING, color=Color.WHITE,
                         position=Position(7, 1)))
    
    engine.board.current_turn = Color.BLACK
    
    assert engine.is_stalemate()
    assert not engine.is_checkmate()

def test_algebraic_notation():
    # Test conversion to algebraic notation
    pos = Position(4, 5)  # e4
    assert pos.to_algebraic() == 'e4'
    
    # Test conversion from algebraic notation
    pos = Position.from_algebraic('e4')
    assert pos.rank == 4
    assert pos.file == 5

def test_castling():
    engine = ChessEngine()
    
    # Clear pieces between king and rook
    engine.set_piece(Position(1, 6), None)  # f1
    engine.set_piece(Position(1, 7), None)  # g1
    
    # Test kingside castling
    moves = engine.get_legal_moves(Position(1, 5))  # e1
    assert Position(1, 7) in moves  # g1 - Kingside castling should be possible
    
    # Execute castling move
    king = engine.get_piece(Position(1, 5))  # e1
    move = Move(from_pos=Position(1, 5),
                to_pos=Position(1, 7),
                piece=king,
                is_castling=True)
    assert engine.make_move(move)
    
    # Verify king and rook positions after castling
    assert engine.get_piece(Position(1, 7)).type == PieceType.KING  # g1
    assert engine.get_piece(Position(1, 6)).type == PieceType.ROOK  # f1
