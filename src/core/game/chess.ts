export type PieceType = 'pawn' | 'rook' | 'knight' | 'bishop' | 'queen' | 'king';
export type PieceColor = 'white' | 'black';

export interface ChessPiece {
  type: PieceType;
  color: PieceColor;
  id: string;
  hasMoved?: boolean;
}

export interface ChessPosition {
  row: number;
  col: number;
}

export interface ChessMove {
  from: ChessPosition;
  to: ChessPosition;
  piece: ChessPiece;
  capturedPiece?: ChessPiece;
  isEnPassant?: boolean;
  isCastling?: boolean;
  isPromotion?: boolean;
  promotionPiece?: PieceType;
  timestamp: number;
}

export interface ChessBoard {
  squares: (ChessPiece | null)[][];
  currentPlayer: PieceColor;
  moveHistory: ChessMove[];
  isCheck: boolean;
  isCheckmate: boolean;
  isStalemate: boolean;
  canCastleKingside: { white: boolean; black: boolean };
  canCastleQueenside: { white: boolean; black: boolean };
  enPassantTarget?: ChessPosition;
}

export interface GameState {
  board: ChessBoard;
  gameId: string;
  players: {
    white: Player;
    black: Player;
  };
  gameMode: GameMode;
  status: GameStatus;
  startTime: number;
  endTime?: number;
  result?: GameResult;
  analysis?: GameAnalysis;
}

export type GameMode = 'casual' | 'ranked' | 'training' | 'cultural' | 'ai';
export type GameStatus = 'waiting' | 'active' | 'paused' | 'finished';
export type GameResult = 'white_wins' | 'black_wins' | 'draw' | 'abandoned';

export interface Player {
  id: string;
  name: string;
  rating?: number;
  avatar?: string;
  isAI?: boolean;
  aiLevel?: number;
}

export interface GameAnalysis {
  accuracy: { white: number; black: number };
  blunders: ChessMove[];
  mistakes: ChessMove[];
  bestMoves: ChessMove[];
  openingName?: string;
  evaluation: number[];
  timeSpent: number[];
  insights: AnalysisInsight[];
}

export interface AnalysisInsight {
  type: 'tactical' | 'positional' | 'endgame' | 'opening';
  message: string;
  moveNumber: number;
  severity: 'info' | 'warning' | 'error';
  suggestion?: string;
}

export interface ChessEngine {
  evaluatePosition(board: ChessBoard): number;
  getBestMove(board: ChessBoard, depth: number): ChessMove | null;
  isValidMove(board: ChessBoard, move: ChessMove): boolean;
  makeMove(board: ChessBoard, move: ChessMove): ChessBoard;
  getLegalMoves(board: ChessBoard, position: ChessPosition): ChessPosition[];
  isInCheck(board: ChessBoard, color: PieceColor): boolean;
  isCheckmate(board: ChessBoard, color: PieceColor): boolean;
  isStalemate(board: ChessBoard, color: PieceColor): boolean;
}

