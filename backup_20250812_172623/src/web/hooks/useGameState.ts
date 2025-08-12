import { useState, useCallback, useEffect } from 'react';
import { ChessPosition, ChessPiece, GameState, ChessMove } from '../../shared/types/chess';
import { INITIAL_FEN, GAME_STATUS } from '../../shared/constants/game';
import { generateId } from '../../shared/utils/id';
import { 
  algebraicToCoords,
  coordsToAlgebraic,
  isValidPosition,
  isSamePosition,
} from '../../shared/utils/chess';

interface UseGameStateProps {
  initialFen?: string;
  culturalStyle?: string;
  timeControl?: {
    initial: number;
    increment: number;
  };
}

interface UseGameStateReturn {
  gameState: GameState;
  selectedSquare: ChessPosition | null;
  possibleMoves: ChessPosition[];
  lastMove: ChessMove | null;
  pieceAt: (position: ChessPosition) => ChessPiece | undefined;
  selectSquare: (position: ChessPosition | null) => void;
  makeMove: (from: ChessPosition, to: ChessPosition) => boolean;
  resetGame: () => void;
  undoLastMove: () => void;
  isCheck: boolean;
  isCheckmate: boolean;
  isDraw: boolean;
  currentPlayer: 'white' | 'black';
}

export function useGameState({
  initialFen = INITIAL_FEN,
  culturalStyle = 'modern',
  timeControl,
}: UseGameStateProps = {}): UseGameStateReturn {
  // Estado do jogo
  const [gameState, setGameState] = useState<GameState>({
    id: generateId(),
    fen: initialFen,
    moveHistory: [],
    currentPlayer: 'white',
    isCheck: false,
    isCheckmate: false,
    isDraw: false,
    status: GAME_STATUS.ACTIVE,
    timeControl,
  });

  // Estado da interface
  const [selectedSquare, setSelectedSquare] = useState<ChessPosition | null>(null);
  const [possibleMoves, setPossibleMoves] = useState<ChessPosition[]>([]);
  const [lastMove, setLastMove] = useState<ChessMove | null>(null);

  // Reseta o jogo para o estado inicial
  const resetGame = useCallback(() => {
    setGameState({
      id: generateId(),
      fen: initialFen,
      moveHistory: [],
      currentPlayer: 'white',
      isCheck: false,
      isCheckmate: false,
      isDraw: false,
      status: GAME_STATUS.ACTIVE,
      timeControl,
    });
    setSelectedSquare(null);
    setPossibleMoves([]);
    setLastMove(null);
  }, [initialFen, timeControl]);

  // Retorna a peça em uma posição específica
  const pieceAt = useCallback((position: ChessPosition): ChessPiece | undefined => {
    const { row, col } = position;
    const fenParts = gameState.fen.split(' ');
    const boardFen = fenParts[0];
    const ranks = boardFen.split('/');

    // Converte a posição do tabuleiro para o índice no FEN
    let currentRank = ranks[row];
    let currentCol = 0;

    for (let i = 0; i < currentRank.length; i++) {
      const char = currentRank[i];
      if (isNaN(parseInt(char))) {
        if (currentCol === col) {
          const isWhite = char === char.toUpperCase();
          const pieceType = char.toLowerCase();
          return {
            type: pieceType,
            color: isWhite ? 'white' : 'black'
          };
        }
        currentCol++;
      } else {
        currentCol += parseInt(char);
        if (currentCol > col) {
          return undefined;
        }
      }
    }

    return undefined;
  }, [gameState.fen]);

  // Calcula movimentos possíveis para uma peça
  const calculatePossibleMoves = useCallback((position: ChessPosition, piece: ChessPiece): ChessPosition[] => {
    const moves: ChessPosition[] = [];
    const { row, col } = position;

    // Direções de movimento por tipo de peça
    const directions: { row: number; col: number }[] = [];
    
    switch (piece.type) {
      case 'p': // Peão
        const direction = piece.color === 'white' ? -1 : 1;
        const startRow = piece.color === 'white' ? 6 : 1;
        
        // Movimento para frente
        if (isValidPosition({ row: row + direction, col }) && !pieceAt({ row: row + direction, col })) {
          moves.push({ row: row + direction, col });
          // Movimento duplo inicial
          if (row === startRow && !pieceAt({ row: row + 2 * direction, col })) {
            moves.push({ row: row + 2 * direction, col });
          }
        }
        
        // Capturas diagonais
        for (const dx of [-1, 1]) {
          const newPos = { row: row + direction, col: col + dx };
          if (isValidPosition(newPos)) {
            const targetPiece = pieceAt(newPos);
            if (targetPiece && targetPiece.color !== piece.color) {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'n': // Cavalo
        const knightMoves = [
          { row: -2, col: -1 }, { row: -2, col: 1 },
          { row: -1, col: -2 }, { row: -1, col: 2 },
          { row: 1, col: -2 }, { row: 1, col: 2 },
          { row: 2, col: -1 }, { row: 2, col: 1 },
        ];
        for (const move of knightMoves) {
          const newPos = { row: row + move.row, col: col + move.col };
          if (isValidPosition(newPos)) {
            const targetPiece = pieceAt(newPos);
            if (!targetPiece || targetPiece.color !== piece.color) {
              moves.push(newPos);
            }
          }
        }
        break;

      case 'b': // Bispo
        directions.push(
          { row: -1, col: -1 }, { row: -1, col: 1 },
          { row: 1, col: -1 }, { row: 1, col: 1 }
        );
        break;

      case 'r': // Torre
        directions.push(
          { row: -1, col: 0 }, { row: 1, col: 0 },
          { row: 0, col: -1 }, { row: 0, col: 1 }
        );
        break;

      case 'q': // Rainha
        directions.push(
          { row: -1, col: -1 }, { row: -1, col: 0 }, { row: -1, col: 1 },
          { row: 0, col: -1 }, { row: 0, col: 1 },
          { row: 1, col: -1 }, { row: 1, col: 0 }, { row: 1, col: 1 }
        );
        break;

      case 'k': // Rei
        directions.push(
          { row: -1, col: -1 }, { row: -1, col: 0 }, { row: -1, col: 1 },
          { row: 0, col: -1 }, { row: 0, col: 1 },
          { row: 1, col: -1 }, { row: 1, col: 0 }, { row: 1, col: 1 }
        );
        break;
    }

    // Processa movimentos nas direções permitidas
    for (const dir of directions) {
      let distance = piece.type === 'k' ? 1 : 7;
      for (let i = 1; i <= distance; i++) {
        const newPos = {
          row: row + dir.row * i,
          col: col + dir.col * i
        };

        if (!isValidPosition(newPos)) break;

        const targetPiece = pieceAt(newPos);
        if (!targetPiece) {
          moves.push(newPos);
        } else {
          if (targetPiece.color !== piece.color) {
            moves.push(newPos);
          }
          break;
        }
      }
    }

    return moves;
  }, [pieceAt]);

  // Seleciona uma casa e calcula movimentos possíveis
  const selectSquare = useCallback((position: ChessPosition | null) => {
    if (!position) {
      setSelectedSquare(null);
      setPossibleMoves([]);
      return;
    }

    const piece = pieceAt(position);
    if (!piece || piece.color !== gameState.currentPlayer) {
      setSelectedSquare(null);
      setPossibleMoves([]);
      return;
    }

    setSelectedSquare(position);
    setPossibleMoves(calculatePossibleMoves(position, piece));
  }, [gameState.currentPlayer, pieceAt, calculatePossibleMoves]);

  // Executa um movimento
  const makeMove = useCallback((from: ChessPosition, to: ChessPosition): boolean => {
    if (!isValidPosition(from) || !isValidPosition(to)) {
      return false;
    }

    const piece = pieceAt(from);
    if (!piece || piece.color !== gameState.currentPlayer) {
      return false;
    }

    const isValidMove = possibleMoves.some(move => isSamePosition(move, to));
    if (!isValidMove) {
      return false;
    }

    // TODO: Implementar lógica de movimento e atualização do estado do jogo
    const capturedPiece = pieceAt(to);
    const move: ChessMove = {
      from,
      to,
      piece,
      captured: capturedPiece,
    };

    setGameState(prev => ({
      ...prev,
      currentPlayer: prev.currentPlayer === 'white' ? 'black' : 'white',
      moveHistory: [...prev.moveHistory, move],
    }));

    setLastMove(move);
    setSelectedSquare(null);
    setPossibleMoves([]);

    return true;
  }, [gameState.currentPlayer, pieceAt, possibleMoves]);

  // Desfaz o último movimento
  const undoLastMove = useCallback(() => {
    if (gameState.moveHistory.length === 0) {
      return;
    }

    // TODO: Implementar lógica para desfazer o último movimento
    setGameState(prev => ({
      ...prev,
      moveHistory: prev.moveHistory.slice(0, -1),
      currentPlayer: prev.currentPlayer === 'white' ? 'black' : 'white',
    }));

    setLastMove(null);
    setSelectedSquare(null);
    setPossibleMoves([]);
  }, [gameState.moveHistory]);

  // Atualiza o estado quando o FEN inicial muda
  useEffect(() => {
    resetGame();
  }, [initialFen, resetGame]);

  return {
    gameState,
    selectedSquare,
    possibleMoves,
    lastMove,
    pieceAt,
    selectSquare,
    makeMove,
    resetGame,
    undoLastMove,
    isCheck: gameState.isCheck,
    isCheckmate: gameState.isCheckmate,
    isDraw: gameState.isDraw,
    currentPlayer: gameState.currentPlayer,
  };
}
