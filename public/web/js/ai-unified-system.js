/**
 * 🧠 Sistema de IA Unificado - Aeon Chess
 * 
 * Este sistema integra todas as funcionalidades de IA:
 * - IA Professor para análise e ensino
 * - IA Generativa para criação de tabuleiros
 * - Sistema de personalidades de IA avançado
 * - Orquestração inteligente
 * 
 * @version 2.1.0
 * @author Aeon Chess Team
 */

class AIUnifiedSystem {
    constructor() {
        this.personalities = new Map();
        this.activePersonality = null;
        this.teacherMode = false;
        this.generativeMode = false;
        this.orchestrationEnabled = true;
        this.orchestrator = null;
        
        this.initializePersonalities();
        this.initializeEventListeners();
        this.loadUserPreferences();
        
        // Inicializa orquestrador após carregar preferências
        this.initializeOrchestrator();
        
        console.log('🧠 Sistema de IA Unificado inicializado');
    }

    /**
     * Inicializa o orquestrador
     */
    initializeOrchestrator() {
        if (this.orchestrationEnabled) {
            // Aguarda o carregamento do orquestrador
            const checkOrchestrator = setInterval(() => {
                if (window.AIOrchestrator) {
                    clearInterval(checkOrchestrator);
                    this.orchestrator = new window.AIOrchestrator(this);
                    console.log('🎼 Orquestrador integrado ao sistema de IA');
                }
            }, 100);
        }
    }

