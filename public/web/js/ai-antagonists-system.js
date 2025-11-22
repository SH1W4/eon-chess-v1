/**
 * 👹 Sistema de Antagonistas de IA - Aeon Chess
 * 
 * Este sistema cria antagonistas desafiadores com personalidades únicas:
 * - Antagonistas baseados em jogadores históricos
 * - Antagonistas com estilos específicos
 * - Antagonistas com níveis de dificuldade variados
 * - Sistema de evolução e adaptação
 * 
 * @version 1.0.0
 * @author Aeon Chess Team
 */

class AIAntagonistsSystem {
    constructor() {
        this.antagonists = new Map();
        this.activeAntagonist = null;
        this.difficultyLevel = 'medium';
        this.adaptationEnabled = true;
        this.learningEnabled = true;
        
        this.initializeAntagonists();
        this.initializeEventListeners();
        this.loadAntagonistPreferences();
        
        console.log('👹 Sistema de Antagonistas de IA inicializado');
    }

    /**
     * Inicializa os antagonistas disponíveis
     */
    initializeAntagonists() {
        // Antagonista: O Mestre Implacável
        this.antagonists.set('implacable_master', {
            name: 'O Mestre Implacável',
            description: 'Um jogador que nunca perdoa erros e explora cada fraqueza',
            style: 'punishing',
            difficulty: 'expert',
            color: '#8B0000',
            // Características avançadas
            strengths: ['Punição de erros', 'Análise profunda', 'Precisão técnica', 'Pressão constante'],
            weaknesses: ['Pode ser previsível', 'Menos criativo', 'Rigidez estratégica'],
            preferredOpenings: ['Defesa Siciliana', 'Gambito do Rei', 'Defesa Francesa'],
            endgameSpecialty: 'Finais técnicos precisos',
            timeManagement: 'aggressive',
            riskTolerance: 'low',
            communicationStyle: 'cold',
            personalityTraits: ['Implacável', 'Técnico', 'Punitivo', 'Preciso'],
            motivationalQuotes: [
                'Cada erro será punido sem misericórdia.',
                'A precisão é a única virtude que importa.',
                'Não há lugar para compaixão no xadrez.'
            ],
            analysisFocus: ['erros', 'punicao', 'precisao', 'pressao'],
            learningPath: ['tecnica_avancada', 'punicao_erros', 'finais_tecnicos', 'pressao_constante'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'immediate_punishment',
                responseToGoodMoves: 'increased_pressure',
                adaptationSpeed: 'slow',
                psychologicalWarfare: 'high',
                mercyLevel: 'none'
            }
        });

        // Antagonista: O Psicólogo Sombrio
        this.antagonists.set('dark_psychologist', {
            name: 'O Psicólogo Sombrio',
            description: 'Especialista em guerra psicológica e manipulação mental',
            style: 'psychological',
            difficulty: 'advanced',
            color: '#2F4F4F',
            // Características avançadas
            strengths: ['Guerra psicológica', 'Manipulação mental', 'Leitura de oponente', 'Pressão emocional'],
            weaknesses: ['Pode ser vulnerável a jogadas diretas', 'Menos focado em técnica pura'],
            preferredOpenings: ['Defesa Holandesa', 'Gambito Budapest', 'Abertura Bird'],
            endgameSpecialty: 'Finais psicológicos',
            timeManagement: 'manipulative',
            riskTolerance: 'calculated',
            communicationStyle: 'manipulative',
            personalityTraits: ['Manipulador', 'Psicológico', 'Sombrio', 'Calculista'],
            motivationalQuotes: [
                'A mente é o tabuleiro mais importante.',
                'Cada movimento é uma mensagem para sua psique.',
                'O medo é meu aliado mais poderoso.'
            ],
            analysisFocus: ['psicologia', 'manipulacao', 'medo', 'pressao_emocional'],
            learningPath: ['psicologia_xadrez', 'manipulacao_mental', 'guerra_psicologica', 'leitura_oponente'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'psychological_pressure',
                responseToGoodMoves: 'mind_games',
                adaptationSpeed: 'medium',
                psychologicalWarfare: 'maximum',
                mercyLevel: 'none'
            }
        });

        // Antagonista: O Artista Destrutivo
        this.antagonists.set('destructive_artist', {
            name: 'O Artista Destrutivo',
            description: 'Cria posições caóticas e destrói a harmonia do jogo',
            style: 'chaotic',
            difficulty: 'intermediate',
            color: '#FF4500',
            // Características avançadas
            strengths: ['Criatividade destrutiva', 'Caos controlado', 'Posições complexas', 'Sacrifícios artísticos'],
            weaknesses: ['Pode ser imprevisível demais', 'Menos consistente', 'Risco excessivo'],
            preferredOpenings: ['Gambito do Rei Aceito', 'Defesa Benoni', 'Gambito Blackmar-Diemer'],
            endgameSpecialty: 'Finais caóticos',
            timeManagement: 'chaotic',
            riskTolerance: 'extreme',
            communicationStyle: 'artistic',
            personalityTraits: ['Destrutivo', 'Artístico', 'Caótico', 'Criativo'],
            motivationalQuotes: [
                'A beleza está na destruição da ordem.',
                'O caos é minha tela, o xadrez minha arte.',
                'Quebre as regras para criar algo único.'
            ],
            analysisFocus: ['caos', 'destruicao', 'criatividade', 'sacrificios'],
            learningPath: ['caos_controlado', 'sacrificios_artisticos', 'posicoes_complexas', 'destruicao_harmonia'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'creative_destruction',
                responseToGoodMoves: 'increased_chaos',
                adaptationSpeed: 'fast',
                psychologicalWarfare: 'medium',
                mercyLevel: 'low'
            }
        });

        // Antagonista: O Calculador Máquina
        this.antagonists.set('machine_calculator', {
            name: 'O Calculador Máquina',
            description: 'Análise fria e calculada, como uma máquina sem emoções',
            style: 'mechanical',
            difficulty: 'expert',
            color: '#708090',
            // Características avançadas
            strengths: ['Cálculo preciso', 'Análise fria', 'Eficiência máxima', 'Sem emoções'],
            weaknesses: ['Pode ser previsível', 'Falta de criatividade', 'Rigidez absoluta'],
            preferredOpenings: ['Defesa Caro-Kann', 'Abertura Inglesa', 'Defesa Escandinava'],
            endgameSpecialty: 'Finais matemáticos',
            timeManagement: 'precise',
            riskTolerance: 'calculated',
            communicationStyle: 'mechanical',
            personalityTraits: ['Mecânico', 'Calculado', 'Frio', 'Eficiente'],
            motivationalQuotes: [
                'A emoção é o erro mais comum no xadrez.',
                'Cada movimento é uma equação a ser resolvida.',
                'A eficiência é a única métrica que importa.'
            ],
            analysisFocus: ['calculo', 'eficiencia', 'precisao', 'matematica'],
            learningPath: ['calculo_avancado', 'eficiencia_maxima', 'analise_fria', 'matematica_xadrez'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'mathematical_exploitation',
                responseToGoodMoves: 'increased_calculation',
                adaptationSpeed: 'slow',
                psychologicalWarfare: 'none',
                mercyLevel: 'none'
            }
        });

        // Antagonista: O Predador Noturno
        this.antagonists.set('night_predator', {
            name: 'O Predador Noturno',
            description: 'Caça suas presas com paciência e precisão mortal',
            style: 'predatory',
            difficulty: 'advanced',
            color: '#191970',
            // Características avançadas
            strengths: ['Paciência de caçador', 'Precisão mortal', 'Instinto predatório', 'Emboscadas'],
            weaknesses: ['Pode ser lento no início', 'Menos agressivo inicialmente'],
            preferredOpenings: ['Defesa Pirc', 'Abertura Reti', 'Defesa Moderna'],
            endgameSpecialty: 'Finais de caçador',
            timeManagement: 'patient',
            riskTolerance: 'low',
            communicationStyle: 'predatory',
            personalityTraits: ['Predatório', 'Paciente', 'Mortal', 'Instintivo'],
            motivationalQuotes: [
                'A presa mais saborosa é aquela que pensa que está segura.',
                'A paciência é a arma do verdadeiro predador.',
                'Cada movimento é um passo em direção ao abate.'
            ],
            analysisFocus: ['paciencia', 'emboscada', 'predacao', 'morte_lenta'],
            learningPath: ['paciencia_predatoria', 'emboscadas', 'instinto_cacador', 'morte_gradual'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'lethal_strike',
                responseToGoodMoves: 'increased_patience',
                adaptationSpeed: 'medium',
                psychologicalWarfare: 'high',
                mercyLevel: 'none'
            }
        });

        // Antagonista: O Imperador Tirano
        this.antagonists.set('tyrant_emperor', {
            name: 'O Imperador Tirano',
            description: 'Domina o tabuleiro com autoridade absoluta e controle total',
            style: 'tyrannical',
            difficulty: 'expert',
            color: '#800020',
            // Características avançadas
            strengths: ['Controle absoluto', 'Autoridade dominante', 'Poder esmagador', 'Dominação total'],
            weaknesses: ['Pode ser arrogante', 'Subestima oponentes', 'Rigidez imperial'],
            preferredOpenings: ['Abertura Espanhola', 'Defesa Índia do Rei', 'Gambito da Dama'],
            endgameSpecialty: 'Finais imperiais',
            timeManagement: 'dominant',
            riskTolerance: 'medium',
            communicationStyle: 'imperial',
            personalityTraits: ['Tirânico', 'Dominante', 'Autoritário', 'Poderoso'],
            motivationalQuotes: [
                'O tabuleiro é meu império, as peças meus súditos.',
                'A submissão é a única opção para os fracos.',
                'O poder absoluto corrompe absolutamente.'
            ],
            analysisFocus: ['dominacao', 'controle', 'poder', 'autoridade'],
            learningPath: ['dominacao_absoluta', 'controle_imperial', 'poder_esmagador', 'autoridade_total'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'imperial_punishment',
                responseToGoodMoves: 'increased_domination',
                adaptationSpeed: 'slow',
                psychologicalWarfare: 'high',
                mercyLevel: 'none'
            }
        });

        // Antagonista: O Ilusionista Mestre
        this.antagonists.set('master_illusionist', {
            name: 'O Ilusionista Mestre',
            description: 'Cria ilusões e armadilhas que confundem e enganam',
            style: 'deceptive',
            difficulty: 'advanced',
            color: '#9932CC',
            // Características avançadas
            strengths: ['Ilusões complexas', 'Armadilhas sutis', 'Engano mestre', 'Confusão mental'],
            weaknesses: ['Pode ser vulnerável a jogadas diretas', 'Complexidade excessiva'],
            preferredOpenings: ['Gambito Evans', 'Defesa Alekhine', 'Abertura Trompowsky'],
            endgameSpecialty: 'Finais ilusórios',
            timeManagement: 'deceptive',
            riskTolerance: 'high',
            communicationStyle: 'mysterious',
            personalityTraits: ['Ilusório', 'Enganoso', 'Misterioso', 'Complexo'],
            motivationalQuotes: [
                'A verdade é apenas uma ilusão que você aceita.',
                'Cada movimento é uma armadilha disfarçada.',
                'O que você vê não é o que realmente existe.'
            ],
            analysisFocus: ['ilusao', 'armadilha', 'engano', 'confusao'],
            learningPath: ['ilusoes_complexas', 'armadilhas_sutis', 'engano_mestre', 'confusao_mental'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'deceptive_trap',
                responseToGoodMoves: 'increased_illusion',
                adaptationSpeed: 'fast',
                psychologicalWarfare: 'maximum',
                mercyLevel: 'low'
            }
        });

        // Antagonista: O Berserker Furioso
        this.antagonists.set('furious_berserker', {
            name: 'O Berserker Furioso',
            description: 'Ataque frenético e agressão descontrolada',
            style: 'berserk',
            difficulty: 'intermediate',
            color: '#DC143C',
            // Características avançadas
            strengths: ['Agressão descontrolada', 'Ataque frenético', 'Intensidade máxima', 'Fúria incontrolável'],
            weaknesses: ['Pode ser imprevisível', 'Falta de estratégia', 'Risco extremo'],
            preferredOpenings: ['Gambito do Rei', 'Ataque Grob', 'Gambito Blackmar-Diemer'],
            endgameSpecialty: 'Finais de ataque',
            timeManagement: 'frenetic',
            riskTolerance: 'extreme',
            communicationStyle: 'aggressive',
            personalityTraits: ['Furioso', 'Berserk', 'Agressivo', 'Incontrolável'],
            motivationalQuotes: [
                'A fúria é minha força, o caos minha arma!',
                'Cada movimento é um golpe mortal!',
                'A destruição é a única linguagem que entendo!'
            ],
            analysisFocus: ['furia', 'ataque', 'agressao', 'destruicao'],
            learningPath: ['furia_berserk', 'ataque_frenetico', 'agressao_maxima', 'destruicao_total'],
            // Comportamento específico
            behavior: {
                responseToMistakes: 'berserk_rage',
                responseToGoodMoves: 'increased_fury',
                adaptationSpeed: 'very_fast',
                psychologicalWarfare: 'high',
                mercyLevel: 'none'
            }
        });

        this.activeAntagonist = this.antagonists.get('implacable_master');
    }

