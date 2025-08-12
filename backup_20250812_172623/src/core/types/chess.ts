export type PieceColor = 'white' | 'black';
export type PieceType = 'king' | 'queen' | 'rook' | 'bishop' | 'knight' | 'pawn';
export type GameMode = 'classic' | 'adaptive' | 'coaching' | 'analysis';
export type GameStatus = 'active' | 'check' | 'checkmate' | 'stalemate' | 'draw';

export interface ChessPosition {
  row: number;
  col: number;
}

export interface ChessPiece {
  type: PieceType;
  color: PieceColor;
  hasMoved?: boolean;
}

export interface ChessMove {
  from: ChessPosition;
  to: ChessPosition;
  piece: ChessPiece;
  captured?: ChessPiece;
  promotion?: PieceType;
  castling?: 'kingside' | 'queenside';
  enPassant?: boolean;
  timestamp: number;
}

export interface ChessBoard {
  squares: (ChessPiece | null)[][];
  currentPlayer: PieceColor;
  moveHistory: ChessMove[];
  capturedPieces: {
    white: ChessPiece[];
    black: ChessPiece[];
  };
}

export interface Player {
  id: string;
  name: string;
  rating?: number;
  isAI?: boolean;
  aiLevel?: number;
}

export interface GameState {
  gameId: string;
  board: ChessBoard;
  players: {
    white: Player;
    black: Player;
  };
  gameMode: GameMode;
  status: GameStatus;
  startTime: number;
  endTime?: number;
  winner?: PieceColor;
}
