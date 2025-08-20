// AEON CHESS - Tabuleiro de Demonstração Visual Interativa
// Versão: 1.0 - Demonstrações Automáticas e Conceitos Visuais

class ChessDemoBoard {
    constructor() {
        this.board = null;
        this.chess = null;
        this.currentDemo = 'opening-evolution';
        this.isPlaying = false;
        this.demoInterval = null;
        this.currentStep = 0;

        this.demos = {
            'opening-evolution': {
                name: 'Evolução de Aberturas',
                description: 'Demonstra a evolução de aberturas famosas',
                duration: 8000,
                steps: [{
                        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                        description: 'Posição inicial'
                    },
                    {
                        fen: 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: '1.e4 - Abertura do peão do rei'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: '1...e5 - Resposta simétrica'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: '2.Nf3 - Desenvolvimento do cavalo'
                    },
                    {
                        fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: '2...Nf6 - Defesa do peão'
                    },
                    {
                        fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 3',
                        description: 'Posição após 3 movimentos'
                    }
                ]
            },
            'tactical-patterns': {
                name: 'Padrões Táticos',
                description: 'Demonstra padrões táticos famosos',
                duration: 6000,
                steps: [{
                        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                        description: 'Posição inicial'
                    },
                    {
                        fen: 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Preparando o ataque'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Desenvolvimento'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: 'Cavalo ativo'
                    },
                    {
                        fen: 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: 'Posição tática'
                    }
                ]
            },
            'endgame-demonstration': {
                name: 'Finais Clássicos',
                description: 'Demonstra finais famosos',
                duration: 10000,
                steps: [{
                        fen: '8/8/8/8/8/8/4K3/4k3',
                        description: 'Rei vs Rei'
                    },
                    {
                        fen: '8/8/8/8/8/8/4K3/4k3',
                        description: 'Posição de zugzwang'
                    },
                    {
                        fen: '8/8/8/8/8/8/4K3/4k3',
                        description: 'Manobra do rei'
                    }
                ]
            },
            'ai-analysis': {
                name: 'Análise da IA',
                description: 'Simula como a IA analisa posições',
                duration: 5000,
                steps: [{
                        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                        description: 'Análise inicial'
                    },
                    {
                        fen: 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Avaliação: +0.2'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Avaliação: +0.1'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: 'Avaliação: +0.4'
                    }
                ]
            },
            'historical-positions': {
                name: 'Posições Históricas',
                description: 'Posições famosas da história do xadrez',
                duration: 12000,
                steps: [{
                        fen: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                        description: 'Posição inicial'
                    },
                    {
                        fen: 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Fischer vs Spassky 1972'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR',
                        description: 'Kasparov vs Deep Blue 1997'
                    },
                    {
                        fen: 'rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R',
                        description: 'Morphy vs Duke 1858'
                    }
                ]
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
            this.startDemo();
        }
    }

    setupBoard() {
        if (this.board && this.board.setPosition) {
            this.board.setPosition('start');
        }
    }

    setupEventListeners() {
        // Demo selector
        const demoSelect = document.getElementById('demo-type');
        if (demoSelect) {
            demoSelect.addEventListener('change', (e) => {
                this.currentDemo = e.target.value;
                this.stopDemo();
                this.startDemo();
            });
        }

        // Play/Pause button
        const playPauseBtn = document.getElementById('demo-play-pause');
        if (playPauseBtn) {
            playPauseBtn.addEventListener('click', () => {
                this.toggleDemo();
            });
        }

        // Speed control
        const speedSelect = document.getElementById('demo-speed');
        if (speedSelect) {
            speedSelect.addEventListener('change', (e) => {
                this.changeSpeed(e.target.value);
            });
        }
    }

    startDemo() {
        if (this.isPlaying) return;

        this.isPlaying = true;
        this.currentStep = 0;

        const demo = this.demos[this.currentDemo];
        if (!demo) return;

        // Update play button
        const playPauseBtn = document.getElementById('demo-play-pause');
        if (playPauseBtn) {
            playPauseBtn.innerHTML = '<i class="fas fa-pause mr-2"></i>Pausar';
            playPauseBtn.classList.add('bg-red-600');
        }

        // Start the demo
        this.playDemoStep();
    }

    playDemoStep() {
        if (!this.isPlaying) return;

        const demo = this.demos[this.currentDemo];
        if (!demo || this.currentStep >= demo.steps.length) {
            this.currentStep = 0; // Loop back to start
        }

        const step = demo.steps[this.currentStep];
        if (step) {
            // Update board position
            if (this.board && this.board.setPosition) {
                this.board.setPosition(step.fen);
            }

            // Update description
            this.updateDescription(step.description);

            // Update step counter
            this.updateStepCounter();

            // Move to next step
            this.currentStep++;

            // Schedule next step
            this.demoInterval = setTimeout(() => {
                this.playDemoStep();
            }, demo.duration);
        }
    }

    stopDemo() {
        this.isPlaying = false;
        clearTimeout(this.demoInterval);

        // Update play button
        const playPauseBtn = document.getElementById('demo-play-pause');
        if (playPauseBtn) {
            playPauseBtn.innerHTML = '<i class="fas fa-play mr-2"></i>Reproduzir';
            playPauseBtn.classList.remove('bg-red-600');
        }
    }

    toggleDemo() {
        if (this.isPlaying) {
            this.stopDemo();
        } else {
            this.startDemo();
        }
    }

    changeSpeed(speed) {
        const speeds = {
            'slow': 2.0,
            'normal': 1.0,
            'fast': 0.5
        };

        const multiplier = speeds[speed] || 1.0;

        // Update all demo durations
        Object.keys(this.demos).forEach(key => {
            this.demos[key].duration = this.demos[key].duration * multiplier;
        });

        // Restart demo if playing
        if (this.isPlaying) {
            this.stopDemo();
            this.startDemo();
        }
    }

    updateDescription(description) {
        const descElement = document.getElementById('demo-description');
        if (descElement) {
            descElement.innerHTML = `
                <div class="text-center">
                    <h4 class="text-lg font-semibold text-white mb-2">${this.demos[this.currentDemo].name}</h4>
                    <p class="text-gray-300">${description}</p>
                </div>
            `;
        }
    }

    updateStepCounter() {
        const counterElement = document.getElementById('demo-step-counter');
        if (counterElement) {
            const demo = this.demos[this.currentDemo];
            const current = this.currentStep;
            const total = demo.steps.length;

            counterElement.innerHTML = `
                <div class="text-center">
                    <span class="text-sm text-gray-400">Passo ${current} de ${total}</span>
                    <div class="w-full bg-gray-700 rounded-full h-2 mt-2">
                        <div class="bg-blue-500 h-2 rounded-full transition-all duration-300" 
                             style="width: ${(current / total) * 100}%"></div>
                    </div>
                </div>
            `;
        }
    }

    // Method to get current position for visual effects
    getCurrentPosition() {
        const demo = this.demos[this.currentDemo];
        if (demo && this.currentStep < demo.steps.length) {
            return demo.steps[this.currentStep].fen;
        }
        return 'start';
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.chessDemoBoard = new ChessDemoBoard();
});