    /**
     * Inicializa os event listeners do sistema
     */
    initializeEventListeners() {
        // Eventos de mudança de antagonista
        document.addEventListener('antagonistChanged', (e) => {
            this.changeAntagonist(e.detail.antagonist);
        });

        // Eventos de ajuste de dificuldade
        document.addEventListener('difficultyChanged', (e) => {
            this.setDifficulty(e.detail.difficulty);
        });

        // Eventos de adaptação
        document.addEventListener('adaptationToggled', (e) => {
            this.toggleAdaptation(e.detail.enabled);
        });
    }

    /**
     * Carrega as preferências de antagonista
     */
    loadAntagonistPreferences() {
        try {
            const preferences = localStorage.getItem('antagonistPreferences');
            if (preferences) {
                const prefs = JSON.parse(preferences);
                this.activeAntagonist = this.antagonists.get(prefs.antagonist) || this.activeAntagonist;
                this.difficultyLevel = prefs.difficulty || 'medium';
                this.adaptationEnabled = prefs.adaptationEnabled !== false;
                this.learningEnabled = prefs.learningEnabled !== false;
            }
        } catch (error) {
            console.warn('Erro ao carregar preferências de antagonista:', error);
        }
    }

    /**
     * Salva as preferências de antagonista
     */
    saveAntagonistPreferences() {
        try {
            const preferences = {
                antagonist: this.activeAntagonist.style,
                difficulty: this.difficultyLevel,
                adaptationEnabled: this.adaptationEnabled,
                learningEnabled: this.learningEnabled
            };
            localStorage.setItem('antagonistPreferences', JSON.stringify(preferences));
        } catch (error) {
            console.warn('Erro ao salvar preferências de antagonista:', error);
        }
    }

