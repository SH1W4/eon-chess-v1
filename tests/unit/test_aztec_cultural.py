#!/usr/bin/env python3

import sys
import os

# Add src directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from cultural.cultures.aztec_culture import aztec_culture
from core.board.board import Board, Piece, PieceType, Color, Position

def test_aztec_cultural_system() -> None:
    print("\n=== Testing Aztec Piece Names ===")
    for piece_type in ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']:
        aztec_name = aztec_culture.get_piece_name(piece_type)
        print(f"{piece_type.title():8} -> {aztec_name}")

def test_aztec_narratives() -> None:
    print("\n=== Testing Aztec Narratives ===")
    
    # Test move narrative
    piece = aztec_culture.get_piece_name('knight')
    move_narrative = aztec_culture.get_narrative('move', piece=piece)
    print(f"\nMove Narrative:\n{move_narrative}")
    
    # Test capture narrative
    attacker = aztec_culture.get_piece_name('knight')
    target = aztec_culture.get_piece_name('pawn')
    capture_narrative = aztec_culture.get_narrative('capture', piece=attacker, target=target)
    print(f"\nCapture Narrative:\n{capture_narrative}")
    
    # Test check narrative
    check_narrative = aztec_culture.get_narrative('check')
    print(f"\nCheck Narrative:\n{check_narrative}")
    
    # Test victory narrative
    victory_narrative = aztec_culture.get_narrative('victory')
    print(f"\nVictory Narrative:\n{victory_narrative}")

def test_cultural_weights() -> None:
    print("\n=== Testing Cultural Weights ===")
    
    # Test base weights
    print("\nBase weights:")
    for piece_type in ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']:
        weight = aztec_culture.calculate_cultural_weight(piece_type, {})
        print(f"{piece_type.title():8} -> {weight:.2f}")
    
    # Test contextual weights
    print("\nContextual weights:")
    contexts = [
        {'is_capture': True, 'is_check': False, 'is_promotion': False},
        {'is_capture': False, 'is_check': True, 'is_promotion': False},
        {'is_capture': False, 'is_check': False, 'is_promotion': True},
        {'is_capture': True, 'is_check': True, 'is_promotion': True}
    ]
    
    for context in contexts:
        print(f"\nContext: {context}")
        for piece_type in ['king', 'queen', 'bishop']:
            weight = aztec_culture.calculate_cultural_weight(piece_type, context)
            print(f"{piece_type.title():8} -> {weight:.2f}")

def test_cultural_events() -> None:
    print("\n=== Testing Cultural Events ===")
    
    events = ['sacrificio_ritual', 'guerra_florida', 'profecia_cumprida']
    for event_type in events:
        event = aztec_culture.trigger_event(event_type)
        if event:
            print(f"\nEvent: {event_type}")
            print(f"Description: {event['description']}")
            print(f"Impact: {event['impact']}")
            print(f"Triggers: {', '.join(event['triggers'])}")

def test_game_integration() -> None:
    print("\n=== Testing Game Integration ===")
    
    board = Board()
    
    # Test a few moves with cultural narratives
    moves = [
        ('e2', 'e4'),  # Pawn
        ('g1', 'f3'),  # Knight
        ('f1', 'c4'),  # Bishop
    ]
    
    for from_pos, to_pos in moves:
        piece = board.get_piece(from_pos)
        if piece:
            # Get Aztec name for piece
            aztec_name = aztec_culture.get_piece_name(piece.type.name.lower())
            
            # Generate narrative for move
            narrative = aztec_culture.get_narrative('move', piece=aztec_name)
            print(f"\nMoving {aztec_name} from {from_pos} to {to_pos}")
            print(f"Narrative: {narrative}")
            
            # Execute move
            result = board.move_piece(from_pos, to_pos)
            if result['success']:
                print("Move successful")
                print(board.display())
            else:
                print(f"Move failed: {result['error']}")

if __name__ == "__main__":
    print("\n=== Aztec Cultural Chess System Test ===\n")
    test_aztec_names()
    test_aztec_narratives()
    test_cultural_weights()
    test_cultural_events()
    test_game_integration()
