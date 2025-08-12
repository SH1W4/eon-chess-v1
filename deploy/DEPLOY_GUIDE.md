# 🚀 Guia de Deploy Local - AEON Chess

## Visão Geral

Este guia detalha o processo completo para fazer o deploy local do AEON Chess em um MacBook Air com 8GB de RAM, utilizando Docker, nginx, PostgreSQL e Redis com otimizações específicas para recursos limitados.

## Pré-requisitos

- macOS 15.5+
- Docker Desktop instalado e rodando
- Homebrew instalado
- 2GB de RAM livre
- 5GB de espaço em disco

## Estrutura do Deploy

```
AEON Chess Local Deploy
├── nginx (Proxy Reverso + SSL)
│   ├── Serve frontend estático
│   └── Proxy para API backend
├── Backend (FastAPI)
│   ├── 2 workers Uvicorn
│   └── Limite de 512MB RAM
├── PostgreSQL
│   └── Otimizado para 256MB RAM
└── Redis
    └── Cache com 64MB limite
```

## Passo a Passo

### 1. Preparação Inicial

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/seu-usuario/aeon-chess.git
cd aeon-chess

# Verifique a branch
git checkout main
git pull origin main
```

### 2. Build da Aplicação

Execute o script de build otimizado:

```bash
./deploy/build-production.sh
```

Este script irá:
- Construir o frontend com otimizações
- Compilar o backend Python
- Criar as imagens Docker
- Gerar informações de build

### 3. Setup do Ambiente Local

Execute o script de setup:

```bash
./deploy/setup-local.sh
```

Este script irá:
- Instalar mkcert (se necessário)
- Configurar o domínio `aeon-chess.local`
- Gerar certificados SSL válidos
- Criar chaves secretas seguras
- Preparar os diretórios necessários

### 4. Iniciar os Serviços

```bash
# Iniciar todos os serviços
docker compose -f docker-compose.production.yml up -d

# Verificar o status
docker compose -f docker-compose.production.yml ps

# Ver os logs
docker compose -f docker-compose.production.yml logs -f
```

### 5. Acessar a Aplicação

Abra seu navegador e acesse:
- **https://aeon-chess.local** - Interface principal
- **https://aeon-chess.local/api/docs** - Documentação da API

## Monitoramento de Recursos

### Verificar uso de memória:
```bash
docker stats --no-stream
```

### Limites configurados:
- **nginx**: 128MB RAM, 0.25 CPU
- **backend**: 512MB RAM, 0.5 CPU  
- **postgres**: 256MB RAM, 0.25 CPU
- **redis**: 128MB RAM, 0.25 CPU
- **Total**: ~1GB RAM

## Troubleshooting

### 1. Erro de certificado SSL
```bash
# Reinstalar certificados
cd certs
mkcert -uninstall
mkcert -install
mkcert aeon-chess.local
cd ..
```

### 2. Domínio não resolve
```bash
# Verificar /etc/hosts
cat /etc/hosts | grep aeon-chess

# Se não existir, adicionar:
echo "127.0.0.1 aeon-chess.local" | sudo tee -a /etc/hosts
```

### 3. Docker sem memória
```bash
# Parar containers não usados
docker container prune -f

# Limpar imagens antigas
docker image prune -a -f

# Limpar volumes não usados
docker volume prune -f
```

### 4. Backend não conecta ao banco
```bash
# Verificar se o postgres está saudável
docker compose -f docker-compose.production.yml ps postgres

# Ver logs do postgres
docker compose -f docker-compose.production.yml logs postgres

# Reiniciar apenas o postgres
docker compose -f docker-compose.production.yml restart postgres
```

## Comandos Úteis

### Gestão dos Serviços
```bash
# Parar tudo
docker compose -f docker-compose.production.yml down

# Parar e remover volumes (CUIDADO: apaga dados)
docker compose -f docker-compose.production.yml down -v

# Reiniciar um serviço específico
docker compose -f docker-compose.production.yml restart backend

# Escalar backend (não recomendado com 8GB RAM)
docker compose -f docker-compose.production.yml up -d --scale backend=3
```

### Backup do Banco
```bash
# Backup
docker compose -f docker-compose.production.yml exec postgres \
  pg_dump -U aeon_user aeon_chess > backup.sql

# Restore
docker compose -f docker-compose.production.yml exec -T postgres \
  psql -U aeon_user aeon_chess < backup.sql
```

### Logs e Debug
```bash
# Logs de um serviço específico
docker compose -f docker-compose.production.yml logs -f backend

# Últimas 100 linhas
docker compose -f docker-compose.production.yml logs --tail=100

# Acessar shell do container
docker compose -f docker-compose.production.yml exec backend sh
```

## Otimizações para MacBook Air 8GB

### 1. Reduzir uso de memória do Docker Desktop
- Docker Desktop → Settings → Resources
- Memory: 4GB (máximo)
- CPUs: 2

### 2. Habilitar swap no macOS
```bash
# Verificar swap atual
sysctl vm.swapusage

# Aumentar se necessário (requer SIP desabilitado)
sudo nvram boot-args="vm_compressor=2"
```

### 3. Fechar aplicações desnecessárias
- Chrome/Safari com muitas abas
- Slack, Discord, etc.
- IDEs pesadas

### 4. Monitorar Activity Monitor
- Manter Memory Pressure em verde/amarelo
- Verificar uso de swap

## Próximos Passos

Após o deploy local bem-sucedido:

1. **Testes de Performance**
   - Verificar tempo de resposta da API
   - Testar jogadas simultâneas
   - Monitorar uso de recursos

2. **Deploy em Produção**
   - Configurar VPS ou cloud provider
   - Setup de domínio real
   - Configurar CDN para assets
   - Implementar backup automático

3. **Melhorias**
   - Adicionar cache de página com Varnish
   - Implementar queue com Celery
   - Adicionar monitoramento com Prometheus

## Suporte

Em caso de problemas:
1. Verifique os logs detalhados
2. Consulte a documentação em `/docs`
3. Abra uma issue no GitHub
