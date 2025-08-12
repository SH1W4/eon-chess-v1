from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class SystemMonitor:
    """Lightweight system monitor used by integration tests.

    Tracks simple counters and timings for game moves and AI evaluations.
    """
    active: bool = False
    session_id: Optional[str] = None
    started_at: float = 0.0
    metrics: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Initialize default metrics expected by tests
        self.metrics.setdefault("game_moves", 0)
        self.metrics.setdefault("ai_calculations", 0)
        self.metrics.setdefault("errors", 0)
        self.metrics.setdefault("uptime_seconds", 0.0)

    def start_monitoring(self, session_id: str = "default") -> None:
        self.active = True
        self.session_id = session_id
        self.started_at = time.time()

    def stop_monitoring(self) -> None:
        if self.active:
            self.metrics["uptime_seconds"] = time.time() - self.started_at
        self.active = False

    # Convenience incrementors the rest of the code can call (no-ops if inactive)
    def record_game_move(self, count: int = 1) -> None:
        self.metrics["game_moves"] = self.metrics.get("game_moves", 0) + (count or 0)

    def record_ai_calculation(self, count: int = 1) -> None:
        self.metrics["ai_calculations"] = self.metrics.get("ai_calculations", 0) + (count or 0)

    def record_error(self, count: int = 1) -> None:
        self.metrics["errors"] = self.metrics.get("errors", 0) + (count or 0)

    def get_metrics(self) -> Dict[str, float]:
        # Update uptime live if still active
        if self.active:
            self.metrics["uptime_seconds"] = time.time() - self.started_at
        return dict(self.metrics)
