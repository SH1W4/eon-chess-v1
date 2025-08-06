#!/usr/bin/env python3

"""
Testes do Sistema de Antagonistas Híbridos
Valida a implementação dos antagonistas que combinam múltiplos perfis
"""

import unittest
from pathlib import Path
import tempfile
import yaml
from src.cultural.antagonists.hybrid_antagonist import (
    BehaviorProfile,
    CulturalProfile,
    HybridAntagonist
)

class TestHybridAntagonist(unittest.TestCase):
    def setUp(self):
        """Prepara ambiente de teste"""
        # Cria perfil de guerreiro
        self.warrior_profile = BehaviorProfile(
            name="warrior",
            patterns=["aggressive_attack", "defensive_stance", "tactical_retreat"],
            volatility=0.8,
            adaptation_rate=0.7,
            focus_areas=["combat", "territory", "honor"]
        )
        
        # Cria perfil de estrategista
        self.strategist_profile = BehaviorProfile(
            name="strategist",
            patterns=["resource_management", "diplomatic_approach", "long_term_planning"],
            volatility=0.4,
            adaptation_rate=0.9,
            focus_areas=["diplomacy", "economy", "planning"]
        )
        
        # Cria perfil cultural viking
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
        
        # Cria antagonista híbrido
        self.antagonist = HybridAntagonist(
            name="strategic_warrior",
            primary_behavior=self.warrior_profile,
            secondary_behavior=self.strategist_profile,
            cultural_profile=self.viking_profile
        )
    
    def test_antagonist_creation(self):
        """Testa criação do antagonista"""
        self.assertEqual(self.antagonist.name, "strategic_warrior")
        self.assertEqual(self.antagonist.primary_behavior.name, "warrior")
        self.assertEqual(self.antagonist.secondary_behavior.name, "strategist")
        self.assertEqual(self.antagonist.cultural_profile.name, "viking")
        
        # Verifica estado inicial
        self.assertEqual(self.antagonist.adaptation_state['behavior_volatility'], 0.0)
        self.assertEqual(self.antagonist.adaptation_state['cultural_resonance'], 0.0)
        self.assertEqual(len(self.antagonist.emergent_patterns), 0)
    
    def test_context_adaptation(self):
        """Testa adaptação ao contexto"""
        context = {
            'cultural_values': ['honor', 'strength', 'wisdom'],
            'focus_areas': ['combat', 'strategy']
        }
        
        state = self.antagonist.adapt_to_context(context)
        
        # Verifica adaptação
        self.assertGreater(state['behavior_volatility'], 0)
        self.assertGreater(state['cultural_resonance'], 0)
        self.assertGreater(state['integration_level'], 0)
        
        # Verifica geração de padrões emergentes
        self.assertGreater(len(self.antagonist.emergent_patterns), 0)
        
        # Verifica estrutura dos padrões
        for pattern in self.antagonist.emergent_patterns:
            self.assertIn('name', pattern)
            self.assertIn('base_patterns', pattern)
            self.assertIn('adaptation_rate', pattern)
            self.assertTrue(pattern['evolution_enabled'])
    
    def test_tactical_response(self):
        """Testa geração de resposta tática"""
        situation = {
            'type': 'combat_situation',
            'focus_areas': ['combat', 'territory'],
            'intensity': 0.8
        }
        
        # Adapta ao contexto primeiro
        self.antagonist.adapt_to_context({
            'cultural_values': ['honor', 'strength'],
            'focus_areas': ['combat']
        })
        
        response = self.antagonist.get_tactical_response(situation)
        
        # Verifica estrutura da resposta
        self.assertIn('focus', response)
        self.assertIn('patterns', response)
        self.assertIn('adaptation_state', response)
        self.assertIn('cultural_context', response)
        
        # Verifica relevância dos padrões
        if response['patterns']:
            pattern = response['patterns'][0]
            self.assertIn('relevance_score', pattern)
            self.assertIn('intensity', pattern)
            self.assertEqual(pattern['intensity'], situation['intensity'])
    
    def test_state_persistence(self):
        """Testa persistência de estado"""
        # Adapta ao contexto para gerar estado
        self.antagonist.adapt_to_context({
            'cultural_values': ['honor', 'strength'],
            'focus_areas': ['combat']
        })
        
        # Salva estado
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            self.antagonist.save_state(tmp.name)
            
            # Carrega estado em novo antagonista
            loaded_antagonist = HybridAntagonist.load_state(tmp.name)
            
            # Verifica dados carregados
            self.assertEqual(loaded_antagonist.name, self.antagonist.name)
            self.assertEqual(
                loaded_antagonist.primary_behavior.name,
                self.antagonist.primary_behavior.name
            )
            self.assertEqual(
                loaded_antagonist.adaptation_state,
                self.antagonist.adaptation_state
            )
            self.assertEqual(
                len(loaded_antagonist.emergent_patterns),
                len(self.antagonist.emergent_patterns)
            )
    
    def test_behavioral_focus(self):
        """Testa seleção de foco comportamental"""
        # Situação alinhada com perfil primário
        situation1 = {'focus_areas': ['combat', 'planning']}
        focus1 = self.antagonist._select_behavioral_focus(situation1)
        self.assertEqual(focus1, 'combat')
        
        # Situação alinhada com perfil secundário
        situation2 = {'focus_areas': ['diplomacy', 'economy']}
        focus2 = self.antagonist._select_behavioral_focus(situation2)
        self.assertEqual(focus2, 'diplomacy')
        
        # Situação sem alinhamento
        situation3 = {'focus_areas': ['unknown']}
        focus3 = self.antagonist._select_behavioral_focus(situation3)
        self.assertEqual(focus3, 'combat')  # Primeiro foco do perfil primário
    
    def test_cultural_resonance(self):
        """Testa cálculo de ressonância cultural"""
        # Contexto com alta sobreposição
        context1 = {'cultural_values': ['honor', 'bravery', 'strength']}
        resonance1 = self.antagonist._calculate_cultural_resonance(context1)
        self.assertGreater(resonance1, 0.5)
        
        # Contexto com baixa sobreposição
        context2 = {'cultural_values': ['peace', 'harmony']}
        resonance2 = self.antagonist._calculate_cultural_resonance(context2)
        self.assertLess(resonance2, 0.5)
        
        # Contexto vazio
        context3 = {'cultural_values': []}
        resonance3 = self.antagonist._calculate_cultural_resonance(context3)
        self.assertEqual(resonance3, 0.0)

if __name__ == '__main__':
    unittest.main()
