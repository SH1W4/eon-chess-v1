from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import threading
from pathlib import Path

class AdvancedCache:
    """Cache avançado com suporte a persistência e métricas."""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict] = {}
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        
    def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache com suporte a TTL."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
                
            metadata = self._metadata[key]
            if self._is_expired(metadata['timestamp']):
                self._evict(key)
                self._misses += 1
                return None
                
            self._hits += 1
            metadata['access_count'] += 1
            metadata['last_access'] = datetime.now()
            return self._cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Armazena um valor no cache com TTL opcional."""
        with self._lock:
            if len(self._cache) >= self._max_size:
                self._evict_lru()
            
            self._cache[key] = value
            self._metadata[key] = {
                'timestamp': datetime.now(),
                'ttl': ttl or self._ttl,
                'access_count': 0,
                'last_access': datetime.now(),
                'size': self._estimate_size(value)
            }
    
    def _is_expired(self, timestamp: datetime) -> bool:
        """Verifica se um item expirou."""
        age = (datetime.now() - timestamp).total_seconds()
        return age > self._ttl
    
    def _evict(self, key: str) -> None:
        """Remove um item do cache."""
        del self._cache[key]
        del self._metadata[key]
        self._evictions += 1
    
    def _evict_lru(self) -> None:
        """Remove o item menos recentemente usado."""
        lru_key = min(
            self._metadata.items(),
            key=lambda x: x[1]['last_access']
        )[0]
        self._evict(lru_key)
    
    def _estimate_size(self, value: Any) -> int:
        """Estima o tamanho em bytes de um valor."""
        return len(json.dumps(value)) if hasattr(value, '__dict__') else 1
    
    def get_metrics(self) -> Dict[str, float]:
        """Retorna métricas do cache."""
        total_ops = self._hits + self._misses
        return {
            'hit_rate': self._hits / max(total_ops, 1),
            'miss_rate': self._misses / max(total_ops, 1),
            'eviction_rate': self._evictions / max(total_ops, 1),
            'size': len(self._cache),
            'memory_usage': sum(m['size'] for m in self._metadata.values())
        }
    
    def persist(self, filepath: str) -> None:
        """Persiste o cache em disco."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with self._lock:
            with open(filepath, 'w') as f:
                json.dump({
                    'cache': self._cache,
                    'metadata': self._metadata
                }, f)
    
    def load(self, filepath: str) -> None:
        """Carrega o cache do disco."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                with self._lock:
                    self._cache = data['cache']
                    self._metadata = data['metadata']
        except FileNotFoundError:
            pass  # Ignora se arquivo não existe

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import hashlib
import json

@dataclass
class CacheEntry:
    """Entrada do cache com tempo de vida"""
    value: Any
    expiry: datetime
    metadata: Dict = field(default_factory=dict)

class CulturalCache:
    """Sistema de cache para operações culturais"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl  # TTL padrão em segundos
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Gera uma chave única para os argumentos"""
        # Combina todos os argumentos em uma string
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        key_string = "|".join(key_parts)
        
        # Gera um hash SHA-256
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera um valor do cache"""
        if key not in self.cache:
            self.stats['misses'] += 1
            return None
            
        entry = self.cache[key]
        if datetime.now() > entry.expiry:
            self.stats['evictions'] += 1
            del self.cache[key]
            return None
            
        self.stats['hits'] += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, metadata: Optional[Dict] = None) -> None:
        """Armazena um valor no cache"""
        ttl = ttl or self.default_ttl
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = CacheEntry(value, expiry, metadata or {})
    
    def clear(self) -> None:
        """Limpa todo o cache"""
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'evictions': 0}
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do cache"""
        return self.stats.copy()

class CulturalCacheDecorator:
    """Decorador para cache de funções culturais"""
    
    def __init__(self, cache: CulturalCache, ttl: Optional[int] = None):
        self.cache = cache
        self.ttl = ttl
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Gera chave do cache
            cache_key = self.cache._generate_key(func.__name__, *args, **kwargs)
            
            # Tenta recuperar do cache
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Executa função e armazena resultado
            result = func(*args, **kwargs)
            self.cache.set(cache_key, result, self.ttl)
            
            return result
        return wrapper

# Cache específico para análise cultural
class CulturalAnalysisCache(CulturalCache):
    """Cache especializado para análise cultural"""
    
    def __init__(self, default_ttl: int = 3600):
        super().__init__(default_ttl)
        self.pattern_cache: Dict[str, List[str]] = {}
    
    def cache_pattern(self, pattern_type: str, board_state: Dict) -> None:
        """Armazena um padrão reconhecido"""
        key = self._generate_key(pattern_type, json.dumps(board_state, sort_keys=True))
        if key not in self.pattern_cache:
            self.pattern_cache[key] = []
        self.pattern_cache[key].append(pattern_type)
    
    def get_patterns(self, board_state: Dict) -> List[str]:
        """Recupera padrões reconhecidos para um estado"""
        patterns = []
        board_key = json.dumps(board_state, sort_keys=True)
        
        for key in self.pattern_cache:
            if board_key in key:
                patterns.extend(self.pattern_cache[key])
        
        return patterns
    
    def clear_patterns(self) -> None:
        """Limpa cache de padrões"""
        self.pattern_cache.clear()

# Cache específico para eventos culturais
class CulturalEventCache(CulturalCache):
    """Cache especializado para eventos culturais"""
    
    def __init__(self, default_ttl: int = 1800):  # TTL menor para eventos
        super().__init__(default_ttl)
        self.active_events: Dict[str, List[str]] = {}
    
    def cache_event(self, culture: str, event_type: str, board_state: Dict) -> None:
        """Armazena um evento ativo"""
        key = self._generate_key(culture, event_type, json.dumps(board_state, sort_keys=True))
        if culture not in self.active_events:
            self.active_events[culture] = []
        self.active_events[culture].append(event_type)
        
        # Armazena no cache principal também
        self.set(key, True)
    
    def get_active_events(self, culture: str) -> List[str]:
        """Recupera eventos ativos para uma cultura"""
        return self.active_events.get(culture, [])
    
    def clear_events(self, culture: Optional[str] = None) -> None:
        """Limpa eventos de uma cultura ou todos"""
        if culture:
            if culture in self.active_events:
                del self.active_events[culture]
        else:
            self.active_events.clear()

# Cache específico para narrativas
class NarrativeCache(CulturalCache):
    """Cache especializado para narrativas"""
    
    def __init__(self, default_ttl: int = 7200):  # TTL maior para narrativas
        super().__init__(default_ttl)
        self.narrative_history: Dict[str, List[str]] = {}
    
    def cache_narrative(self, culture: str, narrative: str, context: Dict) -> None:
        """Armazena uma narrativa gerada"""
        key = self._generate_key(culture, json.dumps(context, sort_keys=True))
        if culture not in self.narrative_history:
            self.narrative_history[culture] = []
        self.narrative_history[culture].append(narrative)
        
        # Armazena no cache principal também
        self.set(key, narrative)
    
    def get_recent_narratives(self, culture: str, limit: int = 5) -> List[str]:
        """Recupera narrativas recentes de uma cultura"""
        narratives = self.narrative_history.get(culture, [])
        return narratives[-limit:] if narratives else []
    
    def clear_narratives(self, culture: Optional[str] = None) -> None:
        """Limpa narrativas de uma cultura ou todas"""
        if culture:
            if culture in self.narrative_history:
                del self.narrative_history[culture]
        else:
            self.narrative_history.clear()

# Exemplo de uso do cache
def cache_example():
    # Criação dos caches especializados
    analysis_cache = CulturalAnalysisCache()
    event_cache = CulturalEventCache()
    narrative_cache = NarrativeCache()
    
    # Exemplo de uso do decorador
    @CulturalCacheDecorator(analysis_cache)
    def analyze_position(board_state: Dict) -> Dict:
        # Simulação de análise complexa
        return {'score': 0.5, 'patterns': ['pattern1', 'pattern2']}
    
    # Uso dos caches
    board_state = {'position': 'some_position'}
    
    # Cache de análise
    analysis_cache.cache_pattern('spiral', board_state)
    patterns = analysis_cache.get_patterns(board_state)
    
    # Cache de eventos
    event_cache.cache_event('indian', 'chakravyuha', board_state)
    active_events = event_cache.get_active_events('indian')
    
    # Cache de narrativas
    narrative_cache.cache_narrative('arabic', 'Uma narrativa poética', {'context': 'some_context'})
    recent = narrative_cache.get_recent_narratives('arabic')
    
    return {
        'patterns': patterns,
        'events': active_events,
        'narratives': recent
    }
