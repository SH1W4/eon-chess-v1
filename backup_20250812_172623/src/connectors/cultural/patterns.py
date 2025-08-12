from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class CulturalPattern:
    """Padrão cultural base."""
    id: str
    name: str
    description: str
    weight: float
    context_rules: List[str]
    creation_date: datetime
    last_update: datetime
    attributes: Dict[str, float]

# Padrões culturais básicos pré-definidos
BASE_PATTERNS = {
    "classical_chess": CulturalPattern(
        id="pattern_001",
        name="Classical Chess Style",
        description="Padrão de jogo clássico, focado em controle do centro e desenvolvimento de peças",
        weight=1.0,
        context_rules=[
            "priorizar desenvolvimento de peças",
            "controlar centro do tabuleiro",
            "proteger o rei"
        ],
        creation_date=datetime.now(),
        last_update=datetime.now(),
        attributes={
            "strategic_depth": 0.9,
            "tactical_complexity": 0.8,
            "positional_understanding": 0.85
        }
    ),
    "romantic_chess": CulturalPattern(
        id="pattern_002",
        name="Romantic Chess Style",
        description="Estilo de jogo agressivo com foco em sacrifícios e ataques",
        weight=0.8,
        context_rules=[
            "priorizar ataques ao rei",
            "aceitar sacrifícios por iniciativa",
            "buscar combinações táticas"
        ],
        creation_date=datetime.now(),
        last_update=datetime.now(),
        attributes={
            "aggression": 0.9,
            "creativity": 0.85,
            "risk_taking": 0.8
        }
    ),
    "modern_chess": CulturalPattern(
        id="pattern_003",
        name="Modern Chess Style",
        description="Abordagem flexível e dinâmica ao jogo",
        weight=0.9,
        context_rules=[
            "manter flexibilidade estrutural",
            "equilibrar atividade de peças",
            "adaptar ao estilo do oponente"
        ],
        creation_date=datetime.now(),
        last_update=datetime.now(),
        attributes={
            "adaptability": 0.9,
            "balance": 0.85,
            "dynamism": 0.85
        }
    ),
    "hypermodern_chess": CulturalPattern(
        id="pattern_004",
        name="Hypermodern Chess Style",
        description="Controle do centro à distância e jogo flexível de flancos",
        weight=0.75,
        context_rules=[
            "controlar centro com peças",
            "desenvolver estrutura fianchetto",
            "pressionar flancos"
        ],
        creation_date=datetime.now(),
        last_update=datetime.now(),
        attributes={
            "innovation": 0.9,
            "strategic_depth": 0.85,
            "positional_complexity": 0.8
        }
    )
}

# Métricas de coerência para padrões
COHERENCE_METRICS = {
    "pattern_compatibility": 0.8,  # Compatibilidade entre padrões
    "context_relevance": 0.85,    # Relevância ao contexto atual
    "temporal_consistency": 0.9,   # Consistência ao longo do tempo
    "cultural_alignment": 0.85     # Alinhamento com aspectos culturais
}

# Sistema de warm-up
WARMUP_SEQUENCE = [
    {
        "phase": "initialization",
        "patterns": ["classical_chess"],
        "duration": 5  # segundos
    },
    {
        "phase": "basic_adaptation",
        "patterns": ["classical_chess", "modern_chess"],
        "duration": 10
    },
    {
        "phase": "full_activation",
        "patterns": ["classical_chess", "modern_chess", "romantic_chess", "hypermodern_chess"],
        "duration": 15
    }
]
