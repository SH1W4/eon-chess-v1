#!/bin/bash

# Script para testar a landing page do ChessMaster

echo "🚀 Iniciando servidor para a landing page ChessMaster..."
echo "📍 Acesse: http://localhost:8080"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

cd landing-page
python3 -m http.server 8080