    /**
     * Muda o antagonista ativo
     */
    changeAntagonist(antagonistKey) {
        const antagonist = this.antagonists.get(antagonistKey);
        if (antagonist) {
            this.activeAntagonist = antagonist;
            this.saveAntagonistPreferences();
            this.updateUI();
            this.notifyAntagonistChange();
            
            console.log(`👹 Antagonista alterado para: ${antagonist.name}`);
        }
    }

    /**
     * Define o nível de dificuldade
     */
    setDifficulty(difficulty) {
        this.difficultyLevel = difficulty;
        this.saveAntagonistPreferences();
        this.updateDifficulty();
        
        console.log(`👹 Dificuldade alterada para: ${difficulty}`);
    }

    /**
     * Ativa/desativa adaptação
     */
    toggleAdaptation(enabled) {
        this.adaptationEnabled = enabled;
        this.saveAntagonistPreferences();
        
        console.log(`👹 Adaptação: ${enabled ? 'ATIVADA' : 'DESATIVADA'}`);
    }

    /**
     * Atualiza a interface
     */
    updateUI() {
        // Atualiza indicador de antagonista
        const indicator = document.getElementById('antagonist-indicator');
        if (indicator) {
            indicator.textContent = this.activeAntagonist.name;
            indicator.style.color = this.activeAntagonist.color;
        }

        // Atualiza descrição
        const description = document.getElementById('antagonist-description');
        if (description) {
            description.textContent = this.activeAntagonist.description;
        }

        // Atualiza estilo visual
        this.updateVisualStyle();
    }

