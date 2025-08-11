"""
CHESS Integration Module
Provides connectors for NEXUS, ARQUIMAX, and Symbiotic Framework
"""

from .nexus_connector import (
    NexusConnector,
    NexusConfig,
    initialize_nexus
)

from .arquimax_connector import (
    ArquimaxConnector,
    ArquimaxConfig,
    initialize_arquimax,
    Task,
    TaskStatus
)

from .symbiotic_framework import (
    SymbioticFramework,
    SymbioticConfig,
    EvolutionPhase,
    initialize_symbiotic
)

__all__ = [
    # NEXUS
    'NexusConnector',
    'NexusConfig',
    'initialize_nexus',
    
    # ARQUIMAX
    'ArquimaxConnector',
    'ArquimaxConfig',
    'initialize_arquimax',
    'Task',
    'TaskStatus',
    
    # Symbiotic
    'SymbioticFramework',
    'SymbioticConfig',
    'EvolutionPhase',
    'initialize_symbiotic'
]

__version__ = '1.0.0'
