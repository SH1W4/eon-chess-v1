#!/usr/bin/env python3

"""
Cultura Samurai
Implementação detalhada da cultura samurai e seus elementos
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import yaml
import json

@dataclass
class SamuraiPractice:
    """Prática cultural samurai"""
    name: str
    description: str
    significance: float
    required_resources: List[str]
    cultural_impact: Dict[str, float]

@dataclass
class SamuraiValue:
    """Valor cultural samurai"""
    name: str
    description: str
    importance: float
    manifestations: List[str]
    related_values: List[str]

class SamuraiCulture:
    """Implementação da cultura samurai"""
    def __init__(self):
        self.name = "Samurai"
        self.era = "Feudal Japan"
        self.core_values = self._initialize_values()
        self.cultural_practices = self._initialize_practices()
        self.belief_system = self._initialize_beliefs()
        self.social_structure = self._initialize_social_structure()
        
    def _initialize_values(self) -> Dict[str, SamuraiValue]:
        """Inicializa valores culturais samurai"""
        return {
            "bushido": SamuraiValue(
                name="bushido",
                description="Código de conduta e honra do guerreiro",
                importance=0.95,
                manifestations=[
                    "loyalty_service",
                    "honor_maintenance",
                    "duty_fulfillment"
                ],
                related_values=["honor", "loyalty", "duty"]
            ),
            "honor": SamuraiValue(
                name="honor",
                description="Integridade pessoal e reputação",
                importance=0.9,
                manifestations=[
                    "word_keeping",
                    "name_protection",
                    "respectful_conduct"
                ],
                related_values=["bushido", "integrity", "respect"]
            ),
            "discipline": SamuraiValue(
                name="discipline",
                description="Autocontrole e dedicação ao aperfeiçoamento",
                importance=0.85,
                manifestations=[
                    "martial_training",
                    "mind_control",
                    "daily_practice"
                ],
                related_values=["perfection", "control", "dedication"]
            ),
            "loyalty": SamuraiValue(
                name="loyalty",
                description="Devoção absoluta ao senhor e clã",
                importance=0.8,
                manifestations=[
                    "lord_service",
                    "clan_protection",
                    "sacrifice_willingness"
                ],
                related_values=["duty", "devotion", "sacrifice"]
            )
        }
        
    def _initialize_practices(self) -> Dict[str, SamuraiPractice]:
        """Inicializa práticas culturais samurai"""
        return {
            "martial_arts": SamuraiPractice(
                name="martial_arts",
                description="Treinamento nas artes marciais",
                significance=0.9,
                required_resources=[
                    "weapons",
                    "training_ground",
                    "instructor"
                ],
                cultural_impact={
                    "combat_skill": 0.9,
                    "discipline": 0.8,
                    "spiritual_growth": 0.7
                }
            ),
            "meditation": SamuraiPractice(
                name="meditation",
                description="Prática de meditação e cultivo mental",
                significance=0.85,
                required_resources=[
                    "quiet_space",
                    "meditation_knowledge",
                    "time"
                ],
                cultural_impact={
                    "mental_strength": 0.9,
                    "spiritual_awareness": 0.8,
                    "self_control": 0.7
                }
            ),
            "ceremonial_arts": SamuraiPractice(
                name="ceremonial_arts",
                description="Práticas artísticas e cerimoniais",
                significance=0.8,
                required_resources=[
                    "ceremonial_items",
                    "artistic_materials",
                    "cultural_knowledge"
                ],
                cultural_impact={
                    "cultural_refinement": 0.8,
                    "spiritual_harmony": 0.7,
                    "artistic_expression": 0.9
                }
            )
        }
        
    def _initialize_beliefs(self) -> Dict[str, Dict]:
        """Inicializa sistema de crenças samurai"""
        return {
            "philosophy": {
                "schools": [
                    "Zen Buddhism",
                    "Confucianism",
                    "Bushido"
                ],
                "principles": [
                    "Righteousness",
                    "Courage",
                    "Benevolence",
                    "Respect",
                    "Sincerity",
                    "Honor",
                    "Loyalty",
                    "Self-Control"
                ],
                "significance": 0.95
            },
            "spirituality": {
                "practices": [
                    "zazen",
                    "tea_ceremony",
                    "calligraphy",
                    "flower_arrangement"
                ],
                "significance": 0.9
            },
            "death": {
                "concepts": [
                    "honorable_death",
                    "seppuku",
                    "afterlife",
                    "ancestor_worship"
                ],
                "significance": 0.85
            },
            "rituals": {
                "types": [
                    "sword_ceremony",
                    "tea_ceremony",
                    "coming_of_age",
                    "death_ritual"
                ],
                "significance": 0.8
            }
        }
        
    def _initialize_social_structure(self) -> Dict[str, Dict]:
        """Inicializa estrutura social samurai"""
        return {
            "classes": {
                "daimyo": {
                    "status": "feudal_lord",
                    "influence": 0.95,
                    "responsibilities": [
                        "domain_governance",
                        "warfare",
                        "vassal_management"
                    ]
                },
                "samurai": {
                    "status": "warrior",
                    "influence": 0.85,
                    "responsibilities": [
                        "military_service",
                        "administration",
                        "cultural_refinement"
                    ]
                },
                "hatamoto": {
                    "status": "high_ranking_samurai",
                    "influence": 0.8,
                    "responsibilities": [
                        "direct_service",
                        "special_duties",
                        "command"
                    ]
                },
                "gokenin": {
                    "status": "low_ranking_samurai",
                    "influence": 0.7,
                    "responsibilities": [
                        "local_duties",
                        "support_roles",
                        "basic_service"
                    ]
                }
            },
            "institutions": {
                "castle": {
                    "type": "administrative_center",
                    "importance": 0.9,
                    "functions": [
                        "military_command",
                        "administration",
                        "ceremonial_events"
                    ]
                },
                "dojo": {
                    "type": "training_center",
                    "importance": 0.85,
                    "functions": [
                        "martial_training",
                        "character_development",
                        "tradition_preservation"
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
                f"Seguir {primary_value['name']}, demonstrando "
                f"{primary_value['description']}"
            )
            
        if primary_practice:
            recommendations.append(
                f"Cultivar {primary_practice['name']}, focando em "
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
            'philosophical': [],
            'spiritual': [],
            'mortality': [],
            'ritual': []
        }
        
        # Verifica referências filosóficas
        for school in self.belief_system['philosophy']['schools']:
            if school.lower() in situation.get('description', '').lower():
                relevant_beliefs['philosophical'].append(school)
                
        # Verifica referências espirituais
        for practice in self.belief_system['spirituality']['practices']:
            if practice.lower() in situation.get('description', '').lower():
                relevant_beliefs['spiritual'].append(practice)
                
        # Verifica referências sobre morte
        for concept in self.belief_system['death']['concepts']:
            if concept.lower() in situation.get('description', '').lower():
                relevant_beliefs['mortality'].append(concept)
                
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