    /**
     * Atualiza o estilo visual baseado no antagonista
     */
    updateVisualStyle() {
        const root = document.documentElement;
        root.style.setProperty('--antagonist-primary-color', this.activeAntagonist.color);
        
        // Aplica tema de cores baseado no antagonista
        const theme = this.getAntagonistTheme();
        root.style.setProperty('--antagonist-theme-bg', theme.background);
        root.style.setProperty('--antagonist-theme-text', theme.text);
        root.style.setProperty('--antagonist-theme-accent', theme.accent);
    }

    /**
     * Obtém o tema visual do antagonista
     */
    getAntagonistTheme() {
        const themes = {
            punishing: {
                background: '#fff0f0',
                text: '#8B0000',
                accent: '#CD5C5C'
            },
            psychological: {
                background: '#f0f0f0',
                text: '#2F4F4F',
                accent: '#708090'
            },
            chaotic: {
                background: '#fff8f0',
                text: '#FF4500',
                accent: '#FF6347'
            },
            mechanical: {
                background: '#f8f8f8',
                text: '#708090',
                accent: '#C0C0C0'
            },
            predatory: {
                background: '#f0f0ff',
                text: '#191970',
                accent: '#4169E1'
            },
            tyrannical: {
                background: '#fff0f5',
                text: '#800020',
                accent: '#DC143C'
            },
            deceptive: {
                background: '#fdf8ff',
                text: '#9932CC',
                accent: '#DDA0DD'
            },
            berserk: {
                background: '#fff0f0',
                text: '#DC143C',
                accent: '#FF6347'
            }
        };

        return themes[this.activeAntagonist.style] || themes.punishing;
    }

