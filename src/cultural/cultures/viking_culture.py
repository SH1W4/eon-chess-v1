#!/usr/bin/env python3

"""
Cultura Viking
Implementação detalhada da cultura nórdica e seus elementos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml
import json

@dataclass
class VikingPractice:
    """Prática cultural viking"""
    name: str
    description: str
    significance: float
    required_resources: List[str]
    cultural_impact: Dict[str, float]

@dataclass
class VikingValue:
    """Valor cultural viking"""
    name: str
    description: str
    importance: float
    manifestations: List[str]
    related_values: List[str]

class VikingCulture:
    """Implementação da cultura viking"""
    def __init__(self):
        self.name = "Viking"
        self.era = "Viking Age"
        self.core_values = self._initialize_values()
        self.cultural_practices = self._initialize_practices()
        self.belief_system = self._initialize_beliefs()
        self.social_structure = self._initialize_social_structure()
        
    def _initialize_values(self) -> Dict[str, VikingValue]:
        """Inicializa valores culturais vikings"""
        return {
            "honor": VikingValue(
                name="honor",
                description="Conceito fundamental de honra pessoal e familiar",
                importance=0.95,
                manifestations=[
                    "cumprimento_palavras",
                    "defesa_reputação",
                    "lealdade_grupo"
                ],
                related_values=["courage", "loyalty", "reputation"]
            ),
            "courage": VikingValue(
                name="courage",
                description="Bravura em batalha e enfrentamento de desafios",
                importance=0.9,
                manifestations=[
                    "prowess_battle",
                    "exploration_unknown",
                    "face_challenges"
                ],
                related_values=["honor", "strength", "glory"]
            ),
            "strength": VikingValue(
                name="strength",
                description="Força física e mental como virtude central",
                importance=0.85,
                manifestations=[
                    "combat_skill",
                    "endurance",
                    "leadership"
                ],
                related_values=["courage", "resilience", "power"]
            ),
            "exploration": VikingValue(
                name="exploration",
                description="Desejo de explorar e descobrir novos territórios",
                importance=0.8,
                manifestations=[
                    "seafaring",
                    "colonization",
                    "trade_routes"
                ],
                related_values=["courage", "ambition", "wisdom"]
            )
        }
        
    def _initialize_practices(self) -> Dict[str, VikingPractice]:
        """Inicializa práticas culturais vikings"""
        return {
            "raiding": VikingPractice(
                name="raiding",
                description="Expedições de saque e exploração",
                significance=0.9,
                required_resources=[
                    "ships",
                    "weapons",
                    "warriors"
                ],
                cultural_impact={
                    "wealth": 0.8,
                    "reputation": 0.9,
                    "territorial_expansion": 0.7
                }
            ),
            "seafaring": VikingPractice(
                name="seafaring",
                description="Navegação e exploração marítima",
                significance=0.85,
                required_resources=[
                    "ships",
                    "navigation_knowledge",
                    "crew"
                ],
                cultural_impact={
                    "exploration": 0.9,
                    "trade": 0.8,
                    "technological_advancement": 0.7
                }
            ),
            "trading": VikingPractice(
                name="trading",
                description="Comércio e estabelecimento de rotas comerciais",
                significance=0.8,
                required_resources=[
                    "goods",
                    "ships",
                    "trading_posts"
                ],
                cultural_impact={
                    "wealth": 0.8,
                    "cultural_exchange": 0.7,
                    "diplomatic_relations": 0.6
                }
            )
        }
        
    def _initialize_beliefs(self) -> Dict[str, Dict]:
        """Inicializa sistema de crenças viking"""
        return {
            "cosmology": {
                "worlds": [
                    "Asgard",
                    "Midgard",
                    "Jotunheim",
                    "Niflheim",
                    "Muspelheim",
                    "Alfheim",
                    "Svartalfheim",
                    "Vanaheim",
                    "Helheim"
                ],
                "significance": 0.9
            },
            "deities": {
                "major": [
                    "Odin",
                    "Thor",
                    "Freya",
                    "Tyr",
                    "Loki"
                ],
                "significance": 0.85
            },
            "afterlife": {
                "realms": [
                    "Valhalla",
                    "Folkvangr",
                    "Helheim"
                ],
                "significance": 0.8
            },
            "rituals": {
                "types": [
                    "blót",
                    "sumbel",
                    "burial_rites"
                ],
                "significance": 0.75
            }
        }
        
    def _initialize_social_structure(self) -> Dict[str, Dict]:
        """Inicializa estrutura social viking"""
        return {
            "classes": {
                "jarls": {
                    "status": "nobility",
                    "influence": 0.9,
                    "responsibilities": [
                        "leadership",
                        "warfare",
                        "justice"
                    ]
                },
                "karls": {
                    "status": "freemen",
                    "influence": 0.7,
                    "responsibilities": [
                        "farming",
                        "crafting",
                        "trading"
                    ]
                },
                "thralls": {
                    "status": "slaves",
                    "influence": 0.3,
                    "responsibilities": [
                        "labor",
                        "service"
                    ]
                }
            },
            "institutions": {
                "thing": {
                    "type": "assembly",
                    "importance": 0.8,
                    "functions": [
                        "law_making",
                        "dispute_resolution",
                        "community_decisions"
                    ]
                },
                "hirð": {
                    "type": "warrior_retinue",
                    "importance": 0.75,
                    "functions": [
                        "military_service",
                        "protection",
                        "raiding"
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
                f"Agir com {primary_value['name']}, demonstrando "
                f"{primary_value['description']}"
            )
            
        if primary_practice:
            recommendations.append(
                f"Empregar {primary_practice['name']}, focando em "
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
            'ritual': []
        }
        
        # Verifica referências cosmológicas
        for world in self.belief_system['cosmology']['worlds']:
            if world.lower() in situation.get('description', '').lower():
                relevant_beliefs['cosmological'].append(world)
                
        # Verifica referências divinas
        for deity in self.belief_system['deities']['major']:
            if deity.lower() in situation.get('description', '').lower():
                relevant_beliefs['divine'].append(deity)
                
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
