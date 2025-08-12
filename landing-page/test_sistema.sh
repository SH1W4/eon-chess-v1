#!/bin/bash

echo "🔍 TESTE COMPLETO DO SISTEMA AEON CHESS"
echo "========================================"

# Verificar estrutura de arquivos
echo "1. 📁 Verificando estrutura de arquivos..."
echo "   - index.html: $(test -f index.html && echo "✅ OK" || echo "❌ FALTANDO")"
echo "   - js/chess-engine.js: $(test -f js/chess-engine.js && echo "✅ OK" || echo "❌ FALTANDO")"
echo "   - js/terminal-cultural.js: $(test -f js/terminal-cultural.js && echo "✅ OK" || echo "❌ FALTANDO")"
echo "   - css/styles.css: $(test -f css/styles.css && echo "✅ OK" || echo "❌ FALTANDO")"

# Verificar se HTML inclui os scripts
echo ""
echo "2. 🔗 Verificando inclusão de scripts no HTML..."
if [ -f "index.html" ]; then
    echo "   - chess-engine.js incluído: $(grep -q "chess-engine.js" index.html && echo "✅ OK" || echo "❌ NÃO INCLUÍDO")"
    echo "   - terminal-cultural.js incluído: $(grep -q "terminal-cultural.js" index.html && echo "✅ OK" || echo "❌ NÃO INCLUÍDO")"
    echo "   - Elemento terminal-output existe: $(grep -q "terminal-output" index.html && echo "✅ OK" || echo "❌ NÃO EXISTE")"
    echo "   - Elemento hero-board existe: $(grep -q "hero-board\|chessboard" index.html && echo "✅ OK" || echo "❌ NÃO EXISTE")"
else
    echo "   ❌ index.html não encontrado!"
fi

# Verificar conteúdo dos arquivos JavaScript
echo ""
echo "3. 🧩 Verificando conteúdo dos scripts..."
if [ -f "js/terminal-cultural.js" ]; then
    echo "   - Classe AeonTerminalCultural: $(grep -q "class AeonTerminalCultural" js/terminal-cultural.js && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - Ring Definitivo: $(grep -q "ring_definitivo" js/terminal-cultural.js && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - Genghis vs Alexandre: $(grep -q "genghis_alexandre" js/terminal-cultural.js && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - Funções globais expostas: $(grep -q "window.experiencia" js/terminal-cultural.js && echo "✅ OK" || echo "❌ FALTANDO")"
fi

if [ -f "js/chess-engine.js" ]; then
    echo "   - ChessGame class: $(grep -q "class ChessGame\|ChessGame.*=" js/chess-engine.js && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - AI integration: $(grep -q "makeAIMove\|aiMove" js/chess-engine.js && echo "✅ OK" || echo "❌ FALTANDO")"
fi

# Verificar sintaxe JavaScript
echo ""
echo "4. ⚙️ Verificando sintaxe JavaScript..."
if command -v node >/dev/null 2>&1; then
    if [ -f "js/terminal-cultural.js" ]; then
        if node -c js/terminal-cultural.js 2>/dev/null; then
            echo "   - terminal-cultural.js: ✅ SINTAXE OK"
        else
            echo "   - terminal-cultural.js: ❌ ERRO DE SINTAXE"
            echo "     Erros:"
            node -c js/terminal-cultural.js 2>&1 | head -3
        fi
    fi
    
    if [ -f "js/chess-engine.js" ]; then
        if node -c js/chess-engine.js 2>/dev/null; then
            echo "   - chess-engine.js: ✅ SINTAXE OK"
        else
            echo "   - chess-engine.js: ❌ ERRO DE SINTAXE"
            echo "     Erros:"
            node -c js/chess-engine.js 2>&1 | head -3
        fi
    fi
else
    echo "   ⚠️ Node.js não encontrado - pulando verificação de sintaxe"
fi

# Verificar se os elementos HTML necessários existem
echo ""
echo "5. 🎯 Verificando elementos HTML necessários..."
if [ -f "index.html" ]; then
    echo "   - Botão 'Jogar Agora': $(grep -q "Jogar Agora\|jogar-agora" index.html && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - Terminal demo section: $(grep -q "terminal-demo" index.html && echo "✅ OK" || echo "❌ FALTANDO")"
    echo "   - Seção gamificada: $(grep -q "gamified\|journey" index.html && echo "✅ OK" || echo "❌ FALTANDO")"
fi

# Teste de servidor local
echo ""
echo "6. 🌐 Testando servidor local..."
echo "   Iniciando servidor na porta 8005..."

# Função para parar o servidor
cleanup() {
    echo "   🛑 Parando servidor..."
    kill $SERVER_PID 2>/dev/null
    exit
}
trap cleanup EXIT

# Iniciar servidor em background
python3 -m http.server 8005 > /dev/null 2>&1 &
SERVER_PID=$!

# Aguardar servidor iniciar
sleep 2

# Testar se servidor está respondendo
if curl -s http://localhost:8005 > /dev/null 2>&1; then
    echo "   ✅ Servidor funcionando em http://localhost:8005"
    
    # Testar se arquivos estão sendo servidos
    echo "   - index.html acessível: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8005/index.html | grep -q "200" && echo "✅ OK" || echo "❌ ERRO")"
    echo "   - CSS acessível: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8005/css/styles.css | grep -q "200" && echo "✅ OK" || echo "❌ ERRO")"
    echo "   - JS acessível: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8005/js/terminal-cultural.js | grep -q "200" && echo "✅ OK" || echo "❌ ERRO")"
else
    echo "   ❌ Servidor não está respondendo"
fi

echo ""
echo "7. 🧪 RESULTADOS DO TESTE"
echo "=========================="

# Verificar problemas críticos
CRITICAL_ISSUES=0

if [ ! -f "index.html" ]; then
    echo "❌ CRÍTICO: index.html não encontrado"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ -f "index.html" ] && ! grep -q "terminal-cultural.js" index.html; then
    echo "❌ CRÍTICO: Script terminal-cultural.js não incluído no HTML"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ -f "js/terminal-cultural.js" ] && ! grep -q "class AeonTerminalCultural" js/terminal-cultural.js; then
    echo "❌ CRÍTICO: Classe principal não encontrada no script"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ -f "index.html" ] && ! grep -q "terminal-output" index.html; then
    echo "❌ CRÍTICO: Elemento terminal-output não encontrado no HTML"
    CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
fi

if [ $CRITICAL_ISSUES -eq 0 ]; then
    echo "✅ SISTEMA PARECE ESTAR CONFIGURADO CORRETAMENTE!"
    echo ""
    echo "🚀 Para testar:"
    echo "   1. Acesse: http://localhost:8005"
    echo "   2. Verifique se o terminal cultural está funcionando"
    echo "   3. Teste os botões de confrontos épicos"
    echo "   4. Verifique se o tabuleiro de xadrez está visível"
    echo ""
    echo "   Pressione CTRL+C quando terminar o teste"
    
    # Manter servidor rodando para teste
    wait $SERVER_PID
else
    echo "❌ ENCONTRADOS $CRITICAL_ISSUES PROBLEMAS CRÍTICOS!"
    echo ""
    echo "🔧 AÇÕES NECESSÁRIAS:"
    echo "   - Verificar se todos os arquivos existem"
    echo "   - Verificar se scripts estão incluídos corretamente no HTML"
    echo "   - Verificar sintaxe dos arquivos JavaScript"
    echo "   - Verificar se elementos HTML necessários existem"
fi
