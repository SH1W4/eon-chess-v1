#!/usr/bin/env python3
"""
API REST Principal - AEON Chess
Servidor FastAPI com endpoints de jogo, autenticação e WebSocket
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
import json
import asyncio
import uuid
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class MoveRequest(BaseModel):
    from_pos: str
    to_pos: str
    promotion: Optional[str] = None

class GameRequest(BaseModel):
    player_name: str
    cultural_profile: str = "persian"
    ai_difficulty: str = "adaptive"
    time_control: Optional[int] = 900  # 15 minutos

class GameResponse(BaseModel):
    game_id: str
    status: str
    board_state: Dict[str, Any]
    current_turn: str
    cultural_profile: str
    narrative: Optional[str] = None

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

# Configurações
SECRET_KEY = "aeon-chess-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.game_connections: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str, game_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
        if game_id not in self.game_connections:
            self.game_connections[game_id] = []
        self.game_connections[game_id].append(client_id)
        
        logger.info(f"Client {client_id} connected to game {game_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
        # Remover das conexões de jogo
        for game_id, clients in self.game_connections.items():
            if client_id in clients:
                clients.remove(client_id)
                
        logger.info(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

    async def broadcast_to_game(self, message: str, game_id: str):
        if game_id in self.game_connections:
            for client_id in self.game_connections[game_id]:
                if client_id in self.active_connections:
                    await self.active_connections[client_id].send_text(message)

# Gerenciador de jogos
class GameManager:
    def __init__(self):
        self.games: Dict[str, Dict[str, Any]] = {}
        self.user_games: Dict[str, List[str]] = {}

    def create_game(self, user_id: str, config: GameRequest) -> str:
        game_id = str(uuid.uuid4())
        
        self.games[game_id] = {
            "id": game_id,
            "white_player": user_id,
            "black_player": "ai",
            "status": "active",
            "created_at": datetime.now(),
            "config": config.dict(),
            "moves": [],
            "current_turn": "white",
            "board_state": self._initialize_board(),
            "cultural_profile": config.cultural_profile,
            "ai_difficulty": config.ai_difficulty,
            "time_white": config.time_control,
            "time_black": config.time_control
        }
        
        if user_id not in self.user_games:
            self.user_games[user_id] = []
        self.user_games[user_id].append(game_id)
        
        return game_id

    def _initialize_board(self) -> Dict[str, Any]:
        """Inicializa o estado do tabuleiro"""
        return {
            "a1": {"type": "rook", "color": "white"},
            "b1": {"type": "knight", "color": "white"},
            "c1": {"type": "bishop", "color": "white"},
            "d1": {"type": "queen", "color": "white"},
            "e1": {"type": "king", "color": "white"},
            "f1": {"type": "bishop", "color": "white"},
            "g1": {"type": "knight", "color": "white"},
            "h1": {"type": "rook", "color": "white"},
            "a2": {"type": "pawn", "color": "white"},
            "b2": {"type": "pawn", "color": "white"},
            "c2": {"type": "pawn", "color": "white"},
            "d2": {"type": "pawn", "color": "white"},
            "e2": {"type": "pawn", "color": "white"},
            "f2": {"type": "pawn", "color": "white"},
            "g2": {"type": "pawn", "color": "white"},
            "h2": {"type": "pawn", "color": "white"},
            "a7": {"type": "pawn", "color": "black"},
            "b7": {"type": "pawn", "color": "black"},
            "c7": {"type": "pawn", "color": "black"},
            "d7": {"type": "pawn", "color": "black"},
            "e7": {"type": "pawn", "color": "black"},
            "f7": {"type": "pawn", "color": "black"},
            "g7": {"type": "pawn", "color": "black"},
            "h7": {"type": "pawn", "color": "black"},
            "a8": {"type": "rook", "color": "black"},
            "b8": {"type": "knight", "color": "black"},
            "c8": {"type": "bishop", "color": "black"},
            "d8": {"type": "queen", "color": "black"},
            "e8": {"type": "king", "color": "black"},
            "f8": {"type": "bishop", "color": "black"},
            "g8": {"type": "knight", "color": "black"},
            "h8": {"type": "rook", "color": "black"}
        }

    def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        return self.games.get(game_id)

    def make_move(self, game_id: str, move: MoveRequest) -> Dict[str, Any]:
        game = self.games.get(game_id)
        if not game:
            raise ValueError("Game not found")
        
        # Validar movimento (simplificado)
        piece = game["board_state"].get(move.from_pos)
        if not piece:
            raise ValueError("No piece at from position")
        
        # Executar movimento
        game["board_state"][move.to_pos] = piece
        del game["board_state"][move.from_pos]
        
        # Adicionar à história
        game["moves"].append({
            "from": move.from_pos,
            "to": move.to_pos,
            "piece": piece["type"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Alternar turno
        game["current_turn"] = "black" if game["current_turn"] == "white" else "white"
        
        return game

# Inicializar gerenciadores
manager = ConnectionManager()
game_manager = GameManager()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AEON Chess API Server...")
    yield
    # Shutdown
    logger.info("Shutting down AEON Chess API Server...")

# Criar aplicação FastAPI
app = FastAPI(
    title="AEON Chess API",
    description="API REST para o sistema de xadrez adaptativo AEON",
    version="0.2.1",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid authentication")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication")

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "AEON Chess API",
        "version": "0.2.1",
        "status": "active",
        "endpoints": {
            "auth": "/auth/login",
            "games": "/api/games",
            "websocket": "/ws/{game_id}"
        }
    }

@app.post("/auth/login", response_model=AuthResponse)
async def login(auth: AuthRequest):
    # Simplificado - em produção, verificar contra banco de dados
    if auth.username and len(auth.password) >= 6:
        access_token = create_access_token(data={"sub": auth.username})
        return AuthResponse(
            access_token=access_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/games", response_model=GameResponse)
async def create_game(
    game_config: GameRequest,
    current_user: str = Depends(verify_token)
):
    """Criar novo jogo"""
    game_id = game_manager.create_game(current_user, game_config)
    game = game_manager.get_game(game_id)
    
    return GameResponse(
        game_id=game_id,
        status=game["status"],
        board_state=game["board_state"],
        current_turn=game["current_turn"],
        cultural_profile=game["cultural_profile"]
    )

@app.get("/api/games/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: str,
    current_user: str = Depends(verify_token)
):
    """Obter estado do jogo"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameResponse(
        game_id=game_id,
        status=game["status"],
        board_state=game["board_state"],
        current_turn=game["current_turn"],
        cultural_profile=game["cultural_profile"]
    )

