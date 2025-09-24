// AEON CHESS - Sistema de Orquestração Inteligente "AEON Brain"
// Versão: 1.0 - Orquestrador Adaptativo Multi-IA com Aprendizado Contínuo
// Inspirado na estratégia da MANUS AI: Multi-agente mascarado como agente único

class AEONBrainOrchestrator {
    constructor() {
        this.name = 'AEON Brain';
        this.version = '1.0.0';
        this.intelligence = 'adaptive';

        // Sistema de IA disponível
        this.aiModels = new Map();
        this.modelCapabilities = new Map();
        this.performanceMetrics = new Map();
        this.learningEngine = new LearningEngine();
        this.taskAnalyzer = new TaskAnalyzer();
        this.costOptimizer = new CostOptimizer();

        // Cache inteligente e histórico de decisões
        this.decisionCache = new Map();
        this.decisionHistory = [];
        this.performanceHistory = [];

        // Configurações do orquestrador
        this.config = {
            autoSelection: true,
            learningEnabled: true,
            costOptimization: true,
            qualityThreshold: 0.85,
            maxRetries: 3,
            fallbackStrategy: 'intelligent'
        };

        this.init();
    }

    async init() {
        console.log(`🧠 ${this.name} v${this.version} inicializando...`);

        await this.initializeAIModels();
        await this.initializeCapabilities();
        await this.initializeLearningEngine();
        await this.loadPerformanceData();

        console.log(`🧠 ${this.name} inicializado com sucesso!`);
        console.log(`📊 Modelos disponíveis: ${this.aiModels.size}`);
        console.log(`🎯 Modo: ${this.intelligence}`);
    }

    async initializeAIModels() {
        // Inicializar todos os modelos de IA disponíveis
        const models = [{
                id: 'openai-gpt5',
                name: 'OpenAI GPT-5',
                provider: 'openai',
                capabilities: ['reasoning', 'code_generation', 'multimodal', 'chess_expertise'],
                performance: {
                    accuracy: 0.95,
                    speed: 0.8,
                    cost: 0.3
                },
                specializations: ['complex_strategy', 'creative_positions', 'code_validation']
            },
            {
                id: 'anthropic-claude35',
                name: 'Claude 3.5 Sonnet',
                provider: 'anthropic',
                capabilities: ['reasoning', 'mathematics', 'vision', 'chess_analysis'],
                performance: {
                    accuracy: 0.92,
                    speed: 0.7,
                    cost: 0.4
                },
                specializations: ['mathematical_analysis', 'position_evaluation', 'strategic_planning']
            },
            {
                id: 'google-gemini2',
                name: 'Google Gemini 2.0',
                provider: 'google',
                capabilities: ['multimodal', 'reasoning', 'mathematics', 'pattern_recognition'],
                performance: {
                    accuracy: 0.90,
                    speed: 0.75,
                    cost: 0.35
                },
                specializations: ['visual_patterns', 'mathematical_optimization', 'multimodal_analysis']
            },
            {
                id: 'groq-llama32',
                name: 'Groq Llama 3.2',
                provider: 'groq',
                capabilities: ['ultra_fast', 'reasoning', 'mathematics', 'efficiency'],
                performance: {
                    accuracy: 0.88,
                    speed: 0.95,
                    cost: 0.2
                },
                specializations: ['rapid_generation', 'batch_processing', 'real_time_analysis']
            },
            {
                id: 'together-llama32',
                name: 'Together AI Llama 3.2',
                provider: 'together',
                capabilities: ['open_source', 'customizable', 'cost_effective', 'chess_specialized'],
                performance: {
                    accuracy: 0.87,
                    speed: 0.6,
                    cost: 0.15
                },
                specializations: ['cost_optimization', 'custom_training', 'specialized_chess']
            },
            {
                id: 'chess-ai-v2',
                name: 'Chess AI v2',
                provider: 'chessai',
                capabilities: ['chess_expertise', 'opening_database', 'endgame_tablebase', 'position_validation'],
                performance: {
                    accuracy: 0.94,
                    speed: 0.8,
                    cost: 0.25
                },
                specializations: ['opening_theory', 'endgame_analysis', 'position_validation', 'chess_specific']
            },
            {
                id: 'local-ml',
                name: 'Local ML Models',
                provider: 'local',
                capabilities: ['offline', 'privacy', 'custom_training', 'real_time'],
                performance: {
                    accuracy: 0.82,
                    speed: 0.9,
                    cost: 0.05
                },
                specializations: ['privacy_focused', 'real_time_learning', 'custom_chess_models']
            }
        ];

        for (const model of models) {
            this.aiModels.set(model.id, model);
            this.modelCapabilities.set(model.id, model.capabilities);
            this.performanceMetrics.set(model.id, model.performance);
        }
    }

