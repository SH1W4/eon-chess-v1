/**
 * ARKITECT Simple Solution - Efeito de Esquadrinhamento Simples
 * Sistema direto e funcional
 */

class ArkitectSimpleSolution {
    constructor() {
        this.name = 'ARKITECT Simple Solution';
        this.version = '3.0.0';
        this.isActive = false;
        this.currentSquare = 0;
        this.interval = null;

        console.log('🏗️ ARKITECT: Solução criada');
        this.init();
    }

    init() {
        console.log('🏗️ ARKITECT: Inicializando...');

        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        console.log('🏗️ ARKITECT: Configurando...');

        // Encontrar o tabuleiro
        this.board = document.querySelector('#aeon-board');

        if (this.board) {
            console.log('🏗️ ARKITECT: Tabuleiro encontrado ✅');

            // Aguardar o tabuleiro estar completamente inicializado
            this.waitForBoardReady();
        } else {
            console.log('🏗️ ARKITECT: Tabuleiro não encontrado, tentando novamente...');
            setTimeout(() => this.setup(), 1000);
        }
    }

    waitForBoardReady() {
        // Verificar se o tabuleiro tem a estrutura necessária
        const boardWrapper = this.board.querySelector('.chess-board-wrapper');

        if (boardWrapper) {
            console.log('🏗️ ARKITECT: Tabuleiro inicializado ✅');
            this.createEffectsContainer();
        } else {
            console.log('🏗️ ARKITECT: Aguardando inicialização do tabuleiro...');
            setTimeout(() => this.waitForBoardReady(), 500);
        }
    }

    createEffectsContainer() {
        // Criar container para efeitos
        this.effectsContainer = document.createElement('div');
        this.effectsContainer.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
        `;

        this.board.appendChild(this.effectsContainer);
        console.log('🏗️ ARKITECT: Container de efeitos criado ✅');

        // Criar indicador de progresso
        this.createProgressIndicator();

        // Ativar automaticamente após 2 segundos
        setTimeout(() => {
            console.log('🏗️ ARKITECT: Ativando automaticamente...');
            this.start();
        }, 2000);
    }

    createProgressIndicator() {
        // Indicador de progresso discreto - movido para canto inferior esquerdo
        const progressContainer = document.createElement('div');
        progressContainer.style.cssText = `
            position: absolute;
            bottom: 5px;
            left: 5px;
            width: 60px;
            height: 3px;
            background: rgba(0, 255, 0, 0.3);
            border-radius: 2px;
            z-index: 1002;
            overflow: hidden;
            pointer-events: none;
        `;

        this.progressBar = document.createElement('div');
        this.progressBar.style.cssText = `
            height: 100%;
            background: #00ff00;
            width: 0%;
            transition: width 0.3s ease-out;
        `;

        progressContainer.appendChild(this.progressBar);
        this.effectsContainer.appendChild(progressContainer);

        console.log('🏗️ ARKITECT: Indicador de progresso criado no canto inferior esquerdo');
    }

    start() {
        if (!this.effectsContainer) {
            console.log('🏗️ ARKITECT: Container não está pronto');
            return;
        }

        console.log('🏗️ ARKITECT: Iniciando efeito de esquadrinhamento...');
        this.isActive = true;
        this.currentSquare = 0;
        this.startScanning();
    }

    startScanning() {
        if (!this.isActive) return;

        // Limpar efeito anterior
        this.clearEffect();

        // Criar efeito na casa atual
        this.createSquareEffect();

        // Atualizar progresso
        this.updateProgress();

        // Mover para próxima casa
        this.currentSquare++;

        if (this.currentSquare < 64) {
            // Continuar escaneando
            this.interval = setTimeout(() => {
                this.startScanning();
            }, 800); // 800ms por casa - mais lento
        } else {
            // Reiniciar após completar
            console.log('🏗️ ARKITECT: Escaneamento completo, reiniciando...');
            setTimeout(() => {
                if (this.isActive) {
                    this.currentSquare = 0;
                    this.startScanning();
                }
            }, 3000); // 3 segundos de pausa
        }
    }

    updateProgress() {
        if (this.progressBar) {
            const progress = (this.currentSquare / 64) * 100;
            this.progressBar.style.width = progress + '%';
        }
    }

    createSquareEffect() {
        const row = Math.floor(this.currentSquare / 8);
        const col = this.currentSquare % 8;

        // Calcular posição da casa
        const size = 12.5; // 100% / 8 = 12.5%
        const left = col * size;
        const top = row * size;

        // Criar indicador visual principal
        const indicator = document.createElement('div');
        indicator.style.cssText = `
            position: absolute;
            left: ${left}%;
            top: ${top}%;
            width: ${size}%;
            height: ${size}%;
            border: 2px solid #00ff00;
            background: rgba(0, 255, 0, 0.1);
            z-index: 1001;
            animation: squareScan 0.8s ease-in-out;
        `;

        // Criar efeito de scan interno
        const scanEffect = document.createElement('div');
        scanEffect.style.cssText = `
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 30%, rgba(0, 255, 255, 0.3) 50%, transparent 70%);
            animation: internalScan 0.8s ease-in-out;
        `;

        // Criar ponto de análise
        const analysisPoint = document.createElement('div');
        analysisPoint.style.cssText = `
            position: absolute;
            left: 50%;
            top: 50%;
            width: 4px;
            height: 4px;
            background: #00ffff;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: analysisPulse 0.8s ease-in-out;
        `;

        indicator.appendChild(scanEffect);
        indicator.appendChild(analysisPoint);
        this.effectsContainer.appendChild(indicator);

        // Remover após animação
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.parentNode.removeChild(indicator);
            }
        }, 800);
    }

    clearEffect() {
        if (this.effectsContainer) {
            this.effectsContainer.innerHTML = '';
        }
    }

    stop() {
        console.log('🏗️ ARKITECT: Parando efeito...');
        this.isActive = false;

        if (this.interval) {
            clearTimeout(this.interval);
        }

        this.clearEffect();
    }

    test() {
        console.log('🏗️ ARKITECT: Testando efeito...');
        this.start();
    }

    getStatus() {
        return {
            name: this.name,
            version: this.version,
            isActive: this.isActive,
            currentSquare: this.currentSquare,
            board: this.board ? '✅' : '❌',
            effectsContainer: this.effectsContainer ? '✅' : '❌'
        };
    }
}

// Adicionar CSS para animações
const arkitectStyles = document.createElement('style');
arkitectStyles.textContent = `
    @keyframes squareScan {
        0% { 
            border-color: #00ff00;
            background: rgba(0, 255, 0, 0.1);
            transform: scale(1);
        }
        50% { 
            border-color: #00ffff;
            background: rgba(0, 255, 255, 0.2);
            transform: scale(1.02);
        }
        100% { 
            border-color: #00ff00;
            background: rgba(0, 255, 0, 0.1);
            transform: scale(1);
        }
    }
    
