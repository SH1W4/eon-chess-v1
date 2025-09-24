/**
 * 🎼 Orquestrador Inteligente de IA - Aeon Chess
 * 
 * Este sistema coordena e otimiza todas as funcionalidades de IA:
 * - Coordenação entre personalidades
 * - Otimização de recursos
 * - Aprendizado adaptativo
 * - Balanceamento de carga
 * 
 * @version 2.0.0
 * @author Aeon Chess Team
 */

class AIOrchestrator {
    constructor(aiSystem) {
        this.aiSystem = aiSystem;
        this.tasks = new Map();
        this.resources = new Map();
        this.performance = new Map();
        this.learning = new Map();
        
        this.initializeResources();
        this.initializePerformanceTracking();
        this.initializeLearning();
        
        console.log('🎼 Orquestrador de IA inicializado');
    }

    /**
     * Inicializa recursos do sistema
     */
    initializeResources() {
        this.resources.set('cpu', { current: 0, max: 100, unit: '%' });
        this.resources.set('memory', { current: 0, max: 512, unit: 'MB' });
        this.resources.set('network', { current: 0, max: 1000, unit: 'KB/s' });
        this.resources.set('ai_instances', { current: 0, max: 10, unit: 'count' });
        
        // Monitora recursos em tempo real
        this.startResourceMonitoring();
    }

    /**
     * Inicializa rastreamento de performance
     */
    initializePerformanceTracking() {
        this.performance.set('response_time', []);
        this.performance.set('accuracy', []);
        this.performance.set('user_satisfaction', []);
        this.performance.set('resource_efficiency', []);
        
        // Inicia coleta de métricas
        this.startPerformanceCollection();
    }

    /**
     * Inicializa sistema de aprendizado
     */
    initializeLearning() {
        this.learning.set('user_preferences', new Map());
        this.learning.set('task_patterns', new Map());
        this.learning.set('optimization_rules', new Map());
        this.learning.set('failure_patterns', new Map());
        
        // Carrega dados de aprendizado salvos
        this.loadLearningData();
    }

    /**
     * Inicia monitoramento de recursos
     */
    startResourceMonitoring() {
        setInterval(() => {
            this.updateResourceUsage();
        }, 2000); // Atualiza a cada 2 segundos
    }

    /**
     * Inicia coleta de métricas de performance
     */
    startPerformanceCollection() {
        setInterval(() => {
            this.collectPerformanceMetrics();
        }, 5000); // Coleta a cada 5 segundos
    }

    /**
     * Atualiza uso de recursos
     */
    updateResourceUsage() {
        // Simula monitoramento de recursos (em produção seria integrado com APIs do sistema)
        this.resources.get('cpu').current = Math.random() * 80 + 10; // 10-90%
        this.resources.get('memory').current = Math.random() * 400 + 50; // 50-450MB
        this.resources.get('network').current = Math.random() * 800 + 100; // 100-900KB/s
        this.resources.get('ai_instances').current = Math.floor(Math.random() * 8) + 1; // 1-8 instâncias
        
        // Verifica se há sobrecarga
        this.checkResourceOverload();
    }

    /**
     * Verifica sobrecarga de recursos
     */
    checkResourceOverload() {
        const cpu = this.resources.get('cpu');
        const memory = this.resources.get('memory');
        
        if (cpu.current > 80) {
            console.warn('⚠️ Alto uso de CPU detectado:', cpu.current.toFixed(1) + '%');
            this.optimizeResourceUsage('cpu');
        }
        
        if (memory.current > 400) {
            console.warn('⚠️ Alto uso de memória detectado:', memory.current.toFixed(1) + 'MB');
            this.optimizeResourceUsage('memory');
        }
    }

    /**
     * Otimiza uso de recursos
     */
    optimizeResourceUsage(resourceType) {
        switch (resourceType) {
            case 'cpu':
                // Reduz complexidade de análises
                this.aiSystem.activePersonality.analysisDepth = Math.max(3, this.aiSystem.activePersonality.analysisDepth - 1);
                console.log('🎯 Reduzida profundidade de análise para otimizar CPU');
                break;
                
            case 'memory':
                // Limpa caches e dados temporários
                this.clearTemporaryData();
                console.log('🧹 Cache limpo para otimizar memória');
                break;
        }
    }

