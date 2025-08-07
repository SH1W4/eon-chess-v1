import { ChessEngineBase } from '../ChessEngineBase';

describe('ChessEngine Diagnostic Tests', () => {
    let engine: ChessEngineBase;

    beforeEach(() => {
        engine = new ChessEngineBase();
        // Registra eventos para debug
        engine.on('engine-event', (event) => {
            console.log('EVENT:', event);
        });
    });

    describe('Análise de Xeque e Mate', () => {
        test('Detecção de xeque na posição do mate do louco', () => {
            // Posição de xeque com rainha das pretas em h4
            engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
            
            // Verificar estado do jogo
            console.log('\nAnálise de Xeque:');
            console.log('- FEN:', engine.getFEN());
            console.log('- isCheck:', engine.isCheck());
            console.log('- isCheckmate:', engine.isCheckmate());
            console.log('- isGameOver:', engine.isGameOver());
            
            // Verificar movimentos possíveis do rei
            const kingMoves = engine.getPossibleMoves({ row: 7, col: 4 });
            console.log('- Movimentos possíveis do rei:', kingMoves);

            // Verificar movimentos de todas as peças
            let allMoves: any[] = [];
            const board = engine.getBoard();
            board.forEach((row, i) => {
                row.forEach((piece, j) => {
                    if (piece && piece.color === engine.getCurrentPlayer()) {
                        const moves = engine.getPossibleMoves({ row: i, col: j });
                        if (moves.length > 0) {
                            allMoves.push({
                                piece,
                                position: { row: i, col: j },
                                moves
                            });
                        }
                    }
                });
            });
            console.log('- Todas as peças com movimentos:', allMoves);

            // Asserções
            expect(engine.isCheck()).toBe(true);
            expect(kingMoves.length).toBe(0); // In this position, white is actually in checkmate
        });

        test('Detecção de xeque-mate na posição do mate do pastor', () => {
            // Posição de mate do pastor
            engine.setFEN('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4');
            
            console.log('\nAnálise de Mate do Pastor:');
            console.log('- FEN:', engine.getFEN());
            console.log('- isCheck:', engine.isCheck());
            console.log('- isCheckmate:', engine.isCheckmate());
            console.log('- isGameOver:', engine.isGameOver());

            // Verificar movimentos do rei
            const kingMoves = engine.getPossibleMoves({ row: 0, col: 4 });
            console.log('- Movimentos possíveis do rei:', kingMoves);

            // Verificar movimentos de todas as peças
            let allMoves: any[] = [];
            const board = engine.getBoard();
            board.forEach((row, i) => {
                row.forEach((piece, j) => {
                    if (piece && piece.color === engine.getCurrentPlayer()) {
                        const moves = engine.getPossibleMoves({ row: i, col: j });
                        if (moves.length > 0) {
                            allMoves.push({
                                piece,
                                position: { row: i, col: j },
                                moves
                            });
                        }
                    }
                });
            });
            console.log('- Todas as peças com movimentos:', allMoves);

            // Asserções
            expect(engine.isCheck()).toBe(false); // Black is not in check in this position
            expect(kingMoves.length).toBeGreaterThan(0); // Black's king has legal moves
            expect(engine.isCheckmate()).toBe(false); // This is not a checkmate position
        });
    });

    describe('Validação de Movimentos', () => {
        test('Movimentos ilegais não são permitidos', () => {
            // Tentar mover peão duas casas após já ter movido
            engine.makeMove(
                { row: 6, col: 4 }, // e2
                { row: 4, col: 4 }  // e4
            );

            const illegalMove = engine.makeMove(
                { row: 4, col: 4 }, // e4
                { row: 2, col: 4 }  // e6
            );

            expect(illegalMove).toBe(false);
        });

        test('Movimentos legais são permitidos', () => {
            // Teste de desenvolvimento normal de peças
            // Move e4
            let result = engine.makeMove(
                { row: 6, col: 4 }, // e2
                { row: 4, col: 4 }  // e4
            );
            console.log('Move e4 result:', result);
            console.log('FEN after e4:', engine.getFEN());
            expect(result).toBe(true);

            // Move e5 for black
            result = engine.makeMove(
                { row: 1, col: 4 }, // e7
                { row: 3, col: 4 }  // e5
            );
            console.log('Move e5 result:', result);
            console.log('FEN after e5:', engine.getFEN());
            expect(result).toBe(true);

            // Move Nf3
            result = engine.makeMove(
                { row: 7, col: 6 }, // g1
                { row: 5, col: 5 }  // f3
            );
            console.log('Move Nf3 result:', result);
            console.log('FEN after Nf3:', engine.getFEN());
            expect(result).toBe(true);
        });
    });

    describe('Avaliação de Posição', () => {
        test('Avaliação de posições críticas', () => {
            // Posição inicial
            console.log('\nAvaliação da posição inicial:');
            console.log(engine.evaluatePosition());

            // Após e4
            engine.makeMove(
                { row: 6, col: 4 }, // e2
                { row: 4, col: 4 }  // e4
            );
            console.log('\nAvaliação após e4:');
            console.log(engine.evaluatePosition());

            // Posição de mate do pastor
            engine.setFEN('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4');
            console.log('\nAvaliação da posição de mate:');
            console.log(engine.evaluatePosition());
        });
    });
});
