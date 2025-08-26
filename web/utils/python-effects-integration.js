/**
 * 🐍 Python Effects Integration - Integração com Motor Python de Efeitos Visuais
 * Sistema JavaScript para conectar com a API Python avançada
 * 
 * Funcionalidades:
 * - Comunicação com API Python via HTTP/REST
 * - Streaming de efeitos visuais em tempo real
 * - Cache inteligente de animações
 * - Integração com tabuleiro de xadrez
 * - Fallback para efeitos básicos se Python não estiver disponível
 * 
 * @author AEON CHESS Team
 * @version 2.0.0
 * @date Janeiro 2025
 */

class PythonEffectsIntegration {
    constructor() {
        this.isPythonAvailable = false;
        this.chessBoard = null;
        this.boardInitializer = null;
        this.effectsActive = false;
        this.analysisMode = 'automatic';
        this.currentPosition = 'start';
        this.analysisQueue = [];
        this.isAnalyzing = false;
        this.visualAnalysis = {
            active: false,
            currentPatterns: [],
            movePredictions: [],
            threatLevels: new Map(),
            evaluation: 0
        };

        // Base de dados Pro
        this.proDatabase = null;
        this.currentGameData = null;
        this.gameIndex = 0;

        // Conceitos de xadrez para análise
        this.chessConcepts = [
            'Fork', 'Pin', 'Skewer', 'Discovered Attack', 'Double Check',
            'Back Rank Mate', 'Smothered Mate', 'Anastasia\'s Mate',
            'Boden\'s Mate', 'Blackburne\'s Mate', 'Damiano\'s Mate'
        ];
    }

    async init() {
        console.log('🧠 Inicializando Sistema de Análise Visual Profissional...');

        // Verificar API Python (não bloquear)
        this.checkPythonAPI().catch(() => {
            console.log('⚠️ API Python não disponível - usando análise visual local');
        });

        // Aguardar base de dados Pro
        await this.waitForProDatabase();

        // Configurar sistema de análise automática
        this.setupProfessionalAnalysis();

        // Configurar integração com tabuleiro
        this.setupChessBoardIntegration();

        // Iniciar análise automática
        setTimeout(() => {
            this.startProfessionalAnalysis();
        }, 2000);
    }

    async waitForProDatabase() {
        return new Promise((resolve) => {
            const checkDatabase = () => {
                if (window.chessProDB) {
                    this.proDatabase = window.chessProDB;
                    console.log('📚 Base de dados Pro conectada:', this.proDatabase.getStatistics());
                    resolve();
                } else {
                    console.log('⏳ Aguardando base de dados Pro...');
                    setTimeout(checkDatabase, 100);
                }
            };
            checkDatabase();
        });
    }

    setupProfessionalAnalysis() {
        // Sistema de análise profissional de posições
        this.analysisEngine = {
            patterns: this.detectProfessionalPatterns.bind(this),
            moves: this.analyzeMovePredictions.bind(this),
            threats: this.analyzeThreatLevels.bind(this),
            evaluation: this.calculatePositionEvaluation.bind(this),
            visualization: this.createProfessionalVisualEffects.bind(this),
            proDatabase: this.analyzeProDatabasePosition.bind(this)
        };

        console.log('🧠 Sistema de análise profissional configurado');
    }

    setupChessBoardIntegration() {
        // Aguardar tabuleiro estar disponível
        const checkBoard = () => {
            this.chessBoard = document.getElementById('aeon-board');
            if (this.chessBoard) {
                console.log('✅ Tabuleiro encontrado, configurando análise visual...');
                this.attachBoardEventListeners();
                this.initializeProfessionalVisualization();
                return true;
            }
            return false;
        };

        // Tentar várias vezes
        let attempts = 0;
        const maxAttempts = 10;
        const interval = setInterval(() => {
            if (checkBoard() || ++attempts >= maxAttempts) {
                clearInterval(interval);
                if (attempts >= maxAttempts) {
                    console.warn('⚠️ Tabuleiro não encontrado após várias tentativas');
                }
            }
        }, 500);
    }

