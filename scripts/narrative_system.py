#!/usr/bin/env python3

"""
Sistema Narrativo Dinâmico do CHESS
Implementa geração de narrativas dinâmicas e elementos dramáticos avançados
"""

import logging
import yaml
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='narrative_system.log'
)

class NarrativeSystem:
    def __init__(self):
        self.config_dir = Path('../config')
        self.data_dir = Path('../cultural_data/narratives')
        
    def create_dynamic_narrative(self, name, elements):
        """Cria uma nova narrativa dinâmica"""
        logging.info(f"Criando narrativa dinâmica: {name}")
        config_path = self.data_dir / "dynamic" / f"{name.lower()}.yaml"
        
        narrative_config = {
            "name": name,
            "type": "dynamic",
            "elements": elements,
            "dramatic_elements": {
                "arcs": self.generate_dramatic_arcs(elements),
                "climax_points": self.generate_climax_points(elements),
                "resolution_paths": self.generate_resolution_paths(elements)
            },
            "adaptation_rules": {
                "context_sensitivity": 0.9,
                "narrative_flexibility": 0.7,
                "evolution_enabled": True
            }
        }
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(narrative_config, f)
            
    def generate_dramatic_arcs(self, elements):
        """Gera arcos dramáticos baseados nos elementos narrativos"""
        arcs = []
        for theme in elements.get("themes", []):
            arc = {
                "theme": theme,
                "phases": ["setup", "development", "climax", "resolution"],
                "adaptation": {
                    "intensity": 0.8,
                    "pacing": "dynamic",
                    "context_aware": True
                }
            }
            arcs.append(arc)
        return arcs
    
    def generate_climax_points(self, elements):
        """Gera pontos de clímax para a narrativa"""
        return [
            {
                "type": "major",
                "triggers": elements.get("major_triggers", []),
                "intensity": 0.9,
                "adaptation": True
            },
            {
                "type": "minor",
                "triggers": elements.get("minor_triggers", []),
                "intensity": 0.6,
                "adaptation": True
            }
        ]
    
    def generate_resolution_paths(self, elements):
        """Gera caminhos de resolução possíveis"""
        return [
            {
                "type": "victory",
                "conditions": elements.get("victory_conditions", []),
                "impact": "major"
            },
            {
                "type": "strategic",
                "conditions": elements.get("strategic_conditions", []),
                "impact": "moderate"
            },
            {
                "type": "cultural",
                "conditions": elements.get("cultural_conditions", []),
                "impact": "significant"
            }
        ]

def main():
    narrative = NarrativeSystem()
    
    # Implementação de Narrativas Dinâmicas
    cultural_conflict = {
        "themes": ["cultural_clash", "power_struggle", "adaptation"],
        "major_triggers": ["territory_control", "resource_dominance", "cultural_supremacy"],
        "minor_triggers": ["local_disputes", "resource_competition", "cultural_exchange"],
        "victory_conditions": ["complete_dominance", "cultural_assimilation", "peaceful_coexistence"],
        "strategic_conditions": ["resource_balance", "territorial_agreement", "cultural_respect"],
        "cultural_conditions": ["shared_values", "cultural_understanding", "mutual_growth"]
    }
    narrative.create_dynamic_narrative("CulturalConflict", cultural_conflict)
    
    mystical_journey = {
        "themes": ["spiritual_growth", "inner_conflict", "enlightenment"],
        "major_triggers": ["spiritual_awakening", "existential_crisis", "divine_intervention"],
        "minor_triggers": ["personal_challenges", "moral_choices", "spiritual_tests"],
        "victory_conditions": ["spiritual_mastery", "inner_peace", "enlightened_leadership"],
        "strategic_conditions": ["balanced_growth", "mindful_decisions", "harmonious_existence"],
        "cultural_conditions": ["cultural_transcendence", "spiritual_harmony", "collective_growth"]
    }
    narrative.create_dynamic_narrative("MysticalJourney", mystical_journey)
    
    empire_evolution = {
        "themes": ["empire_building", "civilization_growth", "legacy_creation"],
        "major_triggers": ["empire_formation", "golden_age", "civilization_crisis"],
        "minor_triggers": ["cultural_developments", "technological_advances", "social_changes"],
        "victory_conditions": ["empire_dominance", "cultural_achievement", "lasting_legacy"],
        "strategic_conditions": ["sustainable_growth", "balanced_expansion", "cultural_preservation"],
        "cultural_conditions": ["cultural_excellence", "societal_harmony", "historical_impact"]
    }
    narrative.create_dynamic_narrative("EmpireEvolution", empire_evolution)

if __name__ == "__main__":
    main()
