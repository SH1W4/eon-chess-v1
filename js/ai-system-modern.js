/**
 * 🧠 AI System Modern - Sistema Moderno de IA para Xadrez
 * Versão ES6 com Vite para máxima confiabilidade e performance
 * 
 * @author AEON CHESS Team
 * @version 2.0.0
 * @date Janeiro 2025
 */

// Configurações do sistema
const AI_CONFIG = {
    name: 'CHESS OS AI System',
    version: '2.0.0',
    debug: true,
    terminal: {
        width: 400,
        height: 300,
        position: 'center'
    }
};

// Sistema de logging moderno
class Logger {
    static log(message, type = 'info') {
        if (!AI_CONFIG.debug) return;

        const timestamp = new Date().toLocaleTimeString();
        const prefix = {
            info: '🔍',
            success: '✅',
            error: '❌',
            warning: '⚠️',
            ai: '🧠'
        } [type] || '🔍';

        console.log(`[${timestamp}] ${prefix} ${message}`);
    }

    static error(message, error = null) {
        Logger.log(message, 'error');
        if (error) console.error(error);
    }
}

// Gerenciador de elementos DOM
class DOMManager {
    constructor() {
        this.elements = new Map();
        this.observers = new Map();
    }

    // Buscar elemento com retry
    async getElement(selector, maxRetries = 5, delay = 100) {
        for (let i = 0; i < maxRetries; i++) {
            const element = document.querySelector(selector);
            if (element) {
                Logger.log(`Elemento encontrado: ${selector}`, 'success');
                return element;
            }

            Logger.log(`Tentativa ${i + 1} para encontrar: ${selector}`, 'warning');
            await this.sleep(delay);
        }

        Logger.log(`Elemento não encontrado após ${maxRetries} tentativas: ${selector}`, 'error');
        return null;
    }

    // Observar mudanças no DOM
    observeElement(selector, callback) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    const element = document.querySelector(selector);
                    if (element) {
                        callback(element);
                        observer.disconnect();
                    }
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        this.observers.set(selector, observer);
        return observer;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Sistema de terminal moderno
class ModernTerminal {
    constructor() {
        this.isOpen = false;
        this.element = null;
        this.content = null;
        this.domManager = new DOMManager();
    }

    async create() {
        Logger.log('Criando terminal moderno...', 'info');

        try {
            // Criar container do terminal
            this.element = document.createElement('div');
            this.element.id = 'modern-ai-terminal';
            this.element.className = 'modern-terminal';

            // Aplicar estilos inline para máxima compatibilidade
            Object.assign(this.element.style, {
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                width: `${AI_CONFIG.terminal.width}px`,
                height: `${AI_CONFIG.terminal.height}px`,
                background: 'rgba(15, 15, 15, 0.95)',
                border: '1px solid rgba(0, 255, 255, 0.3)',
                borderRadius: '16px',
                padding: '20px',
                zIndex: '1001',
                backdropFilter: 'blur(20px)',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.4)',
                fontFamily: 'SF Mono, Monaco, Consolas, monospace',
                overflow: 'hidden',
                display: 'none',
                opacity: '0',
                transition: 'opacity 0.3s ease'
            });

            // Criar header
            const header = this.createHeader();
            this.element.appendChild(header);

            // Criar conteúdo
            this.content = this.createContent();
            this.element.appendChild(this.content);

            // Adicionar ao DOM
            document.body.appendChild(this.element);

            Logger.log('Terminal criado com sucesso!', 'success');
            return true;

        } catch (error) {
            Logger.error('Erro ao criar terminal:', error);
            return false;
        }
    }

