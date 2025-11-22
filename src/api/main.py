from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
import os

# Adicionar diretório raiz ao path para importar módulos src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.cultural.storyteller import StoryGenerator
from src.cultural.narrative import CulturalContext, NarrativeStyle

# Metadata para documentação OpenAPI
tags_metadata = [
    {
        "name": "health",
        "description": "Endpoints de verificação de status do sistema",
    },
    {
        "name": "narrative",
        "description": "Sistema de geração de narrativas culturais para partidas de xadrez",
    },
]

app = FastAPI(
    title="AEON CHESS Engine API",
    description="""
## 🏰 Motor de Xadrez com IA e Narrativa Cultural

API backend para o AEON CHESS, uma plataforma de xadrez que combina:
- 🧠 **Inteligência Artificial** avançada usando python-chess
- 📖 **Narrativas Culturais** adaptativas baseadas em contexto histórico
- 🎮 **Sistema de Gamificação** com progressão e conquistas

### Recursos Principais
* Geração de narrativas contextualizadas para aberturas de jogo
* Suporte a múltiplos estilos narrativos (histórico, épico, educacional)
* Integração com tabuleiro avançado usando python-chess engine
* API RESTful com documentação automática

### Tecnologias
- FastAPI (framework web)
- Python-chess (engine de xadrez)
- Pydantic (validação de dados)
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados com documentação
class NarrativeRequest(BaseModel):
    """Configuração para geração de narrativa cultural"""
    region: str = Field(
        default="europeu",
        description="Região cultural para contextualizar a narrativa",
        example="europeu"
    )
    era: str = Field(
        default="medieval",
        description="Período histórico da narrativa",
        example="medieval"
    )
    style: str = Field(
        default="historical",
        description="Estilo narrativo (historical, epic, educational)",
        example="historical"
    )
    language: str = Field(
        default="pt-br",
        description="Idioma da narrativa gerada",
        example="pt-br"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "region": "europeu",
                "era": "renascimento",
                "style": "epic",
                "language": "pt-br"
            }
        }

class MoveEvent(BaseModel):
    """Evento de movimento de peça no tabuleiro"""
    move_number: int = Field(..., description="Número do movimento na partida", example=1)
    piece_type: str = Field(..., description="Tipo da peça (P, N, B, R, Q, K)", example="P")
    color: str = Field(..., description="Cor da peça (white/black)", example="white")
    from_pos: List[int] = Field(..., description="Posição de origem [linha, coluna]", example=[6, 4])
    to_pos: List[int] = Field(..., description="Posição de destino [linha, coluna]", example=[4, 4])
    is_capture: bool = Field(..., description="Se o movimento captura uma peça", example=False)
    is_check: bool = Field(..., description="Se o movimento resulta em xeque", example=False)
    is_checkmate: bool = Field(..., description="Se o movimento resulta em xeque-mate", example=False)
    
    class Config:
        schema_extra = {
            "example": {
                "move_number": 1,
                "piece_type": "P",
                "color": "white",
                "from_pos": [6, 4],
                "to_pos": [4, 4],
                "is_capture": False,
                "is_check": False,
                "is_checkmate": False
            }
        }

# Instância global do gerador (simplificado para demo)
# Em produção, isso seria gerenciado por sessão
generator = None

@app.get(
    "/health",
    tags=["health"],
    summary="Verificar status do sistema",
    description="Retorna o status de saúde da API e informações sobre o engine",
    response_description="Status do sistema e versão do engine"
)
async def health_check():
    """
    Endpoint de health check para monitoramento do sistema.
    
    Retorna:
    - **status**: Estado atual do sistema (online/offline)
    - **engine**: Nome e versão do motor de xadrez
    """
    return {
        "status": "online",
        "engine": "AEON CHESS v1.0",
        "api_version": "1.0.0",
        "features": ["narrative_generation", "chess_engine", "cultural_context"]
    }

from src.core.board import Board

@app.post(
    "/api/narrative/init",
    tags=["narrative"],
    summary="Inicializar geração de narrativa",
    description="""
    Inicializa o sistema de narrativa cultural com contexto específico e gera
    uma abertura narrativa para uma nova partida de xadrez.
    
    O sistema adapta a narrativa baseado em:
    - **Região cultural**: Contexto geográfico/cultural
    - **Era histórica**: Período temporal
    - **Estilo narrativo**: Tom e abordagem da narrativa
    - **Idioma**: Língua de saída
    """,
    response_description="Narrativa de abertura gerada",
    responses={
        200: {
            "description": "Narrativa gerada com sucesso",
            "content": {
                "application/json": {
                    "example": {
                        "opening": "No ano de medieval, dois reinos poderosos se encontram em um campo de batalha singular..."
                    }
                }
            }
        },
        400: {
            "description": "Parâmetros inválidos",
            "content": {
                "application/json": {
                    "example": {"detail": "Estilo narrativo inválido"}
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {"detail": "Erro ao gerar narrativa"}
                }
            }
        }
    }
)
async def init_narrative(request: NarrativeRequest):
    """
    Inicializa o gerador de narrativas e cria uma abertura contextualizada.
    
    Este endpoint:
    1. Configura o contexto cultural baseado nos parâmetros
    2. Inicializa um tabuleiro de xadrez na posição inicial
    3. Gera uma narrativa de abertura adaptada ao contexto
    
    Args:
        request: Configuração de narrativa (região, era, estilo, idioma)
        
    Returns:
        dict: Objeto contendo a narrativa de abertura gerada
        
    Raises:
        HTTPException 400: Se o estilo narrativo for inválido
        HTTPException 500: Se houver erro na geração da narrativa
    """
    global generator
    try:
        style_enum = NarrativeStyle(request.style)
        context = CulturalContext(
            region=request.region,
            era=request.era,
            style=style_enum,
            language=request.language
        )
        generator = StoryGenerator(context)
        board = Board()  # Criar tabuleiro inicial
        opening = generator.generate_game_opening(board)
        return {"opening": opening, "context": request.dict()}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Estilo narrativo inválido. Opções: historical, epic, educational"
        )
    except Exception as e:
        import traceback
        error_msg = f"Erro ao gerar narrativa: {str(e)}"
        print(f"[ERROR] {error_msg}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post(
    "/api/narrative/move",
    tags=["narrative"],
    summary="Gerar narrativa para movimento",
    description="""
    Gera uma narrativa contextualizada para um movimento específico no jogo.
    
    A narrativa é adaptada baseado em:
    - Tipo de peça movida
    - Se houve captura
    - Se resultou em xeque ou xeque-mate
    - Contexto cultural previamente configurado
    """,
    response_description="Narrativa do movimento gerada"
)
async def generate_move_narrative(event: MoveEvent):
    """
    Gera narrativa para um movimento de peça.
    
    Args:
        event: Informações sobre o movimento (peça, posições, capturas, etc.)
        
    Returns:
        dict: Objeto contendo a narrativa do movimento
    """
    global generator
    if not generator:
        # Inicializar com padrão se não existir
        context = CulturalContext("europeu", "medieval", NarrativeStyle.HISTORICAL, "pt-br")
        generator = StoryGenerator(context)
    
    # Gerar narrativa baseada no evento
    piece_names = {
        "P": "Peão", "N": "Cavalo", "B": "Bispo",
        "R": "Torre", "Q": "Rainha", "K": "Rei"
    }
    piece_name = piece_names.get(event.piece_type, event.piece_type)
    
    narrative = f"O {piece_name} move-se de {event.from_pos} para {event.to_pos}."
    
    if event.is_capture:
        narrative += " Uma captura decisiva!"
    if event.is_check:
        narrative += " Xeque ao rei!"
    if event.is_checkmate:
        narrative += " Xeque-mate! A partida termina!"
    
    return {
        "narrative": narrative,
        "move_number": event.move_number,
        "piece": piece_name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