    /**
     * Limpa dados temporários
     */
    clearTemporaryData() {
        // Limpa dados não essenciais
        this.tasks.clear();
        this.performance.forEach((metrics, key) => {
            if (metrics.length > 100) {
                metrics.splice(0, 50); // Mantém apenas as 50 métricas mais recentes
            }
        });
    }

    /**
     * Coleta métricas de performance
     */
    collectPerformanceMetrics() {
        const now = Date.now();
        
        // Simula métricas de performance
        const responseTime = Math.random() * 2000 + 100; // 100-2100ms
        const accuracy = Math.random() * 0.3 + 0.7; // 70-100%
        const userSatisfaction = Math.random() * 0.4 + 0.6; // 60-100%
        const resourceEfficiency = this.calculateResourceEfficiency();
        
        // Adiciona métricas
        this.performance.get('response_time').push({ timestamp: now, value: responseTime });
        this.performance.get('accuracy').push({ timestamp: now, value: accuracy });
        this.performance.get('user_satisfaction').push({ timestamp: now, value: userSatisfaction });
        this.performance.get('resource_efficiency').push({ timestamp: now, value: resourceEfficiency });
        
        // Analisa tendências
        this.analyzePerformanceTrends();
    }

    /**
     * Calcula eficiência de recursos
     */
    calculateResourceEfficiency() {
        const cpu = this.resources.get('cpu');
        const memory = this.resources.get('memory');
        
        // Eficiência baseada no uso de recursos (menor = melhor)
        const cpuEfficiency = 1 - (cpu.current / cpu.max);
        const memoryEfficiency = 1 - (memory.current / memory.max);
        
        return (cpuEfficiency + memoryEfficiency) / 2;
    }

    /**
     * Analisa tendências de performance
     */
    analyzePerformanceTrends() {
        const metrics = ['response_time', 'accuracy', 'user_satisfaction', 'resource_efficiency'];
        
        metrics.forEach(metric => {
            const data = this.performance.get(metric);
            if (data.length >= 10) {
                const recent = data.slice(-10);
                const older = data.slice(-20, -10);
                
                const recentAvg = recent.reduce((sum, item) => sum + item.value, 0) / recent.length;
                const olderAvg = older.reduce((sum, item) => sum + item.value, 0) / older.length;
                
                const trend = recentAvg - olderAvg;
                const trendDirection = trend > 0 ? 'melhorando' : trend < 0 ? 'piorando' : 'estável';
                
                console.log(`📈 ${metric}: ${trendDirection} (${trend > 0 ? '+' : ''}${trend.toFixed(3)})`);
                
                // Aplica otimizações baseadas em tendências
                this.applyTrendBasedOptimizations(metric, trend);
            }
        });
    }

    /**
     * Aplica otimizações baseadas em tendências
     */
    applyTrendBasedOptimizations(metric, trend) {
        switch (metric) {
            case 'response_time':
                if (trend > 500) { // Piorando
                    this.aiSystem.activePersonality.analysisDepth = Math.max(2, this.aiSystem.activePersonality.analysisDepth - 1);
                    console.log('⚡ Reduzida profundidade para melhorar tempo de resposta');
                }
                break;
                
            case 'accuracy':
                if (trend < -0.1) { // Piorando
                    this.aiSystem.activePersonality.analysisDepth = Math.min(10, this.aiSystem.activePersonality.analysisDepth + 1);
                    console.log('🎯 Aumentada profundidade para melhorar precisão');
                }
                break;
                
            case 'user_satisfaction':
                if (trend < -0.1) { // Piorando
                    this.optimizeUserExperience();
                }
                break;
        }
    }

    /**
     * Otimiza experiência do usuário
     */
    optimizeUserExperience() {
        // Ajusta personalidade para melhor experiência
        const currentStyle = this.aiSystem.activePersonality.style;
        
        if (currentStyle === 'competitive' && this.performance.get('user_satisfaction').slice(-5).some(p => p.value < 0.5)) {
            // Muda para personalidade mais amigável se satisfação estiver baixa
            this.aiSystem.changePersonality('teacher');
            console.log('🎭 Personalidade alterada para melhorar experiência do usuário');
        }
    }

