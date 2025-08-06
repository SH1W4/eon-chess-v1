#!/usr/bin/env python3

"""
Script de Validação do Sistema Cultural
Testa e valida as implementações culturais, narrativas e comportamentais
"""

import sys
import os
from pathlib import Path
import json
import datetime
import logging

# Adiciona diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

from cultural.behavior_stabilizer import BehaviorStabilizer
from cultural.narrative_generator import NarrativeGenerator
from cultural.narrative_integrator import NarrativeIntegrator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='cultural_validation.log'
)

def validate_behavior_stabilization():
    """Valida estabilização comportamental"""
    print("\n=== Validando Estabilização Comportamental ===")
    stabilizer = BehaviorStabilizer()
    
    # Testar padrões instáveis
    test_patterns = [
        {
            "name": "aggressive_adaptation",
            "volatility_index": 0.8,
            "stability_score": 0.4,
            "adaptation_rate": 0.9
        },
        {
            "name": "rapid_evolution",
            "volatility_index": 0.9,
            "stability_score": 0.3,
            "adaptation_rate": 0.95
        }
    ]
    
    results = []
    for pattern in test_patterns:
        stabilized = stabilizer.stabilize_behavior(pattern)
        results.append({
            "original": pattern,
            "stabilized": stabilized,
            "improvement": {
                "volatility_reduction": pattern["volatility_index"] - stabilized.get("volatility_index", 0),
                "stability_increase": stabilized.get("stability_score", 0) - pattern["stability_score"],
                "adaptation_control": pattern["adaptation_rate"] - stabilized["adaptation_rate"]
            }
        })
        
    print("\nResultados da Estabilização:")
    for result in results:
        print(f"\nPadrão: {result['original']['name']}")
        print(f"- Redução de volatilidade: {result['improvement']['volatility_reduction']:.2f}")
        print(f"- Aumento de estabilidade: {result['improvement']['stability_increase']:.2f}")
        print(f"- Controle de adaptação: {result['improvement']['adaptation_control']:.2f}")
    
    return results

def validate_narrative_generation():
    """Valida geração narrativa"""
    print("\n=== Validando Geração Narrativa ===")
    generator = NarrativeGenerator()
    
    # Testar diferentes contextos
    test_contexts = [
        {
            "cultural_focus": "conflito territorial",
            "current_state": {
                "tension_level": 0.7,
                "cultural_diversity": 0.8,
                "adaptation_rate": 0.6
            }
        },
        {
            "cultural_focus": "jornada espiritual",
            "current_state": {
                "tension_level": 0.4,
                "cultural_diversity": 0.9,
                "adaptation_rate": 0.7
            }
        }
    ]
    
    results = []
    for context in test_contexts:
        narrative = generator.generate_narrative(context)
        results.append({
            "context": context,
            "narrative": narrative,
            "evaluation": {
                "theme_alignment": evaluate_theme_alignment(narrative, context),
                "narrative_coherence": evaluate_narrative_coherence(narrative),
                "cultural_relevance": evaluate_cultural_relevance(narrative, context)
            }
        })
        
    print("\nResultados da Geração Narrativa:")
    for result in results:
        print(f"\nContexto: {result['context']['cultural_focus']}")
        print(f"- Alinhamento temático: {result['evaluation']['theme_alignment']:.2f}")
        print(f"- Coerência narrativa: {result['evaluation']['narrative_coherence']:.2f}")
        print(f"- Relevância cultural: {result['evaluation']['cultural_relevance']:.2f}")
    
    return results

def validate_narrative_integration():
    """Valida integração narrativa"""
    print("\n=== Validando Integração Narrativa ===")
    integrator = NarrativeIntegrator()
    
    # Testar integração entre narrativas e culturas
    test_narratives = [
        {
            "name": "conflito_territorial",
            "theme": "território",
            "arc": "confronto",
            "elements": {
                "characters": [
                    {
                        "archetype": "guerreiro",
                        "traits": ["corajoso", "leal"]
                    }
                ],
                "settings": [
                    {
                        "type": "fronteira",
                        "description": "Local de disputa territorial"
                    }
                ]
            }
        }
    ]
    
    test_cultures = [
        {
            "name": "viking",
            "attributes": {
                "cultural_values": ["honra", "bravura", "exploração"]
            },
            "narrative_elements": {
                "cultural_practices": ["raid", "navegação"],
                "key_stories": ["conquista", "exploração"]
            }
        },
        {
            "name": "samurai",
            "attributes": {
                "cultural_values": ["honra", "disciplina", "lealdade"]
            },
            "narrative_elements": {
                "cultural_practices": ["bushido", "meditação"],
                "key_stories": ["sacrifício", "dever"]
            }
        }
    ]
    
    results = []
    integrated = integrator.integrate_narratives(test_narratives, test_cultures)
    for narrative_name, integration in integrated["integration_map"].items():
        results.append({
            "narrative": narrative_name,
            "evaluation": {
                "cultural_connection": evaluate_cultural_connection(integration),
                "thematic_alignment": evaluate_thematic_alignment(integration),
                "integration_quality": evaluate_integration_quality(integration)
            }
        })
        
    print("\nResultados da Integração Narrativa:")
    for result in results:
        print(f"\nNarrativa: {result['narrative']}")
        print(f"- Conexão cultural: {result['evaluation']['cultural_connection']:.2f}")
        print(f"- Alinhamento temático: {result['evaluation']['thematic_alignment']:.2f}")
        print(f"- Qualidade da integração: {result['evaluation']['integration_quality']:.2f}")
    
    return results

