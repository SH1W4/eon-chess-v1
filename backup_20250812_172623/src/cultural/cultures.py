from dataclasses import dataclass
from typing import Dict, List, Optional
from core.board.board import PieceType
from cultural.culture_framework import ChessCulture, CulturalTheme, PieceCulturalIdentity

# Cultura Persa
persian_culture = ChessCulture(
    name="Império Persa",
    description="A sofisticada cultura do xadrez persa (shatranj), berço do xadrez moderno",
    historical_period="224-651 D.C.",
    themes={
        "Sabedoria Antiga": CulturalTheme(
            name="Sabedoria Antiga",
            description="A tradição milenar do xadrez persa",
            weight=0.9,
            narratives=[
                "Com a sabedoria dos antigos reis, {piece} move-se com propósito",
                "Seguindo as tradições do shatranj, {piece} executa sua estratégia",
                "Como nos jardins de Persépolis, {piece} tece seu caminho"
            ],
            historical_context="Baseado no desenvolvimento do shatranj na Pérsia antiga"
        ),
        "Poder Real": CulturalTheme(
            name="Poder Real",
            description="A autoridade e majestade da corte persa",
            weight=0.8,
            narratives=[
                "Com a autoridade do Xá, {piece} comanda o campo",
                "Como um nobre da corte persa, {piece} demonstra sua influência",
                "Pela glória do império, {piece} avança com dignidade"
            ],
            historical_context="Reflete a estrutura hierárquica da corte persa"
        ),
        "Arte da Guerra": CulturalTheme(
            name="Arte da Guerra",
            description="As táticas militares persas",
            weight=0.7,
            narratives=[
                "Como os Imortais persas, {piece} mantém sua posição",
                "Com a precisão dos arqueiros persas, {piece} domina o campo",
                "Seguindo a arte da guerra persa, {piece} executa sua manobra"
            ],
            historical_context="Baseado nas táticas militares do exército persa"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Xá",
            description="O rei persa, centro do poder imperial",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="O título dos imperadores persas"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Vazir",
            description="O conselheiro principal do Xá",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Origem do nome 'Vizir', conselheiro real"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Pil",
            description="O elefante de guerra persa",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="Nome original do bispo no shatranj"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Asb",
            description="O cavaleiro persa",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.7,
            historical_significance="Cavalaria persa, famosa por sua excelência"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Rukh",
            description="A carruagem de guerra",
            piece_type=PieceType.ROOK,
            cultural_value=0.6,
            historical_significance="Origem do nome 'Rook' no xadrez"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Sarbaz",
            description="O soldado persa",
            piece_type=PieceType.PAWN,
            cultural_value=0.4,
            historical_significance="Infantaria do exército persa"
        )
    }
)

# Cultura Mongol
mongol_culture = ChessCulture(
    name="Império Mongol",
    description="A cultura dos conquistadores das estepes",
    historical_period="1206-1368 D.C.",
    themes={
        "Conquista": CulturalTheme(
            name="Conquista",
            description="O espírito conquistador mongol",
            weight=0.9,
            narratives=[
                "Como as hordas douradas, {piece} avança sem medo",
                "Com a força das estepes, {piece} domina o território",
                "Pela glória do Khan, {piece} subjuga seus inimigos"
            ],
            historical_context="Baseado nas conquistas do império mongol"
        ),
        "Mobilidade": CulturalTheme(
            name="Mobilidade",
            description="A extraordinária mobilidade dos guerreiros mongóis",
            weight=0.8,
            narratives=[
                "Veloz como um arqueiro montado, {piece} ataca com precisão",
                "Com a rapidez das estepes, {piece} muda de posição",
                "Como os cavaleiros mongóis, {piece} executa uma manobra veloz"
            ],
            historical_context="Reflete a supremacia da cavalaria mongol"
        ),
        "União das Tribos": CulturalTheme(
            name="União das Tribos",
            description="A unificação das tribos sob o Grande Khan",
            weight=0.7,
            narratives=[
                "Unido sob a bandeira do Khan, {piece} avança com propósito",
                "Com a força das tribos unidas, {piece} mostra seu poder",
                "Pela honra do clã, {piece} defende sua posição"
            ],
            historical_context="Baseado na unificação das tribos mongóis"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Khan",
            description="O líder supremo dos mongóis",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="Título dos imperadores mongóis"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Khatun",
            description="A rainha mongol",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Título das rainhas mongóis"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Shaman",
            description="O líder espiritual mongol",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="Líderes espirituais das tribos"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Noyan",
            description="O comandante da cavalaria",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.8,
            historical_significance="Comandantes militares mongóis"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Ordu",
            description="A horda mongol",
            piece_type=PieceType.ROOK,
            cultural_value=0.7,
            historical_significance="As divisões do exército mongol"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Cerig",
            description="O guerreiro mongol",
            piece_type=PieceType.PAWN,
            cultural_value=0.5,
            historical_significance="Guerreiros das tribos mongóis"
        )
    }
)

