// AEON CHESS - Performance Optimizer v2.0 (Arquimax Enhanced)
// TaskMash SuperEscopo: Performance Critical Improvements

class PerformanceOptimizerV2 {
    constructor() {
        this.cdnConfig = {
            primary: 'https://cdn.aeonchess.com',
            fallback: 'https://backup-cdn.aeonchess.com',
            regions: ['us-east', 'eu-west', 'asia-pacific'],
            cacheTTL: 86400 // 24 horas
        };
        
        this.cacheConfig = {
            memory: new Map(),
            localStorage: 'aeon_chess_cache',
            sessionStorage: 'aeon_chess_session',
            maxSize: 50 * 1024 * 1024, // 50MB
            compression: true
        };
        
        this.metrics = {
            loadTimes: [],
            cacheHits: 0,
            cacheMisses: 0,
            cdnUsage: 0,
            compressionRatio: 0
        };
        
        this.init();
    }
    
    init() {
        this.setupCDN();
        this.setupCache();
        this.setupCompression();
        this.setupMonitoring();
        this.optimizeImages();
        this.optimizeCSS();
        this.optimizeJS();
    }
    
    setupCDN() {
        // CDN Configuration
        const cdnElement = document.createElement('script');
        cdnElement.src = `${this.cdnConfig.primary}/js/cdn-loader.js`;
        cdnElement.onerror = () => this.fallbackCDN();
        document.head.appendChild(cdnElement);
        
        console.log('🏛️ ARKITECT: CDN configurado com fallback');
    }
    
    fallbackCDN() {
        console.log('🔄 ARKITECT: Usando CDN de fallback');
        const fallbackElement = document.createElement('script');
        fallbackElement.src = `${this.cdnConfig.fallback}/js/cdn-loader.js`;
        document.head.appendChild(fallbackElement);
    }
    
    setupCache() {
        // Memory Cache
        this.cacheConfig.memory = new Map();
        
        // Local Storage Cache
        if (localStorage) {
            const cached = localStorage.getItem(this.cacheConfig.localStorage);
            if (cached) {
                try {
                    const parsed = JSON.parse(cached);
                    this.cacheConfig.memory = new Map(parsed);
                } catch (e) {
                    console.warn('ARKITECT: Cache corrompido, recriando');
                }
            }
        }
        
        // Cache cleanup
        setInterval(() => this.cleanupCache(), 300000); // 5 minutos
    }
    
    setupCompression() {
        // Gzip compression simulation
        if (this.cacheConfig.compression) {
            this.compressData = (data) => {
                // Simulação de compressão
                return btoa(JSON.stringify(data)).slice(0, -2);
            };
            
            this.decompressData = (compressed) => {
                // Simulação de descompressão
                return JSON.parse(atob(compressed + '=='));
            };
        }
    }
    
