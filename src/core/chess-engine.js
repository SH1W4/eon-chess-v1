// AEON CHESS Engine - Sistema de Avaliação e IA
// Versão: 2.0 - Integração com Landing Page

class AeonChessEngine {
    constructor() {
        this.game = null;
        this.analysisDepth = 3;
        this.evaluationCache = new Map();
        this.openingBook = this.initializeOpeningBook();
    }

    initializeOpeningBook() {
        // Aberturas populares com primeiros movimentos
        return {
            'e2e4': {
                'e7e5': { name: 'Abertura Espanhola', moves: ['g1f3', 'b8c6', 'f1b5'] },
                'c7c5': { name: 'Defesa Siciliana', moves: ['g1f3', 'd7d6', 'd2d4'] },
                'e7e6': { name: 'Defesa Francesa', moves: ['d2d4', 'd7d5', 'e4d5'] }
            },
            'd2d4': {
                'd7d5': { name: 'Gambito da Dama', moves: ['c2c4', 'd5c4', 'e2e3'] },
                'g8f6': { name: 'Defesa Índia', moves: ['c2c4', 'g7g6', 'b1c3'] }
            }
        };
    }

    setGame(game) {
        this.game = game;
    }

    // Avaliação de posição baseada em material e posição
    evaluatePosition(fen = null) {
        if (!this.game) return 0;
        
        const position = fen || this.game.fen();
        
        // Verificar cache
        if (this.evaluationCache.has(position)) {
            return this.evaluationCache.get(position);
        }
        
        let score = 0;
        
        // Avaliação de material
        score += this.evaluateMaterial(position);
        
        // Avaliação de posição
        score += this.evaluatePositional(position);
        
        // Avaliação de desenvolvimento
        score += this.evaluateDevelopment(position);
        
        // Avaliação de segurança do rei
        score += this.evaluateKingSafety(position);
        
        // Cache do resultado
        this.evaluationCache.set(position, score);
        
        return score;
    }

    evaluateMaterial(fen) {
        const pieceValues = {
            'p': 100,   // peão
            'n': 320,   // cavalo
            'b': 330,   // bispo
            'r': 500,   // torre
            'q': 900,   // dama
            'k': 20000  // rei
        };
        
        const board = fen.split(' ')[0];
        let score = 0;
        
        for (let char of board) {
            if (char === '/' || !isNaN(Number(char))) continue;
            
            const isWhite = char === char.toUpperCase();
            const piece = char.toLowerCase();
            const value = pieceValues[piece] || 0;
            
            score += isWhite ? value : -value;
        }
        
        return score;
    }

    evaluatePositional(fen) {
        const pieceSquareTables = {
            'p': [ // peões
                0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0
            ],
            'n': [ // cavalos
                -50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50
            ],
            'b': [ // bispos
                -20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20
            ],
            'r': [ // torres
                0,  0,  0,  0,  0,  0,  0,  0,
                5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0
            ],
            'q': [ // dama
                -20,-10,-10, -5, -5,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5,  5,  5,  5,  0,-10,
                -5,  0,  5,  5,  5,  5,  0, -5,
                0,  0,  5,  5,  5,  5,  0, -5,
                -10,  5,  5,  5,  5,  5,  0,-10,
                -10,  0,  5,  0,  0,  0,  0,-10,
                -20,-10,-10, -5, -5,-10,-10,-20
            ],
            'k': [ // rei (meio-jogo)
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20
            ]
        };
        
        const board = fen.split(' ')[0];
        let score = 0;
        let squareIndex = 0;
        
        for (let char of board) {
            if (char === '/') continue;
            
            if (!isNaN(Number(char))) {
                squareIndex += parseInt(char);
                continue;
            }
            
            const isWhite = char === char.toUpperCase();
            const piece = char.toLowerCase();
            const table = pieceSquareTables[piece];
            
            if (table) {
                const index = isWhite ? squareIndex : 63 - squareIndex;
                score += isWhite ? table[index] : -table[index];
            }
            
            squareIndex++;
        }
        
        return score;
    }