    /**
     * Inicializa as personalidades de IA disponíveis
     */
    initializePersonalities() {
        // Personalidade: Mestre Estratégico
        this.personalities.set('strategic', {
            name: 'Mestre Estratégico',
            description: 'Foca em planos de longo prazo e estruturas posicionais',
            style: 'strategic',
            difficulty: 'advanced',
            voice: 'calm',
            analysisDepth: 8,
            teachingStyle: 'methodical',
            color: '#2E8B57',
            // Características avançadas
            strengths: ['Visão estratégica', 'Planejamento longo prazo', 'Estrutura de peões', 'Coordenação de peças'],
            weaknesses: ['Pode ser lento', 'Menos tático', 'Rigidez posicional'],
            preferredOpenings: ['Sistema Colle', 'Defesa Francesa', 'Gambito da Dama'],
            endgameSpecialty: 'Finais de torre e peão',
            timeManagement: 'conservative',
            riskTolerance: 'low',
            communicationStyle: 'analytical',
            motivationalQuotes: [
                'A estratégia é a arte de fazer o plano antes da batalha.',
                'O controle do centro é a base de toda estratégia sólida.',
                'Peões são a alma do xadrez.'
            ],
            analysisFocus: ['estrutura', 'controle_centro', 'desenvolvimento', 'coordenação'],
            learningPath: ['fundamentos_posicionais', 'estrutura_peoes', 'planos_estrategicos', 'finais_posicionais']
        });

        // Personalidade: Tático Agressivo
        this.personalities.set('tactical', {
            name: 'Tático Agressivo',
            description: 'Especialista em combinações, sacrifícios e ataques',
            style: 'tactical',
            difficulty: 'intermediate',
            voice: 'energetic',
            analysisDepth: 6,
            teachingStyle: 'dynamic',
            color: '#DC143C',
            // Características avançadas
            strengths: ['Visão tática', 'Cálculo rápido', 'Sacrifícios', 'Ataques'],
            weaknesses: ['Pode ser impulsivo', 'Menos posicional', 'Risco excessivo'],
            preferredOpenings: ['Gambito do Rei', 'Defesa Siciliana', 'Ataque Indiano'],
            endgameSpecialty: 'Finais de combinação',
            timeManagement: 'aggressive',
            riskTolerance: 'high',
            communicationStyle: 'passionate',
            motivationalQuotes: [
                'A melhor defesa é o ataque!',
                'Sacrifícios são a alma da tática.',
                'Encontre a combinação que seu oponente não vê.'
            ],
            analysisFocus: ['combinações', 'sacrifícios', 'ataques', 'táticas'],
            learningPath: ['taticas_basicas', 'sacrifícios', 'combinações', 'ataques']
        });

        // Personalidade: Professor Paciente
        this.personalities.set('teacher', {
            name: 'Professor Paciente',
            description: 'Foca no aprendizado progressivo e explicações detalhadas',
            style: 'educational',
            difficulty: 'beginner',
            voice: 'gentle',
            analysisDepth: 4,
            teachingStyle: 'explanatory',
            color: '#4169E1',
            // Características avançadas
            strengths: ['Didática', 'Paciência', 'Explicações claras', 'Progressão gradual'],
            weaknesses: ['Pode ser lento', 'Menos competitivo', 'Foco excessivo em teoria'],
            preferredOpenings: ['Abertura Italiana', 'Defesa Escocesa', 'Gambito Evans'],
            endgameSpecialty: 'Finais básicos',
            timeManagement: 'balanced',
            riskTolerance: 'medium',
            communicationStyle: 'encouraging',
            motivationalQuotes: [
                'Cada erro é uma oportunidade de aprendizado.',
                'O xadrez é uma jornada, não uma corrida.',
                'A paciência é a virtude do verdadeiro mestre.'
            ],
            analysisFocus: ['fundamentos', 'regras', 'desenvolvimento', 'segurança'],
            learningPath: ['regras_basicas', 'desenvolvimento', 'taticas_simples', 'finais_basicos']
        });

        // Personalidade: Artista Criativo
        this.personalities.set('creative', {
            name: 'Artista Criativo',
            description: 'Cria posições únicas e artisticamente interessantes',
            style: 'artistic',
            difficulty: 'varied',
            voice: 'inspirational',
            analysisDepth: 5,
            teachingStyle: 'creative',
            color: '#9932CC',
            // Características avançadas
            strengths: ['Criatividade', 'Originalidade', 'Visão artística', 'Flexibilidade'],
            weaknesses: ['Pode ser imprevisível', 'Menos sistemático', 'Risco criativo'],
            preferredOpenings: ['Abertura Bird', 'Defesa Benoni', 'Gambito Budapest'],
            endgameSpecialty: 'Finais artísticos',
            timeManagement: 'creative',
            riskTolerance: 'high',
            communicationStyle: 'inspirational',
            motivationalQuotes: [
                'A beleza está na originalidade do pensamento.',
                'Quebre as regras convencionais para criar algo único.',
                'A arte do xadrez está na expressão da criatividade.'
            ],
            analysisFocus: ['criatividade', 'originalidade', 'expressão', 'beleza'],
            learningPath: ['criatividade', 'aberturas_estranhas', 'posições_unicas', 'arte_xadrez']
        });

        // Personalidade: Competidor Feroz
        this.personalities.set('competitive', {
            name: 'Competidor Feroz',
            description: 'Joga para vencer, sem piedade, focado em resultados',
            style: 'aggressive',
            difficulty: 'expert',
            voice: 'determined',
            analysisDepth: 10,
            teachingStyle: 'challenging',
            color: '#8B0000',
            // Características avançadas
            strengths: ['Determinação', 'Foco no resultado', 'Análise profunda', 'Competitividade'],
            weaknesses: ['Pode ser impiedoso', 'Menos didático', 'Pressão excessiva'],
            preferredOpenings: ['Defesa Grünfeld', 'Abertura Inglesa', 'Defesa Nimzo-Índia'],
            endgameSpecialty: 'Finais técnicos complexos',
            timeManagement: 'aggressive',
            riskTolerance: 'calculated',
            communicationStyle: 'direct',
            motivationalQuotes: [
                'A vitória não é tudo, é a única coisa.',
                'Cada movimento deve ter um propósito.',
                'A pressão faz diamantes, e campeões.'
            ],
            analysisFocus: ['vantagem', 'pressão', 'precisão', 'resultado'],
            learningPath: ['aberturas_avancadas', 'meio_jogo_agressivo', 'finais_tecnicos', 'psicologia']
        });

        // Personalidade: Sábio Zen
        this.personalities.set('zen', {
            name: 'Sábio Zen',
            description: 'Equilibra estratégia e filosofia, foca na harmonia do jogo',
            style: 'balanced',
            difficulty: 'advanced',
            voice: 'contemplative',
            analysisDepth: 7,
            teachingStyle: 'philosophical',
            color: '#228B22',
            // Características avançadas
            strengths: ['Equilíbrio', 'Sabedoria', 'Visão filosófica', 'Harmonia'],
            weaknesses: ['Pode ser abstrato', 'Menos prático', 'Foco excessivo na filosofia'],
            preferredOpenings: ['Abertura Reti', 'Defesa Caro-Kann', 'Abertura Réti'],
            endgameSpecialty: 'Finais equilibrados',
            timeManagement: 'balanced',
            riskTolerance: 'low',
            communicationStyle: 'contemplative',
            motivationalQuotes: [
                'A harmonia está no equilíbrio entre ataque e defesa.',
                'O verdadeiro mestre vê a beleza em todas as posições.',
                'A sabedoria do xadrez está na compreensão da unidade.'
            ],
            analysisFocus: ['equilibrio', 'harmonia', 'sabedoria', 'unidade'],
            learningPath: ['filosofia_xadrez', 'equilibrio_posicional', 'harmonia_estrategica', 'sabedoria_jogo']
        });

        // Personalidade: Inovador Tecnológico
        this.personalities.set('innovator', {
            name: 'Inovador Tecnológico',
            description: 'Combina IA moderna com análise tradicional, sempre na vanguarda',
            style: 'innovative',
            difficulty: 'expert',
            voice: 'futuristic',
            analysisDepth: 12,
            teachingStyle: 'cutting_edge',
            color: '#00CED1',
            // Características avançadas
            strengths: ['Tecnologia avançada', 'Análise profunda', 'Inovação', 'Precisão'],
            weaknesses: ['Pode ser complexo', 'Menos humano', 'Dependência tecnológica'],
            preferredOpenings: ['Defesa Moderna', 'Abertura Trompowsky', 'Defesa Pirc'],
            endgameSpecialty: 'Finais com IA',
            timeManagement: 'precise',
            riskTolerance: 'calculated',
            communicationStyle: 'technical',
            motivationalQuotes: [
                'O futuro do xadrez está na fusão de mente e máquina.',
                'A inovação é a chave para o progresso.',
                'Cada análise deve quebrar os limites do possível.'
            ],
            analysisFocus: ['tecnologia', 'inovacao', 'precisao', 'futuro'],
            learningPath: ['ia_avancada', 'analise_profunda', 'tecnologia_xadrez', 'futuro_jogo']
        });

        // Personalidade: Mentor Inspirador
        this.personalities.set('mentor', {
            name: 'Mentor Inspirador',
            description: 'Foca no desenvolvimento pessoal e crescimento do jogador',
            style: 'mentoring',
            difficulty: 'intermediate',
            voice: 'encouraging',
            analysisDepth: 6,
            teachingStyle: 'transformative',
            color: '#FF8C00',
            // Características avançadas
            strengths: ['Mentoria', 'Desenvolvimento pessoal', 'Motivação', 'Crescimento'],
            weaknesses: ['Pode ser subjetivo', 'Menos técnico', 'Foco excessivo no indivíduo'],
            preferredOpenings: ['Abertura Larsen', 'Defesa Holandesa', 'Gambito Blackmar-Diemer'],
            endgameSpecialty: 'Finais de desenvolvimento',
            timeManagement: 'adaptive',
            riskTolerance: 'medium',
            communicationStyle: 'transformative',
            motivationalQuotes: [
                'O maior adversário que você enfrenta é você mesmo.',
                'Cada derrota é uma lição disfarçada de vitória.',
                'O crescimento vem da coragem de enfrentar seus medos.'
            ],
            analysisFocus: ['crescimento', 'desenvolvimento', 'motivacao', 'transformacao'],
            learningPath: ['desenvolvimento_pessoal', 'psicologia_xadrez', 'crescimento_mental', 'transformacao_jogo']
        });

        this.activePersonality = this.personalities.get('teacher');
    }

