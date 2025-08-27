// AEON CHESS - Otimizador de Performance
// Versão: 1.0 - Cache Inteligente e Lazy Loading

class PerformanceOptimizer {
    constructor() {
        this.cache = new Map();
        this.lazyLoadQueue = [];
        this.performanceMetrics = {
            cacheHits: 0,
            cacheMisses: 0,
            loadTimes: [],
            memoryUsage: []
        };
        
        this.init();
    }
    
    init() {
        // Configurar observador de performance
        this.setupPerformanceObserver();
        
        // Configurar cache automático
        this.setupAutoCache();
        
        // Inicializar lazy loading
        this.initLazyLoading();
        
        console.log('🚀 Performance Optimizer inicializado');
    }
    
    // ===== SISTEMA DE CACHE =====
    setCache(key, data, ttl = 300000) { // 5 minutos padrão
        const cacheEntry = {
            data,
            timestamp: Date.now(),
            ttl,
            accessCount: 0
        };
        
        this.cache.set(key, cacheEntry);
        
        // Limpar cache expirado
        this.cleanupExpiredCache();
        
        return true;
    }
    
    getCache(key) {
        const entry = this.cache.get(key);
        
        if (!entry) {
            this.performanceMetrics.cacheMisses++;
            return null;
        }
        
        // Verificar se expirou
        if (Date.now() - entry.timestamp > entry.ttl) {
            this.cache.delete(key);
            this.performanceMetrics.cacheMisses++;
            return null;
        }
        
        // Atualizar estatísticas
        entry.accessCount++;
        this.performanceMetrics.cacheHits++;
        
        return entry.data;
    }
    
    clearCache(pattern = null) {
        if (pattern) {
            for (const key of this.cache.keys()) {
                if (key.includes(pattern)) {
                    this.cache.delete(key);
                }
            }
        } else {
            this.cache.clear();
        }
        
        console.log('🧹 Cache limpo');
    }
    
    cleanupExpiredCache() {
        const now = Date.now();
        for (const [key, entry] of this.cache.entries()) {
            if (now - entry.timestamp > entry.ttl) {
                this.cache.delete(key);
            }
        }
    }
    