    async initializeCapabilities() {
        // Mapear capacidades para tipos de tarefas
        this.capabilityMapping = {
            'chess_position_generation': {
                primary: ['openai-gpt5', 'anthropic-claude35'],
                secondary: ['google-gemini2', 'chess-ai-v2'],
                fallback: ['together-llama32', 'local-ml']
            },
            'complex_strategy_analysis': {
                primary: ['openai-gpt5', 'anthropic-claude35'],
                secondary: ['google-gemini2'],
                fallback: ['chess-ai-v2', 'together-llama32']
            },
            'mathematical_optimization': {
                primary: ['anthropic-claude35', 'google-gemini2'],
                secondary: ['openai-gpt5', 'groq-llama32'],
                fallback: ['together-llama32', 'local-ml']
            },
            'rapid_generation': {
                primary: ['groq-llama32', 'local-ml'],
                secondary: ['openai-gpt5', 'google-gemini2'],
                fallback: ['together-llama32', 'chess-ai-v2']
            },
            'cost_optimized': {
                primary: ['together-llama32', 'local-ml'],
                secondary: ['chess-ai-v2', 'groq-llama32'],
                fallback: ['google-gemini2', 'anthropic-claude35']
            },
            'privacy_focused': {
                primary: ['local-ml'],
                secondary: ['together-llama32'],
                fallback: ['chess-ai-v2']
            }
        };
    }

    async initializeLearningEngine() {
        await this.learningEngine.initialize();
        console.log('🧠 Engine de aprendizado inicializado');
    }

    async loadPerformanceData() {
        // Carregar dados de performance salvos
        const saved = localStorage.getItem('aeonBrainPerformance');
        if (saved) {
            this.performanceHistory = JSON.parse(saved);
        }
    }

    // Método principal de orquestração - interface única para o usuário
    async generateChessPosition(task, userProfile, preferences = {}) {
        console.log(`🧠 ${this.name} recebeu tarefa: ${task.type}`);

        try {
            // 1. Analisar a tarefa e contexto
            const taskAnalysis = await this.taskAnalyzer.analyze(task, userProfile, preferences);

            // 2. Selecionar a melhor IA automaticamente
            const selectedModel = await this.selectOptimalModel(taskAnalysis);

            // 3. Executar a tarefa com a IA selecionada
            const result = await this.executeTask(selectedModel, task, taskAnalysis);

            // 4. Avaliar performance e aprender
            await this.evaluateAndLearn(selectedModel, taskAnalysis, result);

            // 5. Retornar resultado unificado (usuário não sabe qual IA foi usada)
            return this.unifyResult(result, selectedModel);

        } catch (error) {
            console.error(`🧠 Erro no orquestrador:`, error);
            return await this.handleError(task, error);
        }
    }

    async selectOptimalModel(taskAnalysis) {
        const {
            taskType,
            complexity,
            urgency,
            costSensitivity,
            qualityRequirement
        } = taskAnalysis;

        // Usar cache de decisões se disponível
        const cacheKey = this.generateCacheKey(taskAnalysis);
        if (this.decisionCache.has(cacheKey)) {
            const cachedDecision = this.decisionCache.get(cacheKey);
            if (this.isDecisionValid(cachedDecision)) {
                console.log(`🧠 Usando decisão em cache: ${cachedDecision.modelId}`);
                return cachedDecision;
            }
        }

        // Calcular score para cada modelo disponível
        const modelScores = await this.calculateModelScores(taskAnalysis);

        // Selecionar modelo com melhor score
        const bestModel = this.selectBestModel(modelScores);

        // Cache da decisão
        this.decisionCache.set(cacheKey, bestModel);

        console.log(`🧠 Modelo selecionado: ${bestModel.modelId} (score: ${bestModel.score.toFixed(3)})`);
        return bestModel;
    }

