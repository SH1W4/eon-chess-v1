
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { Chess } from 'chess.js';

interface ChessState {
  game: Chess;
  evaluation: number;
  history: any[];
  aiLevel: 'beginner' | 'club' | 'master';
  culturalContext: string;
}

export const useChessStore = create<ChessState>()(
  immer((set, get) => ({
    game: new Chess(),
    evaluation: 0,
    history: [],
    aiLevel: 'club',
    culturalContext: 'classical',
    
    makeMove: (move: any) => set((state) => {
      state.game.move(move);
      state.history.push(move);
      state.evaluation = calculateEvaluation(state.game);
    }),
    
    setAIIntelligence: (level: 'beginner' | 'club' | 'master') => set((state) => {
      state.aiLevel = level;
    }),
    
    resetGame: () => set((state) => {
      state.game = new Chess();
      state.history = [];
      state.evaluation = 0;
    })
  }))
);

function calculateEvaluation(game: Chess): number {
  // Implementação da avaliação
  return 0;
}
