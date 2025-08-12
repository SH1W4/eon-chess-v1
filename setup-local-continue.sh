#!/bin/bash

echo "🚀 AEON Chess - Continuando Setup Local"
echo "========================================"

# 7. Preparando o backend
echo "7. Preparando o backend Python..."
cd src/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt || echo "⚠️  Arquivo requirements.txt não encontrado, criando..."

# Criar requirements.txt se não existir
if [ ! -f requirements.txt ]; then
    cat > requirements.txt << 'REQ'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
numpy==1.24.3
python-chess==1.999
websockets==12.0
httpx==0.25.2
prometheus-client==0.19.0
REQ
    pip install -r requirements.txt
fi

# Voltar para o diretório raiz
cd ../..

# 8. Inicializando banco de dados
echo "8. Inicializando banco de dados..."
docker-compose -f docker-compose.local.yml up -d postgres redis
sleep 5

# 9. Construindo imagens Docker
echo "9. Construindo imagens Docker..."
docker-compose -f docker-compose.local.yml build

# 10. Iniciando todos os serviços
echo "10. Iniciando todos os serviços..."
docker-compose -f docker-compose.docker-compose -f docke"
docker-compose -f docker-compose.docker-compose -f docke"
redis
:"
echo "1. Aguarde alguns segundos para os serviços iniciarem"
echo "2. Acesse https://aeon-chess.local no seu navegador"
echo "3. Para ver os logs: docker-compose -f docker-compose.local.yml logs -f"
echo "4. Para parar: docker-compose -f docker-compose.local.yml down"
echo ""
echo "🔍 Verificando status dos serviços..."
sleep 5
docker-compose -f docker-compose.local.yml ps
