/**
 * 🧠 Smart Chess Board - Sistema Inteligente de Tabuleiro
 * Interface fluida e intuitiva para a base de dados Pro
 * 
 * Funcionalidades:
 * - Navegação inteligente por categorias
 * - Demonstração automática contextual
 * - Interface minimalista e eficiente
 * - Integração perfeita com ARKITECT
 * - Sistema de aprendizado adaptativo
 * 
 * @author AEON CHESS Team
 * @version 2.0.0
 * @date Janeiro 2025
 */

class SmartChessBoard {
    constructor() {
        this.name = 'Smart Chess Board';
        this.version = '2.0.0';
        this.board = null;
        this.database = null;
        this.currentPosition = null;
        this.currentCategory = 'openings';
        this.autoDemo = false;
        this.demoInterval = null;
        this.arkitectActive = false;
        this.learningMode = false;
        this.positionHistory = [];
        this.currentIndex = 0;

        console.log(`🧠 ${this.name} v${this.version} inicializando...`);
        this.init();
    }

    async init() {
        // Aguardar sistemas
        await this.waitForSystems();

        // Configurar tabuleiro
        this.setupBoard();

        // Conectar base de dados
        this.connectDatabase();

        // Criar interface inteligente
        this.createSmartInterface();

        // Iniciar modo de aprendizado
        this.startLearningMode();

        console.log('🧠 Smart Chess Board ativo!');
    }

    async waitForSystems() {
        return new Promise((resolve) => {
            const checkSystems = () => {
                const boardReady = document.querySelector('#aeon-board .chess-board-wrapper');
                const databaseReady = window.chessProDB;
                const arkitectReady = window.arkitectSolution;

                if (boardReady && databaseReady && arkitectReady) {
                    this.board = document.querySelector('#aeon-board');
                    this.database = window.chessProDB;
                    console.log('🧠 Todos os sistemas prontos');
                    resolve();
                } else {
                    setTimeout(checkSystems, 100);
                }
            };
            checkSystems();
        });
    }

    setupBoard() {
        if (!this.board) return;

        // Garantir visibilidade
        this.board.style.display = 'block';
        this.board.style.visibility = 'visible';
        this.board.style.opacity = '1';
        this.board.style.width = '100%';
        this.board.style.aspectRatio = '1 / 1';

        // Ajustar wrapper
        const wrapper = this.board.querySelector('.chess-board-wrapper');
        if (wrapper) {
            wrapper.style.width = '100%';
            wrapper.style.height = '100%';
        }

        console.log('🧠 Tabuleiro configurado');
    }

    connectDatabase() {
        if (!this.database) return;

        // Expor métodos no tabuleiro
        this.board.loadPosition = (position) => this.loadPosition(position);
        this.board.nextPosition = () => this.nextPosition();
        this.board.prevPosition = () => this.prevPosition();
        this.board.toggleDemo = () => this.toggleAutoDemo();
        this.board.toggleArkitect = () => this.toggleArkitect();

        console.log('🧠 Base de dados conectada:', this.database.getStatistics());
    }

    createSmartInterface() {
        const heroBoard = document.querySelector('.hero-chess-board');
        if (!heroBoard) return;

        // Remover interfaces antigas
        this.removeOldInterfaces();

        // Criar interface inteligente
        const smartInterface = document.createElement('div');
        smartInterface.className = 'smart-interface';
        smartInterface.innerHTML = `
            <div class="smart-header">
                <div class="smart-title">
                    <h4>🧠 Smart Chess Pro</h4>
                    <div class="smart-stats">${this.database.totalPositions} posições</div>
                </div>
                <div class="smart-controls">
                    <button id="smart-prev" class="smart-btn" title="Posição Anterior">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button id="smart-play" class="smart-btn" title="Demonstração Automática">
                        <i class="fas fa-play"></i>
                    </button>
                    <button id="smart-next" class="smart-btn" title="Próxima Posição">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                    <button id="smart-arkitect" class="smart-btn" title="Análise ARKITECT">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
            
            <div class="smart-categories">
                <button class="category-btn active" data-category="openings">
                    <i class="fas fa-chess-king"></i>
                    <span>Aberturas</span>
                </button>
                <button class="category-btn" data-category="tacticalPatterns">
                    <i class="fas fa-bolt"></i>
                    <span>Táticas</span>
                </button>
                <button class="category-btn" data-category="classicEndgames">
                    <i class="fas fa-flag-checkered"></i>
                    <span>Finais</span>
                </button>
                <button class="category-btn" data-category="historicalPositions">
                    <i class="fas fa-landmark"></i>
                    <span>Histórico</span>
                </button>
                <button class="category-btn" data-category="grandmasterGames">
                    <i class="fas fa-crown"></i>
                    <span>Mestres</span>
                </button>
            </div>

            <div class="smart-info">
                <div id="smart-position-title" class="position-title">Carregando posição...</div>
                <div id="smart-position-desc" class="position-desc"></div>
                <div id="smart-position-analysis" class="position-analysis"></div>
            </div>

            <div class="smart-progress">
                <div class="progress-bar">
                    <div id="smart-progress-fill" class="progress-fill"></div>
                </div>
                <div class="progress-text">
                    <span id="smart-position-counter">0/0</span>
                </div>
            </div>
        `;

        heroBoard.appendChild(smartInterface);
        this.addSmartCSS();
        this.setupSmartEvents();

        console.log('🧠 Interface inteligente criada');
    }

