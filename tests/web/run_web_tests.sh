#!/bin/bash

# Configura o trap para limpar processos ao sair
trap 'kill $(jobs -p)' EXIT

# Inicia o servidor Next.js em background
echo "Starting Next.js server..."
cd ../.. && npm run dev &

# Espera o servidor iniciar
echo "Waiting for server to start..."
sleep 10

# Executa os testes
echo "Running tests..."
cd tests/web
pytest test_chess_components.py -v

# O trap cuidará de matar os processos em background
