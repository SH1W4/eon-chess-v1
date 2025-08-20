/**
 * 🎯 Chess Learning System - Sistema de Aprendizado Automático
 * Demonstra conceitos de xadrez automaticamente usando a base de dados Pro
 * 
 * Funcionalidades:
 * - Demonstração automática de aberturas, táticas, finais
 * - Integração com base de dados Pro
 * - Controles de velocidade e modo
 * - Progresso visual da demonstração
 * - Análise em tempo real
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class ChessLearningSystem {
    constructor() {
        this.name = 'Chess Learning System';
        this.version = '1.0.0';
        this.isActive = false;
        this.currentMode = 'openings';
        this.currentSpeed = 'normal';
        this.currentStep = 0;
        this.totalSteps = 6;
        this.demoInterval = null;
        this.currentPosition = null;

        // Configurações de velocidade
        this.speedConfig = {
            slow: 8000, // 8 segundos
            normal: 6000, // 6 segundos
            fast: 4000 // 4 segundos
        };

        // Estados de demonstração
        this.demoStates = {
            playing: false,
            paused: false,
            stopped: true
        };

        // Elementos do DOM
        this.elements = {
            learningMode: null,
            learningSpeed: null,
            playPauseBtn: null,
            learningInfo: null,
            learningProgress: null,
            board: null
        };

        console.log(`🎯 ${this.name} v${this.version} inicializando...`);
        this.init();
    }

    async init() {
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.delayedInit();
            });
        } else {
            this.delayedInit();
        }
    }

    delayedInit() {
        console.log('🎯 Iniciando sistema de aprendizado...');

        // Aguardar base de dados Pro carregar
        this.waitForProDatabase().then(() => {
            this.setupElements();
            this.setupEventListeners();
            this.loadInitialPosition();
            console.log('🎯 Sistema de aprendizado ativo!');
        });
    }

    async waitForProDatabase() {
        return new Promise((resolve) => {
            const checkDatabase = () => {
                if (window.chessProDB) {
                    console.log('🎯 Base de dados Pro conectada:', window.chessProDB.getStatistics());
                    resolve();
                } else {
                    setTimeout(checkDatabase, 100);
                }
            };
            checkDatabase();
        });
    }

    setupElements() {
        this.elements.learningMode = document.getElementById('learning-mode');
        this.elements.learningSpeed = document.getElementById('learning-speed');
        this.elements.playPauseBtn = document.getElementById('learning-play-pause');
        this.elements.learningInfo = document.getElementById('learning-info');
        this.elements.learningProgress = document.getElementById('learning-progress');
        this.elements.board = document.getElementById('aeon-board');

        if (!this.elements.board) {
            console.warn('🎯 Tabuleiro não encontrado!');
        }
    }

    setupEventListeners() {
        // Seletor de modo
        if (this.elements.learningMode) {
            this.elements.learningMode.addEventListener('change', (e) => {
                this.currentMode = e.target.value;
                this.loadModePositions();
                console.log('🎯 Modo alterado para:', this.currentMode);
            });
        }

        // Seletor de velocidade
        if (this.elements.learningSpeed) {
            this.elements.learningSpeed.addEventListener('change', (e) => {
                this.currentSpeed = e.target.value;
                this.updateDemoSpeed();
                console.log('🎯 Velocidade alterada para:', this.currentSpeed);
            });
        }

        // Botão play/pause
        if (this.elements.playPauseBtn) {
            this.elements.playPauseBtn.addEventListener('click', () => {
                this.togglePlayPause();
            });
        }
    }

    loadInitialPosition() {
        // Carregar primeira posição baseada no modo atual
        this.loadModePositions();

        // Iniciar demonstração automática após 10 segundos (mais lento)
        setTimeout(() => {
            this.startDemo();
        }, 10000);
    }

    loadModePositions() {
        if (!window.chessProDB) return;

        const modeMap = {
            'openings': 'openings',
            'tactics': 'tacticalPatterns',
            'endgames': 'classicEndgames',
            'strategy': 'aiAnalysis',
            'history': 'historicalPositions'
        };

        const category = modeMap[this.currentMode];
        if (category) {
            this.loadCategoryPositions(category);
        }
    }

    loadCategoryPositions(category) {
        const categoryData = window.chessProDB[category];
        if (!categoryData) return;

        console.log(`🎯 Carregando posições de ${categoryData.category}...`);

        // Coletar todas as posições da categoria
        this.availablePositions = [];
        Object.values(categoryData.subcategories).forEach(subcategory => {
            if (subcategory.positions) {
                this.availablePositions.push(...subcategory.positions);
            }
        });

        console.log(`🎯 ${this.availablePositions.length} posições carregadas para demonstração`);

        // Atualizar interface
        this.updateLearningInfo();
    }

    updateLearningInfo() {
        if (!this.elements.learningInfo) return;

        const modeNames = {
            'openings': 'Aberturas',
            'tactics': 'Táticas',
            'endgames': 'Finais',
            'strategy': 'Estratégia',
            'history': 'História'
        };

        const modeName = modeNames[this.currentMode] || this.currentMode;
        const positionCount = this.availablePositions ? this.availablePositions.length : 0;

        this.elements.learningInfo.innerHTML = `
            <h4 class="text-lg font-semibold text-white mb-2">🎯 ${modeName}</h4>
            <p class="text-gray-300 text-sm">${positionCount} posições disponíveis para aprendizado</p>
        `;
    }

    startDemo() {
        if (this.demoStates.playing) return;

        this.demoStates.playing = true;
        this.demoStates.stopped = false;
        this.demoStates.paused = false;

        // Atualizar botão
        if (this.elements.playPauseBtn) {
            this.elements.playPauseBtn.innerHTML = '<i class="fas fa-pause mr-2"></i>Pausar Aprendizado';
            this.elements.playPauseBtn.classList.add('bg-gradient-to-r', 'from-red-600', 'to-pink-600');
            this.elements.playPauseBtn.classList.remove('from-blue-600', 'to-purple-600');
        }

        // Iniciar demonstração
        this.runDemoStep();

        console.log('🎯 Demonstração iniciada');
    }

    pauseDemo() {
        if (!this.demoStates.playing) return;

        this.demoStates.playing = false;
        this.demoStates.paused = true;

        // Parar intervalo
        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        // Atualizar botão
        if (this.elements.playPauseBtn) {
            this.elements.playPauseBtn.innerHTML = '<i class="fas fa-play mr-2"></i>Continuar Aprendizado';
            this.elements.playPauseBtn.classList.remove('bg-gradient-to-r', 'from-red-600', 'to-pink-600');
            this.elements.playPauseBtn.classList.add('from-blue-600', 'to-purple-600');
        }

        console.log('🎯 Demonstração pausada');
    }

    stopDemo() {
        this.demoStates.playing = false;
        this.demoStates.paused = false;
        this.demoStates.stopped = true;
        this.currentStep = 0;

        // Parar intervalo
        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        // Atualizar botão
        if (this.elements.playPauseBtn) {
            this.elements.playPauseBtn.innerHTML = '<i class="fas fa-play mr-2"></i>Iniciar Aprendizado';
            this.elements.playPauseBtn.classList.remove('bg-gradient-to-r', 'from-red-600', 'to-pink-600');
            this.elements.playPauseBtn.classList.add('from-blue-600', 'to-purple-700');
        }

        // Resetar progresso
        this.updateProgress(0);

        console.log('🎯 Demonstração parada');
    }

    togglePlayPause() {
        if (this.demoStates.stopped) {
            this.startDemo();
        } else if (this.demoStates.playing) {
            this.pauseDemo();
        } else if (this.demoStates.paused) {
            this.startDemo();
        }
    }

    runDemoStep() {
        if (!this.demoStates.playing) return;

        // Carregar próxima posição
        this.loadNextPosition();

        // Atualizar progresso
        this.currentStep++;
        this.updateProgress(this.currentStep);

        // Verificar se chegou ao final
        if (this.currentStep >= this.totalSteps) {
            this.completeDemo();
            return;
        }

        // Agendar próximo passo
        const speed = this.speedConfig[this.currentSpeed];
        this.demoInterval = setTimeout(() => {
            this.runDemoStep();
        }, speed);
    }

    loadNextPosition() {
        if (!this.availablePositions || this.availablePositions.length === 0) return;

        // Selecionar posição (por enquanto, usar a primeira)
        const position = this.availablePositions[0];
        this.currentPosition = position;

        // Atualizar tabuleiro
        this.updateBoard(position);

        // Atualizar informações
        this.updatePositionInfo(position);

        console.log('🎯 Nova posição carregada:', position.name || position.fen);
    }

    updateBoard(position) {
        if (!this.elements.board || !position.fen) return;

        try {
            // Tentar definir posição
            if (this.elements.board.setPosition) {
                this.elements.board.setPosition(position.fen);
            } else if (this.elements.board.position) {
                this.elements.board.position = position.fen;
            } else {
                this.elements.board.setAttribute('position', position.fen);
            }
        } catch (error) {
            console.warn('🎯 Erro ao atualizar tabuleiro:', error);
        }
    }

    updatePositionInfo(position) {
        if (!this.elements.learningInfo) return;

        let description = '';
        if (position.description) description += position.description;
        if (position.themes) description += ` • Temas: ${position.themes.join(', ')}`;
        if (position.level) description += ` • Nível: ${position.level}`;

        this.elements.learningInfo.innerHTML = `
            <h4 class="text-lg font-semibold text-white mb-2">🎯 ${position.name || 'Posição de Aprendizado'}</h4>
            <p class="text-gray-300 text-sm">${description || 'Conceito sendo demonstrado'}</p>
        `;
    }

    updateProgress(step) {
        if (!this.elements.learningProgress) return;

        const percentage = (step / this.totalSteps) * 100;

        this.elements.learningProgress.innerHTML = `
            <span class="text-sm text-gray-400">Passo ${step} de ${this.totalSteps}</span>
            <div class="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div class="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300" style="width: ${percentage}%"></div>
            </div>
        `;
    }

    completeDemo() {
        console.log('🎯 Demonstração concluída!');

        // Mostrar mensagem de conclusão
        if (this.elements.learningInfo) {
            this.elements.learningInfo.innerHTML = `
                <h4 class="text-lg font-semibold text-white mb-2">🎉 Aprendizado Concluído!</h4>
                <p class="text-gray-300 text-sm">Você explorou conceitos fundamentais de ${this.currentMode}</p>
            `;
        }

        // Parar demonstração
        this.stopDemo();

        // Reiniciar automaticamente após 5 segundos
        setTimeout(() => {
            this.currentStep = 0;
            this.startDemo();
        }, 5000);
    }

    updateDemoSpeed() {
        if (this.demoStates.playing) {
            // Reiniciar com nova velocidade
            this.pauseDemo();
            setTimeout(() => {
                this.startDemo();
            }, 100);
        }
    }

    // API pública
    getCurrentMode() {
        return this.currentMode;
    }

    getCurrentSpeed() {
        return this.currentSpeed;
    }

    getCurrentPosition() {
        return this.currentPosition;
    }

    isPlaying() {
        return this.demoStates.playing;
    }

    // Métodos para integração
    setMode(mode) {
        this.currentMode = mode;
        this.loadModePositions();
    }

    setSpeed(speed) {
        this.currentSpeed = speed;
        this.updateDemoSpeed();
    }

    forceStart() {
        this.startDemo();
    }

    forceStop() {
        this.stopDemo();
    }
}

// Disponibilizar globalmente
if (typeof window !== 'undefined') {
    window.ChessLearningSystem = ChessLearningSystem;

    // Inicializar automaticamente quando DOM estiver pronto
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => {
            window.chessLearningSystem = new ChessLearningSystem();
        }, 1000);
    });
}

// Exportar para módulos (se suportado)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChessLearningSystem;
}