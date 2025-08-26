/**
 * 🔍 Debug Corner Elements - Verifica elementos no canto superior direito
 */

class DebugCornerElements {
    constructor() {
        this.name = 'Debug Corner Elements';
        this.version = '1.0.0';

        console.log(`🔍 ${this.name} v${this.version} carregado`);
        this.init();
    }

    init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startDebug());
        } else {
            this.startDebug();
        }
    }

    startDebug() {
        console.log('🔍 Iniciando debug de elementos no canto superior direito...');

        // Verificar imediatamente
        this.checkCornerElements();

        // Verificar periodicamente
        setInterval(() => {
            this.checkCornerElements();
        }, 3000);
    }

    checkCornerElements() {
        const aeonBoard = document.querySelector('#aeon-board');
        if (!aeonBoard) {
            console.log('🔍 Tabuleiro #aeon-board não encontrado');
            return;
        }

        const boardRect = aeonBoard.getBoundingClientRect();
        console.log('🔍 Posição do tabuleiro:', {
            top: boardRect.top,
            left: boardRect.left,
            right: boardRect.right,
            bottom: boardRect.bottom
        });

        // Verificar elementos fixos que podem estar sobrepondo
        const fixedElements = document.querySelectorAll('[style*="position: fixed"]');
        fixedElements.forEach((element, index) => {
            const rect = element.getBoundingClientRect();
            const style = element.style.cssText;

            // Verificar se está no canto superior direito
            if (rect.top < 100 && rect.right > window.innerWidth - 200) {
                console.log(`🔍 Elemento fixo ${index} no canto superior direito:`, {
                    element: element,
                    id: element.id,
                    className: element.className,
                    style: style,
                    rect: {
                        top: rect.top,
                        left: rect.left,
                        right: rect.right,
                        bottom: rect.bottom
                    }
                });

                // Verificar se sobrepõe o tabuleiro
                if (this.elementsOverlap(rect, boardRect)) {
                    console.log(`🔍 ⚠️ Elemento ${index} sobrepõe o tabuleiro!`);
                    console.log('🔍 Removendo elemento problemático...');
                    element.remove();
                }
            }
        });

        // Verificar elementos absolutos dentro do tabuleiro
        const absoluteElements = aeonBoard.querySelectorAll('[style*="position: absolute"]');
        absoluteElements.forEach((element, index) => {
            const style = element.style.cssText;
            console.log(`🔍 Elemento absoluto ${index} dentro do tabuleiro:`, {
                element: element,
                style: style
            });

            // Verificar se está no canto superior direito do tabuleiro
            if (style.includes('top: 0') || style.includes('right: 0') ||
                style.includes('top: 0px') || style.includes('right: 0px')) {
                console.log(`🔍 ⚠️ Elemento ${index} no canto superior direito do tabuleiro!`);
                console.log('🔍 Removendo elemento problemático...');
                element.remove();
            }
        });

        // Verificar elementos com z-index alto
        const highZIndexElements = document.querySelectorAll('[style*="z-index"]');
        highZIndexElements.forEach((element, index) => {
            const rect = element.getBoundingClientRect();
            const style = element.style.cssText;

            // Extrair z-index
            const zIndexMatch = style.match(/z-index:\s*(\d+)/);
            if (zIndexMatch) {
                const zIndex = parseInt(zIndexMatch[1]);
                if (zIndex > 50 && this.elementsOverlap(rect, boardRect)) {
                    console.log(`🔍 Elemento com z-index alto ${index}:`, {
                        element: element,
                        zIndex: zIndex,
                        style: style,
                        rect: {
                            top: rect.top,
                            left: rect.left,
                            right: rect.right,
                            bottom: rect.bottom
                        }
                    });
                }
            }
        });
    }

    elementsOverlap(rect1, rect2) {
        return !(rect1.right < rect2.left ||
            rect1.left > rect2.right ||
            rect1.bottom < rect2.top ||
            rect1.top > rect2.bottom);
    }

    // Método público para forçar verificação
    forceCheck() {
        console.log('🔍 Forçando verificação de elementos...');
        this.checkCornerElements();
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.DebugCornerElements = DebugCornerElements;
    window.debugCornerElements = new DebugCornerElements();
}

console.log('🔍 Debug Corner Elements carregado');