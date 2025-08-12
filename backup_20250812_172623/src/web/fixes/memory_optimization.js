// ARKITECT Memory Leak Fixes for React Components
export const memoryOptimizations = {
  useCleanup: (cleanup) => {
    React.useEffect(() => {
      return cleanup;
    }, []);
  },
  
  useOptimizedState: (initial) => {
    const [state, setState] = React.useState(initial);
    React.useEffect(() => {
      return () => setState(null);
    }, []);
    return [state, setState];
  },
  
  lazyLoadComponent: (path) => {
    return React.lazy(() => import(path));
  }
};

// Performance optimizations
export const performanceConfig = {
  renderBatching: true,
  virtualScrolling: true,
  memoization: true,
  debounceTime: 300
};

// Service Worker registration
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}