#!/usr/bin/env python3
"""
API REST Principal Simplificada - AEON Chess
Servidor FastAPI básico para teste inicial
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel
import logging
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

class GameRequest(BaseModel):
    player_name: str
    cultural_profile: str = "persian"
    ai_difficulty: str = "adaptive"

class GameResponse(BaseModel):
    game_id: str
    status: str
    message: str

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 AEON Chess API starting up...")
    yield
    # Shutdown
    logger.info("👋 AEON Chess API shutting down...")

# Criar aplicação FastAPI
app = FastAPI(
    title="AEON Chess API",
    description="Backend API for AEON Chess - Adaptive Chess Engine",
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

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="0.2.1"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AEON Chess API",
        "version": "0.2.1",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Create game endpoint
@app.post("/api/v1/game/create", response_model=GameResponse)
async def create_game(request: GameRequest):
    """Create a new game"""
    game_id = str(uuid.uuid4())
    
    logger.info(f"Creating new game {game_id} for player {request.player_name}")
    
    return GameResponse(
        game_id=game_id,
        status="created",
        message=f"Game created for {request.player_name} with {request.cultural_profile} profile"
    )

# Get game endpoint
@app.get("/api/v1/game/{game_id}")
async def get_game(game_id: str):
    """Get game by ID"""
    return {
        "game_id": game_id,
        "status": "active",
        "message": "Game endpoint placeholder"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
