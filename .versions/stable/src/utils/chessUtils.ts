import { 
  ChessBoard, 
  ChessPiece, 
  ChessPosition, 
  ChessMove, 
  PieceType, 
  PieceColor 
} from '../types/chess';

export const createInitialBoard = (): ChessBoard => {
  const squares: (ChessPiece | null)[][] = Array(8).fill(null).map(() => Array(8).fill(null));
  
  // Place pawns
  for (let col = 0; col < 8; col++) {
    squares[1][col] = createPiece('pawn', 'black', `bp${col}`);
    squares[6][col] = createPiece('pawn', 'white', `wp${col}`);
  }
  
  // Place other pieces
  const pieceOrder: PieceType[] = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'];
  
  for (let col = 0; col < 8; col++) {
    squares[0][col] = createPiece(pieceOrder[col], 'black', `b${pieceOrder[col]}${col}`);
    squares[7][col] = createPiece(pieceOrder[col], 'white', `w${pieceOrder[col]}${col}`);
  }
  
  return {
    squares,
    currentPlayer: 'white',
    moveHistory: [],
    isCheck: false,
    isCheckmate: false,
    isStalemate: false,
    canCastleKingside: { white: true, black: true },
    canCastleQueenside: { white: true, black: true },
  };
};

export const createPiece = (type: PieceType, color: PieceColor, id: string): ChessPiece => ({
  type,
  color,
  id,
  hasMoved: false,
});

export const getPieceSymbol = (piece: ChessPiece): string => {
  const symbols = {
    white: {
      king: '♔',
      queen: '♕',
      rook: '♖',
      bishop: '♗',
      knight: '♘',
      pawn: '♙',
    },
    black: {
      king: '♚',
      queen: '♛',
      rook: '♜',
      bishop: '♝',
      knight: '♞',
      pawn: '♟',
    },
  };
  
  return symbols[piece.color][piece.type];
};

export const isValidPosition = (position: ChessPosition): boolean => {
  return position.row >= 0 && position.row < 8 && position.col >= 0 && position.col < 8;
};

export const isSamePosition = (pos1: ChessPosition, pos2: ChessPosition): boolean => {
  return pos1.row === pos2.row && pos1.col === pos2.col;
};

export const getSquareColor = (row: number, col: number): 'light' | 'dark' => {
  return (row + col) % 2 === 0 ? 'light' : 'dark';
};

export const positionToAlgebraic = (position: ChessPosition): string => {
  const files = 'abcdefgh';
  const ranks = '87654321';
  return files[position.col] + ranks[position.row];
};

export const algebraicToPosition = (algebraic: string): ChessPosition => {
  const files = 'abcdefgh';
  const ranks = '87654321';
  return {
    col: files.indexOf(algebraic[0]),
    row: ranks.indexOf(algebraic[1]),
  };
};

export const getPossibleMoves = (
  board: ChessBoard, 
  position: ChessPosition
): ChessPosition[] => {
  const piece = board.squares[position.row][position.col];
  if (!piece) return [];
  
  const moves: ChessPosition[] = [];
  
  switch (piece.type) {
    case 'pawn':
      moves.push(...getPawnMoves(board, position, piece));
      break;
    case 'rook':
      moves.push(...getRookMoves(board, position, piece));
      break;
    case 'knight':
      moves.push(...getKnightMoves(board, position, piece));
      break;
    case 'bishop':
      moves.push(...getBishopMoves(board, position, piece));
      break;
    case 'queen':
      moves.push(...getQueenMoves(board, position, piece));
      break;
    case 'king':
      moves.push(...getKingMoves(board, position, piece));
      break;
  }
  
  return moves.filter(move => isValidPosition(move));
};

const getPawnMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  const moves: ChessPosition[] = [];
  const direction = piece.color === 'white' ? -1 : 1;
  const startRow = piece.color === 'white' ? 6 : 1;
  
  // Forward move
  const oneStep = { row: position.row + direction, col: position.col };
  if (isValidPosition(oneStep) && !board.squares[oneStep.row][oneStep.col]) {
    moves.push(oneStep);
    
    // Two steps from starting position
    if (position.row === startRow) {
      const twoSteps = { row: position.row + 2 * direction, col: position.col };
      if (isValidPosition(twoSteps) && !board.squares[twoSteps.row][twoSteps.col]) {
        moves.push(twoSteps);
      }
    }
  }
  
  // Captures
  const captureLeft = { row: position.row + direction, col: position.col - 1 };
  const captureRight = { row: position.row + direction, col: position.col + 1 };
  
  [captureLeft, captureRight].forEach(capture => {
    if (isValidPosition(capture)) {
      const targetPiece = board.squares[capture.row][capture.col];
      if (targetPiece && targetPiece.color !== piece.color) {
        moves.push(capture);
      }
    }
  });
  
  return moves;
};

const getRookMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  const moves: ChessPosition[] = [];
  const directions = [
    { row: 0, col: 1 },   // Right
    { row: 0, col: -1 },  // Left
    { row: 1, col: 0 },   // Down
    { row: -1, col: 0 },  // Up
  ];
  
  directions.forEach(direction => {
    for (let i = 1; i < 8; i++) {
      const newPos = {
        row: position.row + direction.row * i,
        col: position.col + direction.col * i,
      };
      
      if (!isValidPosition(newPos)) break;
      
      const targetPiece = board.squares[newPos.row][newPos.col];
      if (!targetPiece) {
        moves.push(newPos);
      } else {
        if (targetPiece.color !== piece.color) {
          moves.push(newPos);
        }
        break;
      }
    }
  });
  
  return moves;
};

const getKnightMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  const moves: ChessPosition[] = [];
  const knightMoves = [
    { row: -2, col: -1 }, { row: -2, col: 1 },
    { row: -1, col: -2 }, { row: -1, col: 2 },
    { row: 1, col: -2 },  { row: 1, col: 2 },
    { row: 2, col: -1 },  { row: 2, col: 1 },
  ];
  
  knightMoves.forEach(move => {
    const newPos = {
      row: position.row + move.row,
      col: position.col + move.col,
    };
    
    if (isValidPosition(newPos)) {
      const targetPiece = board.squares[newPos.row][newPos.col];
      if (!targetPiece || targetPiece.color !== piece.color) {
        moves.push(newPos);
      }
    }
  });
  
  return moves;
};

const getBishopMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  const moves: ChessPosition[] = [];
  const directions = [
    { row: 1, col: 1 },   // Down-right
    { row: 1, col: -1 },  // Down-left
    { row: -1, col: 1 },  // Up-right
    { row: -1, col: -1 }, // Up-left
  ];
  
  directions.forEach(direction => {
    for (let i = 1; i < 8; i++) {
      const newPos = {
        row: position.row + direction.row * i,
        col: position.col + direction.col * i,
      };
      
      if (!isValidPosition(newPos)) break;
      
      const targetPiece = board.squares[newPos.row][newPos.col];
      if (!targetPiece) {
        moves.push(newPos);
      } else {
        if (targetPiece.color !== piece.color) {
          moves.push(newPos);
        }
        break;
      }
    }
  });
  
  return moves;
};

const getQueenMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  return [
    ...getRookMoves(board, position, piece),
    ...getBishopMoves(board, position, piece),
  ];
};

const getKingMoves = (
  board: ChessBoard, 
  position: ChessPosition, 
  piece: ChessPiece
): ChessPosition[] => {
  const moves: ChessPosition[] = [];
  const kingMoves = [
    { row: -1, col: -1 }, { row: -1, col: 0 }, { row: -1, col: 1 },
    { row: 0, col: -1 },                       { row: 0, col: 1 },
    { row: 1, col: -1 },  { row: 1, col: 0 },  { row: 1, col: 1 },
  ];
  
  kingMoves.forEach(move => {
    const newPos = {
      row: position.row + move.row,
      col: position.col + move.col,
    };
    
    if (isValidPosition(newPos)) {
      const targetPiece = board.squares[newPos.row][newPos.col];
      if (!targetPiece || targetPiece.color !== piece.color) {
        moves.push(newPos);
      }
    }
  });
  
  return moves;
};

export const isValidMove = (board: ChessBoard, move: ChessMove): boolean => {
  const possibleMoves = getPossibleMoves(board, move.from);
  return possibleMoves.some(pos => isSamePosition(pos, move.to));
};

export const makeMove = (board: ChessBoard, move: ChessMove): ChessBoard => {
  const newBoard = JSON.parse(JSON.stringify(board)) as ChessBoard;
  
  // Move the piece
  newBoard.squares[move.to.row][move.to.col] = move.piece;
  newBoard.squares[move.from.row][move.from.col] = null;
  
  // Mark piece as moved
  if (newBoard.squares[move.to.row][move.to.col]) {
    newBoard.squares[move.to.row][move.to.col]!.hasMoved = true;
  }
  
  // Add move to history
  newBoard.moveHistory.push(move);
  
  // Switch current player
  newBoard.currentPlayer = newBoard.currentPlayer === 'white' ? 'black' : 'white';
  
  return newBoard;
};

export const boardToFEN = (board: ChessBoard): string => {
  // Simplified FEN generation
  let fen = '';
  
  for (let row = 0; row < 8; row++) {
    let emptyCount = 0;
    for (let col = 0; col < 8; col++) {
      const piece = board.squares[row][col];
      if (piece) {
        if (emptyCount > 0) {
          fen += emptyCount;
          emptyCount = 0;
        }
        const pieceChar = getPieceChar(piece);
        fen += piece.color === 'white' ? pieceChar.toUpperCase() : pieceChar.toLowerCase();
      } else {
        emptyCount++;
      }
    }
    if (emptyCount > 0) {
      fen += emptyCount;
    }
    if (row < 7) fen += '/';
  }
  
  fen += ` ${board.currentPlayer === 'white' ? 'w' : 'b'}`;
  
  return fen;
};

const getPieceChar = (piece: ChessPiece): string => {
  const chars = {
    king: 'k',
    queen: 'q',
    rook: 'r',
    bishop: 'b',
    knight: 'n',
    pawn: 'p',
  };
  return chars[piece.type];
};

