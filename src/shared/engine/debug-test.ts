import { ChessEngineBase } from './ChessEngineBase';

// Função básica para log
function log(message: string) {
    process.stdout.write(message + '\n');
}

try {
    log('=== Teste de Debug Iniciado ===');

    // Criando instância do motor
    const engine = new ChessEngineBase();
    log('Motor criado com sucesso');

    // Testando FEN inicial
    const fen = engine.getFEN();
    log(`FEN inicial: ${fen}`);

    // Testando movimento simples
    const moveResult = engine.makeMove(
        { row: 6, col: 4 }, // e2
        { row: 4, col: 4 }  // e4
    );
    log(`Resultado do movimento e2-e4: ${moveResult ? 'SUCESSO' : 'FALHA'}`);

    // Testando FEN após movimento
    const newFen = engine.getFEN();
    log(`FEN após movimento: ${newFen}`);

    log('=== Teste de Debug Concluído ===');
} catch (error) {
    log('ERRO: ' + (error instanceof Error ? error.message : String(error)));
    process.exit(1);
}