    /**
     * Inicializa os event listeners do sistema
     */
    initializeEventListeners() {
        // Eventos de mudança de personalidade
        document.addEventListener('personalityChanged', (e) => {
            this.changePersonality(e.detail.personality);
        });

        // Eventos de análise de tabuleiro
        document.addEventListener('boardAnalysisRequested', (e) => {
            this.analyzeBoard(e.detail.fen, e.detail.depth);
        });

        // Eventos de geração de tabuleiro
        document.addEventListener('boardGenerationRequested', (e) => {
            this.generateBoard(e.detail.theme, e.detail.complexity);
        });

        // Eventos de ensino
        document.addEventListener('teachingRequested', (e) => {
            this.startTeaching(e.detail.topic, e.detail.level);
        });
    }

    /**
     * Carrega as preferências do usuário
     */
    loadUserPreferences() {
        try {
            const preferences = localStorage.getItem('aiPreferences');
            if (preferences) {
                const prefs = JSON.parse(preferences);
                this.activePersonality = this.personalities.get(prefs.personality) || this.activePersonality;
                this.teacherMode = prefs.teacherMode || false;
                this.generativeMode = prefs.generativeMode || false;
                this.orchestrationEnabled = prefs.orchestrationEnabled !== false;
            }
        } catch (error) {
            console.warn('Erro ao carregar preferências de IA:', error);
        }
    }