    /**
     * Orquestra tarefa de IA
     */
    async orchestrateTask(taskType, parameters) {
        const taskId = this.generateTaskId();
        const startTime = Date.now();
        
        try {
            // Verifica recursos disponíveis
            if (!this.checkResourceAvailability(taskType)) {
                throw new Error('Recursos insuficientes para executar tarefa');
            }
            
            // Cria tarefa
            const task = {
                id: taskId,
                type: taskType,
                parameters: parameters,
                startTime: startTime,
                status: 'running',
                personality: this.aiSystem.activePersonality.style,
                priority: this.calculateTaskPriority(taskType, parameters)
            };
            
            this.tasks.set(taskId, task);
            
            // Executa tarefa baseada no tipo
            let result;
            switch (taskType) {
                case 'analysis':
                    result = await this.executeAnalysis(parameters);
                    break;
                case 'generation':
                    result = await this.executeGeneration(parameters);
                    break;
                case 'teaching':
                    result = await this.executeTeaching(parameters);
                    break;
                default:
                    throw new Error(`Tipo de tarefa não suportado: ${taskType}`);
            }
            
            // Atualiza tarefa
            task.status = 'completed';
            task.endTime = Date.now();
            task.duration = task.endTime - task.startTime;
            task.result = result;
            
            // Aprende com a execução
            this.learnFromTaskExecution(task);
            
            return result;
            
        } catch (error) {
            // Atualiza tarefa com erro
            const task = this.tasks.get(taskId);
            if (task) {
                task.status = 'failed';
                task.error = error.message;
                task.endTime = Date.now();
                task.duration = task.endTime - task.startTime;
            }
            
            // Aprende com o erro
            this.learnFromFailure(taskType, error);
            
            throw error;
        }
    }

    /**
     * Verifica disponibilidade de recursos
     */
    checkResourceAvailability(taskType) {
        const cpu = this.resources.get('cpu');
        const memory = this.resources.get('memory');
        
        // Diferentes tipos de tarefa têm diferentes requisitos
        const requirements = {
            analysis: { cpu: 20, memory: 50 },
            generation: { cpu: 30, memory: 80 },
            teaching: { cpu: 15, memory: 40 }
        };
        
        const req = requirements[taskType] || { cpu: 25, memory: 60 };
        
        return cpu.current + req.cpu <= cpu.max && memory.current + req.memory <= memory.max;
    }

    /**
     * Calcula prioridade da tarefa
     */
    calculateTaskPriority(taskType, parameters) {
        let priority = 5; // Prioridade padrão
        
        // Análise tem prioridade alta
        if (taskType === 'analysis') priority += 2;
        
        // Ensino tem prioridade média-alta
        if (taskType === 'teaching') priority += 1;
        
        // Geração tem prioridade média
        if (taskType === 'generation') priority += 0;
        
        // Ajusta baseado em parâmetros
        if (parameters.urgent) priority += 3;
        if (parameters.complexity === 'high') priority += 1;
        
        return Math.min(10, Math.max(1, priority));
    }

    /**
     * Executa análise
     */
    async executeAnalysis(parameters) {
        const { fen, depth } = parameters;
        return await this.aiSystem.analyzeBoard(fen, depth);
    }

    /**
     * Executa geração
     */
    async executeGeneration(parameters) {
        const { theme, complexity } = parameters;
        return await this.aiSystem.generateBoard(theme, complexity);
    }

    /**
     * Executa ensino
     */
    async executeTeaching(parameters) {
        const { topic, level } = parameters;
        return await this.aiSystem.startTeaching(topic, level);
    }

    /**
     * Aprende com execução da tarefa
     */
    learnFromTaskExecution(task) {
        // Aprende padrões de execução
        const patternKey = `${task.type}_${task.personality}`;
        const patterns = this.learning.get('task_patterns');
        
        if (!patterns.has(patternKey)) {
            patterns.set(patternKey, []);
        }
        
        patterns.get(patternKey).push({
            duration: task.duration,
            success: task.status === 'completed',
            timestamp: task.startTime
        });
        
        // Mantém apenas os últimos 100 padrões
        if (patterns.get(patternKey).length > 100) {
            patterns.get(patternKey).splice(0, 50);
        }
        
        // Aprende preferências do usuário
        this.learnUserPreferences(task);
    }

