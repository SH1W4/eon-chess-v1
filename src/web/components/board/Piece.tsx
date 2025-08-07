import React from 'react';
import { ChessPiece } from '../../../shared/types/chess';
import { getPieceSymbol } from '../../../shared/utils/chess';

interface PieceProps {
  piece: ChessPiece;
  isDragging?: boolean;
  culturalStyle?: string;
  size?: number;
  onDragStart?: (e: React.DragEvent) => void;
  onDragEnd?: (e: React.DragEvent) => void;
}

export const Piece: React.FC<PieceProps> = ({
  piece,
  isDragging,
  culturalStyle = 'modern',
  size,
  onDragStart,
  onDragEnd,
}) => {
  // Define o estilo da peça baseado no estilo cultural
  const pieceStyles = {
    modern: 'traditional',
    ancient: 'hieroglyphic',
    medieval: 'artistic'
  };
  const pieceStyle = pieceStyles[culturalStyle as keyof typeof pieceStyles] || 'traditional';

  // Calcula a escala baseada no estado de dragging
  const scale = isDragging ? 1.2 : 1;

  // Determina o símbolo da peça
  const symbol = getPieceSymbol(piece);

  // Estilo base da peça
  const baseStyle = {
    fontSize: `${size}px`,
    lineHeight: `${size}px`,
    transform: `scale(${scale})`,
    transition: 'transform 150ms ease',
    color: piece.color === 'white' ? '#fff' : '#000',
    textShadow: piece.color === 'white'
      ? '2px 2px 2px rgba(0,0,0,0.4)'
      : '2px 2px 2px rgba(255,255,255,0.4)',
    cursor: 'grab',
    userSelect: 'none' as const,
  };

  // Modifica o estilo baseado no tema cultural
  const culturalModifiers = {
    traditional: {},
    artistic: {
      filter: 'drop-shadow(2px 2px 3px rgba(0,0,0,0.3))',
    },
    minimalist: {
      textShadow: 'none',
      fontWeight: 'normal',
    },
    hieroglyphic: {
      fontFamily: "'Noto Sans', sans-serif",
      fontWeight: 'normal',
    },
  };

  const styleModifiers = culturalModifiers[pieceStyle as keyof typeof culturalModifiers] || {};

  return (
    <div
      className={`
        select-none
        flex
        items-center
        justify-center
        transform
        transition-transform
        ${isDragging ? 'cursor-grabbing z-50' : 'cursor-grab'}
      `}
      style={{
        width: size,
        height: size,
        transform: `scale(${scale})`,
        transition: 'transform 150ms ease',
      }}
      draggable={true}
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
    >
      <div
        className="text-5xl select-none relative"
        style={{
          color: piece.color === 'white' ? '#fff' : '#000',
          textShadow: piece.color === 'white'
            ? '2px 2px 2px rgba(0,0,0,0.4)'
            : '2px 2px 2px rgba(255,255,255,0.4)',
          lineHeight: '1',
          ...styleModifiers,
        }}
      >
        {symbol}
      </div>
    </div>
  );
};

// Otimização de renderização
export const MemoizedPiece = React.memo(Piece);
