/**
 * 🎨 Modern UI Integration - AEON CHESS v2.0
 * Integração moderna de UI com design system atualizado
 * 
 * @author AEON CHESS Team
 * @version 2.0.0
 * @date Janeiro 2025
 */

// ===============================
// 🎯 SISTEMA DE BOTÕES MODERNO
// ===============================

class ModernButtonManager {
    constructor() {
        this.buttons = new Map();
        this.initialized = false;
    }

    async init() {
        console.log('🎨 Inicializando sistema de botões moderno...');

        try {
            await this.waitForDOM();
            this.setupModernButtons();
            this.setupButtonEffects();
            this.setupAIIntegration();

            this.initialized = true;
            console.log('✅ Sistema de botões moderno inicializado!');

        } catch (error) {
            console.error('❌ Erro na inicialização dos botões:', error);
        }
    }

    async waitForDOM() {
        if (document.readyState === 'loading') {
            await new Promise(resolve => {
                document.addEventListener('DOMContentLoaded', resolve);
            });
        }

        // Aguardar um pouco mais para garantir que tudo carregou
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    setupModernButtons() {
        console.log('🎯 Configurando botões modernos...');

        // Botões principais da aplicação
        const buttonConfigs = {
            'ai-fab': {
                type: 'ai-terminal',
                icon: 'fas fa-brain',
                title: 'CHESS OS - Terminal da IA',
                handler: () => this.toggleAITerminal()
            },
            'cta-play': {
                type: 'primary-action',
                icon: 'fas fa-chess',
                title: 'Começar a jogar',
                handler: () => this.startGame()
            },
            'cta-demo': {
                type: 'secondary-action',
                icon: 'fas fa-play-circle',
                title: 'Ver demonstração',
                handler: () => this.showDemo()
            },
            'nav-play': {
                type: 'navigation',
                icon: 'fas fa-play',
                title: 'Jogar agora',
                handler: () => this.navigateToGame()
            }
        };

        // Configurar cada botão
        Object.entries(buttonConfigs).forEach(([id, config]) => {
            this.setupButton(id, config);
        });
    }

    setupButton(id, config) {
        const button = document.getElementById(id);
        if (!button) {
            console.warn(`⚠️ Botão não encontrado: ${id}`);
            return;
        }

        // Aplicar classes modernas se não tiver
        if (!button.classList.contains('btn')) {
            button.classList.add('btn');

            // Aplicar estilo baseado no tipo
            switch (config.type) {
                case 'ai-terminal':
                    button.classList.add('btn-primary');
                    break;
                case 'primary-action':
                    button.classList.add('btn-accent', 'btn-xl');
                    break;
                case 'secondary-action':
                    button.classList.add('btn-ghost', 'btn-xl');
                    break;
                case 'navigation':
                    button.classList.add('btn-accent', 'btn-lg');
                    break;
            }
        }

        // Configurar evento de clique
        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log(`🔍 Botão clicado: ${id}`);

            // Adicionar feedback visual
            this.addClickFeedback(button);

            // Executar handler
            if (config.handler) {
                config.handler();
            }
        });

        // Armazenar referência
        this.buttons.set(id, {
            element: button,
            config: config
        });

