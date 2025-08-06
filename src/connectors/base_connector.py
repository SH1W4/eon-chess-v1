from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseConnector(ABC):
    """Interface base para todos os conectores do sistema."""
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._is_initialized: bool = False
        
    @abstractmethod
    async def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Inicializa o conector com configurações opcionais."""
        pass
        
    @abstractmethod
    async def connect(self) -> bool:
        """Estabelece conexão com o sistema alvo."""
        pass
        
    @abstractmethod
    async def disconnect(self) -> bool:
        """Desconecta do sistema alvo."""
        pass
        
    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do conector."""
        pass
        
    @abstractmethod
    async def update_state(self, new_state: Dict[str, Any]) -> bool:
        """Atualiza o estado do conector."""
        pass
        
    @abstractmethod
    async def verify_health(self) -> bool:
        """Verifica a saúde do conector."""
        pass
