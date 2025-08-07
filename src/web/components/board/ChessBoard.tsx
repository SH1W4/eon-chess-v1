import React, { useState, useCallback, useMemo } from 'react';
import { ChessPosition, ChessPiece } from '../../../shared/types/chess';
import { useGameState } from '../../hooks/useGameState';
import { MemoizedSquare } from './Square';
import { MemoizedPiece } from './Piece';
import { BOARD_SIZE } from '../../../shared/constants/game';

interface ChessBoardProps {
  initialFen?: string;
  orientation?: 'white' | 'black';
  culturalStyle?: string;
  showCoordinates?: boolean;
  onMove?: (from: ChessPosition, to: ChessPosition) => void;
  onGameEnd?: (result: string) => void;
}

export const ChessBoard: React.FC<ChessBoardProps> = ({
  initialFen,
  orientation = 'white',
  culturalStyle = 'modern',
  showCoordinates = true,
  onMove,
  onGameEnd,
}) => {
  // Estado do jogo
  const {
    gameState,
    selectedSquare,
    possibleMoves,
    lastMove,
    pieceAt,
    selectSquare,
    makeMove,
  } = useGameState({
    initialFen,
    culturalStyle,
  });

  // Estado de arrastar e soltar
  const [draggedPiece, setDraggedPiece] = useState<{
    piece: ChessPiece;
    position: ChessPosition;
  } | null>(null);

  // Calcula o tamanho do tabuleiro baseado no container
  const boardSize = useMemo(() => {
    // TODO: Implementar lógica de responsividade
    return 400; // Tamanho fixo para exemplo
  }, []);

  const squareSize = boardSize / BOARD_SIZE;

  // Manipuladores de eventos de arrastar e soltar
  const handleDragStart = useCallback((
    position: ChessPosition,
    piece: ChessPiece,
    e: React.DragEvent
  ) => {
    if (piece.color !== gameState.currentPlayer) {
      e.preventDefault();
      return;
    }

    setDraggedPiece({ piece, position });
    selectSquare(position);

    // Define a imagem de arrasto transparente
    const dragImage = new Image();
    dragImage.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    e.dataTransfer.setDragImage(dragImage, 0, 0);
  }, [gameState.currentPlayer, selectSquare]);

  const handleDragEnd = useCallback(() => {
    setDraggedPiece(null);
  }, []);

  const handleDrop = useCallback((toPosition: ChessPosition) => {
    if (!draggedPiece) return;

    const success = makeMove(draggedPiece.position, toPosition);
    if (success && onMove) {
      onMove(draggedPiece.position, toPosition);
    }

    setDraggedPiece(null);
  }, [draggedPiece, makeMove, onMove]);

  // Manipulador de clique na casa
  const handleSquareClick = useCallback((position: ChessPosition) => {
    if (selectedSquare) {
      if (makeMove(selectedSquare, position) && onMove) {
        onMove(selectedSquare, position);
      }
    } else {
      selectSquare(position);
    }
  }, [selectedSquare, makeMove, onMove, selectSquare]);

  // Renderiza o tabuleiro
  const renderBoard = useCallback(() => {
    const board = [];
    const rangeY = orientation === 'white' 
      ? Array.from({ length: BOARD_SIZE }, (_, i) => i)
      : Array.from({ length: BOARD_SIZE }, (_, i) => BOARD_SIZE - 1 - i);
    
    const rangeX = orientation === 'white'
      ? Array.from({ length: BOARD_SIZE }, (_, i) => i)
      : Array.from({ length: BOARD_SIZE }, (_, i) => BOARD_SIZE - 1 - i);

    for (const row of rangeY) {
      for (const col of rangeX) {
        const position: ChessPosition = { row, col };
        const piece = pieceAt(position);
        const isSelected = selectedSquare && 
          selectedSquare.row === row && 
          selectedSquare.col === col;
        const isPossibleMove = possibleMoves.some(
          move => move.row === row && move.col === col
        );
        const isLastMove = lastMove && (
          (lastMove.from.row === row && lastMove.from.col === col) ||
          (lastMove.to.row === row && lastMove.to.col === col)
        );

        board.push(
          <div
            key={`${row}-${col}`}
            data-testid={`square-${row}-${col}`}
            style={{
              width: squareSize,
              height: squareSize,
            }}
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => handleDrop(position)}
          >
            <MemoizedSquare
              position={position}
              piece={piece}
              isSelected={isSelected}
              isPossibleMove={isPossibleMove}
              isLastMove={isLastMove}
              showCoordinates={showCoordinates}
              culturalStyle={culturalStyle}
              onClick={() => handleSquareClick(position)}
            >
              {piece && (
                <MemoizedPiece
                  piece={piece}
                  isDragging={draggedPiece?.position === position}
                  culturalStyle={culturalStyle}
                  size={squareSize * 0.8}
                  onDragStart={(e) => handleDragStart(position, piece, e)}
                  onDragEnd={handleDragEnd}
                />
              )}
            </MemoizedSquare>
          </div>
        );
      }
    }

    return board;
  }, [
    orientation,
    squareSize,
    pieceAt,
    selectedSquare,
    possibleMoves,
    lastMove,
    draggedPiece,
    culturalStyle,
    showCoordinates,
    handleDragStart,
    handleDragEnd,
    handleDrop,
    handleSquareClick,
  ]);

  // Efeito para verificar fim de jogo
  React.useEffect(() => {
    if (gameState.isCheckmate || gameState.isDraw) {
      let result = '';
      if (gameState.isCheckmate) {
        result = gameState.currentPlayer === 'white' ? 'black' : 'white';
      } else {
        result = 'draw';
      }
      onGameEnd?.(result);
    }
  }, [gameState.isCheckmate, gameState.isDraw, gameState.currentPlayer, onGameEnd]);

  return (
    <div
      className="relative"
      style={{
        width: boardSize,
        height: boardSize,
      }}
    >
      {/* Container do tabuleiro com gradiente de fundo */}
      <div className="p-2 rounded-lg shadow-xl bg-gradient-to-br from-emerald-700 to-emerald-900">
        {/* Grade do tabuleiro */}
        <div
          data-testid="chessboard"
          data-style={culturalStyle}
          className="grid grid-cols-8 rounded-md overflow-hidden border-4 border-emerald-800"
          style={{
            backgroundImage: `url('/images/patterns/${culturalStyle}.png')`
          }}
        >
          {renderBoard()}
        </div>
      </div>

      {/* Indicador de xeque */}
      {gameState.isCheck && (
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            border: '4px solid #f59e0b',
            animation: 'pulse 2s infinite',
          }}
        />
      )}

      {/* Indicador de xeque-mate */}
      {gameState.isCheckmate && (
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            border: '4px solid #ef4444',
            animation: 'shake 0.5s',
          }}
        />
      )}

      {/* Estilo cultural específico */}
      <style jsx>{`
        @keyframes pulse {
          0% { opacity: 0.5; }
          50% { opacity: 1; }
          100% { opacity: 0.5; }
        }

        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }

        .grid {
          background-image: url('/images/patterns/${culturalStyle}.png');
          background-size: cover;
          background-blend-mode: overlay;
        }
      `}</style>
    </div>
  );
};

// Otimização de renderização
export const MemoizedChessBoard = React.memo(ChessBoard);
