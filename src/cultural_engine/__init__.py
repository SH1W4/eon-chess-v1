"""
Cultural Engine - Sistema de integração de perfis de liderança e geração de narrativas culturais
para o ChessMaster.

Este módulo implementa:
- Cache eficiente para perfis e padrões
- Processamento de perfis de liderança
- Geração de narrativas culturais
- Análise de padrões estratégicos
"""

from .cache.lru_cache import LRUCache
from .cache.profile_cache_manager import ProfileCacheManager
from .processors.leadership_profile_processor import LeadershipProfileProcessor
from .processors.narrative_generator import NarrativeGenerator

__version__ = '1.0.0'
__author__ = 'ChessMaster Team'

__all__ = [
    'LRUCache',
    'ProfileCacheManager',
    'LeadershipProfileProcessor',
    'NarrativeGenerator',
]
