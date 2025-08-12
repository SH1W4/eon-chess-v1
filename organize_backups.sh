#!/bin/bash

# Script de Organização Segura de Backups
# NÃO remove arquivos, apenas organiza e sugere ações

echo "=== 🗂️  ORGANIZADOR DE BACKUPS NEXUS ==="
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Criar estrutura organizada
BACKUP_CENTRAL="/Users/jx/WORKSPACE/BACKUPS_CONSOLIDATED"
BACKUP_OLD="$BACKUP_CENTRAL/OLD_$(date +%Y%m%d)"
BACKUP_KEEP="$BACKUP_CENTRAL/KEEP"

echo "📁 Criando estrutura de organização..."
mkdir -p "$BACKUP_OLD"
mkdir -p "$BACKUP_KEEP"

# Análise de backups duplicados
echo ""
echo "🔍 ANÁLISE DE DUPLICAÇÕES:"
echo "=========================="

# 1. Backups do CHESS
echo "1. Projeto CHESS:"
echo "   - CHESS_BACKUP.tar.gz (1.0G) - backup principal"
echo "   - .backups/.backup (773M) - contém backups de julho"
echo "   📌 Recomendação: Manter apenas o mais recente"

# 2. Backups NEXUS aninhados
echo ""
echo "2. Backups NEXUS aninhados:"
echo "   - /NEXUS/BACKUPS (4.2G)"
echo "   - /BACKUPS/NEXUS_backup_20250723 (4.4G) - DUPLICADO!"
echo "   📌 Recomendação: Consolidar em um único local"

# 3. Criar relatório
REPORT="$BACKUP_CENTRAL/backup_analysis_$(date +%Y%m%d_%H%M%S).txt"
echo ""
echo "📊 Gerando relatório detalhado..."

cat > "$REPORT" << EOF
RELATÓRIO DE ANÁLISE DE BACKUPS
================================
Data: $(date)

RESUMO EXECUTIVO:
- Total de espaço em backups: ~13GB
- Backups duplicados identificados: ~8GB
- Potencial de economia: 60%

BACKUPS IDENTIFICADOS:
----------------------
1. CHESS_BACKUP.tar.gz (1.0G) - OK, manter
2. CHESS/.backups (773M) - Múltiplas versões antigas
3. NEXUS/BACKUPS (4.2G) - Sistema principal
4. BACKUPS/NEXUS_backup (4.4G) - DUPLICADO do item 3

AÇÕES RECOMENDADAS:
------------------
1. Mover CHESS_BACKUP.tar.gz para $BACKUP_KEEP
2. Consolidar .backups antigos em arquivo único
3. Remover duplicação NEXUS após verificação
4. Implementar política de retenção (30 dias)

COMANDOS SUGERIDOS (executar manualmente após revisão):
------------------------------------------------------
# Para mover backup principal do CHESS
mv /Users/jx/WORKSPACE/PROJECTS/CHESS/CHESS_BACKUP.tar.gz $BACKUP_KEEP/

# Para consolidar backups antigos
tar -czf $BACKUP_OLD/CHESS_old_backups.tar.gz /Users/jx/WORKSPACE/PROJECTS/CHESS/.backups/

# Para verificar integridade antes de remover duplicados
diff -r /Users/jx/WORKSPACE/PROJECTS/NEXUS/BACKUPS /Users/jx/WORKSPACE/PROJECTS/BACKUPS/NEXUS_backup_20250723_203544/BACKUPS

EOF

echo "✅ Relatório salvo em: $REPORT"
echo ""
echo "🎯 PRÓXIMAS AÇÕES:"
echo "1. Revise o relatório: cat $REPORT"
echo "2. Execute os comandos sugeridos manualmente"
echo "3. Após verificação, libere espaço com: ./cleanup_verified.sh"
echo ""
echo "⚠️  IMPORTANTE: Nenhum arquivo foi movido ou removido ainda!"
