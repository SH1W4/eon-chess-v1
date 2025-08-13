
import React, { Suspense } from 'react';

interface LazyComponentProps {
  component: React.ComponentType<any>;
  fallback?: React.ReactNode;
  [key: string]: any;
}

export const LazyComponent: React.FC<LazyComponentProps> = ({ 
  component: Component, 
  fallback = <div>Carregando...</div>, 
  ...props 
}) => (
  <Suspense fallback={fallback}>
    <Component {...props} />
  </Suspense>
);
