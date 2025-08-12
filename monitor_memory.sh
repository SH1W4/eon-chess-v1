#!/bin/bash

# Monitor de Memória NEXUS
# Monitora e alerta sobre uso excessivo de memória

echo "🧠 NEXUS Memory Monitor v1.0"
echo "============================"

while true; do
    clear
    echo "📊 Status de Memória - $(date '+%H:%M:%S')"
    echo "============================"
    
    # Memória total e livre
    vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-20s %10.2f MB\n", "$1:", $2 * $size / 1048576);' | grep -E "(free|active|inactive|wired|compressor)"
    
    echo ""
    echo "🔝 Top 5 Processos por Memória:"
    echo "--------------------------------"
    ps aux | sort -nrk 4 | head -6 | tail -5 | awk '{printf "%-20s %5.1f%% %8.0f MB\n", substr($11,1,20), $4, $6/1024}'
    
    # Alerta se memória livre < 100MB
    FREE_MB=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    FREE_MB=$((FREE_MB * 4096 / 1048576))
    
    if [ $FREE_MB -lt 100 ]; then
        echo ""
        echo "⚠️  ALERTA: Memória livre muito baixa! ($FREE_MB MB)"
        echo "   Considere fechar algumas aplicações"
    fi
    
    echo ""
    echo "Pressione Ctrl+C para sair | Atualiza em 5s..."
    sleep 5
done