    removeOldInterfaces() {
        const oldInterfaces = document.querySelectorAll('.consolidated-interface, .pro-database-controls, .ai-control-panel');
        oldInterfaces.forEach(interface => interface.remove());
    }

    setupSmartEvents() {
        // Controles de navegação
        document.getElementById('smart-prev') ? .addEventListener('click', () => this.prevPosition());
        document.getElementById('smart-next') ? .addEventListener('click', () => this.nextPosition());
        document.getElementById('smart-play') ? .addEventListener('click', () => this.toggleAutoDemo());
        document.getElementById('smart-arkitect') ? .addEventListener('click', () => this.toggleArkitect());

        // Categorias
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const category = e.currentTarget.dataset.category;
                this.changeCategory(category);

                // Atualizar botões ativos
                document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        // Conectar botão "Iniciar Aprendizado" existente
        const learningButton = document.getElementById('learning-play-pause');
        if (learningButton) {
            learningButton.addEventListener('click', () => {
                console.log('🧠 Botão "Iniciar Aprendizado" clicado');
                this.toggleAutoDemo();

                // Atualizar texto do botão
                if (this.autoDemo) {
                    learningButton.innerHTML = '<i class="fas fa-pause mr-2"></i>Pausar Aprendizado';
                    learningButton.classList.remove('from-blue-600', 'to-purple-600');
                    learningButton.classList.add('from-yellow-600', 'to-orange-600');
                } else {
                    learningButton.innerHTML = '<i class="fas fa-play mr-2"></i>Iniciar Aprendizado';
                    learningButton.classList.remove('from-yellow-600', 'to-orange-600');
                    learningButton.classList.add('from-blue-600', 'to-purple-600');
                }
            });
            console.log('🧠 Botão "Iniciar Aprendizado" conectado');
        }

        // Conectar seletor de modo de aprendizado
        const learningModeSelect = document.getElementById('learning-mode');
        if (learningModeSelect) {
            learningModeSelect.addEventListener('change', (e) => {
                const mode = e.target.value;
                console.log('🧠 Modo de aprendizado alterado para:', mode);

                // Mapear modos para categorias
                const modeToCategory = {
                    'openings': 'openings',
                    'tactics': 'tacticalPatterns',
                    'endgames': 'classicEndgames',
                    'strategy': 'aiAnalysis',
                    'history': 'historicalPositions'
                };

                if (modeToCategory[mode]) {
                    this.changeCategory(modeToCategory[mode]);
                }
            });
            console.log('🧠 Seletor de modo de aprendizado conectado');
        }

        console.log('🧠 Eventos inteligentes configurados');
    }

    changeCategory(category) {
        if (!this.database) {
            console.error('🧠 Base de dados não disponível para mudança de categoria');
            return;
        }

        this.currentCategory = category;
        this.currentIndex = 0;
        this.positionHistory = this.getAllPositions(category);

        console.log(`🧠 Categoria alterada para: ${category} (${this.positionHistory.length} posições)`);

        if (this.positionHistory.length > 0) {
            this.loadCurrentPosition();
        } else {
            console.error(`🧠 Nenhuma posição encontrada para categoria: ${category}`);
        }
    }

