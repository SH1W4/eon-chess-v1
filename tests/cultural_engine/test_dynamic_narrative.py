#!/usr/bin/env python3

"""
Testes do Sistema de Narrativas Dinâmicas
Valida a geração e evolução de narrativas adaptativas
"""

import unittest
from pathlib import Path
import tempfile
import yaml
from src.cultural.narrative.dynamic_narrative import (
    DynamicNarrative,
    NarrativeElement,
    NarrativeArc,
    CulturalContext
)

class TestDynamicNarrative(unittest.TestCase):
    def setUp(self):
        """Prepara ambiente de teste"""
        self.narrative_system = DynamicNarrative()
        
        # Criar contexto de teste
        self.test_context = CulturalContext(
            culture_name="viking",
            values=["honor", "bravery", "strength", "exploration"],
            practices=["raiding", "seafaring", "trading"],
            historical_elements={
                "era": "viking_age",
                "region": "scandinavia",
                "notable_events": ["norse_exploration", "trade_establishment"]
            },
            current_state={
                "tension": 0.7,
                "cultural_resonance": 0.8,
                "adaptation": 0.6
            }
        )
        
        # Criar elementos narrativos de teste
        self.test_elements = [
            NarrativeElement(
                name="confronto_honra",
                type="conflict",
                weight=0.8,
                cultural_value=0.9,
                adaptability=0.7
            ),
            NarrativeElement(
                name="jornada_exploração",
                type="journey",
                weight=0.85,
                cultural_value=0.85,
                adaptability=0.8
            ),
            NarrativeElement(
                name="ritual_ancestral",
                type="tradition",
                weight=0.9,
                cultural_value=0.95,
                adaptability=0.6
            )
        ]
        
        # Criar arco narrativo de teste
        self.test_arc = NarrativeArc(
            name="conflito_cultural",
            stages=[
                "tensão_inicial",
                "escalada_conflito",
                "confronto_direto",
                "resolução"
            ],
            intensity_curve=[0.3, 0.6, 0.9, 0.5],
            cultural_elements=self.test_elements,
            resolution_paths=[
                "vitória_honrosa",
                "acordo_pacífico",
                "síntese_cultural"
            ]
        )
        
        # Carregar arco no sistema
        self.narrative_system.arcs[self.test_arc.name] = self.test_arc
        for element in self.test_elements:
            self.narrative_system.elements[element.name] = element
    
    def test_narrative_generation(self):
        """Testa geração de narrativa"""
        narrative = self.narrative_system.generate_narrative(self.test_context)
        
        # Verifica estrutura básica
        self.assertIn('arc', narrative)
        self.assertIn('stages', narrative)
        self.assertIn('elements', narrative)
        self.assertIn('state', narrative)
        
        # Verifica estado inicial
        self.assertEqual(narrative['state']['current_stage'], 0)
        self.assertGreater(narrative['state']['intensity'], 0)
        self.assertGreater(narrative['state']['cultural_resonance'], 0)
        
        # Verifica elementos adaptados
        self.assertGreater(len(narrative['elements']), 0)
        for element in narrative['elements']:
            self.assertIn('name', element)
            self.assertIn('weight', element)
            self.assertIn('cultural_value', element)
    
    def test_narrative_evolution(self):
        """Testa evolução da narrativa"""
        # Gera narrativa inicial
        initial_narrative = self.narrative_system.generate_narrative(
            self.test_context
        )
        
        # Simula eventos
        test_events = [
            {
                'type': 'conflict',
                'intensity': 0.8,
                'cultural_values': ['honor', 'strength'],
                'path_suggestion': 'vitória_honrosa'
            },
            {
                'type': 'resolution',
                'intensity': 0.4,
                'cultural_values': ['wisdom', 'harmony'],
                'path_suggestion': 'acordo_pacífico'
            }
        ]
        
        # Evolui narrativa
        evolved_narrative = self.narrative_system.evolve_narrative(
            initial_narrative,
            self.test_context,
            test_events
        )
        
        # Verifica evolução
        self.assertNotEqual(
            evolved_narrative['state']['intensity'],
            initial_narrative['state']['intensity']
        )
        self.assertGreater(len(self.narrative_system.evolution_history), 0)
    
    def test_cultural_alignment(self):
        """Testa alinhamento cultural"""
        alignment = self.narrative_system._calculate_cultural_alignment(
            self.test_elements,
            self.test_context
        )
        
        # Verifica cálculo de alinhamento
        self.assertGreater(alignment, 0)
        self.assertLessEqual(alignment, 1)
        
        # Testa com contexto diferente
        different_context = CulturalContext(
            culture_name="peaceful",
            values=["peace", "harmony", "wisdom"],
            practices=["meditation", "farming"],
            historical_elements={},
            current_state={"tension": 0.3}
        )
        
        different_alignment = self.narrative_system._calculate_cultural_alignment(
            self.test_elements,
            different_context
        )
        
        # Alinhamento deve ser menor com contexto diferente
        self.assertLess(different_alignment, alignment)
    
    def test_intensity_calculation(self):
        """Testa cálculo de intensidade"""
        intensity = self.narrative_system._calculate_intensity(
            self.test_context
        )
        
        # Verifica valor de intensidade
        self.assertGreater(intensity, 0)
        self.assertLessEqual(intensity, 1)
        
        # Testa com estados diferentes
        high_tension_context = CulturalContext(
            culture_name="viking",
            values=self.test_context.values,
            practices=self.test_context.practices,
            historical_elements=self.test_context.historical_elements,
            current_state={"tension": 0.9, "conflict": 0.8}
        )
        
        high_intensity = self.narrative_system._calculate_intensity(
            high_tension_context
        )
        
        self.assertGreater(high_intensity, intensity)
    
    def test_path_viability(self):
        """Testa viabilidade de caminhos narrativos"""
        # Testa caminho alinhado com valores
        viable_path = "jornada_honra_bravura"
        self.assertTrue(
            self.narrative_system._is_path_viable(
                viable_path,
                self.test_context
            )
        )
        
        # Testa caminho não alinhado
        non_viable_path = "caminho_paz_harmonia"
        self.assertFalse(
            self.narrative_system._is_path_viable(
                non_viable_path,
                self.test_context
            )
        )
    
    def test_narrative_consistency(self):
        """Testa consistência narrativa ao longo do tempo"""
        # Gera narrativa inicial
        narrative = self.narrative_system.generate_narrative(self.test_context)
        
        # Evolui múltiplas vezes
        events_sequence = [
            # Sequência 1: Escalada de tensão
            [{
                'type': 'conflict',
                'intensity': 0.7,
                'cultural_values': ['honor', 'strength']
            }],
            # Sequência 2: Pico de conflito
            [{
                'type': 'confrontation',
                'intensity': 0.9,
                'cultural_values': ['bravery', 'strength']
            }],
            # Sequência 3: Resolução
            [{
                'type': 'resolution',
                'intensity': 0.5,
                'cultural_values': ['honor', 'wisdom']
            }]
        ]
        
        previous_stage = narrative['state']['current_stage']
        evolution_states = []
        
        for events in events_sequence:
            narrative = self.narrative_system.evolve_narrative(
                narrative,
                self.test_context,
                events
            )
            evolution_states.append(narrative['state'])
            
            # Verifica progressão
            current_stage = narrative['state']['current_stage']
            self.assertGreaterEqual(current_stage, previous_stage)
            previous_stage = current_stage
        
        # Verifica coerência da evolução
        self.assertEqual(len(evolution_states), len(events_sequence))
        self.assertGreater(
            evolution_states[-1]['cultural_resonance'],
            evolution_states[0]['cultural_resonance']
        )
    
    def test_element_adaptation(self):
        """Testa adaptação de elementos narrativos"""
        # Adapta elementos ao contexto
        adapted_elements = self.narrative_system._adapt_elements(
            self.test_elements,
            self.test_context
        )
        
        # Verifica adaptações
        self.assertEqual(len(adapted_elements), len(self.test_elements))
        for element in adapted_elements:
            self.assertIn('weight', element)
            self.assertIn('cultural_value', element)
            self.assertIn('adaptability', element)
            
            # Verifica se pesos foram ajustados
            original_element = next(
                e for e in self.test_elements
                if e.name == element['name']
            )
            self.assertNotEqual(element['weight'], original_element.weight)
    
    def test_cultural_resonance(self):
        """Testa cálculo de ressonância cultural"""
        resonance = self.narrative_system._calculate_resonance(
            self.test_context
        )
        
        # Verifica valor de ressonância
        self.assertGreater(resonance, 0)
        self.assertLessEqual(resonance, 1)
        
        # Testa com contexto altamente alinhado
        aligned_context = CulturalContext(
            culture_name="viking",
            values=self.test_context.values,
            practices=self.test_context.practices,
            historical_elements=self.test_context.historical_elements,
            current_state={
                value: 0.9 for value in self.test_context.values
            }
        )
        
        high_resonance = self.narrative_system._calculate_resonance(
            aligned_context
        )
        
        self.assertGreater(high_resonance, resonance)

if __name__ == '__main__':
    unittest.main()
