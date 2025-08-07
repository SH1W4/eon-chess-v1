#!/bin/bash

echo "=== Iniciando Ativação Total do ARKITECT ==="

# Ativa ambiente virtual
source venv/bin/activate

# Verifica dependências
pip install -r requirements.txt

# Cria diretórios necessários se não existirem
mkdir -p logs
mkdir -p .arkitect/cache
mkdir -p .arkitect/data

# Inicia ARKITECT com integração total
python scripts/arkitect_full_integration.py
