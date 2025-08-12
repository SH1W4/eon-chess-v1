#!/bin/bash

echo "🚀 AEON Chess - Execução Local Simplificada"
echo "==========================================="
echo ""
echo "⚠️  Executando sem Docker - apenas frontend e backend básico"
echo ""

# 1. Iniciar o backend em modo desenvolvimento
echo "1. Iniciando backend FastAPI..."
cd src/api
source venv/bin/activate

# Criar arquivo main.py se não existir
if [ ! -f main.py ]; then
    cat > main.py << 'MAIN'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AEON Chess API", version="0.2.1")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://aeon-chess.local"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AEON Chess API", "version": "0.2.1"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
MAIN
fi

# Iniciar o backend em background
python main.py &
BACKEND_PID=$!
cd ../..

# 2. Servir o frontend estático
echo ""
echo "2. Servindo frontend estático..."
echo ""

# Instalar http-server se não estiver instalado
if ! command -v http-server &> /dev/null; then
    echo "Instalando http-server..."
    npm install -g http-server
fi

# Servir o frontend
echo "✅ Setup simplificado concluído!"
echo ""
echo "📋 Acessos:"
echo "- Frontend: http://localhost:8080"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Para parar os serviços, pressione Ctrl+C"
echo ""

# Servir frontend
cd out
http-server -p 8080 -c-1

# Cleanup ao sair
trap "kill $BACKEND_PID 2>/dev/null" EXIT