    createHeader() {
        const header = document.createElement('div');
        Object.assign(header.style, {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px',
            padding: '15px 20px',
            background: 'linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 100, 200, 0.1))',
            borderRadius: '12px',
            border: '1px solid rgba(0, 255, 255, 0.2)'
        });

        // Título
        const title = document.createElement('div');
        title.innerHTML = `
            <span style="color: #00ffff; font-size: 14px; font-weight: 600; letter-spacing: 0.5px;">
                🧠 ${AI_CONFIG.name} v${AI_CONFIG.version}
            </span>
        `;

        // Botão fechar
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.title = 'Fechar Terminal';
        Object.assign(closeBtn.style, {
            width: '24px',
            height: '24px',
            background: 'rgba(255, 255, 255, 0.05)',
            border: 'none',
            borderRadius: '50%',
            color: '#888',
            fontSize: '18px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'all 0.2s ease'
        });

        closeBtn.addEventListener('click', () => this.close());
        closeBtn.addEventListener('mouseenter', () => {
            closeBtn.style.background = 'rgba(255, 107, 107, 0.2)';
            closeBtn.style.color = '#ff6b6b';
        });
        closeBtn.addEventListener('mouseleave', () => {
            closeBtn.style.background = 'rgba(255, 255, 255, 0.05)';
            closeBtn.style.color = '#888';
        });

        header.appendChild(title);
        header.appendChild(closeBtn);
        return header;
    }

    createContent() {
        const content = document.createElement('div');
        Object.assign(content.style, {
            height: 'calc(100% - 80px)',
            overflowY: 'auto',
            color: '#00ff88',
            fontSize: '11px',
            lineHeight: '1.4',
            padding: '10px',
            background: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '8px',
            border: '1px solid rgba(0, 255, 255, 0.1)'
        });

        return content;
    }

    open() {
        if (!this.element) return;

        Logger.log('Abrindo terminal...', 'info');
        this.element.style.display = 'block';

        // Animar entrada
        setTimeout(() => {
            this.element.style.opacity = '1';
        }, 10);

        this.isOpen = true;
        this.addMessage('Terminal ativado com sucesso!', 'success');
    }

    close() {
        if (!this.element) return;

        Logger.log('Fechando terminal...', 'info');
        this.element.style.opacity = '0';

        setTimeout(() => {
            this.element.style.display = 'none';
        }, 300);

        this.isOpen = false;
    }

    addMessage(message, type = 'info') {
        if (!this.content) return;

        const messageEl = document.createElement('div');
        const colors = {
            info: '#00ffff',
            success: '#00ff88',
            error: '#ff6b6b',
            warning: '#ffa500',
            ai: '#00ff88'
        };

        Object.assign(messageEl.style, {
            marginBottom: '12px',
            padding: '8px 12px',
            color: colors[type] || colors.info,
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '6px',
            borderLeft: `3px solid ${colors[type] || colors.info}`,
            transition: 'all 0.2s ease'
        });

        messageEl.textContent = message;
        this.content.appendChild(messageEl);

        // Auto-scroll
        this.content.scrollTop = this.content.scrollHeight;
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
}

// Sistema principal da IA
class ModernAISystem {
    constructor() {
        this.terminal = new ModernTerminal();
        this.domManager = new DOMManager();
        this.isInitialized = false;
        this.fabButton = null;
    }

    async init() {
        Logger.log('Inicializando sistema moderno da IA...', 'info');

        try {
            // Aguardar DOM estar pronto
            if (document.readyState === 'loading') {
                await new Promise(resolve => {
                    document.addEventListener('DOMContentLoaded', resolve);
                });
            }

            // Aguardar um pouco mais para garantir que tudo carregou
            await this.domManager.sleep(500);

            // Criar terminal
            const terminalCreated = await this.terminal.create();
            if (!terminalCreated) {
                throw new Error('Falha ao criar terminal');
            }

            // Integrar com botão FAB
            await this.integrateWithFAB();

            this.isInitialized = true;
            Logger.log('Sistema moderno da IA inicializado com sucesso!', 'success');

        } catch (error) {
            Logger.error('Erro na inicialização:', error);
        }
    }

