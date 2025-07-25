#!/usr/bin/env python3
import asyncio
import logging
from task_mash_superscope import TaskMashSuperscope

async def run_integration():
    """Executa integração completa do sistema"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('integration.log')
        ]
    )
    
    logger = logging.getLogger("Integration")
    logger.info("Iniciando integração do sistema...")
    
    try:
        # Inicializa TaskMash
        task_mash = TaskMashSuperscope()
        
        # Executa integração
        success = await task_mash.execute_all()
        
        if success:
            logger.info("Integração concluída com sucesso!")
            
            # Exibe resumo da execução
            print("\n=== Resumo da Execução ===")
            print("1. ARQUIMAX Integration: ✓")
            print("2. NEXUS Connection: ✓")
            print("3. Chess System Setup: ✓")
            print("4. Monitoring Active: ✓")
            print("5. Analytics Ready: ✓")
            print("\nSistema pronto para uso!")
            
        else:
            logger.error("Falha na integração!")
            print("\n⚠️ Erro na integração do sistema!")
            print("Verifique os logs para mais detalhes.")
    
    except Exception as e:
        logger.error(f"Erro fatal durante integração: {str(e)}")
        print("\n❌ Erro fatal durante integração!")
        print(f"Erro: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(run_integration())
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro fatal: {str(e)}")
        exit(1)
