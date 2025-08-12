import { useState, useEffect } from 'react';

interface ResponsiveBoardDimensions {
  boardSize: number;
  squareSize: number;
  pieceSize: number;
}

export const useResponsiveBoard = (
  containerRef: React.RefObject<HTMLDivElement>,
  minSize: number = 280,
  maxSize: number = 800
): ResponsiveBoardDimensions => {
  const [dimensions, setDimensions] = useState<ResponsiveBoardDimensions>({
    boardSize: minSize,
    squareSize: minSize / 8,
    pieceSize: (minSize / 8) * 0.8,
  });

  useEffect(() => {
    const updateDimensions = () => {
      if (!containerRef.current) return;

      const container = containerRef.current;
      const containerWidth = container.clientWidth;
      const containerHeight = container.clientHeight;
      
      // Calcula o tamanho ideal do tabuleiro
      let idealSize = Math.min(containerWidth, containerHeight);
      
      // Aplica limites mínimo e máximo
      idealSize = Math.max(minSize, Math.min(maxSize, idealSize));
      
      // Calcula tamanhos derivados
      const squareSize = idealSize / 8;
      const pieceSize = squareSize * 0.8;

      setDimensions({
        boardSize: idealSize,
        squareSize,
        pieceSize,
      });
    };

    // Atualiza dimensões iniciais
    updateDimensions();

    // Configura observer para mudanças no tamanho do container
    const resizeObserver = new ResizeObserver(updateDimensions);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    // Configura listener para mudanças na janela
    window.addEventListener('resize', updateDimensions);

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', updateDimensions);
    };
  }, [containerRef, minSize, maxSize]);

  return dimensions;
};
