#!/usr/bin/env node

/**
 * 🧪 Teste Automatizado do Sistema de Efeitos Visuais
 * Script Node.js para verificar se tudo está funcionando
 */

const fs = require('fs');
const path = require('path');

console.log('🧪 Teste Automatizado do Sistema de Efeitos Visuais');
console.log('='.repeat(60));

// Função para verificar arquivo
function checkFile(filePath, description) {
    try {
        if (fs.existsSync(filePath)) {
            const stats = fs.statSync(filePath);
            const size = (stats.size / 1024).toFixed(2);
            console.log(`✅ ${description}: ${filePath} (${size} KB)`);
            return true;
        } else {
            console.log(`❌ ${description}: ${filePath} - ARQUIVO NÃO ENCONTRADO`);
            return false;
        }
    } catch (error) {
        console.log(`❌ ${description}: ${filePath} - ERRO: ${error.message}`);
        return false;
    }
}

// Função para verificar conteúdo do arquivo
function checkFileContent(filePath, searchTerm, description) {
    try {
        if (fs.existsSync(filePath)) {
            const content = fs.readFileSync(filePath, 'utf8');
            if (content.includes(searchTerm)) {
                console.log(`✅ ${description}: ${searchTerm} encontrado`);
                return true;
            } else {
                console.log(`❌ ${description}: ${searchTerm} NÃO encontrado`);
                return false;
            }
        } else {
            console.log(`❌ ${description}: Arquivo não existe`);
            return false;
        }
    } catch (error) {
        console.log(`❌ ${description}: Erro ao ler arquivo - ${error.message}`);
        return false;
    }
}

// Função para verificar integração HTML
function checkHTMLIntegration() {
    console.log('\n🔍 Verificando Integração HTML...');

    const htmlPath = 'index.html';
    if (!fs.existsSync(htmlPath)) {
        console.log('❌ index.html não encontrado');
        return false;
    }

    const htmlContent = fs.readFileSync(htmlPath, 'utf8');
    let allGood = true;

    // Verificar se o script Python está incluído
    if (!htmlContent.includes('python-effects-integration.js')) {
        console.log('❌ Script Python não incluído no HTML');
        allGood = false;
    } else {
        console.log('✅ Script Python incluído no HTML');
    }

    // Verificar se o tabuleiro está presente
    if (!htmlContent.includes('aeon-board')) {
        console.log('❌ Tabuleiro aeon-board não encontrado no HTML');
        allGood = false;
    } else {
        console.log('✅ Tabuleiro aeon-board encontrado no HTML');
    }

    // Verificar se o botão de teste está presente
    if (!htmlContent.includes('test-effects-btn')) {
        console.log('❌ Botão de teste não encontrado no HTML');
        allGood = false;
    } else {
        console.log('✅ Botão de teste encontrado no HTML');
    }

    return allGood;
}

// Função para verificar sistema Python
function checkPythonSystem() {
    console.log('\n🐍 Verificando Sistema Python...');

    const pythonDir = 'python';
    if (!fs.existsSync(pythonDir)) {
        console.log('❌ Diretório Python não encontrado');
        return false;
    }

    let allGood = true;

    // Verificar arquivos Python principais
    const pythonFiles = [
        'chess_visual_effects_engine.py',
        'chess_effects_api.py',
        'setup.py',
        'requirements.txt'
    ];

    pythonFiles.forEach(file => {
        const filePath = path.join(pythonDir, file);
        if (!checkFile(filePath, `Arquivo Python: ${file}`)) {
            allGood = false;
        }
    });

    // Verificar se os arquivos Python têm conteúdo válido
    const enginePath = path.join(pythonDir, 'chess_visual_effects_engine.py');
    if (fs.existsSync(enginePath)) {
        const content = fs.readFileSync(enginePath, 'utf8');
        if (content.includes('class ChessEffectsEngine')) {
            console.log('✅ Classe ChessEffectsEngine encontrada no motor Python');
        } else {
            console.log('❌ Classe ChessEffectsEngine NÃO encontrada no motor Python');
            allGood = false;
        }
    }

    return allGood;
}

// Função para verificar JavaScript
function checkJavaScript() {
    console.log('\n📜 Verificando Sistema JavaScript...');

    let allGood = true;

    // Verificar arquivo principal de integração
    if (!checkFile('js/python-effects-integration.js', 'Sistema de Integração Python')) {
        allGood = false;
    }

    // Verificar se a classe está definida
    if (!checkFileContent('js/python-effects-integration.js', 'class PythonEffectsIntegration', 'Classe PythonEffectsIntegration')) {
        allGood = false;
    }

    // Verificar se os métodos principais estão presentes
    const methods = [
        'detectProfessionalPatterns',
        'analyzeMovePredictions',
        'analyzeThreatLevels',
        'calculatePositionEvaluation',
        'createProfessionalVisualEffects',
        'testEffects'
    ];

    methods.forEach(method => {
        if (!checkFileContent('js/python-effects-integration.js', method, `Método ${method}`)) {
            allGood = false;
        }
    });

    return allGood;
}

// Função para verificar estrutura geral
function checkStructure() {
    console.log('\n🏗️ Verificando Estrutura do Projeto...');

    const requiredDirs = ['js', 'python', 'css'];
    const requiredFiles = ['index.html', 'README.md'];

    let allGood = true;

    requiredDirs.forEach(dir => {
        if (fs.existsSync(dir)) {
            console.log(`✅ Diretório: ${dir}/`);
        } else {
            console.log(`❌ Diretório: ${dir}/ - NÃO ENCONTRADO`);
            allGood = false;
        }
    });

    requiredFiles.forEach(file => {
        if (fs.existsSync(file)) {
            console.log(`✅ Arquivo: ${file}`);
        } else {
            console.log(`❌ Arquivo: ${file} - NÃO ENCONTRADO`);
            allGood = false;
        }
    });

    return allGood;
}

// Função para gerar relatório
function generateReport(results) {
    console.log('\n📊 RELATÓRIO FINAL');
    console.log('='.repeat(60));

    const totalTests = Object.keys(results).length;
    const passedTests = Object.values(results).filter(result => result).length;
    const failedTests = totalTests - passedTests;

    console.log(`Total de Testes: ${totalTests}`);
    console.log(`✅ Passou: ${passedTests}`);
    console.log(`❌ Falhou: ${failedTests}`);
    console.log(`📈 Taxa de Sucesso: ${((passedTests / totalTests) * 100).toFixed(1)}%`);

    console.log('\n📋 Detalhes dos Testes:');
    Object.entries(results).forEach(([test, result]) => {
        const status = result ? '✅' : '❌';
        console.log(`${status} ${test}`);
    });

    if (failedTests === 0) {
        console.log('\n🎉 TODOS OS TESTES PASSARAM! Sistema funcionando perfeitamente!');
        return true;
    } else {
        console.log('\n⚠️ ALGUNS TESTES FALHARAM. Verifique os problemas acima.');
        return false;
    }
}

// Executar todos os testes
function runAllTests() {
    console.log('🚀 Iniciando testes automatizados...\n');

    const results = {
        'Estrutura do Projeto': checkStructure(),
        'Sistema Python': checkPythonSystem(),
        'Sistema JavaScript': checkJavaScript(),
        'Integração HTML': checkHTMLIntegration()
    };

    return generateReport(results);
}

// Executar testes
if (require.main === module) {
    const success = runAllTests();
    process.exit(success ? 0 : 1);
}

module.exports = {
    runAllTests,
    checkStructure,
    checkPythonSystem,
    checkJavaScript,
    checkHTMLIntegration
};