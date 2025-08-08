#!/bin/bash

echo "=== Iniciando Testes de Integração ==="

# Garante que o script pode ser executado do diretório raiz ou do diretório de testes
if [ -f "test_integration.py" ]; then
    TEST_DIR="."
else
    TEST_DIR="tests"
fi

# Executa os testes
python3 "${TEST_DIR}/test_integration.py" -v

echo "=== Testes Concluídos ==="
