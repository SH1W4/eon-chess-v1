from src.cultural.metrics import CulturalMetrics

def demonstrar_analise_cultural():
    """Demonstração prática de análise cultural no xadrez."""
    # Inicialização das métricas
    metrics = CulturalMetrics()
    
    # Análise Bizantina
    print("\n=== Análise Cultural: Império Bizantino ===")
    elementos_bizantinos = [
        "Estratégia Imperial",
        "Diplomacia Bizantina",
        "Hierarquia Militar",
        "Ritual da Corte",
        "Simbolismo Ortodoxo"
    ]
    impacto_bizantino = metrics.analyze_cultural_impact(elementos_bizantinos)
    print(f"Impacto cultural bizantino: {impacto_bizantino}")
    
    # Análise Maia
    print("\n=== Análise Cultural: Civilização Maia ===")
    elementos_maias = [
        "Calendário Sagrado",
        "Hierarquia Sacerdotal",
        "Ritual de Sacrifício",
        "Astronomia Maia",
        "Simbologia Numérica"
    ]
    impacto_maia = metrics.analyze_cultural_impact(elementos_maias)
    print(f"Impacto cultural maia: {impacto_maia}")
    
    # Análise Pós-Singularidade
    print("\n=== Análise Cultural: Era Pós-Singularidade ===")
    elementos_futuristas = [
        "IA Avançada",
        "Computação Quântica",
        "Realidade Aumentada",
        "Consciência Coletiva",
        "Evolução Tecnológica"
    ]
    impacto_futurista = metrics.analyze_cultural_impact(elementos_futuristas)
    print(f"Impacto cultural futurista: {impacto_futurista}")
    
    # Refinamento de métricas
    print("\n=== Refinamento de Métricas ===")
    metrics.refine_metrics()
    
    # Exemplo de uso para novo tema
    print("\n=== Demonstração de Novo Tema ===")
    novo_tema = [
        "Elemento Cultural 1",
        "Elemento Cultural 2",
        "Elemento Cultural 3"
    ]
    impacto_novo = metrics.analyze_cultural_impact(novo_tema)
    print(f"Impacto do novo tema: {impacto_novo}")

if __name__ == "__main__":
    print("Iniciando demonstração de métricas culturais...")
    demonstrar_analise_cultural()
    print("\nDemonstração concluída!")
