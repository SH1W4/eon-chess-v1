import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { 
  GameState, 
  ChessBoard, 
  ChessMove, 
  ChessPosition, 
  PieceColor,
  GameMode,
  Player 
} from '../types/chess';
import { AIProfile, AICoachingSession } from '../types/ai';
import { createInitialBoard } from '../utils/chessUtils';

interface GameStore {
  // Game State
  currentGame: GameState | null;
  gameHistory: GameState[];
  
  // User State
  currentUser: Player | null;
  aiProfile: AIProfile | null;
  
  // AI Coaching
  activeCoachingSession: AICoachingSession | null;
  coachingHistory: AICoachingSession[];
  
  // UI State
  selectedSquare: ChessPosition | null;
  possibleMoves: ChessPosition[];
  isThinking: boolean;
  showAnalysis: boolean;
  
  // Actions
  startNewGame: (mode: GameMode, opponent?: Player) => void;
  makeMove: (move: ChessMove) => void;
  selectSquare: (position: ChessPosition) => void;
  clearSelection: () => void;
  setUser: (user: Player) => void;
  updateAIProfile: (profile: Partial<AIProfile>) => void;
  startCoachingSession: (type: string) => void;
  endCoachingSession: () => void;
  toggleAnalysis: () => void;
  resetGame: () => void;
}

export const useGameStore = create<GameStore>()(
  persist(
    (set, get) => ({
      // Initial State
      currentGame: null,
      gameHistory: [],
      currentUser: null,
      aiProfile: null,
      activeCoachingSession: null,
      coachingHistory: [],
      selectedSquare: null,
      possibleMoves: [],
      isThinking: false,
      showAnalysis: false,

      // Actions
      startNewGame: (mode: GameMode, opponent?: Player) => {
        const user = get().currentUser;
        if (!user) return;

        const newGame: GameState = {
          gameId: `game_${Date.now()}`,
          board: createInitialBoard(),
          players: {
            white: user,
            black: opponent || { 
              id: 'ai', 
              name: 'EstrategiX', 
              isAI: true, 
              aiLevel: 5 
            }
          },
          gameMode: mode,
          status: 'active',
          startTime: Date.now(),
        };

        set({ 
          currentGame: newGame,
          selectedSquare: null,
          possibleMoves: [],
          isThinking: false 
        });
      },

      makeMove: (move: ChessMove) => {
        const { currentGame } = get();
        if (!currentGame || currentGame.status !== 'active') return;

        // Update board with the move
        const newBoard = { ...currentGame.board };
        newBoard.moveHistory = [...newBoard.moveHistory, move];
        
        // Switch current player
        newBoard.currentPlayer = newBoard.currentPlayer === 'white' ? 'black' : 'white';

        const updatedGame: GameState = {
          ...currentGame,
          board: newBoard,
        };

        set({ 
          currentGame: updatedGame,
          selectedSquare: null,
          possibleMoves: [],
          isThinking: newBoard.currentPlayer === 'black' && currentGame.players.black.isAI
        });

        // If it's AI's turn, trigger AI move after a delay
        if (newBoard.currentPlayer === 'black' && currentGame.players.black.isAI) {
          setTimeout(() => {
            // This would call the AI engine to make a move
            // For now, we'll just clear the thinking state
            set({ isThinking: false });
          }, 1000);
        }
      },

      selectSquare: (position: ChessPosition) => {
        const { currentGame, selectedSquare } = get();
        if (!currentGame) return;

        // If same square is selected, clear selection
        if (selectedSquare && 
            selectedSquare.row === position.row && 
            selectedSquare.col === position.col) {
          set({ selectedSquare: null, possibleMoves: [] });
          return;
        }

        // If a square is already selected, try to make a move
        if (selectedSquare) {
          const move: ChessMove = {
            from: selectedSquare,
            to: position,
            piece: currentGame.board.squares[selectedSquare.row][selectedSquare.col]!,
            timestamp: Date.now(),
          };
          
          // Validate and make move (simplified for now)
          get().makeMove(move);
          return;
        }

        // Select new square if it has a piece of the current player
        const piece = currentGame.board.squares[position.row][position.col];
        if (piece && piece.color === currentGame.board.currentPlayer) {
          // Calculate possible moves (simplified for now)
          const possibleMoves: ChessPosition[] = [];
          
          set({ 
            selectedSquare: position, 
            possibleMoves 
          });
        }
      },

      clearSelection: () => {
        set({ selectedSquare: null, possibleMoves: [] });
      },

      setUser: (user: Player) => {
        set({ currentUser: user });
      },

      updateAIProfile: (profile: Partial<AIProfile>) => {
        const { aiProfile } = get();
        if (aiProfile) {
          set({ aiProfile: { ...aiProfile, ...profile } });
        }
      },

      startCoachingSession: (type: string) => {
        const user = get().currentUser;
        if (!user) return;

        const session: AICoachingSession = {
          id: `session_${Date.now()}`,
          userId: user.id,
          type: type as any,
          startTime: Date.now(),
          insights: [],
          exercises: [],
          feedback: [],
        };

        set({ activeCoachingSession: session });
      },

      endCoachingSession: () => {
        const { activeCoachingSession, coachingHistory } = get();
        if (activeCoachingSession) {
          const completedSession = {
            ...activeCoachingSession,
            endTime: Date.now(),
          };
          
          set({ 
            activeCoachingSession: null,
            coachingHistory: [...coachingHistory, completedSession]
          });
        }
      },

      toggleAnalysis: () => {
        set((state) => ({ showAnalysis: !state.showAnalysis }));
      },

      resetGame: () => {
        set({
          currentGame: null,
          selectedSquare: null,
          possibleMoves: [],
          isThinking: false,
          showAnalysis: false,
        });
      },
    }),
    {
      name: 'xadrezmaster-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        currentUser: state.currentUser,
        aiProfile: state.aiProfile,
        gameHistory: state.gameHistory,
        coachingHistory: state.coachingHistory,
      }),
    }
  )
);

