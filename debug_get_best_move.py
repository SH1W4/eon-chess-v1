#!/usr/bin/env python3
"""Debug script para entender problema com get_best_move"""

from src.core.board.board import Board, Piece, PieceType, Color, Position
from src.ai.adaptive_ai import AdaptiveAI

# Setup board
board = Board()

# Add pieces using tuples as test uses
board.pieces = {
    (1, 1): Piece(PieceType.KING, Color.WHITE),
    (3, 3): Piece(PieceType.QUEEN, Color.WHITE),
    (6, 6): Piece(PieceType.KING, Color.BLACK)
}

print("Board pieces:", board.pieces)

# Verifica se pieces é acessível
print("\nTesting board attributes:")
print(f"Has 'pieces': {hasattr(board, 'pieces')}")
print(f"Pieces is dict: {isinstance(board.pieces, dict)}")
print(f"Pieces content: {board.pieces}")

# Testa get_valid_moves para cada peça
for pos, piece in board.pieces.items():
    print(f"\nTesting get_valid_moves for {piece.type} at {pos}:")
    moves = board.get_valid_moves(pos)
    print(f"  Valid moves: {moves}")
    print(f"  Number of moves: {len(moves)}")

# Create AI and test
ai = AdaptiveAI()
print("\n\nCalling ai.get_best_move(board, Color.WHITE)...")
move = ai.get_best_move(board, Color.WHITE)
print(f"Result: {move}")

if move:
    print(f"Move from {move.from_pos} to {move.to_pos}")
    print(f"Piece: {move.piece.type}")
else:
    print("ERROR: get_best_move returned None!")
    
    # Debug mais profundo
    print("\nDEBUG: Checking AI attributes:")
    print(f"AI has profile: {hasattr(ai, 'profile')}")
    print(f"AI has weights: {hasattr(ai, 'weights')}")
    
    # Vamos tentar chamar direto o método interno para ver onde falha
    print("\nTrying to get moves manually...")
    for pos, piece in board.pieces.items():
        if piece.color == Color.WHITE:
            valid_moves = board.get_valid_moves(pos)
            print(f"{piece.type} at {pos} has {len(valid_moves)} valid moves: {valid_moves[:3] if valid_moves else []}")
