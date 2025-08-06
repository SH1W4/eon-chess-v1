#!/usr/bin/env python3

"""
Suite de Testes Comportamentais
Validação completa do sistema comportamental e suas integrações
"""

import unittest
from pathlib import Path
import tempfile
import yaml
import json
from typing import Dict, List
from dataclasses import dataclass

from src.cultural.antagonists.hybrid_antagonist import (
    HybridAntagonist,
    BehaviorProfile,
    CulturalProfile
)
from src.cultural.narrative.dynamic_narrative import (
    DynamicNarrative,
    NarrativeElement,
    NarrativeArc,
    CulturalContext
)

@dataclass
class BehavioralEvent:
    """Evento comportamental para testes"""
    type: str
    intensity: float
    cultural_values: List[str]
    behavioral_triggers: List[str]
    expected_response: Dict[str, float]

class TestBehavioralSystem(unittest.TestCase):
    def setUp(self):
        """Prepara ambiente de teste"""
        # Configura antagonista híbrido
        self.warrior_profile = BehaviorProfile(
            name="warrior",
            patterns=["aggressive_attack", "defensive_stance", "tactical_retreat"],
            volatility=0.8,
            adaptation_rate=0.7,
            focus_areas=["combat", "territory", "honor"]
        )
        
        self.strategist_profile = BehaviorProfile(
            name="strategist",
            patterns=["resource_management", "diplomatic_approach", "planning"],
            volatility=0.4,
            adaptation_rate=0.9,
            focus_areas=["diplomacy", "economy", "planning"]
        )
        
        self.viking_profile = CulturalProfile(
            name="viking",
            values=["honor", "bravery", "strength", "exploration"],
            practices=["raiding", "seafaring", "trading"],
            historical_context={
                "era": "viking_age",
                "region": "scandinavia",
                "notable_events": ["norse_exploration", "trade_establishment"]
            }
        )
        
        self.antagonist = HybridAntagonist(
            name="strategic_warrior",
            primary_behavior=self.warrior_profile,
            secondary_behavior=self.strategist_profile,
            cultural_profile=self.viking_profile
        )
        
        # Configura sistema narrativo
        self.narrative_system = DynamicNarrative()
        self.cultural_context = CulturalContext(
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
        
        # Eventos de teste
        self.test_events = [
            BehavioralEvent(
                type="combat_challenge",
                intensity=0.8,
                cultural_values=["honor", "bravery"],
                behavioral_triggers=["aggressive_attack", "tactical_retreat"],
                expected_response={
                    "aggression": 0.7,
                    "tactical": 0.8,
                    "cultural_alignment": 0.9
                }
            ),
            BehavioralEvent(
                type="resource_dispute",
                intensity=0.6,
                cultural_values=["strength", "honor"],
                behavioral_triggers=["resource_management", "defensive_stance"],
                expected_response={
                    "resource_focus": 0.8,
                    "defensive": 0.6,
                    "cultural_alignment": 0.7
                }
            ),
            BehavioralEvent(
                type="diplomatic_opportunity",
                intensity=0.4,
                cultural_values=["honor", "exploration"],
                behavioral_triggers=["diplomatic_approach", "planning"],
                expected_response={
                    "diplomatic": 0.9,
                    "strategic": 0.7,
                    "cultural_alignment": 0.8
                }
            )
        ]
    
    def test_behavioral_response_consistency(self):
        """Testa consistência das respostas comportamentais"""
        context = {"focus_areas": ["combat", "territory"]}
        
        # Testa múltiplas respostas
        responses = []
        for _ in range(5):
            response = self.antagonist.get_tactical_response(context)
            responses.append(response)
        
        # Verifica consistência
        base_focus = responses[0]['focus']
        base_patterns = set(p['name'] for p in responses[0]['patterns'])
        
        for response in responses[1:]:
            # Foco deve ser consistente para mesmo contexto
            self.assertEqual(response['focus'], base_focus)
            
            # Padrões podem variar mas devem manter sobreposição
            current_patterns = set(p['name'] for p in response['patterns'])
            overlap = len(base_patterns.intersection(current_patterns))
            self.assertGreater(overlap / len(base_patterns), 0.5)
    
    def test_behavioral_adaptation(self):
        """Testa adaptação comportamental a diferentes contextos"""
        contexts = [
            {
                "type": "combat_situation",
                "focus_areas": ["combat", "territory"],
                "intensity": 0.8
            },
            {
                "type": "diplomatic_situation",
                "focus_areas": ["diplomacy", "economy"],
                "intensity": 0.5
            },
            {
                "type": "mixed_situation",
                "focus_areas": ["combat", "planning"],
                "intensity": 0.7
            }
        ]
        
        responses = []
        for context in contexts:
            self.antagonist.adapt_to_context({"cultural_values": ["honor"]})
            response = self.antagonist.get_tactical_response(context)
            responses.append(response)
        
        # Verifica adaptação apropriada
        combat_response = responses[0]
        self.assertEqual(combat_response['focus'], "combat")
        self.assertTrue(
            any("aggressive" in p['name'].lower() 
                for p in combat_response['patterns'])
        )
        
        diplomatic_response = responses[1]
        self.assertEqual(diplomatic_response['focus'], "diplomacy")
        self.assertTrue(
            any("diplomatic" in p['name'].lower() 
                for p in diplomatic_response['patterns'])
        )
        
        mixed_response = responses[2]
        self.assertTrue(
            mixed_response['focus'] in ["combat", "planning"]
        )
    
    def test_cultural_behavioral_integration(self):
        """Testa integração entre comportamento e cultura"""
        # Gera narrativa inicial
        narrative = self.narrative_system.generate_narrative(
            self.cultural_context
        )
        
        # Adapta antagonista ao contexto narrativo
        self.antagonist.adapt_to_context({
            "cultural_values": self.cultural_context.values,
            "focus_areas": ["combat", "territory"]
        })
        
        # Simula eventos comportamentais
        for event in self.test_events:
            # Evolui narrativa
            narrative = self.narrative_system.evolve_narrative(
                narrative,
                self.cultural_context,
                [{
                    "type": event.type,
                    "intensity": event.intensity,
                    "cultural_values": event.cultural_values
                }]
            )
            
            # Gera resposta comportamental
            response = self.antagonist.get_tactical_response({
                "type": event.type,
                "focus_areas": event.behavioral_triggers,
                "intensity": event.intensity
            })
            
            # Verifica integração
            self.assertGreater(
                response['cultural_context']['values'].count(
                    event.cultural_values[0]
                ), 0
            )
            
            # Verifica alinhamento de resposta
            pattern_names = [p['name'] for p in response['patterns']]
            self.assertTrue(
                any(trigger in " ".join(pattern_names).lower()
                    for trigger in event.behavioral_triggers)
            )
    
    def test_behavioral_evolution(self):
        """Testa evolução comportamental ao longo do tempo"""
        # Sequência de eventos evolutivos
        evolution_sequence = [
            {
                "stage": "initial",
                "context": {
                    "cultural_values": ["honor", "bravery"],
                    "focus_areas": ["combat"],
                    "intensity": 0.5
                }
            },
            {
                "stage": "development",
                "context": {
                    "cultural_values": ["honor", "strength"],
                    "focus_areas": ["combat", "territory"],
                    "intensity": 0.7
                }
            },
            {
                "stage": "mastery",
                "context": {
                    "cultural_values": ["honor", "strength", "bravery"],
                    "focus_areas": ["combat", "territory", "planning"],
                    "intensity": 0.9
                }
            }
        ]
        
        evolution_states = []
        for stage in evolution_sequence:
            # Adapta ao novo contexto
            state = self.antagonist.adapt_to_context(stage["context"])
            
            # Gera resposta comportamental
            response = self.antagonist.get_tactical_response({
                "type": "evolution_check",
                "focus_areas": stage["context"]["focus_areas"],
                "intensity": stage["context"]["intensity"]
            })
            
            evolution_states.append({
                "stage": stage["stage"],
                "adaptation_state": state,
                "response": response
            })
        
        # Verifica evolução progressiva
        for i in range(1, len(evolution_states)):
            current = evolution_states[i]
            previous = evolution_states[i-1]
            
            # Adaptação deve melhorar
            self.assertGreater(
                current["adaptation_state"]["integration_level"],
                previous["adaptation_state"]["integration_level"]
            )
            
            # Respostas devem ficar mais sofisticadas
            current_patterns = len(current["response"]["patterns"])
            previous_patterns = len(previous["response"]["patterns"])
            self.assertGreaterEqual(current_patterns, previous_patterns)
    
    def test_behavioral_pattern_emergence(self):
        """Testa emergência de padrões comportamentais"""
        # Adapta ao contexto inicial
        self.antagonist.adapt_to_context({
            "cultural_values": ["honor", "bravery"],
            "focus_areas": ["combat", "planning"]
        })
        
        initial_patterns = set(
            pattern["name"]
            for pattern in self.antagonist.emergent_patterns
        )
        
        # Simula sequência de eventos
        events = [
            {
                "type": "combat_situation",
                "focus_areas": ["combat", "territory"],
                "intensity": 0.8,
                "repeat": 3
            },
            {
                "type": "planning_situation",
                "focus_areas": ["planning", "diplomacy"],
                "intensity": 0.6,
                "repeat": 2
            }
        ]
        
        # Processa eventos
        for event in events:
            for _ in range(event["repeat"]):
                self.antagonist.adapt_to_context({
                    "cultural_values": ["honor", "bravery"],
                    "focus_areas": event["focus_areas"]
                })
                
                response = self.antagonist.get_tactical_response({
                    "type": event["type"],
                    "focus_areas": event["focus_areas"],
                    "intensity": event["intensity"]
                })
        
        # Verifica emergência de novos padrões
        final_patterns = set(
            pattern["name"]
            for pattern in self.antagonist.emergent_patterns
        )
        
        # Deve haver novos padrões
        self.assertGreater(len(final_patterns), len(initial_patterns))
        
        # Novos padrões devem ser hibridizações dos existentes
        new_patterns = final_patterns - initial_patterns
        for pattern in new_patterns:
            self.assertTrue(
                any(base in pattern.lower() 
                    for base in ["combat", "planning", "territory", "diplomacy"])
            )
    
    def test_behavioral_stability(self):
        """Testa estabilidade comportamental sob estresse"""
        # Configuração inicial
        self.antagonist.adapt_to_context({
            "cultural_values": ["honor", "bravery"],
            "focus_areas": ["combat", "planning"],
            "intensity": 0.5
        })
        
        initial_state = self.antagonist.adaptation_state.copy()
        
        # Sequência de eventos estressantes
        stress_events = [
            {
                "type": "high_pressure",
                "focus_areas": ["combat", "territory"],
                "intensity": 0.9
            },
            {
                "type": "crisis",
                "focus_areas": ["planning", "diplomacy"],
                "intensity": 0.95
            },
            {
                "type": "conflict",
                "focus_areas": ["combat", "economy"],
                "intensity": 0.85
            }
        ]
        
        responses = []
        for event in stress_events:
            # Adapta ao evento estressante
            self.antagonist.adapt_to_context({
                "cultural_values": ["honor", "bravery"],
                "focus_areas": event["focus_areas"]
            })
            
            # Gera resposta
            response = self.antagonist.get_tactical_response(event)
            responses.append(response)
        
        # Verifica estabilidade
        final_state = self.antagonist.adaptation_state
        
        # Volatilidade não deve aumentar drasticamente
        volatility_change = abs(
            final_state["behavior_volatility"] - 
            initial_state["behavior_volatility"]
        )
        self.assertLess(volatility_change, 0.3)
        
        # Ressonância cultural deve se manter
        cultural_change = abs(
            final_state["cultural_resonance"] - 
            initial_state["cultural_resonance"]
        )
        self.assertLess(cultural_change, 0.2)
        
        # Respostas devem manter coerência
        for i in range(1, len(responses)):
            current = responses[i]
            previous = responses[i-1]
            
            # Deve haver alguma sobreposição de padrões
            current_patterns = set(p["name"] for p in current["patterns"])
            previous_patterns = set(p["name"] for p in previous["patterns"])
            
            overlap = len(current_patterns.intersection(previous_patterns))
            self.assertGreater(overlap, 0)
    
    def test_behavioral_recovery(self):
        """Testa recuperação comportamental após eventos extremos"""
        # Estado inicial estável
        self.antagonist.adapt_to_context({
            "cultural_values": ["honor", "bravery"],
            "focus_areas": ["combat", "planning"],
            "intensity": 0.5
        })
        
        initial_state = self.antagonist.adaptation_state.copy()
        
        # Evento extremo
        extreme_event = {
            "type": "critical_situation",
            "focus_areas": ["combat", "territory", "economy"],
            "intensity": 1.0
        }
        
        # Resposta ao evento extremo
        self.antagonist.adapt_to_context({
            "cultural_values": ["honor", "strength"],
            "focus_areas": extreme_event["focus_areas"]
        })
        
        crisis_response = self.antagonist.get_tactical_response(extreme_event)
        crisis_state = self.antagonist.adaptation_state.copy()
        
        # Sequência de recuperação
        recovery_events = [
            {
                "type": "stabilization",
                "focus_areas": ["planning", "diplomacy"],
                "intensity": 0.4
            },
            {
                "type": "normalization",
                "focus_areas": ["combat", "economy"],
                "intensity": 0.5
            },
            {
                "type": "integration",
                "focus_areas": ["combat", "planning"],
                "intensity": 0.6
            }
        ]
        
        recovery_states = []
        for event in recovery_events:
            self.antagonist.adapt_to_context({
                "cultural_values": ["honor", "bravery"],
                "focus_areas": event["focus_areas"]
            })
            
            response = self.antagonist.get_tactical_response(event)
            recovery_states.append(self.antagonist.adaptation_state.copy())
        
        # Verifica processo de recuperação
        final_state = recovery_states[-1]
        
        # Volatilidade deve diminuir
        self.assertLess(
            final_state["behavior_volatility"],
            crisis_state["behavior_volatility"]
        )
        
        # Ressonância cultural deve se recuperar
        self.assertGreater(
            final_state["cultural_resonance"],
            crisis_state["cultural_resonance"]
        )
        
        # Estado final deve se aproximar do inicial
        for metric in ["behavior_volatility", "cultural_resonance"]:
            recovery_diff = abs(
                final_state[metric] - initial_state[metric]
            )
            crisis_diff = abs(
                crisis_state[metric] - initial_state[metric]
            )
            self.assertLess(recovery_diff, crisis_diff)

if __name__ == '__main__':
    unittest.main()
