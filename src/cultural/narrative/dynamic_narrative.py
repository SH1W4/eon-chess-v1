#!/usr/bin/env python3

"""
Sistema de Narrativas Dinâmicas
Gera e gerencia narrativas que se adaptam ao contexto e evolução do jogo
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import yaml
import random

logging.basicConfig(level=logging.INFO)

@dataclass
class NarrativeElement:
    """Elemento narrativo base"""
    name: str
    type: str
    weight: float
    cultural_value: float
    adaptability: float

@dataclass
class NarrativeArc:
    """Arco narrativo que estrutura a história"""
    name: str
    stages: List[str]
    intensity_curve: List[float]
    cultural_elements: List[NarrativeElement]
    resolution_paths: List[str]

@dataclass
class CulturalContext:
    """Contexto cultural que influencia a narrativa"""
    culture_name: str
    values: List[str]
    practices: List[str]
    historical_elements: Dict[str, str]
    current_state: Dict[str, float]

class DynamicNarrative:
    """Gerador e gerenciador de narrativas dinâmicas"""
    def __init__(self):
        self.arcs = {}
        self.elements = {}
        self.current_state = {
            'intensity': 0.0,
            'cultural_resonance': 0.0,
            'adaptation_level': 0.0
        }
        self.evolution_history = []
        
    def load_narrative_templates(self, templates_path: str):
        """Carrega templates narrativos"""
        with open(templates_path) as f:
            data = yaml.safe_load(f)
            
        # Carrega arcos narrativos
        for arc_data in data.get('narrative_arcs', []):
            arc = NarrativeArc(
                name=arc_data['name'],
                stages=arc_data['stages'],
                intensity_curve=arc_data['intensity_curve'],
                cultural_elements=[
                    NarrativeElement(**element)
                    for element in arc_data['cultural_elements']
                ],
                resolution_paths=arc_data['resolution_paths']
            )
            self.arcs[arc.name] = arc
            
        # Carrega elementos narrativos
        for elem_data in data.get('narrative_elements', []):
            element = NarrativeElement(**elem_data)
            self.elements[element.name] = element
    
    def generate_narrative(self, context: CulturalContext) -> Dict:
        """Gera narrativa baseada no contexto"""
        # Seleciona arco narrativo apropriado
        selected_arc = self._select_narrative_arc(context)
        
        # Adapta elementos ao contexto
        adapted_elements = self._adapt_elements(
            selected_arc.cultural_elements,
            context
        )
        
        # Gera estrutura narrativa
        narrative = {
            'arc': selected_arc.name,
            'stages': self._generate_stages(selected_arc, context),
            'elements': adapted_elements,
            'state': {
                'current_stage': 0,
                'intensity': self._calculate_intensity(context),
                'cultural_resonance': self._calculate_resonance(context),
                'possible_paths': self._identify_paths(context)
            }
        }
        
        return narrative
    
    def evolve_narrative(self, narrative: Dict, context: CulturalContext,
                        events: List[Dict]) -> Dict:
        """Evolui narrativa baseada em eventos e contexto"""
        # Atualiza estado
        current_stage = narrative['state']['current_stage']
        arc = self.arcs[narrative['arc']]
        
        # Analisa eventos
        event_impact = self._analyze_events(events, context)
        
        # Ajusta intensidade
        new_intensity = self._adjust_intensity(
            narrative['state']['intensity'],
            event_impact,
            arc.intensity_curve[current_stage]
        )
        
        # Adapta elementos
        adapted_elements = self._adapt_elements(
            [self.elements[e['name']] for e in narrative['elements']],
            context
        )
        
        # Atualiza caminhos possíveis
        possible_paths = self._update_paths(
            narrative['state']['possible_paths'],
            event_impact,
            context
        )
        
        # Evolui estado
        evolved_state = {
            'current_stage': self._advance_stage(current_stage, event_impact),
            'intensity': new_intensity,
            'cultural_resonance': self._calculate_resonance(context),
            'possible_paths': possible_paths
        }
        
        # Registra evolução
        self.evolution_history.append({
            'from_state': narrative['state'],
            'to_state': evolved_state,
            'event_impact': event_impact,
            'context_state': context.current_state
        })
        
        return {
            'arc': narrative['arc'],
            'stages': self._generate_stages(arc, context),
            'elements': adapted_elements,
            'state': evolved_state
        }
    
    def _select_narrative_arc(self, context: CulturalContext) -> NarrativeArc:
        """Seleciona arco narrativo apropriado"""
        scored_arcs = []
        for arc in self.arcs.values():
            # Calcula alinhamento cultural
            cultural_alignment = self._calculate_cultural_alignment(
                arc.cultural_elements,
                context
            )
            
            # Calcula adequação ao estado atual
            state_fitness = self._calculate_state_fitness(
                arc.intensity_curve,
                context.current_state
            )
            
            score = (cultural_alignment * 0.7) + (state_fitness * 0.3)
            scored_arcs.append((arc, score))
        
        # Seleciona melhor arco
        return max(scored_arcs, key=lambda x: x[1])[0]
    
    def _adapt_elements(self, elements: List[NarrativeElement],
                       context: CulturalContext) -> List[Dict]:
        """Adapta elementos ao contexto"""
        adapted = []
        for element in elements:
            # Calcula relevância cultural
            cultural_relevance = self._calculate_cultural_relevance(
                element,
                context
            )
            
            # Adapta peso baseado no contexto
            adapted_weight = element.weight * (
                0.7 + (cultural_relevance * 0.3)
            )
            
            adapted.append({
                'name': element.name,
                'type': element.type,
                'weight': adapted_weight,
                'cultural_value': cultural_relevance,
                'adaptability': element.adaptability
            })
        
        return adapted
    
    def _generate_stages(self, arc: NarrativeArc,
                        context: CulturalContext) -> List[Dict]:
        """Gera estágios da narrativa"""
        stages = []
        for i, stage in enumerate(arc.stages):
            # Calcula intensidade do estágio
            intensity = arc.intensity_curve[i]
            
            # Adapta ao contexto cultural
            adapted_intensity = intensity * (
                0.8 + (self._calculate_resonance(context) * 0.2)
            )
            
            stages.append({
                'name': stage,
                'intensity': adapted_intensity,
                'cultural_elements': [
                    e.name for e in arc.cultural_elements
                    if e.weight > 0.5
                ]
            })
        
        return stages
    
    def _calculate_intensity(self, context: CulturalContext) -> float:
        """Calcula intensidade narrativa"""
        base_intensity = sum(
            value for value in context.current_state.values()
        ) / len(context.current_state)
        
        cultural_factor = len(
            [v for v in context.values if v in context.current_state]
        ) / len(context.values)
        
        return base_intensity * (0.8 + (cultural_factor * 0.2))
    
    def _calculate_resonance(self, context: CulturalContext) -> float:
        """Calcula ressonância cultural"""
        active_values = set(
            k for k, v in context.current_state.items()
            if v > 0.5
        )
        cultural_values = set(context.values)
        
        overlap = len(active_values.intersection(cultural_values))
        total = len(active_values.union(cultural_values))
        
        return overlap / total if total > 0 else 0.0
    
    def _identify_paths(self, context: CulturalContext) -> List[str]:
        """Identifica caminhos narrativos possíveis"""
        # Filtra caminhos baseado no contexto
        active_values = set(
            k for k, v in context.current_state.items()
            if v > 0.6
        )
        
        paths = []
        for arc in self.arcs.values():
            if any(
                value in active_values
                for element in arc.cultural_elements
                for value in context.values
            ):
                paths.extend(arc.resolution_paths)
        
        return list(set(paths))  # Remove duplicatas
    
    def _analyze_events(self, events: List[Dict],
                       context: CulturalContext) -> Dict:
        """Analisa impacto dos eventos"""
        impact = {
            'intensity_change': 0.0,
            'cultural_shift': 0.0,
            'path_influence': []
        }
        
        for event in events:
            # Analisa mudança de intensidade
            impact['intensity_change'] += event.get('intensity', 0) * 0.1
            
            # Analisa mudança cultural
            cultural_values = set(event.get('cultural_values', []))
            context_values = set(context.values)
            overlap = len(cultural_values.intersection(context_values))
            
            impact['cultural_shift'] += (overlap / len(context_values)) * 0.1
            
            # Registra influência no caminho
            if event.get('path_suggestion'):
                impact['path_influence'].append(event['path_suggestion'])
        
        return impact
    
    def _adjust_intensity(self, current: float, impact: Dict,
                        target: float) -> float:
        """Ajusta intensidade narrativa"""
        # Calcula nova intensidade
        new_intensity = current + impact['intensity_change']
        
        # Suaviza em direção ao alvo
        return current + (
            (target - current) * 0.2 +  # Tendência ao alvo
            impact['intensity_change']   # Influência dos eventos
        )
    
    def _advance_stage(self, current: int, impact: Dict) -> int:
        """Avança estágio da narrativa"""
        # Avança se impacto for significativo
        if abs(impact['intensity_change']) > 0.3:
            return min(current + 1, len(self.arcs) - 1)
        return current
    
    def _update_paths(self, current_paths: List[str], impact: Dict,
                     context: CulturalContext) -> List[str]:
        """Atualiza caminhos possíveis"""
        # Adiciona novos caminhos sugeridos por eventos
        paths = set(current_paths)
        paths.update(impact['path_influence'])
        
        # Filtra baseado no contexto atual
        return [
            path for path in paths
            if self._is_path_viable(path, context)
        ]
    
    def _is_path_viable(self, path: str, context: CulturalContext) -> bool:
        """Verifica se um caminho é viável no contexto atual"""
        # Implementação básica - pode ser expandida
        return any(
            value in path.lower()
            for value in context.values
        )
    
    def _calculate_cultural_alignment(self, elements: List[NarrativeElement],
                                    context: CulturalContext) -> float:
        """Calcula alinhamento cultural dos elementos"""
        alignments = []
        for element in elements:
            # Verifica alinhamento com valores culturais
            value_alignment = sum(
                1 for value in context.values
                if value.lower() in element.name.lower()
            ) / len(context.values)
            
            # Verifica alinhamento com práticas
            practice_alignment = sum(
                1 for practice in context.practices
                if practice.lower() in element.name.lower()
            ) / len(context.practices)
            
            alignments.append((value_alignment + practice_alignment) / 2)
        
        return sum(alignments) / len(alignments) if alignments else 0.0
    
    def _calculate_state_fitness(self, intensity_curve: List[float],
                               current_state: Dict[str, float]) -> float:
        """Calcula adequação ao estado atual"""
        # Calcula intensidade média atual
        current_intensity = sum(
            value for value in current_state.values()
        ) / len(current_state)
        
        # Encontra ponto mais próximo na curva
        differences = [
            abs(intensity - current_intensity)
            for intensity in intensity_curve
        ]
        
        return 1 - (min(differences) / max(intensity_curve))
    
    def _calculate_cultural_relevance(self, element: NarrativeElement,
                                    context: CulturalContext) -> float:
        """Calcula relevância cultural de um elemento"""
        # Verifica alinhamento com valores
        value_relevance = sum(
            1 for value in context.values
            if value.lower() in element.name.lower()
        ) / len(context.values)
        
        # Verifica alinhamento com práticas
        practice_relevance = sum(
            1 for practice in context.practices
            if practice.lower() in element.name.lower()
        ) / len(context.practices)
        
        # Considera estado atual
        state_relevance = sum(
            value for key, value in context.current_state.items()
            if key.lower() in element.name.lower()
        ) / len(context.current_state)
        
        return (
            value_relevance * 0.4 +
            practice_relevance * 0.3 +
            state_relevance * 0.3
        )