    async calculateModelScores(taskAnalysis) {
        const scores = [];

        for (const [modelId, model] of this.aiModels) {
            let score = 0;

            // Score base de performance
            const performance = this.performanceMetrics.get(modelId);
            score += performance.accuracy * 0.4;
            score += performance.speed * 0.3;
            score += (1 - performance.cost) * 0.2;

            // Score de especialização para a tarefa
            const specializationScore = this.calculateSpecializationScore(modelId, taskAnalysis);
            score += specializationScore * 0.3;

            // Score de disponibilidade e rate limit
            const availabilityScore = await this.checkModelAvailability(modelId);
            score += availabilityScore * 0.2;

            // Score de custo-benefício
            const costBenefitScore = this.calculateCostBenefitScore(modelId, taskAnalysis);
            score += costBenefitScore * 0.1;

            scores.push({
                modelId,
                score: Math.min(score, 1.0),
                breakdown: {
                    performance: performance.accuracy * 0.4 + performance.speed * 0.3 + (1 - performance.cost) * 0.2,
                    specialization: specializationScore * 0.3,
                    availability: availabilityScore * 0.2,
                    costBenefit: costBenefitScore * 0.1
                }
            });
        }

        // Ordenar por score
        return scores.sort((a, b) => b.score - a.score);
    }

    calculateSpecializationScore(modelId, taskAnalysis) {
        const model = this.aiModels.get(modelId);
        const capabilities = this.modelCapabilities.get(modelId);

        let score = 0;

        // Verificar se o modelo tem capacidades específicas para a tarefa
        if (taskAnalysis.taskType === 'chess_position_generation') {
            if (capabilities.includes('chess_expertise')) score += 0.5; // Aumentado de 0.4
            if (capabilities.includes('creative_positions')) score += 0.3;
            if (capabilities.includes('position_validation')) score += 0.4; // Aumentado de 0.3
        }

        if (taskAnalysis.taskType === 'complex_strategy_analysis') {
            if (capabilities.includes('reasoning')) score += 0.4;
            if (capabilities.includes('chess_expertise')) score += 0.3;
            if (capabilities.includes('strategic_planning')) score += 0.3;
        }

        if (taskAnalysis.taskType === 'mathematical_optimization') {
            if (capabilities.includes('mathematics')) score += 0.5;
            if (capabilities.includes('optimization')) score += 0.3;
            if (capabilities.includes('pattern_recognition')) score += 0.2;
        }

        return Math.min(score, 1.0);
    }

    async checkModelAvailability(modelId) {
        // Verificar se o modelo está disponível (rate limit, conectividade, etc.)
        try {
            const model = this.aiModels.get(modelId);

            // Simular verificação de disponibilidade
            if (model.provider === 'local') {
                return 1.0; // Sempre disponível
            }

            // Verificar rate limit e conectividade
            const availability = await this.checkProviderStatus(model.provider);
            return availability;

        } catch (error) {
            console.warn(`Modelo ${modelId} não disponível:`, error);
            return 0.0;
        }
    }

    calculateCostBenefitScore(modelId, taskAnalysis) {
        const model = this.aiModels.get(modelId);
        const performance = this.performanceMetrics.get(modelId);

        // Calcular custo-benefício baseado na complexidade da tarefa
        let costBenefit = 1.0;

        if (taskAnalysis.complexity === 'high' && performance.cost > 0.5) {
            costBenefit = 0.7; // Tarefas complexas podem justificar custo alto
        } else if (taskAnalysis.complexity === 'low' && performance.cost > 0.3) {
            costBenefit = 0.5; // Tarefas simples devem ser baratas
        }

        return costBenefit;
    }

    selectBestModel(scores) {
        // Selecionar modelo com melhor score
        const bestScore = scores[0];

        // Verificar se o score é aceitável
        if (bestScore.score < this.config.qualityThreshold) {
            console.warn(`🧠 Melhor score (${bestScore.score}) abaixo do threshold (${this.config.qualityThreshold})`);
        }

        return {
            modelId: bestScore.modelId,
            score: bestScore.score,
            breakdown: bestScore.breakdown,
            timestamp: Date.now()
        };
    }

