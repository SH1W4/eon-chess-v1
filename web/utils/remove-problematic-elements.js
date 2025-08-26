/**
 * 🧹 Remove Problematic Elements - Limpa elementos que podem estar causando problemas visuais
 */

class ProblematicElementsRemover {
    constructor() {
        this.name = 'Problematic Elements Remover';
        this.version = '1.0.0';

        console.log(`🧹 ${this.name} v${this.version} carregado`);
        this.init();
    }

    init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startCleanup());
        } else {
            this.startCleanup();
        }
    }

    startCleanup() {
        console.log('🧹 Iniciando limpeza de elementos problemáticos...');

        // Limpar imediatamente
        this.removeProblematicElements();

        // Limpar periodicamente
        setInterval(() => {
            this.removeProblematicElements();
        }, 5000);
    }

    removeProblematicElements() {
        // Remover notificações de IA que podem estar no canto superior direito
        const aiNotifications = document.querySelectorAll('#ai-change-notification, [id*="ai-change"], [id*="notification"]');
        aiNotifications.forEach(element => {
            if (element.style.position === 'fixed' &&
                (element.style.top === '20px' || element.style.top === '80px') &&
                element.style.right) {
                console.log('🧹 Removendo notificação de IA problemática:', element);
                element.remove();
            }
        });

        // Remover elementos fixos no canto superior direito que podem estar cobrindo o tabuleiro
        const fixedElements = document.querySelectorAll('[style*="position: fixed"][style*="top"][style*="right"]');
        fixedElements.forEach(element => {
            const style = element.style.cssText;
            if (style.includes('top') && style.includes('right') &&
                (style.includes('z-index') || element.style.zIndex > 100)) {
                console.log('🧹 Removendo elemento fixo problemático:', element);
                element.remove();
            }
        });

        // Remover elementos absolutos que podem estar no canto superior direito do tabuleiro
        const aeonBoard = document.querySelector('#aeon-board');
        if (aeonBoard) {
            const absoluteElements = aeonBoard.querySelectorAll('[style*="position: absolute"]');
            absoluteElements.forEach(element => {
                const style = element.style.cssText;
                if (style.includes('top: 0') || style.includes('right: 0') ||
                    style.includes('top: 0px') || style.includes('right: 0px')) {
                    console.log('🧹 Removendo elemento absoluto problemático do tabuleiro:', element);
                    element.remove();
                }
            });
        }

        // Remover elementos com z-index alto que podem estar cobrindo o tabuleiro
        const highZIndexElements = document.querySelectorAll('[style*="z-index: 50"], [style*="z-index: 100"], [style*="z-index: 1000"]');
        highZIndexElements.forEach(element => {
            const rect = element.getBoundingClientRect();
            const aeonBoardRect = aeonBoard ? aeonBoard.getBoundingClientRect() : null;

            if (aeonBoardRect && this.elementsOverlap(rect, aeonBoardRect)) {
                console.log('🧹 Removendo elemento com z-index alto que sobrepõe o tabuleiro:', element);
                element.remove();
            }
        });
    }

    elementsOverlap(rect1, rect2) {
        return !(rect1.right < rect2.left ||
            rect1.left > rect2.right ||
            rect1.bottom < rect2.top ||
            rect1.top > rect2.bottom);
    }

    // Método público para forçar limpeza
    forceCleanup() {
        console.log('🧹 Forçando limpeza completa...');
        this.removeProblematicElements();
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.ProblematicElementsRemover = ProblematicElementsRemover;
    window.problematicElementsRemover = new ProblematicElementsRemover();
}

console.log('🧹 Problematic Elements Remover carregado');