def evaluate_theme_alignment(narrative, context):
    """Avalia alinhamento temático"""
    if isinstance(narrative["theme"], list):
        theme_match = any(t.lower() in context["cultural_focus"].lower() for t in narrative["theme"])
    else:
        theme_match = narrative["theme"].lower() in context["cultural_focus"].lower()
    return 1.0 if theme_match else 0.5

def evaluate_narrative_coherence(narrative):
    """Avalia coerência narrativa"""
    has_theme = bool(narrative.get("theme"))
    has_arc = bool(narrative.get("arc"))
    has_elements = bool(narrative.get("elements"))
    
    return sum([has_theme, has_arc, has_elements]) / 3

def evaluate_cultural_relevance(narrative, context):
    """Avalia relevância cultural"""
    cultural_focus = context["cultural_focus"].lower()
    narrative_elements = str(narrative).lower()
    
    return 1.0 if cultural_focus in narrative_elements else 0.5

def evaluate_cultural_connection(integration):
    """Avalia conexão cultural"""
    connections = []
    for culture_connection in integration.get("cultural_connections", {}).values():
        connection_score = sum(
            value for value in culture_connection.values()
            if isinstance(value, (int, float))
        ) / len(culture_connection)
        connections.append(connection_score)
    
    return sum(connections) / len(connections) if connections else 0

def evaluate_thematic_alignment(integration):
    """Avalia alinhamento temático"""
    alignments = []
    for culture_alignment in integration.get("thematic_alignments", {}).values():
        if isinstance(culture_alignment, dict):
            theme_harmony = culture_alignment.get("theme_harmony", {})
            if isinstance(theme_harmony, dict):
                alignment_score = sum(
                    value for value in theme_harmony.values()
                    if isinstance(value, (int, float))
                ) / len(theme_harmony)
                alignments.append(alignment_score)
    
    return sum(alignments) / len(alignments) if alignments else 0

def evaluate_integration_quality(integration):
    """Avalia qualidade da integração"""
    cultural_connection = evaluate_cultural_connection(integration)
    thematic_alignment = evaluate_thematic_alignment(integration)
    
    return (cultural_connection + thematic_alignment) / 2

def generate_validation_report(behavior_results, narrative_results, integration_results):
    """Gera relatório de validação"""
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "behavior_stabilization": {
            "patterns_tested": len(behavior_results),
            "average_improvements": {
                "volatility_reduction": sum(r["improvement"]["volatility_reduction"] for r in behavior_results) / len(behavior_results),
                "stability_increase": sum(r["improvement"]["stability_increase"] for r in behavior_results) / len(behavior_results),
                "adaptation_control": sum(r["improvement"]["adaptation_control"] for r in behavior_results) / len(behavior_results)
            }
        },
        "narrative_generation": {
            "contexts_tested": len(narrative_results),
            "average_scores": {
                "theme_alignment": sum(r["evaluation"]["theme_alignment"] for r in narrative_results) / len(narrative_results),
                "narrative_coherence": sum(r["evaluation"]["narrative_coherence"] for r in narrative_results) / len(narrative_results),
                "cultural_relevance": sum(r["evaluation"]["cultural_relevance"] for r in narrative_results) / len(narrative_results)
            }
        },
        "narrative_integration": {
            "integrations_tested": len(integration_results),
            "average_scores": {
                "cultural_connection": sum(r["evaluation"]["cultural_connection"] for r in integration_results) / len(integration_results),
                "thematic_alignment": sum(r["evaluation"]["thematic_alignment"] for r in integration_results) / len(integration_results),
                "integration_quality": sum(r["evaluation"]["integration_quality"] for r in integration_results) / len(integration_results)
            }
        }
    }
    
    # Salvar relatório
    report_file = Path("validation_reports") / f"cultural_validation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n=== Relatório de Validação ===")
    print("\nEstabilização Comportamental:")
    print(f"- Redução média de volatilidade: {report['behavior_stabilization']['average_improvements']['volatility_reduction']:.2f}")
    print(f"- Aumento médio de estabilidade: {report['behavior_stabilization']['average_improvements']['stability_increase']:.2f}")
    print(f"- Controle médio de adaptação: {report['behavior_stabilization']['average_improvements']['adaptation_control']:.2f}")
    
    print("\nGeração Narrativa:")
    print(f"- Alinhamento temático médio: {report['narrative_generation']['average_scores']['theme_alignment']:.2f}")
    print(f"- Coerência narrativa média: {report['narrative_generation']['average_scores']['narrative_coherence']:.2f}")
    print(f"- Relevância cultural média: {report['narrative_generation']['average_scores']['cultural_relevance']:.2f}")
    
    print("\nIntegração Narrativa:")
    print(f"- Conexão cultural média: {report['narrative_integration']['average_scores']['cultural_connection']:.2f}")
    print(f"- Alinhamento temático médio: {report['narrative_integration']['average_scores']['thematic_alignment']:.2f}")
    print(f"- Qualidade média de integração: {report['narrative_integration']['average_scores']['integration_quality']:.2f}")
    
    return report

def main():
    print("Iniciando validação do sistema cultural...")
    
    # Executar validações
    behavior_results = validate_behavior_stabilization()
    narrative_results = validate_narrative_generation()
    integration_results = validate_narrative_integration()
    
    # Gerar relatório
    report = generate_validation_report(
        behavior_results,
        narrative_results,
        integration_results
    )
    
    print("\nValidação concluída. Relatório salvo em validation_reports/")

if __name__ == "__main__":
    main()