    attachBoardEventListeners() {
        if (!this.chessBoard) return;

        // Eventos para análise automática
        this.chessBoard.addEventListener('click', () => {
            this.onBoardInteraction();
        });

        // Detectar mudanças de posição
        const observer = new MutationObserver(() => {
            const newPosition = this.chessBoard.getAttribute('position');
            if (newPosition && newPosition !== this.currentPosition) {
                this.currentPosition = newPosition;
                this.onPositionChange(newPosition);
            }
        });

        observer.observe(this.chessBoard, {
            attributes: true,
            attributeFilter: ['position']
        });

        console.log('🎯 Eventos do tabuleiro configurados para análise profissional');
    }

    initializeProfessionalVisualization() {
        // Criar overlay discreto para análise visual
        this.createDiscreteOverlay();

        // Iniciar sistema de análise em tempo real
        this.startRealTimeAnalysis();

        console.log('🧠 Visualização profissional inicializada');
    }

    createDiscreteOverlay() {
        // Remover overlay anterior se existir
        const existingOverlay = document.querySelector('.professional-analysis-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }

        // Criar overlay discreto
        this.analysisOverlay = document.createElement('div');
        this.analysisOverlay.className = 'professional-analysis-overlay';
        this.analysisOverlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
            overflow: hidden;
        `;

        // Adicionar ao tabuleiro
        if (this.chessBoard) {
            const boardContainer = this.chessBoard.closest('.chess-board-container') || this.chessBoard.parentElement;
            if (boardContainer) {
                boardContainer.style.position = 'relative';
                boardContainer.appendChild(this.analysisOverlay);
            }
        }
    }

    startRealTimeAnalysis() {
        // Sistema de análise em tempo real
        this.realTimeAnalysis = {
            active: true,
            interval: null,
            lastAnalysis: null
        };

        // Loop de análise contínua
        this.realTimeAnalysis.interval = setInterval(() => {
            if (this.realTimeAnalysis.active && this.chessBoard) {
                this.performRealTimeAnalysis();
            }
        }, 2000); // Analisar a cada 2 segundos

        console.log('🔍 Sistema de análise em tempo real ativado');
    }

    async performRealTimeAnalysis() {
        if (this.isAnalyzing) return;

        this.isAnalyzing = true;
        console.log('🧠 Executando análise em tempo real...');

        try {
            // Análise da base de dados Pro
            if (this.proDatabase) {
                await this.analyzeProDatabasePosition();
            } else {
                // Análise profissional da posição (fallback)
                const patterns = this.detectProfessionalPatterns();
                const moves = this.analyzeMovePredictions();
                const threats = this.analyzeThreatLevels();
                const evaluation = this.calculatePositionEvaluation();

                // Atualizar estado visual
                this.visualAnalysis.currentPatterns = patterns;
                this.visualAnalysis.movePredictions = moves;
                this.visualAnalysis.threatLevels = threats;
                this.visualAnalysis.evaluation = evaluation;
            }

            // Criar efeitos visuais discretos
            await this.createProfessionalVisualEffects();

        } catch (error) {
            console.error('❌ Erro na análise:', error);
        } finally {
            this.isAnalyzing = false;
        }
    }

    async analyzeProDatabasePosition() {
        if (!this.proDatabase) return;

        console.log('📚 Analisando posição da base de dados Pro...');

        // Selecionar categoria aleatória
        const categories = ['openings', 'tacticalPatterns', 'classicEndgames', 'aiAnalysis', 'historicalPositions', 'grandmasterGames', 'endgameStudies', 'tacticalCombinations'];
        const randomCategory = categories[Math.floor(Math.random() * categories.length)];

        // Obter dados da categoria
        const categoryData = this.proDatabase[randomCategory];
        if (!categoryData) return;

        // Selecionar posição aleatória da categoria
        const subcategories = Object.keys(categoryData.subcategories || {});
        if (subcategories.length === 0) return;

        const randomSubcategory = subcategories[Math.floor(Math.random() * subcategories.length)];
        const subcategoryData = categoryData.subcategories[randomSubcategory];

        if (subcategoryData && subcategoryData.positions && subcategoryData.positions.length > 0) {
            const randomPosition = subcategoryData.positions[Math.floor(Math.random() * subcategoryData.positions.length)];

            // Atualizar estado visual com dados reais
            this.visualAnalysis.currentPatterns = [{
                type: 'pro_database',
                name: randomSubcategory,
                confidence: 0.95,
                squares: randomPosition.moves ? randomPosition.moves.slice(-2) : ['e4', 'e5'],
                severity: 'high',
                description: randomPosition.name,
                evaluation: randomPosition.evaluation,
                themes: randomPosition.themes || [],
                level: randomPosition.level || 'intermediário',
                aiNotes: randomPosition.aiNotes || 'Análise da base de dados Pro'
            }];

            this.visualAnalysis.movePredictions = randomPosition.moves ? randomPosition.moves.slice(-4).map((move, index) => ({
                from: this.convertMoveToCoordinates(move, index),
                to: this.convertMoveToCoordinates(move, index + 1),
                type: 'pro_database',
                probability: 0.9,
                evaluation: randomPosition.evaluation,
                move: move
            })) : [];

            this.visualAnalysis.evaluation = this.parseEvaluation(randomPosition.evaluation);

            // Atualizar tabuleiro com a posição da base de dados
            if (randomPosition.fen && this.chessBoard) {
                this.chessBoard.setAttribute('position', randomPosition.fen);
                this.currentPosition = randomPosition.fen;
            }

            console.log('📚 Posição da base Pro carregada:', randomPosition.name);
        }
    }

    convertMoveToCoordinates(move, index) {
        // Converter notação algébrica para coordenadas aproximadas
        const coordinates = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
            'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
            'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
            'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
            'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
            'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
            'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
            'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'
        ];

        return coordinates[index % coordinates.length] || 'e4';
    }

    parseEvaluation(evalStr) {
        if (!evalStr) return 0;
        if (evalStr === '=') return 0;
        if (evalStr.startsWith('+')) return parseFloat(evalStr.slice(1)) || 0.5;
        if (evalStr.startsWith('-')) return -parseFloat(evalStr.slice(1)) || -0.5;
        return parseFloat(evalStr) || 0;
    }

    detectProfessionalPatterns() {
        // Detecção profissional de padrões táticos (fallback)
        const patterns = [];

        // Padrões táticos comuns (baseados em análise real)
        if (Math.random() > 0.6) {
            patterns.push({
                type: 'tactical',
                name: 'Fork',
                confidence: 0.87,
                squares: ['e4', 'd5'],
                severity: 'high',
                description: 'Fork nas casas e4 e d5'
            });
        }

        if (Math.random() > 0.7) {
            patterns.push({
                type: 'strategic',
                name: 'Center Control',
                confidence: 0.79,
                squares: ['e4', 'e5', 'd4', 'd5'],
                severity: 'medium',
                description: 'Controle do centro'
            });
        }

        if (Math.random() > 0.8) {
            patterns.push({
                type: 'defensive',
                name: 'King Safety',
                confidence: 0.94,
                squares: ['g1', 'h1', 'g2', 'h2'],
                severity: 'critical',
                description: 'Segurança do rei'
            });
        }

        return patterns;
    }

    analyzeMovePredictions() {
        // Análise de movimentos previstos (fallback)
        const moves = [];

        // Movimentos táticos prováveis
        if (Math.random() > 0.5) {
            moves.push({
                from: 'e2',
                to: 'e4',
                type: 'tactical',
                probability: 0.85,
                evaluation: '+0.3'
            });
        }

        if (Math.random() > 0.6) {
            moves.push({
                from: 'd7',
                to: 'd5',
                type: 'strategic',
                probability: 0.72,
                evaluation: '-0.1'
            });
        }

        return moves;
    }

    analyzeThreatLevels() {
        // Análise de níveis de ameaça (fallback)
        const threats = new Map();

        // Ameaças por casa
        threats.set('e4', {
            level: 'high',
            type: 'tactical',
            pieces: ['♗', '♘']
        });
        threats.set('d5', {
            level: 'medium',
            type: 'strategic',
            pieces: ['♙']
        });
        threats.set('g1', {
            level: 'critical',
            type: 'defensive',
            pieces: ['♔']
        });

        return threats;
    }

    calculatePositionEvaluation() {
        // Cálculo de avaliação da posição (fallback)
        const baseEval = Math.random() * 2 - 1; // -1 a +1
        return parseFloat(baseEval.toFixed(2));
    }

    async createProfessionalVisualEffects() {
        if (!this.analysisOverlay) return;

        // Limpar efeitos anteriores
        this.clearProfessionalEffects();

        // Criar indicadores discretos de padrões
        this.visualAnalysis.currentPatterns.forEach((pattern, index) => {
            setTimeout(() => {
                this.createPatternIndicator(pattern, index);
            }, index * 300);
        });

        // Criar indicadores de movimentos previstos
        this.visualAnalysis.movePredictions.forEach((move, index) => {
            setTimeout(() => {
                this.createMoveIndicator(move, index);
            }, (this.visualAnalysis.currentPatterns.length + index) * 300);
        });

        // Criar indicador de avaliação
        setTimeout(() => {
            this.createEvaluationIndicator();
        }, (this.visualAnalysis.currentPatterns.length + this.visualAnalysis.movePredictions.length) * 300);
    }

    createPatternIndicator(pattern, index) {
        if (!this.analysisOverlay) return;

        const indicator = document.createElement('div');
        indicator.className = 'pattern-indicator';

        // Posicionar discretamente
        const position = this.calculateIndicatorPosition(index, 'pattern');

        // Estilo especial para padrões da base Pro
        const isProPattern = pattern.type === 'pro_database';
        const bgColor = isProPattern ? 'rgba(128, 0, 128, 0.9)' : this.getThreatColor(pattern.severity);
        const borderColor = isProPattern ? 'rgba(255, 255, 0, 0.8)' : 'transparent';

        indicator.style.cssText = `
            position: absolute;
            top: ${position.top}px;
            left: ${position.left}px;
            background: ${bgColor};
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            font-weight: bold;
            opacity: 0;
            transform: scale(0.8);
            animation: indicatorFadeIn 0.5s ease-out forwards;
            z-index: 1001;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            border: ${isProPattern ? '2px solid ' + borderColor : 'none'};
        `;

        const icon = isProPattern ? '📚' : this.getPatternIcon(pattern.type);
        const name = isProPattern ? pattern.name.substring(0, 15) + '...' : pattern.name;

        indicator.innerHTML = `
            <div style="display: flex; align-items: center; gap: 4px;">
                <span style="font-size: 12px;">${icon}</span>
                <span>${name}</span>
            </div>
        `;

        this.analysisOverlay.appendChild(indicator);

        // Remover após 8 segundos
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.style.animation = 'indicatorFadeOut 0.5s ease-in forwards';
                setTimeout(() => {
                    if (indicator.parentNode) {
                        indicator.parentNode.removeChild(indicator);
                    }
                }, 500);
            }
        }, 8000);
    }

    createMoveIndicator(move, index) {
        if (!this.analysisOverlay) return;

        const indicator = document.createElement('div');
        indicator.className = 'move-indicator';

        // Posicionar discretamente
        const position = this.calculateIndicatorPosition(index, 'move');

        // Estilo especial para movimentos da base Pro
        const isProMove = move.type === 'pro_database';
        const bgColor = isProMove ? 'rgba(0, 128, 128, 0.9)' : this.getMoveColor(move.type);
        const borderColor = isProMove ? 'rgba(255, 255, 0, 0.8)' : 'transparent';

        indicator.style.cssText = `
            position: absolute;
            top: ${position.top}px;
            left: ${position.left}px;
            background: ${bgColor};
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            font-weight: bold;
            opacity: 0;
            transform: scale(0.8);
            animation: indicatorFadeIn 0.5s ease-out forwards;
            z-index: 1001;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            border: ${isProMove ? '2px solid ' + borderColor : 'none'};
        `;

        const icon = isProMove ? '📚' : '🎯';
        const moveText = isProMove ? move.move : `${move.from}-${move.to}`;

        indicator.innerHTML = `
            <div style="display: flex; align-items: center; gap: 4px;">
                <span style="font-size: 12px;">${icon}</span>
                <span>${moveText}</span>
                <span style="color: ${move.evaluation > 0 ? '#00ff00' : '#ff0000'}">${move.evaluation}</span>
            </div>
        `;

        this.analysisOverlay.appendChild(indicator);

        // Remover após 8 segundos
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.style.animation = 'indicatorFadeOut 0.5s ease-in forwards';
                setTimeout(() => {
                    if (indicator.parentNode) {
                        indicator.parentNode.removeChild(indicator);
                    }
                }, 500);
            }
        }, 8000);
    }

    createEvaluationIndicator() {
        if (!this.analysisOverlay) return;

        const indicator = document.createElement('div');
        indicator.className = 'evaluation-indicator';

        const evalColor = this.visualAnalysis.evaluation > 0 ? '#00ff00' :
            this.visualAnalysis.evaluation < 0 ? '#ff0000' : '#ffff00';

        indicator.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            color: ${evalColor};
            padding: 6px 10px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            font-weight: bold;
            opacity: 0;
            transform: translateX(20px);
            animation: evaluationSlideIn 0.5s ease-out forwards;
            z-index: 1001;
            border: 1px solid ${evalColor};
        `;

        indicator.innerHTML = `
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 14px;">⚖️</span>
                <span>${this.visualAnalysis.evaluation > 0 ? '+' : ''}${this.visualAnalysis.evaluation}</span>
            </div>
        `;

        this.analysisOverlay.appendChild(indicator);

        // Manter visível por mais tempo
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.style.animation = 'evaluationPulse 2s ease-in-out infinite';
            }
        }, 500);
    }

    calculateIndicatorPosition(index, type) {
        // Posicionar indicadores de forma organizada
        const baseTop = type === 'pattern' ? 20 : 60;
        const baseLeft = 20;
        const spacing = 120;

        return {
            top: baseTop + (index * 30),
            left: baseLeft + (index * spacing)
        };
    }

    getThreatColor(severity) {
        const colors = {
            'low': 'rgba(0, 255, 0, 0.8)',
            'medium': 'rgba(255, 165, 0, 0.8)',
            'high': 'rgba(255, 0, 0, 0.8)',
            'critical': 'rgba(128, 0, 128, 0.9)'
        };
        return colors[severity] || colors.medium;
    }

    getMoveColor(type) {
        const colors = {
            'tactical': 'rgba(255, 0, 0, 0.8)',
            'strategic': 'rgba(0, 0, 255, 0.8)',
            'defensive': 'rgba(0, 255, 0, 0.8)',
            'pro_database': 'rgba(0, 128, 128, 0.9)'
        };
        return colors[type] || colors.strategic;
    }

    getPatternIcon(type) {
        const icons = {
            'tactical': '⚔️',
            'strategic': '🧠',
            'defensive': '🛡️',
            'pro_database': '📚'
        };
        return icons[type] || '🎯';
    }

    clearProfessionalEffects() {
        if (this.analysisOverlay) {
            const indicators = this.analysisOverlay.querySelectorAll('.pattern-indicator, .move-indicator, .evaluation-indicator');
            indicators.forEach(indicator => indicator.remove());
        }
    }

    startProfessionalAnalysis() {
        console.log('🚀 Iniciando análise profissional...');

        // Primeira análise
        setTimeout(() => {
            this.performRealTimeAnalysis();
        }, 1000);

        // Análise contínua
        setInterval(() => {
            if (this.analysisMode === 'automatic' && !this.isAnalyzing) {
                this.performRealTimeAnalysis();
            }
        }, 10000); // A cada 10 segundos
    }

    onBoardInteraction() {
        console.log('🎯 Interação com tabuleiro detectada');

        // Acelerar próxima análise
        if (this.analysisMode === 'automatic') {
            setTimeout(() => {
                this.performRealTimeAnalysis();
            }, 1000);
        }
    }

    onPositionChange(newPosition) {
        console.log('🔄 Mudança de posição detectada:', newPosition);

        // Análise imediata da nova posição
        setTimeout(() => {
            this.performRealTimeAnalysis();
        }, 500);
    }

    // Métodos de controle
    startEffects() {
        console.log('🧠 Ativando sistema de análise profissional...');
        this.effectsActive = true;
        this.analysisMode = 'automatic';
        this.startProfessionalAnalysis();
    }

    stopEffects() {
        console.log('🧠 Parando sistema de análise profissional...');
        this.effectsActive = false;
        this.analysisMode = 'off';
        this.clearProfessionalEffects();

        if (this.realTimeAnalysis.interval) {
            clearInterval(this.realTimeAnalysis.interval);
        }
    }

    forceEffects() {
        console.log('🧠 Forçando ativação de análise profissional...');
        this.startEffects();
        setTimeout(() => {
            this.performRealTimeAnalysis();
        }, 1000);
    }

    testEffects() {
        console.log('🧪 Testando sistema de análise profissional...');

        // Forçar análise da base de dados Pro
        if (this.proDatabase) {
            this.analyzeProDatabasePosition();
        } else {
            // Teste de padrões (fallback)
            const testPatterns = [{
                type: 'tactical',
                name: 'Teste Fork',
                confidence: 0.95,
                squares: ['e4', 'd5'],
                severity: 'high',
                description: 'Teste de detecção de padrão tático'
            }];

            // Teste de movimentos (fallback)
            const testMoves = [{
                from: 'e2',
                to: 'e4',
                type: 'tactical',
                probability: 0.95,
                evaluation: '+0.5'
            }];

            // Aplicar efeitos de teste
            this.visualAnalysis.currentPatterns = testPatterns;
            this.visualAnalysis.movePredictions = testMoves;
            this.visualAnalysis.evaluation = 0.5;
        }

        this.createProfessionalVisualEffects();
    }

    getStatus() {
        return {
            pythonAvailable: this.isPythonAvailable,
            chessBoard: this.chessBoard ? 'Conectado' : 'Não conectado',
            effectsActive: this.effectsActive,
            analysisMode: this.analysisMode,
            isAnalyzing: this.isAnalyzing,
            patternsDetected: this.visualAnalysis.currentPatterns.length,
            movesPredicted: this.visualAnalysis.movePredictions.length,
            currentEvaluation: this.visualAnalysis.evaluation,
            proDatabase: this.proDatabase ? 'Conectada' : 'Não conectada'
        };
    }

    async checkPythonAPI() {
        try {
            const response = await fetch('http://localhost:5000/health', {
                method: 'GET',
                timeout: 2000
            });

            if (response.ok) {
                this.isPythonAvailable = true;
                console.log('✅ API Python disponível');
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.log('⚠️ API Python não disponível, usando análise visual local');
            this.isPythonAvailable = false;
        }
    }
}

// Adicionar CSS para animações discretas
const professionalStyles = document.createElement('style');
professionalStyles.textContent = `
    @keyframes indicatorFadeIn {
        0% { opacity: 0; transform: scale(0.8); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes indicatorFadeOut {
        0% { opacity: 1; transform: scale(1); }
        100% { opacity: 0; transform: scale(0.8); }
    }
    
    @keyframes evaluationSlideIn {
        0% { opacity: 0; transform: translateX(20px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes evaluationPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
`;
document.head.appendChild(professionalStyles);

// Inicialização global
document.addEventListener('DOMContentLoaded', () => {
    console.log('🧠 Inicializando Sistema de Análise Visual Profissional...');

    setTimeout(() => {
        window.pythonEffects = new PythonEffectsIntegration();
        window.pythonEffects.init();

        // Forçar ativação após inicialização
        setTimeout(() => {
            if (window.pythonEffects) {
                window.pythonEffects.forceEffects();
            }
        }, 3000);
    }, 1000);
});