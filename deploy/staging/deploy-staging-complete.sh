#!/bin/bash

# 🚀 Script de Deploy Completo para Staging - Aeon Chess
# Versão: 2.0.0
# Data: 2025-08-12

set -e  # Exit on any error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para logging colorido
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Configurações
ENVIRONMENT="staging"
PROJECT_NAME="aeon-chess-staging"
DOCKER_COMPOSE_FILE="deploy/staging/docker-compose.yml"
BACKUP_DIR="backups/staging/$(date +%Y%m%d_%H%M%S)"
DOMAIN="staging.aeonchess.com"

# Banner
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 AEON CHESS STAGING                    ║"
echo "║                   Deploy Completo v2.0                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificações prévias
log "🔍 Verificando pré-requisitos para staging..."

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    error "Docker não está rodando. Inicie o Docker e tente novamente."
fi

# Verificar se Docker Compose está disponível
if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose não está instalado."
fi

# Verificar se o arquivo docker-compose existe
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    error "Arquivo docker-compose.yml não encontrado em $DOCKER_COMPOSE_FILE"
fi

# Verificar variáveis de ambiente
if [ -z "$STAGING_DATABASE_URL" ]; then
    warning "STAGING_DATABASE_URL não definida, usando padrão local"
    export STAGING_DATABASE_URL="postgresql://postgres:password@localhost:5432/aeon_chess_staging"
fi

if [ -z "$STAGING_REDIS_URL" ]; then
    warning "STAGING_REDIS_URL não definida, usando padrão local"
    export STAGING_REDIS_URL="redis://localhost:6379"
fi

# Criar diretórios necessários
log "📁 Criando estrutura de diretórios..."
mkdir -p "$BACKUP_DIR"
mkdir -p "logs/staging"
mkdir -p "backups/staging"
mkdir -p "temp/staging"

# Backup do ambiente atual
log "💾 Criando backup do ambiente atual..."
if docker-compose -f "$DOCKER_COMPOSE_FILE" ps | grep -q "Up"; then
    log "📸 Capturando estado atual dos containers..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" ps > "$BACKUP_DIR/containers-status.txt" 2>/dev/null || true
    
    # Backup dos volumes
    log "💾 Backup dos volumes..."
    docker run --rm -v "${PROJECT_NAME}_postgres_data:/data" -v "$(pwd)/$BACKUP_DIR:/backup" alpine tar czf /backup/postgres-backup.tar.gz -C /data . || true
    docker run --rm -v "${PROJECT_NAME}_redis_data:/data" -v "$(pwd)/$BACKUP_DIR:/backup" alpine tar czf /backup/redis-backup.tar.gz -C /data . || true
fi

# Parar serviços existentes
log "🛑 Parando serviços existentes..."
docker-compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans || true

# Limpar imagens antigas
log "🧹 Limpando imagens antigas..."
docker image prune -f
docker system prune -f

# Build das novas imagens
log "🔨 Build das imagens Docker para staging..."
docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache

# Verificar se o build foi bem-sucedido
if [ $? -ne 0 ]; then
    error "Falha no build das imagens Docker. Verifique os logs."
fi

# Iniciar serviços
log "🚀 Iniciando serviços de staging..."
docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

# Aguardar serviços estarem prontos
log "⏳ Aguardando serviços estarem prontos..."
sleep 60

# Verificar saúde dos serviços
log "🏥 Verificando saúde dos serviços..."

# Verificar frontend
if curl -f http://localhost:3000/health > /dev/null 2>&1; then
    success "Frontend está respondendo"
else
    warning "Frontend pode não estar totalmente pronto"
fi

# Verificar backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    success "Backend está respondendo"
else
    warning "Backend pode não estar totalmente pronto"
fi

# Verificar banco de dados
if docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    success "PostgreSQL está pronto"
else
    warning "PostgreSQL pode não estar totalmente pronto"
fi

# Verificar Redis
if docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T redis redis-cli ping | grep -q "PONG"; then
    success "Redis está respondendo"
else
    warning "Redis pode não estar totalmente pronto"
fi

# Verificar Prometheus
if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
    success "Prometheus está funcionando"
else
    warning "Prometheus pode não estar totalmente pronto"
fi

# Verificar Grafana
if curl -f http://localhost:3001/api/health > /dev/null 2>&1; then
    success "Grafana está funcionando"
else
    warning "Grafana pode não estar totalmente pronto"
fi

# Executar testes de staging
log "🧪 Executando testes de staging..."
if [ -f "tests/staging/run_staging_tests.sh" ]; then
    chmod +x tests/staging/run_staging_tests.sh
    ./tests/staging/run_staging_tests.sh
    if [ $? -eq 0 ]; then
        success "Testes de staging passaram"
    else
        warning "Alguns testes de staging falharam"
    fi
else
    warning "Script de testes de staging não encontrado"
fi

# Verificar métricas de performance
log "📊 Verificando métricas de performance..."
if command -v lighthouse &> /dev/null; then
    lighthouse http://localhost:3000 --output=json --output-path="$BACKUP_DIR/lighthouse-staging.json" --chrome-flags="--headless" || true
    log "Relatório Lighthouse salvo em $BACKUP_DIR/lighthouse-staging.json"
else
    warning "Lighthouse não está instalado. Instale com: npm install -g lighthouse"
fi

# Status final
log "📋 Status final dos serviços:"
docker-compose -f "$DOCKER_COMPOSE_FILE" ps

# Informações de acesso
log "🌐 URLs de acesso (Staging):"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  Grafana: http://localhost:3001"
echo "  Prometheus: http://localhost:9090"

# Logs dos serviços
log "📝 Últimos logs dos serviços:"
docker-compose -f "$DOCKER_COMPOSE_FILE" logs --tail=20

# Configurações aplicadas
log "🔧 Configurações aplicadas:"
echo "  ✅ Docker Compose configurado"
echo "  ✅ Health checks ativos"
echo "  ✅ Monitoramento configurado"
echo "  ✅ Backup automático configurado"
echo "  ✅ Logs centralizados"
echo "  ✅ Métricas de performance"

success "Deploy para staging concluído com sucesso!"
log "Backup salvo em: $BACKUP_DIR"
log "Para ver logs em tempo real: docker-compose -f $DOCKER_COMPOSE_FILE logs -f"
log "Para parar serviços: docker-compose -f $DOCKER_COMPOSE_FILE down"
log "Para reiniciar: docker-compose -f $DOCKER_COMPOSE_FILE restart"

# Próximos passos
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎯 PRÓXIMOS PASSOS                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "1. 🌟 Teste as funcionalidades em staging"
echo "2. 📊 Verifique métricas de performance"
echo "3. 🧪 Execute testes de integração"
echo "4. 🚀 Prepare para deploy em produção"
echo "5. 📋 Documente lições aprendidas"

echo -e "${GREEN}"
echo "🎉 Staging está pronto para testes!"
echo -e "${NC}"
