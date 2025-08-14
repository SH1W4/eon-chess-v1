#!/bin/bash

# 🧠 AEON CHESS - ARKITECT Integration
# Script de Instalação Completa

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Banner
echo -e "${PURPLE}"
cat << 'EOF'
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🧠 AEON CHESS - ARKITECT                  ║
    ║                    Sistema Inteligente                       ║
    ║                    Instalador Completo                       ║
    ╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar sistema operacional
check_os() {
    log "Verificando sistema operacional..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log "Sistema Linux detectado"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log "Sistema macOS detectado"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
        log "Sistema Windows detectado"
    else
        error "Sistema operacional não suportado: $OSTYPE"
    fi
}

# Verificar dependências
check_dependencies() {
    log "Verificando dependências..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker não encontrado. Instale o Docker primeiro."
    else
        DOCKER_VERSION=$(docker --version)
        log "Docker encontrado: $DOCKER_VERSION"
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
    else
        COMPOSE_VERSION=$(docker-compose --version)
        log "Docker Compose encontrado: $COMPOSE_VERSION"
    fi
    
    # Verificar Node.js (para desenvolvimento)
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log "Node.js encontrado: $NODE_VERSION"
    else
        warn "Node.js não encontrado (opcional para desenvolvimento)"
    fi
    
    # Verificar Git
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        log "Git encontrado: $GIT_VERSION"
    else
        warn "Git não encontrado (opcional)"
    fi
}

# Criar estrutura de diretórios
create_directories() {
    log "Criando estrutura de diretórios..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p backups
    
    log "Diretórios criados: logs/, data/, backups/"
}

# Configurar variáveis de ambiente
setup_environment() {
    log "Configurando variáveis de ambiente..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# 🧠 AEON CHESS - ARKITECT Configuration
NODE_ENV=production
ARKITECT_ENABLED=true
NEXT_TELEMETRY_DISABLED=1
PORT=3000

# Redis Configuration (opcional)
REDIS_URL=redis://redis:6379

# Logging
LOG_LEVEL=info
LOG_FILE=logs/aeon-chess.log

# Performance
ARKITECT_PERFORMANCE_MODE=true
ARKITECT_ANALYSIS_INTERVAL=1000
EOF
        log "Arquivo .env criado"
    else
        log "Arquivo .env já existe"
    fi
}

# Construir e iniciar containers
build_and_start() {
    log "Construindo e iniciando containers..."
    
    # Parar containers existentes
    docker-compose down 2>/dev/null || true
    
    # Construir imagem
    log "Construindo imagem Docker..."
    docker-compose build --no-cache
    
    # Iniciar serviços
    log "Iniciando serviços..."
    docker-compose up -d
    
    # Aguardar inicialização
    log "Aguardando inicialização dos serviços..."
    sleep 10
    
    # Verificar status
    check_status
}

# Verificar status dos serviços
check_status() {
    log "Verificando status dos serviços..."
    
    # Verificar container principal
    if docker-compose ps | grep -q "Up"; then
        log "✅ Serviços iniciados com sucesso"
    else
        error "❌ Falha ao iniciar serviços"
    fi
    
    # Verificar health check
    log "Verificando health check..."
    sleep 5
    
    if curl -f http://localhost:3000/chess-test > /dev/null 2>&1; then
        log "✅ Health check passou"
    else
        warn "⚠️ Health check falhou - aguardando mais tempo..."
        sleep 10
        if curl -f http://localhost:3000/chess-test > /dev/null 2>&1; then
            log "✅ Health check passou após aguardar"
        else
            error "❌ Health check falhou definitivamente"
        fi
    fi
}

# Mostrar informações finais
show_final_info() {
    echo -e "${CYAN}"
    cat << 'EOF'
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎉 INSTALAÇÃO CONCLUÍDA!                  ║
    ╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    log "🧠 AEON CHESS com ARKITECT está rodando!"
    echo
    echo -e "${BLUE}📊 Informações do Sistema:${NC}"
    echo -e "   🌐 URL Principal: ${GREEN}http://localhost:3000${NC}"
    echo -e "   🧪 Página de Teste: ${GREEN}http://localhost:3000/chess-test${NC}"
    echo -e "   🔧 Status: ${GREEN}docker-compose ps${NC}"
    echo -e "   📝 Logs: ${GREEN}docker-compose logs -f${NC}"
    echo
    echo -e "${BLUE}🎮 Como Usar:${NC}"
    echo -e "   1. Acesse: ${GREEN}http://localhost:3000/chess-test${NC}"
    echo -e "   2. Teste o tabuleiro ARKITECT"
    echo -e "   3. Verifique a análise inteligente"
    echo -e "   4. Use os controles de debug"
    echo
    echo -e "${BLUE}🔧 Comandos Úteis:${NC}"
    echo -e "   Parar: ${GREEN}docker-compose down${NC}"
    echo -e "   Reiniciar: ${GREEN}docker-compose restart${NC}"
    echo -e "   Logs: ${GREEN}docker-compose logs -f aeon-chess${NC}"
    echo -e "   Status: ${GREEN}docker-compose ps${NC}"
    echo
    echo -e "${BLUE}📚 Documentação:${NC}"
    echo -e "   ARKITECT Integration: ${GREEN}ARKITECT_INTEGRATION.md${NC}"
    echo -e "   Verification Report: ${GREEN}VERIFICATION_REPORT.md${NC}"
    echo
    echo -e "${PURPLE}🚀 Sistema pronto para uso!${NC}"
}

# Função principal
main() {
    log "Iniciando instalação do AEON CHESS com ARKITECT..."
    
    check_os
    check_dependencies
    create_directories
    setup_environment
    build_and_start
    show_final_info
    
    log "Instalação concluída com sucesso!"
}

# Executar função principal
main "$@"
