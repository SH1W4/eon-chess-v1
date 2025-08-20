/**
 * 🎯 Chess Board Consolidation - Consolidação do Tabuleiro 1
 * Sistema unificado para o primeiro tabuleiro com base de dados Pro
 * 
 * Funcionalidades:
 * - Integração completa com base de dados Pro
 * - Remoção de elementos desnecessários
 * - Sistema de demonstração automática
 * - Efeito ARKITECT integrado
 * - Interface limpa e funcional
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class ChessBoardConsolidation {
    constructor() {
        this.name = 'Chess Board Consolidation';
        this.version = '1.0.0';
        this.board = null;
        this.database = null;
        this.currentPosition = null;
        this.autoDemo = false;
        this.demoInterval = null;
        this.arkitectActive = false;

        console.log(`🎯 ${this.name} v${this.version} inicializando...`);
        this.init();
    }

    async init() {
        // Aguardar carregamento dos sistemas
        await this.waitForSystems();

        // Configurar tabuleiro
        this.setupBoard();

        // Conectar base de dados
        this.connectDatabase();

        // Configurar interface
        this.setupInterface();

        // Iniciar demonstração automática
        this.startAutoDemo();

        console.log('🎯 Tabuleiro 1 consolidado e ativo!');
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
                    console.log('🎯 Todos os sistemas prontos');
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

        // Garantir que o tabuleiro esteja visível
        this.board.style.display = 'block';
        this.board.style.visibility = 'visible';
        this.board.style.opacity = '1';
        this.board.style.width = '100%';
        this.board.style.aspectRatio = '1 / 1';

        // Ajustar wrapper se necessário
        const wrapper = this.board.querySelector('.chess-board-wrapper');
        if (wrapper) {
            wrapper.style.width = '100%';
            wrapper.style.height = '100%';
        }

        console.log('🎯 Tabuleiro configurado');
    }

    connectDatabase() {
        if (!this.database) return;

        // Expor métodos de atualização no tabuleiro
        this.board.loadPosition = (position) => this.loadPosition(position);
        this.board.loadRandomPosition = () => this.loadRandomPosition();
        this.board.toggleDemo = () => this.toggleAutoDemo();

        console.log('🎯 Base de dados conectada:', this.database.getStatistics());
    }

    setupInterface() {
        // Remover elementos desnecessários
        this.removeUnnecessaryElements();

        // Criar interface limpa
        this.createCleanInterface();

        // Configurar eventos
        this.setupEventListeners();
    }

    removeUnnecessaryElements() {
        // Remover barra de avaliação lateral
        const evalBar = document.querySelector('[aria-label="Barra de avaliação"]');
        if (evalBar) {
            evalBar.remove();
        }

        // Remover avaliação de posição
        const positionEval = document.getElementById('position-evaluation');
        if (positionEval) {
            positionEval.closest('.bg-[#0f0f0f]') ? .remove();
        }

        // Remover controles antigos
        const oldControls = document.querySelectorAll('.pro-database-controls, .ai-control-panel');
        oldControls.forEach(control => control.remove());

        console.log('🎯 Elementos desnecessários removidos');
    }

    createCleanInterface() {
        const heroBoard = document.querySelector('.hero-chess-board');
        if (!heroBoard) return;

        // Criar interface consolidada
        const interfaceContainer = document.createElement('div');
        interfaceContainer.className = 'consolidated-interface';
        interfaceContainer.innerHTML = `
            <div class="interface-header">
                <h4>🎯 Base de Dados Pro</h4>
                <div class="interface-stats">
                    <span>${this.database.totalPositions} posições</span>
                </div>
            </div>
            
            <div class="interface-controls">
                <select id="consolidated-category-select">
                    <option value="openings">🎯 Aberturas (${this.database.openings.total})</option>
                    <option value="tacticalPatterns">⚔️ Padrões Táticos (${this.database.tacticalPatterns.total})</option>
                    <option value="classicEndgames">🏁 Finais Clássicos (${this.database.classicEndgames.total})</option>
                    <option value="aiAnalysis">🤖 Análise de IA (${this.database.aiAnalysis.total})</option>
                    <option value="historicalPositions">🏛️ Posições Históricas (${this.database.historicalPositions.total})</option>
                    <option value="grandmasterGames">👑 Grandes Mestres (${this.database.grandmasterGames.total})</option>
                    <option value="endgameStudies">🎯 Estudos de Finais (${this.database.endgameStudies.total})</option>
                    <option value="tacticalCombinations">⚡ Combinações Táticas (${this.database.tacticalCombinations.total})</option>
                </select>
                
                <div class="interface-buttons">
                    <button id="consolidated-demo-toggle" class="interface-btn">
                        <i class="fas fa-play"></i> Demonstração Auto
                    </button>
                    <button id="consolidated-random-btn" class="interface-btn">
                        <i class="fas fa-random"></i> Aleatório
                    </button>
                    <button id="consolidated-arkitect-toggle" class="interface-btn">
                        <i class="fas fa-eye"></i> ARKITECT
                    </button>
                </div>
            </div>

            <div class="interface-info">
                <div id="consolidated-position-title" class="position-title">Selecione uma categoria...</div>
                <div id="consolidated-position-description" class="position-description"></div>
            </div>
        `;

        heroBoard.appendChild(interfaceContainer);
        this.addConsolidatedCSS();

        console.log('🎯 Interface consolidada criada');
    }

    setupEventListeners() {
        // Seletor de categoria
        const categorySelect = document.getElementById('consolidated-category-select');
        if (categorySelect) {
            categorySelect.addEventListener('change', (e) => {
                this.currentCategory = e.target.value;
                this.loadRandomPosition();
            });
        }

        // Botão de demonstração automática
        const demoToggle = document.getElementById('consolidated-demo-toggle');
        if (demoToggle) {
            demoToggle.addEventListener('click', () => this.toggleAutoDemo());
        }

        // Botão aleatório
        const randomBtn = document.getElementById('consolidated-random-btn');
        if (randomBtn) {
            randomBtn.addEventListener('click', () => this.loadRandomPosition());
        }

        // Botão ARKITECT
        const arkitectToggle = document.getElementById('consolidated-arkitect-toggle');
        if (arkitectToggle) {
            arkitectToggle.addEventListener('click', () => this.toggleArkitect());
        }

        console.log('🎯 Eventos configurados');
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
                console.warn('🎯 Erro ao atualizar tabuleiro:', error);
            }
        }

        // Atualizar interface
        this.updateInterface(position);

        console.log('🎯 Posição carregada:', position.name || position.fen);
    }

    loadRandomPosition() {
        const categoryData = this.database[this.currentCategory || 'openings'];
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

    updateInterface(position) {
        const titleEl = document.getElementById('consolidated-position-title');
        const descEl = document.getElementById('consolidated-position-description');

        if (titleEl) {
            titleEl.textContent = position.name || 'Posição Profissional';
        }

        if (descEl) {
            let description = '';
            if (position.description) description += position.description;
            if (position.themes) description += ` • Temas: ${position.themes.join(', ')}`;
            if (position.level) description += ` • Nível: ${position.level}`;
            if (position.aiNotes) description += ` • ${position.aiNotes}`;

            descEl.textContent = description || 'Análise profissional disponível';
        }
    }

    toggleAutoDemo() {
        const button = document.getElementById('consolidated-demo-toggle');

        if (this.autoDemo) {
            this.stopAutoDemo();
            if (button) {
                button.innerHTML = '<i class="fas fa-play"></i> Demonstração Auto';
                button.classList.remove('active');
            }
        } else {
            this.startAutoDemo();
            if (button) {
                button.innerHTML = '<i class="fas fa-pause"></i> Pausar Demo';
                button.classList.add('active');
            }
        }
    }

    startAutoDemo() {
        if (this.autoDemo) return;

        this.autoDemo = true;
        this.demoInterval = setInterval(() => {
            this.loadRandomPosition();
        }, 10000); // 10 segundos por posição

        console.log('🎯 Demonstração automática iniciada');
    }

    stopAutoDemo() {
        this.autoDemo = false;

        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        console.log('🎯 Demonstração automática parada');
    }

    toggleArkitect() {
        const button = document.getElementById('consolidated-arkitect-toggle');

        if (this.arkitectActive) {
            if (window.arkitectSolution) {
                window.arkitectSolution.stop();
            }
            this.arkitectActive = false;
            if (button) {
                button.innerHTML = '<i class="fas fa-eye"></i> ARKITECT';
                button.classList.remove('active');
            }
        } else {
            if (window.arkitectSolution) {
                window.arkitectSolution.start();
            }
            this.arkitectActive = true;
            if (button) {
                button.innerHTML = '<i class="fas fa-eye-slash"></i> ARKITECT';
                button.classList.add('active');
            }
        }
    }

    addConsolidatedCSS() {
        if (document.getElementById('consolidated-css')) return;

        const style = document.createElement('style');
        style.id = 'consolidated-css';
        style.textContent = `
            .consolidated-interface {
                margin-top: 20px;
                padding: 20px;
                background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
                border: 1px solid #333;
                border-radius: 16px;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            }

            .interface-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 12px;
                border-bottom: 1px solid #333;
            }

            .interface-header h4 {
                margin: 0;
                color: #fff;
                font-size: 16px;
                font-weight: 600;
            }

            .interface-stats {
                font-size: 12px;
                color: #888;
                padding: 4px 10px;
                background: #333;
                border-radius: 6px;
            }

            .interface-controls {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 16px;
            }

            #consolidated-category-select {
                width: 100%;
                padding: 10px 14px;
                background: #333;
                border: 1px solid #444;
                border-radius: 8px;
                color: #fff;
                font-size: 14px;
                cursor: pointer;
            }

            #consolidated-category-select:focus {
                outline: none;
                border-color: #555;
                box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
            }

            .interface-buttons {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }

            .interface-btn {
                flex: 1;
                min-width: 120px;
                padding: 8px 12px;
                background: #333;
                border: 1px solid #444;
                border-radius: 6px;
                color: #fff;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .interface-btn:hover {
                background: #444;
                border-color: #555;
            }

            .interface-btn.active {
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                border-color: #3b82f6;
            }

            .interface-info {
                padding: 12px;
                background: #0f0f0f;
                border: 1px solid #333;
                border-radius: 8px;
            }

            .position-title {
                color: #fff;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 8px;
            }

            .position-description {
                color: #ccc;
                font-size: 12px;
                line-height: 1.4;
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
            currentPosition: this.currentPosition ? .name || 'Nenhuma'
        };
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.ChessBoardConsolidation = ChessBoardConsolidation;

    // Inicializar automaticamente
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🎯 Inicializando consolidação do tabuleiro...');
        window.chessBoardConsolidation = new ChessBoardConsolidation();
    });
}

console.log('🎯 Chess Board Consolidation carregado');