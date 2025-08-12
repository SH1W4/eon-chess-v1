import create from 'zustand';

export type AdaptivePhase = 'initialization' | 'adaptation' | 'evolution' | 'autonomy';

interface AdaptiveMetrics {
  adaptiveCohesion: number;
  resourceBalance: number;
  evolutionStability: number;
}

interface AdaptiveState {
  phase: AdaptivePhase;
  metrics: AdaptiveMetrics;
  primaryCapabilities: string[];
  secondaryCapabilities: string[];
  setPhase: (phase: AdaptivePhase) => void;
  updateMetrics: (metrics: Partial<AdaptiveMetrics>) => void;
  addPrimaryCapability: (capability: string) => void;
  removePrimaryCapability: (capability: string) => void;
  addSecondaryCapability: (capability: string) => void;
  removeSecondaryCapability: (capability: string) => void;
}

const useAdaptiveStore = create<AdaptiveState>((set) => ({
  // Estado inicial
  phase: 'initialization',
  metrics: {
    adaptiveCohesion: 0,
    resourceBalance: 0,
    evolutionStability: 0
  },
  primaryCapabilities: [],
  secondaryCapabilities: [],

  // Ações
  setPhase: (phase) => set({ phase }),

  updateMetrics: (newMetrics) =>
    set((state) => ({
      metrics: {
        ...state.metrics,
        ...newMetrics
      }
    })),

  addPrimaryCapability: (capability) =>
    set((state) => ({
      primaryCapabilities: [...state.primaryCapabilities, capability]
    })),

  removePrimaryCapability: (capability) =>
    set((state) => ({
      primaryCapabilities: state.primaryCapabilities.filter(cap => cap !== capability)
    })),

  addSecondaryCapability: (capability) =>
    set((state) => ({
      secondaryCapabilities: [...state.secondaryCapabilities, capability]
    })),

  removeSecondaryCapability: (capability) =>
    set((state) => ({
      secondaryCapabilities: state.secondaryCapabilities.filter(cap => cap !== capability)
    }))
}));

export default useAdaptiveStore;
