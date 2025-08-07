from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass
import json
import hashlib

@dataclass
class CacheEntry:
    """Entrada do cache com metadados."""
    key: str
    data: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_access: Optional[datetime] = None

class NarrativeCache:
    """Gerenciador de cache para o conector narrativo."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl  # TTL padrão em segundos
        self.cache: Dict[str, CacheEntry] = {}
        self.hit_count = 0
        self.miss_count = 0
        self.preload_patterns: Dict[str, List[str]] = {
            "opening_sequence": [
                "game_start",
                "initial_position",
                "first_moves"
            ],
            "midgame_patterns": [
                "positional_play",
                "tactical_opportunities",
                "strategic_planning"
            ],
            "endgame_scenarios": [
                "king_and_pawn",
                "rook_endings",
                "piece_coordination"
            ]
        }
        
    async def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache."""
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry.expires_at:
                entry.access_count += 1
                entry.last_access = datetime.now()
                self.hit_count += 1
                return entry.data
            else:
                # Item expirado
                del self.cache[key]
        self.miss_count += 1
        return None
        
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Armazena um item no cache."""
        try:
            # Limpa cache se necessário
            if len(self.cache) >= self.max_size:
                await self._cleanup()
                
            # Calcula expiração
            ttl = ttl or self.default_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            # Cria entrada
            entry = CacheEntry(
                key=key,
                data=value,
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            self.cache[key] = entry
            return True
        except Exception as e:
            print(f"Erro ao armazenar em cache: {e}")
            return False
            
    async def preload(self, pattern: str) -> bool:
        """Pré-carrega dados no cache baseado em padrões."""
        try:
            if pattern not in self.preload_patterns:
                return False
                
            keys = self.preload_patterns[pattern]
            for key in keys:
                # Simula carregamento de dados
                data = await self._generate_sample_data(key)
                await self.set(key, data)
                
            return True
        except Exception as e:
            print(f"Erro no pré-carregamento: {e}")
            return False
            
    async def _cleanup(self):
        """Limpa entradas antigas do cache."""
        now = datetime.now()
        
        # Remove itens expirados
        expired = [k for k, v in self.cache.items() if v.expires_at <= now]
        for key in expired:
            del self.cache[key]
            
        # Se ainda precisar de espaço, remove itens menos acessados
        if len(self.cache) >= self.max_size:
            items = sorted(
                self.cache.items(),
                key=lambda x: (x[1].access_count, x[1].last_access or datetime.min)
            )
            # Remove 20% dos itens menos acessados
            remove_count = max(1, len(self.cache) // 5)
            for key, _ in items[:remove_count]:
                del self.cache[key]
                
    async def _generate_sample_data(self, key: str) -> Dict[str, Any]:
        """Gera dados de exemplo para pré-carregamento."""
        # Simula processamento
        await asyncio.sleep(0.1)
        
        return {
            "key": key,
            "type": "narrative_element",
            "timestamp": datetime.now().isoformat(),
            "complexity": 0.7,
            "attributes": {
                "adaptability": 0.8,
                "coherence": 0.9
            }
        }
        
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total_requests if total_requests > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }
        
    def generate_key(self, data: Any) -> str:
        """Gera uma chave única para os dados."""
        if isinstance(data, (str, int, float, bool)):
            content = str(data)
        elif isinstance(data, (dict, list)):
            content = json.dumps(data, sort_keys=True)
        else:
            content = str(hash(data))
            
        return hashlib.sha256(content.encode()).hexdigest()[:32]