    getAllPositions(category) {
        if (!this.database) {
            console.error('🧠 Base de dados não disponível para getAllPositions');
            return [];
        }

        const categoryData = this.database[category];
        if (!categoryData) {
            console.error(`🧠 Categoria ${category} não encontrada na base de dados`);
            return [];
        }

        if (!categoryData.subcategories) {
            console.error(`🧠 Subcategorias não encontradas para ${category}`);
            return [];
        }

        const allPositions = [];
        let totalSubcategories = 0;
        let totalPositions = 0;

        Object.values(categoryData.subcategories).forEach(subcategory => {
            totalSubcategories++;
            if (subcategory.positions && Array.isArray(subcategory.positions)) {
                allPositions.push(...subcategory.positions);
                totalPositions += subcategory.positions.length;
            }
        });

        console.log(`🧠 Categoria ${category}: ${totalSubcategories} subcategorias, ${totalPositions} posições`);
        return allPositions;
    }

    loadCurrentPosition() {
        if (this.positionHistory.length === 0) return;

        const position = this.positionHistory[this.currentIndex];
        this.loadPosition(position);
        this.updateProgress();
    }

    nextPosition() {
        if (this.positionHistory.length === 0) return;

        this.currentIndex = (this.currentIndex + 1) % this.positionHistory.length;
        this.loadCurrentPosition();
    }

    prevPosition() {
        if (this.positionHistory.length === 0) return;

        this.currentIndex = this.currentIndex === 0 ?
            this.positionHistory.length - 1 : this.currentIndex - 1;
        this.loadCurrentPosition();
    }

    loadPosition(position) {
        this.currentPosition = position;

        // Atualizar tabuleiro
        if (this.board && position.fen) {
            try {
                if (this.board.setPosition) {
                    this.board.setPosition(position.fen);
                } else if (this.board.position) {
                    this.board.position = position.fen;
                }
            } catch (error) {
                console.warn('🧠 Erro ao atualizar tabuleiro:', error);
            }
        }

        // Atualizar interface
        this.updateSmartInterface(position);

        console.log('🧠 Posição carregada:', position.name || position.fen);
    }

    updateSmartInterface(position) {
        const titleEl = document.getElementById('smart-position-title');
        const descEl = document.getElementById('smart-position-desc');
        const analysisEl = document.getElementById('smart-position-analysis');

        if (titleEl) {
            titleEl.textContent = position.name || 'Posição Profissional';
        }

        if (descEl) {
            let description = '';
            if (position.description) description += position.description;
            if (position.themes) description += ` • Temas: ${position.themes.join(', ')}`;
            if (position.level) description += ` • Nível: ${position.level}`;

            descEl.textContent = description || 'Análise profissional disponível';
        }

        if (analysisEl) {
            let analysis = '';
            if (position.aiNotes) analysis += `🧠 ${position.aiNotes}`;
            if (position.evaluation) analysis += ` • Avaliação: ${position.evaluation}`;
            if (position.explanation) analysis += ` • ${position.explanation}`;

            analysisEl.textContent = analysis || 'Análise disponível';
        }
    }

    updateProgress() {
        const progressFill = document.getElementById('smart-progress-fill');
        const positionCounter = document.getElementById('smart-position-counter');

        if (progressFill && this.positionHistory.length > 0) {
            const progress = ((this.currentIndex + 1) / this.positionHistory.length) * 100;
            progressFill.style.width = `${progress}%`;
        }

        if (positionCounter) {
            positionCounter.textContent = `${this.currentIndex + 1}/${this.positionHistory.length}`;
        }
    }

    toggleAutoDemo() {
        console.log('🧠 Alternando demonstração automática...');

        if (this.autoDemo) {
            this.stopAutoDemo();
            console.log('🧠 Demonstração automática parada');
        } else {
            // Verificar se há posições disponíveis
            if (this.positionHistory.length === 0) {
                console.log('🧠 Nenhuma posição disponível, carregando aberturas...');
                this.changeCategory('openings');
            }

            this.startAutoDemo();
            console.log('🧠 Demonstração automática iniciada');
        }
    }

    startAutoDemo() {
        if (this.autoDemo) {
            console.log('🧠 Demonstração automática já está ativa');
            return;
        }

        // Verificar se há posições disponíveis
        if (this.positionHistory.length === 0) {
            console.error('🧠 Nenhuma posição disponível para demonstração');
            return;
        }

        this.autoDemo = true;
        this.demoInterval = setInterval(() => {
            console.log('🧠 Avançando para próxima posição...');
            this.nextPosition();
        }, 8000); // 8 segundos por posição

        console.log('🧠 Demonstração automática iniciada com', this.positionHistory.length, 'posições');
    }

    stopAutoDemo() {
        this.autoDemo = false;

        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        console.log('🧠 Demonstração automática parada');
    }

