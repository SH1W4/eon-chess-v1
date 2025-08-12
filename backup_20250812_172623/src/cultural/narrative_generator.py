#!/usr/bin/env python3

"""
Gerador de Narrativas Dinâmicas
Cria e gerencia narrativas adaptativas baseadas em contexto cultural
"""

import logging
import yaml
from pathlib import Path
import json
import datetime
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='narrative_generator.log'
)

class NarrativeGenerator:
    def __init__(self):
        self.data_dir = Path('../cultural_data')
        self.load_narrative_templates()
        
    def load_narrative_templates(self):
        """Carrega templates narrativos"""
        templates_path = self.data_dir / "narratives" / "templates"
        self.templates = {
            "cultural_conflict": {
                "themes": ["poder", "território", "identidade", "adaptação"],
                "arcs": ["confronto", "negociação", "assimilação", "síntese"],
                "resolutions": ["vitória", "acordo", "transformação", "transcendência"]
            },
            "hero_journey": {
                "themes": ["crescimento", "desafio", "sacrifício", "revelação"],
                "arcs": ["chamado", "iniciação", "provação", "retorno"],
                "resolutions": ["conquista", "sabedoria", "transformação", "legado"]
            },
            "empire_building": {
                "themes": ["expansão", "administração", "conflito", "legado"],
                "arcs": ["fundação", "crescimento", "desafio", "estabelecimento"],
                "resolutions": ["domínio", "equilíbrio", "queda", "renascimento"]
            }
        }
        
    def generate_narrative(self, context):
        """Gera narrativa baseada no contexto"""
        template = self.select_template(context)
        narrative = self.construct_narrative(template, context)
        self.add_dynamic_elements(narrative, context)
        return narrative
        
    def select_template(self, context):
        """Seleciona template apropriado"""
        cultural_focus = context.get("cultural_focus", "")
        if "conflito" in cultural_focus or "guerra" in cultural_focus:
            return self.templates["cultural_conflict"]
        elif "jornada" in cultural_focus or "desenvolvimento" in cultural_focus:
            return self.templates["hero_journey"]
        else:
            return self.templates["empire_building"]
        
    def construct_narrative(self, template, context):
        """Constrói narrativa básica"""
        theme = random.choice(template["themes"])
        arc = random.choice(template["arcs"])
        resolution = random.choice(template["resolutions"])
        
        narrative = {
            "theme": theme,
            "arc": arc,
            "resolution": resolution,
            "context": context,
            "elements": self.generate_narrative_elements(theme, arc),
            "adaptations": []
        }
        
        return narrative
        
    def generate_narrative_elements(self, theme, arc):
        """Gera elementos narrativos"""
        return {
            "characters": self.generate_characters(theme),
            "plot_points": self.generate_plot_points(arc),
            "settings": self.generate_settings(theme),
            "conflicts": self.generate_conflicts(theme)
        }
        
    def generate_characters(self, theme):
        """Gera personagens baseados no tema"""
        characters = []
        archetypes = {
            "poder": ["líder", "conselheiro", "guerreiro", "diplomata"],
            "território": ["explorador", "defensor", "estrategista", "pioneiro"],
            "identidade": ["mentor", "aprendiz", "tradicionalista", "inovador"],
            "adaptação": ["adaptador", "conservador", "mediador", "catalisador"]
        }
        
        selected_archetypes = archetypes.get(theme, archetypes["poder"])
        for archetype in selected_archetypes:
            character = {
                "archetype": archetype,
                "motivation": self.generate_motivation(archetype),
                "traits": self.generate_traits(archetype),
                "development_path": self.generate_development_path(archetype)
            }
            characters.append(character)
            
        return characters
        
    def generate_motivation(self, archetype):
        """Gera motivação para personagem"""
        motivations = {
            "líder": ["unificação", "poder", "legado", "ordem"],
            "conselheiro": ["sabedoria", "equilíbrio", "progresso", "harmonia"],
            "guerreiro": ["honra", "proteção", "conquista", "glória"],
            "diplomata": ["paz", "aliança", "entendimento", "cooperação"]
        }
        return random.choice(motivations.get(archetype, ["sobrevivência", "crescimento"]))
        
    def generate_traits(self, archetype):
        """Gera características do personagem"""
        trait_sets = {
            "líder": ["carismático", "decisivo", "visionário"],
            "conselheiro": ["sábio", "ponderado", "observador"],
            "guerreiro": ["corajoso", "disciplinado", "leal"],
            "diplomata": ["persuasivo", "empático", "paciente"]
        }
        return random.sample(trait_sets.get(archetype, ["adaptável", "resiliente"]), 2)
        
    def generate_development_path(self, archetype):
        """Gera caminho de desenvolvimento"""
        paths = {
            "líder": ["consolidação", "expansão", "transcendência"],
            "conselheiro": ["iluminação", "influência", "legado"],
            "guerreiro": ["maestria", "honra", "liderança"],
            "diplomata": ["mediação", "aliança", "harmonia"]
        }
        return random.choice(paths.get(archetype, ["crescimento", "adaptação"]))
        
    def generate_plot_points(self, arc):
        """Gera pontos de trama"""
        plot_points = []
        arc_structures = {
            "confronto": ["tensão inicial", "escalada", "confronto", "resultado"],
            "negociação": ["divergência", "diálogo", "compromisso", "acordo"],
            "assimilação": ["encontro", "conflito", "adaptação", "integração"],
            "síntese": ["separação", "exploração", "combinação", "unificação"]
        }
        
        for point in arc_structures.get(arc, ["início", "meio", "fim"]):
            plot_point = {
                "name": point,
                "description": self.generate_plot_description(point),
                "requirements": self.generate_plot_requirements(point),
                "consequences": self.generate_plot_consequences(point)
            }
            plot_points.append(plot_point)
            
        return plot_points
        
    def generate_plot_description(self, point):
        """Gera descrição do ponto de trama"""
        descriptions = {
            "tensão inicial": "Surgimento de conflito entre culturas",
            "escalada": "Intensificação das diferenças e disputas",
            "confronto": "Momento decisivo de enfrentamento",
            "resultado": "Consequências e transformações do conflito"
        }
        return descriptions.get(point, "Desenvolvimento da história")
        
    def generate_plot_requirements(self, point):
        """Gera requisitos para ponto de trama"""
        return {
            "cultural_state": random.random(),
            "conflict_level": random.random(),
            "adaptation_rate": random.random()
        }
        
    def generate_plot_consequences(self, point):
        """Gera consequências do ponto de trama"""
        return {
            "cultural_impact": random.random(),
            "relationship_change": random.random(),
            "system_adaptation": random.random()
        }
        
    def generate_settings(self, theme):
        """Gera cenários"""
        settings = []
        setting_types = {
            "poder": ["palácio", "campo de batalha", "sala do conselho"],
            "território": ["fronteira", "assentamento", "rota comercial"],
            "identidade": ["templo", "vila", "local sagrado"],
            "adaptação": ["encruzilhada", "novo território", "zona de contato"]
        }
        
        for setting_type in setting_types.get(theme, ["local neutro"]):
            setting = {
                "type": setting_type,
                "description": self.generate_setting_description(setting_type),
                "cultural_elements": self.generate_cultural_elements(setting_type),
                "significance": self.generate_setting_significance(setting_type)
            }
            settings.append(setting)
            
        return settings
        
    def generate_setting_description(self, setting_type):
        """Gera descrição do cenário"""
        descriptions = {
            "palácio": "Centro de poder e decisão",
            "campo de batalha": "Local de confronto e provação",
            "sala do conselho": "Espaço de negociação e estratégia"
        }
        return descriptions.get(setting_type, "Ambiente significativo")
        
    def generate_cultural_elements(self, setting_type):
        """Gera elementos culturais do cenário"""
        return {
            "arquitetura": random.random(),
            "simbolismo": random.random(),
            "atmosfera": random.random()
        }
        
    def generate_setting_significance(self, setting_type):
        """Gera significância do cenário"""
        return {
            "cultural_weight": random.random(),
            "narrative_importance": random.random(),
            "symbolic_value": random.random()
        }
        
    def generate_conflicts(self, theme):
        """Gera conflitos"""
        conflicts = []
        conflict_types = {
            "poder": ["sucessão", "dominação", "influência"],
            "território": ["fronteira", "recursos", "colonização"],
            "identidade": ["tradição", "mudança", "assimilação"],
            "adaptação": ["resistência", "integração", "transformação"]
        }
        
        for conflict_type in conflict_types.get(theme, ["genérico"]):
            conflict = {
                "type": conflict_type,
                "description": self.generate_conflict_description(conflict_type),
                "stakes": self.generate_conflict_stakes(conflict_type),
                "resolution_paths": self.generate_resolution_paths(conflict_type)
            }
            conflicts.append(conflict)
            
        return conflicts
        
    def generate_conflict_description(self, conflict_type):
        """Gera descrição do conflito"""
        descriptions = {
            "sucessão": "Disputa pelo poder e liderança",
            "dominação": "Luta por controle e influência",
            "influência": "Competição por prestígio e autoridade"
        }
        return descriptions.get(conflict_type, "Situação de conflito")
        
    def generate_conflict_stakes(self, conflict_type):
        """Gera apostas do conflito"""
        return {
            "cultural_impact": random.random(),
            "power_shift": random.random(),
            "relationship_change": random.random()
        }
        
    def generate_resolution_paths(self, conflict_type):
        """Gera caminhos de resolução"""
        return {
            "negotiation": random.random(),
            "conflict": random.random(),
            "integration": random.random()
        }
        
    def add_dynamic_elements(self, narrative, context):
        """Adiciona elementos dinâmicos à narrativa"""
        narrative["dynamic_elements"] = {
            "adaptation_points": self.generate_adaptation_points(narrative, context),
            "cultural_influences": self.generate_cultural_influences(narrative, context),
            "emergence_opportunities": self.generate_emergence_opportunities(narrative, context)
        }
        
    def generate_adaptation_points(self, narrative, context):
        """Gera pontos de adaptação"""
        return [
            {
                "trigger": "cultural_threshold",
                "condition": {"type": "cultural_tension", "threshold": 0.7},
                "adaptation": {"type": "narrative_shift", "intensity": 0.5}
            },
            {
                "trigger": "character_development",
                "condition": {"type": "character_growth", "threshold": 0.6},
                "adaptation": {"type": "arc_adjustment", "intensity": 0.4}
            }
        ]
        
    def generate_cultural_influences(self, narrative, context):
        """Gera influências culturais"""
        return {
            "primary_culture": {
                "influence_level": random.random(),
                "adaptation_rate": random.random()
            },
            "secondary_cultures": [
                {
                    "culture": "adjacent",
                    "influence_level": random.random(),
                    "interaction_type": "cooperative"
                }
            ]
        }
        
    def generate_emergence_opportunities(self, narrative, context):
        """Gera oportunidades de emergência"""
        return [
            {
                "type": "cultural_synthesis",
                "probability": random.random(),
                "impact": random.random()
            },
            {
                "type": "character_transformation",
                "probability": random.random(),
                "impact": random.random()
            }
        ]

def main():
    generator = NarrativeGenerator()
    
    # Exemplo de contexto
    context = {
        "cultural_focus": "conflito territorial",
        "current_state": {
            "tension_level": 0.7,
            "cultural_diversity": 0.8,
            "adaptation_rate": 0.6
        }
    }
    
    # Gerar narrativa
    narrative = generator.generate_narrative(context)
    
    print("\n=== Narrativa Gerada ===")
    print(json.dumps(narrative, indent=2))

if __name__ == "__main__":
    main()
