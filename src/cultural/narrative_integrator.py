#!/usr/bin/env python3

"""
Integrador Narrativo
Melhora a integração entre narrativas e elementos culturais
"""

import logging
import yaml
from pathlib import Path
import json
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='narrative_integrator.log'
)

class NarrativeIntegrator:
    def __init__(self):
        self.data_dir = Path('../cultural_data')
        self.cultures_dir = self.data_dir / "configurations" / "themes"
        self.narratives_dir = self.data_dir / "narratives" / "dynamic"
        
    def integrate_narratives(self, narratives, cultures):
        """Integra narrativas com culturas"""
        integrated = {
            "timestamp": datetime.datetime.now().isoformat(),
            "integration_map": self.create_integration_map(narratives, cultures),
            "cultural_bridges": self.create_cultural_bridges(narratives, cultures),
            "narrative_adaptations": self.create_narrative_adaptations(narratives, cultures)
        }
        
        self.apply_integration(integrated)
        return integrated
        
    def create_integration_map(self, narratives, cultures):
        """Cria mapa de integração"""
        integration_map = {}
        
        for narrative in narratives:
            narrative_points = self.extract_narrative_points(narrative)
            cultural_elements = self.extract_cultural_elements(cultures)
            
            integration_map[narrative["name"]] = {
                "cultural_connections": self.map_cultural_connections(narrative_points, cultural_elements),
                "thematic_alignments": self.map_thematic_alignments(narrative_points, cultural_elements),
                "values": self.map_value_resonance(narrative_points, cultural_elements)
            }
            
        return integration_map
            
    def map_value_resonance(self, narrative_points, cultural_elements):
        """Mapeia ressonância de valores"""
        resonance = {}
        
        for culture_name, elements in cultural_elements.items():
            resonance[culture_name] = {
                "direct_matches": self.calculate_direct_value_matches(
                    narrative_points["elements"].get("values", []),
                    elements["values"]
                ),
                "thematic_alignment": self.calculate_theme_value_alignment(
                    narrative_points["themes"],
                    elements["values"]
                ),
                "character_values": self.calculate_character_value_resonance(
                    narrative_points["elements"].get("characters", []),
                    elements["values"]
                )
            }
            
        return resonance
        
    def calculate_direct_value_matches(self, narrative_values, cultural_values):
        """Calcula correspondências diretas de valores"""
        if not narrative_values or not cultural_values:
            return 0.0
            
        matches = sum(
            1 for value in narrative_values
            if any(cv.lower() == value.lower() for cv in cultural_values)
        )
        return matches / len(narrative_values)
        
    def calculate_theme_value_alignment(self, themes, cultural_values):
        """Calcula alinhamento entre temas e valores"""
        if not themes or not cultural_values:
            return 0.0
            
        alignments = sum(
            1 for theme in themes
            if any(value.lower() in theme.lower() for value in cultural_values)
        )
        return alignments / len(themes)
        
    def calculate_character_value_resonance(self, characters, cultural_values):
        """Calcula ressonância entre valores de personagens e culturais"""
        if not characters or not cultural_values:
            return 0.0
            
        resonances = []
        for character in characters:
            traits = character.get("traits", [])
            if not traits:
                continue
                
            matches = sum(
                1 for trait in traits
                if any(value.lower() in trait.lower() for value in cultural_values)
            )
            resonances.append(matches / len(traits))
            
        return sum(resonances) / len(resonances) if resonances else 0.0
        
    def extract_narrative_points(self, narrative):
        """Extrai pontos narrativos relevantes"""
        return {
            "themes": narrative.get("theme", []),
            "arcs": narrative.get("arc", []),
            "elements": narrative.get("elements", {}),
            "dynamic_elements": narrative.get("dynamic_elements", {})
        }
        
    def extract_cultural_elements(self, cultures):
        """Extrai elementos culturais relevantes"""
        cultural_elements = {}
        
        for culture in cultures:
            cultural_elements[culture["name"]] = {
                "values": culture.get("attributes", {}).get("cultural_values", []),
                "practices": culture.get("narrative_elements", {}).get("cultural_practices", []),
                "stories": culture.get("narrative_elements", {}).get("key_stories", [])
            }
            
        return cultural_elements
        
    def map_cultural_connections(self, narrative_points, cultural_elements):
        """Mapeia conexões culturais"""
        connections = {}
        
        for culture_name, elements in cultural_elements.items():
            connections[culture_name] = {
                "value_overlap": self.calculate_overlap(narrative_points["themes"], elements["values"]),
                "practice_alignment": self.calculate_overlap(
                    narrative_points["elements"].get("settings", []),
                    elements["practices"]
                ),
                "story_resonance": self.calculate_overlap(
                    narrative_points["elements"].get("plot_points", []),
                    elements["stories"]
                )
            }
            
        return connections
        
    def map_thematic_alignments(self, narrative_points, cultural_elements):
        """Mapeia alinhamentos temáticos"""
        alignments = {}
        
        for culture_name, elements in cultural_elements.items():
            alignments[culture_name] = {
                "theme_harmony": self.calculate_theme_harmony(narrative_points["themes"], elements["values"]),
                "arc_compatibility": self.calculate_arc_compatibility(narrative_points["arcs"], elements["stories"]),
                "element_synergy": self.calculate_element_synergy(narrative_points["elements"], elements)
            }
            
        return alignments
        
    def calculate_overlap(self, set_a, set_b):
        """Calcula sobreposição entre conjuntos"""
        set_a = set(str(x).lower() for x in set_a)
        set_b = set(str(x).lower() for x in set_b)
        
        intersection = set_a.intersection(set_b)
        union = set_a.union(set_b)
        
        return len(intersection) / len(union) if union else 0
        
    def calculate_theme_harmony(self, themes, values):
        """Calcula harmonia temática"""
        return {
            "direct_match": self.calculate_overlap(themes, values),
            "semantic_alignment": self.calculate_semantic_similarity(themes, values),
            "value_reinforcement": self.calculate_value_reinforcement(themes, values)
        }
        
    def calculate_semantic_similarity(self, set_a, set_b):
        """Calcula similaridade semântica"""
        # Simplificado para demonstração
        return sum(any(b in a.lower() for b in set_b) for a in set_a) / len(set_a) if set_a else 0
        
    def calculate_value_reinforcement(self, themes, values):
        """Calcula reforço de valores"""
        # Simplificado para demonstração
        return sum(any(v in t.lower() for v in values) for t in themes) / len(themes) if themes else 0
        
    def calculate_arc_compatibility(self, arcs, stories):
        """Calcula compatibilidade de arcos narrativos"""
        return {
            "structural_alignment": self.calculate_overlap(arcs, stories),
            "narrative_flow": self.calculate_narrative_flow(arcs, stories),
            "story_integration": self.calculate_story_integration(arcs, stories)
        }
        
    def calculate_narrative_flow(self, arcs, stories):
        """Calcula fluxo narrativo"""
        # Simplificado para demonstração
        return len(set(arcs).intersection(stories)) / len(arcs) if arcs else 0
        
    def calculate_story_integration(self, arcs, stories):
        """Calcula integração de histórias"""
        # Simplificado para demonstração
        return sum(any(s in a.lower() for s in stories) for a in arcs) / len(arcs) if arcs else 0
        
    def calculate_element_synergy(self, narrative_elements, cultural_elements):
        """Calcula sinergia entre elementos"""
        return {
            "character_alignment": self.calculate_character_alignment(
                narrative_elements.get("characters", []),
                cultural_elements
            ),
            "setting_resonance": self.calculate_setting_resonance(
                narrative_elements.get("settings", []),
                cultural_elements
            ),
            "conflict_harmony": self.calculate_conflict_harmony(
                narrative_elements.get("conflicts", []),
                cultural_elements
            )
        }
        
    def calculate_character_alignment(self, characters, cultural_elements):
        """Calcula alinhamento de personagens"""
        if not characters:
            return 0.0
            
        alignments = []
        for character in characters:
            cultural_match = sum(
                any(trait.lower() in str(v).lower() for v in cultural_elements["values"])
                for trait in character.get("traits", [])
            )
            alignments.append(cultural_match / len(character.get("traits", [])) if character.get("traits") else 0)
            
        return sum(alignments) / len(alignments) if alignments else 0
        
    def calculate_setting_resonance(self, settings, cultural_elements):
        """Calcula ressonância de cenários"""
        if not settings:
            return 0.0
            
        resonances = []
        for setting in settings:
            cultural_match = sum(
                1 for practice in cultural_elements["practices"]
                if practice.lower() in setting["description"].lower()
            )
            resonances.append(cultural_match / len(cultural_elements["practices"]) if cultural_elements["practices"] else 0)
            
        return sum(resonances) / len(resonances) if resonances else 0
        
    def calculate_conflict_harmony(self, conflicts, cultural_elements):
        """Calcula harmonia de conflitos"""
        if not conflicts:
            return 0.0
            
        harmonies = []
        for conflict in conflicts:
            cultural_match = sum(
                any(story.lower() in conflict["description"].lower() for story in cultural_elements["stories"])
            )
            harmonies.append(cultural_match / len(cultural_elements["stories"]) if cultural_elements["stories"] else 0)
            
        return sum(harmonies) / len(harmonies) if harmonies else 0
        
    def create_cultural_bridges(self, narratives, cultures):
        """Cria pontes culturais"""
        bridges = {}
        
        for narrative in narratives:
            bridges[narrative["name"]] = {
                "cultural_adaptations": self.create_cultural_adaptations(narrative, cultures),
                "value_translations": self.create_value_translations(narrative, cultures),
                "practice_integrations": self.create_practice_integrations(narrative, cultures)
            }
            
        return bridges
        
    def create_cultural_adaptations(self, narrative, cultures):
        """Cria adaptações culturais"""
        adaptations = {}
        
        for culture in cultures:
            adaptations[culture["name"]] = {
                "narrative_elements": self.adapt_narrative_elements(narrative, culture),
                "character_modifications": self.adapt_characters(narrative, culture),
                "setting_adjustments": self.adapt_settings(narrative, culture)
            }
            
        return adaptations
        
    def adapt_narrative_elements(self, narrative, culture):
        """Adapta elementos narrativos"""
        return {
            "theme_adaptation": self.adapt_theme(narrative["theme"], culture),
            "arc_adaptation": self.adapt_arc(narrative["arc"], culture),
            "resolution_adaptation": self.adapt_resolution(narrative.get("resolution"), culture)
        }
        
    def adapt_theme(self, theme, culture):
        """Adapta tema para cultura específica"""
        cultural_values = culture.get("attributes", {}).get("cultural_values", [])
        return {
            "original_theme": theme,
            "cultural_interpretation": self.find_cultural_interpretation(theme, cultural_values),
            "adaptation_level": self.calculate_adaptation_level(theme, cultural_values)
        }

    def adapt_arc(self, arc, culture):
        """Adapta arco narrativo para cultura específica"""
        cultural_stories = culture.get("narrative_elements", {}).get("key_stories", [])
        return {
            "original_arc": arc,
            "cultural_interpretation": self.find_cultural_interpretation(arc, cultural_stories),
            "adaptation_level": self.calculate_adaptation_level(arc, cultural_stories)
        }

    def adapt_resolution(self, resolution, culture):
        """Adapta resolução para cultura específica"""
        if not resolution:
            return None
        cultural_values = culture.get("attributes", {}).get("cultural_values", [])
        return {
            "original_resolution": resolution,
            "cultural_interpretation": self.find_cultural_interpretation(resolution, cultural_values),
            "adaptation_level": self.calculate_adaptation_level(resolution, cultural_values)
        }

    def adapt_characters(self, narrative, culture):
        """Adapta personagens para cultura específica"""
        return [{
            "original_character": character,
            "cultural_traits": self.adapt_character_traits(character.get("traits", []), culture),
            "cultural_role": self.find_cultural_role(character.get("archetype"), culture)
        } for character in narrative.get("elements", {}).get("characters", [])]

    def adapt_character_traits(self, traits, culture):
        """Adapta traços de personagem para cultura específica"""
        cultural_values = culture.get("attributes", {}).get("cultural_values", [])
        return [{
            "original_trait": trait,
            "cultural_equivalent": self.find_cultural_interpretation(trait, cultural_values)
        } for trait in traits]

    def find_cultural_role(self, archetype, culture):
        """Encontra papel cultural equivalente"""
        cultural_roles = culture.get("narrative_elements", {}).get("character_roles", [])
        matching_roles = [role for role in cultural_roles if archetype.lower() in role.lower()]
        return matching_roles[0] if matching_roles else archetype

    def adapt_settings(self, narrative, culture):
        """Adapta cenários para cultura específica"""
        return [{
            "original_setting": setting,
            "cultural_context": self.adapt_setting_context(setting, culture),
            "cultural_significance": self.find_cultural_significance(setting.get("type"), culture)
        } for setting in narrative.get("elements", {}).get("settings", [])]

    def adapt_setting_context(self, setting, culture):
        """Adapta contexto do cenário para cultura específica"""
        cultural_practices = culture.get("narrative_elements", {}).get("cultural_practices", [])
        return [{
            "practice": practice,
            "relevance": self.calculate_practice_relevance(setting.get("description", ""), practice)
        } for practice in cultural_practices]

    def find_cultural_significance(self, setting_type, culture):
        """Encontra significado cultural do cenário"""
        cultural_places = culture.get("narrative_elements", {}).get("significant_places", [])
        matching_places = [place for place in cultural_places if setting_type.lower() in place.lower()]
        return matching_places[0] if matching_places else setting_type

    def calculate_practice_relevance(self, setting_description, practice):
        """Calcula relevância de prática cultural para o cenário"""
        if practice.lower() in setting_description.lower():
            return 1.0
        return 0.0
        
    def find_cultural_interpretation(self, theme, cultural_values):
        """Encontra interpretação cultural"""
        # Simplificado para demonstração
        matching_values = [v for v in cultural_values if any(t.lower() in v.lower() for t in [theme])]
        return matching_values[0] if matching_values else theme
        
    def calculate_adaptation_level(self, theme, cultural_values):
        """Calcula nível de adaptação"""
        # Simplificado para demonstração
        return sum(any(t.lower() in v.lower() for t in [theme]) for v in cultural_values) / len(cultural_values) if cultural_values else 0
        
    def create_value_translations(self, narrative, cultures):
        """Cria traduções de valores"""
        translations = {}
        
        for culture in cultures:
            translations[culture["name"]] = {
                "value_mappings": self.map_cultural_values(narrative, culture),
                "concept_bridges": self.create_concept_bridges(narrative, culture),
                "meaning_adaptations": self.create_meaning_adaptations(narrative, culture)
            }
            
        return translations

    def map_cultural_values(self, narrative, culture):
        """Mapeia valores narrativos para culturais"""
        values = []
        cultural_values = culture.get("attributes", {}).get("cultural_values", [])
        
        # Valores dos personagens
        for character in narrative.get("elements", {}).get("characters", []):
            for trait in character.get("traits", []):
                values.append({
                    "narrative_value": trait,
                    "cultural_value": self.find_cultural_value(trait, cultural_values),
                    "context": "character_trait"
                })
                
        # Valores temáticos
        if isinstance(narrative.get("theme"), str):
            theme_values = [narrative["theme"]]
        else:
            theme_values = narrative.get("theme", [])
            
        for theme in theme_values:
            values.append({
                "narrative_value": theme,
                "cultural_value": self.find_cultural_value(theme, cultural_values),
                "context": "theme"
            })
            
        return values
            
    def find_cultural_value(self, value, cultural_values):
        """Encontra valor cultural correspondente"""
        matches = [cv for cv in cultural_values if value.lower() in cv.lower()]
        return matches[0] if matches else value

    def create_concept_bridges(self, narrative, culture):
        """Cria pontes conceituais"""
        bridges = []
        cultural_concepts = culture.get("narrative_elements", {}).get("key_concepts", [])
        
        # Conceitos de personagens
        for character in narrative.get("elements", {}).get("characters", []):
            archetype = character.get("archetype")
            if archetype:
                bridges.append({
                    "narrative_concept": archetype,
                    "cultural_concept": self.find_cultural_concept(archetype, cultural_concepts),
                    "context": "character_archetype"
                })
                
        # Conceitos de cenário
        for setting in narrative.get("elements", {}).get("settings", []):
            setting_type = setting.get("type")
            if setting_type:
                bridges.append({
                    "narrative_concept": setting_type,
                    "cultural_concept": self.find_cultural_concept(setting_type, cultural_concepts),
                    "context": "setting_type"
                })
                
        return bridges
            
    def find_cultural_concept(self, concept, cultural_concepts):
        """Encontra conceito cultural correspondente"""
        matches = [cc for cc in cultural_concepts if concept.lower() in cc.lower()]
        return matches[0] if matches else concept

    def create_meaning_adaptations(self, narrative, culture):
        """Cria adaptações de significado"""
        adaptations = []
        cultural_meanings = culture.get("narrative_elements", {}).get("cultural_meanings", [])
        
        # Significados de personagens
        for character in narrative.get("elements", {}).get("characters", []):
            archetype = character.get("archetype")
            if archetype:
                adaptations.append({
                    "original_meaning": f"character_archetype_{archetype}",
                    "cultural_meaning": self.find_cultural_meaning(archetype, cultural_meanings),
                    "context": "character"
                })
                
        # Significados de cenário
        for setting in narrative.get("elements", {}).get("settings", []):
            setting_type = setting.get("type")
            if setting_type:
                adaptations.append({
                    "original_meaning": f"setting_type_{setting_type}",
                    "cultural_meaning": self.find_cultural_meaning(setting_type, cultural_meanings),
                    "context": "setting"
                })
                
        return adaptations
            
    def find_cultural_meaning(self, element, cultural_meanings):
        """Encontra significado cultural correspondente"""
        matches = [cm for cm in cultural_meanings if element.lower() in cm.get("element", "").lower()]
        return matches[0].get("meaning") if matches else f"cultural_meaning_of_{element}"
        
    def create_practice_integrations(self, narrative, cultures):
        """Cria integrações de práticas"""
        integrations = {}
        
        for culture in cultures:
            integrations[culture["name"]] = {
                "ritual_adaptations": self.adapt_rituals(narrative, culture),
                "custom_incorporations": self.incorporate_customs(narrative, culture),
                "tradition_bridges": self.create_tradition_bridges(narrative, culture)
            }
            
        return integrations

    def adapt_rituals(self, narrative, culture):
        """Adapta rituais para contexto cultural"""
        adaptations = []
        cultural_rituals = culture.get("narrative_elements", {}).get("cultural_rituals", [])
        
        for setting in narrative.get("elements", {}).get("settings", []):
            setting_type = setting.get("type")
            if setting_type:
                matching_rituals = self.find_matching_rituals(setting_type, cultural_rituals)
                if matching_rituals:
                    adaptations.append({
                        "setting": setting_type,
                        "rituals": [{
                            "ritual": ritual,
                            "relevance": self.calculate_ritual_relevance(setting, ritual)
                        } for ritual in matching_rituals]
                    })
                    
        return adaptations

    def find_matching_rituals(self, setting_type, cultural_rituals):
        """Encontra rituais correspondentes ao cenário"""
        return [ritual for ritual in cultural_rituals 
                if setting_type.lower() in ritual.get("settings", [])]

    def calculate_ritual_relevance(self, setting, ritual):
        """Calcula relevância do ritual para o cenário"""
        setting_keywords = set(setting.get("description", "").lower().split())
        ritual_keywords = set(ritual.get("description", "").lower().split())
        
        intersection = len(setting_keywords.intersection(ritual_keywords))
        return intersection / len(ritual_keywords) if ritual_keywords else 0

    def incorporate_customs(self, narrative, culture):
        """Incorpora costumes culturais"""
        incorporations = []
        cultural_customs = culture.get("narrative_elements", {}).get("cultural_customs", [])
        
        for character in narrative.get("elements", {}).get("characters", []):
            archetype = character.get("archetype")
            if archetype:
                matching_customs = self.find_matching_customs(archetype, cultural_customs)
                if matching_customs:
                    incorporations.append({
                        "character_archetype": archetype,
                        "customs": [{
                            "custom": custom,
                            "relevance": self.calculate_custom_relevance(character, custom)
                        } for custom in matching_customs]
                    })
                    
        return incorporations

    def find_matching_customs(self, archetype, cultural_customs):
        """Encontra costumes correspondentes ao arquetipo"""
        return [custom for custom in cultural_customs 
                if archetype.lower() in custom.get("archetypes", [])]

    def calculate_custom_relevance(self, character, custom):
        """Calcula relevância do costume para o personagem"""
        character_traits = set(trait.lower() for trait in character.get("traits", []))
        custom_traits = set(trait.lower() for trait in custom.get("traits", []))
        
        intersection = len(character_traits.intersection(custom_traits))
        return intersection / len(custom_traits) if custom_traits else 0

    def create_tradition_bridges(self, narrative, culture):
        """Cria pontes entre tradições"""
        bridges = []
        cultural_traditions = culture.get("narrative_elements", {}).get("cultural_traditions", [])
        
        # Tradições em cenários
        for setting in narrative.get("elements", {}).get("settings", []):
            setting_type = setting.get("type")
            if setting_type:
                matching_traditions = self.find_matching_traditions(setting_type, cultural_traditions)
                if matching_traditions:
                    bridges.append({
                        "setting_type": setting_type,
                        "traditions": [{
                            "tradition": tradition,
                            "relevance": self.calculate_tradition_relevance(setting, tradition)
                        } for tradition in matching_traditions]
                    })
                    
        return bridges

    def find_matching_traditions(self, setting_type, cultural_traditions):
        """Encontra tradições correspondentes ao cenário"""
        return [tradition for tradition in cultural_traditions 
                if setting_type.lower() in tradition.get("settings", [])]

    def calculate_tradition_relevance(self, setting, tradition):
        """Calcula relevância da tradição para o cenário"""
        setting_elements = set(setting.get("description", "").lower().split())
        tradition_elements = set(tradition.get("description", "").lower().split())
        
        intersection = len(setting_elements.intersection(tradition_elements))
        return intersection / len(tradition_elements) if tradition_elements else 0
        
    def create_narrative_adaptations(self, narratives, cultures):
        """Cria adaptações narrativas"""
        adaptations = {}
        
        for narrative in narratives:
            adaptations[narrative["name"]] = {
                "structural_adaptations": self.adapt_narrative_structure(narrative, cultures),
                "thematic_modifications": self.modify_themes(narrative, cultures),
                "character_evolutions": self.evolve_characters(narrative, cultures)
            }
            
        return adaptations

    def adapt_narrative_structure(self, narrative, cultures):
        """Adapta estrutura narrativa"""
        adaptations = {}
        
        for culture in cultures:
            cultural_structures = culture.get("narrative_elements", {}).get("narrative_structures", [])
            matching_structures = self.find_matching_structures(narrative, cultural_structures)
            
            if matching_structures:
                adaptations[culture["name"]] = [{
                    "structure": structure,
                    "compatibility": self.calculate_structure_compatibility(narrative, structure)
                } for structure in matching_structures]
                
        return adaptations

    def find_matching_structures(self, narrative, cultural_structures):
        """Encontra estruturas narrativas correspondentes"""
        arc = narrative.get("arc", "")
        return [structure for structure in cultural_structures 
                if arc.lower() in structure.get("arcs", [])]

    def calculate_structure_compatibility(self, narrative, structure):
        """Calcula compatibilidade com estrutura narrativa"""
        arc_match = narrative.get("arc", "").lower() in structure.get("arcs", [])
        theme_match = any(theme.lower() in structure.get("themes", []) 
                         for theme in ([narrative.get("theme")] if isinstance(narrative.get("theme"), str) 
                                      else narrative.get("theme", [])))
        
        return (arc_match + theme_match) / 2

    def modify_themes(self, narrative, cultures):
        """Modifica temas para contextos culturais"""
        modifications = {}
        
        for culture in cultures:
            cultural_themes = culture.get("narrative_elements", {}).get("cultural_themes", [])
            narrative_theme = narrative.get("theme")
            
            if narrative_theme:
                if isinstance(narrative_theme, str):
                    theme_list = [narrative_theme]
                else:
                    theme_list = narrative_theme
                    
                modifications[culture["name"]] = [{
                    "original_theme": theme,
                    "cultural_interpretation": self.find_cultural_theme(theme, cultural_themes),
                    "resonance": self.calculate_theme_resonance(theme, cultural_themes)
                } for theme in theme_list]
                
        return modifications

    def find_cultural_theme(self, theme, cultural_themes):
        """Encontra tema cultural correspondente"""
        matches = [ct for ct in cultural_themes if theme.lower() in ct.get("variations", [])]
        return matches[0].get("theme") if matches else theme

    def calculate_theme_resonance(self, theme, cultural_themes):
        """Calcula ressonância do tema no contexto cultural"""
        for cultural_theme in cultural_themes:
            if theme.lower() in cultural_theme.get("variations", []):
                return cultural_theme.get("resonance", 0.5)
        return 0.0

    def evolve_characters(self, narrative, cultures):
        """Evolui personagens para contextos culturais"""
        evolutions = {}
        
        for culture in cultures:
            cultural_archetypes = culture.get("narrative_elements", {}).get("character_archetypes", [])
            
            evolutions[culture["name"]] = [{
                "original_character": character,
                "cultural_evolution": self.evolve_character(character, cultural_archetypes),
                "evolution_metrics": self.calculate_evolution_metrics(character, cultural_archetypes)
            } for character in narrative.get("elements", {}).get("characters", [])]
            
        return evolutions

    def evolve_character(self, character, cultural_archetypes):
        """Evolui personagem para contexto cultural"""
        archetype = character.get("archetype")
        if not archetype:
            return character
            
        matching_archetype = next((ca for ca in cultural_archetypes 
                                  if archetype.lower() in ca.get("variants", [])), None)
                                  
        if not matching_archetype:
            return character
            
        return {
            "archetype": matching_archetype.get("archetype", archetype),
            "traits": self.evolve_traits(character.get("traits", []), matching_archetype),
            "motivations": self.evolve_motivations(character, matching_archetype)
        }

    def evolve_traits(self, traits, cultural_archetype):
        """Evolui traços para contexto cultural"""
        cultural_traits = cultural_archetype.get("traits", [])
        evolved_traits = []
        
        for trait in traits:
            matching_trait = next((ct for ct in cultural_traits 
                                  if trait.lower() in ct.get("variations", [])), None)
            evolved_traits.append(matching_trait.get("trait", trait) if matching_trait else trait)
            
        return evolved_traits

    def evolve_motivations(self, character, cultural_archetype):
        """Evolui motivações para contexto cultural"""
        cultural_motivations = cultural_archetype.get("motivations", [])
        original_motivation = character.get("motivation")
        
        if not original_motivation:
            return []
            
        matching_motivation = next((cm for cm in cultural_motivations 
                                   if original_motivation.lower() in cm.get("variations", [])), None)
                                   
        return [matching_motivation.get("motivation", original_motivation)] if matching_motivation else [original_motivation]

    def calculate_evolution_metrics(self, character, cultural_archetypes):
        """Calcula métricas de evolução do personagem"""
        archetype = character.get("archetype")
        if not archetype:
            return {
                "archetype_resonance": 0.0,
                "trait_alignment": 0.0,
                "motivation_harmony": 0.0
            }
            
        matching_archetype = next((ca for ca in cultural_archetypes 
                                  if archetype.lower() in ca.get("variants", [])), None)
                                  
        if not matching_archetype:
            return {
                "archetype_resonance": 0.0,
                "trait_alignment": 0.0,
                "motivation_harmony": 0.0
            }
            
        return {
            "archetype_resonance": self.calculate_archetype_resonance(character, matching_archetype),
            "trait_alignment": self.calculate_trait_alignment(character, matching_archetype),
            "motivation_harmony": self.calculate_motivation_harmony(character, matching_archetype)
        }

    def calculate_archetype_resonance(self, character, cultural_archetype):
        """Calcula ressonância do arquétipo"""
        archetype = character.get("archetype", "").lower()
        cultural_variants = [v.lower() for v in cultural_archetype.get("variants", [])]
        
        if archetype in cultural_variants:
            return 1.0
        return 0.0

    def calculate_trait_alignment(self, character, cultural_archetype):
        """Calcula alinhamento de traços"""
        character_traits = set(trait.lower() for trait in character.get("traits", []))
        cultural_traits = set(trait.get("trait", "").lower() 
                            for trait in cultural_archetype.get("traits", []))
        
        if not character_traits or not cultural_traits:
            return 0.0
            
        intersection = len(character_traits.intersection(cultural_traits))
        return intersection / len(character_traits)

    def calculate_motivation_harmony(self, character, cultural_archetype):
        """Calcula harmonia de motivações"""
        motivation = character.get("motivation", "").lower()
        cultural_motivations = [m.get("motivation", "").lower() 
                              for m in cultural_archetype.get("motivations", [])]
        
        if not motivation or not cultural_motivations:
            return 0.0
            
        return 1.0 if motivation in cultural_motivations else 0.0
        
    def apply_integration(self, integrated):
        """Aplica integração"""
        output_file = self.data_dir / "integration" / f"narrative_integration_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(integrated, f, indent=2)
            
        logging.info(f"Integração narrativa salva em {output_file}")

def main():
    integrator = NarrativeIntegrator()
    
    # Exemplo de narrativas e culturas
    narratives = [
        {
            "name": "conflito_territorial",
            "theme": "território",
            "arc": "confronto",
            "elements": {
                "characters": [
                    {
                        "archetype": "guerreiro",
                        "traits": ["corajoso", "leal"]
                    }
                ],
                "settings": [
                    {
                        "type": "fronteira",
                        "description": "Local de disputa territorial"
                    }
                ]
            }
        }
    ]
    
    cultures = [
        {
            "name": "viking",
            "attributes": {
                "cultural_values": ["honra", "bravura", "exploração"]
            },
            "narrative_elements": {
                "cultural_practices": ["raid", "navegação"],
                "key_stories": ["conquista", "exploração"]
            }
        }
    ]
    
    # Realizar integração
    integrated = integrator.integrate_narratives(narratives, cultures)
    
    print("\n=== Integração Narrativa ===")
    print(json.dumps(integrated, indent=2))

if __name__ == "__main__":
    main()
