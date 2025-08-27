// AEON CHESS - Sistema de Notificações Avançado
// Versão: 1.0 - Feedback Visual e Persistência

class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.settings = {
            maxNotifications: 5,
            autoHide: true,
            autoHideDelay: 5000,
            position: 'top-right',
            animationDuration: 300,
            soundEnabled: true
        };
        
        this.sounds = {
            success: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT',
            warning: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT',
            error: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT',
            info: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT'
        };
        
        this.init();
    }
    
    init() {
        this.createContainer();
        this.loadSettings();
        this.setupEventListeners();
        
        console.log('🔔 Sistema de Notificações inicializado');
    }
    
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.className = `notification-container ${this.settings.position}`;
        
        // Estilos inline para garantir funcionamento
        Object.assign(this.container.style, {
            position: 'fixed',
            top: this.settings.position.includes('top') ? '20px' : 'auto',
            bottom: this.settings.position.includes('bottom') ? '20px' : 'auto',
            left: this.settings.position.includes('left') ? '20px' : 'auto',
            right: this.settings.position.includes('right') ? '20px' : 'auto',
            zIndex: '10000',
            maxWidth: '400px',
            pointerEvents: 'none'
        });
        
        document.body.appendChild(this.container);
    }
    
    loadSettings() {
        const saved = localStorage.getItem('notification-settings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
        }
    }
    
    saveSettings() {
        localStorage.setItem('notification-settings', JSON.stringify(this.settings));
    }
    
    setupEventListeners() {
        // Eventos de teclado para controle
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'n') {
                this.toggleContainer();
            }
        });
        
        // Limpar notificações antigas ao focar na janela
        window.addEventListener('focus', () => {
            this.cleanupOldNotifications();
        });
    }
    
    // ===== CRIAR NOTIFICAÇÕES =====
    show(message, type = 'info', options = {}) {
        const notification = this.createNotification(message, type, options);
        
        // Adicionar à lista
        this.notifications.push(notification);
        
        // Adicionar ao container
        this.container.appendChild(notification.element);
        
        // Animar entrada
        this.animateIn(notification);
        
        // Configurar auto-hide
        if (this.settings.autoHide && options.persistent !== true) {
            this.setupAutoHide(notification);
        }
        
        // Tocar som
        if (this.settings.soundEnabled) {
            this.playSound(type);
        }
        
        // Limpar notificações antigas
        this.cleanupOldNotifications();
        
        return notification;
    }
    
    createNotification(message, type, options) {
        const id = this.generateId();
        const element = document.createElement('div');
        
        element.className = `notification notification-${type}`;
        element.dataset.id = id;
        
        // Conteúdo da notificação
        element.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    ${this.getIcon(type)}
                </div>
                <div class="notification-body">
                    <div class="notification-message">${message}</div>
                    ${options.details ? `<div class="notification-details">${options.details}</div>` : ''}
                </div>
                <div class="notification-actions">
                    ${options.actions ? this.renderActions(options.actions, id) : ''}
                    <button class="notification-close" onclick="notificationSystem.close('${id}')">
                        <span>&times;</span>
                    </button>
                </div>
            </div>
            ${options.progress ? '<div class="notification-progress"></div>' : ''}
        `;
        
        // Estilos inline
        Object.assign(element.style, {
            background: this.getColor(type),
            color: 'white',
            padding: '1rem',
            margin: '0.5rem 0',
            borderRadius: '0.5rem',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transform: 'translateX(100%)',
            transition: `transform ${this.settings.animationDuration}ms ease-out`,
            pointerEvents: 'auto',
            maxWidth: '100%',
            wordWrap: 'break-word'
        });
        
        return {
            id,
            element,
            type,
            message,
            options,
            timestamp: Date.now(),
            progress: options.progress || null
        };
    }
    
    getIcon(type) {
        const icons = {
            success: '✅',
            warning: '⚠️',
            error: '❌',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }
    
    getColor(type) {
        const colors = {
            success: '#10b981',
            warning: '#f59e0b',
            error: '#ef4444',
            info: '#3b82f6'
        };
        return colors[type] || colors.info;
    }
    
    renderActions(actions, notificationId) {
        return actions.map(action => `
            <button class="notification-action" onclick="notificationSystem.executeAction('${notificationId}', '${action.key}')">
                ${action.label}
            </button>
        `).join('');
    }
    
    // ===== ANIMAÇÕES =====
    animateIn(notification) {
        requestAnimationFrame(() => {
            notification.element.style.transform = 'translateX(0)';
        });
    }
    
    animateOut(notification) {
        return new Promise(resolve => {
            notification.element.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                resolve();
            }, this.settings.animationDuration);
        });
    }
    
    // ===== CONTROLE DE NOTIFICAÇÕES =====
    close(id) {
        const notification = this.notifications.find(n => n.id === id);
        if (!notification) return;
        
        this.animateOut(notification).then(() => {
            this.removeNotification(notification);
        });
    }
    
    removeNotification(notification) {
        const index = this.notifications.indexOf(notification);
        if (index > -1) {
            this.notifications.splice(index, 1);
        }
        
        if (notification.element.parentNode) {
            notification.element.parentNode.removeChild(notification.element);
        }
    }
    
    closeAll() {
        this.notifications.forEach(notification => {
            this.close(notification.id);
        });
    }
    
    // ===== FUNÇÕES DE CONVENIÊNCIA =====
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }
    
    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }
    
    error(message, options = {}) {
        return this.show(message, 'error', options);
    }
    
    info(message, options = {}) {
        return this.show(message, 'info', options);
    }
    
    // ===== NOTIFICAÇÕES ESPECIAIS =====
    showProgress(message, progressCallback) {
        const notification = this.show(message, 'info', {
            progress: true,
            persistent: true
        });
        
        const progressBar = notification.element.querySelector('.notification-progress');
        
        if (progressCallback) {
            progressCallback((progress) => {
                if (progressBar) {
                    progressBar.style.width = `${progress}%`;
                    progressBar.style.background = '#10b981';
                    progressBar.style.height = '4px';
                    progressBar.style.transition = 'width 0.3s ease';
                }
                
                if (progress >= 100) {
                    setTimeout(() => {
                        this.close(notification.id);
                    }, 1000);
                }
            });
        }
        
        return notification;
    }
    
    showToast(message, type = 'info', duration = 3000) {
        const notification = this.show(message, type, {
            toast: true,
            persistent: false
        });
        
        setTimeout(() => {
            this.close(notification.id);
        }, duration);
        
        return notification;
    }
    
    // ===== AÇÕES =====
    executeAction(notificationId, actionKey) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (!notification || !notification.options.actions) return;
        
        const action = notification.options.actions.find(a => a.key === actionKey);
        if (action && action.callback) {
            action.callback(notification);
        }
    }
    
    // ===== AUTO-HIDE =====
    setupAutoHide(notification) {
        setTimeout(() => {
            if (this.notifications.includes(notification)) {
                this.close(notification.id);
            }
        }, this.settings.autoHideDelay);
    }
    
    // ===== SONS =====
    playSound(type) {
        try {
            const audio = new Audio(this.sounds[type] || this.sounds.info);
            audio.volume = 0.3;
            audio.play().catch(() => {
                // Ignorar erros de áudio
            });
        } catch (error) {
            // Fallback silencioso
        }
    }
    
    // ===== UTILITÁRIOS =====
    generateId() {
        return 'notification-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    }
    
    cleanupOldNotifications() {
        const now = Date.now();
        const maxAge = 300000; // 5 minutos
        
        this.notifications = this.notifications.filter(notification => {
            if (now - notification.timestamp > maxAge) {
                this.removeNotification(notification);
                return false;
            }
            return true;
        });
    }
    
    toggleContainer() {
        if (this.container.style.display === 'none') {
            this.container.style.display = 'block';
        } else {
            this.container.style.display = 'none';
        }
    }
    
    // ===== CONFIGURAÇÕES =====
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.saveSettings();
        
        // Aplicar mudanças
        if (newSettings.position) {
            this.container.className = `notification-container ${this.settings.position}`;
        }
    }
    
    getSettings() {
        return { ...this.settings };
    }
    
    // ===== ESTATÍSTICAS =====
    getStats() {
        return {
            total: this.notifications.length,
            byType: this.notifications.reduce((acc, n) => {
                acc[n.type] = (acc[n.type] || 0) + 1;
                return acc;
            }, {}),
            settings: this.settings
        };
    }
    
    // ===== LIMPEZA =====
    destroy() {
        this.closeAll();
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
        this.notifications = [];
        
        console.log('🧹 Sistema de Notificações destruído');
    }
}

// Criar instância global
const notificationSystem = new NotificationSystem();

// Exportar para uso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationSystem;
} else {
    window.NotificationSystem = NotificationSystem;
    window.notificationSystem = notificationSystem;
}
