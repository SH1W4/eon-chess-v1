import { ChessPosition, ChessPiece } from '../types/chess';
import { BOARD_SIZE, PIECE_SYMBOLS } from '../constants/game';

/**
 * Converte coordenadas algébricas (ex: "e4") para coordenadas internas (row, col)
 */
export function algebraicToCoords(square: string): ChessPosition {
  const col = square.charCodeAt(0) - 'a'.charCodeAt(0);
  const row = BOARD_SIZE - parseInt(square[1]);
  return { row, col };
}

/**
 * Converte coordenadas internas (row, col) para notação algébrica (ex: "e4")
 */
export function coordsToAlgebraic(position: ChessPosition): string {
  const { row, col } = position;
  const file = String.fromCharCode('a'.charCodeAt(0) + col);
  const rank = BOARD_SIZE - row;
  return `${file}${rank}`;
}

/**
 * Verifica se uma posição está dentro do tabuleiro
 */
export function isValidPosition(position: ChessPosition): boolean {
  const { row, col } = position;
  return row >= 0 && row < BOARD_SIZE && col >= 0 && col < BOARD_SIZE;
}

/**
 * Compara duas posições
 */
export function isSamePosition(a: ChessPosition, b: ChessPosition): boolean {
  return a.row === b.row && a.col === b.col;
}

/**
 * Retorna a cor de uma casa do tabuleiro
 */
export function getSquareColor(row: number, col: number): 'light' | 'dark' {
  return (row + col) % 2 === 0 ? 'light' : 'dark';
}

/**
 * Retorna o símbolo Unicode para uma peça
 */
export function getPieceSymbol(piece: ChessPiece): string {
  const symbol = piece.color === 'white' 
    ? piece.type.toUpperCase() 
    : piece.type.toLowerCase();
  return PIECE_SYMBOLS[symbol] || '';
}

/**
 * Gera array com todas as posições do tabuleiro
 */
export function getAllSquares(): ChessPosition[] {
  const squares: ChessPosition[] = [];
  for (let row = 0; row < BOARD_SIZE; row++) {
    for (let col = 0; col < BOARD_SIZE; col++) {
      squares.push({ row, col });
    }
  }
  return squares;
}

/**
 * Retorna as coordenadas das casas destacadas para um movimento
 */
export function getHighlightedSquares(
  selectedSquare: ChessPosition | null,
  lastMove: { from: ChessPosition; to: ChessPosition } | null,
  possibleMoves: ChessPosition[]
): {
  selected: ChessPosition | null;
  lastMove: { from: ChessPosition; to: ChessPosition } | null;
  possible: ChessPosition[];
} {
  return {
    selected: selectedSquare,
    lastMove,
    possible: possibleMoves,
  };
}

/**
 * Retorna a distância entre duas casas
 */
export function getSquareDistance(a: ChessPosition, b: ChessPosition): number {
  const rowDiff = Math.abs(a.row - b.row);
  const colDiff = Math.abs(a.col - b.col);
  return Math.max(rowDiff, colDiff);
}

/**
 * Retorna a direção do movimento entre duas casas
 */
export function getMoveDirection(
  from: ChessPosition,
  to: ChessPosition
): { rowDir: number; colDir: number } {
  const rowDir = Math.sign(to.row - from.row);
  const colDir = Math.sign(to.col - from.col);
  return { rowDir, colDir };
}

/**
 * Verifica se um movimento é diagonal
 */
export function isDiagonalMove(from: ChessPosition, to: ChessPosition): boolean {
  const rowDiff = Math.abs(to.row - from.row);
  const colDiff = Math.abs(to.col - from.col);
  return rowDiff === colDiff && rowDiff > 0;
}

/**
 * Verifica se um movimento é ortogonal (horizontal ou vertical)
 */
export function isOrthogonalMove(from: ChessPosition, to: ChessPosition): boolean {
  return (from.row === to.row && from.col !== to.col) ||
         (from.col === to.col && from.row !== to.row);
}

/**
 * Calcula o caminho entre duas casas (para verificar obstruções)
 */
export function getPathBetween(
  from: ChessPosition,
  to: ChessPosition
): ChessPosition[] {
  const path: ChessPosition[] = [];
  const { rowDir, colDir } = getMoveDirection(from, to);
  let { row, col } = from;

  while (row !== to.row || col !== to.col) {
    row += rowDir;
    col += colDir;
    if (row === to.row && col === to.col) break;
    path.push({ row, col });
  }

  return path;
}

/**
 * Formata um movimento para notação algébrica
 */
export function formatMove(
  from: ChessPosition,
  to: ChessPosition,
  piece: ChessPiece,
  capture?: boolean,
  promotion?: string
): string {
  const fromSquare = coordsToAlgebraic(from);
  const toSquare = coordsToAlgebraic(to);
  const pieceSymbol = piece.type.toUpperCase();
  const captureSymbol = capture ? 'x' : '';
  const promotionSymbol = promotion ? `=${promotion.toUpperCase()}` : '';

  return `${pieceSymbol}${fromSquare}${captureSymbol}${toSquare}${promotionSymbol}`;
}