    /**
     * Aprende preferências do usuário
     */
    learnUserPreferences(task) {
        const preferences = this.learning.get('user_preferences');
        
        // Aprende preferência por personalidade
        if (task.status === 'completed') {
            const personalityKey = `preferred_${task.type}`;
            if (!preferences.has(personalityKey)) {
                preferences.set(personalityKey, new Map());
            }
            
            const personalityPrefs = preferences.get(personalityKey);
            const currentCount = personalityPrefs.get(task.personality) || 0;
            personalityPrefs.set(task.personality, currentCount + 1);
        }
        
        // Salva dados de aprendizado
        this.saveLearningData();
    }

    /**
     * Aprende com falhas
     */
    learnFromFailure(taskType, error) {
        const failures = this.learning.get('failure_patterns');
        
        if (!failures.has(taskType)) {
            failures.set(taskType, []);
        }
        
        failures.get(taskType).push({
            error: error.message,
            timestamp: Date.now(),
            personality: this.aiSystem.activePersonality.style
        });
        
        // Mantém apenas os últimos 50 falhas
        if (failures.get(taskType).length > 50) {
            failures.get(taskType).splice(0, 25);
        }
        
        // Aplica correções baseadas em falhas
        this.applyFailureBasedCorrections(taskType, error);
    }

    /**
     * Aplica correções baseadas em falhas
     */
    applyFailureBasedCorrections(taskType, error) {
        const failures = this.learning.get('failure_patterns');
        const recentFailures = failures.get(taskType) || [];
        
        // Se há muitas falhas recentes, tenta otimizar
        const recentFailuresCount = recentFailures.filter(f => 
            Date.now() - f.timestamp < 300000 // Últimos 5 minutos
        ).length;
        
        if (recentFailuresCount > 3) {
            console.warn(`⚠️ Muitas falhas detectadas para ${taskType}, aplicando otimizações`);
            
            // Reduz complexidade
            if (this.aiSystem.activePersonality.analysisDepth > 3) {
                this.aiSystem.activePersonality.analysisDepth--;
                console.log('🔧 Reduzida complexidade devido a falhas');
            }
            
            // Muda para personalidade mais estável
            if (this.aiSystem.activePersonality.style !== 'teacher') {
                this.aiSystem.changePersonality('teacher');
                console.log('🎭 Mudança para personalidade mais estável devido a falhas');
            }
        }
    }

