"""
Interfaces base para o sistema AEON Chess.
Define contratos para implementação dos diferentes componentes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

# Tipos básicos
class MoveType(Enum):
    NORMAL = "normal"
    CAPTURE = "capture"
    CASTLE = "castle"
    EN_PASSANT = "en_passant"
    PROMOTION = "promotion"

@dataclass
class Position:
    rank: int
    file: int

@dataclass
class Move:
    from_pos: Position
    to_pos: Position
    move_type: MoveType
    promotion_piece: Optional[str] = None

@dataclass
class GameState:
    board_state: Dict[Position, str]
    current_turn: str
    move_history: List[Move]
    captured_pieces: List[str]

# Interface do Motor de Xadrez
class IChessEngine(ABC):
    """Interface base para motores de xadrez."""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Inicializa o motor."""
        pass
    
    @abstractmethod
    async def get_valid_moves(self, position: Position) -> List[Move]:
        """Retorna movimentos válidos para uma posição."""
        pass
    
    @abstractmethod
    async def make_move(self, move: Move) -> bool:
        """Executa um movimento."""
        pass
    
    @abstractmethod
    async def evaluate_position(self) -> float:
        """Avalia a posição atual."""
        pass
    
    @abstractmethod
    async def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """Verifica se o jogo acabou e retorna o vencedor."""
        pass

# Interface do Campo Quântico
class IQuantumField(ABC):
    """Interface para o campo quântico."""
    
    @abstractmethod
    async def initialize_field(self) -> bool:
        """Inicializa o campo quântico."""
        pass
    
    @abstractmethod
    async def update_field(self, game_state: GameState) -> None:
        """Atualiza o campo com novo estado."""
        pass
    
    @abstractmethod
    async def calculate_influences(self, position: Position) -> Dict[Position, float]:
        """Calcula influências quânticas."""
        pass
    
    @abstractmethod
    async def get_quantum_state(self) -> Dict[str, float]:
        """Retorna estado quântico atual."""
        pass
    
    @abstractmethod
    async def collapse_field(self) -> GameState:
        """Colapsa o campo em um estado clássico."""
        pass

# Interface do Aprendizado Simbiótico
class ISymbioticLearner(ABC):
    """Interface para o sistema de aprendizado simbiótico."""
    
    @abstractmethod
    async def initialize_learning(self) -> bool:
        """Inicializa sistema de aprendizado."""
        pass
    
    @abstractmethod
    async def process_game_state(self, state: GameState) -> None:
        """Processa um estado do jogo."""
        pass
    
    @abstractmethod
    async def suggest_move(self, state: GameState) -> Move:
        """Sugere próximo movimento."""
        pass
    
    @abstractmethod
    async def evolve_strategies(self) -> None:
        """Evolui estratégias de jogo."""
        pass
    
    @abstractmethod
    async def get_learning_metrics(self) -> Dict[str, float]:
        """Retorna métricas de aprendizado."""
        pass

# Interface do Analisador de Arquitetura
class IArchitectureAnalyzer(ABC):
    """Interface para análise arquitetural do sistema."""
    
    @abstractmethod
    async def analyze_system(self) -> Dict[str, Dict]:
        """Analisa estado do sistema."""
        pass
    
    @abstractmethod
    async def optimize_resources(self) -> bool:
        """Otimiza uso de recursos."""
        pass
    
    @abstractmethod
    async def detect_bottlenecks(self) -> List[Dict]:
        """Detecta gargalos no sistema."""
        pass
    
    @abstractmethod
    async def suggest_improvements(self) -> List[Dict]:
        """Sugere melhorias arquiteturais."""
        pass
    
    @abstractmethod
    async def get_health_metrics(self) -> Dict[str, float]:
        """Retorna métricas de saúde do sistema."""
        pass

# Interface de Integração
class ISystemIntegration(ABC):
    """Interface para integração entre sistemas."""
    
    @abstractmethod
    async def connect_systems(self) -> bool:
        """Estabelece conexão entre sistemas."""
        pass
    
    @abstractmethod
    async def synchronize_state(self) -> bool:
        """Sincroniza estado entre sistemas."""
        pass
    
    @abstractmethod
    async def handle_communication(self, message: Dict) -> Dict:
        """Processa comunicação entre sistemas."""
        pass
    
    @abstractmethod
    async def manage_resources(self) -> bool:
        """Gerencia recursos compartilhados."""
        pass
    
    @abstractmethod
    async def monitor_integration(self) -> Dict[str, float]:
        """Monitora estado da integração."""
        pass