    /**
     * Salva as preferências do usuário
     */
    saveUserPreferences() {
        try {
            const preferences = {
                personality: this.activePersonality.style,
                teacherMode: this.teacherMode,
                generativeMode: this.generativeMode,
                orchestrationEnabled: this.orchestrationEnabled
            };
            localStorage.setItem('aiPreferences', JSON.stringify(preferences));
        } catch (error) {
            console.warn('Erro ao salvar preferências de IA:', error);
        }
    }

    /**
     * Muda a personalidade ativa
     */
    changePersonality(personalityKey) {
        const personality = this.personalities.get(personalityKey);
        if (personality) {
            this.activePersonality = personality;
            this.saveUserPreferences();
            this.updateUI();
            this.notifyPersonalityChange();
            
            console.log(`🧠 Personalidade alterada para: ${personality.name}`);
        }
    }

    /**
     * Atualiza a interface com a personalidade ativa
     */
    updateUI() {
        // Atualiza indicador de personalidade
        const indicator = document.getElementById('ai-personality-indicator');
        if (indicator) {
            indicator.textContent = this.activePersonality.name;
            indicator.style.color = this.activePersonality.color;
        }

        // Atualiza descrição
        const description = document.getElementById('ai-personality-description');
        if (description) {
            description.textContent = this.activePersonality.description;
        }

        // Atualiza estilo visual
        this.updateVisualStyle();
    }

    /**
     * Atualiza o estilo visual baseado na personalidade
     */
    updateVisualStyle() {
        const root = document.documentElement;
        root.style.setProperty('--ai-primary-color', this.activePersonality.color);
        
        // Aplica tema de cores baseado na personalidade
        const theme = this.getPersonalityTheme();
        root.style.setProperty('--ai-theme-bg', theme.background);
        root.style.setProperty('--ai-theme-text', theme.text);
        root.style.setProperty('--ai-theme-accent', theme.accent);
    }

    /**
     * Obtém o tema visual da personalidade
     */
    getPersonalityTheme() {
        const themes = {
            strategic: {
                background: '#f8f9fa',
                text: '#2E8B57',
                accent: '#20B2AA'
            },
            tactical: {
                background: '#fff5f5',
                text: '#DC143C',
                accent: '#FF6347'
            },
            educational: {
                background: '#f0f8ff',
                text: '#4169E1',
                accent: '#87CEEB'
            },
            artistic: {
                background: '#fdf8ff',
                text: '#9932CC',
                accent: '#DDA0DD'
            },
            aggressive: {
                background: '#fff0f0',
                text: '#8B0000',
                accent: '#CD5C5C'
            },
            balanced: {
                background: '#f0fff0',
                text: '#228B22',
                accent: '#90EE90'
            },
            innovative: {
                background: '#f0ffff',
                text: '#00CED1',
                accent: '#40E0D0'
            },
            mentoring: {
                background: '#fff8f0',
                text: '#FF8C00',
                accent: '#FFA500'
            }
        };

        return themes[this.activePersonality.style] || themes.educational;
    }

    /**
     * Notifica mudança de personalidade
     */
    notifyPersonalityChange() {
        const event = new CustomEvent('aiPersonalityChanged', {
            detail: {
                personality: this.activePersonality,
                previousPersonality: this.activePersonality
            }
        });
        document.dispatchEvent(event);
    }

    /**
     * Analisa um tabuleiro usando a personalidade ativa
     */
    async analyzeBoard(fen, depth = null) {
        const analysisDepth = depth || this.activePersonality.analysisDepth;
        
        console.log(`🧠 Analisando tabuleiro com ${this.activePersonality.name} (profundidade: ${analysisDepth})`);

        try {
            // Usa orquestrador se disponível
            if (this.orchestrator && this.orchestrationEnabled) {
                return await this.orchestrator.orchestrateTask('analysis', {
                    fen: fen,
                    depth: analysisDepth
                });
            } else {
                // Execução direta sem orquestração
                const analysis = await this.performAnalysis(fen, analysisDepth);
                const personalizedAnalysis = this.personalizeAnalysis(analysis);
                this.dispatchAnalysisResult(personalizedAnalysis);
                return personalizedAnalysis;
            }
        } catch (error) {
            console.error('Erro na análise:', error);
            throw error;
        }
    }

