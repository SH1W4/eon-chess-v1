import asyncio
from connectors.cultural.cultural_connector import CulturalConnector
from connectors.narrative.narrative_connector import NarrativeConnector
from connectors.quantum.quantum_connector import QuantumConnector
from monitoring.cultural_monitor import CulturalMonitor
from monitoring.narrative_monitor import NarrativeMonitor
from monitoring.quantum_monitor import QuantumMonitor

async def test_connector(name: str, connector, monitor):
    """Testa um conector específico."""
    print(f"\n=== Testando {name} ===")
    
    # Inicialização
    print("1. Testando inicialização...")
    config = {
        "cache_enabled": True,
        "validation_enabled": True,
        "enable_auto_optimization": True,
        "cache_config": {
            "max_size": 1000,
            "default_ttl": 3600
        }
    }
    
    init_success = await connector.initialize(config)
    print(f"Inicialização: {'Sucesso' if init_success else 'Falha'}")
    
    # Conexão
    print("\n2. Testando conexão...")
    connect_success = await connector.connect()
    print(f"Conexão: {'Sucesso' if connect_success else 'Falha'}")
    
    # Estado
    print("\n3. Testando gestão de estado...")
    state = await connector.get_state()
    print(f"Estado atual: {state}")
    
    # Monitoramento
    print("\n3.1. Testando monitoramento...")
    await monitor.check_health()
    health_summary = monitor.get_health_summary()
    print(f"Estado de saúde: {health_summary['status']}")
    print(f"Métricas: {health_summary['metrics']}")
    if health_summary['alerts']:
        print(f"Alertas: {health_summary['alerts']}")
    
    # Atualização de estado
    print("\n4. Testando atualização de estado...")
    update_success = await connector.update_state({
        "test_update": True,
        "timestamp": "2025-08-07T08:49:01Z"
    })
    print(f"Atualização: {'Sucesso' if update_success else 'Falha'}")
    
    # Verificação de saúde
    print("\n5. Testando verificação de saúde...")
    health = await connector.verify_health()
    print(f"Saúde: {'OK' if health else 'Crítica'}")
    
    # Aguarda otimizações
    print("\n5.1. Aguardando ciclo de otimização...")
    await asyncio.sleep(2)  # Aguarda um pouco para ver otimizações
    
    if hasattr(connector, '_optimizer'):
        stats = connector._optimizer.get_optimization_stats()
        print(f"Estatísticas de otimização: {stats}")
    
    if hasattr(connector, '_cache'):
        cache_stats = connector._cache.get_stats()
        print(f"Estatísticas de cache: {cache_stats}")
    
    # Desconexão
    print("\n6. Testando desconexão...")
    disconnect_success = await connector.disconnect()
    print(f"Desconexão: {'Sucesso' if disconnect_success else 'Falha'}")

async def main():
    """Função principal para testar todos os conectores."""
    print("=== Iniciando Testes dos Conectores ===\n")
    
    # Criando instâncias dos conectores e monitores
    cultural = CulturalConnector()
    cultural_monitor = CulturalMonitor()
    
    narrative = NarrativeConnector()
    narrative_monitor = NarrativeMonitor()
    
    quantum = QuantumConnector()
    quantum_monitor = QuantumMonitor()
    
    # Testando cada conector
    await test_connector("Conector Cultural", cultural, cultural_monitor)
    await test_connector("Conector Narrativo", narrative, narrative_monitor)
    await test_connector("Conector Quântico", quantum, quantum_monitor)
    
    print("\n=== Testes Concluídos ===")

if __name__ == "__main__":
    asyncio.run(main())
