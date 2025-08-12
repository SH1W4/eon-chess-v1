#!/bin/bash

# NEXUS Memory Optimizer
# Para sistemas com memória limitada

echo "🚀 NEXUS Memory Optimizer"
echo "========================"

# 1. Finalizar processos helpers desnecessários
echo "1. Limpando processos auxiliares..."
killall -KILL "Opera Helper" 2>/dev/null
killall -KILL "Safari Web Content" 2>/dev/null
killall -KILL "Notion Helper" 2>/dev/null
echo "   ✓ Processos auxiliares finalizados"

# 2. Limpar caches
echo "2. Limpando caches do sistema..."
rm -rf ~/Library/Caches/com.operasoftware.Opera 2>/dev/null
rm -rf ~/Library/Caches/notion.id* 2>/dev/null
echo "   ✓ Caches limpos"

# 3. Mostrar status
echo "3. Status atual:"
vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("   %-15s %8.0f MB\n", "$1:", $2 * $size / 1048576);' | grep -E "(free|wired|active)"

echo ""
echo "⚡ Para máxima eficiência:"
echo "   1. Reinicie o Warp Terminal"
echo "   2. Use apenas um navegador por vez"
echo "   3. Execute: sudo purge"
echo ""
echo "✅ Otimização concluída!"
