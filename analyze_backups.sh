#!/bin/bash

# Análise Segura de Backups
echo "=== 📦 ANÁLISE DE BACKUPS ==="
echo "Analisando sem remover nada..."
echo ""

# 1. Listar backups grandes
echo "🔍 BACKUPS PRINCIPAIS:"
echo "----------------------"
find ~/WORKSPACE/PROJECTS -name "BACKUPS" -type d -exec du -sh {} \; 2>/dev/null | sort -hr

echo ""
echo "📁 ARQUIVOS DE BACKUP:"
echo "---------------------"
find ~/WORKSPACE/PROJECTS -name "*.backup" -o -name "*.old" -o -name "*.bak" -o -name "*.tar.gz" | while read file; do
    size=$(du -sh "$file" 2>/dev/null | cut -f1)
    echo "$size - $file"
done | sort -hr | head -20

echo ""
echo "💡 RECOMENDAÇÕES:"
echo "1. Pasta NEXUS/BACKUPS tem 4.2GB - verificar se todos são necessários"
echo "2. CHESS_BACKUP.tar.gz tem 1GB - pode ser movido para drive externo"
echo "3. Consolidar múltiplos venvs em um por projeto"
echo ""
echo "📊 ESPAÇO POTENCIAL A LIBERAR: ~8-10 GB"
echo ""
echo "Para prosseguir com organização segura, execute:"
echo "./organize_backups.sh"
