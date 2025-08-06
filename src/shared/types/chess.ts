// Tipos compartilhados entre web e mobile

export type PieceType = 'p' | 'n' | 'b' | 'r' | 'q' | 'k';
export type PieceColor = 'white' | 'black';

export interface ChessPiece {
  type: PieceType;
  color: PieceColor;
}

export interface ChessPosition {
  row: number;
  col: number;
}

export interface ChessMove {
  from: ChessPosition;
  to: ChessPosition;
  piece: ChessPiece;
  captured?: ChessPiece;
  promotion?: PieceType;
  isCheck?: boolean;
  isCheckmate?: boolean;
}

export interface GameState {
  id: string;
  fen: string;
  moveHistory: ChessMove[];
  currentPlayer: PieceColor;
  isCheck: boolean;
  isCheckmate: boolean;
  isDraw: boolean;
  status: 'active' | 'completed' | 'aborted';
  timeControl?: {
    initial: number;
    increment: number;
  };
}

export interface PlayerProfile {
  id: string;
  name: string;
  rating: number;
  culturalStyle?: string;
  preferences: {
    theme: string;
    pieceStyle: string;
    boardStyle: string;
    soundEnabled: boolean;
    animations: boolean;
  };
}

export interface GameAnalysis {
  accuracy_score: number;
  brilliant_moves_count: number;
  blunders_count: number;
  mistakes_count: number;
  inaccuracies_count: number;
  average_move_time: number;
  opening_accuracy: number;
  middlegame_score: number;
  endgame_score: number;
  opening_name: string;
  improvement_suggestions: string[];
  ai_commentary: string;
}

export interface CulturalContext {
  theme: string;
  narratives: string[];
  eventTriggers: {
    condition: string;
    effect: string;
  }[];
  styleModifiers: {
    pieces?: string;
    board?: string;
    animations?: string;
  };
}

// Interfaces para integração com ARQUIMAX
export interface ArquimaxMetrics {
  performance: {
    responseTime: number;
    renderTime: number;
    memoryUsage: number;
  };
  usage: {
    activeUsers: number;
    gamesInProgress: number;
    analyticsRequests: number;
  };
  quality: {
    errorRate: number;
    crashRate: number;
    userSatisfaction: number;
  };
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'critical';
  components: {
    [key: string]: {
      status: 'up' | 'down' | 'degraded';
      lastCheck: Date;
      metrics: Record<string, number>;
    };
  };
  lastUpdate: Date;
}

// Tipos para o sistema de cache
export interface CacheConfig {
  ttl: number;
  maxSize: number;
  invalidationStrategy: 'lru' | 'fifo' | 'custom';
  warmupRules: {
    pattern: string;
    priority: number;
  }[];
}

// Tipos para eventos e mensagens
export type GameEvent = 
  | { type: 'MOVE_MADE'; payload: ChessMove }
  | { type: 'GAME_STARTED'; payload: GameState }
  | { type: 'GAME_ENDED'; payload: GameState }
  | { type: 'ANALYSIS_READY'; payload: GameAnalysis }
  | { type: 'CULTURAL_EVENT'; payload: CulturalContext };