        console.log(`✅ Botão configurado: ${id}`);
    }

    setupButtonEffects() {
        console.log('✨ Configurando efeitos de botões...');

        // Adicionar efeitos hover para todos os botões
        document.querySelectorAll('.btn').forEach(button => {
            // Efeito ripple
            button.addEventListener('click', (e) => {
                this.createRippleEffect(button, e);
            });

            // Efeito de loading
            if (!button.dataset.effectsAdded) {
                button.dataset.effectsAdded = 'true';

                // Adicionar animação de entrada se não tiver
                if (!button.classList.contains('animate-fade-in') &&
                    !button.classList.contains('animate-scale-in')) {
                    button.classList.add('animate-fade-in');
                }
            }
        });
    }

    setupAIIntegration() {
        console.log('🧠 Configurando integração com IA...');

        // Integrar com sistema de IA quando disponível
        if (window.aiSystem) {
            console.log('✅ Sistema de IA encontrado, integrando...');
            this.integrateWithAI();
        } else {
            // Aguardar sistema de IA carregar
            console.log('⏳ Aguardando sistema de IA...');
            this.waitForAISystem();
        }
    }

    async waitForAISystem() {
        let attempts = 0;
        const maxAttempts = 20; // 10 segundos máximo

        while (attempts < maxAttempts) {
            if (window.aiSystem && window.aiSystem.isInitialized) {
                console.log('✅ Sistema de IA carregado, integrando...');
                this.integrateWithAI();
                return;
            }

            await new Promise(resolve => setTimeout(resolve, 500));
            attempts++;
        }

        console.warn('⚠️ Sistema de IA não foi carregado após 10 segundos');
        this.createFallbackAI();
    }

    integrateWithAI() {
        const aiFab = this.buttons.get('ai-fab');
        if (aiFab && window.aiSystem) {
            console.log('🔗 Integrando botão FAB com sistema de IA...');

            // Atualizar handler para usar sistema real
            aiFab.config.handler = () => {
                console.log('🧠 Abrindo terminal da IA...');
                window.aiSystem.terminal.toggle();
            };

            // Atualizar visual
            const button = aiFab.element;
            button.style.background = 'linear-gradient(135deg, #00ffff 0%, #0080ff 100%)';
            button.style.boxShadow = '0 4px 12px rgba(0, 255, 255, 0.4)';

            console.log('✅ Botão FAB integrado com sucesso!');
        }
    }

    createFallbackAI() {
        console.log('🔧 Criando sistema de IA de fallback...');

        // Criar um sistema básico de fallback
        window.aiSystem = {
            terminal: {
                toggle: () => {
                    console.log('🧠 Terminal de IA (fallback) ativado!');
                    this.showAIMessage();
                }
            },
            isInitialized: true
        };

        this.integrateWithAI();
        console.log('✅ Sistema de IA de fallback criado!');
    }

    showAIMessage() {
        // Criar uma mensagem temporária
        const message = document.createElement('div');
        message.className = 'glass rounded-lg p-4 animate-fade-in';
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1001;
            max-width: 400px;
            color: white;
            text-align: center;
        `;

        message.innerHTML = `
            <div class="flex items-center justify-center mb-4">
                <i class="fas fa-brain text-3xl text-cyan-400"></i>
            </div>
            <h3 class="text-lg font-semibold mb-2">CHESS OS IA</h3>
            <p class="text-sm opacity-90 mb-4">Sistema de IA carregando...</p>
            <button class="btn btn-primary btn-sm" onclick="this.parentElement.remove()">
                Fechar
            </button>
        `;

        document.body.appendChild(message);

        // Remover automaticamente após 3 segundos
        setTimeout(() => {
            if (message.parentElement) {
                message.remove();
            }
        }, 3000);
    }

    addClickFeedback(button) {
        // Adicionar classe de feedback
        button.style.transform = 'scale(0.95)';

        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    createRippleEffect(button, event) {
        // Criar efeito ripple
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 600ms linear;
            background-color: rgba(255, 255, 255, 0.3);
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            pointer-events: none;
        `;

        // Adicionar CSS para animação se não existir
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
                .btn {
                    position: relative;
                    overflow: hidden;
                }
            `;
            document.head.appendChild(style);
        }

        button.appendChild(ripple);

        // Remover ripple após animação
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Handlers para botões
    toggleAITerminal() {
        console.log('🧠 Alternando terminal da IA...');
        if (window.aiSystem && window.aiSystem.terminal) {
            window.aiSystem.terminal.toggle();
        } else {
            this.showAIMessage();
        }
    }

    startGame() {
        console.log('🎮 Iniciando jogo...');
        // Implementar lógica do jogo
        this.showMessage('🎮 Iniciando jogo...', 'info');
    }

    showDemo() {
        console.log('🎬 Mostrando demo...');
        // Implementar lógica da demo
        this.showMessage('🎬 Carregando demonstração...', 'info');
    }

    navigateToGame() {
        console.log('🎯 Navegando para o jogo...');
        // Implementar navegação
        this.showMessage('🎯 Carregando interface de jogo...', 'info');
    }

    showMessage(text, type = 'info') {
        // Usar sistema de notificação existente se disponível
        if (window.showNotification) {
            window.showNotification(text, type);
        } else {
            console.log(`💬 ${text}`);
        }
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO AUTOMÁTICA
// ===============================

// Criar instância global
window.modernUI = new ModernButtonManager();

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.modernUI.init();
    });
} else {
    window.modernUI.init();
}

// Log de carregamento
console.log('🎨 Sistema de UI moderno carregado!');