#!/bin/bash

# Script de Sincronização do XadrezMaster
# Mantém o projeto sincronizado entre local, backups e cloud

CHESS_ROOT="/Users/jx/WORKSPACE/PROJECTS/CHESS"
CLOUD_PATH="/Users/jx/Library/Mobile Documents/com~apple~CloudDocs/ChessMaster.ai"
VERSION_FILE="$CHESS_ROOT/.versions/config.json"

# Função para backup do sistema
system_backup() {
    echo "Realizando backup do sistema..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    tar -czf "$CHESS_ROOT/.backup/system/CHESS_$TIMESTAMP.tar.gz" \
        --exclude='.backup' \
        --exclude='.cloud' \
        --exclude='node_modules' \
        --exclude='venv' \
        -C "$CHESS_ROOT" .
    echo "✓ Backup do sistema concluído"
}

# Função para sincronização com cloud
cloud_sync() {
    echo "Sincronizando com iCloud..."
    
    # Sync assets
    rsync -av --delete \
        "$CHESS_ROOT/assets/" \
        "$CHESS_ROOT/.cloud/assets/"
    
    # Sync documentação
    rsync -av --delete \
        "$CHESS_ROOT/docs/" \
        "$CHESS_ROOT/.cloud/sync/docs/"
    
    echo "✓ Sincronização com cloud concluída"
}

# Função para versionamento
version_control() {
    echo "Atualizando versões..."
    
    # Copia versão atual para stable se necessário
    if [ -f "$CHESS_ROOT/.versions/config.json" ]; then
        cp -r "$CHESS_ROOT/src" "$CHESS_ROOT/.versions/stable/"
        cp -r "$CHESS_ROOT/docs" "$CHESS_ROOT/.versions/stable/"
    fi
    
    echo "✓ Controle de versão atualizado"
}

# Execução principal
echo "=== Iniciando Sincronização do XadrezMaster ==="
system_backup
cloud_sync
version_control
echo "=== Sincronização Concluída ==="
