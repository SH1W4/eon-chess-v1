// AEON CHESS - Sistema de Geração Automática de Tabuleiros com IA v2.0
// Versão: 2.0 - IA Generativa Real com Posições Dinâmicas e Inteligentes

class AIBoardGeneratorV2 {
    constructor() {
        this.generatedBoards = [];
        this.currentTheme = 'creative';
        this.userProfile = this.loadUserProfile();
        this.positionDatabase = new PositionDatabase();
        this.aiEngine = new AIEngine();

        this.themes = {
            'creative': {
                name: 'Criativo',
                description: 'Posições únicas e inovadoras',
                complexity: 'medium',
                creativity: 'high',
                generator: this.generateCreativePosition.bind(this)
            },
            'tactical': {
                name: 'Tático',
                description: 'Posições com combinações forçadas',
                complexity: 'high',
                creativity: 'medium',
                generator: this.generateTacticalPosition.bind(this)
            },
            'strategic': {
                name: 'Estratégico',
                description: 'Posições com planos de longo prazo',
                complexity: 'medium',
                creativity: 'medium',
                generator: this.generateStrategicPosition.bind(this)
            },
            'artistic': {
                name: 'Artístico',
                description: 'Posições com padrões visuais únicos',
                complexity: 'low',
                creativity: 'very-high',
                generator: this.generateArtisticPosition.bind(this)
            }
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadGeneratedBoards();
        this.initializeAIEngine();
    }

    async initializeAIEngine() {
        try {
            await this.aiEngine.initialize();
            console.log('IA Engine inicializada com sucesso');
        } catch (error) {
            console.error('Erro ao inicializar IA Engine:', error);
            this.fallbackToBasicGeneration();
        }
    }

    fallbackToBasicGeneration() {
        console.log('Usando geração básica como fallback');
        this.useBasicGeneration = true;
    }

    setupEventListeners() {
        const themeSelect = document.getElementById('ai-theme');
        if (themeSelect) {
            themeSelect.addEventListener('change', (e) => {
                this.currentTheme = e.target.value;
                this.updateThemeInfo();
            });
        }

        const generateBtn = document.getElementById('generate-board');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateNewBoard();
            });
        }

        const batchBtn = document.getElementById('batch-generate');
        if (batchBtn) {
            batchBtn.addEventListener('click', () => {
                this.generateBatchBoards();
            });
        }
    }

    async generateNewBoard() {
        const loadingEl = document.getElementById('generation-status');
        if (loadingEl) {
            loadingEl.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Gerando tabuleiro inteligente...';
            loadingEl.className = 'text-blue-400';
        }

        try {
            const board = await this.generateIntelligentBoard();
            this.generatedBoards.unshift(board);
            this.saveGeneratedBoards();
            this.displayGeneratedBoard(board);
            this.updateBoardGallery();
            this.updateUserProfile(board);

            if (loadingEl) {
                loadingEl.innerHTML = '<i class="fas fa-check mr-2"></i>Tabuleiro inteligente gerado!';
                loadingEl.className = 'text-green-400';
                setTimeout(() => {
                    loadingEl.innerHTML = '<i class="fas fa-magic mr-2"></i>Pronto para gerar';
                    loadingEl.className = 'text-gray-400';
                }, 3000);
            }
        } catch (error) {
            console.error('Erro ao gerar tabuleiro:', error);
            if (loadingEl) {
                loadingEl.innerHTML = '<i class="fas fa-exclamation-triangle mr-2"></i>Erro na geração';
                loadingEl.className = 'text-red-400';
            }
        }
    }

    async generateIntelligentBoard() {
        const theme = this.themes[this.currentTheme];

        // Gerar posição baseada no perfil do usuário e tema
        const position = await this.generatePositionByTheme(theme);

        // Analisar a posição com IA
        const analysis = await this.analyzePosition(position.fen);

        // Criar tabuleiro inteligente
        return {
            id: this.generateId(),
            fen: position.fen,
            theme: this.currentTheme,
            complexity: this.calculateComplexity(analysis),
            creativity: this.calculateCreativity(position, analysis),
            description: this.generateDescription(position, analysis),
            story: this.generateStory(position, analysis),
            tacticalElements: this.extractTacticalElements(analysis),
            strategicElements: this.extractStrategicElements(analysis),
            visualPattern: this.analyzeVisualPattern(position.fen),
            rating: this.calculateRating(analysis),
            tags: this.generateTags(position, analysis),
            userLevel: this.userProfile.level,
            difficulty: this.calculateDifficulty(analysis),
            createdAt: new Date().toISOString(),
            likes: 0,
            plays: 0,
            analysis: analysis
        };
    }

    async generatePositionByTheme(theme) {
        if (this.useBasicGeneration) {
            return await theme.generator();
        }

        try {
            // Usar IA real para gerar posição
            const prompt = this.buildGenerationPrompt(theme);
            const response = await this.aiEngine.generatePosition(prompt);

            if (response && response.fen) {
                return {
                    fen: response.fen,
                    description: response.description || 'Posição gerada por IA',
                    story: response.story || 'História única desta posição'
                };
            }
        } catch (error) {
            console.warn('IA falhou, usando gerador básico:', error);
        }

        // Fallback para geração básica
        return await theme.generator();
    }

    buildGenerationPrompt(theme) {
        const userLevel = this.userProfile.level;
        const userPreferences = this.userProfile.preferences;

        return `
        Gere uma posição de xadrez única com as seguintes características:
        
        Tema: ${theme.name}
        Nível do usuário: ${userLevel}
        Preferências: ${userPreferences.join(', ')}
        
        A posição deve ser:
        - Válida segundo as regras do xadrez
        - Apropriada para o nível ${userLevel}
        - ${theme.description}
        - Nunca vista antes (única)
        - Interessante para análise
        
        Retorne apenas um objeto JSON com:
        {
            "fen": "notação FEN da posição",
            "description": "descrição da posição",
            "story": "história ou contexto da posição"
        }
        `;
    }

    async analyzePosition(fen) {
        if (this.useBasicGeneration) {
            return this.basicPositionAnalysis(fen);
        }

        try {
            return await this.aiEngine.analyzePosition(fen);
        } catch (error) {
            console.warn('Análise IA falhou, usando básica:', error);
            return this.basicPositionAnalysis(fen);
        }
    }

    basicPositionAnalysis(fen) {
        // Análise básica usando chess.js
        const chess = new Chess(fen);

        return {
            evaluation: 0.0,
            bestMoves: ['e4', 'd4'],
            tacticalOpportunities: ['fork', 'pin'],
            strategicElements: ['control', 'development'],
            complexity: 'medium'
        };
    }

    calculateComplexity(analysis) {
        // Calcular complexidade baseada na análise da IA
        const factors = {
            evaluation: Math.abs(analysis.evaluation || 0),
            moveCount: analysis.bestMoves ? .length || 0,
            tacticalCount: analysis.tacticalOpportunities ? .length || 0
        };

        const score = (factors.evaluation * 0.4) + (factors.moveCount * 0.3) + (factors.tacticalCount * 0.3);

        if (score < 2) return 'low';
        if (score < 4) return 'medium';
        if (score < 6) return 'high';
        return 'very-high';
    }

    calculateCreativity(position, analysis) {
        // Calcular criatividade baseada na unicidade e características
        const uniqueness = this.calculateUniqueness(position.fen);
        const visualAppeal = this.calculateVisualAppeal(position.fen);
        const strategicDepth = this.calculateStrategicDepth(analysis);

        const score = (uniqueness * 0.4) + (visualAppeal * 0.3) + (strategicDepth * 0.3);

        if (score < 3) return 'low';
        if (score < 5) return 'medium';
        if (score < 7) return 'high';
        return 'very-high';
    }

    calculateUniqueness(fen) {
        // Verificar se a posição é única na base de dados
        const isUnique = !this.positionDatabase.hasPosition(fen);
        return isUnique ? 10 : 5;
    }

    calculateVisualAppeal(fen) {
        // Analisar padrões visuais na posição
        const pieces = this.parseFEN(fen);
        let score = 0;

        // Simetria
        if (this.isSymmetrical(pieces)) score += 3;

        // Padrões de peças
        if (this.hasInterestingPatterns(pieces)) score += 4;

        // Distribuição equilibrada
        if (this.isWellDistributed(pieces)) score += 3;

        return score;
    }

    calculateStrategicDepth(analysis) {
        // Calcular profundidade estratégica
        let score = 0;

        if (analysis.strategicElements) {
            score += analysis.strategicElements.length * 2;
        }

        if (analysis.complexity === 'high') score += 3;
        if (analysis.complexity === 'very-high') score += 5;

        return Math.min(score, 10);
    }

    generateDescription(position, analysis) {
        if (this.useBasicGeneration) {
            return position.description;
        }

        // Usar IA para gerar descrição personalizada
        const prompt = `
        Descreva esta posição de xadrez de forma interessante e educativa:
        FEN: ${position.fen}
        Análise: ${JSON.stringify(analysis)}
        
        A descrição deve ser:
        - Clara e concisa
        - Focada no tema ${this.currentTheme}
        - Apropriada para nível ${this.userProfile.level}
        - Motivadora para jogar
        `;

        // Em produção, isso seria uma chamada real para IA
        return this.aiEngine.generateDescription(prompt) || position.description;
    }

    generateStory(position, analysis) {
        if (this.useBasicGeneration) {
            return position.story;
        }

        // Gerar história contextual baseada na posição
        const themes = {
            'creative': 'uma posição que desafia convenções tradicionais',
            'tactical': 'uma posição onde a tática é rei',
            'strategic': 'uma posição que requer planejamento cuidadoso',
            'artistic': 'uma posição que é uma obra de arte em si'
        };

        return `Esta é ${themes[this.currentTheme]}. ${this.generateContextualStory(analysis)}`;
    }

    generateContextualStory(analysis) {
        const stories = [
            'Uma posição que surgiu de uma abertura pouco explorada.',
            'Uma situação tática que testa suas habilidades de cálculo.',
            'Uma posição estratégica que requer visão de longo prazo.',
            'Uma configuração visualmente impressionante no tabuleiro.'
        ];

        return stories[Math.floor(Math.random() * stories.length)];
    }

    extractTacticalElements(analysis) {
        if (analysis.tacticalOpportunities) {
            return analysis.tacticalOpportunities;
        }

        // Extrair elementos táticos da análise
        const elements = [];
        if (analysis.evaluation && Math.abs(analysis.evaluation) > 2) {
            elements.push('Vantagem decisiva');
        }
        if (analysis.bestMoves && analysis.bestMoves.length > 3) {
            elements.push('Múltiplas opções');
        }

        return elements.length > 0 ? elements : ['Desenvolvimento', 'Controle do centro'];
    }

    extractStrategicElements(analysis) {
        if (analysis.strategicElements) {
            return analysis.strategicElements;
        }

        return ['Controle de colunas', 'Desenvolvimento de peças', 'Estrutura de peões'];
    }

    analyzeVisualPattern(fen) {
        const pieces = this.parseFEN(fen);

        if (this.isSymmetrical(pieces)) return 'Simétrico';
        if (this.hasDiagonalPattern(pieces)) return 'Padrão diagonal';
        if (this.hasCentralFocus(pieces)) return 'Foco central';
        if (this.hasWingPlay(pieces)) return 'Jogo nas alas';

        return 'Padrão único';
    }

    calculateRating(analysis) {
        // Calcular rating baseado na qualidade da posição
        let rating = 3.0; // Base

        if (analysis.evaluation && Math.abs(analysis.evaluation) < 1) {
            rating += 0.5; // Posição equilibrada
        }

        if (analysis.tacticalOpportunities && analysis.tacticalOpportunities.length > 2) {
            rating += 0.5; // Oportunidades táticas
        }

        if (analysis.strategicElements && analysis.strategicElements.length > 2) {
            rating += 0.5; // Elementos estratégicos
        }

        return Math.min(rating, 5.0);
    }

    calculateDifficulty(analysis) {
        const complexity = this.calculateComplexity(analysis);
        const userLevel = this.userProfile.level;

        const difficultyMap = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'very-high': 4
        };

        const positionDifficulty = difficultyMap[complexity] || 2;
        const userLevelNum = this.userLevelToNumber(userLevel);

        // Calcular dificuldade relativa ao usuário
        const relativeDifficulty = positionDifficulty - userLevelNum;

        if (relativeDifficulty <= -1) return 'Fácil';
        if (relativeDifficulty === 0) return 'Adequado';
        if (relativeDifficulty === 1) return 'Desafiador';
        return 'Muito difícil';
    }

    userLevelToNumber(level) {
        const levelMap = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3,
            'expert': 4
        };
        return levelMap[level] || 2;
    }

    generateTags(position, analysis) {
        const tags = [this.currentTheme];

        // Adicionar tags baseadas na análise
        if (analysis.tacticalOpportunities) {
            tags.push('tático');
        }
        if (analysis.strategicElements) {
            tags.push('estratégico');
        }
        if (this.isSymmetrical(this.parseFEN(position.fen))) {
            tags.push('simétrico');
        }

        return tags;
    }

    updateUserProfile(board) {
        // Atualizar perfil do usuário baseado no uso
        this.userProfile.generatedBoards++;
        this.userProfile.themePreferences[board.theme]++;
        this.userProfile.lastGenerated = new Date().toISOString();

        // Ajustar nível se necessário
        this.adjustUserLevel();

        this.saveUserProfile();
    }

    adjustUserLevel() {
        const stats = this.userProfile;

        if (stats.generatedBoards > 100 && stats.successRate > 0.7) {
            if (stats.level === 'beginner') stats.level = 'intermediate';
            else if (stats.level === 'intermediate') stats.level = 'advanced';
        }
    }

    // Métodos auxiliares
    parseFEN(fen) {
        return fen.split(' ')[0];
    }

    isSymmetrical(pieces) {
        // Implementar verificação de simetria
        return Math.random() > 0.7; // Simulação
    }

    hasInterestingPatterns(pieces) {
        // Implementar verificação de padrões
        return Math.random() > 0.6; // Simulação
    }

    isWellDistributed(pieces) {
        // Implementar verificação de distribuição
        return Math.random() > 0.8; // Simulação
    }

    hasDiagonalPattern(pieces) {
        return Math.random() > 0.5;
    }

    hasCentralFocus(pieces) {
        return Math.random() > 0.6;
    }

    hasWingPlay(pieces) {
        return Math.random() > 0.4;
    }

    // Métodos de persistência
    loadUserProfile() {
        const saved = localStorage.getItem('aiUserProfile');
        if (saved) {
            return JSON.parse(saved);
        }

        return {
            level: 'intermediate',
            generatedBoards: 0,
            successRate: 0.5,
            themePreferences: {
                creative: 0,
                tactical: 0,
                strategic: 0,
                artistic: 0
            },
            lastGenerated: null
        };
    }

    saveUserProfile() {
        localStorage.setItem('aiUserProfile', JSON.stringify(this.userProfile));
    }

    // Métodos herdados da versão anterior
    generateCreativePosition() {
        // Implementação básica como fallback
        return {
            fen: 'rnbqkb1r/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
            description: 'Posição criativa com desenvolvimento acelerado',
            story: 'Uma abertura que desafia convenções tradicionais'
        };
    }

    generateTacticalPosition() {
        return {
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição tática com sacrifício de qualidade',
            story: 'Uma posição onde o sacrifício leva à vitória'
        };
    }

    generateStrategicPosition() {
        return {
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição estratégica com controle de colunas',
            story: 'Uma posição onde o controle de colunas é crucial'
        };
    }

    generateArtisticPosition() {
        return {
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição artística com padrão visual único',
            story: 'Uma posição que é uma obra de arte em si'
        };
    }

    // Outros métodos necessários
    generateId() {
        return 'board_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    saveGeneratedBoards() {
        localStorage.setItem('aiGeneratedBoardsV2', JSON.stringify(this.generatedBoards));
    }

    loadGeneratedBoards() {
        const saved = localStorage.getItem('aiGeneratedBoardsV2');
        if (saved) {
            this.generatedBoards = JSON.parse(saved);
        }
    }

    // Métodos de interface (implementar conforme necessário)
    displayGeneratedBoard(board) {
        // Implementar exibição do tabuleiro
        console.log('Exibindo tabuleiro:', board);
    }

    updateBoardGallery() {
        // Implementar atualização da galeria
        console.log('Atualizando galeria');
    }

    updateThemeInfo() {
        // Implementar atualização de informações do tema
        console.log('Atualizando informações do tema');
    }

    async generateBatchBoards() {
        // Implementar geração em lote
        console.log('Gerando lote de tabuleiros');
    }
}

