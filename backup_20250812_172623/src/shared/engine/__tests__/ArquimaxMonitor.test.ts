import { ChessEngineBase } from '../ChessEngineBase';
import { EngineEvent, HealthStatus } from '../../types/engine';

describe('ArquimaxMonitor Tests', () => {
  let engine: ChessEngineBase;

  beforeEach(() => {
    engine = new ChessEngineBase();
  });

  test('Monitoramento de saúde inicial', () => {
    const health = engine.checkHealth();
    
    expect(health).toBeDefined();
    expect(health.status).toBe('healthy');
    expect(health.metrics).toBeDefined();
    expect(health.metrics.movesPerSecond).toBe(0);
    expect(health.metrics.cacheHitRate).toBe(0);
  });

  test('Monitoramento de eventos de movimento', () => {
    // Executa uma série de movimentos
    const moves = [
      [{ row: 6, col: 4 }, { row: 4, col: 4 }], // e4
      [{ row: 1, col: 4 }, { row: 3, col: 4 }], // e5
      [{ row: 7, col: 6 }, { row: 5, col: 5 }], // Nf3
    ];

    moves.forEach(([from, to]) => {
      engine.makeMove(from, to);
    });

    const health = engine.checkHealth();
    expect(health.metrics.movesPerSecond).toBeGreaterThan(0);
  });

  test('Detecção de estado degradado', () => {
    // Simula um grande número de movimentos em curto período
    const moves = [
      [{ row: 6, col: 4 }, { row: 4, col: 4 }], // e4
      [{ row: 1, col: 4 }, { row: 3, col: 4 }], // e5
      [{ row: 7, col: 6 }, { row: 5, col: 5 }], // Nf3
      [{ row: 0, col: 6 }, { row: 2, col: 5 }], // Nf6
      [{ row: 7, col: 5 }, { row: 4, col: 2 }], // Bc4
    ];

    // Executa os movimentos várias vezes
    for (let i = 0; i < 10; i++) {
      moves.forEach(([from, to]) => {
        engine.makeMove(from, to);
        engine.undoLastMove();
      });
    }

    const health = engine.checkHealth();
    expect(['degraded', 'unhealthy']).toContain(health.status);
  });

  test('Eventos são registrados corretamente', () => {
    const eventLog: EngineEvent[] = [];
    engine.on('engine-event', (event) => eventLog.push(event));

    // Faz um movimento que causa xeque
    engine.makeMove({ row: 6, col: 4 }, { row: 4, col: 4 }); // e4
    engine.makeMove({ row: 1, col: 4 }, { row: 3, col: 4 }); // e5
    engine.makeMove({ row: 7, col: 5 }, { row: 4, col: 2 }); // Bc4
    engine.makeMove({ row: 1, col: 5 }, { row: 3, col: 5 }); // f5
    engine.makeMove({ row: 7, col: 3 }, { row: 3, col: 7 }); // Qh5 - xeque

    // Verifica os eventos registrados
    expect(eventLog).toContainEqual(
      expect.objectContaining({ type: 'MOVE_MADE' })
    );
    expect(eventLog).toContainEqual(
      expect.objectContaining({ type: 'CHECK' })
    );
  });

  test('Cache hit rate é registrado', () => {
    // Realiza a mesma análise várias vezes
    const position = { row: 4, col: 4 };
    
    for (let i = 0; i < 10; i++) {
      engine.getPossibleMoves(position);
    }

    const health = engine.checkHealth();
    expect(health.metrics.cacheHitRate).toBeGreaterThan(0);
  });
});
