#!/bin/bash

# 🧪 Script de Testes para Staging - Aeon Chess
# Versão: 1.0.0
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

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configurações
STAGING_URL="http://localhost:3000"
API_URL="http://localhost:8000"
GRAFANA_URL="http://localhost:3001"
PROMETHEUS_URL="http://localhost:9090"

# Banner
echo -e "${MAGENTA}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🧪 TESTES DE STAGING                      ║"
echo "║                   Aeon Chess v1.0.0                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Função para testar endpoint
test_endpoint() {
    local url=$1
    local name=$2
    local expected_status=${3:-200}
    
    log "🧪 Testando $name: $url"
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_status" ]; then
            success "$name está respondendo (Status: $response)"
            return 0
        else
            warning "$name retornou status $response (esperado: $expected_status)"
            return 1
        fi
    else
        error "$name não está acessível"
        return 1
    fi
}

# Função para testar funcionalidade específica
test_functionality() {
    local name=$1
    local test_func=$2
    
    log "🔍 Testando funcionalidade: $name"
    if $test_func; then
        success "$name: ✅ Funcionando"
        return 0
    else
        warning "$name: ⚠️ Problemas detectados"
        return 1
    fi
}

# Teste 1: Health Checks
test_health_checks() {
    log "🏥 Testando health checks..."
    
    local all_passed=true
    
    # Frontend health
    if test_endpoint "$STAGING_URL/health" "Frontend Health" 200; then
        success "Frontend health check: ✅"
    else
        warning "Frontend health check: ⚠️"
        all_passed=false
    fi
    
    # Backend health
    if test_endpoint "$API_URL/health" "Backend Health" 200; then
        success "Backend health check: ✅"
    else
        warning "Backend health check: ⚠️"
        all_passed=false
    fi
    
    # Grafana health
    if test_endpoint "$GRAFANA_URL/api/health" "Grafana Health" 200; then
        success "Grafana health check: ✅"
    else
        warning "Grafana health check: ⚠️"
        all_passed=false
    fi
    
    # Prometheus health
    if test_endpoint "$PROMETHEUS_URL/-/healthy" "Prometheus Health" 200; then
        success "Prometheus health check: ✅"
    else
        warning "Prometheus health check: ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Teste 2: Funcionalidades Básicas
test_basic_functionality() {
    log "🎯 Testando funcionalidades básicas..."
    
    local all_passed=true
    
    # Testar página principal
    if curl -s "$STAGING_URL" | grep -q "Aeon Chess"; then
        success "Página principal carregada: ✅"
    else
        warning "Página principal não carregou corretamente: ⚠️"
        all_passed=false
    fi
    
    # Testar API básica
    if curl -s "$API_URL/docs" | grep -q "FastAPI"; then
        success "Documentação da API acessível: ✅"
    else
        warning "Documentação da API não acessível: ⚠️"
        all_passed=false
    fi
    
    # Testar Grafana
    if curl -s "$GRAFANA_URL" | grep -q "Grafana"; then
        success "Grafana acessível: ✅"
    else
        warning "Grafana não acessível: ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Teste 3: Performance Básica
test_basic_performance() {
    log "⚡ Testando performance básica..."
    
    local all_passed=true
    
    # Testar tempo de resposta do frontend
    local start_time=$(date +%s%N)
    if curl -s "$STAGING_URL" > /dev/null; then
        local end_time=$(date +%s%N)
        local response_time=$(( (end_time - start_time) / 1000000 ))
        
        if [ $response_time -lt 5000 ]; then
            success "Frontend response time: ${response_time}ms ✅"
        else
            warning "Frontend response time: ${response_time}ms (lento) ⚠️"
            all_passed=false
        fi
    else
        warning "Frontend não respondeu ⚠️"
        all_passed=false
    fi
    
    # Testar tempo de resposta da API
    start_time=$(date +%s%N)
    if curl -s "$API_URL/health" > /dev/null; then
        end_time=$(date +%s%N)
        response_time=$(( (end_time - start_time) / 1000000 ))
        
        if [ $response_time -lt 1000 ]; then
            success "API response time: ${response_time}ms ✅"
        else
            warning "API response time: ${response_time}ms (lento) ⚠️"
            all_passed=false
        fi
    else
        warning "API não respondeu ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Teste 4: Monitoramento
test_monitoring() {
    log "📊 Testando sistema de monitoramento..."
    
    local all_passed=true
    
    # Testar métricas do Prometheus
    if curl -s "$PROMETHEUS_URL/api/v1/targets" | grep -q "up"; then
        success "Prometheus targets: ✅"
    else
        warning "Prometheus targets: ⚠️"
        all_passed=false
    fi
    
    # Testar dashboards do Grafana
    if curl -s "$GRAFANA_URL/api/dashboards" | grep -q "dashboards"; then
        success "Grafana dashboards: ✅"
    else
        warning "Grafana dashboards: ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Teste 5: Banco de Dados
test_database() {
    log "🗄️ Testando banco de dados..."
    
    local all_passed=true
    
    # Verificar se PostgreSQL está rodando
    if docker-compose -f deploy/staging/docker-compose.yml exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
        success "PostgreSQL está rodando: ✅"
    else
        warning "PostgreSQL não está rodando: ⚠️"
        all_passed=false
    fi
    
    # Verificar se Redis está rodando
    if docker-compose -f deploy/staging/docker-compose.yml exec -T redis redis-cli ping | grep -q "PONG"; then
        success "Redis está rodando: ✅"
    else
        warning "Redis não está rodando: ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Teste 6: Segurança Básica
test_basic_security() {
    log "🔒 Testando segurança básica..."
    
    local all_passed=true
    
    # Testar se não há informações sensíveis expostas
    if curl -s "$STAGING_URL" | grep -q "password\|secret\|key"; then
        warning "Possíveis informações sensíveis expostas: ⚠️"
        all_passed=false
    else
        success "Sem informações sensíveis expostas: ✅"
    fi
    
    # Testar headers de segurança
    if curl -s -I "$STAGING_URL" | grep -q "X-Frame-Options\|X-Content-Type-Options"; then
        success "Headers de segurança presentes: ✅"
    else
        warning "Headers de segurança ausentes: ⚠️"
        all_passed=false
    fi
    
    return $([ "$all_passed" = true ] && echo 0 || echo 1)
}

# Executar todos os testes
main() {
    log "🚀 Iniciando testes de staging..."
    
    local test_results=()
    local total_tests=6
    local passed_tests=0
    
    # Executar testes
    test_results+=("$(test_health_checks && echo 0 || echo 1)")
    test_results+=("$(test_basic_functionality && echo 0 || echo 1)")
    test_results+=("$(test_basic_performance && echo 0 || echo 1)")
    test_results+=("$(test_monitoring && echo 0 || echo 1)")
    test_results+=("$(test_database && echo 0 || echo 1)")
    test_results+=("$(test_basic_security && echo 0 || echo 1)")
    
    # Contar testes passados
    for result in "${test_results[@]}"; do
        if [ "$result" -eq 0 ]; then
            ((passed_tests++))
        fi
    done
    
    # Relatório final
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    📊 RELATÓRIO FINAL                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo "🎯 Total de testes: $total_tests"
    echo "✅ Testes passados: $passed_tests"
    echo "❌ Testes falharam: $((total_tests - passed_tests))"
    echo "📊 Taxa de sucesso: $(( (passed_tests * 100) / total_tests ))%"
    
    if [ $passed_tests -eq $total_tests ]; then
        echo -e "${GREEN}"
        echo "🏆 TODOS OS TESTES PASSARAM! Staging está pronto para produção!"
        echo -e "${NC}"
        exit 0
    elif [ $passed_tests -gt $((total_tests / 2)) ]; then
        echo -e "${YELLOW}"
        echo "⚠️ Maioria dos testes passou. Staging pode ser usado com cautela."
        echo -e "${NC}"
        exit 1
    else
        echo -e "${RED}"
        echo "❌ Muitos testes falharam. Staging precisa de correções."
        echo -e "${NC}"
        exit 1
    fi
}

# Executar se chamado diretamente
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
