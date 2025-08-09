"""Cultural profiles and definitions.
Expose named culture objects for compatibility with tests.
"""

from .aztec_culture import aztec_culture  # existing

# Re-export cultures defined in the sibling module `cultural/cultures.py`
try:
    # Attempt to import from module file src/cultural/cultures.py
    from .. import cultures as _cultures
    persian_culture = getattr(_cultures, "persian_culture", None)
    mongol_culture = getattr(_cultures, "mongol_culture", None)
    chinese_culture = getattr(_cultures, "chinese_culture", None)
    del _cultures
except Exception:
    # If unavailable, keep package import working without raising
    persian_culture = mongol_culture = chinese_culture = None