    async executeTask(selectedModel, task, taskAnalysis) {
        const model = this.aiModels.get(selectedModel.modelId);
        console.log(`🧠 Executando tarefa com ${model.name}`);

        try {
            // Executar a tarefa usando a IA selecionada
            const result = await this.executeWithModel(selectedModel.modelId, task, taskAnalysis);
            
            // Validar resultado com Chess AI v2 se não for o próprio Chess AI v2
            if (selectedModel.modelId !== 'chess-ai-v2') {
                const validatedResult = await this.validatePosition(result, task);
                if (!validatedResult.isValid) {
                    throw new Error('Posição inválida segundo Chess AI v2');
                }
                result.validationScore = validatedResult.score;
            }

            // Registrar execução bem-sucedida
            this.recordSuccessfulExecution(selectedModel.modelId, taskAnalysis, result);

            return result;

        } catch (error) {
            console.error(`🧠 Erro na execução com ${model.name}:`, error);

            // Tentar fallback se configurado
            if (this.config.fallbackStrategy === 'intelligent') {
                return await this.executeFallback(task, taskAnalysis, selectedModel);
            }

            throw error;
        }
    }

    async executeWithModel(modelId, task, taskAnalysis) {
        // Implementar execução específica para cada modelo
        const model = this.aiModels.get(modelId);

        switch (model.provider) {
            case 'openai':
                return await this.executeWithOpenAI(modelId, task, taskAnalysis);
            case 'anthropic':
                return await this.executeWithAnthropic(modelId, task, taskAnalysis);
            case 'google':
                return await this.executeWithGoogle(modelId, task, taskAnalysis);
            case 'groq':
                return await this.executeWithGroq(modelId, task, taskAnalysis);
            case 'together':
                return await this.executeWithTogether(modelId, task, taskAnalysis);
            case 'chessai':
                return await this.executeWithChessAI(modelId, task, taskAnalysis);
            case 'local':
                return await this.executeWithLocalML(modelId, task, taskAnalysis);
            default:
                throw new Error(`Provedor não suportado: ${model.provider}`);
        }
    }

    async executeWithOpenAI(modelId, task, taskAnalysis) {
        // Implementar execução com OpenAI GPT-5
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'openai');

