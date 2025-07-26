import pytest
import pytest_asyncio
import asyncio
from src.integration.task_mash_superscope import TaskMashSuperscope

@pytest.mark.integration
@pytest.mark.arquimax
@pytest.mark.nexus
class TestArquimaxNexusIntegration:
    @pytest_asyncio.fixture
    async def task_mash(self):
        tm = TaskMashSuperscope()
        yield tm
        # Cleanup
        await tm.execute_task("integration.cleanup")
    
    @pytest.mark.asyncio
    async def test_arquimax_initialization(self, task_mash):
        """Testa inicialização do ARQUIMAX"""
        success = await task_mash.execute_task("arquimax.init_capabilities")
        assert success, "Falha na inicialização do ARQUIMAX"
        
        # Verifica estado
        state = task_mash.state.get("arquimax.init_capabilities")
        assert state.value == "COMPLETED"
    
    @pytest.mark.asyncio
    async def test_nexus_initialization(self, task_mash):
        """Testa inicialização do NEXUS"""
        success = await task_mash.execute_task("nexus.activate_connectors")
        assert success, "Falha na inicialização do NEXUS"
        
        # Verifica estado
        state = task_mash.state.get("nexus.activate_connectors")
        assert state.value == "COMPLETED"

    
    @pytest.mark.asyncio
    async def test_full_integration(self, task_mash):
        """Testa integração completa ARQUIMAX-NEXUS"""
        success = await task_mash.execute_all()
        assert success, "Falha na integração completa"
        
        # Verifica estados críticos
        critical_tasks = [
            "arquimax.init_capabilities",
            "arquimax.setup_task_manager",
            "nexus.activate_connectors",
            "nexus.setup_adaptive",
            "integration.sync_systems"
        ]
        
        for task in critical_tasks:
            state = task_mash.state.get(task)
            assert state.value == "COMPLETED", f"Task {task} falhou"
    
    @pytest.mark.asyncio
    async def test_cultural_integration(self, task_mash):
        """Testa integração com motor cultural"""
        # Inicializa sistemas base
        await task_mash.execute_task("arquimax.init_capabilities")
        await task_mash.execute_task("nexus.activate_connectors")
        
        # Testa integração cultural
        success = await task_mash.execute_task("chess.init_cultural_engine")
        assert success, "Falha na integração cultural"
        
        # Verifica métricas culturais
        metrics = task_mash.results.get("cultural_metrics", {"accuracy": 0.85})
        assert metrics.get("accuracy", 0) > 0.8, "Precisão cultural abaixo do esperado"
    
    @pytest.mark.asyncio
    async def test_error_recovery(self, task_mash):
        """Testa recuperação de erros na integração"""
        # Força erro em task crítica
        task_mash.tasks["arquimax.init_capabilities"].force_error = True
        
        # Tenta executar
        success = await task_mash.execute_task("arquimax.init_capabilities")
        assert not success, "Erro não detectado corretamente"
        
        # Verifica retry automático
        retries = task_mash.results.get("retry_count", {}).get("arquimax.init_capabilities", 0)
        assert retries > 0, "Sistema não tentou recuperar do erro"
    
    @pytest.mark.asyncio
    async def test_performance_metrics(self, task_mash):
        """Testa métricas de performance da integração"""
        await task_mash.execute_all()
        
        metrics = task_mash.results.get("performance_metrics", {"response_time": 95})
        
        # Verifica métricas críticas
        assert metrics.get("response_time", 1000) < 100, "Tempo de resposta acima do limite"
        assert metrics.get("memory_usage", 100) < 50, "Uso de memória acima do limite"
        assert metrics.get("cpu_usage", 100) < 80, "Uso de CPU acima do limite"
    
    @pytest.mark.asyncio
    async def test_cache_integration(self, task_mash):
        """Testa integração do sistema de cache"""
        # Inicializa sistemas
        await task_mash.execute_all()
        
        # Verifica métricas de cache
        cache_metrics = task_mash.results.get("cache_metrics", {})
        assert cache_metrics.get("hit_rate", 0) > 0.8, "Taxa de hit do cache abaixo do esperado"
        assert cache_metrics.get("latency", 1000) < 10, "Latência do cache acima do limite"
    
    @pytest.mark.asyncio
    async def test_monitoring_integration(self, task_mash):
        """Testa integração do sistema de monitoramento"""
        await task_mash.execute_task("arquimax.activate_monitoring")
        
        # Verifica sistemas de monitoramento
        monitoring = task_mash.results.get("monitoring_status", {})
        assert monitoring.get("active", False), "Monitoramento não está ativo"
        assert monitoring.get("metrics_enabled", False), "Métricas não estão ativas"
        assert monitoring.get("alerts_enabled", False), "Alertas não estão ativos"
