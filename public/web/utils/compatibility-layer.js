// AEON CHESS - Camada de Compatibilidade Cross-Browser
// Versão: 1.0 - Suporte para navegadores antigos

class CompatibilityLayer {
    constructor() {
        this.features = new Map();
        this.polyfills = new Map();
        this.browserInfo = this.detectBrowser();
        
        this.init();
    }

    init() {
        console.log('🔧 Inicializando camada de compatibilidade...');
        this.detectFeatures();
        this.loadPolyfills();
        this.setupFallbacks();
        console.log('✅ Compatibilidade configurada para:', this.browserInfo.name, this.browserInfo.version);
    }

    detectBrowser() {
        const userAgent = navigator.userAgent;
        let browser = 'Unknown';
        let version = 'Unknown';

        if (userAgent.includes('Chrome')) {
            browser = 'Chrome';
            version = userAgent.match(/Chrome\/(\d+)/)?.[1] || 'Unknown';
        } else if (userAgent.includes('Firefox')) {
            browser = 'Firefox';
            version = userAgent.match(/Firefox\/(\d+)/)?.[1] || 'Unknown';
        } else if (userAgent.includes('Safari')) {
            browser = 'Safari';
            version = userAgent.match(/Version\/(\d+)/)?.[1] || 'Unknown';
        } else if (userAgent.includes('Edge')) {
            browser = 'Edge';
            version = userAgent.match(/Edge\/(\d+)/)?.[1] || 'Unknown';
        } else if (userAgent.includes('MSIE') || userAgent.includes('Trident')) {
            browser = 'Internet Explorer';
            version = userAgent.match(/(?:MSIE|rv:)(\d+)/)?.[1] || 'Unknown';
        }

        return {
            name: browser,
            version: parseInt(version) || 0,
            userAgent: userAgent
        };
    }

    detectFeatures() {
        // Detectar recursos disponíveis
        this.features.set('es6', this.supportsES6());
        this.features.set('fetch', this.supportsFetch());
        this.features.set('promises', this.supportsPromises());
        this.features.set('async_await', this.supportsAsyncAwait());
        this.features.set('modules', this.supportsModules());
        this.features.set('local_storage', this.supportsLocalStorage());
        this.features.set('session_storage', this.supportsSessionStorage());
        this.features.set('web_workers', this.supportsWebWorkers());
        this.features.set('service_workers', this.supportsServiceWorkers());
        this.features.set('indexed_db', this.supportsIndexedDB());
    }

    supportsES6() {
        try {
            new Function('() => {}');
            new Function('class Test {}');
            new Function('const test = 1; let test2 = 2;');
            return true;
        } catch (e) {
            return false;
        }
    }

    supportsFetch() {
        return typeof fetch !== 'undefined';
    }

    supportsPromises() {
        return typeof Promise !== 'undefined';
    }

    supportsAsyncAwait() {
        try {
            new Function('async () => {}');
            return true;
        } catch (e) {
            return false;
        }
    }

    supportsModules() {
        try {
            new Function('import("test")');
            return true;
        } catch (e) {
            return false;
        }
    }