        // Aqui você faria a chamada real para a API OpenAI
        // Por enquanto, simulamos
        return await this.simulateExecution('openai', prompt, taskAnalysis);
    }

    async executeWithAnthropic(modelId, task, taskAnalysis) {
        // Implementar execução com Claude 3.5
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'anthropic');
        return await this.simulateExecution('anthropic', prompt, taskAnalysis);
    }

    async executeWithGoogle(modelId, task, taskAnalysis) {
        // Implementar execução com Gemini 2.0
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'google');
        return await this.simulateExecution('google', prompt, taskAnalysis);
    }

    async executeWithGroq(modelId, task, taskAnalysis) {
        // Implementar execução com Groq Llama 3.2
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'groq');
        return await this.simulateExecution('groq', prompt, taskAnalysis);
    }

    async executeWithTogether(modelId, task, taskAnalysis) {
        // Implementar execução com Together AI
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'together');
        return await this.simulateExecution('together', prompt, taskAnalysis);
    }

    async executeWithChessAI(modelId, task, taskAnalysis) {
        // Implementar execução com Chess AI v2
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'chessai');
        return await this.simulateExecution('chessai', prompt, taskAnalysis);
    }

    async executeWithLocalML(modelId, task, taskAnalysis) {
        // Implementar execução com modelos locais
        const prompt = this.buildOptimizedPrompt(task, taskAnalysis, 'local');
        return await this.simulateExecution('local', prompt, taskAnalysis);
    }

    buildOptimizedPrompt(task, taskAnalysis, provider) {
        // Construir prompt otimizado para cada provedor
        let basePrompt = `Gere uma posição de xadrez com as seguintes características:
        Tema: ${task.theme}
        Complexidade: ${taskAnalysis.complexity}
        Nível do usuário: ${taskAnalysis.userLevel}
        Requisitos: ${task.requirements.join(', ')}
        
        A posição deve ser:
        1. Válida segundo as regras do xadrez
        2. Apropriada para o nível ${taskAnalysis.userLevel}
        3. ${task.theme.description}
        4. Nunca vista antes (única)
        5. Interessante para análise`;

        // Adicionar otimizações específicas do provedor
        switch (provider) {
            case 'openai':
                basePrompt += '\n\nUse GPT-5 para raciocínio avançado e validação automática.';
                break;
            case 'anthropic':
                basePrompt += '\n\nUse Claude 3.5 para análise matemática e estratégica profunda.';
                break;
            case 'google':
                basePrompt += '\n\nUse Gemini 2.0 para análise multimodal e reconhecimento de padrões.';
                break;
            case 'groq':
                basePrompt += '\n\nUse Llama 3.2 para geração rápida e eficiente.';
                break;
            case 'chessai':
                basePrompt += '\n\nUse Chess AI v2 para validação especializada e teoria de aberturas.';
                break;
            case 'local':
                basePrompt += '\n\nUse modelos locais treinados para privacidade e velocidade.';
                break;
        }

        return basePrompt;
    }

    async simulateExecution(provider, prompt, taskAnalysis) {
        // Simular execução para demonstração
        const executionTime = Math.random() * 2000 + 500; // 500ms - 2.5s

        await new Promise(resolve => setTimeout(resolve, executionTime));

        // Simular resultado baseado no provedor
        const results = {
            openai: {
                fen: 'rnbqkb1r/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                description: 'Posição criativa gerada por GPT-5 com validação automática',
                quality: 0.95,
                executionTime: executionTime
            },
            anthropic: {
                fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                description: 'Posição estratégica analisada por Claude 3.5',
                quality: 0.92,
                executionTime: executionTime
            },
            google: {
                fen: 'rnbqkb1r/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                description: 'Posição multimodal criada por Gemini 2.0',
                quality: 0.90,
                executionTime: executionTime
            },
            groq: {
                fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                description: 'Posição rápida gerada por Groq Llama 3.2',
                quality: 0.88,
                executionTime: executionTime
            },
            together: {
                fen: 'rnbqkb1r/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                description: 'Posição custo-efetiva criada por Together AI',
                quality: 0.87,
                executionTime: executionTime
            },
            chessai: {
                fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                description: 'Posição validada por Chess AI v2',
                quality: 0.94,
                executionTime: executionTime
            },
            local: {
                fen: 'rnbqkb1r/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                description: 'Posição privada gerada por modelos locais',
                quality: 0.82,
                executionTime: executionTime
            }
        };

        return {
            ...results[provider],
            provider: provider,
            taskType: taskAnalysis.taskType,
            complexity: taskAnalysis.complexity
        };
    }

    async evaluateAndLearn(selectedModel, taskAnalysis, result) {
        // Avaliar performance e aprender com o resultado
        const evaluation = {
            modelId: selectedModel.modelId,
            taskType: taskAnalysis.taskType,
            complexity: taskAnalysis.complexity,
            quality: result.quality,
            executionTime: result.executionTime,
            timestamp: Date.now()
        };

        // Registrar avaliação
        this.performanceHistory.push(evaluation);

        // Treinar engine de aprendizado
        await this.learningEngine.train(evaluation);

        // Salvar dados de performance
        this.savePerformanceData();

        // Atualizar métricas do modelo
        this.updateModelMetrics(selectedModel.modelId, evaluation);

        console.log(`🧠 Aprendizado registrado: ${selectedModel.modelId} - Qualidade: ${result.quality}`);
    }

    unifyResult(result, selectedModel) {
        // Retornar resultado unificado - usuário não sabe qual IA foi usada
        return {
            success: true,
            data: {
                fen: result.fen,
                description: result.description,
                quality: result.quality,
                generatedAt: new Date().toISOString()
            },
            metadata: {
                executionTime: result.executionTime,
                complexity: result.complexity,
                // Não expor qual IA foi usada
                system: 'AEON Brain',
                version: this.version
            }
        };
    }

    async handleError(task, error) {
        console.error(`🧠 Erro na execução:`, error);

        // Tentar fallback automático
        try {
            const fallbackResult = await this.executeFallback(task, {
                complexity: 'low'
            }, null);
            return this.unifyResult(fallbackResult, {
                modelId: 'fallback'
            });
        } catch (fallbackError) {
            console.error(`🧠 Fallback também falhou:`, fallbackError);

            // Retornar erro genérico para o usuário
            return {
                success: false,
                error: 'Erro interno do sistema. Tente novamente.',
                metadata: {
                    system: 'AEON Brain',
                    timestamp: new Date().toISOString()
                }
            };
        }
    }

    async executeFallback(task, taskAnalysis, originalModel) {
        console.log(`🧠 Executando fallback...`);

        // Se o erro não foi do Chess AI v2, tentar primeiro com ele
        if (originalModel?.modelId !== 'chess-ai-v2') {
            try {
                console.log(`🧠 Tentando fallback com Chess AI v2...`);
                const result = await this.executeWithChessAI('chess-ai-v2', task, taskAnalysis);
                result.fallbackType = 'chess-ai';
                return result;
            } catch (error) {
                console.warn(`🧠 Fallback com Chess AI v2 falhou:`, error);
            }
        }

        // Se Chess AI v2 falhar ou não estiver disponível, usar modelo local
        console.log(`🧠 Usando modelo local como último fallback...`);
        const result = await this.executeWithLocalML('local-ml', task, taskAnalysis);
        result.fallbackType = 'local';
        return result;
    }

    async validatePosition(position, task) {
        console.log(`🧠 Validando posição com Chess AI v2...`);
        
        try {
            const validationResult = await this.executeWithChessAI('chess-ai-v2', {
                type: 'validate_position',
                position: position.fen,
                requirements: task.requirements
            }, {
                taskType: 'position_validation',
                complexity: 'low'
            });

            // Considerar válido se score de validação > 0.9
            const isValid = validationResult.quality > 0.9;
            
            console.log(`🧠 Validação completada: ${isValid ? 'Válida' : 'Inválida'} (score: ${validationResult.quality})`);
            
            return {
                isValid,
                score: validationResult.quality,
                details: validationResult.description
            };

        } catch (error) {
            console.error(`🧠 Erro na validação:`, error);
            // Em caso de erro na validação, assumir válido para não bloquear
            return {
                isValid: true,
                score: 0.8,
                details: 'Erro na validação, assumindo válido'
            };
        }
    }

    // Métodos auxiliares
    generateCacheKey(taskAnalysis) {
        return `${taskAnalysis.taskType}_${taskAnalysis.complexity}_${taskAnalysis.userLevel}`;
    }

    isDecisionValid(decision) {
        const maxAge = 5 * 60 * 1000; // 5 minutos
        return (Date.now() - decision.timestamp) < maxAge;
    }

    recordSuccessfulExecution(modelId, taskAnalysis, result) {
        this.decisionHistory.push({
            modelId,
            taskType: taskAnalysis.taskType,
            complexity: taskAnalysis.complexity,
            success: true,
            timestamp: Date.now()
        });
    }

    updateModelMetrics(modelId, evaluation) {
        const metrics = this.performanceMetrics.get(modelId);
        if (metrics) {
            // Atualizar métricas com média móvel
            metrics.accuracy = (metrics.accuracy * 0.9) + (evaluation.quality * 0.1);
            metrics.speed = (metrics.speed * 0.9) + ((1000 / evaluation.executionTime) * 0.1);
        }
    }

    savePerformanceData() {
        localStorage.setItem('aeonBrainPerformance', JSON.stringify(this.performanceHistory));
    }

    // Métodos públicos para controle e monitoramento
    async getSystemStatus() {
        return {
            name: this.name,
            version: this.version,
            modelsAvailable: this.aiModels.size,
            autoSelection: this.config.autoSelection,
            learningEnabled: this.config.learningEnabled,
            performanceHistory: this.performanceHistory.length,
            decisionCache: this.decisionCache.size
        };
    }

    async getModelPerformance() {
        const performance = {};
        for (const [modelId, metrics] of this.performanceMetrics) {
            performance[modelId] = {
                ...metrics,
                recentEvaluations: this.performanceHistory
                    .filter(e => e.modelId === modelId)
                    .slice(-10)
            };
        }
        return performance;
    }

    async updateConfiguration(newConfig) {
        this.config = {
            ...this.config,
            ...newConfig
        };
        console.log(`🧠 Configuração atualizada:`, this.config);
    }

    async clearCache() {
        this.decisionCache.clear();
        console.log(`🧠 Cache limpo`);
    }

    async resetLearning() {
        await this.learningEngine.reset();
        this.performanceHistory = [];
        this.decisionHistory = [];
        this.savePerformanceData();
        console.log(`🧠 Aprendizado resetado`);
    }
}

