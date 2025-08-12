import { ChessBoard, ChessPiece, PieceType, PieceColor } from '../types/chess';

export function createInitialBoard(): ChessBoard {
  const squares: (ChessPiece | null)[][] = Array(8).fill(null).map(() => Array(8).fill(null));
  
  // Setup pawns
  for (let col = 0; col < 8; col++) {
    squares[1][col] = { type: 'pawn', color: 'black' };
    squares[6][col] = { type: 'pawn', color: 'white' };
  }
  
  // Setup other pieces
  const pieceOrder: PieceType[] = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
  
  for (let col = 0; col < 8; col++) {
    squares[0][col] = { type: pieceOrder[col], color: 'black' };
    squares[7][col] = { type: pieceOrder[col], color: 'white' };
  }
  
  return {
    squares,
    currentPlayer: 'white',
    moveHistory: [],
    capturedPieces: {
      white: [],
      black: []
    }
  };
}

export function getPieceSymbol(piece: ChessPiece): string {
  const symbols = {
    white: {
      king: '♔',
      queen: '♕',
      rook: '♖',
      bishop: '♗',
      knight: '♘',
      pawn: '♙'
    },
    black: {
      king: '♚',
      queen: '♛',
      rook: '♜',
      bishop: '♝',
      knight: '♞',
      pawn: '♟'
    }
  };
  
  return symbols[piece.color][piece.type];
}

export function squareToNotation(row: number, col: number): string {
  const file = String.fromCharCode(97 + col); // a-h
  const rank = 8 - row; // 8-1
  return `${file}${rank}`;
}

export function notationToSquare(notation: string): { row: number; col: number } {
  const file = notation.charCodeAt(0) - 97; // a-h to 0-7
  const rank = parseInt(notation[1]); // 1-8
  return { row: 8 - rank, col: file };
}