    /**
     * Gera um novo tabuleiro baseado no tema e complexidade
     */
    async generateBoard(theme, complexity = 'medium') {
        console.log(`🧠 Gerando tabuleiro ${theme} com ${this.activePersonality.name}`);

        try {
            // Usa orquestrador se disponível
            if (this.orchestrator && this.orchestrationEnabled) {
                return await this.orchestrator.orchestrateTask('generation', {
                    theme: theme,
                    complexity: complexity
                });
            } else {
                // Execução direta sem orquestração
                const board = await this.generatePosition(theme, complexity);
                const personalizedBoard = this.personalizeBoard(board);
                this.dispatchBoardGenerated(personalizedBoard);
                return personalizedBoard;
            }
        } catch (error) {
            console.error('Erro na geração:', error);
            throw error;
        }
    }

    /**
     * Inicia sessão de ensino
     */
    async startTeaching(topic, level = 'beginner') {
        console.log(`🧠 Iniciando ensino com ${this.activePersonality.name}`);

        try {
            // Usa orquestrador se disponível
            if (this.orchestrator && this.orchestrationEnabled) {
                return await this.orchestrator.orchestrateTask('teaching', {
                    topic: topic,
                    level: level
                });
            } else {
                // Execução direta sem orquestração
                const lessonPlan = this.createLessonPlan(topic, level);
                const session = await this.beginTeachingSession(lessonPlan);
                this.dispatchTeachingStarted(session);
                return session;
            }
        } catch (error) {
            console.error('Erro no ensino:', error);
            throw error;
        }
    }

    /**
     * Realiza análise técnica do tabuleiro
     */
    async performAnalysis(fen, depth) {
        // Simula análise da IA (em produção, seria integrado com Stockfish ou similar)
        return new Promise((resolve) => {
            setTimeout(() => {
                const analysis = {
                    evaluation: this.calculateEvaluation(fen),
                    bestMoves: this.findBestMoves(fen, depth),
                    plan: this.generatePlan(fen),
                    threats: this.identifyThreats(fen),
                    opportunities: this.identifyOpportunities(fen),
                    depth: depth,
                    timestamp: Date.now()
                };
                resolve(analysis);
            }, 1000 + (depth * 200)); // Tempo baseado na profundidade
        });
    }

    /**
     * Gera posição de tabuleiro
     */
    async generatePosition(theme, complexity) {
        // Simula geração de posição (em produção, seria integrado com IA generativa)
        return new Promise((resolve) => {
            setTimeout(() => {
                const board = {
                    fen: this.generateFEN(theme, complexity),
                    theme: theme,
                    complexity: complexity,
                    description: this.generateDescription(theme, complexity),
                    difficulty: this.calculateDifficulty(complexity),
                    timestamp: Date.now()
                };
                resolve(board);
            }, 500);
        });
    }