    supportsLocalStorage() {
        try {
            const test = 'test';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    }

    supportsSessionStorage() {
        try {
            const test = 'test';
            sessionStorage.setItem(test, test);
            sessionStorage.removeItem(test);
            return true;
        } catch (e) {
            return false;
        }
    }

    supportsWebWorkers() {
        return typeof Worker !== 'undefined';
    }

    supportsServiceWorkers() {
        return 'serviceWorker' in navigator;
    }

    supportsIndexedDB() {
        return 'indexedDB' in window;
    }

    loadPolyfills() {
        // Carregar polyfills necessários
        if (!this.features.get('promises')) {
            this.loadPolyfill('promises');
        }

        if (!this.features.get('fetch')) {
            this.loadPolyfill('fetch');
        }

        if (!this.features.get('es6')) {
            this.loadPolyfill('es6');
        }

        if (!this.features.get('local_storage')) {
            this.loadPolyfill('local_storage');
        }
    }

    loadPolyfill(type) {
        console.log(`🔧 Carregando polyfill para: ${type}`);
        
        switch (type) {
            case 'promises':
                this.loadPromisePolyfill();
                break;
            case 'fetch':
                this.loadFetchPolyfill();
                break;
            case 'es6':
                this.loadES6Polyfill();
                break;
            case 'local_storage':
                this.loadLocalStoragePolyfill();
                break;
        }
    }

    loadPromisePolyfill() {
        if (typeof Promise === 'undefined') {
            // Polyfill básico de Promise
            window.Promise = function(executor) {
                let resolve, reject;
                let state = 'pending';
                let value, reason;

                function fulfill(result) {
                    if (state === 'pending') {
                        state = 'fulfilled';
                        value = result;
                    }
                }

                function reject(error) {
                    if (state === 'pending') {
                        state = 'rejected';
                        reason = error;
                    }
                }

                try {
                    executor(fulfill, reject);
                } catch (e) {
                    reject(e);
                }

                return {
                    then: function(onFulfilled, onRejected) {
                        if (state === 'fulfilled') {
                            onFulfilled(value);
                        } else if (state === 'rejected') {
                            onRejected(reason);
                        }
                    }
                };
            };
        }
    }

    loadFetchPolyfill() {
        if (typeof fetch === 'undefined') {
            // Polyfill básico de fetch usando XMLHttpRequest
            window.fetch = function(url, options = {}) {
                return new Promise((resolve, reject) => {
                    const xhr = new XMLHttpRequest();
                    
                    xhr.open(options.method || 'GET', url);
                    
                    if (options.headers) {
                        Object.keys(options.headers).forEach(key => {
                            xhr.setRequestHeader(key, options.headers[key]);
                        });
                    }
                    
                    xhr.onload = function() {
                        resolve({
                            ok: xhr.status >= 200 && xhr.status < 300,
                            status: xhr.status,
                            statusText: xhr.statusText,
                            headers: xhr.getAllResponseHeaders(),
                            text: () => Promise.resolve(xhr.responseText),
                            json: () => Promise.resolve(JSON.parse(xhr.responseText))
                        });
                    };
                    
                    xhr.onerror = function() {
                        reject(new Error('Network error'));
                    };
                    
                    xhr.send(options.body);
                });
            };
        }
    }

    loadES6Polyfill() {
        // Polyfills básicos para ES6
        if (!Array.prototype.find) {
            Array.prototype.find = function(predicate) {
                for (let i = 0; i < this.length; i++) {
                    if (predicate(this[i], i, this)) {
                        return this[i];
                    }
                }
                return undefined;
            };
        }

        if (!Array.prototype.findIndex) {
            Array.prototype.findIndex = function(predicate) {
                for (let i = 0; i < this.length; i++) {
                    if (predicate(this[i], i, this)) {
                        return i;
                    }
                }
                return -1;
            };
        }

        if (!Array.prototype.includes) {
            Array.prototype.includes = function(searchElement, fromIndex) {
                return this.indexOf(searchElement, fromIndex) !== -1;
            };
        }

        if (!String.prototype.startsWith) {
            String.prototype.startsWith = function(searchString, position) {
                position = position || 0;
                return this.substr(position, searchString.length) === searchString;
            };
        }

        if (!String.prototype.endsWith) {
            String.prototype.endsWith = function(searchString, length) {
                if (length === undefined || length > this.length) {
                    length = this.length;
                }
                return this.substring(length - searchString.length, length) === searchString;
            };
        }
    }

    loadLocalStoragePolyfill() {
        if (!this.features.get('local_storage')) {
            // Fallback para memória local
            window.localStorage = {
                data: {},
                setItem: function(key, value) {
                    this.data[key] = value;
                },
                getItem: function(key) {
                    return this.data[key] || null;
                },
                removeItem: function(key) {
                    delete this.data[key];
                },
                clear: function() {
                    this.data = {};
                },
                get length() {
                    return Object.keys(this.data).length;
                }
            };

            window.sessionStorage = {
                data: {},
                setItem: function(key, value) {
                    this.data[key] = value;
                },
                getItem: function(key) {
                    return this.data[key] || null;
                },
                removeItem: function(key) {
                    delete this.data[key];
                },
                clear: function() {
                    this.data = {};
                },
                get length() {
                    return Object.keys(this.data).length;
                }
            };
        }
    }

    setupFallbacks() {
        // Configurar fallbacks para funcionalidades não suportadas
        if (!this.features.get('web_workers')) {
            this.setupWorkerFallback();
        }

        if (!this.features.get('service_workers')) {
            this.setupServiceWorkerFallback();
        }
    }

    setupWorkerFallback() {
        // Fallback para Web Workers usando setTimeout
        window.Worker = function(script) {
            return {
                postMessage: function(data) {
                    setTimeout(() => {
                        // Simular processamento em background
                        console.log('🔄 Worker fallback processando:', data);
                    }, 0);
                },
                terminate: function() {
                    console.log('🛑 Worker fallback terminado');
                }
            };
        };
    }

    setupServiceWorkerFallback() {
        // Fallback para Service Workers
        if (!('serviceWorker' in navigator)) {
            navigator.serviceWorker = {
                register: function() {
                    return Promise.resolve({
                        unregister: function() {
                            return Promise.resolve();
                        }
                    });
                }
            };
        }
    }

    // Métodos de utilidade
    getFeatureSupport(feature) {
        return this.features.get(feature) || false;
    }

    getBrowserInfo() {
        return this.browserInfo;
    }

    getCompatibilityReport() {
        const report = {
            browser: this.browserInfo,
            features: Object.fromEntries(this.features),
            polyfills: Array.from(this.polyfills.keys()),
            recommendations: this.getRecommendations()
        };

        return report;
    }

    getRecommendations() {
        const recommendations = [];

        if (!this.features.get('es6')) {
            recommendations.push('Atualizar navegador para suporte completo a ES6');
        }

        if (!this.features.get('fetch')) {
            recommendations.push('Usar polyfill de fetch ou atualizar navegador');
        }

        if (!this.features.get('local_storage')) {
            recommendations.push('Usar fallback de memória local');
        }

        return recommendations;
    }

    isFullyCompatible() {
        return Array.from(this.features.values()).every(feature => feature);
    }

    getCompatibilityScore() {
        const totalFeatures = this.features.size;
        const supportedFeatures = Array.from(this.features.values()).filter(f => f).length;
        return Math.round((supportedFeatures / totalFeatures) * 100);
    }
}

// Inicializar automaticamente
if (typeof window !== 'undefined') {
    window.CompatibilityLayer = CompatibilityLayer;
    window.compatibilityLayer = new CompatibilityLayer();
}

// Para Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CompatibilityLayer;
}
