export enum PieceColor {
  WHITE = 'white',
  BLACK = 'black'
}

export interface Position {
  x: number;
  y: number;
}

export interface ChessMove {
  from: Position;
  to: Position;
  piece: string;
  captured?: string;
  promotion?: string;
  castling?: boolean;
  enPassant?: boolean;
}

export interface GameAnalysis {
  evaluation: number;
  bestMove: ChessMove | null;
  depth: number;
  nodes: number;
  time: number;
  pv: ChessMove[];
}
