// AEON CHESS - Sistema de Tratamento de Erros Robusto
// Versão: 1.0 - Fallbacks e Recuperação Automática

class ErrorHandler {
    constructor() {
        this.errorCount = new Map();
        this.maxErrors = 3;
        this.errorTimeout = 60000; // 1 minuto
        this.fallbacks = new Map();
        this.recoveryStrategies = new Map();
        
        this.init();
    }

    init() {
        this.setupFallbacks();
        this.setupRecoveryStrategies();
        this.setupGlobalErrorHandling();
        console.log('✅ Error Handler inicializado');
    }

    setupFallbacks() {
        // Fallbacks para diferentes tipos de erro
        this.fallbacks.set('ai_integration', {
            primary: 'ai-integration-real.js',
            secondary: 'ai-integration-core.js',
            tertiary: 'ai-system-modern.js',
            local: 'local-ai-fallback.js'
        });

        this.fallbacks.set('chess_engine', {
            primary: 'chess-engine.js',
            secondary: 'smart-chess-board.js',
            tertiary: 'board-initializer.js',
            local: 'local-chess-fallback.js'
        });

        this.fallbacks.set('database', {
            primary: 'chess-pro-database.js',
            secondary: 'chess-pro-integration.js',
            tertiary: 'local-storage-fallback.js',
            local: 'memory-fallback.js'
        });
    }

    setupRecoveryStrategies() {
        // Estratégias de recuperação para diferentes erros
        this.recoveryStrategies.set('network_error', {
            retry: true,
            maxRetries: 3,
            retryDelay: 1000,
            fallback: 'offline_mode'
        });

        this.recoveryStrategies.set('api_error', {
            retry: true,
            maxRetries: 2,
            retryDelay: 2000,
            fallback: 'local_mode'
        });

        this.recoveryStrategies.set('memory_error', {
            retry: false,
            fallback: 'cleanup_and_retry'
        });
    }

    setupGlobalErrorHandling() {
        // Capturar erros globais não tratados
        window.addEventListener('error', (event) => {
            this.handleGlobalError(event.error, event.filename, event.lineno);
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.handleUnhandledRejection(event.reason);
        });
    }

    async handleError(error, context, component) {
        const errorInfo = {
            message: error.message,
            stack: error.stack,
            context: context,
            component: component,
            timestamp: Date.now(),
            userAgent: navigator.userAgent
        };

        console.error('🚨 Erro capturado:', errorInfo);

        // Incrementar contador de erros
        const errorKey = `${component}_${context}`;
        const currentCount = this.errorCount.get(errorKey) || 0;
        this.errorCount.set(errorKey, currentCount + 1);

        // Verificar se excedeu o limite de erros
        if (currentCount >= this.maxErrors) {
            return await this.activateFallback(component, context);
        }

        // Tentar recuperação automática
        return await this.attemptRecovery(error, context, component);
    }

    async attemptRecovery(error, context, component) {
        const errorType = this.classifyError(error);
        const strategy = this.recoveryStrategies.get(errorType);

        if (!strategy) {
            console.warn('⚠️ Estratégia de recuperação não encontrada para:', errorType);
            return false;
        }

        if (strategy.retry) {
            return await this.retryOperation(component, context, strategy);
        } else {
            return await this.activateFallback(component, context);
        }
    }

    classifyError(error) {
        if (error.name === 'NetworkError' || error.message.includes('fetch')) {
            return 'network_error';
        } else if (error.name === 'APIError' || error.message.includes('API')) {
            return 'api_error';
        } else if (error.name === 'MemoryError' || error.message.includes('memory')) {
            return 'memory_error';
        } else if (error.name === 'TypeError' || error.name === 'ReferenceError') {
            return 'code_error';
        }
        return 'unknown_error';
    }

    async retryOperation(component, context, strategy) {
        for (let attempt = 1; attempt <= strategy.maxRetries; attempt++) {
            try {
                console.log(`🔄 Tentativa ${attempt} de recuperação para ${component}`);
                
                // Aguardar antes de tentar novamente
                if (attempt > 1) {
                    await this.delay(strategy.retryDelay * attempt);
                }

                // Tentar reexecutar a operação
                const result = await this.reexecuteOperation(component, context);
                if (result) {
                    console.log(`✅ Recuperação bem-sucedida na tentativa ${attempt}`);
                    return true;
                }
            } catch (retryError) {
                console.warn(`⚠️ Tentativa ${attempt} falhou:`, retryError.message);
            }
        }

        console.error(`❌ Todas as tentativas de recuperação falharam para ${component}`);
        return await this.activateFallback(component, context);
    }

