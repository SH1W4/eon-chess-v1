"""Compatibility shim for older tests expecting `narrative.engine_simple`.
Exports NarrativeEngine from the current implementation.
"""
try:
    # Prefer the structured engine module if available
    from .engine.engine import NarrativeEngine  # type: ignore
except Exception:  # Fallback to the simpler engine if present
    from .engine import NarrativeEngine  # type: ignore
