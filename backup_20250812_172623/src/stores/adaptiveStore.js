import create from 'zustand';
import arkitectAdapter from '../adapters/arkitectAdapter';

// Inicializa o adaptador do ARKITECT
arkitectAdapter.initialize();

const useAdaptiveStore = create((set) => ({
  // Estado inicial otimizado pelo ARKITECT
  metrics: arkitectAdapter.getMetrics(),
  phase: arkitectAdapter.getPhase(),

  // Capacidades do sistema
  primaryCapabilities: [
    'Gerenciamento de Recursos',
    'Análise de Performance',
    'Otimização Adaptativa',
    'Monitoramento em Tempo Real'
  ],

  secondaryCapabilities: [
    'Auto-recuperação',
    'Balanceamento de Carga',
    'Predição de Comportamento',
    'Ajuste Dinâmico'
  ],

  // Padrões adaptativos
  patterns: arkitectAdapter.getPatterns(),

  // Ações aprimoradas com ARKITECT
  updateMetrics: async () => {
    const newMetrics = await arkitectAdapter.updateMetrics();
    set({ metrics: newMetrics });
  },

  updatePhase: async () => {
    const newPhase = await arkitectAdapter.checkPhaseTransition();
    set({ phase: newPhase });
  },

  optimizeSystem: async () => {
    await arkitectAdapter.optimizeSystem();
    const newMetrics = arkitectAdapter.getMetrics();
    const newPhase = arkitectAdapter.getPhase();
    const newPatterns = arkitectAdapter.getPatterns();
    
    set({
      metrics: newMetrics,
      phase: newPhase,
      patterns: newPatterns
    });
  },

  // Ações de capacidades
  activateCapability: async (capability) => {
    const success = await arkitectAdapter.activateCapability(capability);
    if (success) {
      set(state => ({
        primaryCapabilities: [...state.primaryCapabilities, capability]
      }));
    }
    return success;
  },

  deactivateCapability: async (capability) => {
    const success = await arkitectAdapter.deactivateCapability(capability);
    if (success) {
      set(state => ({
        primaryCapabilities: state.primaryCapabilities.filter(cap => cap !== capability)
      }));
    }
    return success;
  },

  // Ações de padrões
  analyzePatterns: async () => {
    const newPatterns = await arkitectAdapter.analyzePatterns();
    set({ patterns: newPatterns });
  },

  // Otimizações avançadas
  optimizeResourceAllocation: async () => {
    const success = await arkitectAdapter.optimizeResources();
    if (success) {
      const newMetrics = arkitectAdapter.getMetrics();
      set({ metrics: newMetrics });
    }
    return success;
  },

  improveAdaptation: async () => {
    const success = await arkitectAdapter.improveAdaptation();
    if (success) {
      const newMetrics = arkitectAdapter.getMetrics();
      const newPhase = arkitectAdapter.getPhase();
      set({ 
        metrics: newMetrics,
        phase: newPhase
      });
    }
    return success;
  },

  // Ações de evolução
  evolveSystem: async () => {
    const evolutionResult = await arkitectAdapter.evolveSystem();
    if (evolutionResult.success) {
      set({
        metrics: evolutionResult.metrics,
        phase: evolutionResult.phase,
        patterns: evolutionResult.patterns,
        primaryCapabilities: [...evolutionResult.capabilities.primary],
        secondaryCapabilities: [...evolutionResult.capabilities.secondary]
      });
    }
    return evolutionResult.success;
  },

  // Análises e insights
  getSystemInsights: async () => {
    return await arkitectAdapter.analyzeSystem();
  },

  getPredictions: async () => {
    return await arkitectAdapter.predictBehavior();
  },

  // Funções de utilidade
  getMetricsHistory: () => {
    return arkitectAdapter.getMetrics().history;
  },

  getPhaseProgress: () => {
    return arkitectAdapter.getPhaseProgress();
  },

  getSystemHealth: () => {
    const metrics = arkitectAdapter.getMetrics();
    return (metrics.adaptiveCohesion + metrics.resourceBalance + metrics.evolutionStability) / 3;
  }
}));

export default useAdaptiveStore;
