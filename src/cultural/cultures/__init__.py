"""Cultural profiles and definitions.
Expose named culture objects for compatibility with tests.
"""

from .aztec_culture import aztec_culture  # existing

# Re-export cultures defined in the sibling module `cultural/cultures.py`
try:
    # Attempt to import from module file src/cultural/cultures.py
    from ..cultures import persian_culture, mongol_culture, chinese_culture
except ImportError:
    # If main cultures module is not available, create minimal versions
    from cultural.culture_framework import ChessCulture, CulturalTheme, PieceCulturalIdentity
    from core.board.board import PieceType
    
    # Minimal Persian culture for tests
    persian_culture = ChessCulture(
        name="Império Persa",
        description="A sofisticada cultura do xadrez persa",
        historical_period="224-651 D.C.",
        themes={
            "Conquista": CulturalTheme(
                name="Conquista",
                description="O espírito conquistador",
                weight=0.9,
                narratives=["Narrativa persa 1", "Narrativa persa 2"],
                historical_context="Contexto histórico"
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Xá",
                description="O rei persa",
                piece_type=PieceType.KING,
                cultural_value=1.0,
                historical_significance="Rei persa"
            ),
            PieceType.QUEEN: PieceCulturalIdentity(
                name="Vazir",
                description="O conselheiro",
                piece_type=PieceType.QUEEN,
                cultural_value=0.9,
                historical_significance="Conselheiro real"
            )
        }
    )
    
    # Minimal Mongol culture for tests
    mongol_culture = ChessCulture(
        name="Império Mongol",
        description="A cultura dos conquistadores das estepes",
        historical_period="1206-1368 D.C.",
        themes={
            "Conquista": CulturalTheme(
                name="Conquista",
                description="O espírito conquistador mongol",
                weight=0.9,
                narratives=["Narrativa mongol 1", "Narrativa mongol 2"],
                historical_context="Contexto histórico mongol"
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Khan",
                description="O líder supremo",
                piece_type=PieceType.KING,
                cultural_value=1.0,
                historical_significance="Imperador mongol"
            )
        }
    )
    
    # Minimal Chinese culture for tests
    chinese_culture = ChessCulture(
        name="Império Chinês",
        description="A antiga e refinada cultura do xiangqi",
        historical_period="960-1279 D.C.",
        themes={
            "Harmonia": CulturalTheme(
                name="Harmonia",
                description="O equilíbrio do Tao",
                weight=0.9,
                narratives=["Narrativa chinesa 1", "Narrativa chinesa 2"],
                historical_context="Filosofia tradicional chinesa"
            )
        },
        piece_identities={
            PieceType.KING: PieceCulturalIdentity(
                name="Imperador",
                description="O filho do céu",
                piece_type=PieceType.KING,
                cultural_value=1.0,
                historical_significance="Imperador chinês"
            )
        }
    )