    // ===== LAZY LOADING =====
    addLazyLoad(element, callback, threshold = 0.1) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    callback(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold });
        
        observer.observe(element);
        this.lazyLoadQueue.push({ element, observer });
    }
    
    initLazyLoading() {
        // Lazy load para imagens
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            this.addLazyLoad(img, (target) => {
                target.src = target.dataset.src;
                target.classList.add('fade-in');
            });
        });
        
        // Lazy load para componentes
        const components = document.querySelectorAll('[data-lazy-load]');
        components.forEach(component => {
            this.addLazyLoad(component, (target) => {
                this.loadComponent(target);
            });
        });
    }
    
    loadComponent(element) {
        const componentType = element.dataset.lazyLoad;
        
        switch (componentType) {
            case 'chess-board':
                this.loadChessBoard(element);
                break;
            case 'ai-analysis':
                this.loadAIAnalysis(element);
                break;
            case 'game-history':
                this.loadGameHistory(element);
                break;
            default:
                console.log(`Componente desconhecido: ${componentType}`);
        }
    }
    
    // ===== COMPRESSÃO DE DADOS =====
    compressData(data) {
        try {
            const jsonString = JSON.stringify(data);
            
            // Compressão simples para strings longas
            if (jsonString.length > 1000) {
                return {
                    compressed: true,
                    data: this.simpleCompression(jsonString),
                    originalSize: jsonString.length
                };
            }
            
            return {
                compressed: false,
                data: jsonString,
                originalSize: jsonString.length
            };
        } catch (error) {
            console.error('Erro na compressão:', error);
            return { compressed: false, data, originalSize: 0 };
        }
    }
    
    decompressData(compressedData) {
        if (!compressedData.compressed) {
            return JSON.parse(compressedData.data);
        }
        
        try {
            const decompressed = this.simpleDecompression(compressedData.data);
            return JSON.parse(decompressed);
        } catch (error) {
            console.error('Erro na descompressão:', error);
            return null;
        }
    }
    
    simpleCompression(str) {
        // Compressão básica para strings repetitivas
        let compressed = str;
        const commonPatterns = [
            ['"position":', 'p:'],
            ['"move":', 'm:'],
            ['"color":', 'c:'],
            ['"piece":', 'pc:'],
            ['"timestamp":', 't:']
        ];
        
        commonPatterns.forEach(([pattern, replacement]) => {
            compressed = compressed.replace(new RegExp(pattern, 'g'), replacement);
        });
        
        return compressed;
    }
    
    simpleDecompression(str) {
        let decompressed = str;
        const commonPatterns = [
            ['p:', '"position":'],
            ['m:', '"move":'],
            ['c:', '"color":'],
            ['pc:', '"piece":'],
            ['t:', '"timestamp":']
        ];
        
        commonPatterns.forEach(([pattern, replacement]) => {
            decompressed = decompressed.replace(new RegExp(pattern, 'g'), replacement);
        });
        
        return decompressed;
    }
    
    // ===== MONITORAMENTO DE PERFORMANCE =====
    setupPerformanceObserver() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach(entry => {
                    this.performanceMetrics.loadTimes.push({
                        name: entry.name,
                        duration: entry.duration,
                        timestamp: Date.now()
                    });
                });
            });
            
            observer.observe({ entryTypes: ['navigation', 'resource'] });
        }
    }
    
    measurePerformance(name, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        
        this.performanceMetrics.loadTimes.push({
            name,
            duration: end - start,
            timestamp: Date.now()
        });
        
        return result;
    }
    
    getPerformanceReport() {
        const avgLoadTime = this.performanceMetrics.loadTimes.length > 0
            ? this.performanceMetrics.loadTimes.reduce((sum, entry) => sum + entry.duration, 0) / this.performanceMetrics.loadTimes.length
            : 0;
        
        const cacheHitRate = this.performanceMetrics.cacheHits + this.performanceMetrics.cacheMisses > 0
            ? (this.performanceMetrics.cacheHits / (this.performanceMetrics.cacheHits + this.performanceMetrics.cacheMisses)) * 100
            : 0;
        
        return {
            cacheStats: {
                hits: this.performanceMetrics.cacheHits,
                misses: this.performanceMetrics.cacheMisses,
                hitRate: cacheHitRate.toFixed(2) + '%',
                size: this.cache.size
            },
            performance: {
                averageLoadTime: avgLoadTime.toFixed(2) + 'ms',
                totalMeasurements: this.performanceMetrics.loadTimes.length
            },
            memory: {
                cacheSize: this.cache.size,
                lazyLoadQueue: this.lazyLoadQueue.length
            }
        };
    }
    
    // ===== OTIMIZAÇÕES ESPECÍFICAS =====
    loadChessBoard(element) {
        // Carregar tabuleiro de forma otimizada
        const boardData = this.getCache('chess-board-data');
        
        if (boardData) {
            element.innerHTML = this.renderChessBoard(boardData);
        } else {
            // Simular carregamento
            element.innerHTML = '<div class="loading">Carregando tabuleiro...</div>';
            
            setTimeout(() => {
                const mockData = this.generateMockBoardData();
                this.setCache('chess-board-data', mockData);
                element.innerHTML = this.renderChessBoard(mockData);
            }, 500);
        }
    }
    
    loadAIAnalysis(element) {
        element.innerHTML = '<div class="card">Análise de IA carregada</div>';
    }
    
    loadGameHistory(element) {
        element.innerHTML = '<div class="card">Histórico de jogos carregado</div>';
    }
    
    renderChessBoard(data) {
        // Renderização otimizada do tabuleiro
        return `<div class="chess-board">Tabuleiro renderizado</div>`;
    }
    
    generateMockBoardData() {
        return {
            pieces: [],
            moves: [],
            timestamp: Date.now()
        };
    }
    
    // ===== UTILITÁRIOS =====
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    // ===== LIMPEZA =====
    destroy() {
        // Limpar observadores
        this.lazyLoadQueue.forEach(({ observer }) => observer.disconnect());
        this.lazyLoadQueue = [];
        
        // Limpar cache
        this.clearCache();
        
        console.log('🧹 Performance Optimizer destruído');
    }
}

// Exportar para uso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceOptimizer;
} else {
    window.PerformanceOptimizer = PerformanceOptimizer;
}