    evaluateDevelopment(fen) {
        const board = fen.split(' ')[0];
        let whiteDevelopment = 0;
        let blackDevelopment = 0;
        let squareIndex = 0;
        
        for (let char of board) {
            if (char === '/') continue;
            
            if (!isNaN(Number(char))) {
                squareIndex += parseInt(char);
                continue;
            }
            
            const isWhite = char === char.toUpperCase();
            const piece = char.toLowerCase();
            
            // Avaliar desenvolvimento de peças menores
            if (piece === 'n' || piece === 'b') {
                const rank = Math.floor(squareIndex / 8);
                const file = squareIndex % 8;
                
                // Peças no centro são melhores
                const centerBonus = Math.max(0, 3 - Math.abs(3.5 - file)) * 10;
                const developmentBonus = isWhite ? (7 - rank) * 5 : rank * 5;
                
                if (isWhite) {
                    whiteDevelopment += centerBonus + developmentBonus;
                } else {
                    blackDevelopment += centerBonus + developmentBonus;
                }
            }
            
            squareIndex++;
        }
        
        return whiteDevelopment - blackDevelopment;
    }

    evaluateKingSafety(fen) {
        const board = fen.split(' ')[0];
        let whiteKingSafety = 0;
        let blackKingSafety = 0;
        let squareIndex = 0;
        
        // Encontrar posição dos reis
        let whiteKingPos = -1;
        let blackKingPos = -1;
        
        for (let char of board) {
            if (char === '/') continue;
            
            if (!isNaN(Number(char))) {
                squareIndex += parseInt(char);
                continue;
            }
            
            if (char === 'K') whiteKingPos = squareIndex;
            if (char === 'k') blackKingPos = squareIndex;
            
            squareIndex++;
        }
        
        // Avaliar segurança baseada na posição
        if (whiteKingPos !== -1) {
            const rank = Math.floor(whiteKingPos / 8);
            const file = whiteKingPos % 8;
            
            // Rei no centro é mais seguro no meio-jogo
            const centerDistance = Math.abs(3.5 - file) + Math.abs(3.5 - rank);
            whiteKingSafety = Math.max(0, 7 - centerDistance) * 10;
        }
        
        if (blackKingPos !== -1) {
            const rank = Math.floor(blackKingPos / 8);
            const file = blackKingPos % 8;
            
            const centerDistance = Math.abs(3.5 - file) + Math.abs(3.5 - rank);
            blackKingSafety = Math.max(0, 7 - centerDistance) * 10;
        }
        
        return whiteKingSafety - blackKingSafety;
    }

    // Encontrar melhor movimento usando minimax com alpha-beta pruning
    findBestMove(depth = 3) {
        if (!this.game) return null;
        
        const moves = this.game.moves({ verbose: true });
        if (moves.length === 0) return null;
        
        let bestMove = null;
        let bestScore = this.game.turn() === 'w' ? -Infinity : Infinity;
        const alpha = -Infinity;
        const beta = Infinity;
        
        for (const move of moves) {
            this.game.move(move);
            const score = this.minimax(depth - 1, alpha, beta, this.game.turn() === 'b');
            this.game.undo();
            
            if (this.game.turn() === 'w') {
                if (score > bestScore) {
                    bestScore = score;
                    bestMove = move;
                }
            } else {
                if (score < bestScore) {
                    bestScore = score;
                    bestMove = move;
                }
            }
        }
        
        return bestMove;
    }

    minimax(depth, alpha, beta, isMaximizing) {
        if (depth === 0 || this.game.game_over()) {
            return this.evaluatePosition();
        }
        
        const moves = this.game.moves({ verbose: true });
        
        if (isMaximizing) {
            let maxScore = -Infinity;
            
            for (const move of moves) {
                this.game.move(move);
                const score = this.minimax(depth - 1, alpha, beta, false);
                this.game.undo();
                
                maxScore = Math.max(maxScore, score);
                alpha = Math.max(alpha, score);
                
                if (beta <= alpha) break; // Alpha-beta pruning
            }
            
            return maxScore;
        } else {
            let minScore = Infinity;
            
            for (const move of moves) {
                this.game.move(move);
                const score = this.minimax(depth - 1, alpha, beta, true);
                this.game.undo();
                
                minScore = Math.min(minScore, score);
                beta = Math.min(beta, score);
                
                if (beta <= alpha) break; // Alpha-beta pruning
            }
            
            return minScore;
        }
    }

