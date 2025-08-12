#!/bin/bash

# AEON Chess - Local Development Setup Script

set -e

echo "🚀 AEON Chess - Configuração do Ambiente Local"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Este script foi otimizado para macOS${NC}"
    exit 1
fi

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Check dependencies
echo -e "\n${YELLOW}1. Verificando dependências...${NC}"

if ! command_exists brew; then
    echo -e "${RED}Homebrew não encontrado. Instale em: https://brew.sh${NC}"
    exit 1
fi

if ! command_exists docker; then
    echo -e "${RED}Docker não encontrado. Instale Docker Desktop para Mac${NC}"
    exit 1
fi

# Install mkcert if not present
if ! command_exists mkcert; then
    echo "Instalando mkcert para certificados SSL locais..."
    brew install mkcert
    mkcert -install
fi

# 2. Setup local domain
echo -e "\n${YELLOW}2. Configurando domínio local...${NC}"

# Add to /etc/hosts if not present
if ! grep -q "aeon-chess.local" /etc/hosts; then
    echo "Adicionando aeon-chess.local ao /etc/hosts..."
    echo "127.0.0.1 aeon-chess.local" | sudo tee -a /etc/hosts
    echo -e "${GREEN}✓ Domínio configurado${NC}"
else
    echo -e "${GREEN}✓ Domínio já configurado${NC}"
fi

# 3. Generate SSL certificates
echo -e "\n${YELLOW}3. Gerando certificados SSL...${NC}"

cd certs
if [ ! -f "aeon-chess.local.pem" ]; then
    mkcert aeon-chess.local
    echo -e "${GREEN}✓ Certificados SSL gerados${NC}"
else
    echo -e "${GREEN}✓ Certificados SSL já existem${NC}"
fi
cd ..

# 4. Setup environment
echo -e "\n${YELLOW}4. Configurando variáveis de ambiente...${NC}"

if [ ! -f ".env.production" ]; then
    echo -e "${RED}Arquivo .env.production não encontrado${NC}"
    exit 1
fi

# Generate secure keys
if grep -q "aeon-chess-secret-key-production-2025-secure" .env.production; then
    echo "Gerando chaves secretas seguras..."
    SECRET_KEY=$(openssl rand -hex 32)
    JWT_SECRET=$(openssl rand -hex 32)
    
    # Create temp file
    cp .env.production .env.production.tmp
    
    # Replace keys
    sed -i '' "s/aeon-chess-secret-key-production-2025-secure/$SECRET_KEY/g" .env.production.tmp
    sed -i '' "s/aeon-jwt-secret-production-2025/$JWT_SECRET/g" .env.production.tmp
    
    mv .env.production.tmp .env.production
    echo -e "${GREEN}✓ Chaves secretas geradas${NC}"
fi

# 5. Build frontend
echo -e "\n${YELLOW}5. Build do frontend...${NC}"

if [ -d "frontend" ]; then
    echo "Construindo frontend otimizado..."
    docker compose -f docker-compose.production.yml build frontend-builder
    docker compose -f docker-compose.production.yml run --rm frontend-builder
    echo -e "${GREEN}✓ Frontend construído${NC}"
else
    echo -e "${RED}Diretório frontend não encontrado${NC}"
fi

# 6. Create necessary directories
echo -e "\n${YELLOW}6. Criando diretórios necessários...${NC}"

mkdir -p logs
mkdir -p data/postgres
mkdir -p data/redis

echo -e "${GREEN}✓ Diretórios criados${NC}"

# 7. Docker setup
echo -e "\n${YELLOW}7. Preparando Docker...${NC}"

# Check Docker daemon
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Docker não está rodando. Inicie o Docker Desktop${NC}"
    exit 1
fi

# Build images
echo "Construindo imagens Docker..."
docker compose -f docker-compose.production.yml build

echo -e "${GREEN}✓ Imagens Docker construídas${NC}"

# 8. Summary
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✅ Setup Completo!${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\nPara iniciar o AEON Chess:"
echo -e "  ${YELLOW}docker compose -f docker-compose.production.yml up -d${NC}"

echo -e "\nAcesse em:"
echo -e "  ${GREEN}https://aeon-chess.local${NC}"

echo -e "\nComandos úteis:"
echo -e "  Ver logs: ${YELLOW}docker compose -f docker-compose.production.yml logs -f${NC}"
echo -e "  Parar: ${YELLOW}docker compose -f docker-compose.production.yml down${NC}"
echo -e "  Status: ${YELLOW}docker compose -f docker-compose.production.yml ps${NC}"

echo -e "\n${YELLOW}Nota:${NC} Na primeira vez, aguarde alguns segundos para o banco de dados inicializar."