    /**
     * Gera ID único para tarefa
     */
    generateTaskId() {
        return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Carrega dados de aprendizado salvos
     */
    loadLearningData() {
        try {
            const savedData = localStorage.getItem('aiLearningData');
            if (savedData) {
                const data = JSON.parse(savedData);
                
                // Restaura dados de aprendizado
                Object.keys(data).forEach(key => {
                    if (this.learning.has(key)) {
                        if (key === 'user_preferences') {
                            // Restaura Map aninhado
                            const preferences = new Map();
                            Object.keys(data[key]).forEach(prefKey => {
                                preferences.set(prefKey, new Map(Object.entries(data[key][prefKey])));
                            });
                            this.learning.set(key, preferences);
                        } else {
                            this.learning.set(key, new Map(Object.entries(data[key])));
                        }
                    }
                });
                
                console.log('📚 Dados de aprendizado carregados');
            }
        } catch (error) {
            console.warn('Erro ao carregar dados de aprendizado:', error);
        }
    }

    /**
     * Salva dados de aprendizado
     */
    saveLearningData() {
        try {
            const dataToSave = {};
            
            this.learning.forEach((value, key) => {
                if (key === 'user_preferences') {
                    // Converte Map aninhado para objeto
                    const preferences = {};
                    value.forEach((innerMap, prefKey) => {
                        preferences[prefKey] = Object.fromEntries(innerMap);
                    });
                    dataToSave[key] = preferences;
                } else {
                    dataToSave[key] = Object.fromEntries(value);
                }
            });
            
            localStorage.setItem('aiLearningData', JSON.stringify(dataToSave));
        } catch (error) {
            console.warn('Erro ao salvar dados de aprendizado:', error);
        }
    }

    /**
     * Obtém estatísticas do orquestrador
     */
    getOrchestratorStats() {
        const totalTasks = this.tasks.size;
        const completedTasks = Array.from(this.tasks.values()).filter(t => t.status === 'completed').length;
        const failedTasks = Array.from(this.tasks.values()).filter(t => t.status === 'failed').length;
        const runningTasks = Array.from(this.tasks.values()).filter(t => t.status === 'running').length;
        
        const avgResponseTime = this.calculateAverageResponseTime();
        const resourceEfficiency = this.calculateResourceEfficiency();
        
        return {
            totalTasks,
            completedTasks,
            failedTasks,
            runningTasks,
            successRate: totalTasks > 0 ? (completedTasks / totalTasks * 100).toFixed(1) : 0,
            avgResponseTime: avgResponseTime.toFixed(0),
            resourceEfficiency: (resourceEfficiency * 100).toFixed(1),
            activePersonalities: this.aiSystem.personalities.size,
            learningDataSize: this.getLearningDataSize(),
            timestamp: Date.now()
        };
    }

    /**
     * Calcula tempo médio de resposta
     */
    calculateAverageResponseTime() {
        const completedTasks = Array.from(this.tasks.values()).filter(t => t.status === 'completed');
        if (completedTasks.length === 0) return 0;
        
        const totalDuration = completedTasks.reduce((sum, task) => sum + task.duration, 0);
        return totalDuration / completedTasks.length;
    }

    /**
     * Obtém tamanho dos dados de aprendizado
     */
    getLearningDataSize() {
        let size = 0;
        this.learning.forEach((value, key) => {
            size += value.size;
        });
        return size;
    }

    /**
     * Obtém recomendações de otimização
     */
    getOptimizationRecommendations() {
        const recommendations = [];
        
        // Verifica performance
        const responseTimeData = this.performance.get('response_time');
        if (responseTimeData.length > 0) {
            const recentAvg = responseTimeData.slice(-10).reduce((sum, item) => sum + item.value, 0) / 10;
            if (recentAvg > 1500) {
                recommendations.push({
                    type: 'performance',
                    priority: 'high',
                    message: 'Tempo de resposta alto detectado. Considere reduzir profundidade de análise.',
                    action: 'reduce_analysis_depth'
                });
            }
        }
        
        // Verifica recursos
        const cpu = this.resources.get('cpu');
        if (cpu.current > 70) {
            recommendations.push({
                type: 'resource',
                priority: 'medium',
                message: 'Uso de CPU elevado. Considere otimizar operações.',
                action: 'optimize_cpu_usage'
            });
        }
        
        // Verifica falhas
        const failures = this.learning.get('failure_patterns');
        failures.forEach((failureList, taskType) => {
            const recentFailures = failureList.filter(f => Date.now() - f.timestamp < 600000); // Últimos 10 minutos
            if (recentFailures.length > 2) {
                recommendations.push({
                    type: 'reliability',
                    priority: 'high',
                    message: `Muitas falhas em ${taskType}. Considere mudar personalidade ou reduzir complexidade.`,
                    action: 'change_personality'
                });
            }
        });
        
        return recommendations;
    }

    /**
     * Aplica recomendação de otimização
     */
    applyOptimizationRecommendation(recommendation) {
        switch (recommendation.action) {
            case 'reduce_analysis_depth':
                this.aiSystem.activePersonality.analysisDepth = Math.max(2, this.aiSystem.activePersonality.analysisDepth - 1);
                console.log('🔧 Aplicada otimização: profundidade de análise reduzida');
                break;
                
            case 'optimize_cpu_usage':
                this.optimizeResourceUsage('cpu');
                console.log('🔧 Aplicada otimização: uso de CPU otimizado');
                break;
                
            case 'change_personality':
                this.aiSystem.changePersonality('teacher');
                console.log('🔧 Aplicada otimização: personalidade alterada para mais estável');
                break;
        }
        
        return true;
    }
}

// Exporta para uso global
window.AIOrchestrator = AIOrchestrator;

console.log('🎼 Orquestrador de IA carregado');
