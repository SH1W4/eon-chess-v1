# Audio system for CHESS with cultural integration.
# Minimal stub to be extended by frontend/backend layers.
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

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
        self.current_culture = culture

    def set_phase(self, phase: str) -> None:
        assert phase in {"opening", "midgame", "endgame"}
        self.current_phase = phase

    def mute(self, value: bool = True) -> None:
        self.muted = value

    def next_track(self) -> TrackSpec:
        culture = self.current_culture or "default"
        base = f"assets/audio/{culture}"
        return TrackSpec(culture=culture, phase=self.current_phase, path=f"{base}/{self.current_phase}.mp3")

    def sfx_for_event(self, event: str) -> str:
        culture = self.current_culture or "default"
        return f"assets/audio/{culture}/sfx/{event}.mp3"
