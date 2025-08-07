import { EventEmitter } from 'events';
import { EngineEvent, EngineMetrics, HealthStatus } from '../../types/engine';

/**
 * Sistema de monitoramento ARQUIMAX para o motor de xadrez.
 * 
 * Responsável por:
 * - Coleta de métricas em tempo real
 * - Verificações de saúde do sistema
 * - Monitoramento de performance
 * - Logs de eventos
 */
export class ArquimaxMonitor {
  private metrics: EngineMetrics;
  private eventEmitter: EventEmitter;
  private startTime: number;
  private moveCount: number;
  private lastHealthCheck: number;
  private healthCheckInterval: number;

  constructor() {
    this.metrics = {
      movesPerSecond: 0,
      averageThinkingTime: 0,
      cacheHitRate: 0,
      memoryUsage: 0,
      cpuUsage: 0
    };
    this.eventEmitter = new EventEmitter();
    this.startTime = Date.now();
    this.moveCount = 0;
    this.lastHealthCheck = Date.now();
    this.healthCheckInterval = 5000; // 5 segundos
  }

  /**
   * Registra um evento do motor de xadrez.
   * 
   * @param event - Evento a ser registrado
   */
  public recordEvent(event: EngineEvent): void {
    this.eventEmitter.emit('engine-event', event);
    
    if (event.type === 'MOVE_MADE') {
      this.moveCount++;
      this.updateMovesPerSecond();
    }
  }

  /**
   * Realiza verificação de saúde do sistema.
   * 
   * @returns Status atual de saúde do sistema
   */
  public checkHealth(): HealthStatus {
    const now = Date.now();
    
    // Atualiza métricas apenas se passou o intervalo definido
    if (now - this.lastHealthCheck >= this.healthCheckInterval) {
      this.updateMetrics();
      this.lastHealthCheck = now;
    }

    return {
      status: this.evaluateHealth(),
      metrics: this.metrics,
      timestamp: now
    };
  }

  /**
   * Obtém métricas atuais do sistema.
   * 
   * @returns Métricas coletadas
   */
  public getMetrics(): EngineMetrics {
    return { ...this.metrics };
  }

  /**
   * Registra uso de cache.
   * 
   * @param hit - true se houve hit no cache, false se houve miss
   */
  private cacheHits: number = 0;
  private cacheAccesses: number = 0;

  public recordCacheAccess(hit: boolean): void {
    this.cacheAccesses++;
    if (hit) this.cacheHits++;
    this.metrics.cacheHitRate = this.cacheHits / this.cacheAccesses;
  }

  /**
   * Registra tempo de pensamento para um movimento.
   * 
   * @param thinkingTime - Tempo em millisegundos
   */
  public recordThinkingTime(thinkingTime: number): void {
    const current = this.metrics.averageThinkingTime;
    this.metrics.averageThinkingTime = 
      (current * this.moveCount + thinkingTime) / (this.moveCount + 1);
  }

  private updateMovesPerSecond(): void {
    const elapsedSeconds = (Date.now() - this.startTime) / 1000;
    this.metrics.movesPerSecond = this.moveCount / elapsedSeconds;
  }

  private async updateMetrics(): Promise<void> {
    // Atualiza uso de memória
    if (process.memoryUsage) {
      const { heapUsed } = process.memoryUsage();
      this.metrics.memoryUsage = heapUsed / 1024 / 1024; // Em MB
    }

    // Atualiza uso de CPU (implementação simplificada)
    this.metrics.cpuUsage = await this.measureCPUUsage();
  }

  private evaluateHealth(): 'healthy' | 'degraded' | 'unhealthy' {
    // Critérios de saúde
    const memoryThreshold = 512; // MB
    const cpuThreshold = 80; // %
    const moveRateThreshold = 0.5; // moves/sec

    if (
      this.metrics.memoryUsage > memoryThreshold ||
      this.metrics.cpuUsage > cpuThreshold
    ) {
      return 'unhealthy';
    }

    // Sistema recém iniciado está saudável por padrão
    if (this.moveCount === 0) {
      return 'healthy';
    }

    if (
      this.metrics.movesPerSecond < moveRateThreshold ||
      (this.metrics.cacheHitRate < 0.3 && this.moveCount > 10)
    ) {
      return 'degraded';
    }

    return 'healthy';
  }

  private async measureCPUUsage(): Promise<number> {
    // Implementação simplificada de medição de CPU
    // Em uma implementação real, usaríamos métricas do sistema operacional
    return new Promise((resolve) => {
      setTimeout(() => {
        // Simula medição de CPU entre 0-100%
        resolve(Math.random() * 100);
      }, 100);
    });
  }
}