    toggleArkitect() {
        const button = document.getElementById('smart-arkitect');

        if (this.arkitectActive) {
            if (window.arkitectSolution) {
                window.arkitectSolution.stop();
            }
            this.arkitectActive = false;
            if (button) {
                button.innerHTML = '<i class="fas fa-eye"></i>';
                button.classList.remove('active');
            }
        } else {
            if (window.arkitectSolution) {
                window.arkitectSolution.start();
            }
            this.arkitectActive = true;
            if (button) {
                button.innerHTML = '<i class="fas fa-eye-slash"></i>';
                button.classList.add('active');
            }
        }
    }

    startLearningMode() {
        // Garantir que a base de dados está carregada
        if (!this.database) {
            console.error('🧠 Base de dados não disponível para modo de aprendizado');
            return;
        }

        // Inicializar com aberturas
        this.changeCategory('openings');

        // Verificar se as posições foram carregadas
        if (this.positionHistory.length === 0) {
            console.error('🧠 Nenhuma posição carregada para automação');
            return;
        }

        // Iniciar demonstração automática após 3 segundos
        setTimeout(() => {
            console.log('🧠 Iniciando demonstração automática...');
            this.startAutoDemo();
        }, 3000);

        console.log('🧠 Modo de aprendizado iniciado com', this.positionHistory.length, 'posições');
    }

    addSmartCSS() {
        if (document.getElementById('smart-css')) return;

        const style = document.createElement('style');
        style.id = 'smart-css';
        style.textContent = `
            .smart-interface {
                margin-top: 20px;
                padding: 20px;
                background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
                border: 1px solid #333;
                border-radius: 16px;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            }

            .smart-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px solid #333;
            }

            .smart-title {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .smart-title h4 {
                margin: 0;
                color: #fff;
                font-size: 16px;
                font-weight: 600;
            }

            .smart-stats {
                font-size: 12px;
                color: #888;
                padding: 4px 10px;
                background: #333;
                border-radius: 6px;
            }

            .smart-controls {
                display: flex;
                gap: 8px;
            }

            .smart-btn {
                width: 40px;
                height: 40px;
                background: #333;
                border: 1px solid #444;
                border-radius: 8px;
                color: #fff;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .smart-btn:hover {
                background: #444;
                border-color: #555;
                transform: translateY(-1px);
            }

            .smart-btn.active {
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                border-color: #3b82f6;
            }

            .smart-categories {
                display: flex;
                gap: 8px;
                margin-bottom: 16px;
                flex-wrap: wrap;
            }

            .category-btn {
                flex: 1;
                min-width: 100px;
                padding: 10px 12px;
                background: #333;
                border: 1px solid #444;
                border-radius: 8px;
                color: #fff;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 12px;
            }

            .category-btn:hover {
                background: #444;
                border-color: #555;
            }

            .category-btn.active {
                background: linear-gradient(135deg, #10b981, #059669);
                border-color: #10b981;
            }

            .smart-info {
                padding: 16px;
                background: #0f0f0f;
                border: 1px solid #333;
                border-radius: 8px;
                margin-bottom: 16px;
            }

            .position-title {
                color: #fff;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
            }

            .position-desc {
                color: #ccc;
                font-size: 14px;
                line-height: 1.4;
                margin-bottom: 8px;
            }

            .position-analysis {
                color: #3b82f6;
                font-size: 12px;
                font-style: italic;
                line-height: 1.3;
            }

            .smart-progress {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .progress-bar {
                flex: 1;
                height: 6px;
                background: #333;
                border-radius: 3px;
                overflow: hidden;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #10b981, #3b82f6);
                width: 0%;
                transition: width 0.3s ease;
            }

            .progress-text {
                font-size: 12px;
                color: #888;
                min-width: 50px;
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }

    getStatus() {
        return {
            name: this.name,
            version: this.version,
            board: this.board ? '✅' : '❌',
            database: this.database ? '✅' : '❌',
            autoDemo: this.autoDemo,
            arkitectActive: this.arkitectActive,
            currentCategory: this.currentCategory,
            currentPosition: this.currentPosition ? .name || 'Nenhuma',
            totalPositions: this.positionHistory.length,
            currentIndex: this.currentIndex
        };
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.SmartChessBoard = SmartChessBoard;

    // Inicializar automaticamente
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🧠 Inicializando Smart Chess Board...');
        window.smartChessBoard = new SmartChessBoard();
    });
}

console.log('🧠 Smart Chess Board carregado');