    /**
     * Notifica mudança de antagonista
     */
    notifyAntagonistChange() {
        const event = new CustomEvent('antagonistChanged', {
            detail: {
                antagonist: this.activeAntagonist,
                previousAntagonist: this.activeAntagonist
            }
        });
        document.dispatchEvent(event);
    }

    /**
     * Atualiza dificuldade
     */
    updateDifficulty() {
        // Ajusta comportamento baseado na dificuldade
        const difficultyMultipliers = {
            'easy': 0.7,
            'medium': 1.0,
            'hard': 1.3,
            'expert': 1.6,
            'nightmare': 2.0
        };

        const multiplier = difficultyMultipliers[this.difficultyLevel] || 1.0;
        
        // Ajusta profundidade de análise
        this.activeAntagonist.analysisDepth = Math.floor(this.activeAntagonist.analysisDepth * multiplier);
        
        console.log(`👹 Dificuldade ajustada: ${this.difficultyLevel} (multiplicador: ${multiplier})`);
    }

    /**
     * Analisa posição com o antagonista ativo
     */
    async analyzePosition(fen, playerMove = null) {
        console.log(`👹 ${this.activeAntagonist.name} analisando posição...`);

        try {
            const analysis = await this.performAntagonistAnalysis(fen, playerMove);
            const personalizedAnalysis = this.personalizeAntagonistAnalysis(analysis);
            
            this.dispatchAnalysisResult(personalizedAnalysis);
            return personalizedAnalysis;
        } catch (error) {
            console.error('Erro na análise do antagonista:', error);
            throw error;
        }
    }

