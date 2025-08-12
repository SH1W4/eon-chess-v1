#!/usr/bin/env python3
"""
Endpoint de Health Check para AEON Chess
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "service": "aeon-chess-backend",
        "version": "1.0.0",
        "timestamp": "2025-08-12T19:52:00Z"
    }

@router.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "AEON Chess Backend API",
        "version": "1.0.0",
        "status": "running"
    }

