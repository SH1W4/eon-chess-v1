import asyncio
import logging
from core.orchestration.aeon_orchestrator import AEONOrchestrator

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aeon_execution.log'),
        logging.StreamHandler()
    ]
)

async def main():
    """Função principal de execução do AEON Chess"""
    logger = logging.getLogger(__name__)
    logger.info("Iniciando AEON Chess System")

    try:
        # Inicializa o orquestrador
        orchestrator = AEONOrchestrator()
        
        # Executa o workflow completo
        success = await orchestrator.execute_full_workflow()
        
        if success:
            # Obtém métricas finais
            metrics = await orchestrator.get_system_metrics()
            logger.info(f"Execução concluída com sucesso. Métricas finais:")
            logger.info(f"- Índice Simbiótico: {metrics.symbiotic_index}")
            logger.info(f"- Taxa de Adaptação: {metrics.adaptation_rate}")
            logger.info(f"- Progresso de Evolução: {metrics.evolution_progress}")
        else:
            logger.error("Falha na execução do workflow")
            
    except Exception as e:
        logger.error(f"Erro crítico durante execução: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