    /**
     * Inicia sessão de ensino
     */
    async beginTeachingSession(lessonPlan) {
        // Simula início de sessão
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(lessonPlan);
            }, 300);
        });
    }

    /**
     * Cria plano de aula personalizado
     */
    createLessonPlan(topic, level) {
        const plans = {
            strategic: {
                beginner: ['Conceitos básicos de estratégia', 'Controle do centro', 'Desenvolvimento de peças'],
                intermediate: ['Estrutura de peões', 'Planejamento de longo prazo', 'Coordenação de peças'],
                advanced: ['Estratégia posicional', 'Timing', 'Compensação material']
            },
            tactical: {
                beginner: ['Táticas básicas', 'Garfos', 'Pinos'],
                intermediate: ['Sacrifícios', 'Combinações', 'Temas táticos'],
                advanced: ['Táticas complexas', 'Cálculo', 'Visão tática']
            },
            educational: {
                beginner: ['Regras básicas', 'Movimento das peças', 'Xeque e xeque-mate'],
                intermediate: ['Aberturas básicas', 'Meio-jogo', 'Final básico'],
                advanced: ['Teoria de aberturas', 'Estratégia avançada', 'Finais complexos']
            }
        };

        const style = this.activePersonality.style;
        const availablePlans = plans[style] || plans.educational;
        const plan = availablePlans[level] || availablePlans.beginner;

        return {
            topic: topic,
            level: level,
            style: style,
            lessons: plan,
            personality: this.activePersonality.name,
            estimatedDuration: this.estimateDuration(level, plan.length)
        };
    }

    /**
     * Personaliza análise baseada na personalidade
     */
    personalizeAnalysis(analysis) {
        const personality = this.activePersonality;
        
        // Aplica estilo da personalidade
        switch (personality.style) {
            case 'strategic':
                analysis.focus = 'Estratégia de longo prazo';
                analysis.recommendations = this.addStrategicAdvice(analysis);
                break;
            case 'tactical':
                analysis.focus = 'Combinações táticas';
                analysis.recommendations = this.addTacticalAdvice(analysis);
                break;
            case 'educational':
                analysis.focus = 'Aprendizado e compreensão';
                analysis.recommendations = this.addEducationalAdvice(analysis);
                break;
            case 'artistic':
                analysis.focus = 'Possibilidades criativas';
                analysis.recommendations = this.addCreativeAdvice(analysis);
                break;
            case 'aggressive':
                analysis.focus = 'Vantagem competitiva';
                analysis.recommendations = this.addCompetitiveAdvice(analysis);
                break;
            case 'balanced':
                analysis.focus = 'Equilíbrio e harmonia';
                analysis.recommendations = this.addZenAdvice(analysis);
                break;
            case 'innovative':
                analysis.focus = 'Inovação e tecnologia';
                analysis.recommendations = this.addInnovativeAdvice(analysis);
                break;
            case 'mentoring':
                analysis.focus = 'Desenvolvimento pessoal';
                analysis.recommendations = this.addMentoringAdvice(analysis);
                break;
        }

        analysis.personality = personality.name;
        analysis.style = personality.style;
        
        return analysis;
    }

    /**
     * Personaliza tabuleiro gerado
     */
    personalizeBoard(board) {
        const personality = this.activePersonality;
        
        // Aplica características da personalidade
        board.personality = personality.name;
        board.style = personality.style;
        board.characteristics = this.getPersonalityCharacteristics();
        
        return board;
    }

    /**
     * Obtém características da personalidade
     */
    getPersonalityCharacteristics() {
        return this.activePersonality.strengths || ['Característica padrão'];
    }

    /**
     * Obtém fraquezas da personalidade
     */
    getPersonalityWeaknesses() {
        return this.activePersonality.weaknesses || ['Sem fraquezas identificadas'];
    }

    /**
     * Obtém aberturas preferidas da personalidade
     */
    getPersonalityOpenings() {
        return this.activePersonality.preferredOpenings || ['Aberturas padrão'];
    }

    /**
     * Obtém especialidade em finais da personalidade
     */
    getPersonalityEndgameSpecialty() {
        return this.activePersonality.endgameSpecialty || 'Finais gerais';
    }

    /**
     * Obtém citações motivacionais da personalidade
     */
    getPersonalityQuotes() {
        return this.activePersonality.motivationalQuotes || ['Sem citações disponíveis'];
    }

    /**
     * Obtém foco de análise da personalidade
     */
    getPersonalityAnalysisFocus() {
        return this.activePersonality.analysisFocus || ['Análise geral'];
    }

    /**
     * Obtém caminho de aprendizado da personalidade
     */
    getPersonalityLearningPath() {
        return this.activePersonality.learningPath || ['Aprendizado geral'];
    }

    /**
     * Obtém estilo de comunicação da personalidade
     */
    getPersonalityCommunicationStyle() {
        return this.activePersonality.communicationStyle || 'padrão';
    }

    /**
     * Obtém tolerância ao risco da personalidade
     */
    getPersonalityRiskTolerance() {
        return this.activePersonality.riskTolerance || 'médio';
    }

    /**
     * Obtém gerenciamento de tempo da personalidade
     */
    getPersonalityTimeManagement() {
        return this.activePersonality.timeManagement || 'equilibrado';
    }

    // Métodos auxiliares para simulação
    calculateEvaluation(fen) { return Math.random() * 2 - 1; }
    findBestMoves(fen, depth) { return ['e4', 'd4', 'Nf3']; }
    generatePlan(fen) { return 'Desenvolver peças e controlar o centro'; }
    identifyThreats(fen) { return ['Xeque em 2', 'Perda de peça']; }
    identifyOpportunities(fen) { return ['Desenvolvimento', 'Controle do centro']; }
    generateFEN(theme, complexity) { return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'; }
    generateDescription(theme, complexity) { return `Posição ${theme} de complexidade ${complexity}`; }
    calculateDifficulty(complexity) { return complexity === 'hard' ? 8 : complexity === 'medium' ? 5 : 3; }
    estimateDuration(level, lessons) { return level === 'beginner' ? lessons * 10 : lessons * 15; }

    // Métodos de conselhos personalizados
    addStrategicAdvice(analysis) { return ['Foque no controle do centro', 'Desenvolva suas peças']; }
    addTacticalAdvice(analysis) { return ['Procure combinações', 'Identifique sacrifícios']; }
    addEducationalAdvice(analysis) { return ['Entenda a posição', 'Aprenda com cada movimento']; }
    addCreativeAdvice(analysis) { return ['Explore possibilidades únicas', 'Pense fora da caixa']; }
    addCompetitiveAdvice(analysis) { return ['Maximize suas chances', 'Jogue para vencer']; }
    addZenAdvice(analysis) { return ['Mantenha o equilíbrio', 'Harmonize suas peças']; }
    addInnovativeAdvice(analysis) { return ['Use tecnologia avançada', 'Quebre paradigmas']; }
    addMentoringAdvice(analysis) { return ['Cresça como jogador', 'Desenvolva sua mente']; }

    // Métodos de dispatch de eventos
    dispatchAnalysisResult(analysis) {
        const event = new CustomEvent('aiAnalysisComplete', { detail: analysis });
        document.dispatchEvent(event);
    }

    dispatchBoardGenerated(board) {
        const event = new CustomEvent('aiBoardGenerated', { detail: board });
        document.dispatchEvent(event);
    }

    dispatchTeachingStarted(session) {
        const event = new CustomEvent('aiTeachingStarted', { detail: session });
        document.dispatchEvent(event);
    }

    /**
     * Obtém estatísticas do sistema
     */
    getStats() {
        const baseStats = {
            activePersonality: this.activePersonality.name,
            totalPersonalities: this.personalities.size,
            teacherMode: this.teacherMode,
            generativeMode: this.generativeMode,
            orchestrationEnabled: this.orchestrationEnabled,
            timestamp: Date.now()
        };

        // Adiciona estatísticas do orquestrador se disponível
        if (this.orchestrator) {
            const orchestratorStats = this.orchestrator.getOrchestratorStats();
            return { ...baseStats, orchestrator: orchestratorStats };
        }

        return baseStats;
    }

    /**
     * Obtém todas as personalidades disponíveis
     */
    getPersonalities() {
        return Array.from(this.personalities.values());
    }

    /**
     * Ativa/desativa modo professor
     */
    toggleTeacherMode() {
        this.teacherMode = !this.teacherMode;
        this.saveUserPreferences();
        console.log(`🧠 Modo professor: ${this.teacherMode ? 'ATIVADO' : 'DESATIVADO'}`);
    }

    /**
     * Ativa/desativa modo generativo
     */
    toggleGenerativeMode() {
        this.generativeMode = !this.generativeMode;
        this.saveUserPreferences();
        console.log(`🧠 Modo generativo: ${this.generativeMode ? 'ATIVADO' : 'DESATIVADO'}`);
    }

    /**
     * Ativa/desativa orquestração
     */
    toggleOrchestration() {
        this.orchestrationEnabled = !this.orchestrationEnabled;
        this.saveUserPreferences();
        
        if (this.orchestrationEnabled && !this.orchestrator) {
            this.initializeOrchestrator();
        }
        
        console.log(`🧠 Orquestração: ${this.orchestrationEnabled ? 'ATIVADA' : 'DESATIVADA'}`);
    }

    /**
     * Obtém recomendações de otimização do orquestrador
     */
    getOptimizationRecommendations() {
        if (this.orchestrator) {
            return this.orchestrator.getOptimizationRecommendations();
        }
        return [];
    }

    /**
     * Aplica recomendação de otimização
     */
    applyOptimizationRecommendation(recommendation) {
        if (this.orchestrator) {
            return this.orchestrator.applyOptimizationRecommendation(recommendation);
        }
        return false;
    }
}

// Exporta para uso global
window.AIUnifiedSystem = AIUnifiedSystem;

// Inicializa automaticamente quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.aiSystem = new AIUnifiedSystem();
});

console.log('🧠 Sistema de IA Unificado carregado');
