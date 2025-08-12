from typing import Dict, Any, Optional, List
import asyncio
import logging
import json
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

@dataclass
class CacheStats:
    """Estatísticas do cache."""
    hits: int = 0
    misses: int = 0
    size: int = 0
    items: int = 0
    evictions: int = 0

class BaseCacheStrategy(ABC):
    """Interface base para estratégias de cache."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Armazena um item no cache."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Remove um item do cache."""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Limpa todo o cache."""
        pass
    
    @abstractmethod
    def get_stats(self) -> CacheStats:
        """Retorna estatísticas do cache."""
        pass

class LRUCache(BaseCacheStrategy):
    """Implementação de cache LRU (Least Recently Used)."""
    
    def __init__(self, size: int, ttl: int):
        self.size = size
        self.default_ttl = ttl
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}
        self.expiry: Dict[str, float] = {}
        self.stats = CacheStats()
    
    async def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache."""
        try:
            if key not in self.cache:
                self.stats.misses += 1
                return None
            
            # Verifica expiração
            if self.expiry[key] < time.time():
                await self.delete(key)
                self.stats.misses += 1
                return None
            
            # Atualiza timestamp de acesso
            self.timestamps[key] = time.time()
            self.stats.hits += 1
            
            return self.cache[key]
            
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Armazena um item no cache."""
        try:
            # Verifica tamanho
            if len(self.cache) >= self.size:
                await self._evict()
            
            # Armazena valor
            self.cache[key] = value
            self.timestamps[key] = time.time()
            
            # Configura expiração
            ttl = ttl if ttl is not None else self.default_ttl
            self.expiry[key] = time.time() + ttl
            
            self.stats.items = len(self.cache)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Remove um item do cache."""
        try:
            del self.cache[key]
            del self.timestamps[key]
            del self.expiry[key]
            
            self.stats.items = len(self.cache)
            return True
            
        except KeyError:
            return False
            
        except Exception as e:
            logger.error(f"Erro ao remover do cache: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpa todo o cache."""
        try:
            self.cache.clear()
            self.timestamps.clear()
            self.expiry.clear()
            
            self.stats = CacheStats()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {str(e)}")
            return False
    
    async def _evict(self) -> bool:
        """Remove o item menos recentemente usado."""
        try:
            if not self.timestamps:
                return True
            
            # Encontra item mais antigo
            oldest_key = min(
                self.timestamps.keys(),
                key=lambda k: self.timestamps[k]
            )
            
            # Remove item
            await self.delete(oldest_key)
            self.stats.evictions += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao executar eviction: {str(e)}")
            return False
    
    def get_stats(self) -> CacheStats:
        """Retorna estatísticas do cache."""
        return self.stats

class DistributedCache(BaseCacheStrategy):
    """Implementação de cache distribuído usando Redis."""
    
    def __init__(
        self,
        config: Dict[str, Any]
    ):
        self.config = config
        self.stats = CacheStats()
        self._setup_redis()
    
    def _setup_redis(self):
        """Configura conexão com Redis."""
        try:
            import redis
            from redis.cluster import RedisCluster
            
            if self.config["modo"] == "cluster":
                self.redis = RedisCluster(
                    startup_nodes=[
                        {"host": "localhost", "port": "6379"}  # Configurar
                    ],
                    decode_responses=True
                )
            else:
                self.redis = redis.Redis(
                    host="localhost",  # Configurar
                    port=6379,
                    db=0,
                    decode_responses=True
                )
            
        except ImportError:
            logger.error("Redis não instalado")
            raise
            
        except Exception as e:
            logger.error(f"Erro ao configurar Redis: {str(e)}")
            raise
    
    async def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache distribuído."""
        try:
            value = await self.redis.get(key)
            
            if value is None:
                self.stats.misses += 1
                return None
            
            self.stats.hits += 1
            return json.loads(value)
            
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache distribuído: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Armazena um item no cache distribuído."""
        try:
            serialized = json.dumps(value)
            
            if ttl:
                await self.redis.setex(key, ttl, serialized)
            else:
                await self.redis.set(key, serialized)
            
            self.stats.items = await self.redis.dbsize()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache distribuído: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Remove um item do cache distribuído."""
        try:
            await self.redis.delete(key)
            self.stats.items = await self.redis.dbsize()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover do cache distribuído: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpa todo o cache distribuído."""
        try:
            await self.redis.flushdb()
            self.stats = CacheStats()
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache distribuído: {str(e)}")
            return False
    
    def get_stats(self) -> CacheStats:
        """Retorna estatísticas do cache distribuído."""
        try:
            info = self.redis.info()
            
            self.stats.size = info["used_memory"]
            self.stats.items = info["db0"]["keys"]
            self.stats.evictions = info["evicted_keys"]
            
            return self.stats
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas do cache: {str(e)}")
            return self.stats

class CacheManager:
    """Gerenciador principal de cache."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Inicializa caches
        self.local_cache = LRUCache(
            size=self._parse_size(config["local"]["tamanho"]),
            ttl=config["local"]["ttl"]
        )
        
        self.distributed_cache = DistributedCache(
            config["distribuido"]
        )
        
        # Configuração adaptativa
        self.adaptive_config = config["adaptativo"]
        self.learning_enabled = self.adaptive_config["aprendizado"]
        self.optimization_enabled = self.adaptive_config["otimizacao"]
        
        # Métricas adaptativas
        self.adaptive_metrics = {
            "hit_rates": [],
            "latencies": [],
            "patterns": {}
        }
    
    def _parse_size(self, size_str: str) -> int:
        """Converte string de tamanho para bytes."""
        units = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 * 1024,
            "GB": 1024 * 1024 * 1024
        }
        
        size = size_str.upper()
        for unit, multiplier in units.items():
            if size.endswith(unit):
                return int(size[:-len(unit)]) * multiplier
        
        return int(size)  # Assume bytes se não houver unidade
    
    async def get(self, key: str) -> Optional[Any]:
        """Recupera um item do cache."""
        try:
            start_time = time.time()
            
            # Tenta cache local
            value = await self.local_cache.get(key)
            if value is not None:
                await self._record_metrics("local", "hit", time.time() - start_time)
                return value
            
            # Tenta cache distribuído
            value = await self.distributed_cache.get(key)
            if value is not None:
                # Atualiza cache local
                await self.local_cache.set(key, value)
                await self._record_metrics("distributed", "hit", time.time() - start_time)
                return value
            
            await self._record_metrics("all", "miss", time.time() - start_time)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao recuperar do cache: {str(e)}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Armazena um item no cache."""
        try:
            # Armazena em ambos os caches
            local_success = await self.local_cache.set(key, value, ttl)
            dist_success = await self.distributed_cache.set(key, value, ttl)
            
            return local_success and dist_success
            
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Remove um item do cache."""
        try:
            # Remove de ambos os caches
            local_success = await self.local_cache.delete(key)
            dist_success = await self.distributed_cache.delete(key)
            
            return local_success and dist_success
            
        except Exception as e:
            logger.error(f"Erro ao remover do cache: {str(e)}")
            return False
    
    async def clear(self) -> bool:
        """Limpa todos os caches."""
        try:
            # Limpa ambos os caches
            local_success = await self.local_cache.clear()
            dist_success = await self.distributed_cache.clear()
            
            return local_success and dist_success
            
        except Exception as e:
            logger.error(f"Erro ao limpar caches: {str(e)}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas combinadas dos caches."""
        return {
            "local": self.local_cache.get_stats().__dict__,
            "distributed": self.distributed_cache.get_stats().__dict__,
            "adaptive": self.adaptive_metrics
        }
    
    async def _record_metrics(
        self,
        cache_type: str,
        operation: str,
        latency: float
    ):
        """Registra métricas para otimização adaptativa."""
        if not self.learning_enabled:
            return
            
        # Registra latência
        self.adaptive_metrics["latencies"].append({
            "cache_type": cache_type,
            "operation": operation,
            "latency": latency,
            "timestamp": time.time()
        })
        
        # Limita histórico de latências
        if len(self.adaptive_metrics["latencies"]) > 1000:
            self.adaptive_metrics["latencies"] = self.adaptive_metrics["latencies"][-1000:]
        
        # Calcula taxa de hit
        if operation in ["hit", "miss"]:
            self.adaptive_metrics["hit_rates"].append({
                "cache_type": cache_type,
                "is_hit": operation == "hit",
                "timestamp": time.time()
            })
            
            # Limita histórico de hit rates
            if len(self.adaptive_metrics["hit_rates"]) > 1000:
                self.adaptive_metrics["hit_rates"] = self.adaptive_metrics["hit_rates"][-1000:]
    
    async def optimize(self):
        """Otimiza os caches baseado em métricas."""
        if not self.optimization_enabled:
            return
            
        try:
            # Analisa padrões de acesso
            patterns = await self._analyze_patterns()
            
            # Ajusta TTLs baseado em padrões
            if patterns["high_churn"]:
                await self.adjust_ttl(increment=-300)  # Reduz TTL em 5 minutos
            elif patterns["stable_hits"]:
                await self.adjust_ttl(increment=300)   # Aumenta TTL em 5 minutos
            
            # Ajusta tamanho do cache local
            if patterns["memory_pressure"]:
                await self._reduce_local_cache()
            elif patterns["cache_underutil"]:
                await self._increase_local_cache()
            
        except Exception as e:
            logger.error(f"Erro durante otimização: {str(e)}")
    
    async def _analyze_patterns(self) -> Dict[str, bool]:
        """Analisa padrões nos dados de métricas."""
        try:
            recent_rates = self.adaptive_metrics["hit_rates"][-100:]
            recent_latencies = self.adaptive_metrics["latencies"][-100:]
            
            # Calcula métricas
            hit_rate = sum(1 for r in recent_rates if r["is_hit"]) / len(recent_rates)
            avg_latency = sum(l["latency"] for l in recent_latencies) / len(recent_latencies)
            
            return {
                "high_churn": hit_rate < 0.3,  # Alta taxa de miss
                "stable_hits": hit_rate > 0.7,  # Alta taxa de hit
                "memory_pressure": avg_latency > 0.1,  # Latência alta
                "cache_underutil": hit_rate < 0.5 and avg_latency < 0.01  # Subutilizado
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar padrões: {str(e)}")
            return {
                "high_churn": False,
                "stable_hits": False,
                "memory_pressure": False,
                "cache_underutil": False
            }
    
    async def adjust_ttl(self, increment: int):
        """Ajusta o TTL dos caches."""
        try:
            # Ajusta TTL local
            self.config["local"]["ttl"] = max(
                60,  # Mínimo 1 minuto
                min(
                    86400,  # Máximo 24 horas
                    self.config["local"]["ttl"] + increment
                )
            )
            
            # Ajusta TTL distribuído
            self.config["distribuido"]["ttl"] = max(
                300,  # Mínimo 5 minutos
                min(
                    604800,  # Máximo 7 dias
                    self.config["distribuido"]["ttl"] + increment
                )
            )
            
            logger.info(f"TTLs ajustados: local={self.config['local']['ttl']}s, "
                       f"distribuído={self.config['distribuido']['ttl']}s")
            
        except Exception as e:
            logger.error(f"Erro ao ajustar TTL: {str(e)}")
    
    async def _reduce_local_cache(self):
        """Reduz o tamanho do cache local."""
        try:
            current_size = self._parse_size(self.config["local"]["tamanho"])
            new_size = int(current_size * 0.8)  # Reduz 20%
            
            self.config["local"]["tamanho"] = f"{new_size}B"
            await self.local_cache.clear()  # Reinicia com novo tamanho
            
            logger.info(f"Cache local reduzido para {new_size} bytes")
            
        except Exception as e:
            logger.error(f"Erro ao reduzir cache local: {str(e)}")
    
    async def _increase_local_cache(self):
        """Aumenta o tamanho do cache local."""
        try:
            current_size = self._parse_size(self.config["local"]["tamanho"])
            new_size = int(current_size * 1.2)  # Aumenta 20%
            
            self.config["local"]["tamanho"] = f"{new_size}B"
            logger.info(f"Cache local aumentado para {new_size} bytes")
            
        except Exception as e:
            logger.error(f"Erro ao aumentar cache local: {str(e)}")
    
    async def check_health(self) -> bool:
        """Verifica a saúde dos caches."""
        try:
            # Verifica métricas recentes
            stats = await self.get_stats()
            
            # Verifica hit rate
            total_ops = stats["local"]["hits"] + stats["local"]["misses"]
            if total_ops > 0:
                hit_rate = stats["local"]["hits"] / total_ops
                if hit_rate < 0.1:  # Menos de 10% de hit rate
                    logger.warning(f"Hit rate muito baixo: {hit_rate:.2%}")
                    return False
            
            # Verifica evictions
            if stats["local"]["evictions"] > 1000:
                logger.warning("Alto número de evictions")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao verificar saúde do cache: {str(e)}")
            return False
    
    def close(self):
        """Fecha as conexões dos caches."""
        try:
            # Fecha cache distribuído
            self.distributed_cache.redis.close()
            logger.info("Conexões de cache fechadas com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao fechar conexões de cache: {str(e)}")
            raise
