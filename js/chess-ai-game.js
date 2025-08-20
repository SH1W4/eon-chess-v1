// AEON CHESS - Sistema de Jogo contra IA
// Versão: 1.0 - Múltiplos Níveis e Autoplay

class ChessAIGame {
    constructor() {
        this.chess = null;
        this.board = null;
        this.aiLevel = 'intermediate'; // beginner, intermediate, advanced, master
        this.isPlaying = false;
        this.isAutoPlaying = false;
        this.autoPlayInterval = null;
        this.gameHistory = [];
        this.currentPosition = 'start';

        this.aiLevels = {
            beginner: {
                name: 'Iniciante',
                depth: 2,
                timeLimit: 1000,
                description: 'Ideal para jogadores que estão aprendendo'
            },
            intermediate: {
                name: 'Intermediário',
                depth: 4,
                timeLimit: 2000,
                description: 'Desafio para jogadores com experiência'
            },
            advanced: {
                name: 'Avançado',
                depth: 6,
                timeLimit: 3000,
                description: 'Para jogadores experientes'
            },
            master: {
                name: 'Mestre',
                depth: 8,
                timeLimit: 5000,
                description: 'Nível de grande mestre - muito difícil!'
            }
        };

        this.init();
    }

    init() {
        this.chess = new Chess();
        this.board = document.getElementById('aeon-board');

        if (this.board) {
            this.setupBoard();
            this.setupEventListeners();
            this.updateUI();
        }
    }

    setupBoard() {
        if (this.board && this.board.setPosition) {
            this.board.setPosition('start');
            this.board.addEventListener('onDrop', (source, target) => {
                this.handleMove(source, target);
            });
        }
    }

