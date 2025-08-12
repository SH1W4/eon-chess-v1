
import React, { lazy, Suspense } from 'react';

// Lazy load de componentes pesados
const TerminalCultural = lazy(() => import('./js/terminal-cultural.js'));
const ChessEngine = lazy(() => import('./components/ChessEngine'));
const Analytics = lazy(() => import('./components/Analytics'));

export const LazyLoader: React.FC<{ component: string }> = ({ component }) => {
  const ComponentMap = {
    terminal: TerminalCultural,
    engine: ChessEngine,
    analytics: Analytics
  };
  
  const Component = ComponentMap[component as keyof typeof ComponentMap];
  
  return (
    <Suspense fallback={<div className="loading-spinner">Carregando...</div>}>
      <Component />
    </Suspense>
  );
};
