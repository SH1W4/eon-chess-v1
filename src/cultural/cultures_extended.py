from dataclasses import dataclass
from typing import Dict, List, Optional
from core.board.board import PieceType
from cultural.culture_framework import ChessCulture, CulturalTheme, PieceCulturalIdentity

# Cultura Indiana (Chaturanga)
indian_culture = ChessCulture(
    name="Império Indiano",
    description="A antiga tradição do Chaturanga, ancestral do xadrez moderno",
    historical_period="600 D.C.",
    themes={
        "Dharma": CulturalTheme(
            name="Dharma",
            description="O dever sagrado e a ordem cósmica",
            weight=0.9,
            narratives=[
                "Seguindo o dharma, {piece} cumpre seu dever sagrado",
                "Em harmonia com a ordem cósmica, {piece} se move",
                "Como ditam as escrituras antigas, {piece} avança"
            ],
            historical_context="Baseado nos conceitos védicos de dever e ordem"
        ),
        "Quatro Braços": CulturalTheme(
            name="Quatro Braços",
            description="Os quatro ramos do exército indiano antigo",
            weight=0.8,
            narratives=[
                "Como parte das quatro forças, {piece} toma posição",
                "Unindo os braços do exército, {piece} coordena o movimento",
                "Na tradição dos quatro poderes, {piece} executa sua função"
            ],
            historical_context="Baseado na composição tradicional do exército indiano"
        ),
        "Karma": CulturalTheme(
            name="Karma",
            description="A lei da ação e consequência",
            weight=0.7,
            narratives=[
                "O karma guia {piece} em sua jornada",
                "As ações passadas determinam o movimento de {piece}",
                "Seguindo o fluxo do karma, {piece} encontra seu caminho"
            ],
            historical_context="Conceito fundamental da filosofia indiana"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Raja",
            description="O rei, líder supremo",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="O governante supremo no sistema indiano"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Mantri",
            description="O ministro sábio",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Conselheiro principal do Raja"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Gaja",
            description="O elefante de guerra",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="Elemento crucial nos exércitos indianos"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Ashva",
            description="O cavalo de batalha",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.7,
            historical_significance="A cavalaria do exército indiano"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Ratha",
            description="A carruagem de guerra",
            piece_type=PieceType.ROOK,
            cultural_value=0.6,
            historical_significance="As carruagens do exército indiano"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Padati",
            description="O soldado de infantaria",
            piece_type=PieceType.PAWN,
            cultural_value=0.4,
            historical_significance="A infantaria do exército indiano"
        )
    }
)

# Cultura Árabe (Shatranj)
arabic_culture = ChessCulture(
    name="Califado Árabe",
    description="A era dourada do xadrez árabe (shatranj)",
    historical_period="800-1200 D.C.",
    themes={
        "Sabedoria": CulturalTheme(
            name="Sabedoria",
            description="A tradição intelectual árabe",
            weight=0.9,
            narratives=[
                "Com a sabedoria dos califas, {piece} escolhe seu caminho",
                "Seguindo os ensinamentos dos mestres, {piece} se move",
                "A tradição dos sábios guia {piece}"
            ],
            historical_context="Baseado na rica tradição intelectual árabe"
        ),
        "Poesia do Movimento": CulturalTheme(
            name="Poesia do Movimento",
            description="A elegância da tradição poética árabe",
            weight=0.8,
            narratives=[
                "Como versos de um poema, {piece} tece seu movimento",
                "Com a elegância da caligrafia, {piece} traça seu caminho",
                "Na métrica dos antigos poetas, {piece} compõe sua jogada"
            ],
            historical_context="Influência da poesia árabe clássica"
        ),
        "Honra do Deserto": CulturalTheme(
            name="Honra do Deserto",
            description="Os códigos de honra beduínos",
            weight=0.7,
            narratives=[
                "Com a honra dos beduínos, {piece} enfrenta seu destino",
                "Como guardião do deserto, {piece} protege seu território",
                "Seguindo o código do deserto, {piece} avança"
            ],
            historical_context="Baseado nos códigos de honra tradicionais"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Califa",
            description="O líder supremo do califado",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="Líder espiritual e temporal"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Vizir",
            description="O conselheiro do califa",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Principal conselheiro do califado"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Al-Fil",
            description="O elefante sábio",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="Origem do nome 'alfil' no xadrez"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Faras",
            description="O cavalo árabe",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.7,
            historical_significance="A famosa cavalaria árabe"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Rukh",
            description="A fortaleza móvel",
            piece_type=PieceType.ROOK,
            cultural_value=0.6,
            historical_significance="Origem do termo 'rook' no xadrez"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Jundi",
            description="O soldado do califado",
            piece_type=PieceType.PAWN,
            cultural_value=0.4,
            historical_significance="A infantaria do exército árabe"
        )
    }
)

# Cultura Japonesa (Shogi)
japanese_culture = ChessCulture(
    name="Japão Feudal",
    description="A tradição do shogi, o xadrez japonês",
    historical_period="1000-1600 D.C.",
    themes={
        "Bushido": CulturalTheme(
            name="Bushido",
            description="O código dos samurais",
            weight=0.9,
            narratives=[
                "Seguindo o bushido, {piece} age com honra",
                "Com a disciplina do samurai, {piece} executa seu movimento",
                "No caminho do guerreiro, {piece} avança"
            ],
            historical_context="O código de conduta dos samurais"
        ),
        "Harmonia": CulturalTheme(
            name="Harmonia",
            description="O conceito de wa (harmonia)",
            weight=0.8,
            narratives=[
                "Em harmonia com o tabuleiro, {piece} encontra seu lugar",
                "Como bambu ao vento, {piece} se adapta",
                "Mantendo o wa, {piece} move-se com graça"
            ],
            historical_context="Conceito fundamental da cultura japonesa"
        ),
        "Renascimento": CulturalTheme(
            name="Renascimento",
            description="A capacidade de renascer em batalha",
            weight=0.7,
            narratives=[
                "Como fênix renascida, {piece} retorna à batalha",
                "O espírito do guerreiro renasce em {piece}",
                "Da derrota surge nova força em {piece}"
            ],
            historical_context="Baseado no conceito de peças drops do shogi"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Gyoku",
            description="A joia preciosa (rei)",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="O rei no shogi"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Hisha",
            description="O carro voador",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Uma das peças mais poderosas do shogi"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Kakugyo",
            description="O ministro diagonal",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="O bispo no shogi"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Keima",
            description="O cavalo honorável",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.7,
            historical_significance="O cavalo no shogi"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Yari",
            description="A lança samurai",
            piece_type=PieceType.ROOK,
            cultural_value=0.6,
            historical_significance="A torre no shogi"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Fu",
            description="O soldado de infantaria",
            piece_type=PieceType.PAWN,
            cultural_value=0.4,
            historical_significance="O peão no shogi"
        )
    }
)
