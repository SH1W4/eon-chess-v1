#!/usr/bin/env python3

"""
Sistema de Antagonistas Híbridos
Implementa antagonistas que combinam diferentes perfis culturais e comportamentais
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO)

@dataclass
class BehaviorProfile:
    """Perfil comportamental do antagonista"""
    name: str
    patterns: List[str]
    volatility: float
    adaptation_rate: float
    focus_areas: List[str]

@dataclass
class CulturalProfile:
    """Perfil cultural do antagonista"""
    name: str
    values: List[str]
    practices: List[str]
    historical_context: Dict[str, str]

class HybridAntagonist:
    """Antagonista que combina múltiplos perfis"""
    def __init__(self, name: str, primary_behavior: BehaviorProfile, 
                 secondary_behavior: BehaviorProfile, cultural_profile: CulturalProfile):
        self.name = name
        self.primary_behavior = primary_behavior
        self.secondary_behavior = secondary_behavior
        self.cultural_profile = cultural_profile
        self.adaptation_state = {
            'behavior_volatility': 0.0,
            'cultural_resonance': 0.0,
            'integration_level': 0.0
        }
        self.emergent_patterns = []
        
    def adapt_to_context(self, context: Dict) -> Dict:
        """Adapta comportamento ao contexto"""
        # Calcula volatilidade comportamental
        behavior_volatility = (
            self.primary_behavior.volatility * 0.7 +
            self.secondary_behavior.volatility * 0.3
        )
        
        # Calcula ressonância cultural
        cultural_resonance = self._calculate_cultural_resonance(context)
        
        # Atualiza estado de adaptação
        self.adaptation_state.update({
            'behavior_volatility': behavior_volatility,
            'cultural_resonance': cultural_resonance,
            'integration_level': (behavior_volatility + cultural_resonance) / 2
        })
        
        # Gera padrões emergentes
        self._generate_emergent_patterns()
        
        return self.adaptation_state
    
    def _calculate_cultural_resonance(self, context: Dict) -> float:
        """Calcula ressonância cultural com o contexto"""
        context_values = set(context.get('cultural_values', []))
        antagonist_values = set(self.cultural_profile.values)
        
        # Calcula sobreposição de valores
        value_overlap = len(context_values.intersection(antagonist_values))
        total_values = len(context_values.union(antagonist_values))
        
        return value_overlap / total_values if total_values > 0 else 0.0
    
    def _generate_emergent_patterns(self):
        """Gera padrões comportamentais emergentes"""
        primary_patterns = set(self.primary_behavior.patterns)
        secondary_patterns = set(self.secondary_behavior.patterns)
        
        # Combina padrões dos dois perfis
        self.emergent_patterns = [
            {
                'name': f"hybrid_{p1}_{p2}",
                'base_patterns': [p1, p2],
                'adaptation_rate': self.adaptation_state['integration_level'],
                'evolution_enabled': True
            }
            for p1 in primary_patterns
            for p2 in secondary_patterns
        ]
    
    def get_tactical_response(self, situation: Dict) -> Dict:
        """Gera resposta tática para uma situação"""
        # Analisa prioridades comportamentais
        primary_focus = self._select_behavioral_focus(situation)
        
        # Seleciona padrões relevantes
        relevant_patterns = self._select_relevant_patterns(situation)
        
        return {
            'focus': primary_focus,
            'patterns': relevant_patterns,
            'adaptation_state': self.adaptation_state,
            'cultural_context': {
                'values': self.cultural_profile.values,
                'practices': self.cultural_profile.practices
            }
        }
    
    def _select_behavioral_focus(self, situation: Dict) -> str:
        """Seleciona foco comportamental baseado na situação"""
        primary_areas = set(self.primary_behavior.focus_areas)
        secondary_areas = set(self.secondary_behavior.focus_areas)
        situation_focus = situation.get('focus_areas', [])
        
        # Prioriza áreas que se sobrepõem com a situação
        overlapping_primary = primary_areas.intersection(situation_focus)
        overlapping_secondary = secondary_areas.intersection(situation_focus)
        
        if overlapping_primary:
            return list(overlapping_primary)[0]
        elif overlapping_secondary:
            return list(overlapping_secondary)[0]
        else:
            return self.primary_behavior.focus_areas[0]
    
    def _select_relevant_patterns(self, situation: Dict) -> List[Dict]:
        """Seleciona padrões relevantes para a situação"""
        situation_type = situation.get('type', '')
        situation_intensity = situation.get('intensity', 0.5)
        
        relevant = []
        for pattern in self.emergent_patterns:
            # Verifica relevância dos padrões base
            base_relevance = any(
                base in situation_type
                for base in pattern['base_patterns']
            )
            
            if base_relevance:
                pattern_copy = pattern.copy()
                pattern_copy['intensity'] = situation_intensity
                pattern_copy['relevance_score'] = (
                    pattern['adaptation_rate'] * situation_intensity
                )
                relevant.append(pattern_copy)
        
        # Ordena por relevância
        return sorted(relevant, key=lambda x: x['relevance_score'], reverse=True)
    
    def save_state(self, filepath: str):
        """Salva estado do antagonista"""
        state = {
            'name': self.name,
            'primary_behavior': {
                'name': self.primary_behavior.name,
                'patterns': self.primary_behavior.patterns,
                'volatility': self.primary_behavior.volatility,
                'adaptation_rate': self.primary_behavior.adaptation_rate,
                'focus_areas': self.primary_behavior.focus_areas
            },
            'secondary_behavior': {
                'name': self.secondary_behavior.name,
                'patterns': self.secondary_behavior.patterns,
                'volatility': self.secondary_behavior.volatility,
                'adaptation_rate': self.secondary_behavior.adaptation_rate,
                'focus_areas': self.secondary_behavior.focus_areas
            },
            'cultural_profile': {
                'name': self.cultural_profile.name,
                'values': self.cultural_profile.values,
                'practices': self.cultural_profile.practices,
                'historical_context': self.cultural_profile.historical_context
            },
            'adaptation_state': self.adaptation_state,
            'emergent_patterns': self.emergent_patterns
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(state, f, sort_keys=False)
    
    @classmethod
    def load_state(cls, filepath: str) -> 'HybridAntagonist':
        """Carrega estado do antagonista"""
        with open(filepath) as f:
            state = yaml.safe_load(f)
        
        primary_behavior = BehaviorProfile(
            name=state['primary_behavior']['name'],
            patterns=state['primary_behavior']['patterns'],
            volatility=state['primary_behavior']['volatility'],
            adaptation_rate=state['primary_behavior']['adaptation_rate'],
            focus_areas=state['primary_behavior']['focus_areas']
        )
        
        secondary_behavior = BehaviorProfile(
            name=state['secondary_behavior']['name'],
            patterns=state['secondary_behavior']['patterns'],
            volatility=state['secondary_behavior']['volatility'],
            adaptation_rate=state['secondary_behavior']['adaptation_rate'],
            focus_areas=state['secondary_behavior']['focus_areas']
        )
        
        cultural_profile = CulturalProfile(
            name=state['cultural_profile']['name'],
            values=state['cultural_profile']['values'],
            practices=state['cultural_profile']['practices'],
            historical_context=state['cultural_profile']['historical_context']
        )
        
        antagonist = cls(
            name=state['name'],
            primary_behavior=primary_behavior,
            secondary_behavior=secondary_behavior,
            cultural_profile=cultural_profile
        )
        
        antagonist.adaptation_state = state['adaptation_state']
        antagonist.emergent_patterns = state['emergent_patterns']
        
        return antagonist
