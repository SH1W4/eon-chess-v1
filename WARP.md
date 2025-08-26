# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## 🏗️ Architecture Overview

This is a sophisticated chess platform with a clear separation between the core engine and web interface:

### Core Engine Architecture
- `/src/ai/` - Advanced AI system with evaluation and caching components
- `/src/core/` - Core chess logic including board and evaluation engines
- `/src/cultural/` - Cultural narrative system with storytelling features
- `/src/quantum/` - Advanced quantum-inspired computation system
- `/src/traditional/` - Traditional chess components

### Tech Stack
- Python backend engine with OpenCV, PyTorch and chess-specific libraries
- Next.js/React frontend with TypeScript and Tailwind CSS
- PostgreSQL for main data storage
- Redis for caching and sessions
- Docker-based deployment with Docker Compose orchestration

## 🚀 Development Environment Setup

### System Requirements
- Docker Desktop with Docker Compose
- 4GB RAM minimum
- 2GB free disk space

### Quick Start
```bash
# Clone and deploy with automatic installer
git clone https://github.com/NEO-SH1W4/aeon-chess.git
cd aeon-chess
chmod +x install.sh
./install.sh

# Or deploy manually with Docker
docker-compose build --no-cache
docker-compose up -d
```

### Development URLs
- Main Application: http://localhost:3000
- Debug Interface: http://localhost:3000/chess-test

## 🧪 Testing & Validation

### Key Performance Metrics
- Response Time: < 5ms
- AI Accuracy: 85-95%
- System Efficiency: 90-95%
- Move Quality Rating: 0-100%

### Run Tests
```bash
# Execute all tests
pytest

# Debug console access
curl -f http://localhost:3000/chess-test

# View real-time logs
docker-compose logs -f aeon-chess
```

## 🔍 Diagnostic Commands

### Docker Management
```bash
# Check service status
docker-compose ps

# Service logs
docker-compose logs -f aeon-chess

# Resource monitoring
docker stats

# Rebuild and restart services
docker-compose up -d --build
```

### Specific Component Logs
```bash
# Error logs
docker-compose logs aeon-chess | grep ERROR

# Performance metrics
docker-compose logs aeon-chess | grep "ms"

# ARKITECT integration logs
docker-compose logs aeon-chess | grep ARKITECT
```

## 📝 Version Management

### Deploy New Version
```bash
# View available versions
git tag -l

# Deploy specific version
git checkout v1.0.1
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🔧 System Architecture Notes

1. The interface layer (`index.html` and JS files) is just a representation of the underlying system.
   Actual logic resides in the core engines.

2. Data flow sequence:
   - Interface captures user interaction
   - JS processors send to backend
   - Python API processes
   - Core Engine executes complex logic
   - Database stores/retrieves data
   - Response returns through chain

3. Key system components:
   - Core chess engine with advanced evaluation
   - Cultural narrative system
   - Visual effects engine
   - AI-driven analysis
   - ARKITECT integration

4. State and awareness are maintained through multiple layers:
   - Direct channel (immediate transfer)
   - Synchronous channel (near-zero latency)
   - Metacognitive channel (consciousness bridge)
