#!/usr/bin/env python3

"""
Cultura Maia
Implementação detalhada da cultura maia e seus elementos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml
import json

@dataclass
class MayanPractice:
    """Prática cultural maia"""
    name: str
    description: str
    significance: float
    required_resources: List[str]
    cultural_impact: Dict[str, float]

@dataclass
class MayanValue:
    """Valor cultural maia"""
    name: str
    description: str
    importance: float
    manifestations: List[str]
    related_values: List[str]

class MayanCulture:
    """Implementação da cultura maia"""
    def __init__(self):
        self.name = "Mayan"
        self.era = "Classic Period"
        self.core_values = self._initialize_values()
        self.cultural_practices = self._initialize_practices()
        self.belief_system = self._initialize_beliefs()
        self.social_structure = self._initialize_social_structure()
        
    def _initialize_values(self) -> Dict[str, MayanValue]:
        """Inicializa valores culturais maias"""
        return {
            "knowledge": MayanValue(
                name="knowledge",
                description="Busca pelo conhecimento e sabedoria ancestral",
                importance=0.95,
                manifestations=[
                    "astronomical_observation",
                    "calendar_keeping",
                    "hieroglyphic_writing"
                ],
                related_values=["wisdom", "tradition", "education"]
            ),
            "harmony": MayanValue(
                name="harmony",
                description="Equilíbrio entre mundo natural e espiritual",
                importance=0.9,
                manifestations=[
                    "ritual_ceremonies",
                    "nature_respect",
                    "spiritual_balance"
                ],
                related_values=["balance", "spirituality", "nature"]
            ),
            "legacy": MayanValue(
                name="legacy",
                description="Preservação e continuidade cultural",
                importance=0.85,
                manifestations=[
                    "monument_building",
                    "knowledge_transmission",
                    "artistic_expression"
                ],
                related_values=["tradition", "heritage", "art"]
            ),
            "sacrifice": MayanValue(
                name="sacrifice",
                description="Dedicação aos deuses e bem comum",
                importance=0.8,
                manifestations=[
                    "ritual_offerings",
                    "personal_sacrifice",
                    "communal_service"
                ],
                related_values=["devotion", "commitment", "community"]
            )
        }
        
    def _initialize_practices(self) -> Dict[str, MayanPractice]:
        """Inicializa práticas culturais maias"""
        return {
            "astronomy": MayanPractice(
                name="astronomy",
                description="Observação e registro dos corpos celestes",
                significance=0.9,
                required_resources=[
                    "observatories",
                    "mathematical_knowledge",
                    "writing_materials"
                ],
                cultural_impact={
                    "knowledge": 0.9,
                    "spiritual_connection": 0.8,
                    "technological_advancement": 0.7
                }
            ),
            "agriculture": MayanPractice(
                name="agriculture",
                description="Cultivo sustentável e ritual",
                significance=0.85,
                required_resources=[
                    "land",
                    "tools",
                    "ritual_knowledge"
                ],
                cultural_impact={
                    "sustainability": 0.8,
                    "community_cohesion": 0.7,
                    "spiritual_harmony": 0.9
                }
            ),
            "architecture": MayanPractice(
                name="architecture",
                description="Construção de templos e cidades",
                significance=0.8,
                required_resources=[
                    "stone",
                    "labor_force",
                    "architectural_knowledge"
                ],
                cultural_impact={
                    "cultural_legacy": 0.9,
                    "spiritual_expression": 0.8,
                    "social_organization": 0.7
                }
            )
        }
        
    def _initialize_beliefs(self) -> Dict[str, Dict]:
        """Inicializa sistema de crenças maia"""
        return {
            "cosmology": {
                "layers": [
                    "Upperworld",
                    "Middleworld",
                    "Underworld"
                ],
                "sacred_directions": [
                    "East",
                    "North",
                    "West",
                    "South",
                    "Center"
                ],
                "significance": 0.95
            },
            "deities": {
                "major": [
                    "Itzamna",
                    "Kukulcan",
                    "Chaak",
                    "Ix Chel",
                    "Kinich Ahau"
                ],
                "significance": 0.9
            },
            "time": {
                "calendars": [
                    "Tzolkin",
                    "Haab",
                    "Long Count"
                ],
                "cycles": [
                    "Creation",
                    "Destruction",
                    "Renewal"
                ],
                "significance": 0.85
            },
            "rituals": {
                "types": [
                    "blood_letting",
                    "ball_game",
                    "harvest_ceremony",
                    "new_year_ritual"
                ],
                "significance": 0.8
            }
        }
        
    def _initialize_social_structure(self) -> Dict[str, Dict]:
        """Inicializa estrutura social maia"""
        return {
            "classes": {
                "rulers": {
                    "status": "divine_kings",
                    "influence": 0.95,
                    "responsibilities": [
                        "governance",
                        "ritual_leadership",
                        "warfare"
                    ]
                },
                "nobles": {
                    "status": "elite",
                    "influence": 0.8,
                    "responsibilities": [
                        "administration",
                        "religious_duties",
                        "knowledge_keeping"
                    ]
                },
                "artisans": {
                    "status": "skilled_workers",
                    "influence": 0.6,
                    "responsibilities": [
                        "crafting",
                        "building",
                        "artistic_creation"
                    ]
                },
                "commoners": {
                    "status": "workers",
                    "influence": 0.4,
                    "responsibilities": [
                        "farming",
                        "labor",
                        "trade"
                    ]
                }
            },
            "institutions": {
                "temples": {
                    "type": "religious_center",
                    "importance": 0.9,
                    "functions": [
                        "ritual_performance",
                        "knowledge_preservation",
                        "astronomical_observation"
                    ]
                },
                "markets": {
                    "type": "economic_center",
                    "importance": 0.7,
                    "functions": [
                        "trade",
                        "resource_distribution",
                        "social_interaction"
                    ]
                }
            }
        }
    
    def get_cultural_response(self, situation: Dict) -> Dict:
        """Gera resposta cultural para uma situação"""
        response = {
            'values_activated': self._identify_relevant_values(situation),
            'practices_suggested': self._identify_relevant_practices(situation),
            'cultural_guidance': self._generate_cultural_guidance(situation)
        }
        
        return response
    
    def _identify_relevant_values(self, situation: Dict) -> List[Dict]:
        """Identifica valores relevantes para a situação"""
        relevant_values = []
        
        for value_name, value in self.core_values.items():
            relevance = 0.0
            
            # Verifica palavras-chave na situação
            if any(word in situation.get('description', '').lower() 
                  for word in value.manifestations):
                relevance += 0.3
            
            # Verifica contexto
            if situation.get('context', '') in value.manifestations:
                relevance += 0.3
                
            # Verifica alinhamento com valores relacionados
            if any(related in situation.get('values', [])
                  for related in value.related_values):
                relevance += 0.4
                
            if relevance > 0:
                relevant_values.append({
                    'name': value_name,
                    'description': value.description,
                    'relevance': relevance,
                    'importance': value.importance
                })
                
        return sorted(
            relevant_values,
            key=lambda x: (x['relevance'], x['importance']),
            reverse=True
        )
    
    def _identify_relevant_practices(self, situation: Dict) -> List[Dict]:
        """Identifica práticas relevantes para a situação"""
        relevant_practices = []
        
        for practice_name, practice in self.cultural_practices.items():
            relevance = 0.0
            
            # Verifica recursos disponíveis
            available_resources = set(situation.get('available_resources', []))
            required_resources = set(practice.required_resources)
            resource_overlap = len(available_resources.intersection(required_resources))
            
            if resource_overlap > 0:
                relevance += 0.3 * (resource_overlap / len(required_resources))
            
            # Verifica impacto cultural desejado
            desired_impacts = situation.get('desired_impacts', {})
            for impact, value in practice.cultural_impact.items():
                if impact in desired_impacts:
                    relevance += 0.3 * value
            
            # Verifica significância prática
            relevance += 0.4 * practice.significance
            
            if relevance > 0:
                relevant_practices.append({
                    'name': practice_name,
                    'description': practice.description,
                    'relevance': relevance,
                    'significance': practice.significance,
                    'required_resources': practice.required_resources
                })
                
        return sorted(
            relevant_practices,
            key=lambda x: (x['relevance'], x['significance']),
            reverse=True
        )
    
    def _generate_cultural_guidance(self, situation: Dict) -> Dict:
        """Gera orientação cultural para a situação"""
        values = self._identify_relevant_values(situation)
        practices = self._identify_relevant_practices(situation)
        
        # Determina prioridades
        primary_value = values[0] if values else None
        primary_practice = practices[0] if practices else None
        
        # Gera recomendações
        recommendations = []
        if primary_value:
            recommendations.append(
                f"Buscar {primary_value['name']}, manifestando "
                f"{primary_value['description']}"
            )
            
        if primary_practice:
            recommendations.append(
                f"Praticar {primary_practice['name']}, focando em "
                f"{primary_practice['description']}"
            )
            
        # Considera estrutura social
        social_guidance = []
        for class_name, class_info in self.social_structure['classes'].items():
            if any(resp in situation.get('responsibilities', [])
                  for resp in class_info['responsibilities']):
                social_guidance.append({
                    'class': class_name,
                    'status': class_info['status'],
                    'expected_behavior': class_info['responsibilities']
                })
        
        return {
            'primary_value': primary_value['name'] if primary_value else None,
            'primary_practice': primary_practice['name'] if primary_practice else None,
            'recommendations': recommendations,
            'social_guidance': social_guidance,
            'belief_relevance': self._identify_relevant_beliefs(situation)
        }
    
    def _identify_relevant_beliefs(self, situation: Dict) -> Dict:
        """Identifica crenças relevantes para a situação"""
        relevant_beliefs = {
            'cosmological': [],
            'divine': [],
            'temporal': [],
            'ritual': []
        }
        
        # Verifica referências cosmológicas
        for layer in self.belief_system['cosmology']['layers']:
            if layer.lower() in situation.get('description', '').lower():
                relevant_beliefs['cosmological'].append(layer)
                
        # Verifica referências divinas
        for deity in self.belief_system['deities']['major']:
            if deity.lower() in situation.get('description', '').lower():
                relevant_beliefs['divine'].append(deity)
                
        # Verifica referências temporais
        for calendar in self.belief_system['time']['calendars']:
            if calendar.lower() in situation.get('description', '').lower():
                relevant_beliefs['temporal'].append(calendar)
                
        # Verifica contexto ritual
        for ritual in self.belief_system['rituals']['types']:
            if ritual in situation.get('context', ''):
                relevant_beliefs['ritual'].append(ritual)
                
        return relevant_beliefs
    
    def save_state(self, filepath: str):
        """Salva estado da cultura"""
        state = {
            'name': self.name,
            'era': self.era,
            'core_values': {
                name: {
                    'name': value.name,
                    'description': value.description,
                    'importance': value.importance,
                    'manifestations': value.manifestations,
                    'related_values': value.related_values
                }
                for name, value in self.core_values.items()
            },
            'cultural_practices': {
                name: {
                    'name': practice.name,
                    'description': practice.description,
                    'significance': practice.significance,
                    'required_resources': practice.required_resources,
                    'cultural_impact': practice.cultural_impact
                }
                for name, practice in self.cultural_practices.items()
            },
            'belief_system': self.belief_system,
            'social_structure': self.social_structure
        }
        
        with open(filepath, 'w') as f:
            yaml.dump(state, f, sort_keys=False)
