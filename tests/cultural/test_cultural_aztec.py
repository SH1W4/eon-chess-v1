#!/usr/bin/env python3

import sys
import os
from typing import Dict, List, Optional, Union

# Add src directory to PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from cultural.metrics import CulturalMetrics
from cultural.memory import CulturalMemory
from cultural.events import CulturalEventSystem
from cultural.narrative_generator import NarrativeGenerator

def test_aztec_cultural_system():
    print("\n=== Testing Aztec Cultural Chess System ===\n")

    # Initialize components
    metrics = CulturalMetrics()
    memory = CulturalMemory()
    events = CulturalEventSystem()
    narrative = NarrativeGenerator()

    # Load Aztec cultural data
    aztec_elements = [
        "Guerra Florida",
        "Rituais Sagrados",
        "Hierarquia Militar",
        "Sacrifício Ritual",
        "Cosmologia Asteca"
    ]

    # Test cultural impact
    impact = metrics.analyze_cultural_impact(aztec_elements)
    print("\nCultural Impact Analysis:")
    print(f"Overall Impact: {impact['overall_impact']}")
    for element, score in impact['element_scores'].items():
        print(f"- {element}: {score:.2f}")

    # Test narrative generation
    move_context = {
        'piece_type': 'Guerreiro Águia',  # Knight/Cavalo
        'from_pos': 'b1',
        'to_pos': 'c3',
        'is_capture': False
    }

    narrative_text = narrative.generate_move_narrative(**move_context)
    print("\nNarrative Test:")
    print(f"Move Context: {move_context}")
    print(f"Generated Narrative: {narrative_text}")

    # Test cultural event system
    event = events.trigger_cultural_event("sacrificio_ritual", {
        'piece_type': 'Guerreiro Jaguar',  # Pawn/Peão
        'position': 'e4',
        'is_capture': True
    })

    print("\nCultural Event Test:")
    print(f"Event Type: {event.type}")
    print(f"Description: {event.description}")
    print(f"Cultural Impact: {event.impact_score:.2f}")

    # Test cultural memory
    memory.record_event(event)
    context = memory.get_cultural_context()

    print("\nCultural Memory Test:")
    print(f"Recorded Events: {len(memory.events)}")
    print(f"Current Context: {context}")

if __name__ == "__main__":
    test_aztec_cultural_system()
