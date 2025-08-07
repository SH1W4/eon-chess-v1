from typing import Dict, List, Any
from datetime import datetime, timedelta
import asyncio
import logging
import json

from .cultural_patterns import CulturalPattern, CulturalContext

logger = logging.getLogger(__name__)

class CulturalTrainingData:
    """Gerenciador de dados de treinamento para padrões culturais."""
    
    def __init__(self):
        # Configurações de treinamento
        self.config = {
            "min_confidence_threshold": 0.6,
            "learning_rate": 0.1,
            "batch_size": 32,
            "validation_split": 0.2
        }
        
        # Inicializa dados de warm-up
        self.warmup_data = self._initialize_warmup_data()
        
        # Inicializa exemplos de treinamento
        self.training_examples = self._initialize_training_examples()
        
        # Cache para resultados de treinamento
        self.training_results: Dict[str, Any] = {}
        
    def _initialize_warmup_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Inicializa dados de warm-up para diferentes contextos culturais."""
        now = datetime.now()
        
        return {
            "social": [
                {
                    "pattern": CulturalPattern(
                        name="collaborative_learning",
                        description="Padrão de aprendizado colaborativo",
                        indicators=["knowledge_sharing", "peer_feedback", "group_discussion"],
                        strength=0.8,
                        confidence=0.9,
                        last_update=now,
                        context={"type": "social", "scope": "group"}
                    ),
                    "interactions": [
                        {
                            "type": "knowledge_share",
                            "participants": 5,
                            "success_rate": 0.85,
                            "timestamp": (now - timedelta(hours=2)).isoformat()
                        },
                        {
                            "type": "peer_review",
                            "participants": 3,
                            "quality_score": 0.9,
                            "timestamp": (now - timedelta(hours=1)).isoformat()
                        }
                    ],
                    "metrics": {
                        "engagement": 0.88,
                        "effectiveness": 0.92,
                        "sustainability": 0.85
                    }
                },
                {
                    "pattern": CulturalPattern(
                        name="resource_optimization",
                        description="Padrão de otimização coletiva de recursos",
                        indicators=["resource_sharing", "allocation_efficiency", "usage_patterns"],
                        strength=0.75,
                        confidence=0.85,
                        last_update=now,
                        context={"type": "social", "scope": "system"}
                    ),
                    "interactions": [
                        {
                            "type": "resource_allocation",
                            "efficiency": 0.82,
                            "participants": 8,
                            "timestamp": (now - timedelta(hours=3)).isoformat()
                        }
                    ],
                    "metrics": {
                        "efficiency": 0.85,
                        "fairness": 0.90,
                        "sustainability": 0.88
                    }
                }
            ],
            "evolutionary": [
                {
                    "pattern": CulturalPattern(
                        name="adaptive_learning",
                        description="Padrão de aprendizado adaptativo",
                        indicators=["learning_rate", "adaptation_speed", "knowledge_retention"],
                        strength=0.85,
                        confidence=0.88,
                        last_update=now,
                        context={"type": "evolutionary", "scope": "system"}
                    ),
                    "interactions": [
                        {
                            "type": "knowledge_acquisition",
                            "success_rate": 0.89,
                            "retention_rate": 0.92,
                            "timestamp": (now - timedelta(hours=4)).isoformat()
                        }
                    ],
                    "metrics": {
                        "adaptation_speed": 0.87,
                        "retention_quality": 0.91,
                        "application_success": 0.86
                    }
                }
            ],
            "cognitive": [
                {
                    "pattern": CulturalPattern(
                        name="problem_solving",
                        description="Padrão de resolução cognitiva de problemas",
                        indicators=["solution_quality", "processing_speed", "pattern_recognition"],
                        strength=0.82,
                        confidence=0.87,
                        last_update=now,
                        context={"type": "cognitive", "scope": "individual"}
                    ),
                    "interactions": [
                        {
                            "type": "problem_resolution",
                            "success_rate": 0.88,
                            "complexity_level": "high",
                            "timestamp": (now - timedelta(hours=1)).isoformat()
                        }
                    ],
                    "metrics": {
                        "accuracy": 0.89,
                        "speed": 0.85,
                        "efficiency": 0.87
                    }
                }
            ]
        }
        
    def _initialize_training_examples(self) -> List[Dict[str, Any]]:
        """Inicializa exemplos de treinamento para diferentes cenários."""
        now = datetime.now()
        
        return [
            # Exemplo 1: Transição de padrão colaborativo para competitivo
            {
                "scenario": "collaboration_to_competition",
                "initial_state": {
                    "pattern": CulturalPattern(
                        name="collaborative",
                        description="Estado inicial colaborativo",
                        indicators=["resource_sharing", "mutual_aid"],
                        strength=0.9,
                        confidence=0.85,
                        last_update=now - timedelta(hours=2),
                        context={"type": "social", "scope": "group"}
                    ),
                    "metrics": {
                        "collaboration_level": 0.9,
                        "resource_efficiency": 0.7
                    }
                },
                "transition_events": [
                    {
                        "type": "resource_scarcity",
                        "severity": 0.8,
                        "timestamp": (now - timedelta(hours=1)).isoformat()
                    },
                    {
                        "type": "performance_pressure",
                        "intensity": 0.75,
                        "timestamp": now.isoformat()
                    }
                ],
                "expected_outcome": {
                    "pattern": "competitive",
                    "indicators": ["resource_competition", "performance_focus"],
                    "min_strength": 0.7
                }
            },
            
            # Exemplo 2: Emergência de padrão adaptativo
            {
                "scenario": "adaptive_emergence",
                "initial_state": {
                    "pattern": CulturalPattern(
                        name="static",
                        description="Estado inicial estático",
                        indicators=["stability", "consistency"],
                        strength=0.6,
                        confidence=0.8,
                        last_update=now - timedelta(hours=3),
                        context={"type": "evolutionary", "scope": "system"}
                    ),
                    "metrics": {
                        "stability": 0.9,
                        "adaptation_need": 0.3
                    }
                },
                "transition_events": [
                    {
                        "type": "environment_change",
                        "magnitude": 0.7,
                        "timestamp": (now - timedelta(hours=2)).isoformat()
                    }
                ],
                "expected_outcome": {
                    "pattern": "adaptive",
                    "indicators": ["learning_rate", "adaptation_speed"],
                    "min_strength": 0.6
                }
            },
            
            # Exemplo 3: Desenvolvimento de padrão cognitivo
            {
                "scenario": "cognitive_development",
                "initial_state": {
                    "pattern": CulturalPattern(
                        name="basic_processing",
                        description="Processamento cognitivo básico",
                        indicators=["processing_speed", "memory_usage"],
                        strength=0.5,
                        confidence=0.7,
                        last_update=now - timedelta(hours=4),
                        context={"type": "cognitive", "scope": "individual"}
                    ),
                    "metrics": {
                        "processing_efficiency": 0.6,
                        "learning_progress": 0.4
                    }
                },
                "transition_events": [
                    {
                        "type": "learning_exposure",
                        "intensity": 0.8,
                        "duration_hours": 2,
                        "timestamp": (now - timedelta(hours=3)).isoformat()
                    },
                    {
                        "type": "pattern_recognition_training",
                        "complexity": 0.7,
                        "timestamp": (now - timedelta(hours=1)).isoformat()
                    }
                ],
                "expected_outcome": {
                    "pattern": "advanced_cognitive",
                    "indicators": ["pattern_recognition", "learning_curve"],
                    "min_strength": 0.7
                }
            }
        ]
        
    async def apply_warmup_data(self, context: CulturalContext) -> bool:
        """Aplica dados de warm-up ao contexto cultural."""
        try:
            logger.info("Iniciando aplicação de dados de warm-up")
            
            for context_type, patterns in self.warmup_data.items():
                for pattern_data in patterns:
                    # Adiciona padrão ao contexto
                    if pattern_data["pattern"] not in context.dominant_patterns:
                        context.dominant_patterns.append(pattern_data["pattern"])
                    
                    # Registra interações no histórico
                    for interaction in pattern_data["interactions"]:
                        context.interaction_history.append({
                            "pattern": pattern_data["pattern"].name,
                            "data": interaction,
                            "metrics": pattern_data["metrics"]
                        })
            
            logger.info("Dados de warm-up aplicados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao aplicar dados de warm-up: {e}")
            return False
            
    async def run_training_example(
        self,
        context: CulturalContext,
        example_id: str
    ) -> Dict[str, Any]:
        """Executa um exemplo de treinamento específico."""
        try:
            # Encontra exemplo de treinamento
            example = next(
                (e for e in self.training_examples if e["scenario"] == example_id),
                None
            )
            
            if not example:
                raise ValueError(f"Exemplo de treinamento não encontrado: {example_id}")
                
            logger.info(f"Iniciando exemplo de treinamento: {example_id}")
            
            # Aplica estado inicial
            initial_pattern = example["initial_state"]["pattern"]
            context.dominant_patterns = [initial_pattern]
            
            # Processa eventos de transição
            for event in example["transition_events"]:
                # Simula passagem de tempo
                await asyncio.sleep(1)
                
                # Registra evento no histórico
                context.interaction_history.append({
                    "type": "transition_event",
                    "data": event,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Verifica resultado
            expected = example["expected_outcome"]
            final_pattern = next(
                (p for p in context.dominant_patterns if p.name == expected["pattern"]),
                None
            )
            
            success = (
                final_pattern is not None and
                final_pattern.strength >= expected["min_strength"] and
                all(i in final_pattern.indicators for i in expected["indicators"])
            )
            
            # Registra resultado
            result = {
                "scenario": example_id,
                "success": success,
                "final_pattern": final_pattern.__dict__ if final_pattern else None,
                "expected_pattern": expected,
                "timestamp": datetime.now().isoformat()
            }
            
            self.training_results[example_id] = result
            
            logger.info(f"Exemplo de treinamento concluído: {example_id} (Sucesso: {success})")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao executar exemplo de treinamento {example_id}: {e}")
            return {
                "scenario": example_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    def get_training_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos resultados de treinamento."""
        if not self.training_results:
            return {
                "total_examples": 0,
                "success_rate": 0.0,
                "scenarios": {}
            }
            
        total = len(self.training_results)
        successful = sum(1 for r in self.training_results.values() if r["success"])
        
        # Agrupa resultados por cenário
        scenarios = {}
        for result in self.training_results.values():
            scenario = result["scenario"]
            if scenario not in scenarios:
                scenarios[scenario] = {
                    "attempts": 0,
                    "successes": 0
                }
            scenarios[scenario]["attempts"] += 1
            if result["success"]:
                scenarios[scenario]["successes"] += 1
                
        return {
            "total_examples": total,
            "success_rate": successful / total if total > 0 else 0.0,
            "scenarios": {
                name: {
                    "attempts": data["attempts"],
                    "success_rate": data["successes"] / data["attempts"]
                }
                for name, data in scenarios.items()
            }
        }
        
    def get_warmup_summary(self) -> Dict[str, Any]:
        """Retorna um resumo dos dados de warm-up."""
        summary = {
            "total_patterns": 0,
            "patterns_by_type": {},
            "total_interactions": 0,
            "average_metrics": {}
        }
        
        # Agrega métricas de todos os padrões
        all_metrics = {}
        
        for context_type, patterns in self.warmup_data.items():
            # Conta padrões por tipo
            summary["patterns_by_type"][context_type] = len(patterns)
            summary["total_patterns"] += len(patterns)
            
            # Conta interações
            interactions = sum(len(p["interactions"]) for p in patterns)
            summary["total_interactions"] += interactions
            
            # Agrega métricas
            for pattern in patterns:
                for metric, value in pattern["metrics"].items():
                    if metric not in all_metrics:
                        all_metrics[metric] = []
                    all_metrics[metric].append(value)
                    
        # Calcula médias das métricas
        summary["average_metrics"] = {
            metric: sum(values) / len(values)
            for metric, values in all_metrics.items()
        }
        
        return summary
