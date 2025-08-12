import { ChessEngineBase } from './ChessEngineBase';

console.log('Iniciando teste simples...');

const engine = new ChessEngineBase();

console.log('Engine criada');
console.log('FEN inicial:', engine.getFEN());

const result = engine.makeMove(
  { row: 6, col: 4 }, // e2
  { row: 4, col: 4 }  // e4
);

console.log('Movimento e2-e4:', result ? 'SUCESSO' : 'FALHA');
console.log('FEN após movimento:', engine.getFEN());
