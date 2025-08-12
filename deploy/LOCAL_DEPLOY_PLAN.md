# Plano de Deploy Local - AEON Chess

## Análise do Ambiente

### Especificações da Máquina
- **Modelo**: MacBook Air (M1/M2)
- **Memória**: 8 GB RAM
- **Armazenamento**: 31 GB disponíveis
- **OS**: macOS 15.5
- **Docker**: v28.3.2 instalado ✅
- **Homebrew**: Instalado com PostgreSQL 14 e Redis ✅

### Avaliação de Viabilidade
Com 8GB de RAM, a melhor abordagem é usar Docker Compose para otimizar recursos, rodando:
- Frontend: Build estático servido via nginx
- Backend: Python API com workers limitados
- PostgreSQL: Configuração otimizada para desenvolvimento
- Redis: Cache com limite de memória

## Estratégia de Deploy Local

### 1. Domínio Gratuito
Opções recomendadas:
- **aeon-chess.localhost** (resolução local)
- **aeon-chess.local** (mDNS/Bonjour)
- **Ngrok** para acesso externo temporário
- **DuckDNS** para domínio gratuito permanente

### 2. Arquitetura de Deploy

```
┌─────────────────────────────────────────────────┐
│                   nginx (80/443)                 │
│              Proxy Reverso + SSL                 │
└────────────┬────────────────┬───────────────────┘
             │                │
    ┌────────▼──────┐  ┌─────▼──────┐
    │  Frontend     │  │  Backend   │
    │  (React SPA)  │  │  (FastAPI) │
    └───────────────┘  └─────┬──────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL    │
                    │     + Redis     │
                    └─────────────────┘
```

### 3. Configuração de Recursos

```yaml
# Limites de recursos para MacBook Air 8GB
services:
  nginx:
    mem_limit: 128m
    cpus: 0.25
  
  backend:
    mem_limit: 512m
    cpus: 0.5
    environment:
      - WORKERS=2
      - MAX_CONNECTIONS=50
  
  postgres:
    mem_limit: 256m
    cpus: 0.25
    environment:
      - shared_buffers=64MB
      - effective_cache_size=256MB
  
  redis:
    mem_limit: 128m
    cpus: 0.25
    command: redis-server --maxmemory 64mb --maxmemory-policy allkeys-lru
```

### 4. SSL/HTTPS Local
- Usar mkcert para certificados locais confiáveis
- Configurar nginx com SSL
- Redirecionar HTTP → HTTPS

### 5. Otimizações para 8GB RAM
- Build do frontend em multi-stage para reduzir tamanho
- Usar Alpine Linux nas imagens Docker
- Limitar workers e conexões
- Configurar swap no macOS se necessário
- Usar Redis como cache agressivo

## Próximos Passos

1. **Preparar variáveis de ambiente**
2. **Configurar Docker Compose**
3. **Setup de domínio local**
4. **Gerar certificados SSL**
5. **Otimizar builds**
6. **Configurar monitoramento básico**

## Comandos de Deploy

```bash
# Iniciar serviços
docker compose up -d

# Verificar status
docker compose ps

# Logs
docker compose logs -f

# Parar serviços
docker compose down
```
