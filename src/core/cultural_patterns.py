from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)

@dataclass
class CulturalPattern:
    """Padrão cultural identificado no sistema."""
    name: str
    description: str
    indicators: List[str]
    strength: float  # 0.0 a 1.0
    confidence: float  # 0.0 a 1.0
    last_update: datetime
    context: Dict[str, Any]
    
@dataclass
class CulturalContext:
    """Contexto cultural atual do sistema."""
    dominant_patterns: List[CulturalPattern]
    interaction_history: List[Dict[str, Any]]
    confidence_threshold: float
    pattern_lifetime: int  # segundos
    
class CulturalPatternRecognizer:
    """Sistema de reconhecimento de padrões culturais."""
    
    def __init__(self):
        self.patterns: Dict[str, CulturalPattern] = {}
        self.current_context = CulturalContext(
            dominant_patterns=[],
            interaction_history=[],
            confidence_threshold=0.7,
            pattern_lifetime=3600  # 1 hora
        )
        
        # Configurações do reconhecedor
        self.config = {
            "min_pattern_strength": 0.3,
            "max_patterns": 10,
            "history_size": 1000,
            "update_interval": 300  # 5 minutos
        }
        
    async def initialize_patterns(self):
        """Inicializa os padrões culturais básicos."""
        basic_patterns = {
            "collaborative": CulturalPattern(
                name="collaborative",
                description="Padrão de colaboração e compartilhamento",
                indicators=["resource_sharing", "mutual_aid", "collective_decision"],
                strength=0.5,
                confidence=0.8,
                last_update=datetime.now(),
                context={"type": "social", "scope": "group"}
            ),
            "competitive": CulturalPattern(
                name="competitive",
                description="Padrão de competição e otimização",
                indicators=["resource_competition", "performance_focus", "individual_achievement"],
                strength=0.5,
                confidence=0.8,
                last_update=datetime.now(),
                context={"type": "social", "scope": "individual"}
            ),
            "adaptive": CulturalPattern(
                name="adaptive",
                description="Padrão de adaptação e evolução",
                indicators=["learning_rate", "mutation_frequency", "adaptation_success"],
                strength=0.5,
                confidence=0.8,
                last_update=datetime.now(),
                context={"type": "evolutionary", "scope": "system"}
            )
        }
        
        self.patterns.update(basic_patterns)
        await self._validate_patterns()
        
    async def _validate_patterns(self):
        """Valida os padrões culturais existentes."""
        invalid_patterns = []
        
        for name, pattern in self.patterns.items():
            if pattern.strength < self.config["min_pattern_strength"]:
                invalid_patterns.append(name)
            elif (datetime.now() - pattern.last_update).total_seconds() > self.current_context.pattern_lifetime:
                invalid_patterns.append(name)
                
        for name in invalid_patterns:
            del self.patterns[name]
            
    async def recognize_pattern(self, interaction_data: Dict[str, Any]) -> Optional[CulturalPattern]:
        """Reconhece padrões culturais em uma interação."""
        try:
            # Registra interação no histórico
            self.current_context.interaction_history.append({
                "data": interaction_data,
                "timestamp": datetime.now().isoformat()
            })
            
            # Mantém tamanho máximo do histórico
            if len(self.current_context.interaction_history) > self.config["history_size"]:
                self.current_context.interaction_history = self.current_context.interaction_history[-self.config["history_size"]:]
            
            # Analisa padrões
            matched_pattern = None
            highest_confidence = 0.0
            
            for pattern in self.patterns.values():
                confidence = await self._calculate_pattern_match(pattern, interaction_data)
                
                if confidence > highest_confidence and confidence >= self.current_context.confidence_threshold:
                    matched_pattern = pattern
                    highest_confidence = confidence
                    
            if matched_pattern:
                # Atualiza padrão encontrado
                matched_pattern.confidence = highest_confidence
                matched_pattern.last_update = datetime.now()
                
                # Atualiza padrões dominantes
                self._update_dominant_patterns(matched_pattern)
                
            return matched_pattern
            
        except Exception as e:
            logger.error(f"Erro ao reconhecer padrão: {e}")
            return None
            
    async def _calculate_pattern_match(self, pattern: CulturalPattern, data: Dict[str, Any]) -> float:
        """Calcula o nível de confiança do match entre dados e padrão."""
        try:
            indicator_matches = 0
            
            for indicator in pattern.indicators:
                if indicator in data:
                    indicator_matches += 1
                    
            if not pattern.indicators:
                return 0.0
                
            base_confidence = indicator_matches / len(pattern.indicators)
            
            # Ajusta confiança com base no contexto
            context_multiplier = 1.0
            if pattern.context["type"] in data.get("context_type", []):
                context_multiplier *= 1.2
            if pattern.context["scope"] in data.get("context_scope", []):
                context_multiplier *= 1.2
                
            return min(base_confidence * context_multiplier, 1.0)
            
        except Exception as e:
            logger.error(f"Erro ao calcular match de padrão: {e}")
            return 0.0
            
    def _update_dominant_patterns(self, new_pattern: CulturalPattern):
        """Atualiza a lista de padrões dominantes."""
        # Remove padrões antigos
        self.current_context.dominant_patterns = [
            p for p in self.current_context.dominant_patterns
            if (datetime.now() - p.last_update).total_seconds() <= self.current_context.pattern_lifetime
        ]
        
        # Adiciona novo padrão se ainda não existir
        if new_pattern not in self.current_context.dominant_patterns:
            self.current_context.dominant_patterns.append(new_pattern)
            
        # Mantém apenas os padrões mais fortes
        self.current_context.dominant_patterns.sort(key=lambda p: p.strength * p.confidence, reverse=True)
        if len(self.current_context.dominant_patterns) > self.config["max_patterns"]:
            self.current_context.dominant_patterns = self.current_context.dominant_patterns[:self.config["max_patterns"]]
            
    def get_current_context(self) -> CulturalContext:
        """Retorna o contexto cultural atual."""
        return self.current_context
        
    async def update_pattern(self, pattern_name: str, new_data: Dict[str, Any]) -> bool:
        """Atualiza um padrão cultural existente."""
        try:
            if pattern_name not in self.patterns:
                return False
                
            pattern = self.patterns[pattern_name]
            
            # Atualiza campos permitidos
            if "indicators" in new_data:
                pattern.indicators = new_data["indicators"]
            if "strength" in new_data:
                pattern.strength = max(0.0, min(1.0, new_data["strength"]))
            if "context" in new_data:
                pattern.context.update(new_data["context"])
                
            pattern.last_update = datetime.now()
            
            # Revalida padrões
            await self._validate_patterns()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar padrão: {e}")
            return False
            
    async def cleanup_patterns(self):
        """Remove padrões obsoletos."""
        try:
            await self._validate_patterns()
            
            # Remove padrões fracos
            weak_patterns = [
                name for name, pattern in self.patterns.items()
                if pattern.strength * pattern.confidence < self.config["min_pattern_strength"]
            ]
            
            for name in weak_patterns:
                del self.patterns[name]
                
        except Exception as e:
            logger.error(f"Erro ao limpar padrões: {e}")
