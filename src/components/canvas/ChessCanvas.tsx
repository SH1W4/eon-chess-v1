
import React, { useRef, useEffect, useCallback } from 'react';

interface ChessCanvasProps {
  fen: string;
  onMove?: (from: string, to: string) => void;
  size?: number;
}

export const ChessCanvas: React.FC<ChessCanvasProps> = ({ 
  fen, 
  onMove, 
  size = 400 
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const contextRef = useRef<CanvasRenderingContext2D | null>(null);
  
  const squareSize = size / 8;
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const context = canvas.getContext('2d');
    if (!context) return;
    
    contextRef.current = context;
    renderBoard();
  }, [fen]);
  
  const renderBoard = useCallback(() => {
    const context = contextRef.current;
    if (!context) return;
    
    // Limpar canvas
    context.clearRect(0, 0, size, size);
    
    // Desenhar quadrados
    for (let rank = 0; rank < 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const x = file * squareSize;
        const y = rank * squareSize;
        const isLight = (rank + file) % 2 === 0;
        
        context.fillStyle = isLight ? '#f0d9b5' : '#b58863';
        context.fillRect(x, y, squareSize, squareSize);
      }
    }
    
    // Aqui você pode adicionar a renderização das peças
    renderPieces();
  }, [fen, size, squareSize]);
  
  const renderPieces = () => {
    // Implementação da renderização das peças
    // Você pode usar sprites ou desenhar as peças diretamente
  };
  
  const handleClick = useCallback((event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || !onMove) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    const file = Math.floor(x / squareSize);
    const rank = Math.floor(y / squareSize);
    
    const square = String.fromCharCode(97 + file) + (8 - rank);
    // Implementar lógica de seleção de peça e movimento
  }, [onMove, squareSize]);
  
  return (
    <canvas
      ref={canvasRef}
      width={size}
      height={size}
      onClick={handleClick}
      className="border-2 border-gray-800 cursor-pointer"
      style={{ maxWidth: '100%', height: 'auto' }}
    />
  );
};
