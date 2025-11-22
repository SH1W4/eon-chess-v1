/**
 * 🛡️ Generation Controller - Sistema de Controle de Geração
 * Controla e limita a geração de tabuleiros para prevenir abuso
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class GenerationController {
    constructor() {
        this.name = 'Generation Controller';
        this.version = '1.0.0';

        // Limites de geração
        this.limits = {
            daily: 50, // Máximo por dia
            hourly: 10, // Máximo por hora
            batch: 5, // Máximo por lote
            cooldown: 30000 // Cooldown entre gerações (30s)
        };

        // Contadores
        this.counters = {
            daily: 0,
            hourly: 0,
            lastGeneration: 0
        };

        // Histórico de gerações
        this.generationHistory = [];

        // Status do sistema
        this.status = 'active';

        this.init();
        console.log(`🛡️ ${this.name} v${this.version} inicializando...`);
    }

    /**
     * Inicializar o controlador
     */
    init() {
        this.loadCounters();
        this.startDailyReset();
        this.startHourlyReset();
        this.updateUI();
    }

    /**
     * Carregar contadores do localStorage
     */
    loadCounters() {
        try {
            const saved = localStorage.getItem('generationCounters');
            if (saved) {
                const data = JSON.parse(saved);

                // Verificar se é do mesmo dia
                const today = new Date().toDateString();
                if (data.date === today) {
                    this.counters.daily = data.daily || 0;
                    this.counters.hourly = data.hourly || 0;
                } else {
                    this.resetDailyCounter();
                }

                this.counters.lastGeneration = data.lastGeneration || 0;
            }
        } catch (error) {
            console.error('Erro ao carregar contadores:', error);
            this.resetCounters();
        }
    }

    /**
     * Salvar contadores no localStorage
     */
    saveCounters() {
        try {
            const data = {
                date: new Date().toDateString(),
                daily: this.counters.daily,
                hourly: this.counters.hourly,
                lastGeneration: this.counters.lastGeneration
            };
            localStorage.setItem('generationCounters', JSON.stringify(data));
        } catch (error) {
            console.error('Erro ao salvar contadores:', error);
        }
    }

    /**
     * Resetar contador diário
     */
    resetDailyCounter() {
        this.counters.daily = 0;
        this.saveCounters();
        this.updateUI();
    }

    /**
     * Resetar contador horário
     */
    resetHourlyCounter() {
        this.counters.hourly = 0;
        this.saveCounters();
        this.updateUI();
    }

    /**
     * Resetar todos os contadores
     */
    resetCounters() {
        this.counters.daily = 0;
        this.counters.hourly = 0;
        this.counters.lastGeneration = 0;
        this.saveCounters();
        this.updateUI();
    }

    /**
     * Iniciar reset diário automático
     */
    startDailyReset() {
        const now = new Date();
        const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
        const timeUntilMidnight = tomorrow - now;

        setTimeout(() => {
            this.resetDailyCounter();
            this.startDailyReset(); // Agendar próximo reset
        }, timeUntilMidnight);
    }

    /**
     * Iniciar reset horário automático
     */
    startHourlyReset() {
        const now = new Date();
        const nextHour = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1);
        const timeUntilNextHour = nextHour - now;

        setTimeout(() => {
            this.resetHourlyCounter();
            this.startHourlyReset(); // Agendar próximo reset
        }, timeUntilNextHour);
    }

    /**
     * Verificar se pode gerar
     */
    canGenerate(type = 'single') {
        // Verificar status do sistema
        if (this.status !== 'active') {
            return {
                allowed: false,
                reason: 'Sistema temporariamente indisponível',
                code: 'SYSTEM_DISABLED'
            };
        }

        // Verificar limite diário
        if (this.counters.daily >= this.limits.daily) {
            return {
                allowed: false,
                reason: 'Limite diário atingido',
                code: 'DAILY_LIMIT_REACHED',
                resetTime: this.getNextResetTime('daily')
            };
        }

        // Verificar limite horário
        if (this.counters.hourly >= this.limits.hourly) {
            return {
                allowed: false,
                reason: 'Limite horário atingido',
                code: 'HOURLY_LIMIT_REACHED',
                resetTime: this.getNextResetTime('hourly')
            };
        }

        // Verificar cooldown
        const timeSinceLastGeneration = Date.now() - this.counters.lastGeneration;
        if (timeSinceLastGeneration < this.limits.cooldown) {
            const remainingCooldown = Math.ceil((this.limits.cooldown - timeSinceLastGeneration) / 1000);
            return {
                allowed: false,
                reason: `Aguarde ${remainingCooldown}s antes da próxima geração`,
                code: 'COOLDOWN_ACTIVE',
                remainingTime: remainingCooldown
            };
        }

        // Verificar limite de lote
        if (type === 'batch' && this.counters.daily + this.limits.batch > this.limits.daily) {
            return {
                allowed: false,
                reason: 'Lote excederia o limite diário',
                code: 'BATCH_LIMIT_EXCEEDED'
            };
        }

        return {
            allowed: true
        };
    }

    /**
     * Registrar geração
     */
    recordGeneration(type = 'single', count = 1) {
        const check = this.canGenerate(type);
        if (!check.allowed) {
            throw new Error(check.reason);
        }

        // Atualizar contadores
        this.counters.daily += count;
        this.counters.hourly += count;
        this.counters.lastGeneration = Date.now();

        // Registrar no histórico
        this.generationHistory.push({
            timestamp: Date.now(),
            type: type,
            count: count,
            userAgent: navigator.userAgent
        });

        // Manter apenas últimas 100 gerações
        if (this.generationHistory.length > 100) {
            this.generationHistory = this.generationHistory.slice(-100);
        }

        // Salvar contadores
        this.saveCounters();

        // Atualizar UI
        this.updateUI();

        return {
            success: true,
            remainingDaily: this.limits.daily - this.counters.daily,
            remainingHourly: this.limits.hourly - this.counters.hourly
        };
    }

    /**
     * Obter tempo até próximo reset
     */
    getNextResetTime(type) {
        const now = new Date();

        if (type === 'daily') {
            const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
            return tomorrow;
        } else if (type === 'hourly') {
            const nextHour = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1);
            return nextHour;
        }

        return null;
    }

    /**
     * Formatar tempo restante
     */
    formatTimeRemaining(targetTime) {
        const now = new Date();
        const diff = targetTime - now;

        if (diff <= 0) return 'Agora';

        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }

    /**
     * Atualizar interface
     */
    updateUI() {
        // Atualizar contadores na UI
        const dailyLimitElement = document.getElementById('daily-limit');
        const dailyUsedElement = document.getElementById('daily-used');

        if (dailyLimitElement) {
            dailyLimitElement.textContent = this.limits.daily;
        }

        if (dailyUsedElement) {
            dailyUsedElement.textContent = this.counters.daily;
        }

        // Atualizar status dos botões
        this.updateButtonStates();
    }

    /**
     * Atualizar estados dos botões
     */
    updateButtonStates() {
        const generateBtn = document.getElementById('generate-board');
        const batchBtn = document.getElementById('batch-generate');
        const smartBtn = document.getElementById('smart-generate');

        // Verificar geração única
        const singleCheck = this.canGenerate('single');
        if (generateBtn) {
            if (singleCheck.allowed) {
                generateBtn.disabled = false;
                generateBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                generateBtn.disabled = true;
                generateBtn.classList.add('opacity-50', 'cursor-not-allowed');
                generateBtn.title = singleCheck.reason;
            }
        }

        // Verificar geração em lote
        const batchCheck = this.canGenerate('batch');
        if (batchBtn) {
            if (batchCheck.allowed) {
                batchBtn.disabled = false;
                batchBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                batchBtn.disabled = true;
                batchBtn.classList.add('opacity-50', 'cursor-not-allowed');
                batchBtn.title = batchCheck.reason;
            }
        }

        // Verificar orquestração
        const smartCheck = this.canGenerate('single');
        if (smartBtn) {
            if (smartCheck.allowed) {
                smartBtn.disabled = false;
                smartBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                smartBtn.disabled = true;
                smartBtn.classList.add('opacity-50', 'cursor-not-allowed');
                smartBtn.title = smartCheck.reason;
            }
        }
    }

    /**
     * Obter estatísticas
     */
    getStats() {
        return {
            limits: this.limits,
            counters: this.counters,
            history: this.generationHistory,
            status: this.status
        };
    }

    /**
     * Definir status do sistema
     */
    setStatus(status) {
        this.status = status;
        this.updateUI();
    }

    /**
     * Definir limites
     */
    setLimits(limits) {
        this.limits = {
            ...this.limits,
            ...limits
        };
        this.updateUI();
    }

    /**
     * Obter relatório de uso
     */
    getUsageReport() {
        const now = new Date();
        const today = now.toDateString();

        // Estatísticas do dia
        const todayGenerations = this.generationHistory.filter(gen => {
            return new Date(gen.timestamp).toDateString() === today;
        });

        // Estatísticas por tipo
        const typeStats = {};
        todayGenerations.forEach(gen => {
            typeStats[gen.type] = (typeStats[gen.type] || 0) + gen.count;
        });

        return {
            date: today,
            dailyUsed: this.counters.daily,
            dailyRemaining: this.limits.daily - this.counters.daily,
            hourlyUsed: this.counters.hourly,
            hourlyRemaining: this.limits.hourly - this.counters.hourly,
            typeBreakdown: typeStats,
            nextDailyReset: this.getNextResetTime('daily'),
            nextHourlyReset: this.getNextResetTime('hourly')
        };
    }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.GenerationController = GenerationController;
}

// Auto-inicialização se estiver no navegador
if (typeof window !== 'undefined' && window.addEventListener) {
    window.addEventListener('DOMContentLoaded', () => {
        console.log('🛡️ Generation Controller carregado e pronto para uso!');
    });