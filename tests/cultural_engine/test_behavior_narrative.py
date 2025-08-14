#!/usr/bin/env python3

"""
Testes de Comportamento e Narrativos
Valida os comportamentos emergentes e sistemas narrativos
"""

import unittest
import yaml
from pathlib import Path

class TestBehaviorNarrative(unittest.TestCase):
    def setUp(self):
        self.cultural_data = Path('../../cultural_data')
        self.load_test_data()
        
    def load_test_data(self):
        """Carrega dados de teste"""
        # Carregar configurações de culturas
        viking_path = self.cultural_data / "configurations" / "themes" / "viking.yaml"
        with open(viking_path) as f:
            self.viking_config = yaml.safe_load(f)
            
        # Carregar configurações de antagonistas
        strategic_warrior_path = self.cultural_data / "antagonists" / "hybrid" / "strategicwarrior.yaml"
        with open(strategic_warrior_path) as f:
            self.antagonist_config = yaml.safe_load(f)
            
        # Carregar configurações narrativas
        cultural_conflict_path = self.cultural_data / "narratives" / "dynamic" / "culturalconflict.yaml"
        with open(cultural_conflict_path) as f:
            self.narrative_config = yaml.safe_load(f)
    
    def test_cultural_behavior(self):
        """Testa comportamentos culturais"""
        # Testar elementos militares
        self.assertIn("naval_warfare", self.viking_config["attributes"]["military_focus"])
        self.assertIn("raid_tactics", self.viking_config["attributes"]["military_focus"])
        
        # Testar elementos econômicos
        self.assertIn("trade_routes", self.viking_config["attributes"]["economic_patterns"])
        self.assertIn("exploration", self.viking_config["attributes"]["economic_patterns"])
        
        # Testar valores culturais
        self.assertIn("honor", self.viking_config["attributes"]["cultural_values"])
        self.assertIn("bravery", self.viking_config["attributes"]["cultural_values"])
    
    def test_antagonist_behavior(self):
        """Testa comportamentos de antagonistas"""
        # Testar perfil primário
        self.assertEqual(self.antagonist_config["profiles"]["primary_profile"]["name"], "warrior")
        self.assertIn("aggressive_tactics", 
                     self.antagonist_config["profiles"]["primary_profile"]["patterns"])
        
        # Testar perfil secundário
        self.assertEqual(self.antagonist_config["profiles"]["secondary_profile"]["name"], "strategist")
        self.assertIn("long_term_planning", 
                     self.antagonist_config["profiles"]["secondary_profile"]["patterns"])
        
        # Testar comportamentos emergentes
        self.assertTrue(len(self.antagonist_config["behavior_patterns"]["emergent"]) > 0)
        
    def test_narrative_system(self):
        """Testa sistema narrativo"""
        # Testar elementos narrativos
        self.assertIn("cultural_clash", self.narrative_config["elements"]["themes"])
        self.assertIn("power_struggle", self.narrative_config["elements"]["themes"])
        
        # Testar gatilhos
        self.assertIn("territory_control", self.narrative_config["elements"]["major_triggers"])
        self.assertIn("cultural_supremacy", self.narrative_config["elements"]["major_triggers"])
        
        # Testar condições de vitória
        self.assertIn("complete_dominance", self.narrative_config["elements"]["victory_conditions"])
        self.assertIn("peaceful_coexistence", self.narrative_config["elements"]["victory_conditions"])
        
    def test_cultural_integration(self):
        """Testa integração entre cultura e narrativa"""
        # Verificar alinhamento de valores culturais com narrativa
        cultural_values = set(self.viking_config["attributes"]["cultural_values"])
        narrative_themes = set(self.narrative_config["elements"]["themes"])
        
        # Deve haver alguma sobreposição entre valores culturais e temas narrativos
        self.assertTrue(len(cultural_values.intersection(narrative_themes)) > 0)
        
    def test_antagonist_narrative(self):
        """Testa integração entre antagonistas e narrativa"""
        # Verificar alinhamento de comportamentos com arcos narrativos
        antagonist_patterns = set(self.antagonist_config["profiles"]["primary_profile"]["patterns"])
        narrative_triggers = set(self.narrative_config["elements"]["major_triggers"])
        
        # Deve haver alguma sobreposição entre padrões de comportamento e gatilhos narrativos
        self.assertTrue(len(antagonist_patterns.intersection(narrative_triggers)) > 0)

if __name__ == '__main__':
    unittest.main()
