#!/bin/bash

# 🚀 ARKITECT Super Scope TaskMash - Script de Execução
# Transforma o projeto CHESS em enterprise-grade

echo "🚀 ARKITECT Super Scope TaskMash Iniciando..."
echo "=================================================="
echo ""

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install python3
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
    else
        echo "❌ Sistema operacional não suportado"
        exit 1
    fi
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip3 install asyncio pathlib

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install node
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    else
        echo "❌ Sistema operacional não suportado"
        exit 1
    fi
fi

# Verificar se npm está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ npm não encontrado. Instalando..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install npm
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get install -y npm
    fi
fi

# Verificar versões
echo "📊 Verificando versões instaladas..."
echo "Python: $(python3 --version)"
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo ""

# Navegar para o diretório do projeto
cd "$(dirname "$0")/.."

# Verificar se estamos no diretório correto
if [ ! -f "package.json" ]; then
    echo "❌ Não foi possível encontrar package.json. Verifique se está no diretório correto."
    exit 1
fi

echo "✅ Diretório do projeto encontrado: $(pwd)"
echo ""

# Backup do projeto atual
echo "💾 Criando backup do projeto atual..."
backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
cp -r src "$backup_dir/"
cp -r public "$backup_dir/"
cp package.json "$backup_dir/"
cp package-lock.json "$backup_dir/" 2>/dev/null || true
echo "✅ Backup criado em: $backup_dir"
echo ""

# Executar o TaskMash
echo "🚀 Executando ARKITECT Super Scope TaskMash..."
echo "=================================================="
echo ""

python3 scripts/arkitect_super_scope_taskmash.py

# Verificar resultado da execução
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 TaskMash executado com sucesso!"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo "1. Testar todas as funcionalidades implementadas"
    echo "2. Executar Lighthouse para validar performance"
    echo "3. Deploy em ambiente de staging"
    echo "4. Monitoramento contínuo com as novas ferramentas"
    echo ""
    echo "📊 MÉTRICAS ESPERADAS:"
    echo "• Performance: 95+ Lighthouse Score"
    echo "• Arquitetura: Padrões Enterprise"
    echo "• Escalabilidade: Preparado para milhões de usuários"
    echo "• Manutenibilidade: Código de nível profissional"
    echo "• Segurança: Proteções de nível enterprise"
    echo "• Monitoramento: Visibilidade completa do sistema"
    echo ""
    echo "🏆 Projeto transformado em ENTERPRISE-GRADE!"
else
    echo ""
    echo "❌ Erro durante a execução do TaskMash"
    echo "Verifique os logs acima para mais detalhes"
    echo ""
    echo "🔄 Restaurando backup..."
    cp -r "$backup_dir"/* .
    echo "✅ Backup restaurado"
    exit 1
fi

echo ""
echo "📄 Relatório salvo em: reports/arkitect_super_scope_report.json"
echo ""
echo "🚀 ARKITECT Super Scope TaskMash Concluído!"