// Engine de Aprendizado
class LearningEngine {
    constructor() {
        this.learningRate = 0.02; // Aumentado de 0.01
        this.trainingData = [];
        this.model = null;
        this.validationThreshold = 0.90; // Novo threshold para validação
        this.batchSize = 5; // Treinar a cada 5 amostras em vez de 10
    }

    async initialize() {
        // Inicializar modelo de aprendizado
        console.log('🧠 Engine de aprendizado inicializando...');

        // Em produção, isso seria um modelo real de ML
        this.model = {
            type: 'reinforcement_learning',
            status: 'ready',
            accuracy: 0.75
        };
    }

    async train(evaluation) {
        // Treinar modelo com nova avaliação
        this.trainingData.push(evaluation);

        // Treinar mais frequentemente (a cada 5 amostras)
        if (this.trainingData.length % this.batchSize === 0) {
            await this.retrainModel();
        }

        // Se a qualidade estiver abaixo do threshold, treinar imediatamente
        if (evaluation.quality < this.validationThreshold) {
            console.log(`🧠 Qualidade abaixo do threshold (${evaluation.quality} < ${this.validationThreshold}), treinando imediatamente...`);
            await this.retrainModel();
        }
    }

    async retrainModel() {
        console.log('🧠 Retreinando modelo de aprendizado...');

        // Simular retreinamento com batch processing
        await new Promise(resolve => setTimeout(resolve, 500)); // Reduzido de 1000ms

        if (this.model) {
            // Calcular média móvel dos últimos resultados
            const recentResults = this.trainingData.slice(-this.batchSize);
            const averageQuality = recentResults.reduce((acc, curr) => acc + curr.quality, 0) / recentResults.length;

            // Ajustar accuracy com base na média recente
            const delta = (averageQuality - this.model.accuracy) * this.learningRate;
            this.model.accuracy += delta;
            this.model.accuracy = Math.min(Math.max(this.model.accuracy, 0.5), 1.0); // Limitar entre 0.5 e 1.0
        }

        console.log(`🧠 Modelo retreinado. Nova precisão: ${this.model?.accuracy.toFixed(3)}`);
    }

