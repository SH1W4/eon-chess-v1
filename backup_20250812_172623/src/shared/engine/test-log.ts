import { ChessEngineBase } from './ChessEngineBase';
import * as fs from 'fs';
import * as path from 'path';

const logFile = path.join(__dirname, 'test.log');
const log = (message: string) => {
  fs.appendFileSync(logFile, message + '\n');
};

try {
  log('Iniciando teste com log...');

  const engine = new ChessEngineBase();

  log('Engine criada');
  log('FEN inicial: ' + engine.getFEN());

  const result = engine.makeMove(
    { row: 6, col: 4 }, // e2
    { row: 4, col: 4 }  // e4
  );

  log('Movimento e2-e4: ' + (result ? 'SUCESSO' : 'FALHA'));
  log('FEN após movimento: ' + engine.getFEN());

} catch (error) {
  if (error instanceof Error) {
    log('ERRO: ' + error.message);
    log('Stack: ' + error.stack);
  } else {
    log('Erro desconhecido: ' + String(error));
  }
}
