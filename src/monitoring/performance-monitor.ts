
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  
  private constructor() {}
  
  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }
  
  initialize() {
    getCLS(this.sendToAnalytics);
    getFID(this.sendToAnalytics);
    getFCP(this.sendToAnalytics);
    getLCP(this.sendToAnalytics);
    getTTFB(this.sendToAnalytics);
  }
  
  private sendToAnalytics(metric: any) {
    // Enviar para Google Analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', metric.name, {
        value: Math.round(metric.value),
        event_category: 'Web Vitals',
        event_label: metric.id,
        non_interaction: true,
      });
    }
    
    // Log local para desenvolvimento
    console.log('Web Vital:', metric.name, metric.value);
  }
  
  measureChessMoveTime(startTime: number) {
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    // Enviar métrica de tempo de movimento
    if (typeof gtag !== 'undefined') {
      gtag('event', 'chess_move_time', {
        value: Math.round(duration),
        event_category: 'Performance',
        event_label: 'move_execution',
      });
    }
    
    return duration;
  }
}

export const performanceMonitor = PerformanceMonitor.getInstance();
