import { create } from 'zustand';

interface SymbioticMetrics {
  symbioticCohesion: number;
  resourceBalance: number;
  emergenceStability: number;
}

interface SymbioticState {
  metrics: SymbioticMetrics;
  phase: 'nucleation' | 'symbiogenesis' | 'emergence' | 'homeostasis';
  hostCapabilities: string[];
  guestCapabilities: string[];
  updateMetrics: (newMetrics: Partial\u003cSymbioticMetrics\u003e) => void;
  setPhase: (phase: SymbioticState['phase']) => void;
  addHostCapability: (capability: string) => void;
  addGuestCapability: (capability: string) => void;
  removeHostCapability: (capability: string) => void;
  removeGuestCapability: (capability: string) => void;
}

const useSymbioticStore = create\u003cSymbioticState\u003e((set) => ({
  metrics: {
    symbioticCohesion: 0.85,
    resourceBalance: 0.75,
    emergenceStability: 0.92,
  },
  phase: 'nucleation',
  hostCapabilities: [
    'resource_management',
    'state_monitoring',
    'event_propagation',
  ],
  guestCapabilities: [
    'resource_consumption',
    'state_reflection',
    'event_handling',
  ],
  updateMetrics: (newMetrics) =>
    set((state) => ({
      metrics: { ...state.metrics, ...newMetrics },
    })),
  setPhase: (phase) => set({ phase }),
  addHostCapability: (capability) =>
    set((state) => ({
      hostCapabilities: [...state.hostCapabilities, capability],
    })),
  addGuestCapability: (capability) =>
    set((state) => ({
      guestCapabilities: [...state.guestCapabilities, capability],
    })),
  removeHostCapability: (capability) =>
    set((state) => ({
      hostCapabilities: state.hostCapabilities.filter((cap) => cap !== capability),
    })),
  removeGuestCapability: (capability) =>
    set((state) => ({
      guestCapabilities: state.guestCapabilities.filter((cap) => cap !== capability),
    })),
}));

export default useSymbioticStore;
