#!/bin/bash

# Instala as dependências
echo "Instalando dependências..."
pip install -r requirements-test.txt

# Inicia o servidor Next.js em background
echo "Iniciando servidor Next.js..."
npm run dev &
SERVER_PID=$!

# Espera o servidor iniciar
echo "Aguardando servidor iniciar..."
sleep 10

# Executa os testes
echo "Executando testes..."
pytest tests/web/ -v

# Mata o servidor
echo "Finalizando servidor..."
kill $SERVER_PID
