from typing import Dict, Any, Optional
from .lru_cache import LRUCache
import json

class ProfileCacheManager:
    """
    Gerenciador de cache específico para perfis de liderança.
    Implementa políticas de cache específicas para diferentes tipos de dados dos perfis.
    """
    def __init__(self):
        # Cache para perfis completos
        self.profile_cache = LRUCache(capacity=100)
        # Cache para padrões estratégicos
        self.pattern_cache = LRUCache(capacity=500)
        # Cache para narrativas
        self.narrative_cache = LRUCache(capacity=200)

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Recupera um perfil completo do cache."""
        return self.profile_cache.get(profile_id)

    def cache_profile(self, profile_id: str, profile_data: Dict[str, Any]) -> None:
        """Armazena um perfil completo no cache."""
        self.profile_cache.put(profile_id, profile_data)

    def get_pattern(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        """Recupera um padrão estratégico do cache."""
        return self.pattern_cache.get(pattern_id)

    def cache_pattern(self, pattern_id: str, pattern_data: Dict[str, Any]) -> None:
        """Armazena um padrão estratégico no cache."""
        self.pattern_cache.put(pattern_id, pattern_data)

    def get_narrative(self, narrative_id: str) -> Optional[str]:
        """Recupera uma narrativa do cache."""
        return self.narrative_cache.get(narrative_id)

    def cache_narrative(self, narrative_id: str, narrative_text: str) -> None:
        """Armazena uma narrativa no cache."""
        self.narrative_cache.put(narrative_id, narrative_text)

    def clear_all(self) -> None:
        """Limpa todos os caches."""
        self.profile_cache.clear()
        self.pattern_cache.clear()
        self.narrative_cache.clear()

    def get_stats(self) -> Dict[str, Dict[str, int]]:
        """Retorna estatísticas do uso do cache."""
        return {
            "profiles": {
                "size": self.profile_cache.get_size(),
                "capacity": self.profile_cache.get_capacity()
            },
            "patterns": {
                "size": self.pattern_cache.get_size(),
                "capacity": self.pattern_cache.get_capacity()
            },
            "narratives": {
                "size": self.narrative_cache.get_size(),
                "capacity": self.narrative_cache.get_capacity()
            }
        }

    def export_cache_state(self, file_path: str) -> None:
        """Exporta o estado atual do cache para um arquivo JSON."""
        cache_state = {
            "profiles": {
                "data": {k: v for k, v in zip(
                    self.profile_cache.get_keys(),
                    [self.profile_cache.get(k) for k in self.profile_cache.get_keys()]
                )},
                "metadata": {
                    "size": self.profile_cache.get_size(),
                    "capacity": self.profile_cache.get_capacity()
                }
            },
            "patterns": {
                "data": {k: v for k, v in zip(
                    self.pattern_cache.get_keys(),
                    [self.pattern_cache.get(k) for k in self.pattern_cache.get_keys()]
                )},
                "metadata": {
                    "size": self.pattern_cache.get_size(),
                    "capacity": self.pattern_cache.get_capacity()
                }
            },
            "narratives": {
                "data": {k: v for k, v in zip(
                    self.narrative_cache.get_keys(),
                    [self.narrative_cache.get(k) for k in self.narrative_cache.get_keys()]
                )},
                "metadata": {
                    "size": self.narrative_cache.get_size(),
                    "capacity": self.narrative_cache.get_capacity()
                }
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cache_state, f, indent=2, ensure_ascii=False)
