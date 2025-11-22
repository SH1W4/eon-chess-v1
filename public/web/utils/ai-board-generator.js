// AEON CHESS - Sistema de Geração Automática de Tabuleiros com IA
// Versão: 1.0 - Tabuleiros Generativos e Personalizados

class AIBoardGenerator {
    constructor() {
        this.generatedBoards = [];
        this.currentTheme = 'creative';
        this.aiModels = {
            'creative': 'creative-chess-v1',
            'tactical': 'tactical-chess-v2',
            'strategic': 'strategic-chess-v3',
            'artistic': 'artistic-chess-v1'
        };

        this.themes = {
            'creative': {
                name: 'Criativo',
                description: 'Posições únicas e inovadoras',
                complexity: 'medium',
                creativity: 'high'
            },
            'tactical': {
                name: 'Tático',
                description: 'Posições com combinações forçadas',
                complexity: 'high',
                creativity: 'medium'
            },
            'strategic': {
                name: 'Estratégico',
                description: 'Posições com planos de longo prazo',
                complexity: 'medium',
                creativity: 'medium'
            },
            'artistic': {
                name: 'Artístico',
                description: 'Posições com padrões visuais únicos',
                complexity: 'low',
                creativity: 'very-high'
            }
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadGeneratedBoards();
    }

    setupEventListeners() {
        // Theme selector
        const themeSelect = document.getElementById('ai-theme');
        if (themeSelect) {
            themeSelect.addEventListener('change', (e) => {
                this.currentTheme = e.target.value;
                this.updateThemeInfo();
            });
        }

        // Generate button
        const generateBtn = document.getElementById('generate-board');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateNewBoard();
            });
        }

        // Batch generate
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
            loadingEl.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Gerando tabuleiro...';
            loadingEl.className = 'text-blue-400';
        }

        try {
            const board = await this.generateBoardWithAI();
            this.generatedBoards.unshift(board);
            this.saveGeneratedBoards();
            this.displayGeneratedBoard(board);
            this.updateBoardGallery();

            if (loadingEl) {
                loadingEl.innerHTML = '<i class="fas fa-check mr-2"></i>Tabuleiro gerado com sucesso!';
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

    async generateBoardWithAI() {
        const theme = this.themes[this.currentTheme];
        const model = this.aiModels[this.currentTheme];

        // Simulação de chamada para IA generativa
        // Em produção, isso seria uma API real
        const board = await this.simulateAIGeneration(theme, model);

        return {
            id: this.generateId(),
            fen: board.fen,
            theme: this.currentTheme,
            complexity: board.complexity,
            creativity: board.creativity,
            description: board.description,
            story: board.story,
            tacticalElements: board.tacticalElements,
            strategicElements: board.strategicElements,
            visualPattern: board.visualPattern,
            createdAt: new Date().toISOString(),
            likes: 0,
            plays: 0,
            rating: board.rating,
            tags: board.tags
        };
    }

    async simulateAIGeneration(theme, model) {
        // Simulação de diferentes tipos de geração baseada no tema
        const generators = {
            'creative': this.generateCreativePosition.bind(this),
            'tactical': this.generateTacticalPosition.bind(this),
            'strategic': this.generateStrategicPosition.bind(this),
            'artistic': this.generateArtisticPosition.bind(this)
        };

        const generator = generators[theme.name.toLowerCase()] || generators.creative;
        return await generator();
    }

    async generateCreativePosition() {
        // Posições criativas com peças em posições inusitadas mas válidas
        const creativePositions = [{
                fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                description: 'Posição criativa com desenvolvimento acelerado',
                story: 'Uma abertura que desafia convenções tradicionais',
                complexity: 'medium',
                creativity: 'high',
                tacticalElements: ['Desenvolvimento rápido', 'Controle do centro'],
                strategicElements: ['Iniciativa', 'Espaço'],
                visualPattern: 'Simétrico com assimetria tática',
                rating: 3.5,
                tags: ['criativo', 'desenvolvimento', 'iniciativa']
            },
            {
                fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                description: 'Posição inicial com twist criativo',
                story: 'O tabuleiro clássico visto sob nova perspectiva',
                complexity: 'low',
                creativity: 'very-high',
                tacticalElements: ['Todas as possibilidades'],
                strategicElements: ['Planejamento', 'Flexibilidade'],
                visualPattern: 'Simetria perfeita',
                rating: 4.0,
                tags: ['clássico', 'criativo', 'fundamental']
            }
        ];

        return creativePositions[Math.floor(Math.random() * creativePositions.length)];
    }

    async generateTacticalPosition() {
        // Posições táticas com combinações forçadas
        const tacticalPositions = [{
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição tática com sacrifício de qualidade',
            story: 'Uma posição onde o sacrifício leva à vitória',
            complexity: 'high',
            creativity: 'medium',
            tacticalElements: ['Sacrifício', 'Combinação', 'Mate'],
            strategicElements: ['Iniciativa', 'Desenvolvimento'],
            visualPattern: 'Assimétrico tático',
            rating: 4.5,
            tags: ['tático', 'sacrifício', 'combinação']
        }];

        return tacticalPositions[Math.floor(Math.random() * tacticalPositions.length)];
    }

    async generateStrategicPosition() {
        // Posições estratégicas com planos de longo prazo
        const strategicPositions = [{
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição estratégica com controle de colunas',
            story: 'Uma posição onde o controle de colunas é crucial',
            complexity: 'medium',
            creativity: 'medium',
            tacticalElements: ['Controle de colunas', 'Desenvolvimento'],
            strategicElements: ['Controle de colunas', 'Planejamento'],
            visualPattern: 'Estrutural',
            rating: 4.0,
            tags: ['estratégico', 'colunas', 'estrutura']
        }];

        return strategicPositions[Math.floor(Math.random() * strategicPositions.length)];
    }

    async generateArtisticPosition() {
        // Posições artísticas com padrões visuais únicos
        const artisticPositions = [{
            fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
            description: 'Posição artística com padrão visual único',
            story: 'Uma posição que é uma obra de arte em si',
            complexity: 'low',
            creativity: 'very-high',
            tacticalElements: ['Beleza visual', 'Simetria'],
            strategicElements: ['Harmonia', 'Equilíbrio'],
            visualPattern: 'Artístico único',
            rating: 4.8,
            tags: ['artístico', 'visual', 'beleza']
        }];

        return artisticPositions[Math.floor(Math.random() * artisticPositions.length)];
    }

    async generateBatchBoards() {
        const count = 5; // Gerar 5 tabuleiros de uma vez
        const batchBoards = [];

        for (let i = 0; i < count; i++) {
            try {
                const board = await this.generateBoardWithAI();
                batchBoards.push(board);
            } catch (error) {
                console.error(`Erro ao gerar tabuleiro ${i + 1}:`, error);
            }
        }

        this.generatedBoards.unshift(...batchBoards);
        this.saveGeneratedBoards();
        this.updateBoardGallery();

        // Notificar sucesso
        const notification = document.getElementById('batch-notification');
        if (notification) {
            notification.innerHTML = `<i class="fas fa-check mr-2"></i>${batchBoards.length} tabuleiros gerados com sucesso!`;
            notification.className = 'text-green-400';
            setTimeout(() => {
                notification.innerHTML = '';
                notification.className = 'hidden';
            }, 5000);
        }
    }

    displayGeneratedBoard(board) {
        const boardContainer = document.getElementById('ai-generated-board');
        if (!boardContainer) return;

        // Criar tabuleiro visual
        const boardHTML = `
            <div class="ai-board-card bg-gradient-to-br from-[#1a1a1a] to-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-6 shadow-xl">
                <div class="flex items-center justify-between mb-4">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                            <i class="fas fa-robot text-white"></i>
                        </div>
                        <div>
                            <h4 class="text-lg font-semibold text-white">${this.themes[board.theme].name}</h4>
                            <p class="text-sm text-gray-400">Gerado por IA</p>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <span class="text-xs text-gray-400">Complexidade:</span>
                        <div class="flex space-x-1">
                            ${this.generateComplexityStars(board.complexity)}
                        </div>
                    </div>
                </div>
                
                <div class="grid lg:grid-cols-2 gap-6">
                    <!-- Tabuleiro -->
                    <div class="space-y-4">
                        <div class="bg-[#0f0f0f] border border-[#2a2a2a] rounded-lg p-4">
                            <chess-board id="ai-board-${board.id}" draggable-pieces="" position="${board.fen}" class="w-full" style="max-width: 100%; aspect-ratio: 1 / 1;"></chess-board>
                        </div>
                        
                        <!-- Controles -->
                        <div class="flex space-x-2">
                            <button class="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm" onclick="aiBoardGenerator.playBoard('${board.id}')">
                                <i class="fas fa-play mr-2"></i>Jogar
                            </button>
                            <button class="px-3 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm" onclick="aiBoardGenerator.analyzeBoard('${board.id}')">
                                <i class="fas fa-brain mr-2"></i>Analisar
                            </button>
                            <button class="px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm" onclick="aiBoardGenerator.saveBoard('${board.id}')">
                                <i class="fas fa-heart mr-2"></i>Salvar
                            </button>
                        </div>
                    </div>
                    
                    <!-- Informações -->
                    <div class="space-y-4">
                        <div>
                            <h5 class="text-md font-semibold text-white mb-2">Descrição</h5>
                            <p class="text-gray-300 text-sm">${board.description}</p>
                        </div>
                        
                        <div>
                            <h5 class="text-md font-semibold text-white mb-2">História</h5>
                            <p class="text-gray-300 text-sm">${board.story}</p>
                        </div>
                        
                        <div>
                            <h5 class="text-md font-semibold text-white mb-2">Elementos Táticos</h5>
                            <div class="flex flex-wrap gap-2">
                                ${board.tacticalElements.map(el => `<span class="px-2 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs">${el}</span>`).join('')}
                            </div>
                        </div>
                        
                        <div>
                            <h5 class="text-md font-semibold text-white mb-2">Elementos Estratégicos</h5>
                            <div class="flex flex-wrap gap-2">
                                ${board.strategicElements.map(el => `<span class="px-2 py-1 bg-purple-500/20 text-purple-400 rounded-full text-xs">${el}</span>`).join('')}
                            </div>
                        </div>
                        
                        <div class="flex items-center justify-between text-sm">
                            <span class="text-gray-400">Avaliação: ${board.rating}/5</span>
                            <span class="text-gray-400">${board.plays} jogos</span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        boardContainer.innerHTML = boardHTML;

        // Inicializar o tabuleiro
        this.initializeChessBoard(board.id, board.fen);
    }

    generateComplexityStars(complexity) {
        const levels = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'very-high': 4
        };

        const stars = levels[complexity] || 2;
        return Array.from({
                length: 4
            }, (_, i) =>
            `<i class="fas fa-star ${i < stars ? 'text-yellow-500' : 'text-gray-600'}"></i>`
        ).join('');
    }

    initializeChessBoard(boardId, fen) {
        // Aguardar o DOM estar pronto
        setTimeout(() => {
            const boardElement = document.getElementById(boardId);
            if (boardElement && boardElement.setPosition) {
                boardElement.setPosition(fen);
            }
        }, 100);
    }

    updateBoardGallery() {
        const gallery = document.getElementById('ai-boards-gallery');
        if (!gallery) return;

        const recentBoards = this.generatedBoards.slice(0, 6); // Mostrar 6 mais recentes

        const galleryHTML = recentBoards.map(board => `
            <div class="ai-board-mini-card bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4 hover:border-[#3a3a3a] transition-all cursor-pointer" onclick="aiBoardGenerator.displayGeneratedBoard(${JSON.stringify(board)})">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs px-2 py-1 bg-blue-500/20 text-blue-400 rounded-full">${this.themes[board.theme].name}</span>
                    <span class="text-xs text-gray-400">${this.formatDate(board.createdAt)}</span>
                </div>
                
                <div class="w-20 h-20 bg-[#0f0f0f] border border-[#2a2a2a] rounded mb-3">
                    <!-- Mini tabuleiro será renderizado aqui -->
                </div>
                
                <div class="text-center">
                    <div class="text-sm font-medium text-white mb-1">${board.description.substring(0, 30)}...</div>
                    <div class="flex items-center justify-center space-x-1 text-xs text-gray-400">
                        <i class="fas fa-star text-yellow-500"></i>
                        <span>${board.rating}</span>
                        <i class="fas fa-heart text-red-500 ml-2"></i>
                        <span>${board.likes}</span>
                    </div>
                </div>
            </div>
        `).join('');

        gallery.innerHTML = galleryHTML;
    }

    updateThemeInfo() {
        const themeInfo = document.getElementById('theme-info');
        if (!themeInfo) return;

        const theme = this.themes[this.currentTheme];
        themeInfo.innerHTML = `
            <div class="bg-[#1a1a1a] border border-[#2a2a2a] rounded-lg p-4">
                <h4 class="text-lg font-semibold text-white mb-2">${theme.name}</h4>
                <p class="text-gray-300 text-sm mb-3">${theme.description}</p>
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <div>
                        <span class="text-gray-400">Complexidade:</span>
                        <span class="text-white ml-2">${theme.complexity}</span>
                    </div>
                    <div>
                        <span class="text-gray-400">Criatividade:</span>
                        <span class="text-white ml-2">${theme.creativity}</span>
                    </div>
                </div>
            </div>
        `;
    }

    playBoard(boardId) {
        const board = this.generatedBoards.find(b => b.id === boardId);
        if (!board) return;

        // Implementar lógica de jogo
        console.log('Jogando tabuleiro:', board);

        // Atualizar estatísticas
        board.plays++;
        this.saveGeneratedBoards();

        // Notificar sucesso
        this.showNotification('Tabuleiro carregado para jogo!', 'success');
    }

    analyzeBoard(boardId) {
        const board = this.generatedBoards.find(b => b.id === boardId);
        if (!board) return;

        // Implementar análise da IA
        console.log('Analisando tabuleiro:', board);

        // Mostrar análise
        this.showNotification('Análise iniciada!', 'info');
    }

    saveBoard(boardId) {
        const board = this.generatedBoards.find(b => b.id === boardId);
        if (!board) return;

        // Implementar sistema de favoritos
        board.likes++;
        this.saveGeneratedBoards();

        // Notificar sucesso
        this.showNotification('Tabuleiro salvo nos favoritos!', 'success');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white z-50 transition-all duration-300 ${
            type === 'success' ? 'bg-green-600' : 
            type === 'error' ? 'bg-red-600' : 
            'bg-blue-600'
        }`;
        notification.innerHTML = message;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    generateId() {
        return 'board_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit'
        });
    }

    saveGeneratedBoards() {
        localStorage.setItem('aiGeneratedBoards', JSON.stringify(this.generatedBoards));
    }

    loadGeneratedBoards() {
        const saved = localStorage.getItem('aiGeneratedBoards');
        if (saved) {
            this.generatedBoards = JSON.parse(saved);
        }
    }
}

// Inicializar o gerador quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
            window.aiBoardGenerator = new AIBoardGenerator();