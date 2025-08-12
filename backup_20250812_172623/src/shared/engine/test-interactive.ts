import { ChessEngineBase } from './ChessEngineBase';
import { ChessPosition, PieceType } from '../types/chess';

// Cria uma instância do motor
const engine = new ChessEngineBase();

// Registra handler de eventos
engine.on('engine-event', (event) => {
  console.log('\nEVENTO:', event);
});

// Função auxiliar para imprimir o tabuleiro
function printBoard() {
  const board = engine.getBoard();
  console.log('\nTabuleiro atual:');
  console.log('  a b c d e f g h');
  board.forEach((row, i) => {
    let line = `${8-i} `;
    row.forEach((piece, j) => {
      if (piece === null) {
        line += '. ';
      } else {
        const symbol = getPieceSymbol(piece.type, piece.color);
        line += symbol + ' ';
      }
    });
    line += `${8-i}`;
    console.log(line);
  });
  console.log('  a b c d e f g h');
  console.log('\nFEN:', engine.getFEN());
  console.log('Jogador atual:', engine.getCurrentPlayer());
}

// Função auxiliar para símbolos das peças
function getPieceSymbol(type: PieceType, color: 'white' | 'black'): string {
  const symbols: {[key: string]: {[key: string]: string}} = {
    'p': { 'white': '♙', 'black': '♟' },
    'n': { 'white': '♘', 'black': '♞' },
    'b': { 'white': '♗', 'black': '♝' },
    'r': { 'white': '♖', 'black': '♜' },
    'q': { 'white': '♕', 'black': '♛' },
    'k': { 'white': '♔', 'black': '♚' }
  };
  return symbols[type][color];
}

// Testes interativos
console.log('=== Teste Interativo do Motor de Xadrez ===\n');

// 1. Teste posição inicial
console.log('1. Posição Inicial');
printBoard();

// 2. Teste movimento válido (e4)
console.log('\n2. Teste de movimento válido (e2-e4)');
const result1 = engine.makeMove(
  { row: 6, col: 4 } as ChessPosition, // e2
  { row: 4, col: 4 } as ChessPosition  // e4
);
console.log('Movimento e2-e4:', result1 ? 'SUCESSO' : 'FALHA');
printBoard();

// 3. Teste movimento inválido
console.log('\n3. Teste de movimento inválido (e7-e5 - não é vez das pretas)');
const result2 = engine.makeMove(
  { row: 1, col: 4 } as ChessPosition, // e7
  { row: 3, col: 4 } as ChessPosition  // e5
);
console.log('Movimento e7-e5:', result2 ? 'SUCESSO' : 'FALHA');

// 4. Teste FEN customizado (posição de mate do pastor)
console.log('\n4. Teste de posição customizada (Mate do Pastor)');
engine.setFEN('r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4');
printBoard();

// 5. Teste avaliação de posição
console.log('\n5. Avaliação da posição atual');
const evaluation = engine.evaluatePosition();
console.log('Avaliação:', evaluation);

// 6. Teste de estados do jogo
console.log('\n6. Estados do jogo');
console.log('Em xeque?', engine.isCheck());
console.log('Xeque-mate?', engine.isCheckmate());
console.log('Empate?', engine.isDraw());
console.log('Jogo terminado?', engine.isGameOver());

// 7. Teste movimentos possíveis
console.log('\n7. Movimentos possíveis da rainha em h5');
const moves = engine.getPossibleMoves({ row: 3, col: 7 } as ChessPosition); // h5
console.log('Movimentos:', moves);

// 8. Teste desfazer movimento
console.log('\n8. Teste desfazer último movimento');
engine.reset(); // Volta para posição inicial
engine.makeMove(
  { row: 6, col: 4 } as ChessPosition, // e2
  { row: 4, col: 4 } as ChessPosition  // e4
);
console.log('\nApós e2-e4:');
printBoard();
engine.undoLastMove();
console.log('\nApós desfazer:');
printBoard();

console.log('\n=== Teste Interativo Concluído ===');
