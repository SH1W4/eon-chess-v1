import { ChessEngineBase } from './ChessEngineBase';
import { ChessPosition, ChessMove, GameAnalysis } from '../types/chess';
import { ArquimaxMetrics, SystemHealth } from '../types/chess';

// Polyfill for performance.now() if needed
const getNow = () => {
  if (typeof performance !== 'undefined' && performance.now) {
    return performance.now();
  }
  return Date.now();
};

class IntegratedChessEngine extends ChessEngineBase {
  private metrics: ArquimaxMetrics = {
    performance: {
      responseTime: 0,
      renderTime: 0,
      memoryUsage: 0
    },
    usage: {
      activeUsers: 1,
      gamesInProgress: 1,
      analyticsRequests: 0
    },
    quality: {
      errorRate: 0,
      crashRate: 0,
      userSatisfaction: 100
    }
  };

  private systemHealth: SystemHealth = {
    status: 'healthy',
    components: {
      'chess-engine': {
        status: 'up',
        lastCheck: new Date(),
        metrics: {}
      },
      'analysis-engine': {
        status: 'up',
        lastCheck: new Date(),
        metrics: {}
      }
    },
    lastUpdate: new Date()
  };

  // Override para adicionar métricas
  makeMove(from: ChessPosition, to: ChessPosition): boolean {
    console.log('\n=== NEXUS-ARQUIMAX: Processando Movimento ===');
    
    const startTime = getNow();
    const result = super.makeMove(from, to);
    const endTime = getNow();

    this.metrics.performance.responseTime = endTime - startTime;
    this.updateSystemHealth();

    if (result) {
      this.metrics.usage.analyticsRequests++;
      console.log('- Movimento processado com sucesso');
      console.log(`- Tempo de resposta: ${this.metrics.performance.responseTime.toFixed(2)}ms`);
      this.printAnalytics();
    } else {
      this.metrics.quality.errorRate += 0.01;
      console.log('- Movimento inválido detectado');
    }

    return result;
  }

  private updateSystemHealth(): void {
    this.systemHealth.lastUpdate = new Date();
    this.systemHealth.components['chess-engine'].lastCheck = new Date();
    this.systemHealth.components['chess-engine'].metrics = {
      responseTime: this.metrics.performance.responseTime,
      errorRate: this.metrics.quality.errorRate
    };
  }

  private printAnalytics(): void {
    const position = this.evaluatePosition();
    console.log('\n=== Análise ARQUIMAX ===');
    console.log(`- Avaliação da posição: ${position}`);
    console.log(`- Jogador atual: ${this.getCurrentPlayer()}`);
    console.log('- Estado do jogo:');
    console.log(`  * Check: ${this.isCheck()}`);
    console.log(`  * Checkmate: ${this.isCheckmate()}`);
    console.log(`  * Draw: ${this.isDraw()}`);
    
    console.log('\n=== Métricas do Sistema ===');
    console.log('- Performance:');
    console.log(`  * Tempo de resposta: ${this.metrics.performance.responseTime.toFixed(2)}ms`);
    console.log(`  * Taxa de erro: ${(this.metrics.quality.errorRate * 100).toFixed(2)}%`);
    console.log('- Utilização:');
    console.log(`  * Requisições de análise: ${this.metrics.usage.analyticsRequests}`);
  }
}

// Teste da integração
console.log('=== Iniciando Teste de Integração NEXUS-ARQUIMAX ===\n');

const engine = new IntegratedChessEngine();

// Função auxiliar para imprimir o tabuleiro
function printBoard() {
  const board = engine.getBoard();
  console.log('\nTabuleiro atual:');
  console.log('  a b c d e f g h');
  board.forEach((row, i) => {
    let line = `${8-i} `;
    row.forEach(piece => {
      if (piece === null) {
        line += '. ';
      } else {
        const symbol = piece.type + (piece.color === 'white' ? 'w' : 'b') + ' ';
        line += symbol;
      }
    });
    line += `${8-i}`;
    console.log(line);
  });
  console.log('  a b c d e f g h\n');
}

// Teste 1: Posição inicial
console.log('1. Verificando posição inicial');
printBoard();

// Teste 2: Movimento de abertura
console.log('2. Executando e4 (Abertura)');
engine.makeMove(
  { row: 6, col: 4 }, // e2
  { row: 4, col: 4 }  // e4
);
printBoard();

// Teste 3: Tentativa de movimento ilegal
console.log('3. Tentando movimento ilegal');
engine.makeMove(
  { row: 0, col: 4 }, // e8
  { row: 4, col: 4 }  // e4
);

// Teste 4: Sequência do Mate do Pastor
console.log('4. Configurando posição do Mate do Pastor');
engine.setFEN('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2');
printBoard();
engine.makeMove(
  { row: 7, col: 5 }, // f1
  { row: 3, col: 1 }  // b5
);
printBoard();

console.log('\n=== Teste de Integração Concluído ===');