    /**
     * Realiza análise específica do antagonista
     */
    async performAntagonistAnalysis(fen, playerMove) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const analysis = {
                    evaluation: this.calculateAntagonistEvaluation(fen),
                    bestMoves: this.findAntagonistMoves(fen),
                    plan: this.generateAntagonistPlan(fen),
                    threats: this.identifyAntagonistThreats(fen),
                    opportunities: this.identifyAntagonistOpportunities(fen),
                    psychologicalFactors: this.analyzePsychologicalFactors(fen, playerMove),
                    depth: this.activeAntagonist.analysisDepth,
                    timestamp: Date.now()
                };
                resolve(analysis);
            }, 1000 + (this.activeAntagonist.analysisDepth * 150));
        });
    }

    /**
     * Personaliza análise baseada no antagonista
     */
    personalizeAntagonistAnalysis(analysis) {
        const antagonist = this.activeAntagonist;
        
        // Aplica estilo do antagonista
        switch (antagonist.style) {
            case 'punishing':
                analysis.focus = 'Punição de erros';
                analysis.recommendations = this.addPunishingAdvice(analysis);
                break;
            case 'psychological':
                analysis.focus = 'Guerra psicológica';
                analysis.recommendations = this.addPsychologicalAdvice(analysis);
                break;
            case 'chaotic':
                analysis.focus = 'Criação de caos';
                analysis.recommendations = this.addChaoticAdvice(analysis);
                break;
            case 'mechanical':
                analysis.focus = 'Cálculo preciso';
                analysis.recommendations = this.addMechanicalAdvice(analysis);
                break;
            case 'predatory':
                analysis.focus = 'Caça paciente';
                analysis.recommendations = this.addPredatoryAdvice(analysis);
                break;
            case 'tyrannical':
                analysis.focus = 'Dominação absoluta';
                analysis.recommendations = this.addTyrannicalAdvice(analysis);
                break;
            case 'deceptive':
                analysis.focus = 'Ilusões e armadilhas';
                analysis.recommendations = this.addDeceptiveAdvice(analysis);
                break;
            case 'berserk':
                analysis.focus = 'Ataque frenético';
                analysis.recommendations = this.addBerserkAdvice(analysis);
                break;
        }

        analysis.antagonist = antagonist.name;
        analysis.style = antagonist.style;
        analysis.difficulty = this.difficultyLevel;
        
        return analysis;
    }

    // Métodos auxiliares para simulação
    calculateAntagonistEvaluation(fen) { 
        return (Math.random() * 2 - 1) * (this.difficultyLevel === 'nightmare' ? 1.5 : 1.0); 
    }
    
    findAntagonistMoves(fen) { 
        const moves = ['e4', 'd4', 'Nf3', 'c4', 'e5', 'd5'];
        return moves.slice(0, Math.floor(Math.random() * 3) + 2);
    }
    
    generateAntagonistPlan(fen) { 
        const plans = [
            'Punir cada erro do oponente',
            'Criar pressão psicológica constante',
            'Estabelecer controle absoluto',
            'Preparar armadilhas sutis',
            'Executar ataque devastador'
        ];
        return plans[Math.floor(Math.random() * plans.length)];
    }
    
    identifyAntagonistThreats(fen) { 
        return ['Xeque em 3', 'Perda de qualidade', 'Ataque no rei', 'Sacrifício devastador'];
    }
    
    identifyAntagonistOpportunities(fen) { 
        return ['Exploitar fraqueza', 'Criar pressão', 'Estabelecer controle', 'Preparar combinação'];
    }
    
    analyzePsychologicalFactors(fen, playerMove) {
        return {
            pressure: Math.random() * 100,
            intimidation: Math.random() * 100,
            confusion: Math.random() * 100,
            fear: Math.random() * 100
        };
    }

    // Métodos de conselhos específicos dos antagonistas
    addPunishingAdvice(analysis) { 
        return ['Punir imediatamente qualquer erro', 'Manter pressão constante', 'Explorar cada fraqueza'];
    }
    
    addPsychologicalAdvice(analysis) { 
        return ['Criar confusão mental', 'Aplicar pressão psicológica', 'Manipular emoções'];
    }
    
    addChaoticAdvice(analysis) { 
        return ['Criar posições caóticas', 'Sacrifícios artísticos', 'Quebrar a harmonia'];
    }
    
    addMechanicalAdvice(analysis) { 
        return ['Cálculo preciso', 'Eficiência máxima', 'Análise fria'];
    }
    
    addPredatoryAdvice(analysis) { 
        return ['Paciência de caçador', 'Preparar emboscada', 'Ataque mortal'];
    }
    
    addTyrannicalAdvice(analysis) { 
        return ['Estabelecer domínio absoluto', 'Esmagar resistência', 'Controle total'];
    }
    
    addDeceptiveAdvice(analysis) { 
        return ['Criar ilusões', 'Preparar armadilhas', 'Confundir o oponente'];
    }
    
    addBerserkAdvice(analysis) { 
        return ['Ataque frenético', 'Destruição total', 'Fúria incontrolável'];
    }

    // Métodos de dispatch de eventos
    dispatchAnalysisResult(analysis) {
        const event = new CustomEvent('antagonistAnalysisComplete', { detail: analysis });
        document.dispatchEvent(event);
    }

    /**
     * Obtém estatísticas do sistema de antagonistas
     */
    getAntagonistStats() {
        return {
            activeAntagonist: this.activeAntagonist.name,
            totalAntagonists: this.antagonists.size,
            difficultyLevel: this.difficultyLevel,
            adaptationEnabled: this.adaptationEnabled,
            learningEnabled: this.learningEnabled,
            timestamp: Date.now()
        };
    }

    /**
     * Obtém todos os antagonistas disponíveis
     */
    getAntagonists() {
        return Array.from(this.antagonists.values());
    }

    /**
     * Obtém características do antagonista ativo
     */
    getAntagonistCharacteristics() {
        return this.activeAntagonist.strengths || ['Característica padrão'];
    }

    /**
     * Obtém fraquezas do antagonista ativo
     */
    getAntagonistWeaknesses() {
        return this.activeAntagonist.weaknesses || ['Sem fraquezas identificadas'];
    }

    /**
     * Obtém aberturas preferidas do antagonista
     */
    getAntagonistOpenings() {
        return this.activeAntagonist.preferredOpenings || ['Aberturas padrão'];
    }

    /**
     * Obtém citações do antagonista
     */
    getAntagonistQuotes() {
        return this.activeAntagonist.motivationalQuotes || ['Sem citações disponíveis'];
    }

    /**
     * Obtém comportamento específico do antagonista
     */
    getAntagonistBehavior() {
        return this.activeAntagonist.behavior || {};
    }
}

// Exporta para uso global
window.AIAntagonistsSystem = AIAntagonistsSystem;

// Inicializa automaticamente quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.antagonistSystem = new AIAntagonistsSystem();
});

console.log('👹 Sistema de Antagonistas de IA carregado');