# Cultura Chinesa
chinese_culture = ChessCulture(
    name="Império Chinês",
    description="A antiga e refinada cultura do xiangqi (xadrez chinês)",
    historical_period="960-1279 D.C. (Dinastia Song)",
    themes={
        "Harmonia Celestial": CulturalTheme(
            name="Harmonia Celestial",
            description="O equilíbrio entre Céu e Terra",
            weight=0.9,
            narratives=[
                "Em harmonia com o Tao, {piece} encontra seu caminho",
                "Seguindo o fluxo do Qi, {piece} move-se naturalmente",
                "Como o equilíbrio do Yin e Yang, {piece} mantém a ordem"
            ],
            historical_context="Baseado na filosofia tradicional chinesa"
        ),
        "Estratégia Militar": CulturalTheme(
            name="Estratégia Militar",
            description="A arte da guerra segundo Sun Tzu",
            weight=0.8,
            narratives=[
                "Como ensina Sun Tzu, {piece} conquista sem batalhar",
                "Com a sabedoria dos antigos estrategistas, {piece} planeja seu movimento",
                "Seguindo a Arte da Guerra, {piece} posiciona-se com precisão"
            ],
            historical_context="Baseado nos princípios de Sun Tzu"
        ),
        "Mandato do Céu": CulturalTheme(
            name="Mandato do Céu",
            description="A autoridade divina do imperador",
            weight=0.7,
            narratives=[
                "Sob o Mandato do Céu, {piece} exerce sua autoridade",
                "Com a bênção dos ancestrais, {piece} protege o império",
                "Como guardião da ordem celestial, {piece} mantém a harmonia"
            ],
            historical_context="Conceito fundamental do poder imperial chinês"
        )
    },
    piece_identities={
        PieceType.KING: PieceCulturalIdentity(
            name="Imperador",
            description="O Filho do Céu",
            piece_type=PieceType.KING,
            cultural_value=1.0,
            historical_significance="O imperador chinês, detentor do Mandato do Céu"
        ),
        PieceType.QUEEN: PieceCulturalIdentity(
            name="Conselheiro",
            description="O sábio conselheiro imperial",
            piece_type=PieceType.QUEEN,
            cultural_value=0.9,
            historical_significance="Baseado no Xiangqi, onde não existe rainha"
        ),
        PieceType.BISHOP: PieceCulturalIdentity(
            name="Erudito",
            description="O oficial letrado",
            piece_type=PieceType.BISHOP,
            cultural_value=0.7,
            historical_significance="Os oficiais da burocracia imperial"
        ),
        PieceType.KNIGHT: PieceCulturalIdentity(
            name="Cavalo de Ferro",
            description="A cavalaria imperial",
            piece_type=PieceType.KNIGHT,
            cultural_value=0.7,
            historical_significance="A importante cavalaria chinesa"
        ),
        PieceType.ROOK: PieceCulturalIdentity(
            name="Carruagem",
            description="A carruagem de guerra",
            piece_type=PieceType.ROOK,
            cultural_value=0.6,
            historical_significance="Elemento crucial nos exércitos chineses"
        ),
        PieceType.PAWN: PieceCulturalIdentity(
            name="Soldado",
            description="O soldado imperial",
            piece_type=PieceType.PAWN,
            cultural_value=0.4,
            historical_significance="A infantaria do exército chinês"
        )
    }
)
