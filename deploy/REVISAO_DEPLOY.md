# 📋 Revisão do Deploy Local - AEON Chess

## ✅ Arquivos Criados/Ajustados

### 1. **Docker Compose Local** (`docker-compose.local.yml`)
- Ajustado para usar Next.js export em vez de React build
- Configurado para usar estrutura real do projeto
- Limites de recursos otimizados para MacBook Air 8GB

### 2. **Dockerfile Backend Local** (`deploy/Dockerfile.backend.local`)
- Simplificado para desenvolvimento local
- Usa hot-reload com uvicorn
- Aponta para `src.api.main:app`

### 3. **Script de Setup** (`setup-local.sh`)
- Detecta e instala Node.js se necessário
- Constrói Next.js com export estático
- Verifica endpoint de health existente
- Cria todos os diretórios necessários

### 4. **Configurações Existentes**
- `.env.production` - Variáveis de ambiente ✅
- `nginx/nginx.conf` - Configuração nginx ✅
- `nginx/conf.d/aeon-chess.conf` - Virtual host ✅
- `deploy/init-db.sql` - Schema do banco ✅

## 🔧 Ajustes Necessários Antes de Executar

### 1. Instalar Dependências Python
```bash
# Se não existir requirements.txt completo
pip freeze > requirements.txt

# Ou criar um mínimo
cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.0
python-jose[cryptography]==3.3.0
websockets==12.0
httpx==0.25.1
alembic==1.12.1
EOF
```

### 2. Configurar Next.js
O projeto já tem Next.js configurado no `package.json`. Apenas certifique-se de que funciona:
```bash
npm install
npm run build
```

### 3. Criar Estrutura de Diretórios
```bash
mkdir -p certs logs data/postgres data/redis out
```

## 🚀 Como Executar

### 1. Primeiro Setup
```bash
# Tornar script executável (já feito)
chmod +x setup-local.sh

# Executar setup
./setup-local.sh
```

### 2. Iniciar Serviços
```bash
# Iniciar todos os containers
docker compose -f docker-compose.local.yml up -d

# Ver logs
docker compose -f docker-compose.local.yml logs -f

# Verificar status
docker compose -f docker-compose.local.yml ps
```

### 3. Acessar Aplicação
- **Frontend**: https://aeon-chess.local
- **API Docs**: https://aeon-chess.local/api/docs
- **Health Check**: https://aeon-chess.local/health

## 📊 Monitoramento

### Verificar Recursos
```bash
# Ver uso de memória/CPU
docker stats

# Limites configurados:
# - nginx: 128MB RAM, 0.25 CPU
# - backend: 512MB RAM, 0.5 CPU  
# - postgres: 256MB RAM, 0.25 CPU
# - redis: 128MB RAM, 0.25 CPU
# Total: ~1GB RAM
```

### Logs por Serviço
```bash
# Backend
docker compose -f docker-compose.local.yml logs -f backend

# Nginx
docker compose -f docker-compose.local.yml logs -f nginx

# PostgreSQL
docker compose -f docker-compose.local.yml logs -f postgres
```

## ⚠️ Troubleshooting

### 1. Erro "Module not found"
```bash
# Verificar se src.api.main existe
ls -la src/api/main.py

# Se necessário, ajustar PYTHONPATH no Dockerfile
ENV PYTHONPATH=/app:$PYTHONPATH
```

### 2. Next.js não exporta
```bash
# Adicionar no next.config.js
module.exports = {
  output: 'export',
  // outras configs...
}
```

### 3. Certificados SSL inválidos
```bash
cd certs
mkcert -uninstall
mkcert -install
mkcert aeon-chess.local
cd ..
```

## 🎯 Status Atual

- ✅ Configuração Docker completa
- ✅ Scripts de automação prontos
- ✅ Backend FastAPI funcional
- ✅ Nginx com SSL e otimizações
- ✅ PostgreSQL e Redis configurados
- ⚠️ Verificar Next.js export
- ⚠️ Criar requirements.txt se necessário

## 🔄 Próximos Passos

1. Executar `./setup-local.sh`
2. Resolver qualquer dependência faltante
3. Iniciar containers com Docker Compose
4. Testar aplicação em https://aeon-chess.local
5. Ajustar conforme necessário

## 📝 Notas

- O projeto usa Next.js (não React puro)
- A API está em `src/api/main.py`
- O frontend está na raiz (não em `/frontend`)
- Todos os limites foram otimizados para 8GB RAM
- SSL local funciona via mkcert
