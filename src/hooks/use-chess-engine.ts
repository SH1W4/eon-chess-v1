
import { useState, useCallback, useEffect } from 'react';

export const useChessEngine = () => {
  const [engine, setEngine] = useState<any>(null);
  const [isReady, setIsReady] = useState(false);
  
  const initializeEngine = useCallback(async () => {
    try {
      const stockfish = await import('stockfish');
      const instance = stockfish();
      
      instance.onmessage = (e: any) => {
        if (e.data === 'uciok') setIsReady(true);
      };
      
      instance.postMessage('uci');
      setEngine(instance);
    } catch (error) {
      console.error('Erro ao inicializar engine:', error);
    }
  }, []);
  
  const getBestMove = useCallback((fen: string, depth: number) => {
    if (!engine || !isReady) return null;
    
    return new Promise<string>((resolve) => {
      engine.onmessage = (e: any) => {
        if (e.data.startsWith('bestmove')) {
          resolve(e.data.split(' ')[1]);
        }
      };
      engine.postMessage(\`position fen \${fen}\`);
      engine.postMessage(\`go depth \${depth}\`);
    });
  }, [engine, isReady]);
  
  useEffect(() => {
    initializeEngine();
  }, [initializeEngine]);
  
  return { engine, isReady, getBestMove };
};
