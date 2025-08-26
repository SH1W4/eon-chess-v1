/**
 * 🔧 Chess Pro Integration - Integração da Base de Dados Pro
 * Sistema de integração entre a base de dados profissional e a interface
 * 
 * Funcionalidades:
 * - Interface de consulta à base de dados
 * - Sistema de busca e filtros
 * - Integração com o primeiro tabuleiro
 * - Modo de demonstração automática
 * - Sistema de progressão baseado na base de dados
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class ChessProIntegration {
    constructor() {
        this.name = 'Chess Pro Integration';
        this.version = '1.0.0';
        this.database = null;
        this.currentCategory = 'openings';
        this.currentPosition = null;
        this.autoDemo = false;
        this.demoInterval = null;

        console.log(`🔧 ${this.name} v${this.version} inicializando...`);
        this.init();
    }

    async init() {
        // Aguardar carregamento da base de dados
        await this.waitForDatabase();

        // Configurar interface
        this.setupInterface();

        // Iniciar modo de demonstração no primeiro tabuleiro
        this.initHeroBoardDemo();

        console.log('🔧 Chess Pro Integration ativo!');
    }

    async waitForDatabase() {
        return new Promise((resolve) => {
            const checkDatabase = () => {
                if (window.chessProDB) {
                    this.database = window.chessProDB;
                    console.log('🔧 Base de dados conectada:', this.database.getStatistics());
                    resolve();
                } else {
                    setTimeout(checkDatabase, 100);
                }
            };
            checkDatabase();
        });
    }

    setupInterface() {
        // Criar controles de categoria no primeiro tabuleiro
        this.createCategoryControls();

        // Configurar eventos
        this.setupEventListeners();
    }

    createCategoryControls() {
        const heroBoard = document.querySelector('.hero-chess-board');
        if (!heroBoard) return;

        // Remover controles existentes
        const existingControls = heroBoard.querySelector('.pro-database-controls');
        if (existingControls) {
            existingControls.remove();
        }

        // Criar novos controles
        const controlsContainer = document.createElement('div');
        controlsContainer.className = 'pro-database-controls';
        controlsContainer.innerHTML = `
            <div class="pro-controls-header">
                <h4>📚 Base de Dados Pro</h4>
                <div class="pro-stats">
                    <span>${this.database.totalPositions} posições</span>
                </div>
            </div>
            
            <div class="pro-category-selector">
                <select id="pro-category-select">
                    <option value="openings">🎯 Aberturas (${this.database.openings.total})</option>
                    <option value="tacticalPatterns">⚔️ Padrões Táticos (${this.database.tacticalPatterns.total})</option>
                    <option value="classicEndgames">🏁 Finais Clássicos (${this.database.classicEndgames.total})</option>
                    <option value="aiAnalysis">🤖 Análise de IA (${this.database.aiAnalysis.total})</option>
                    <option value="historicalPositions">🏛️ Posições Históricas (${this.database.historicalPositions.total})</option>
                    <option value="grandmasterGames">👑 Grandes Mestres (${this.database.grandmasterGames.total})</option>
                    <option value="endgameStudies">🎯 Estudos de Finais (${this.database.endgameStudies.total})</option>
                    <option value="tacticalCombinations">⚡ Combinações Táticas (${this.database.tacticalCombinations.total})</option>
                </select>
            </div>

            <div class="pro-demo-controls">
                <button id="pro-demo-toggle" class="pro-btn-primary">
                    <i class="fas fa-play"></i> Demonstração Auto
                </button>
                <button id="pro-position-next" class="pro-btn-secondary">
                    <i class="fas fa-forward"></i> Próxima
                </button>
                <button id="pro-position-random" class="pro-btn-secondary">
                    <i class="fas fa-random"></i> Aleatória
                </button>
            </div>

            <div class="pro-position-info">
                <div id="pro-position-title">Selecione uma categoria</div>
                <div id="pro-position-description">Explore nossa base de dados profissional</div>
                <div id="pro-position-analysis" class="pro-analysis-hidden"></div>
            </div>
        `;

        // Adicionar estilos
        this.addProDatabaseCSS();

        // Inserir controles
        heroBoard.appendChild(controlsContainer);
    }

    setupEventListeners() {
        // Seletor de categoria
        const categorySelect = document.getElementById('pro-category-select');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => {
                this.currentCategory = e.target.value;
                this.loadCategoryDemo();
            });
        }

        // Controles de demonstração
        const demoToggle = document.getElementById('pro-demo-toggle');
        if (demoToggle) {
            demoToggle.addEventListener('click', () => {
                this.toggleAutoDemo();
            });
        }

        const nextButton = document.getElementById('pro-position-next');
        if (nextButton) {
            nextButton.addEventListener('click', () => {
                this.loadNextPosition();
            });
        }

        const randomButton = document.getElementById('pro-position-random');
        if (randomButton) {
            randomButton.addEventListener('click', () => {
                this.loadRandomPosition();
            });
        }
    }

    initHeroBoardDemo() {
        // Carregar primeira categoria
        this.loadCategoryDemo();

        // Iniciar demonstração automática após 3 segundos
        setTimeout(() => {
            this.startAutoDemo();
        }, 3000);
    }

    loadCategoryDemo() {
        const categoryData = this.database[this.currentCategory];
        if (!categoryData) return;

        console.log(`🔧 Carregando demonstração: ${categoryData.category}`);

        // Atualizar interface
        this.updateCategoryInfo(categoryData);

        // Carregar primeira posição
        this.loadFirstPosition(categoryData);
    }

    updateCategoryInfo(categoryData) {
        const titleEl = document.getElementById('pro-position-title');
        const descEl = document.getElementById('pro-position-description');

        if (titleEl) {
            titleEl.textContent = categoryData.category;
        }

        if (descEl) {
            descEl.textContent = `${categoryData.total} posições disponíveis`;
        }
    }

    loadFirstPosition(categoryData) {
        // Encontrar primeira posição na categoria
        const firstSubcategory = Object.values(categoryData.subcategories)[0];
        if (!firstSubcategory || !firstSubcategory.positions) return;

        const firstPosition = firstSubcategory.positions[0];
        if (firstPosition) {
            this.loadPosition(firstPosition);
        }
    }

    loadPosition(position) {
        this.currentPosition = position;

        // Atualizar tabuleiro
        this.updateBoard(position);

        // Atualizar informações
        this.updatePositionInfo(position);

        console.log('🔧 Posição carregada:', position.name || position.fen);
    }

    updateBoard(position) {
        const boardElement = document.querySelector('#aeon-board');
        if (boardElement && position.fen) {
            try {
                // Tentar definir posição
                if (boardElement.setPosition) {
                    boardElement.setPosition(position.fen);
                } else if (boardElement.position) {
                    boardElement.position = position.fen;
                } else {
                    boardElement.setAttribute('position', position.fen);
                }
            } catch (error) {
                console.warn('🔧 Erro ao atualizar tabuleiro:', error);
            }
        }
    }

    updatePositionInfo(position) {
        const titleEl = document.getElementById('pro-position-title');
        const descEl = document.getElementById('pro-position-description');
        const analysisEl = document.getElementById('pro-position-analysis');

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
            if (position.aiNotes) analysis += `IA: ${position.aiNotes}`;
            if (position.evaluation) analysis += ` • Avaliação: ${position.evaluation}`;
            if (position.explanation) analysis += ` • ${position.explanation}`;

            if (analysis) {
                analysisEl.textContent = analysis;
                analysisEl.className = 'pro-analysis-visible';
            } else {
                analysisEl.className = 'pro-analysis-hidden';
            }
        }
    }

    toggleAutoDemo() {
        const button = document.getElementById('pro-demo-toggle');

        if (this.autoDemo) {
            this.stopAutoDemo();
            if (button) {
                button.innerHTML = '<i class="fas fa-play"></i> Demonstração Auto';
                button.classList.remove('pro-btn-active');
            }
        } else {
            this.startAutoDemo();
            if (button) {
                button.innerHTML = '<i class="fas fa-pause"></i> Pausar Demo';
                button.classList.add('pro-btn-active');
            }
        }
    }

    startAutoDemo() {
        if (this.autoDemo) return;

        this.autoDemo = true;

        // Trocar posição a cada 8 segundos
        this.demoInterval = setInterval(() => {
            this.loadRandomPosition();
        }, 8000);

        console.log('🔧 Demonstração automática iniciada');
    }

    stopAutoDemo() {
        this.autoDemo = false;

        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        console.log('🔧 Demonstração automática parada');
    }

    loadNextPosition() {
        // Implementar navegação sequencial
        this.loadRandomPosition(); // Por enquanto, usar aleatória
    }

    loadRandomPosition() {
        const categoryData = this.database[this.currentCategory];
        if (!categoryData || !categoryData.subcategories) return;

        // Coletar todas as posições da categoria
        const allPositions = [];
        Object.values(categoryData.subcategories).forEach(subcategory => {
            if (subcategory.positions) {
                allPositions.push(...subcategory.positions);
            }
        });

        if (allPositions.length === 0) return;

        // Selecionar posição aleatória
        const randomIndex = Math.floor(Math.random() * allPositions.length);
        const randomPosition = allPositions[randomIndex];

        this.loadPosition(randomPosition);
    }

    addProDatabaseCSS() {
        if (document.getElementById('pro-database-css')) return;

        const style = document.createElement('style');
        style.id = 'pro-database-css';
        style.textContent = `
            .pro-database-controls {
                margin-top: 16px;
                padding: 16px;
                background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
                border: 1px solid #333;
                border-radius: 12px;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }

            .pro-controls-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                padding-bottom: 8px;
                border-bottom: 1px solid #333;
            }

            .pro-controls-header h4 {
                margin: 0;
                color: #fff;
                font-size: 14px;
                font-weight: 600;
            }

            .pro-stats {
                font-size: 12px;
                color: #888;
                padding: 2px 8px;
                background: #333;
                border-radius: 4px;
            }

            .pro-category-selector {
                margin-bottom: 12px;
            }

            #pro-category-select {
                width: 100%;
                padding: 8px 12px;
                background: #333;
                border: 1px solid #444;
                border-radius: 6px;
                color: #fff;
                font-size: 12px;
                cursor: pointer;
            }

            #pro-category-select:focus {
                outline: none;
                border-color: #555;
                box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
            }

            .pro-demo-controls {
                display: flex;
                gap: 8px;
                margin-bottom: 12px;
                flex-wrap: wrap;
            }

            .pro-btn-primary,
            .pro-btn-secondary {
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 4px;
            }

            .pro-btn-primary {
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                flex: 1;
            }

            .pro-btn-primary:hover {
                background: linear-gradient(135deg, #5b52e8, #8b5cf6);
                transform: translateY(-1px);
            }

            .pro-btn-primary.pro-btn-active {
                background: linear-gradient(135deg, #ef4444, #dc2626);
            }

            .pro-btn-secondary {
                background: #333;
                color: #ccc;
                border: 1px solid #444;
            }

            .pro-btn-secondary:hover {
                background: #444;
                color: #fff;
                transform: translateY(-1px);
            }

            .pro-position-info {
                font-size: 12px;
                line-height: 1.4;
            }

            #pro-position-title {
                font-weight: 600;
                color: #fff;
                margin-bottom: 4px;
            }

            #pro-position-description {
                color: #bbb;
                margin-bottom: 8px;
            }

            #pro-position-analysis {
                padding: 8px;
                background: #2a2a2a;
                border-radius: 6px;
                color: #ddd;
                border-left: 3px solid #4f46e5;
                transition: all 0.3s ease;
            }

            .pro-analysis-hidden {
                display: none;
            }

            .pro-analysis-visible {
                display: block;
            }

            /* Responsivo */
            @media (max-width: 640px) {
                .pro-demo-controls {
                    flex-direction: column;
                }
                
                .pro-btn-primary,
                .pro-btn-secondary {
                    flex: none;
                }
            }
        `;

        document.head.appendChild(style);
    }

    // API pública para integração
    getDatabase() {
        return this.database;
    }

    getCurrentPosition() {
        return this.currentPosition;
    }

    setCategory(category) {
        this.currentCategory = category;
        this.loadCategoryDemo();
    }

    // Métodos para integração com outros sistemas
    exportCurrentPosition() {
        if (!this.currentPosition) return null;

        return {
            name: this.currentPosition.name,
            fen: this.currentPosition.fen,
            category: this.currentCategory,
            analysis: this.getCurrentAnalysis()
        };
    }

    getCurrentAnalysis() {
        if (!this.currentPosition) return null;

        return {
            evaluation: this.currentPosition.evaluation,
            themes: this.currentPosition.themes,
            aiNotes: this.currentPosition.aiNotes,
            level: this.currentPosition.level
        };
    }
}

// Disponibilizar globalmente
if (typeof window !== 'undefined') {
    window.ChessProIntegration = ChessProIntegration;

    // Inicializar automaticamente quando DOM estiver pronto
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            window.chessProIntegration = new ChessProIntegration();
        }, 2000);
    });
}

// Exportar para módulos (se suportado)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChessProIntegration;
}