import { ChessPosition, ChessPiece, ChessMove } from './chess';

export interface ChessEngine {
  // Estado do jogo
  getBoard(): ChessPiece[][];
  getFEN(): string;
  setFEN(fen: string): void;
  
  // Movimentos
  getPossibleMoves(position: ChessPosition): ChessMove[];
  makeMove(from: ChessPosition, to: ChessPosition): boolean;
  undoLastMove(): boolean;
  
  // Estado do jogo
  isCheck(): boolean;
  isCheckmate(): boolean;
  isDraw(): boolean;
  isGameOver(): boolean;
  getCurrentPlayer(): 'white' | 'black';
  
  // Avaliação e análise
  evaluatePosition(): number;
  getBestMove(depth: number): ChessMove | null;
  getGameHistory(): ChessMove[];
  
  // Validação
  isValidMove(from: ChessPosition, to: ChessPosition): boolean;
  isValidPosition(position: ChessPosition): boolean;
  
  // Utilidades
  reset(): void;
  clone(): ChessEngine;
}

export interface EngineOptions {
  startPosition?: string;
  timeControl?: {
    initial: number;
    increment: number;
  };
  skillLevel?: number;
  openingBook?: string;
  evaluationParameters?: {
    materialWeight: number;
    positionWeight: number;
    mobilityWeight: number;
    kingSafetyWeight: number;
    pawnStructureWeight: number;
  };
}

export interface EngineAnalysis {
  evaluation: number;
  depth: number;
  bestLine: ChessMove[];
  threats: {
    position: ChessPosition;
    type: 'pin' | 'fork' | 'skewer' | 'discovery';
    severity: number;
  }[];
  positionalFeatures: {
    pawnStructure: number;
    kingSafety: number;
    mobility: number;
    centerControl: number;
    pieceActivity: number;
  };
}

export interface CulturalEngineExtension {
  // Adaptação cultural
  setCulturalStyle(style: string): void;
  getCulturalNarrative(): string[];
  getStyleBasedEvaluation(): {
    style: string;
    evaluation: number;
    explanation: string;
  };
  
  // Eventos culturais
  triggerCulturalEvent(type: string): void;
  getCulturalEventHistory(): {
    type: string;
    timestamp: number;
    description: string;
  }[];
  
  // Análise cultural
  analyzePlayStyle(): {
    dominantStyle: string;
    styleMetrics: Record<string, number>;
    recommendations: string[];
  };
}

// Tipos de eventos do motor
export type EngineEvent = 
  | { type: 'MOVE_MADE'; move: ChessMove }
  | { type: 'POSITION_CHANGED'; fen: string }
  | { type: 'GAME_OVER'; result: string }
  | { type: 'CHECK'; kingPosition: ChessPosition }
  | { type: 'ANALYSIS_READY'; analysis: EngineAnalysis }
  | { type: 'CULTURAL_EVENT'; event: { type: string; description: string } };
