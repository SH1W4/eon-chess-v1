#!/usr/bin/env python3
"""
API REST Simplificada - AEON Chess
Servidor FastAPI básico para staging
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="AEON Chess API",
    description="API para o jogo de xadrez AEON",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de health check
@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "aeon-chess-backend",
        "version": "1.0.0",
        "timestamp": "2025-08-12T19:52:00Z"
    }

# Endpoint raiz
@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "AEON Chess Backend API",
        "version": "1.0.0",
        "status": "running"
    }

# Endpoint de métricas para Prometheus
@app.get("/metrics")
async def metrics():
    """Endpoint de métricas básicas"""
    return {
        "requests_total": 0,
        "requests_active": 0,
        "uptime_seconds": 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
