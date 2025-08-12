import { ChessEngineBase } from '../ChessEngineBase';

describe('ChessEngine Integration Tests', () => {
    let engine: ChessEngineBase;

    beforeEach(() => {
        engine = new ChessEngineBase();
        // Registra eventos para debug
        engine.on('engine-event', (event) => {
            console.log('EVENT:', event);
        });
    });

    test('basic move sequence', () => {
        // 1. Verificar posição inicial
        const initialFen = engine.getFEN();
        console.log('FEN Inicial:', initialFen);
        expect(initialFen).toBe('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1');

        // 2. Fazer um movimento válido (e2-e4)
        const moveResult = engine.makeMove(
            { row: 6, col: 4 }, // e2
            { row: 4, col: 4 }  // e4
        );
        expect(moveResult).toBe(true);
        console.log('FEN após e4:', engine.getFEN());

        // 3. Tentar um movimento inválido
        const invalidMove = engine.makeMove(
            { row: 0, col: 4 }, // e8
            { row: 4, col: 4 }  // e4 (não é vez das pretas)
        );
        expect(invalidMove).toBe(false);

        // 4. Verificar estado do jogo
        expect(engine.isCheck()).toBe(false);
        expect(engine.isCheckmate()).toBe(false);
        expect(engine.isGameOver()).toBe(false);
        expect(engine.getCurrentPlayer()).toBe('black');

        // 5. Carregar posição de xeque
        engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
        console.log('Posição de xeque:', engine.getFEN());
        expect(engine.isCheck()).toBe(true);

        // 6. Verificar movimentos possíveis
        const moves = engine.getPossibleMoves({ row: 7, col: 4 }); // rei branco
        console.log('Movimentos possíveis do rei:', moves);
        expect(moves.length).toBeGreaterThan(0);

        // 7. Testar avaliação de posição
        const evaluation = engine.evaluatePosition();
        console.log('Avaliação da posição:', evaluation);
        expect(typeof evaluation).toBe('number');
    });

    test('detection of special positions', () => {
        // 1. Posição de mate do pastor
        engine.setFEN('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 4 4');
        console.log('Posição do mate do pastor:', engine.getFEN());
        expect(engine.isCheck()).toBe(true);

        // 2. Mate do louco
        engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3');
        console.log('Posição do mate do louco:', engine.getFEN());
        expect(engine.isCheckmate()).toBe(true);
        expect(engine.isGameOver()).toBe(true);
    });

    test('move validation and board state', () => {
        // 1. Verificar estado inicial do tabuleiro
        const board = engine.getBoard();
        expect(board).toHaveLength(8);
        board.forEach(row => expect(row).toHaveLength(8));

        // 2. Testar validação de posição
        expect(engine.isValidPosition({ row: 0, col: 0 })).toBe(true);
        expect(engine.isValidPosition({ row: 8, col: 0 })).toBe(false);

        // 3. Testar validação de movimento
        expect(engine.isValidMove(
            { row: 6, col: 4 }, // e2
            { row: 4, col: 4 }  // e4
        )).toBe(true);

        expect(engine.isValidMove(
            { row: 6, col: 4 }, // e2
            { row: 2, col: 4 }  // e6
        )).toBe(false);
    });
});
