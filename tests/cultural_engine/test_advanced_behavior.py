#!/usr/bin/env python3

"""
Testes Avançados de Comportamento e Narrativas
Validação profunda dos sistemas culturais e narrativos
"""

import unittest
import yaml
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

class TestAdvancedBehavior(unittest.TestCase):
    def setUp(self):
        self.data_dir = Path('../../cultural_data')
        self.load_test_data()
        
    def load_test_data(self):
        """Carrega dados de teste"""
        # Carregar configurações culturais
        for culture in ['viking', 'mayan', 'samurai']:
            config_path = self.data_dir / "configurations" / "themes" / f"{culture}.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    setattr(self, f"{culture}_config", yaml.safe_load(f))
        
        # Carregar configurações de antagonistas
        antagonist_path = self.data_dir / "antagonists" / "hybrid"
        for antagonist in ['strategicwarrior', 'mysticcommander', 'economicwarlord']:
            config_path = antagonist_path / f"{antagonist}.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    setattr(self, f"{antagonist}_config", yaml.safe_load(f))
    
    def test_cultural_military_balance(self):
        """Testa equilíbrio militar entre culturas"""
        viking_military = set(self.viking_config["attributes"]["military_focus"])
        mayan_military = set(self.mayan_config["attributes"]["military_focus"])
        samurai_military = set(self.samurai_config["attributes"]["military_focus"])
        
        # Verificar sobreposição limitada
        viking_mayan_overlap = viking_military.intersection(mayan_military)
        viking_samurai_overlap = viking_military.intersection(samurai_military)
        mayan_samurai_overlap = mayan_military.intersection(samurai_military)
        
        # Não deve haver muita sobreposição entre culturas
        self.assertLess(len(viking_mayan_overlap), len(viking_military) // 2)
        self.assertLess(len(viking_samurai_overlap), len(viking_military) // 2)
        self.assertLess(len(mayan_samurai_overlap), len(mayan_military) // 2)
    
    def test_cultural_economic_synergy(self):
        """Testa sinergias econômicas entre culturas"""
        viking_economic = set(self.viking_config["attributes"]["economic_patterns"])
        mayan_economic = set(self.mayan_config["attributes"]["economic_patterns"])
        samurai_economic = set(self.samurai_config["attributes"]["economic_patterns"])
        
        # Deve haver alguma sinergia econômica
        all_economic = viking_economic.union(mayan_economic).union(samurai_economic)
        self.assertGreater(len(all_economic), 
                          max(len(viking_economic), len(mayan_economic), len(samurai_economic)))
    
    def test_antagonist_complexity(self):
        """Testa complexidade dos antagonistas híbridos"""
        for antagonist in ['strategicwarrior', 'mysticcommander', 'economicwarlord']:
            config = getattr(self, f"{antagonist}_config")
            
            # Verificar comportamentos emergentes
            emergent = config["behavior_patterns"]["emergent"]
            self.assertGreater(len(emergent), 0)
            
            # Verificar adaptação
            self.assertGreater(config["adaptation_rules"]["context_sensitivity"], 0.5)
            self.assertTrue(config["adaptation_rules"]["evolution_enabled"])
    
    def test_antagonist_balance(self):
        """Testa balanceamento entre antagonistas"""
        warriors = self.strategicwarrior_config["profiles"]
        mystics = self.mysticcommander_config["profiles"]
        economics = self.economicwarlord_config["profiles"]
        
        # Verificar diferenciação de perfis
        all_patterns = set()
        for config in [warriors, mystics, economics]:
            patterns = set(config["primary_profile"]["patterns"])
            # Cada antagonista deve ter padrões únicos
            overlap = patterns.intersection(all_patterns)
            self.assertLess(len(overlap), len(patterns) // 2)
            all_patterns.update(patterns)
    
    def test_narrative_depth(self):
        """Testa profundidade das narrativas"""
        narratives_path = self.data_dir / "narratives" / "dynamic"
        for narrative in ['culturalconflict', 'mysticaljourney', 'empireevolution']:
            config_path = narratives_path / f"{narrative}.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                    
                # Verificar elementos narrativos
                self.assertGreater(len(config["elements"]["themes"]), 2)
                self.assertGreater(len(config["elements"]["major_triggers"]), 2)
                self.assertGreater(len(config["elements"]["minor_triggers"]), 2)
                
                # Verificar adaptação narrativa
                self.assertGreater(config["adaptation_rules"]["context_sensitivity"], 0.7)
                self.assertGreater(config["adaptation_rules"]["narrative_flexibility"], 0.6)
    
    def test_narrative_integration(self):
        """Testa integração entre narrativas e culturas"""
        narratives_path = self.data_dir / "narratives" / "dynamic"
        for narrative in ['culturalconflict', 'mysticaljourney', 'empireevolution']:
            config_path = narratives_path / f"{narrative}.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    narrative_config = yaml.safe_load(f)
                
                # Verificar integração com cada cultura
                for culture in ['viking', 'mayan', 'samurai']:
                    culture_config = getattr(self, f"{culture}_config")
                    
                    # Deve haver elementos culturais nas narrativas
                    cultural_values = set(culture_config["attributes"]["cultural_values"])
                    narrative_elements = set(narrative_config["elements"]["themes"])
                    
                    intersection = cultural_values.intersection(narrative_elements)
                    self.assertGreater(len(intersection), 0)
    
    def test_emergent_behavior_chains(self):
        """Testa cadeias de comportamentos emergentes"""
        for antagonist in ['strategicwarrior', 'mysticcommander', 'economicwarlord']:
            config = getattr(self, f"{antagonist}_config")
            emergent = config["behavior_patterns"]["emergent"]
            
            # Verificar conexões entre comportamentos
            for behavior in emergent:
                self.assertEqual(len(behavior["base_patterns"]), 2)
                self.assertGreater(behavior["adaptation_rate"], 0.5)
                self.assertTrue(behavior["evolution_enabled"])

if __name__ == '__main__':
    unittest.main()