@app.post("/api/games/{game_id}/moves")
async def make_move(
    game_id: str,
    move: MoveRequest,
    current_user: str = Depends(verify_token)
):
    """Fazer movimento"""
    try:
        game = game_manager.make_move(game_id, move)
        
        # Broadcast via WebSocket
        await manager.broadcast_to_game(
            json.dumps({
                "type": "move",
                "data": {
                    "from": move.from_pos,
                    "to": move.to_pos,
                    "current_turn": game["current_turn"]
                }
            }),
            game_id
        )
        
        return {
            "success": True,
            "board_state": game["board_state"],
            "current_turn": game["current_turn"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/games/{game_id}/analysis")
async def analyze_position(
    game_id: str,
    current_user: str = Depends(verify_token)
):
    """Analisar posição atual"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Análise simplificada
    return {
        "evaluation": 0.0,
        "best_moves": ["e2e4", "d2d4", "g1f3"],
        "material_balance": 0,
        "position_type": "opening",
        "cultural_insights": {
            "persian": "Posição favorável para desenvolvimento harmonioso",
            "mongol": "Oportunidade para ataque rápido no flanco"
        }
    }

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket para atualizações em tempo real"""
    client_id = str(uuid.uuid4())
    await manager.connect(websocket, client_id, game_id)
    
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Processar mensagem
            if message["type"] == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong"}),
                    client_id
                )
            elif message["type"] == "chat":
                await manager.broadcast_to_game(
                    json.dumps({
                        "type": "chat",
                        "user": client_id[:8],
                        "message": message["data"]
                    }),
                    game_id
                )
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast_to_game(
            json.dumps({
                "type": "user_disconnected",
                "user": client_id[:8]
            }),
            game_id
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_games": len(game_manager.games),
        "active_connections": len(manager.active_connections)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