    setupMonitoring() {
        // Performance monitoring
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                this.metrics.loadTimes.push({
                    name: entry.name,
                    duration: entry.duration,
                    timestamp: Date.now()
                });
            }
        });
        
        observer.observe({ entryTypes: ['navigation', 'resource'] });
        
        // Memory monitoring
        setInterval(() => {
            if (performance.memory) {
                this.metrics.memoryUsage = performance.memory.usedJSHeapSize;
            }
        }, 10000);
    }
    
    optimizeImages() {
        // Lazy loading para imagens
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    optimizeCSS() {
        // CSS optimization
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        stylesheets.forEach(sheet => {
            if (sheet.href.includes('consolidated-theme.css')) {
                sheet.setAttribute('data-optimized', 'true');
                this.prefetchCriticalCSS();
            }
        });
    }
    
    optimizeJS() {
        // JavaScript optimization
        const scripts = document.querySelectorAll('script[src]');
        scripts.forEach(script => {
            if (!script.async && !script.defer) {
                script.defer = true;
            }
        });
    }
    
    prefetchCriticalCSS() {
        // Prefetch critical CSS
        const criticalCSS = [
            '/web/styles/critical.css',
            '/web/styles/chess-theme.css'
        ];
        
        criticalCSS.forEach(css => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = css;
            document.head.appendChild(link);
        });
    }
    
    async cacheResource(url, data) {
        try {
            const compressed = this.cacheConfig.compression ? 
                this.compressData(data) : data;
            
            this.cacheConfig.memory.set(url, {
                data: compressed,
                timestamp: Date.now(),
                size: JSON.stringify(compressed).length
            });
            
            // Persist to localStorage
            if (localStorage) {
                const cacheArray = Array.from(this.cacheConfig.memory.entries());
                localStorage.setItem(this.cacheConfig.localStorage, JSON.stringify(cacheArray));
            }
            
            this.metrics.cacheHits++;
            return true;
        } catch (error) {
            console.error('ARKITECT: Erro ao cachear recurso:', error);
            return false;
        }
    }
    
    async getCachedResource(url) {
        const cached = this.cacheConfig.memory.get(url);
        if (cached && Date.now() - cached.timestamp < this.cdnConfig.cacheTTL * 1000) {
            this.metrics.cacheHits++;
            return this.cacheConfig.compression ? 
                this.decompressData(cached.data) : cached.data;
        }
        
        this.metrics.cacheMisses++;
        return null;
    }
    
    cleanupCache() {
        const now = Date.now();
        const maxAge = this.cdnConfig.cacheTTL * 1000;
        
        for (const [url, data] of this.cacheConfig.memory.entries()) {
            if (now - data.timestamp > maxAge) {
                this.cacheConfig.memory.delete(url);
            }
        }
        
        // Size-based cleanup
        let totalSize = 0;
        for (const [url, data] of this.cacheConfig.memory.entries()) {
            totalSize += data.size;
        }
        
        if (totalSize > this.cacheConfig.maxSize) {
            const entries = Array.from(this.cacheConfig.memory.entries())
                .sort((a, b) => a[1].timestamp - b[1].timestamp);
            
            while (totalSize > this.cacheConfig.maxSize / 2 && entries.length > 0) {
                const [url] = entries.shift();
                const data = this.cacheConfig.memory.get(url);
                totalSize -= data.size;
                this.cacheConfig.memory.delete(url);
            }
        }
    }
    
    getMetrics() {
        return {
            ...this.metrics,
            cacheHitRate: this.metrics.cacheHits / (this.metrics.cacheHits + this.metrics.cacheMisses),
            averageLoadTime: this.metrics.loadTimes.reduce((sum, item) => sum + item.duration, 0) / this.metrics.loadTimes.length,
            memoryUsage: this.metrics.memoryUsage || 0
        };
    }
    
    // Arquimax: Advanced optimization methods
    async optimizeBundle() {
        console.log('🏛️ ARQUIMAX: Otimizando bundle de recursos');
        
        // Bundle CSS
        const cssFiles = [
            '/web/styles/consolidated-theme.css',
            '/web/styles/chess-theme.css'
        ];
        
        // Bundle JS
        const jsFiles = [
            '/web/utils/performance-optimizer-v2.js',
            '/web/utils/notification-system.js',
            '/web/utils/error-handler.js'
        ];
        
        // Create optimized bundles
        await this.createOptimizedBundle('css', cssFiles);
        await this.createOptimizedBundle('js', jsFiles);
    }
    
    async createOptimizedBundle(type, files) {
        const bundle = {
            type,
            files,
            timestamp: Date.now(),
            version: '2.0'
        };
        
        await this.cacheResource(`bundle-${type}`, bundle);
        console.log(`🏛️ ARQUIMAX: Bundle ${type} criado e cacheado`);
    }
}

// Initialize TaskMash SuperEscopo
const taskMashOptimizer = new PerformanceOptimizerV2();

// Export for global use
window.TaskMashOptimizer = taskMashOptimizer;
