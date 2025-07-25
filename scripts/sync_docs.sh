#!/bin/bash

# Script de sincronização de documentação do XadrezMaster

echo "Iniciando sincronização de documentação..."

# Criar diretório de backup se não existir
BACKUP_DIR=".backup/docs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Sincronizar documentos
for dir in tecnico analise arquitetura produto; do
    echo "Sincronizando $dir..."
    
    # Criar diretório de backup
    mkdir -p "$BACKUP_DIR/$dir"
    
    # Copiar arquivos
    cp -r "docs/$dir"/* "$BACKUP_DIR/$dir/" 2>/dev/null || true
done

# Registrar metadados da sincronização
echo "Data: $(date)" > "$BACKUP_DIR/sync_metadata.txt"
echo "Autor: $USER" >> "$BACKUP_DIR/sync_metadata.txt"

echo "Sincronização concluída. Backup salvo em $BACKUP_DIR"

# Verificar documentos
echo "Verificando documentação..."

check_metadata() {
    local file="$1"
    if ! grep -q "^# " "$file" || ! grep -q "^## " "$file"; then
        echo "AVISO: $file pode estar faltando cabeçalhos adequados"
    fi
    if ! grep -q "Versão:" "$file" || ! grep -q "Data:" "$file"; then
        echo "AVISO: $file pode estar faltando metadados básicos"
    fi
}

find docs -name "*.md" -type f | while read -r file; do
    echo "Verificando $file..."
    check_metadata "$file"
done

echo "Verificação concluída."
