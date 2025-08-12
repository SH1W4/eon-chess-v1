import useAdaptiveStore from '../stores/adaptiveStore';

export interface AdaptiveConfig {
  primarySystem: string;
  secondarySystem: string;
  adaptationMode: 'full' | 'partial' | 'minimal';
  coreCapabilities: string[];
}

export interface AdaptiveAnalysis {
  compatibilityMatrix: number[][];
  adaptationPaths: string[];
  evolutionPotential: number;
}

export interface AdaptiveVitals {
  adaptiveHealth: number;
  resourceBalance: number;
  evolutionStability: number;
}

export class AdaptiveSystem {
  private store = useAdaptiveStore;

  /**
   * Inicializa o sistema adaptativo
   */
  async init(config: AdaptiveConfig): Promise<void> {
    // Inicializa o sistema com configurações básicas
    this.store.getState().setPhase('initialization');
    
    // Análise inicial de compatibilidade
    const analysis = await this.analyzeCompatibility(config);
    
    // Atualiza métricas baseado na análise
    this.store.getState().updateMetrics({
      adaptiveCohesion: analysis.evolutionPotential
    });

    // Configura capacidades iniciais
    config.coreCapabilities.forEach(cap => {
      this.store.getState().addPrimaryCapability(cap);
    });
  }

  /**
   * Analisa compatibilidade entre sistemas
   */
  private async analyzeCompatibility(config: AdaptiveConfig): Promise<AdaptiveAnalysis> {
    // Simula análise de compatibilidade
    return {
      compatibilityMatrix: [
        [1.0, 0.8, 0.6],
        [0.8, 1.0, 0.7],
        [0.6, 0.7, 1.0]
      ],
      adaptationPaths: [
        'direct_integration',
        'event_bridge',
        'state_sync'
      ],
      evolutionPotential: 0.85
    };
  }

  /**
   * Avança para próxima fase do sistema
   */
  async evolve(): Promise<boolean> {
    const currentPhase = this.store.getState().phase;
    const metrics = this.store.getState().metrics;

    switch (currentPhase) {
      case 'initialization':
        if (metrics.adaptiveCohesion >= 0.8) {
          this.store.getState().setPhase('adaptation');
          return true;
        }
        break;

      case 'adaptation':
        if (metrics.resourceBalance >= 0.7) {
          this.store.getState().setPhase('evolution');
          return true;
        }
        break;

      case 'evolution':
        if (metrics.evolutionStability >= 0.9) {
          this.store.getState().setPhase('autonomy');
          return true;
        }
        break;
    }

    return false;
  }

  /**
   * Monitora sinais vitais do sistema
   */
  async checkVitals(): Promise<AdaptiveVitals> {
    const metrics = this.store.getState().metrics;

    return {
      adaptiveHealth: metrics.adaptiveCohesion,
      resourceBalance: metrics.resourceBalance,
      evolutionStability: metrics.evolutionStability
    };
  }

  /**
   * Recupera sistema de degradação
   */
  async recover(): Promise<boolean> {
    const metrics = this.store.getState().metrics;

    // Tenta recuperar métricas degradadas
    if (metrics.adaptiveCohesion < 0.6) {
      this.store.getState().updateMetrics({
        adaptiveCohesion: 0.7
      });
    }

    if (metrics.resourceBalance < 0.5) {
      this.store.getState().updateMetrics({
        resourceBalance: 0.6
      });
    }

    return this.checkVitals().then(vitals =>
      vitals.adaptiveHealth >= 0.6 &&
      vitals.resourceBalance >= 0.5
    );
  }

  /**
   * Adiciona nova capacidade ao sistema
   */
  async addCapability(capability: string, type: 'primary' | 'secondary'): Promise<void> {
    if (type === 'primary') {
      this.store.getState().addPrimaryCapability(capability);
    } else {
      this.store.getState().addSecondaryCapability(capability);
    }
  }

  /**
   * Remove capacidade do sistema
   */
  async removeCapability(capability: string, type: 'primary' | 'secondary'): Promise<void> {
    if (type === 'primary') {
      this.store.getState().removePrimaryCapability(capability);
    } else {
      this.store.getState().removeSecondaryCapability(capability);
    }
  }
}
