from collections import OrderedDict
from typing import Any, Optional
import threading

class LRUCache:
    """
    Implementação de cache LRU (Least Recently Used) thread-safe para o motor cultural.
    """
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache."""
        with self._lock:
            if key not in self.cache:
                return None
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        """Adiciona ou atualiza um item no cache."""
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

    def remove(self, key: str) -> None:
        """Remove um item do cache."""
        with self._lock:
            if key in self.cache:
                del self.cache[key]

    def clear(self) -> None:
        """Limpa todo o cache."""
        with self._lock:
            self.cache.clear()

    def get_size(self) -> int:
        """Retorna o tamanho atual do cache."""
        with self._lock:
            return len(self.cache)

    def get_capacity(self) -> int:
        """Retorna a capacidade máxima do cache."""
        return self.capacity

    def get_keys(self) -> list:
        """Retorna todas as chaves no cache."""
        with self._lock:
            return list(self.cache.keys())

    def contains(self, key: str) -> bool:
        """Verifica se uma chave existe no cache."""
        with self._lock:
            return key in self.cache
