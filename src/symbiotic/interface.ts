// Tipos de evento do sistema simbiótico
export type SymbioticEventType = 
  | 'STATE_CHANGE'
  | 'RESOURCE_CHANGE'
  | 'CAPABILITY_ADDED'
  | 'CAPABILITY_REMOVED'
  | 'PHASE_CHANGE'
  | 'METRIC_UPDATE';

// Interface de evento simbiótico
export interface SymbioticEvent {
  type: SymbioticEventType;
  timestamp: number;
  data: any;
  source: string;
}

// Interface de capacidade simbiótica
export interface SymbioticCapability {
  name: string;
  evolutionEnabled: boolean;
  adaptationRate: 'static' | 'dynamic';
  metrics?: {
    usage: number;
    efficiency: number;
    stability: number;
  };
}

// Interface de fase simbiótica
export interface SymbioticPhase {
  name: string;
  tasks: string[];
  transitionCondition: string;
  metrics: {
    completion: number;
    stability: number;
  };
}

// Interface de métricas simbióticas
export interface SymbioticMetrics {
  symbioticCohesion: number;
  resourceBalance: number;
  emergenceStability: number;
  thresholds: {
    symbioticCohesion: number;
    resourceBalance: number;
    emergenceStability: number;
  };
}

// Interface de configuração simbiótica
export interface SymbioticConfig {
  mode: 'full' | 'partial' | 'minimal';
  evolutionEnabled: boolean;
  adaptationRate: number;
  metrics: SymbioticMetrics;
}

// Interface do sistema simbiótico
export interface SymbioticSystem {
  // Inicialização
  init(config: SymbioticConfig): Promise<void>;
  
  // Gerenciamento de fases
  getCurrentPhase(): SymbioticPhase;
  transitionToPhase(phase: string): Promise<boolean>;
  
  // Gerenciamento de capacidades
  addCapability(capability: SymbioticCapability): Promise<void>;
  removeCapability(name: string): Promise<void>;
  getCapabilities(): SymbioticCapability[];
  
  // Métricas e monitoramento
  getMetrics(): SymbioticMetrics;
  updateMetrics(metrics: Partial<SymbioticMetrics>): void;
  
  // Eventos
  addEventListener(type: SymbioticEventType, handler: (event: SymbioticEvent) => void): void;
  removeEventListener(type: SymbioticEventType, handler: (event: SymbioticEvent) => void): void;
  
  // Evolução e adaptação
  evolve(): Promise<void>;
  adapt(changes: any): Promise<void>;
  
  // Diagnóstico
  healthCheck(): Promise<{
    status: 'healthy' | 'degraded' | 'critical';
    issues: string[];
  }>;
}

// Implementação concreta do sistema simbiótico
export class SymbioticSystemImpl implements SymbioticSystem {
  private config: SymbioticConfig;
  private phase: SymbioticPhase;
  private capabilities: SymbioticCapability[];
  private metrics: SymbioticMetrics;
  private eventHandlers: Map<SymbioticEventType, ((event: SymbioticEvent) => void)[]>;

  constructor() {
    this.eventHandlers = new Map();
  }

  async init(config: SymbioticConfig): Promise<void> {
    this.config = config;
    this.metrics = config.metrics;
    this.capabilities = [];
    this.phase = {
      name: 'nucleation',
      tasks: ['core_init', 'analysis'],
      transitionCondition: 'analysis.compatibility_score >= 0.8',
      metrics: {
        completion: 0,
        stability: 1,
      },
    };
  }

  getCurrentPhase(): SymbioticPhase {
    return this.phase;
  }

  async transitionToPhase(phase: string): Promise<boolean> {
    // Implementar lógica de transição de fase
    return true;
  }

  async addCapability(capability: SymbioticCapability): Promise<void> {
    this.capabilities.push(capability);
    this.emitEvent({
      type: 'CAPABILITY_ADDED',
      timestamp: Date.now(),
      data: capability,
      source: 'system',
    });
  }

  async removeCapability(name: string): Promise<void> {
    this.capabilities = this.capabilities.filter(cap => cap.name !== name);
    this.emitEvent({
      type: 'CAPABILITY_REMOVED',
      timestamp: Date.now(),
      data: { name },
      source: 'system',
    });
  }

  getCapabilities(): SymbioticCapability[] {
    return this.capabilities;
  }

  getMetrics(): SymbioticMetrics {
    return this.metrics;
  }

  updateMetrics(metrics: Partial<SymbioticMetrics>): void {
    this.metrics = { ...this.metrics, ...metrics };
    this.emitEvent({
      type: 'METRIC_UPDATE',
      timestamp: Date.now(),
      data: metrics,
      source: 'system',
    });
  }

  addEventListener(type: SymbioticEventType, handler: (event: SymbioticEvent) => void): void {
    if (!this.eventHandlers.has(type)) {
      this.eventHandlers.set(type, []);
    }
    this.eventHandlers.get(type)?.push(handler);
  }

  removeEventListener(type: SymbioticEventType, handler: (event: SymbioticEvent) => void): void {
    const handlers = this.eventHandlers.get(type);
    if (handlers) {
      this.eventHandlers.set(
        type,
        handlers.filter(h => h !== handler)
      );
    }
  }

  private emitEvent(event: SymbioticEvent): void {
    const handlers = this.eventHandlers.get(event.type);
    if (handlers) {
      handlers.forEach(handler => handler(event));
    }
  }

  async evolve(): Promise<void> {
    if (!this.config.evolutionEnabled) return;

    // Implementar lógica de evolução
    this.emitEvent({
      type: 'STATE_CHANGE',
      timestamp: Date.now(),
      data: { action: 'evolution' },
      source: 'system',
    });
  }

  async adapt(changes: any): Promise<void> {
    // Implementar lógica de adaptação
    this.emitEvent({
      type: 'STATE_CHANGE',
      timestamp: Date.now(),
      data: { action: 'adaptation', changes },
      source: 'system',
    });
  }

  async healthCheck(): Promise<{
    status: 'healthy' | 'degraded' | 'critical';
    issues: string[];
  }> {
    const issues: string[] = [];
    
    // Verificar coesão simbiótica
    if (this.metrics.symbioticCohesion < this.metrics.thresholds.symbioticCohesion) {
      issues.push('Coesão simbiótica abaixo do limite');
    }
    
    // Verificar equilíbrio de recursos
    if (this.metrics.resourceBalance < this.metrics.thresholds.resourceBalance) {
      issues.push('Desequilíbrio de recursos detectado');
    }
    
    // Verificar estabilidade emergente
    if (this.metrics.emergenceStability < this.metrics.thresholds.emergenceStability) {
      issues.push('Instabilidade emergente detectada');
    }

    // Determinar status geral
    let status: 'healthy' | 'degraded' | 'critical' = 'healthy';
    if (issues.length > 0) {
      status = issues.length > 2 ? 'critical' : 'degraded';
    }

    return { status, issues };
  }
}
