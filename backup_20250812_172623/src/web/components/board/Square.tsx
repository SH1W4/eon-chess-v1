import React from 'react';
import { ChessPosition, ChessPiece } from '../../../shared/types/chess';
import { getSquareColor } from '../../../shared/utils/chess';

interface SquareProps {
  position: ChessPosition;
  piece?: ChessPiece;
  isSelected?: boolean;
  isPossibleMove?: boolean;
  isLastMove?: boolean;
  showCoordinates?: boolean;
  culturalStyle?: string;
  onClick?: (position: ChessPosition) => void;
  children?: React.ReactNode;
}

export const Square: React.FC<SquareProps> = ({
  position,
  piece,
  isSelected,
  isPossibleMove,
  isLastMove,
  showCoordinates,
  culturalStyle = 'modern',
  onClick,
  children,
}) => {
  const { row, col } = position;
  const squareColor = getSquareColor(row, col);
  
  // Determina a cor final da casa com base nos estados e estilo cultural
  let backgroundColor;
  
  // Cores base do tabuleiro para cada estilo cultural
  const boardColors = {
    modern: {
      light: '#f0d9b5',
      dark: '#b58863'
    },
    ancient: {
      light: '#e6d5ac',
      dark: '#7c6c54'
    },
    medieval: {
      light: '#eed2a4',
      dark: '#8b4513'
    }
  };
  
  // Seleciona as cores base do estilo cultural atual
  const styleColors = boardColors[culturalStyle as keyof typeof boardColors] || boardColors.modern;
  
  // Aplica as cores de acordo com o estado do quadrado
  if (isSelected) {
    backgroundColor = '#fcd34d';
  } else if (isLastMove) {
    backgroundColor = '#34d399';
  } else if (isPossibleMove) {
    backgroundColor = '#fbbf24';
  } else {
    backgroundColor = styleColors[squareColor];
  }

  // Gera coordenadas algébricas para exibição
  const file = String.fromCharCode('a'.charCodeAt(0) + col);
  const rank = 8 - row;

  // Manipulador de clique
  const handleClick = () => {
    onClick?.(position);
  };

  return (
    <div
      className={`
        relative
        w-full
        h-full
        flex
        items-center
        justify-center
        transition-all
        duration-200
        ${isPossibleMove ? 'cursor-pointer' : ''}
        ${isSelected ? 'ring-2 ring-yellow-400' : ''}
        ${isLastMove ? 'ring-2 ring-green-400' : ''}
      `}
      style={{
        backgroundColor: backgroundColor,
      }}
      onClick={handleClick}
    >
      {/* Indicador de movimento possível */}
      {isPossibleMove && !piece && (
        <div
          className="w-3 h-3 rounded-full bg-yellow-400 opacity-50"
        />
      )}

      {/* Indicador de captura possível */}
      {isPossibleMove && piece && (
        <div
          className="absolute inset-0 border-2 border-yellow-400 opacity-50"
        />
      )}

      {/* Conteúdo da casa (peça ou outro elemento) */}
      <div className="relative z-10">
        {children}
      </div>

      {/* Coordenadas */}
      {showCoordinates && (
        <>
          {col === 0 && (
            <span
              className="absolute top-0.5 left-1 text-xs font-bold opacity-75"
              style={{ color: squareColor === 'light' ? '#666' : '#fff' }}
            >
              {rank}
            </span>
          )}
          {row === 7 && (
            <span
              className="absolute bottom-0.5 right-1 text-xs font-bold opacity-75"
              style={{ color: squareColor === 'light' ? '#666' : '#fff' }}
            >
              {file}
            </span>
          )}
        </>
      )}

      {/* Efeito de hover */}
      <div
        className="absolute inset-0 opacity-0 hover:opacity-20 transition-opacity duration-200 bg-white"
      />
    </div>
  );
};

// Otimização de renderização
export const MemoizedSquare = React.memo(Square);