    @keyframes internalScan {
        0% { 
            opacity: 0;
            transform: translateX(-100%) translateY(-100%);
        }
        50% { 
            opacity: 1;
            transform: translateX(0%) translateY(0%);
        }
        100% { 
            opacity: 0;
            transform: translateX(100%) translateY(100%);
        }
    }
    
    @keyframes analysisPulse {
        0% { 
            opacity: 0.5;
            transform: translate(-50%, -50%) scale(1);
            box-shadow: 0 0 5px #00ffff;
        }
        50% { 
            opacity: 1;
            transform: translate(-50%, -50%) scale(1.5);
            box-shadow: 0 0 15px #00ffff;
        }
        100% { 
            opacity: 0.5;
            transform: translate(-50%, -50%) scale(1);
            box-shadow: 0 0 5px #00ffff;
        }
    }
`;
document.head.appendChild(arkitectStyles);

// Inicialização global
document.addEventListener('DOMContentLoaded', () => {
    console.log('🏗️ ARKITECT: DOM carregado, criando solução...');
    window.arkitectSolution = new ArkitectSimpleSolution();
});

// Funções globais
window.startArkitect = function() {
    if (window.arkitectSolution) {
        window.arkitectSolution.start();
    }
};

window.stopArkitect = function() {
    if (window.arkitectSolution) {
        window.arkitectSolution.stop();
    }
};

window.testArkitect = function() {
    if (window.arkitectSolution) {
        window.arkitectSolution.test();
    }
};

window.getArkitectStatus = function() {
    if (window.arkitectSolution) {
        return window.arkitectSolution.getStatus();
    }
    return {
        error: 'Solução não inicializada'
    };
};

console.log('🏗️ ARKITECT Simple Solution carregado');