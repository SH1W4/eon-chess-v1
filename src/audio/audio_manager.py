# Audio system for CHESS with cultural integration.
# Minimal stub to be extended by frontend/backend layers.
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

try:
    # Lazy import to avoid heavy dependencies during import
    from src.cultural.cultural_registry import get_registry
except Exception:  # pragma: no cover
    get_registry = None

@dataclass
class TrackSpec:
    culture: str
    phase: str  # opening|midgame|endgame
    path: str

class AudioManager:
    def __init__(self):
        self.current_culture: Optional[str] = None
        self.current_phase: str = "opening"
        self.muted: bool = False

    def set_culture(self, culture: str) -> None:
        # Validate against Cultural Registry if available
        if get_registry is not None:
            reg = get_registry()
            if reg.get_culture(culture) is None:
                # fallback to default if invalid
                self.current_culture = "default"
                return
        self.current_culture = culture

    def set_phase(self, phase: str) -> None:
        assert phase in {"opening", "midgame", "endgame"}
        self.current_phase = phase

    def mute(self, value: bool = True) -> None:
        self.muted = value

    def next_track(self) -> TrackSpec:
        culture = self.current_culture or "default"
        # Attempt to normalize culture id if registry presents display name mapping
        if get_registry is not None and culture != "default":
            reg = get_registry()
            if reg.get_culture(culture) is None:
                # try lowercasing id
                maybe = culture.lower().replace(" ", "_")
                if reg.get_culture(maybe) is not None:
                    culture = maybe
                else:
                    culture = "default"
        base = f"assets/audio/{culture}"
        return TrackSpec(culture=culture, phase=self.current_phase, path=f"{base}/{self.current_phase}.mp3")

    def sfx_for_event(self, event: str) -> str:
        culture = self.current_culture or "default"
        return f"assets/audio/{culture}/sfx/{event}.mp3"
