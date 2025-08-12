# Compatibility shim for legacy imports
# Exposes CulturalBehavior and AdaptiveDecisionTree at top-level import path
from cultural.adaptive_decision import CulturalBehavior, AdaptiveDecisionTree

__all__ = ["CulturalBehavior", "AdaptiveDecisionTree"]
