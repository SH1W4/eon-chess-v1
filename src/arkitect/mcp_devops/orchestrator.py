import logging
import asyncio
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger('arkitect.mcp_devops')

class SystemType(Enum):
    ARQUIMAX = "arquimax"
    NEXUS = "nexus"

class SystemState(Enum):
    INITIALIZING = "initializing"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"
    STOPPED = "stopped"

class DevOpsOrchestrator:
    def __init__(self):
        self.systems = {}
        self.workflow_engine = None
        self.bridge = None
        self.metrics = {}
        self.state = {}
        logger.info("Inicializando DevOps Orchestrator")

    async def initialize(self):
        """Inicializa o orquestrador e seus componentes"""
        try:
            logger.info("Iniciando inicialização do MCP DevOps")
            
            # Inicializa workflow engine
            from .workflow_engine import WorkflowEngine
            self.workflow_engine = WorkflowEngine()
            await self.workflow_engine.initialize()

            # Inicializa system bridge
            from .system_bridge import SystemBridge
            self.bridge = SystemBridge()
            await self.bridge.initialize()

            # Registra sistemas
            await self._register_systems()

            # Inicia monitoramento
            asyncio.create_task(self._monitor_systems())

            logger.info("MCP DevOps inicializado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro na inicialização do MCP DevOps: {e}")
            return False

    async def _register_systems(self):
        """Registra os sistemas gerenciados"""
        systems_config = {
            SystemType.ARQUIMAX: {
                'capabilities': ['task_management', 'monitoring', 'metrics'],
                'workflows': ['init_capabilities', 'setup_task_manager', 'activate_monitoring'],
                'dependencies': []
            },
            SystemType.NEXUS: {
                'capabilities': ['document_sync', 'connectors', 'adaptive_execution'],
                'workflows': ['activate_connectors', 'setup_adaptive_execution'],
                'dependencies': [SystemType.ARQUIMAX]
            }
        }

        for system_type, config in systems_config.items():
            await self.register_system(system_type, config)

    async def register_system(self, system_type: SystemType, config: Dict):
        """Registra um novo sistema"""
        self.systems[system_type] = {
            'config': config,
            'state': SystemState.STOPPED,
            'last_update': datetime.now().isoformat(),
            'metrics': {},
            'active_workflows': []
        }
        logger.info(f"Sistema {system_type.value} registrado")

    async def start_system(self, system_type: SystemType) -> bool:
        """Inicia um sistema específico"""
        if system_type not in self.systems:
            raise ValueError(f"Sistema {system_type.value} não registrado")

        system = self.systems[system_type]
        
        # Verifica dependências
        for dep in system['config']['dependencies']:
            if self.systems[dep]['state'] != SystemState.ACTIVE:
                logger.error(f"Dependência {dep.value} não está ativa")
                return False

        try:
            # Atualiza estado
            system['state'] = SystemState.INITIALIZING
            
            # Executa workflows de inicialização
            for workflow in system['config']['workflows']:
                success = await self.workflow_engine.execute_workflow(
                    system_type, workflow, {}
                )
                if not success:
                    raise Exception(f"Falha no workflow {workflow}")

            # Ativa sistema no bridge
            await self.bridge.activate_system(system_type)
            
            # Atualiza estado
            system['state'] = SystemState.ACTIVE
            system['last_update'] = datetime.now().isoformat()
            
            logger.info(f"Sistema {system_type.value} iniciado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar {system_type.value}: {e}")
            system['state'] = SystemState.ERROR
            return False

    async def stop_system(self, system_type: SystemType) -> bool:
        """Para um sistema específico"""
        if system_type not in self.systems:
            raise ValueError(f"Sistema {system_type.value} não registrado")

        system = self.systems[system_type]
        
        try:
            # Verifica dependentes
            for other_type, other_system in self.systems.items():
                if system_type in other_system['config']['dependencies']:
                    if other_system['state'] == SystemState.ACTIVE:
                        await self.stop_system(other_type)

            # Desativa sistema no bridge
            await self.bridge.deactivate_system(system_type)
            
            # Atualiza estado
            system['state'] = SystemState.STOPPED
            system['last_update'] = datetime.now().isoformat()
            
            logger.info(f"Sistema {system_type.value} parado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao parar {system_type.value}: {e}")
            system['state'] = SystemState.ERROR
            return False

    async def execute_workflow(self, system_type: SystemType, workflow: str, params: Dict) -> bool:
        """Executa um workflow específico em um sistema"""
        if system_type not in self.systems:
            raise ValueError(f"Sistema {system_type.value} não registrado")

        system = self.systems[system_type]
        if system['state'] != SystemState.ACTIVE:
            raise ValueError(f"Sistema {system_type.value} não está ativo")

        try:
            success = await self.workflow_engine.execute_workflow(
                system_type, workflow, params
            )
            if success:
                system['active_workflows'].append(workflow)
            return success
        except Exception as e:
            logger.error(f"Erro ao executar workflow {workflow} em {system_type.value}: {e}")
            return False

    async def get_system_status(self, system_type: Optional[SystemType] = None) -> Dict:
        """Obtém status de um ou todos os sistemas"""
        if system_type:
            if system_type not in self.systems:
                raise ValueError(f"Sistema {system_type.value} não registrado")
            return self._get_single_system_status(system_type)
        
        return {
            sys_type.value: self._get_single_system_status(sys_type)
            for sys_type in self.systems.keys()
        }

    def _get_single_system_status(self, system_type: SystemType) -> Dict:
        """Obtém status detalhado de um sistema"""
        system = self.systems[system_type]
        return {
            'state': system['state'].value,
            'last_update': system['last_update'],
            'active_workflows': system['active_workflows'],
            'metrics': system['metrics'],
            'capabilities': system['config']['capabilities']
        }

    async def _monitor_systems(self):
        """Monitora estado dos sistemas continuamente"""
        while True:
            try:
                for system_type, system in self.systems.items():
                    if system['state'] == SystemState.ACTIVE:
                        # Atualiza métricas
                        metrics = await self.bridge.get_system_metrics(system_type)
                        system['metrics'] = metrics

                        # Verifica saúde
                        health = await self._check_system_health(system_type)
                        if not health['healthy']:
                            logger.warning(f"Sistema {system_type.value} degradado: {health['reason']}")
                            system['state'] = SystemState.DEGRADED
                            
                            # Tenta recuperar
                            await self._attempt_recovery(system_type)

                await asyncio.sleep(30)  # Intervalo de monitoramento
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                await asyncio.sleep(60)  # Intervalo maior em caso de erro

    async def _check_system_health(self, system_type: SystemType) -> Dict:
        """Verifica saúde de um sistema"""
        system = self.systems[system_type]
        metrics = system['metrics']

        # Implementar verificações específicas aqui
        return {
            'healthy': True,
            'reason': None
        }

    async def _attempt_recovery(self, system_type: SystemType):
        """Tenta recuperar um sistema degradado"""
        try:
            # Para o sistema
            await self.stop_system(system_type)
            await asyncio.sleep(5)  # Aguarda um pouco
            
            # Reinicia o sistema
            success = await self.start_system(system_type)
            if success:
                logger.info(f"Sistema {system_type.value} recuperado com sucesso")
            else:
                logger.error(f"Falha na recuperação do sistema {system_type.value}")
        except Exception as e:
            logger.error(f"Erro na tentativa de recuperação de {system_type.value}: {e}")
