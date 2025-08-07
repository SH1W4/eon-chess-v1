import { ChessEngineBase } from './ChessEngineBase.js';

// Force stdout flush
function forceFlush(message: string) {
    process.stdout.write(message + '\n');
    (process.stdout as any)._handle?.setBlocking?.(true);
}

async function runTest() {
    try {
        forceFlush('=== Iniciando Teste com Flush ===');

        // Criando instância do motor
        const engine = new ChessEngineBase();
        forceFlush('Motor criado com sucesso');

        // Testando FEN inicial
        const fen = engine.getFEN();
        forceFlush(`FEN inicial: ${fen}`);

        // Testando movimento simples
        forceFlush('\nExecutando movimento e2-e4...');
        const moveResult = engine.makeMove(
            { row: 6, col: 4 }, // e2
            { row: 4, col: 4 }  // e4
        );
        forceFlush(`Resultado do movimento: ${moveResult ? 'SUCESSO' : 'FALHA'}`);

        // Testando FEN após movimento
        const newFen = engine.getFEN();
        forceFlush(`FEN após movimento: ${newFen}`);

        // Testando movimento inválido
        forceFlush('\nTentando movimento inválido...');
        const invalidMove = engine.makeMove(
            { row: 0, col: 4 }, // e8
            { row: 4, col: 4 }  // e4
        );
        forceFlush(`Resultado do movimento inválido: ${invalidMove ? 'SUCESSO' : 'FALHA (esperado)'}`);

        // Testando detecção de xeque
        forceFlush('\nConfigurando posição de xeque...');
        engine.setFEN('rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3');
        forceFlush(`Em xeque: ${engine.isCheck()}`);
        forceFlush(`Em xeque-mate: ${engine.isCheckmate()}`);
        forceFlush(`Jogo terminado: ${engine.isGameOver()}`);

        forceFlush('\n=== Teste Concluído ===');
    } catch (error) {
        forceFlush('\nERRO: ' + (error instanceof Error ? error.message : String(error)));
        process.exit(1);
    }
}

runTest().catch(error => {
    forceFlush('\nERRO FATAL: ' + error);
    process.exit(1);
});
