from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import asyncio
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RecoveryAction:
    """Ação de recuperação do sistema."""
    name: str
    description: str
    action: Callable
    severity: str  # 'low', 'medium', 'high', 'critical'
    timeout: int  # segundos
    max_retries: int

@dataclass
class RecoveryAttempt:
    """Tentativa de recuperação."""
    action: RecoveryAction
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    error: Optional[str] = None

class RecoveryManager:
    """Gerenciador de recuperação automática."""
    
    def __init__(self):
        self.recovery_history: List[RecoveryAttempt] = []
        self.active_recoveries: Dict[str, RecoveryAttempt] = {}
        
        # Configurações padrão
        self.config = {
            "max_concurrent_recoveries": 3,
            "retry_delay": 5,  # segundos
            "escalation_threshold": 3,  # tentativas antes de escalar
            "health_check_interval": 60  # segundos
        }
        
        # Ações de recuperação padrão
        self.actions = {
            "state_reset": RecoveryAction(
                name="state_reset",
                description="Reinicia o estado do sistema para um estado conhecido",
                action=self._reset_state,
                severity="medium",
                timeout=30,
                max_retries=3
            ),
            "cache_cleanup": RecoveryAction(
                name="cache_cleanup",
                description="Limpa e reinicializa caches",
                action=self._cleanup_cache,
                severity="low",
                timeout=15,
                max_retries=5
            ),
            "connection_reset": RecoveryAction(
                name="connection_reset",
                description="Reinicia conexões do sistema",
                action=self._reset_connections,
                severity="high",
                timeout=45,
                max_retries=2
            ),
            "emergency_shutdown": RecoveryAction(
                name="emergency_shutdown",
                description="Desliga o sistema de forma segura",
                action=self._emergency_shutdown,
                severity="critical",
                timeout=60,
                max_retries=1
            )
        }
    
    async def attempt_recovery(self, error: Any, context: Dict[str, Any]) -> bool:
        """Tenta recuperar o sistema de um erro."""
        logger.info(f"Iniciando tentativa de recuperação para erro: {error}")
        
        try:
            # Analisa o erro e escolhe ação apropriada
            action = self._select_recovery_action(error, context)
            
            # Verifica se já há muitas recuperações ativas
            if len(self.active_recoveries) >= self.config["max_concurrent_recoveries"]:
                logger.warning("Número máximo de recuperações concorrentes atingido")
                return False
            
            # Inicia tentativa de recuperação
            attempt = RecoveryAttempt(
                action=action,
                start_time=datetime.now()
            )
            
            self.active_recoveries[action.name] = attempt
            
            # Executa ação com timeout
            try:
                async with asyncio.timeout(action.timeout):
                    success = await action.action(context)
                    
                attempt.success = success
                attempt.end_time = datetime.now()
                
                if success:
                    logger.info(f"Recuperação {action.name} bem-sucedida")
                else:
                    logger.warning(f"Recuperação {action.name} falhou")
                    
            except asyncio.TimeoutError:
                attempt.error = "Timeout"
                attempt.success = False
                attempt.end_time = datetime.now()
                logger.error(f"Timeout na recuperação {action.name}")
            
            # Registra tentativa
            self.recovery_history.append(attempt)
            del self.active_recoveries[action.name]
            
            # Se falhou, tenta escalar
            if not attempt.success:
                return await self._handle_recovery_failure(error, context, attempt)
                
            return attempt.success
            
        except Exception as e:
            logger.error(f"Erro durante recuperação: {e}")
            return False
    
    def _select_recovery_action(self, error: Any, context: Dict[str, Any]) -> RecoveryAction:
        """Seleciona a ação de recuperação mais apropriada."""
        # Analisa o tipo de erro
        if "state_corruption" in str(error).lower():
            return self.actions["state_reset"]
        elif "cache" in str(error).lower():
            return self.actions["cache_cleanup"]
        elif "connection" in str(error).lower():
            return self.actions["connection_reset"]
        elif "critical" in str(error).lower():
            return self.actions["emergency_shutdown"]
        
        # Padrão para erros desconhecidos
        return self.actions["state_reset"]
    
    async def _handle_recovery_failure(
        self,
        error: Any,
        context: Dict[str, Any],
        failed_attempt: RecoveryAttempt
    ) -> bool:
        """Lida com falha na recuperação."""
        logger.warning(f"Recuperação falhou: {failed_attempt.action.name}")
        
        # Verifica número de tentativas para esta ação
        action_attempts = [
            a for a in self.recovery_history
            if a.action.name == failed_attempt.action.name
        ]
        
        if len(action_attempts) >= failed_attempt.action.max_retries:
            logger.error(f"Máximo de tentativas atingido para {failed_attempt.action.name}")
            
            # Tenta escalar para próximo nível
            next_action = self._get_escalated_action(failed_attempt.action)
            if next_action:
                logger.info(f"Escalando para ação {next_action.name}")
                await asyncio.sleep(self.config["retry_delay"])
                return await self.attempt_recovery(error, context)
            
            return False
            
        # Aguarda antes de tentar novamente
        await asyncio.sleep(self.config["retry_delay"])
        return await self.attempt_recovery(error, context)
    
    def _get_escalated_action(self, current_action: RecoveryAction) -> Optional[RecoveryAction]:
        """Retorna próxima ação na escala de severidade."""
        severity_levels = ["low", "medium", "high", "critical"]
        current_level = severity_levels.index(current_action.severity)
        
        if current_level + 1 >= len(severity_levels):
            return None
            
        next_level = severity_levels[current_level + 1]
        
        # Encontra ação com próximo nível de severidade
        for action in self.actions.values():
            if action.severity == next_level:
                return action
                
        return None
    
    async def _reset_state(self, context: Dict[str, Any]) -> bool:
        """Reinicia o estado do sistema."""
        try:
            if "state" in context:
                context["state"].clear()
                context["state"]["status"] = "reset"
                context["state"]["reset_time"] = datetime.now().isoformat()
            return True
        except Exception as e:
            logger.error(f"Erro ao resetar estado: {e}")
            return False
    
    async def _cleanup_cache(self, context: Dict[str, Any]) -> bool:
        """Limpa e reinicializa caches."""
        try:
            if "cache" in context:
                context["cache"].clear()
            return True
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False
    
    async def _reset_connections(self, context: Dict[str, Any]) -> bool:
        """Reinicia conexões do sistema."""
        try:
            if "connections" in context:
                for conn in context["connections"].values():
                    await conn.disconnect()
                    await conn.connect()
            return True
        except Exception as e:
            logger.error(f"Erro ao resetar conexões: {e}")
            return False
    
    async def _emergency_shutdown(self, context: Dict[str, Any]) -> bool:
        """Desliga o sistema de forma segura."""
        try:
            # Salva estado
            if "state" in context:
                await self._save_state(context["state"])
                
            # Fecha conexões
            if "connections" in context:
                for conn in context["connections"].values():
                    await conn.disconnect()
                    
            # Limpa recursos
            if "cache" in context:
                context["cache"].clear()
                
            return True
        except Exception as e:
            logger.error(f"Erro no shutdown de emergência: {e}")
            return False
    
    async def _save_state(self, state: Dict[str, Any]):
        """Salva o estado atual do sistema."""
        # Implementar salvamento de estado
        pass
    
    def get_recovery_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de recuperação."""
        if not self.recovery_history:
            return {
                "total_attempts": 0,
                "success_rate": 0.0,
                "average_duration": 0.0,
                "by_action": {}
            }
            
        total = len(self.recovery_history)
        successful = sum(1 for a in self.recovery_history if a.success)
        
        # Calcula estatísticas por ação
        action_stats = {}
        for action_name in self.actions:
            action_attempts = [
                a for a in self.recovery_history
                if a.action.name == action_name
            ]
            
            if action_attempts:
                action_successful = sum(1 for a in action_attempts if a.success)
                action_stats[action_name] = {
                    "attempts": len(action_attempts),
                    "success_rate": action_successful / len(action_attempts),
                    "average_duration": sum(
                        (a.end_time - a.start_time).total_seconds()
                        for a in action_attempts
                    ) / len(action_attempts)
                }
        
        return {
            "total_attempts": total,
            "success_rate": successful / total,
            "average_duration": sum(
                (a.end_time - a.start_time).total_seconds()
                for a in self.recovery_history
            ) / total,
            "by_action": action_stats
        }