    setupEventListeners() {
        // Level selection
        const levelSelect = document.getElementById('ai-level');
        if (levelSelect) {
            levelSelect.addEventListener('change', (e) => {
                this.aiLevel = e.target.value;
                this.updateLevelInfo();
            });
        }

        // Game controls
        const newGameBtn = document.getElementById('new-game');
        if (newGameBtn) {
            newGameBtn.addEventListener('click', () => {
                this.newGame();
            });
        }

        const autoPlayBtn = document.getElementById('auto-play-ai');
        if (autoPlayBtn) {
            autoPlayBtn.addEventListener('click', () => {
                this.toggleAutoPlay();
            });
        }

        const resetBtn = document.getElementById('reset-game-ai');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetGame();
            });
        }

        const undoBtn = document.getElementById('undo-move');
        if (undoBtn) {
            undoBtn.addEventListener('click', () => {
                this.undoMove();
            });
        }
    }

    handleMove(source, target) {
        const move = {
            from: source,
            to: target,
            promotion: 'q' // Always promote to queen for simplicity
        };

        try {
            const result = this.chess.move(move);
            if (result) {
                this.gameHistory.push(result);
                this.updateBoard();
                this.updateGameStatus();

                // Show move analysis
                this.showMoveAnalysis(result);

                // Check for game end
                if (this.chess.isGameOver()) {
                    this.handleGameEnd();
                    return;
                }

                // AI move
                setTimeout(() => {
                    this.makeAIMove();
                }, 500);
            }
        } catch (error) {
            console.error('Invalid move:', error);
        }
    }

    showMoveAnalysis(move) {
        // Update narration with move analysis
        const narrationElement = document.getElementById('aeon-narration');
        if (narrationElement) {
            const analysis = this.analyzeMove(move);
            narrationElement.innerHTML = `
                <div class="text-blue-400">
                    <strong>${move.san}</strong> - ${analysis}
                </div>
            `;
        }
    }

    analyzeMove(move) {
        // Simple move analysis based on piece type and position
        const piece = move.piece;
        const to = move.to;
        const from = move.from;

        let analysis = '';

        switch (piece) {
            case 'p': // Pawn
                if (move.flags.includes('e')) {
                    analysis = 'Captura en passant!';
                } else if (move.to[1] === '8' || move.to[1] === '1') {
                    analysis = 'Promoção para Dama!';
                } else if (Math.abs(to.charCodeAt(1) - from.charCodeAt(1)) === 2) {
                    analysis = 'Avanço duplo do peão';
                } else {
                    analysis = 'Desenvolvimento do peão';
                }
                break;
            case 'n': // Knight
                analysis = 'Desenvolvimento do cavalo';
                break;
            case 'b': // Bishop
                analysis = 'Desenvolvimento do bispo';
                break;
            case 'r': // Rook
                if (move.flags.includes('k') || move.flags.includes('q')) {
                    analysis = 'Roque executado!';
                } else {
                    analysis = 'Desenvolvimento da torre';
                }
                break;
            case 'q': // Queen
                analysis = 'Movimento da dama';
                break;
            case 'k': // King
                if (move.flags.includes('k') || move.flags.includes('q')) {
                    analysis = 'Roque executado!';
                } else {
                    analysis = 'Movimento do rei';
                }
                break;
        }

        // Add capture analysis
        if (move.captured) {
            analysis += ` - Captura ${move.captured}`;
        }

        // Add check analysis
        if (move.san.includes('+')) {
            analysis += ' - Xeque!';
        } else if (move.san.includes('#')) {
            analysis += ' - Xeque-mate!';
        }

        return analysis;
    }

    makeAIMove() {
        if (this.chess.isGameOver()) return;

        const level = this.aiLevels[this.aiLevel];

        // Trigger visual effects to show AI is thinking
        this.triggerAIThinking();

        // Simulate AI thinking time
        setTimeout(() => {
            // For now, we'll make a random legal move
            // In a real implementation, this would use Stockfish or similar
            const moves = this.chess.moves();
            if (moves.length > 0) {
                const randomMove = moves[Math.floor(Math.random() * moves.length)];
                const result = this.chess.move(randomMove);
                if (result) {
                    this.gameHistory.push(result);
                    this.updateBoard();
                    this.updateGameStatus();

                    if (this.chess.isGameOver()) {
                        this.handleGameEnd();
                    }
                }
            }
        }, level.timeLimit);
    }

    triggerAIThinking() {
        // Update status to show AI is thinking
        const statusElement = document.getElementById('game-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="flex items-center justify-center space-x-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                    <span class="text-blue-400">IA está pensando...</span>
                </div>
            `;
        }

        // Trigger visual effects if available
        if (window.chessVisualEffects) {
            // Change effect to show AI analysis
            const effectSelect = document.getElementById('effect-type');
            if (effectSelect) {
                // Temporarily change to computer vision effect
                const currentEffect = effectSelect.value;
                effectSelect.value = 'computerVision';

                // Reset effects to show new analysis
                window.chessVisualEffects.currentEffect = 'computerVision';
                window.chessVisualEffects.resetEffects();

                // Restore original effect after a delay
                setTimeout(() => {
                    effectSelect.value = currentEffect;
                    window.chessVisualEffects.currentEffect = currentEffect;
                    window.chessVisualEffects.resetEffects();
                }, 3000);
            }
        }
    }

    newGame() {
        this.chess.reset();
        this.gameHistory = [];
        this.currentPosition = 'start';
        this.isPlaying = true;
        this.isAutoPlaying = false;

        this.updateBoard();
        this.updateGameStatus();
        this.updateUI();
    }

    resetGame() {
        this.chess.reset();
        this.gameHistory = [];
        this.currentPosition = 'start';
        this.isPlaying = false;
        this.isAutoPlaying = false;

        this.updateBoard();
        this.updateGameStatus();
        this.updateUI();
    }

    undoMove() {
        if (this.gameHistory.length > 0) {
            this.chess.undo();
            this.gameHistory.pop();

            if (this.gameHistory.length > 0) {
                this.chess.undo();
                this.gameHistory.pop();
            }

            this.updateBoard();
            this.updateGameStatus();
        }
    }

    toggleAutoPlay() {
        if (this.isAutoPlaying) {
            this.stopAutoPlay();
        } else {
            this.startAutoPlay();
        }
    }

    startAutoPlay() {
        if (this.isAutoPlaying) return;

        this.isAutoPlaying = true;
        this.isPlaying = true;

        const autoPlayBtn = document.getElementById('auto-play-ai');
        if (autoPlayBtn) {
            autoPlayBtn.textContent = 'Parar Auto-Play';
            autoPlayBtn.classList.add('bg-red-600');
        }

        this.autoPlayInterval = setInterval(() => {
            if (this.chess.isGameOver()) {
                this.stopAutoPlay();
                return;
            }

            // Make a random move for both sides
            const moves = this.chess.moves();
            if (moves.length > 0) {
                const randomMove = moves[Math.floor(Math.random() * moves.length)];
                const result = this.chess.move(randomMove);
                if (result) {
                    this.gameHistory.push(result);
                    this.updateBoard();
                    this.updateGameStatus();
                }
            }
        }, 1500); // 1.5 seconds per move
    }

    stopAutoPlay() {
        this.isAutoPlaying = false;
        clearInterval(this.autoPlayInterval);

        const autoPlayBtn = document.getElementById('auto-play-ai');
        if (autoPlayBtn) {
            autoPlayBtn.textContent = 'Auto-Play';
            autoPlayBtn.classList.remove('bg-red-600');
        }
    }

    updateBoard() {
        if (this.board && this.board.setPosition) {
            try {
                this.board.setPosition(this.chess.fen());
            } catch (error) {
                console.log('Board update:', this.chess.fen());
            }
        }
    }

    updateGameStatus() {
        const statusElement = document.getElementById('game-status');
        if (!statusElement) return;

        let status = '';

        if (this.chess.isCheckmate()) {
            status = 'Xeque-mate! ' + (this.chess.turn() === 'w' ? 'Pretas vencem!' : 'Brancas vencem!');
        } else if (this.chess.isDraw()) {
            status = 'Empate!';
        } else if (this.chess.isCheck()) {
            status = 'Xeque!';
        } else {
            status = this.chess.turn() === 'w' ? 'Vez das Brancas' : 'Vez das Pretas';
        }

        statusElement.textContent = status;

        // Update move history
        this.updateMoveHistory();
    }

    updateMoveHistory() {
        const historyElement = document.getElementById('move-history');
        if (!historyElement) return;

        let html = '';
        this.gameHistory.forEach((move, index) => {
            const moveNumber = Math.floor(index / 2) + 1;
            const isWhiteMove = index % 2 === 0;

            if (isWhiteMove) {
                html += `<div class="flex justify-between items-center py-1">`;
                html += `<span class="text-gray-500">${moveNumber}.</span>`;
                html += `<span class="text-white">${move.san}</span>`;
            } else {
                html += `<span class="text-white ml-4">${move.san}</span>`;
                html += `</div>`;
            }
        });

        historyElement.innerHTML = html;
    }

    updateLevelInfo() {
        const levelInfo = document.getElementById('level-info');
        if (!levelInfo) return;

        const level = this.aiLevels[this.aiLevel];
        levelInfo.innerHTML = `
            <h4 class="font-semibold text-white mb-2">${level.name}</h4>
            <p class="text-sm text-gray-300">${level.description}</p>
            <p class="text-xs text-gray-400">Profundidade: ${level.depth} | Tempo: ${level.timeLimit}ms</p>
        `;
    }

    updateUI() {
        this.updateLevelInfo();
        this.updateGameStatus();
    }

    handleGameEnd() {
        this.isPlaying = false;
        this.stopAutoPlay();

        // Show game result
        const resultElement = document.getElementById('game-result');
        if (resultElement) {
            if (this.chess.isCheckmate()) {
                resultElement.innerHTML = `
                    <div class="bg-gradient-to-r from-red-600 to-purple-600 p-4 rounded-lg text-white text-center">
                        <h3 class="text-xl font-bold mb-2">Xeque-Mate!</h3>
                        <p>${this.chess.turn() === 'w' ? 'Pretas vencem!' : 'Brancas vencem!'}</p>
                    </div>
                `;
            } else if (this.chess.isDraw()) {
                resultElement.innerHTML = `
                    <div class="bg-gradient-to-r from-gray-600 to-blue-600 p-4 rounded-lg text-white text-center">
                        <h3 class="text-xl font-bold mb-2">Empate!</h3>
                        <p>Jogo terminou em empate</p>
                    </div>
                `;
            }
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.chessAIGame = new ChessAIGame();
});