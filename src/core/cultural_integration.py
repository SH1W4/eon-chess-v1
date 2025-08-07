from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import asyncio

from .cultural_patterns import CulturalPattern, CulturalContext
from .cultural_validation import CulturalStateValidator
from cultural.cultures import persian_culture, mongol_culture, chinese_culture
from cultural.cultures.viking_culture import VikingCulture
from cultural.cultures.samurai_culture import SamuraiCulture
from cultural.cultures.mayan_culture import MayanCulture

logger = logging.getLogger(__name__)

class CulturalIntegrator:
    """Integrador de dados culturais existentes com o sistema de padrões."""
    
    def __init__(self):
        self.validator = CulturalStateValidator()
        self.cultures = self._initialize_cultures()
        
    def _initialize_cultures(self) -> Dict[str, Any]:
        """Inicializa todas as culturas disponíveis."""
        return {
            "persian": persian_culture,
            "mongol": mongol_culture,
            "chinese": chinese_culture,
            "viking": VikingCulture(),
            "samurai": SamuraiCulture(),
            "mayan": MayanCulture()
        }
        
    async def generate_cultural_patterns(self) -> Dict[str, List[CulturalPattern]]:
        """Gera padrões culturais a partir das culturas existentes."""
        patterns = {}
        
        for culture_name, culture in self.cultures.items():
            patterns[culture_name] = await self._convert_culture_to_patterns(culture)
            
        return patterns
        
    async def _convert_culture_to_patterns(self, culture: Any) -> List[CulturalPattern]:
        """Converte uma cultura em padrões culturais."""
        patterns = []
        now = datetime.now()
        
        # Converte valores culturais em padrões
        if hasattr(culture, 'core_values'):
            for value_name, value in culture.core_values.items():
                pattern = CulturalPattern(
                    name=f"{value_name}_pattern",
                    description=value.description if hasattr(value, 'description') 
                              else "Cultural value pattern",
                    indicators=value.manifestations if hasattr(value, 'manifestations')
                              else [],
                    strength=value.importance if hasattr(value, 'importance')
                             else 0.5,
                    confidence=0.8,  # Valor base de confiança
                    last_update=now,
                    context={
                        "type": "value",
                        "scope": "cultural",
                        "origin": culture.name if hasattr(culture, 'name') else "unknown"
                    }
                )
                patterns.append(pattern)
                
        # Converte práticas culturais em padrões
        if hasattr(culture, 'cultural_practices'):
            for practice_name, practice in culture.cultural_practices.items():
                pattern = CulturalPattern(
                    name=f"{practice_name}_pattern",
                    description=practice.description if hasattr(practice, 'description')
                              else "Cultural practice pattern",
                    indicators=(
                        practice.required_resources if hasattr(practice, 'required_resources')
                        else []
                    ),
                    strength=practice.significance if hasattr(practice, 'significance')
                             else 0.5,
                    confidence=0.7,  # Valor base de confiança
                    last_update=now,
                    context={
                        "type": "practice",
                        "scope": "behavioral",
                        "origin": culture.name if hasattr(culture, 'name') else "unknown"
                    }
                )
                patterns.append(pattern)
                
        # Converte sistema de crenças em padrões
        if hasattr(culture, 'belief_system'):
            for belief_type, belief_data in culture.belief_system.items():
                if isinstance(belief_data, dict):
                    pattern = CulturalPattern(
                        name=f"{belief_type}_belief_pattern",
                        description=f"Belief system pattern for {belief_type}",
                        indicators=self._extract_belief_indicators(belief_data),
                        strength=belief_data.get('significance', 0.5),
                        confidence=0.9,  # Alta confiança para crenças estabelecidas
                        last_update=now,
                        context={
                            "type": "belief",
                            "scope": "spiritual",
                            "origin": culture.name if hasattr(culture, 'name') else "unknown"
                        }
                    )
                    patterns.append(pattern)
                    
        return patterns
        
    def _extract_belief_indicators(self, belief_data: Dict) -> List[str]:
        """Extrai indicadores de dados de crença."""
        indicators = []
        
        # Procura por listas em diferentes níveis
        for value in belief_data.values():
            if isinstance(value, list):
                indicators.extend(value)
            elif isinstance(value, dict):
                for subvalue in value.values():
                    if isinstance(subvalue, list):
                        indicators.extend(subvalue)
                        
        return list(set(indicators))  # Remove duplicatas
        
    async def create_cultural_context(self, culture_name: str) -> CulturalContext:
        """Cria contexto cultural para uma cultura específica."""
        if culture_name not in self.cultures:
            raise ValueError(f"Cultura não encontrada: {culture_name}")
            
        # Gera padrões para a cultura
        patterns = await self._convert_culture_to_patterns(self.cultures[culture_name])
        
        # Cria contexto cultural
        context = CulturalContext(
            dominant_patterns=patterns,
            interaction_history=[],
            confidence_threshold=0.7,
            pattern_lifetime=3600  # 1 hora
        )
        
        # Valida o contexto
        validation_results = await self.validator.validate_context(context)
        
        if not all(result.success for result in validation_results):
            logger.warning(f"Algumas validações falharam para {culture_name}")
            for result in validation_results:
                if not result.success:
                    logger.warning(f"Falha: {result.message}")
                    
        return context
        
    async def merge_cultural_patterns(
        self,
        culture_names: List[str]
    ) -> Dict[str, List[CulturalPattern]]:
        """Mescla padrões de múltiplas culturas."""
        merged_patterns = {}
        
        # Gera padrões para cada cultura
        for culture_name in culture_names:
            if culture_name in self.cultures:
                patterns = await self._convert_culture_to_patterns(
                    self.cultures[culture_name]
                )
                merged_patterns[culture_name] = patterns
                
        return merged_patterns
        
    async def generate_warmup_data(
        self,
        culture_names: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Gera dados de warm-up baseados nas culturas existentes."""
        warmup_data = {}
        
        for culture_name in culture_names:
            if culture_name not in self.cultures:
                continue
                
            culture = self.cultures[culture_name]
            warmup_data[culture_name] = []
            
            # Gera dados para valores culturais
            if hasattr(culture, 'core_values'):
                for value in culture.core_values.values():
                    warmup_data[culture_name].append({
                        "type": "value",
                        "name": value.name if hasattr(value, 'name') else "unknown",
                        "description": value.description if hasattr(value, 'description')
                                     else "",
                        "importance": value.importance if hasattr(value, 'importance')
                                    else 0.5,
                        "manifestations": value.manifestations if hasattr(value, 'manifestations')
                                        else []
                    })
                    
            # Gera dados para práticas culturais
            if hasattr(culture, 'cultural_practices'):
                for practice in culture.cultural_practices.values():
                    warmup_data[culture_name].append({
                        "type": "practice",
                        "name": practice.name if hasattr(practice, 'name') else "unknown",
                        "description": practice.description if hasattr(practice, 'description')
                                     else "",
                        "significance": practice.significance if hasattr(practice, 'significance')
                                      else 0.5,
                        "required_resources": practice.required_resources if hasattr(practice, 'required_resources')
                                            else []
                    })
                    
            # Gera dados para sistema de crenças
            if hasattr(culture, 'belief_system'):
                for belief_type, belief_data in culture.belief_system.items():
                    if isinstance(belief_data, dict):
                        warmup_data[culture_name].append({
                            "type": "belief",
                            "name": belief_type,
                            "elements": self._extract_belief_indicators(belief_data),
                            "significance": belief_data.get('significance', 0.5)
                        })
                        
        return warmup_data
        
    async def generate_training_examples(
        self,
        culture_names: List[str]
    ) -> List[Dict[str, Any]]:
        """Gera exemplos de treinamento baseados nas culturas existentes."""
        examples = []
        now = datetime.now()
        
        for culture_name in culture_names:
            if culture_name not in self.cultures:
                continue
                
            culture = self.cultures[culture_name]
            
            # Gera exemplos baseados em valores
            if hasattr(culture, 'core_values'):
                for value_name, value in culture.core_values.items():
                    if hasattr(value, 'manifestations') and hasattr(value, 'importance'):
                        example = {
                            "scenario": f"{culture_name}_{value_name}_scenario",
                            "culture": culture_name,
                            "initial_state": {
                                "pattern": CulturalPattern(
                                    name=value_name,
                                    description=value.description if hasattr(value, 'description')
                                              else "",
                                    indicators=value.manifestations[:2],  # Primeiros 2 indicadores
                                    strength=value.importance * 0.8,  # 80% da importância
                                    confidence=0.7,
                                    last_update=now,
                                    context={"type": "value", "scope": "cultural"}
                                ),
                                "metrics": {
                                    "cultural_alignment": 0.6,
                                    "value_expression": 0.5
                                }
                            },
                            "transition_events": [
                                {
                                    "type": "value_reinforcement",
                                    "intensity": 0.7,
                                    "target": value_name
                                }
                            ],
                            "expected_outcome": {
                                "pattern": value_name,
                                "indicators": value.manifestations,
                                "min_strength": value.importance
                            }
                        }
                        examples.append(example)
                        
            # Gera exemplos baseados em práticas
            if hasattr(culture, 'cultural_practices'):
                for practice_name, practice in culture.cultural_practices.items():
                    if hasattr(practice, 'required_resources') and hasattr(practice, 'significance'):
                        example = {
                            "scenario": f"{culture_name}_{practice_name}_scenario",
                            "culture": culture_name,
                            "initial_state": {
                                "pattern": CulturalPattern(
                                    name=practice_name,
                                    description=practice.description if hasattr(practice, 'description')
                                              else "",
                                    indicators=practice.required_resources[:2],
                                    strength=practice.significance * 0.7,
                                    confidence=0.6,
                                    last_update=now,
                                    context={"type": "practice", "scope": "behavioral"}
                                ),
                                "metrics": {
                                    "practice_proficiency": 0.5,
                                    "resource_availability": 0.7
                                }
                            },
                            "transition_events": [
                                {
                                    "type": "practice_training",
                                    "duration_hours": 2,
                                    "intensity": 0.8
                                }
                            ],
                            "expected_outcome": {
                                "pattern": practice_name,
                                "indicators": practice.required_resources,
                                "min_strength": practice.significance
                            }
                        }
                        examples.append(example)
                        
        return examples
        
    def get_cultural_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Retorna metadados das culturas disponíveis."""
        metadata = {}
        
        for culture_name, culture in self.cultures.items():
            metadata[culture_name] = {
                "name": culture.name if hasattr(culture, 'name') else culture_name,
                "era": culture.era if hasattr(culture, 'era') else "Unknown",
                "value_count": len(culture.core_values) if hasattr(culture, 'core_values') else 0,
                "practice_count": len(culture.cultural_practices) if hasattr(culture, 'cultural_practices') else 0,
                "belief_types": list(culture.belief_system.keys()) if hasattr(culture, 'belief_system') else []
            }
            
        return metadata
