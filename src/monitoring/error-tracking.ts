
// Sistema de error tracking com Sentry
export class ErrorTracker {
  private static instance: ErrorTracker;
  private isInitialized = false;
  
  private constructor() {}
  
  static getInstance(): ErrorTracker {
    if (!ErrorTracker.instance) {
      ErrorTracker.instance = new ErrorTracker();
    }
    return ErrorTracker.instance;
  }
  
  initialize(dsn: string, environment: string = 'development') {
    if (this.isInitialized) return;
    
    try {
      // Inicializar Sentry
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.init({
          dsn,
          environment,
          integrations: [
            new (window as any).Sentry.BrowserTracing(),
            new (window as any).Sentry.Replay()
          ],
          tracesSampleRate: 1.0,
          replaysSessionSampleRate: 0.1,
          replaysOnErrorSampleRate: 1.0
        });
        
        this.isInitialized = true;
        console.log('Error tracking inicializado com sucesso');
      }
    } catch (error) {
      console.error('Erro ao inicializar error tracking:', error);
    }
  }
  
  captureException(error: Error, context?: any): void {
    if (!this.isInitialized) return;
    
    try {
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.captureException(error, { extra: context });
      }
    } catch (e) {
      console.error('Erro ao capturar exceção:', e);
    }
  }
  
  captureMessage(message: string, level: 'info' | 'warning' | 'error' = 'info'): void {
    if (!this.isInitialized) return;
    
    try {
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.captureMessage(message, level);
      }
    } catch (e) {
      console.error('Erro ao capturar mensagem:', e);
    }
  }
  
  setUser(user: { id: string; username: string; email?: string }): void {
    if (!this.isInitialized) return;
    
    try {
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.setUser(user);
      }
    } catch (e) {
      console.error('Erro ao definir usuário:', e);
    }
  }
  
  setTag(key: string, value: string): void {
    if (!this.isInitialized) return;
    
    try {
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.setTag(key, value);
      }
    } catch (e) {
      console.error('Erro ao definir tag:', e);
    }
  }
}

export const errorTracker = ErrorTracker.getInstance();
