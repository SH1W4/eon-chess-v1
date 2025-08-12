import { ChessEngineBase } from '../ChessEngineBase.js';
import { ChessPosition, ChessMove } from '../../types/chess.js';

/**
 * Interface simbiótica para análise do motor de xadrez usando NEXUS-ARQUIMAX
 */
export class SymbioticAnalyzer {
    private engine: ChessEngineBase;
    private metrics = {
        analysisRequests: 0,
        errorRate: 0,
        responseTime: 0,
        successRate: 0
    };

    constructor() {
        this.engine = new ChessEngineBase();
        this.engine.on('engine-event', (event) => {
            console.log('\nEVENTO NEXUS:', event);
        });
    }

    /**
     * Analisa uma posição específica
     */
    analyzePosition(fen: string): {
        isValid: boolean;
        check: boolean;
        checkmate: boolean;
        gameOver: boolean;
        possibleMoves: number;
        evaluation: number;
        problems: string[];
    } {
        console.log('\n=== ARQUIMAX: Analisando Posição ===');
        console.log('FEN:', fen);

        const startTime = Date.now();
        const problems: string[] = [];

        try {
            // Carrega a posição
            this.engine.setFEN(fen);

            // Coleta métricas básicas
            const inCheck = this.engine.isCheck();
            const inCheckmate = this.engine.isCheckmate();
            const isGameOver = this.engine.isGameOver();
            const evaluation = this.engine.evaluatePosition();

            // Analisa movimentos possíveis de todas as peças
            const moves = this.getAllPossibleMoves();
            
            // Diagnóstico
            if (inCheck && moves.length === 0 && !inCheckmate) {
                problems.push('Inconsistência: Posição em xeque sem movimentos, mas não é xeque-mate');
            }
            
            if (inCheckmate && moves.length > 0) {
                problems.push('Inconsistência: Posição em xeque-mate com movimentos disponíveis');
            }

            if (!inCheck && inCheckmate) {
                problems.push('Inconsistência: Xeque-mate sem estar em xeque');
            }

            // Atualiza métricas
            this.metrics.analysisRequests++;
            this.metrics.responseTime = Date.now() - startTime;
            this.metrics.successRate = (this.metrics.analysisRequests - problems.length) / this.metrics.analysisRequests;

            return {
                isValid: true,
                check: inCheck,
                checkmate: inCheckmate,
                gameOver: isGameOver,
                possibleMoves: moves.length,
                evaluation: evaluation,
                problems
            };

        } catch (error) {
            this.metrics.errorRate++;
            return {
                isValid: false,
                check: false,
                checkmate: false,
                gameOver: false,
                possibleMoves: 0,
                evaluation: 0,
                problems: [(error instanceof Error) ? error.message : 'Erro desconhecido']
            };
        }
    }

    /**
     * Obtém todos os movimentos possíveis da posição atual
     */
    private getAllPossibleMoves(): ChessMove[] {
        const moves: ChessMove[] = [];
        const board = this.engine.getBoard();

        // Percorre todo o tabuleiro
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const piece = board[row][col];
                if (piece && piece.color === this.engine.getCurrentPlayer()) {
                    const pieceMoves = this.engine.getPossibleMoves({ row, col });
                    moves.push(...pieceMoves);
                }
            }
        }

        return moves;
    }

    /**
     * Analisa uma sequência de movimentos
     */
    analyzeMoveSequence(moves: Array<[ChessPosition, ChessPosition]>): {
        success: boolean;
        moveResults: boolean[];
        finalPosition: string;
        problems: string[];
    } {
        console.log('\n=== ARQUIMAX: Analisando Sequência de Movimentos ===');
        
        const problems: string[] = [];
        const moveResults: boolean[] = [];

        this.engine.reset();
        
        for (const [from, to] of moves) {
            const result = this.engine.makeMove(from, to);
            moveResults.push(result);
            
            if (!result) {
                problems.push(`Movimento inválido: ${JSON.stringify(from)} -> ${JSON.stringify(to)}`);
            }
        }

        return {
            success: problems.length === 0,
            moveResults,
            finalPosition: this.engine.getFEN(),
            problems
        };
    }

    /**
     * Obtém métricas da análise
     */
    getMetrics() {
        return {
            ...this.metrics,
            successRate: (this.metrics.successRate * 100).toFixed(1) + '%',
            errorRate: (this.metrics.errorRate * 100).toFixed(1) + '%',
            averageResponseTime: this.metrics.responseTime / this.metrics.analysisRequests + 'ms'
        };
    }
}

// Teste das posições problemáticas
const analyzer = new SymbioticAnalyzer();

// 1. Análise da posição com problema de movimentos do rei
console.log('\nAnalisando posição de xeque do rei:');
const checkPosition = analyzer.analyzePosition('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
console.log('Resultado:', checkPosition);

// 2. Análise da posição do mate do pastor
console.log('\nAnalisando posição do mate do pastor:');
const scholarsPosition = analyzer.analyzePosition('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4');
console.log('Resultado:', scholarsPosition);

// 3. Métricas finais
console.log('\nMétricas da análise:');
console.log(analyzer.getMetrics());