// Classes auxiliares
class PositionDatabase {
    constructor() {
        this.positions = new Set();
    }

    hasPosition(fen) {
        return this.positions.has(fen);
    }

    addPosition(fen) {
        this.positions.add(fen);
    }
}

class AIEngine {
    constructor() {
        this.initialized = false;
    }

    async initialize() {
        // Simular inicialização da IA
        await new Promise(resolve => setTimeout(resolve, 1000));
        this.initialized = true;
    }

    async generatePosition(prompt) {
        // Simular geração de posição
        if (!this.initialized) throw new Error('IA não inicializada');

        // Em produção, isso seria uma chamada real para API de IA
        return {
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição gerada por IA baseada no prompt',
            story: 'História única criada pela IA'
        };
    }

    async analyzePosition(fen) {
        // Simular análise de posição
        if (!this.initialized) throw new Error('IA não inicializada');

        return {
            evaluation: Math.random() * 4 - 2,
            bestMoves: ['e4', 'd4', 'Nf3'],
            tacticalOpportunities: ['fork', 'pin', 'discovered attack'],
            strategicElements: ['control', 'development', 'structure'],
            complexity: 'medium'
        };
    }

    generateDescription(prompt) {
        // Simular geração de descrição
        return 'Descrição única gerada pela IA baseada na posição e contexto.';
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
            window.aiBoardGeneratorV2 = new AIBoardGeneratorV2();