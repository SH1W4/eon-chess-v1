from typing import Any, Dict, Optional, List
from ..base_connector import BaseConnector
from .narrative_state import NarrativeState, StoryElement, NarrativeFlow

class NarrativeConnector(BaseConnector):
    """
    Conector para o sistema Narrativo.
    Gerencia o fluxo narrativo, histórias e elementos narrativos do sistema.
    """
    
    def __init__(self):
        super().__init__()
        # Inicializa o gerenciador de estado narrativo
        self._narrative_state = NarrativeState()
        # Cache de elementos narrativos frequentes
        self._story_cache: Dict[str, StoryElement] = {}
        # Fluxos narrativos ativos
        self._active_flows: List[NarrativeFlow] = []
        
    async def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Inicializa o conector narrativo com configurações específicas.
        Args:
            config: Configurações incluindo elementos narrativos iniciais,
                   fluxos predefinidos e parâmetros de storytelling.
        """
        try:
            if config:
                # Configura o estado narrativo com os parâmetros fornecidos
                await self._narrative_state.configure(config)
                # Inicializa cache de histórias se especificado
                if "story_cache" in config:
                    self._story_cache = config["story_cache"]
                # Configura fluxos narrativos iniciais
                if "initial_flows" in config:
                    self._active_flows = [
                        NarrativeFlow(**flow) 
                        for flow in config["initial_flows"]
                    ]
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Erro na inicialização do conector narrativo: {e}")
            return False
            
    async def connect(self) -> bool:
        """
        Estabelece conexão com o sistema narrativo.
        Prepara os fluxos narrativos e elementos de história.
        """
        if not self._is_initialized:
            raise RuntimeError("Conector narrativo não inicializado")
        try:
            # Verifica recursos narrativos
            resources_available = await self._check_narrative_resources()
            if not resources_available:
                return False
                
            # Inicializa sistema de storytelling
            await self._narrative_state.initialize_storytelling()
            
            # Prepara fluxos narrativos
            await self._prepare_narrative_flows()
            
            return True
        except Exception as e:
            print(f"Erro na conexão narrativa: {e}")
            return False
            
    async def disconnect(self) -> bool:
        """
        Desconecta do sistema narrativo.
        Salva o estado atual das histórias e fluxos.
        """
        try:
            # Salva estado narrativo atual
            await self._narrative_state.save_checkpoint()
            # Finaliza fluxos narrativos ativos
            await self._finalize_active_flows()
            # Limpa cache de histórias
            self._story_cache.clear()
            return True
        except Exception as e:
            print(f"Erro na desconexão narrativa: {e}")
            return False
            
    async def get_state(self) -> Dict[str, Any]:
        """
        Retorna o estado atual do sistema narrativo.
        Inclui histórias ativas, fluxos e elementos narrativos.
        """
        return await self._narrative_state.get_current_state()
        
    async def update_state(self, new_state: Dict[str, Any]) -> bool:
        """
        Atualiza o estado do sistema narrativo.
        Args:
            new_state: Novo estado narrativo a ser aplicado, incluindo
                      novas histórias, fluxos e elementos narrativos.
        """
        try:
            # Valida o novo estado narrativo
            if await self._validate_narrative_state(new_state):
                await self._narrative_state.update(new_state)
                # Atualiza cache se necessário
                if "story_cache_update" in new_state:
                    await self._update_story_cache(new_state["story_cache_update"])
                return True
            return False
        except Exception as e:
            print(f"Erro na atualização do estado narrativo: {e}")
            return False
            
    async def verify_health(self) -> bool:
        """
        Verifica a saúde do sistema narrativo.
        Analisa coerência das histórias e fluxos narrativos.
        """
        try:
            # Verifica saúde do estado narrativo
            state_health = await self._narrative_state.is_healthy()
            # Verifica coerência dos fluxos
            flow_health = await self._verify_narrative_flows()
            # Verifica integridade do cache
            cache_health = await self._verify_story_cache()
            
            return all([state_health, flow_health, cache_health])
        except Exception as e:
            print(f"Erro na verificação de saúde narrativa: {e}")
            return False
            
    async def add_story_element(self, element: StoryElement) -> bool:
        """
        Adiciona um novo elemento à narrativa atual.
        Args:
            element: Elemento narrativo a ser adicionado.
        """
        try:
            return await self._narrative_state.add_element(element)
        except Exception as e:
            print(f"Erro ao adicionar elemento narrativo: {e}")
            return False
            
    async def create_narrative_flow(self, flow: NarrativeFlow) -> bool:
        """
        Cria um novo fluxo narrativo.
        Args:
            flow: Configuração do novo fluxo narrativo.
        """
        try:
            if await self._validate_narrative_flow(flow):
                self._active_flows.append(flow)
                return True
            return False
        except Exception as e:
            print(f"Erro ao criar fluxo narrativo: {e}")
            return False
            
    async def _check_narrative_resources(self) -> bool:
        """Verifica disponibilidade de recursos narrativos."""
        try:
            # Implementar verificações específicas
            return True
        except Exception:
            return False
            
    async def _prepare_narrative_flows(self) -> None:
        """Prepara os fluxos narrativos do sistema."""
        try:
            for flow in self._active_flows:
                await flow.prepare()
        except Exception as e:
            print(f"Erro ao preparar fluxos narrativos: {e}")
            
    async def _finalize_active_flows(self) -> None:
        """Finaliza os fluxos narrativos ativos."""
        try:
            for flow in self._active_flows:
                await flow.finalize()
            self._active_flows.clear()
        except Exception as e:
            print(f"Erro ao finalizar fluxos narrativos: {e}")
            
    async def _validate_narrative_state(self, state: Dict[str, Any]) -> bool:
        """Valida um novo estado narrativo."""
        try:
            # Implementar validações específicas
            return True
        except Exception:
            return False
            
    async def _validate_narrative_flow(self, flow: NarrativeFlow) -> bool:
        """Valida um novo fluxo narrativo."""
        try:
            # Implementar validações específicas
            return True
        except Exception:
            return False
            
    async def _verify_narrative_flows(self) -> bool:
        """Verifica a saúde dos fluxos narrativos."""
        try:
            return all(flow.is_healthy() for flow in self._active_flows)
        except Exception:
            return False
            
    async def _verify_story_cache(self) -> bool:
        """Verifica a integridade do cache de histórias."""
        try:
            # Implementar verificações específicas
            return True
        except Exception:
            return False
            
    async def _update_story_cache(self, cache_update: Dict[str, Any]) -> None:
        """Atualiza o cache de histórias."""
        try:
            self._story_cache.update(cache_update)
        except Exception as e:
            print(f"Erro ao atualizar cache de histórias: {e}")
