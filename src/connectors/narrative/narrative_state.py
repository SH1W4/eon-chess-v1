from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class StoryElementType(Enum):
    """Tipos de elementos narrativos."""
    CHARACTER = "character"
    PLOT = "plot"
    SETTING = "setting"
    THEME = "theme"
    EVENT = "event"
    CONFLICT = "conflict"
    RESOLUTION = "resolution"

@dataclass
class StoryElement:
    """
    Elemento básico de uma narrativa.
    Representa personagens, eventos, configurações, etc.
    """
    id: str
    type: StoryElementType
    name: str
    description: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class NarrativeFlow:
    """
    Fluxo narrativo que conecta elementos em uma sequência coerente.
    Define como a história se desenvolve ao longo do tempo.
    """
    id: str
    name: str
    description: str
    elements: List[StoryElement] = field(default_factory=list)
    connections: Dict[str, List[str]] = field(default_factory=dict)
    state: str = "inactive"
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    async def prepare(self) -> None:
        """Prepara o fluxo para execução."""
        self.state = "active"
        self.progress = 0.0
        self.updated_at = datetime.now()
        
    async def advance(self, progress: float) -> None:
        """Avança o progresso do fluxo."""
        self.progress = min(1.0, progress)
        self.updated_at = datetime.now()
        
    async def finalize(self) -> None:
        """Finaliza o fluxo narrativo."""
        self.state = "completed"
        self.progress = 1.0
        self.updated_at = datetime.now()
        
    def is_healthy(self) -> bool:
        """Verifica a saúde do fluxo."""
        return self.state in ["active", "completed"] and len(self.elements) > 0

@dataclass
class NarrativeState:
    """
    Estado do sistema narrativo.
    Gerencia elementos, fluxos e coerência narrativa.
    """
    # Timestamp da última atualização
    last_update: datetime = field(default_factory=datetime.now)
    
    # Elementos ativos na narrativa
    active_elements: Dict[str, StoryElement] = field(default_factory=dict)
    
    # Métricas narrativas
    narrative_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Estado do sistema
    system_state: Dict[str, Any] = field(default_factory=dict)
    
    # Status geral
    health_status: str = "unknown"
    
    def __init__(self):
        """Inicializa o estado com valores padrão."""
        self.last_update = datetime.now()
        self.active_elements = {}
        self.narrative_metrics = {
            "coherence_score": 0.0,
            "engagement_level": 0.0,
            "complexity_index": 0.0
        }
        self.system_state = {
            "active_flows": 0,
            "story_elements": 0,
            "narrative_conflicts": []
        }
        self.health_status = "initialized"
        
    async def configure(self, config: Dict[str, Any]) -> None:
        """
        Configura o estado com base nas configurações fornecidas.
        Args:
            config: Configurações incluindo elementos iniciais e métricas.
        """
        try:
            # Configura elementos narrativos
            if "initial_elements" in config:
                for element_data in config["initial_elements"]:
                    element = StoryElement(**element_data)
                    self.active_elements[element.id] = element
                    
            # Configura métricas narrativas
            if "metric_thresholds" in config:
                self.narrative_metrics.update(config["metric_thresholds"])
                
            # Configura estado do sistema
            if "system_config" in config:
                self.system_state.update(config["system_config"])
                
            self.last_update = datetime.now()
        except Exception as e:
            raise ValueError(f"Erro na configuração do estado narrativo: {e}")
            
    async def initialize_storytelling(self) -> None:
        """Inicializa o sistema de storytelling."""
        try:
            # Prepara elementos narrativos
            for element in self.active_elements.values():
                element.updated_at = datetime.now()
                
            # Inicializa métricas
            self.narrative_metrics.update({
                "coherence_score": 1.0,
                "engagement_level": 0.5,
                "complexity_index": 0.3
            })
            
            # Atualiza estado do sistema
            self.system_state.update({
                "active_flows": len(self.active_elements),
                "story_elements": len(self.active_elements),
                "narrative_conflicts": []
            })
            
            self.health_status = "active"
        except Exception as e:
            raise RuntimeError(f"Erro na inicialização do storytelling: {e}")
            
    async def get_current_state(self) -> Dict[str, Any]:
        """Retorna o estado atual completo."""
        return {
            "last_update": self.last_update.isoformat(),
            "active_elements": {
                id: self._element_to_dict(element)
                for id, element in self.active_elements.items()
            },
            "narrative_metrics": self.narrative_metrics,
            "system_state": self.system_state,
            "health_status": self.health_status
        }
        
    async def update(self, new_state: Dict[str, Any]) -> None:
        """
        Atualiza o estado com novos valores.
        Args:
            new_state: Novos valores para atualização do estado.
        """
        try:
            # Atualiza elementos narrativos
            if "elements" in new_state:
                for element_data in new_state["elements"]:
                    element_id = element_data["id"]
                    if element_id in self.active_elements:
                        self._update_element(self.active_elements[element_id], element_data)
                    else:
                        self.active_elements[element_id] = StoryElement(**element_data)
                        
            # Atualiza métricas narrativas
            if "metrics" in new_state:
                self.narrative_metrics.update(new_state["metrics"])
                
            # Atualiza estado do sistema
            if "system_state" in new_state:
                self.system_state.update(new_state["system_state"])
                
            self.last_update = datetime.now()
        except Exception as e:
            raise ValueError(f"Erro na atualização do estado narrativo: {e}")
            
    async def add_element(self, element: StoryElement) -> bool:
        """
        Adiciona um novo elemento narrativo.
        Args:
            element: Elemento a ser adicionado.
        """
        try:
            self.active_elements[element.id] = element
            self.system_state["story_elements"] = len(self.active_elements)
            return True
        except Exception:
            return False
            
    async def save_checkpoint(self) -> Dict[str, Any]:
        """Salva um checkpoint do estado atual."""
        return await self.get_current_state()
        
    async def is_healthy(self) -> bool:
        """
        Verifica se o estado está saudável.
        Considera coerência narrativa e métricas do sistema.
        """
        try:
            # Verifica tempo desde última atualização
            time_since_update = (datetime.now() - self.last_update).total_seconds()
            if time_since_update > 3600:  # 1 hora
                self.health_status = "stale"
                return False
                
            # Verifica elementos narrativos
            if not self.active_elements:
                self.health_status = "no_active_elements"
                return False
                
            # Verifica métricas narrativas
            if self.narrative_metrics["coherence_score"] < 0.5:
                self.health_status = "low_coherence"
                return False
                
            if self.narrative_metrics["engagement_level"] < 0.3:
                self.health_status = "low_engagement"
                return False
                
            # Verifica conflitos narrativos
            if len(self.system_state["narrative_conflicts"]) > 10:
                self.health_status = "too_many_conflicts"
                return False
                
            self.health_status = "healthy"
            return True
        except Exception:
            self.health_status = "error"
            return False
            
    def _element_to_dict(self, element: StoryElement) -> Dict[str, Any]:
        """Converte um elemento narrativo para dicionário."""
        return {
            "id": element.id,
            "type": element.type.value,
            "name": element.name,
            "description": element.description,
            "attributes": element.attributes,
            "relationships": element.relationships,
            "created_at": element.created_at.isoformat(),
            "updated_at": element.updated_at.isoformat()
        }
        
    def _update_element(self, element: StoryElement, data: Dict[str, Any]) -> None:
        """Atualiza um elemento narrativo com novos dados."""
        for key, value in data.items():
            if hasattr(element, key):
                setattr(element, key, value)
        element.updated_at = datetime.now()