    async reset() {
        this.trainingData = [];
        this.model = null;
        await this.initialize();
    }
}

// Analisador de Tarefas
class TaskAnalyzer {
    async analyze(task, userProfile, preferences) {
        return {
            taskType: this.determineTaskType(task),
            complexity: this.assessComplexity(task, userProfile),
            urgency: this.assessUrgency(preferences),
            costSensitivity: this.assessCostSensitivity(preferences),
            qualityRequirement: this.assessQualityRequirement(task, userProfile),
            userLevel: userProfile.level || 'intermediate'
        };
    }

    determineTaskType(task) {
        if (task.theme === 'artistic') return 'creative_generation';
        if (task.complexity === 'high') return 'complex_strategy_analysis';
        if (task.requirements.includes('mathematical')) return 'mathematical_optimization';
        return 'chess_position_generation';
    }

    assessComplexity(task, userProfile) {
        const baseComplexity = task.complexity || 'medium';
        const userLevel = userProfile.level || 'intermediate';

        // Ajustar complexidade baseado no nível do usuário
        if (userLevel === 'beginner' && baseComplexity === 'high') return 'medium';
        if (userLevel === 'expert' && baseComplexity === 'low') return 'medium';

        return baseComplexity;
    }

    assessUrgency(preferences) {
        return preferences.urgency || 'normal';
    }

    assessCostSensitivity(preferences) {
        return preferences.costSensitive || false;
    }

    assessQualityRequirement(task, userProfile) {
        const baseQuality = 0.8;

        if (task.complexity === 'high') return baseQuality + 0.1;
        if (userProfile.level === 'expert') return baseQuality + 0.1;
        if (task.requirements.includes('high_quality')) return baseQuality + 0.15;

        return baseQuality;
    }
}

// Otimizador de Custos
class CostOptimizer {
    constructor() {
        this.costThresholds = {
            low: 0.2,
            medium: 0.5,
            high: 0.8
        };
    }

    optimizeForCost(taskAnalysis, availableModels) {
        if (!taskAnalysis.costSensitivity) return availableModels;

        const threshold = this.costThresholds[taskAnalysis.complexity] || 0.5;

        return availableModels.filter(model => {
            const performance = this.getModelPerformance(model.modelId);
            return performance.cost <= threshold;
        });
    }

    getModelPerformance(modelId) {
        // Retornar performance do modelo
        return {
            cost: 0.3,
            accuracy: 0.9,
            speed: 0.8
        };
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
            window.aeonBrain = new AEONBrainOrchestrator();
            console.log('🧠 AEON Brain disponível globalmente como window.aeonBrain');