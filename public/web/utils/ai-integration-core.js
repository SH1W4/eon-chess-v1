// AEON CHESS - Core de Integração com IA (Versão Otimizada)
// Versão: 2.1 - Sistema Modular e Otimizado

class AIIntegrationCore {
    constructor() {
        this.config = {
                                    openai: {
                            apiKey: process.env.OPENAI_API_KEY || '[YOUR-OPENAI-KEY]',
                model: 'gpt-5',
                maxTokens: 2000,
                temperature: 0.7
            },
                                    anthropic: {
                            apiKey: process.env.ANTHROPIC_API_KEY || '[YOUR-ANTHROPIC-KEY]',
                model: 'claude-3.5-sonnet-20241022',
                maxTokens: 2000
            },
                                    google: {
                            apiKey: process.env.GOOGLE_AI_KEY || '[YOUR-GOOGLE-AI-KEY]',
                model: 'gemini-2.0-flash-exp',
                maxTokens: 2000
            }
        };

        this.currentProvider = 'openai';
        this.fallbackChain = ['openai', 'anthropic', 'google'];
        this.cache = new Map();
        this.rateLimits = new Map();

        this.init();
    }

    async init() {
        this.setupRateLimiting();
        this.setupCaching();
        console.log('✅ AI Integration Core inicializado');
    }

    setupRateLimiting() {
        this.fallbackChain.forEach(provider => {
            this.rateLimits.set(provider, {
                requests: 0,
                lastReset: Date.now(),
                maxRequests: 100,
                resetInterval: 60000 // 1 minuto
            });
        });
    }

    setupCaching() {
        // Cache simples em memória com limite de tamanho
        this.maxCacheSize = 100;
        this.cacheTimeout = 300000; // 5 minutos
    }

    async generatePosition(prompt, theme, userProfile) {
        const cacheKey = this.generateCacheKey(prompt, theme, userProfile);

        // Verificar cache primeiro
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                console.log('✅ Usando posição do cache');
                return cached.data;
            } else {
                this.cache.delete(cacheKey);
            }
        }

        // Tentar gerar com IA real
        for (const provider of this.fallbackChain) {
            try {
                if (await this.checkRateLimit(provider)) {
                    const position = await this.generateWithProvider(provider, prompt, theme, userProfile);

                    if (position && this.validatePosition(position)) {
                        // Cache da posição
                        this.cachePosition(cacheKey, position);
                        return position;
                    }
                }
            } catch (error) {
                console.warn(`⚠️ Erro com provider ${provider}:`, error.message);
                continue;
            }
        }

        // Fallback para geração local
        return await this.generateLocalFallback(theme, userProfile);
    }

    generateCacheKey(prompt, theme, userProfile) {
        return `${prompt}_${theme}_${userProfile.level}_${userProfile.style}`;
    }

    async checkRateLimit(provider) {
        const limit = this.rateLimits.get(provider);
        const now = Date.now();

        if (now - limit.lastReset > limit.resetInterval) {
            limit.requests = 0;
            limit.lastReset = now;
        }

        if (limit.requests >= limit.maxRequests) {
            return false;
        }

        limit.requests++;
        return true;
    }

    async generateWithProvider(provider, prompt, theme, userProfile) {
        // Implementação simplificada para demonstração
        const response = await this.callAPI(provider, {
            prompt,
            theme,
            userProfile,
            maxTokens: this.config[provider].maxTokens,
            temperature: this.config[provider].temperature || 0.7
        });

        return this.parseAPIResponse(response, provider);
    }

    async callAPI(provider, params) {
        // Simulação de chamada de API
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    success: true,
                    data: {
                        position: this.generateRandomPosition(),
                        evaluation: Math.random() * 2 - 1,
                        moves: this.generateRandomMoves()
                    }
                });
            }, 100 + Math.random() * 200);
        });
    }

    parseAPIResponse(response, provider) {
        if (response.success && response.data) {
            return {
                ...response.data,
                provider,
                timestamp: Date.now()
            };
        }
        return null;
    }

    validatePosition(position) {
        return position && 
               position.position && 
               position.evaluation !== undefined &&
               position.moves && 
               position.moves.length > 0;
    }

    generateRandomPosition() {
        // Gerar posição aleatória válida
        const pieces = ['K', 'Q', 'R', 'B', 'N', 'P'];
        const board = Array(8).fill().map(() => Array(8).fill(''));
        
        // Colocar peças aleatoriamente
        for (let i = 0; i < 16; i++) {
            const piece = pieces[Math.floor(Math.random() * pieces.length)];
            const row = Math.floor(Math.random() * 8);
            const col = Math.floor(Math.random() * 8);
            if (board[row][col] === '') {
                board[row][col] = piece;
            }
        }

        return board;
    }

    generateRandomMoves() {
        const moves = [];
        for (let i = 0; i < 5; i++) {
            moves.push({
                from: `${String.fromCharCode(97 + Math.floor(Math.random() * 8))}${Math.floor(Math.random() * 8) + 1}`,
                to: `${String.fromCharCode(97 + Math.floor(Math.random() * 8))}${Math.floor(Math.random() * 8) + 1}`,
                piece: ['P', 'N', 'B', 'R', 'Q', 'K'][Math.floor(Math.random() * 6)]
            });
        }
        return moves;
    }

    async generateLocalFallback(theme, userProfile) {
        console.log('🔄 Usando fallback local');
        return {
            position: this.generateRandomPosition(),
            evaluation: 0,
            moves: this.generateRandomMoves(),
            provider: 'local',
            timestamp: Date.now()
        };
    }

    cachePosition(key, position) {
        // Limpar cache se estiver muito cheio
        if (this.cache.size >= this.maxCacheSize) {
            const oldestKey = this.cache.keys().next().value;
            this.cache.delete(oldestKey);
        }

        this.cache.set(key, {
            data: position,
            timestamp: Date.now()
        });
    }

    // Métodos de utilidade
    getStatus() {
        return {
            providers: this.fallbackChain,
            currentProvider: this.currentProvider,
            cacheSize: this.cache.size,
            rateLimits: Object.fromEntries(this.rateLimits)
        };
    }

    clearCache() {
        this.cache.clear();
        console.log('🗑️ Cache limpo');
    }

    setProvider(provider) {
        if (this.fallbackChain.includes(provider)) {
            this.currentProvider = provider;
            console.log(`🔄 Provider alterado para: ${provider}`);
            return true;
        }
        console.warn(`⚠️ Provider inválido: ${provider}`);
        return false;
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.AIIntegrationCore = AIIntegrationCore;
}

// Para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIIntegrationCore;
}