    async integrateWithFAB() {
        Logger.log('Integrando com botão FAB...', 'info');

        try {
            // Buscar botão FAB
            this.fabButton = await this.domManager.getElement('#ai-fab');

            if (this.fabButton) {
                Logger.log('Botão FAB encontrado, integrando...', 'success');

                // Atualizar visual
                this.fabButton.innerHTML = '<i class="fas fa-brain"></i>';
                this.fabButton.title = 'CHESS OS - Terminal da IA';

                // Aplicar estilos
                Object.assign(this.fabButton.style, {
                    background: 'linear-gradient(135deg, #00ffff 0%, #0080ff 100%)',
                    boxShadow: '0 4px 12px rgba(0, 255, 255, 0.4)',
                    cursor: 'pointer'
                });

                // Adicionar eventos
                this.fabButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    Logger.log('Botão FAB clicado!', 'info');
                    this.terminal.toggle();
                });

                // Efeitos hover
                this.fabButton.addEventListener('mouseenter', () => {
                    this.fabButton.style.transform = 'scale(1.1)';
                    this.fabButton.style.boxShadow = '0 6px 20px rgba(0, 255, 255, 0.6)';
                });

                this.fabButton.addEventListener('mouseleave', () => {
                    this.fabButton.style.transform = 'scale(1)';
                    this.fabButton.style.boxShadow = '0 4px 12px rgba(0, 255, 255, 0.4)';
                });

                Logger.log('Botão FAB integrado com sucesso!', 'success');

            } else {
                Logger.log('Botão FAB não encontrado, criando alternativo...', 'warning');
                await this.createAlternativeButton();
            }

        } catch (error) {
            Logger.error('Erro na integração com FAB:', error);
            await this.createAlternativeButton();
        }
    }

    async createAlternativeButton() {
        Logger.log('Criando botão alternativo...', 'info');

        try {
            const altButton = document.createElement('div');
            altButton.id = 'ai-button-alternative';
            altButton.title = 'CHESS OS - Terminal da IA';

            Object.assign(altButton.style, {
                position: 'fixed',
                bottom: '30px',
                right: '30px',
                width: '60px',
                height: '60px',
                background: 'linear-gradient(135deg, #00ffff 0%, #0080ff 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                zIndex: '1000',
                boxShadow: '0 4px 12px rgba(0, 255, 255, 0.4)',
                transition: 'all 0.3s ease',
                fontSize: '24px',
                color: 'white'
            });

            altButton.innerHTML = '🧠';

            // Eventos
            altButton.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                Logger.log('Botão alternativo clicado!', 'info');
                this.terminal.toggle();
            });

            altButton.addEventListener('mouseenter', () => {
                altButton.style.transform = 'scale(1.1)';
                altButton.style.boxShadow = '0 6px 20px rgba(0, 255, 255, 0.6)';
            });

            altButton.addEventListener('mouseleave', () => {
                altButton.style.transform = 'scale(1)';
                altButton.style.boxShadow = '0 4px 12px rgba(0, 255, 255, 0.4)';
            });

            document.body.appendChild(altButton);
            this.fabButton = altButton;

            Logger.log('Botão alternativo criado com sucesso!', 'success');

        } catch (error) {
            Logger.error('Erro ao criar botão alternativo:', error);
        }
    }
}

// Exportar para uso global
window.ModernAISystem = ModernAISystem;
window.AI_CONFIG = AI_CONFIG;

// Auto-inicialização quando o script carregar
document.addEventListener('DOMContentLoaded', async () => {
    Logger.log('DOM carregado, inicializando sistema moderno da IA...', 'info');

    const aiSystem = new ModernAISystem();
    await aiSystem.init();

    // Disponibilizar globalmente
    window.aiSystem = aiSystem;

    Logger.log('Sistema disponível globalmente como window.aiSystem', 'success');
});

// Log de inicialização