import { ChessEngineBase } from './ChessEngineBase';
import { 
  ChessPosition, 
  ChessMove,
  ArquimaxMetrics, 
  SystemHealth 
} from '../types/chess';

/**
 * Interface simbiótica para teste do motor de xadrez usando NEXUS-ARQUIMAX
 */
class SymbioticChessEngine extends ChessEngineBase {
  private symbioticState = {
    integrationScore: 0,
    adaptationRate: 0,
    evolutionProgress: 0,
    metrics: {
      moves: 0,
      analysisRequests: 0,
      errorRate: 0,
      responseTime: 0
    }
  };

  /**
   * Sobrescreve makeMove para adicionar capacidades simbióticas
   */
  override makeMove(from: ChessPosition, to: ChessPosition): boolean {
    console.log('\n=== NEXUS-ARQUIMAX: Processando Movimento ===');
    
    // ARQUIMAX: Análise prévia
    const preAnalysis = this.analyzePosition('pre-move');
    console.log('Análise prévia:', preAnalysis);

    // NEXUS: Execução adaptativa
    const startTime = Date.now();
    const result = super.makeMove(from, to);
    const endTime = Date.now();

    // Métricas
    this.symbioticState.metrics.moves++;
    this.symbioticState.metrics.responseTime = endTime - startTime;
    
    if (result) {
      // ARQUIMAX: Análise pós-movimento
      const postAnalysis = this.analyzePosition('post-move');
      console.log('Análise pós-movimento:', postAnalysis);
      
      // Atualiza estado simbiótico
      this.updateSymbioticState(true);
      this.symbioticState.metrics.analysisRequests++;
    } else {
      this.symbioticState.metrics.errorRate += 0.01;
      this.updateSymbioticState(false);
    }

    // Relatório
    this.printSymbioticReport();
    
    return result;
  }

  /**
   * Análise de posição com ARQUIMAX
   */
  private analyzePosition(phase: 'pre-move' | 'post-move'): any {
    const analysis = {
      position: this.evaluatePosition(),
      threats: this.analyzePotentialThreats(),
      opportunities: this.analyzePotentialOpportunities(),
      phase
    };

    console.log(`\n=== Análise ARQUIMAX (${phase}) ===`);
    console.log('- Avaliação:', analysis.position);
    console.log('- Ameaças:', analysis.threats.length);
    console.log('- Oportunidades:', analysis.opportunities.length);

    return analysis;
  }

  /**
   * Análise de ameaças potenciais
   */
  private analyzePotentialThreats(): any[] {
    const threats = [];
    const currentPlayer = this.getCurrentPlayer();
    const board = this.getBoard();

    // Analisa ameaças ao rei
    if (this.isCheck()) {
      threats.push({
        type: 'check',
        severity: 'high',
        target: this.findKing(currentPlayer)
      });
    }

    // Analisa ameaças a peças valiosas
    board.forEach((row, i) => {
      row.forEach((piece, j) => {
        if (piece && piece.color === currentPlayer) {
          const moves = this.getPossibleMoves({ row: i, col: j });
          if (moves.some(m => m.captured)) {
            threats.push({
              type: 'piece_threatened',
              severity: 'medium',
              target: { row: i, col: j }
            });
          }
        }
      });
    });

    return threats;
  }

  /**
   * Análise de oportunidades potenciais
   */
  private analyzePotentialOpportunities(): any[] {
    const opportunities: any[] = [];
    const currentPlayer = this.getCurrentPlayer();
    const board = this.getBoard();

    // Analisa oportunidades de captura
    board.forEach((row, i) => {
      row.forEach((piece, j) => {
        if (piece && piece.color === currentPlayer) {
          const moves = this.getPossibleMoves({ row: i, col: j });
          moves.forEach(move => {
            if (move.captured) {
              opportunities.push({
                type: 'capture',
                value: this.getPieceValue(move.captured.type),
                from: { row: i, col: j },
                to: move.to
              });
            }
          });
        }
      });
    });

    return opportunities;
  }

  /**
   * Atualiza estado simbiótico
   */
  private updateSymbioticState(success: boolean): void {
    if (success) {
      this.symbioticState.integrationScore = Math.min(1, this.symbioticState.integrationScore + 0.1);
      this.symbioticState.adaptationRate = Math.min(1, this.symbioticState.adaptationRate + 0.05);
      this.symbioticState.evolutionProgress = Math.min(1, this.symbioticState.evolutionProgress + 0.02);
    } else {
      this.symbioticState.integrationScore = Math.max(0, this.symbioticState.integrationScore - 0.1);
      this.symbioticState.adaptationRate = Math.max(0, this.symbioticState.adaptationRate - 0.05);
    }
  }

  /**
   * Imprime relatório simbiótico
   */
  private printSymbioticReport(): void {
    console.log('\n=== Relatório Simbiótico ===');
    console.log('Estado do Sistema:');
    console.log(`- Integração: ${(this.symbioticState.integrationScore * 100).toFixed(1)}%`);
    console.log(`- Adaptação: ${(this.symbioticState.adaptationRate * 100).toFixed(1)}%`);
    console.log(`- Evolução: ${(this.symbioticState.evolutionProgress * 100).toFixed(1)}%`);
    
    console.log('\nMétricas:');
    console.log(`- Movimentos processados: ${this.symbioticState.metrics.moves}`);
    console.log(`- Análises realizadas: ${this.symbioticState.metrics.analysisRequests}`);
    console.log(`- Taxa de erro: ${(this.symbioticState.metrics.errorRate * 100).toFixed(2)}%`);
    console.log(`- Tempo de resposta médio: ${this.symbioticState.metrics.responseTime}ms`);
  }

  /**
   * Retorna o valor relativo de uma peça
   */
  private getPieceValue(type: string): number {
    const values = { p: 1, n: 3, b: 3, r: 5, q: 9, k: 0 };
    return values[type as keyof typeof values] || 0;
  }
}

// Testes da interface simbiótica
console.log('=== Iniciando Teste Simbiótico ===\n');

const engine = new SymbioticChessEngine();

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

// Teste 2: Abertura com e4
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

console.log('\n=== Teste Simbiótico Concluído ===');