    async reexecuteOperation(component, context) {
        // Implementar lógica de reexecução específica para cada componente
        switch (component) {
            case 'ai_integration':
                return await this.reexecuteAIIntegration(context);
            case 'chess_engine':
                return await this.reexecuteChessEngine(context);
            case 'database':
                return await this.reexecuteDatabase(context);
            default:
                return false;
        }
    }

    async reexecuteAIIntegration(context) {
        try {
            // Tentar reinicializar a integração de IA
            if (window.AIIntegrationCore) {
                const ai = new window.AIIntegrationCore();
                await ai.init();
                return true;
            }
            return false;
        } catch (error) {
            console.warn('⚠️ Falha ao reexecutar integração de IA:', error.message);
            return false;
        }
    }

    async reexecuteChessEngine(context) {
        try {
            // Tentar reinicializar o engine de xadrez
            if (window.ChessBoard) {
                const board = new window.ChessBoard('chessboard', context);
                return true;
            }
            return false;
        } catch (error) {
            console.warn('⚠️ Falha ao reexecutar engine de xadrez:', error.message);
            return false;
        }
    }

    async reexecuteDatabase(context) {
        try {
            // Tentar reconectar ao banco de dados
            if (window.ChessProDatabase) {
                const db = new window.ChessProDatabase();
                await db.connect();
                return true;
            }
            return false;
        } catch (error) {
            console.warn('⚠️ Falha ao reexecutar banco de dados:', error.message);
            return false;
        }
    }

    async activateFallback(component, context) {
        const fallback = this.fallbacks.get(component);
        if (!fallback) {
            console.error('❌ Fallback não encontrado para:', component);
            return false;
        }

        console.log(`🔄 Ativando fallback para ${component}`);

        // Tentar fallbacks em ordem de prioridade
        for (const [priority, fallbackFile] of Object.entries(fallback)) {
            try {
                if (await this.loadFallback(fallbackFile, component, context)) {
                    console.log(`✅ Fallback ${priority} ativado com sucesso: ${fallbackFile}`);
                    return true;
                }
            } catch (error) {
                console.warn(`⚠️ Fallback ${priority} falhou:`, error.message);
            }
        }

        console.error('❌ Todos os fallbacks falharam para:', component);
        return false;
    }

    async loadFallback(fallbackFile, component, context) {
        return new Promise((resolve) => {
            const script = document.createElement('script');
            script.src = `../utils/${fallbackFile}`;
            script.onload = () => {
                console.log(`✅ Fallback carregado: ${fallbackFile}`);
                resolve(true);
            };
            script.onerror = () => {
                console.warn(`⚠️ Falha ao carregar fallback: ${fallbackFile}`);
                resolve(false);
            };
            document.head.appendChild(script);
        });
    }

    handleGlobalError(error, filename, lineno) {
        console.error('🚨 Erro global não tratado:', {
            error: error.message,
            filename,
            lineno,
            stack: error.stack
        });

        // Tentar recuperação automática
        this.handleError(error, 'global', 'system');
    }

    handleUnhandledRejection(reason) {
        console.error('🚨 Promise rejeitada não tratada:', reason);

        // Tentar recuperação automática
        this.handleError(new Error(reason), 'promise', 'system');
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Métodos de utilidade
    getErrorStats() {
        return {
            totalErrors: Array.from(this.errorCount.values()).reduce((a, b) => a + b, 0),
            errorCounts: Object.fromEntries(this.errorCount),
            fallbacks: Object.fromEntries(this.fallbacks),
            recoveryStrategies: Object.fromEntries(this.recoveryStrategies)
        };
    }

    resetErrorCount(component, context) {
        const errorKey = `${component}_${context}`;
        this.errorCount.delete(errorKey);
        console.log(`🔄 Contador de erros resetado para: ${errorKey}`);
    }

    clearAllErrors() {
        this.errorCount.clear();
        console.log('🗑️ Todos os contadores de erro foram limpos');
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.ErrorHandler = ErrorHandler;
    window.errorHandler = new ErrorHandler();
}

// Para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ErrorHandler;
}
