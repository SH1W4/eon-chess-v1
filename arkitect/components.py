# Local shim for ARKITECT components
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ArchitectureAnalyzer:
    depth: str = "deep"
    interval: str = "4h"
    patterns: List[Dict[str, Any]] = field(default_factory=list)

    def add_pattern_analysis(self, pattern_type: str, priority: str) -> None:
        self.patterns.append({"type": pattern_type, "priority": priority})

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "depth": self.depth,
            "patterns_tracked": len(self.patterns),
            "interval": self.interval,
            "score": 0.9,
        }

@dataclass
class CodeQualityAnalyzer:
    threshold: float = 0.9
    frequency: str = "4h"
    standards: List[str] = field(default_factory=list)

    def add_quality_standard(self, standard: str) -> None:
        self.standards.append(standard)

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "threshold": self.threshold,
            "standards": len(self.standards),
            "frequency": self.frequency,
            "quality": 0.92,
        }

@dataclass
class EvolutionTracker:
    retention: str = "30d"
    interval: str = "1d"
    focus: Dict[str, Any] = field(default_factory=dict)

    def add_focus_area(self, component: str, metrics: list[str]) -> None:
        self.focus[component] = metrics

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "retention": self.retention,
            "focus_areas": len(self.focus),
            "interval": self.interval,
            "evolution_index": 0.88,
        }