    // Analisar posição atual e fornecer insights
    analyzePosition() {
        if (!this.game) return null;
        
        const evaluation = this.evaluatePosition();
        const moves = this.game.moves({ verbose: true });
        const isCheck = this.game.in_check();
        const isCheckmate = this.game.in_checkmate();
        const isDraw = this.game.in_draw();
        
        // Encontrar ameaças táticas
        const tacticalThreats = this.findTacticalThreats();
        
        // Avaliar controle do centro
        const centerControl = this.evaluateCenterControl();
        
        // Avaliar desenvolvimento
        const development = this.evaluateDevelopment(this.game.fen());
        
        return {
            evaluation: evaluation,
            moveCount: moves.length,
            isCheck: isCheck,
            isCheckmate: isCheckmate,
            isDraw: isDraw,
            tacticalThreats: tacticalThreats,
            centerControl: centerControl,
            development: development,
            recommendations: this.generateRecommendations(evaluation, moves, isCheck)
        };
    }

    findTacticalThreats() {
        const threats = [];
        const moves = this.game.moves({ verbose: true });
        
        for (const move of moves) {
            if (move.captured) {
                threats.push({
                    type: 'capture',
                    move: move.san,
                    from: move.from,
                    to: move.to,
                    captured: move.captured
                });
            }
            
            if (move.san.includes('+')) {
                threats.push({
                    type: 'check',
                    move: move.san,
                    from: move.from,
                    to: move.to
                });
            }
        }
        
        return threats;
    }

    evaluateCenterControl() {
        const centerSquares = ['d4', 'd5', 'e4', 'e5'];
        let whiteControl = 0;
        let blackControl = 0;
        
        for (const square of centerSquares) {
            const piece = this.game.get(square);
            if (piece) {
                if (piece.color === 'w') {
                    whiteControl++;
                } else {
                    blackControl++;
                }
            }
        }
        
        return whiteControl - blackControl;
    }

    generateRecommendations(evaluation, moves, isCheck) {
        const recommendations = [];
        
        if (isCheck) {
            recommendations.push('Priorize sair do xeque');
        }
        
        if (evaluation > 200) {
            recommendations.push('Mantenha a vantagem material');
        } else if (evaluation < -200) {
            recommendations.push('Busque compensação tática');
        }
        
        if (moves.length < 10) {
            recommendations.push('Desenvolva suas peças');
        }
        
        const captures = moves.filter(m => m.captured);
        if (captures.length > 0) {
            recommendations.push('Considere as capturas disponíveis');
        }
        
        return recommendations;
    }

    // Avaliar qualidade de um movimento específico
    evaluateMove(move, positionBefore, positionAfter) {
        this.game.move(move);
        const evaluationAfter = this.evaluatePosition();
        this.game.undo();
        
        const evaluationBefore = this.evaluatePosition(positionBefore);
        const improvement = evaluationAfter - evaluationBefore;
        
        let score = 0.5; // neutro
        let isTactical = false;
        let reasoning = [];
        
        // Avaliar capturas
        if (move.captured) {
            score += 0.3;
            isTactical = true;
            reasoning.push('captura');
        }
        
        // Avaliar xeques
        if (move.san.includes('+')) {
            score += 0.2;
            isTactical = true;
            reasoning.push('xeque');
        }
        
        // Avaliar desenvolvimento
        if ((move.piece === 'n' || move.piece === 'b') && 
            (move.from[1] === '1' || move.from[1] === '8')) {
            score += 0.2;
            reasoning.push('desenvolvimento');
        }
        
        // Avaliar controle central
        const centralSquares = ['d4', 'd5', 'e4', 'e5'];
        if (centralSquares.includes(move.to)) {
            score += 0.15;
            reasoning.push('controle central');
        }
        
        // Avaliar roque
        if (move.san.includes('O')) {
            score += 0.25;
            reasoning.push('roque');
        }
        
        // Ajustar baseado na avaliação da posição
        if (improvement > 100) {
            score += 0.2;
            reasoning.push('melhora posição');
        } else if (improvement < -100) {
            score -= 0.2;
            reasoning.push('piora posição');
        }
        
        return {
            score: Math.max(0, Math.min(1, score)),
            isTactical,
            reasoning,
            improvement,
            evaluation: evaluationAfter
        };
    }

    // Limpar cache de avaliação
    clearCache() {
        this.evaluationCache.clear();
    }

    // Configurar profundidade de análise
    setAnalysisDepth(depth) {
        this.analysisDepth = Math.max(1, Math.min(6, depth));
    }
}

// Exportar para uso global
window.AeonChessEngine = AeonChessEngine;
