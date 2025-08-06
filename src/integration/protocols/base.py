from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class BaseProtocol(ABC):
    """Interface base para todos os protocolos de comunicação."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        
        # Estado interno
        self._state = {
            "status": "initialized",
            "active": False,
            "last_error": None,
            "metrics": {}
        }
        
        # Configuração específica
        self._setup_config()
    
    def _setup_config(self):
        """Configura parâmetros específicos do protocolo."""
        self.tipo = self.config["tipo"]
        self.formato = self.config["formato"]
        self.timeout = self.config.get("timeout", 5000)  # ms
        self.retry_count = self.config.get("retry", 3)
    
    @abstractmethod
    async def send(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Envia dados através do protocolo."""
        pass
    
    @abstractmethod
    async def receive(self) -> Dict[str, Any]:
        """Recebe dados através do protocolo."""
        pass
    
    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """Valida os dados para o protocolo."""
        pass
    
    @abstractmethod
    async def check_health(self) -> bool:
        """Verifica a saúde do protocolo."""
        pass
    
    async def _send_with_retry(
        self,
        data: Dict[str, Any],
        retry_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """Envia dados com retry em caso de falha."""
        if retry_count is None:
            retry_count = self.retry_count
            
        last_error = None
        for attempt in range(retry_count + 1):
            try:
                if attempt > 0:
                    await asyncio.sleep(self._calculate_backoff(attempt))
                    logger.info(
                        f"Tentativa {attempt + 1} de {retry_count + 1} "
                        f"para envio em {self.name}"
                    )
                
                return await self.send(data)
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Erro na tentativa {attempt + 1} de envio em {self.name}: {str(e)}"
                )
                
                if attempt == retry_count:
                    logger.error(
                        f"Todas as tentativas de envio falharam em {self.name}"
                    )
                    self._state["last_error"] = str(e)
                    raise last_error
    
    async def _receive_with_timeout(
        self,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """Recebe dados com timeout."""
        if timeout is None:
            timeout = self.timeout / 1000  # Converte ms para segundos
            
        try:
            return await asyncio.wait_for(self.receive(), timeout=timeout)
            
        except asyncio.TimeoutError:
            error_msg = f"Timeout ao receber dados em {self.name}"
            logger.error(error_msg)
            self._state["last_error"] = error_msg
            raise
            
        except Exception as e:
            logger.error(f"Erro ao receber dados em {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            raise
    
    def _calculate_backoff(self, attempt: int) -> float:
        """Calcula o tempo de espera para retry usando exponential backoff."""
        base_delay = 0.1  # 100ms
        max_delay = 5.0   # 5s
        
        delay = min(base_delay * (2 ** attempt), max_delay)
        jitter = delay * 0.1  # 10% de jitter
        
        import random
        return delay + random.uniform(-jitter, jitter)
    
    async def _validate_format(self, data: Dict[str, Any]) -> bool:
        """Validação básica do formato dos dados."""
        try:
            if not isinstance(data, dict):
                return False
                
            if self.formato == "json":
                import json
                json.dumps(data)  # Testa serialização
                
            elif self.formato == "proto3":
                # Implementar validação específica para protobuf
                pass
                
            elif self.formato == "binary":
                # Implementar validação específica para binário
                pass
                
            return True
            
        except Exception as e:
            logger.error(
                f"Erro na validação de formato em {self.name}: {str(e)}"
            )
            return False
    
    def increase_timeout(self, factor: float = 1.5):
        """Aumenta o timeout do protocolo."""
        self.timeout = int(self.timeout * factor)
        logger.info(
            f"Timeout aumentado em {self.name} para {self.timeout}ms"
        )
    
    def get_state(self) -> Dict[str, Any]:
        """Retorna o estado atual do protocolo."""
        return {
            **self._state,
            "config": {
                "tipo": self.tipo,
                "formato": self.formato,
                "timeout": self.timeout,
                "retry_count": self.retry_count
            }
        }
    
    async def initialize(self) -> bool:
        """Inicializa o protocolo."""
        try:
            self._state["active"] = True
            self._state["status"] = "active"
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            return False
    
    async def shutdown(self) -> bool:
        """Desliga o protocolo de forma segura."""
        try:
            self._state["active"] = False
            self._state["status"] = "shutdown"
            return True
            
        except Exception as e:
            logger.error(f"Erro ao desligar {self.name}: {str(e)}")
            self._state["last_error"] = str(e)
            return False
