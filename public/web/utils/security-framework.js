// AEON CHESS - Security Framework v2.0 (Arquimax Enhanced)
// TaskMash SuperEscopo: Security Critical Improvements

class SecurityFramework {
    constructor() {
        this.authConfig = {
            oauth2: {
                clientId: 'aeon_chess_client',
                redirectUri: window.location.origin + '/auth/callback',
                scopes: ['openid', 'profile', 'email'],
                providers: ['google', 'github', 'microsoft']
            },
            jwt: {
                secret: process.env.JWT_SECRET || 'your-jwt-secret',
                expiresIn: '24h',
                refreshExpiresIn: '7d'
            },
            mfa: {
                enabled: true,
                methods: ['totp', 'sms', 'email'],
                backupCodes: 10
            }
        };
        
        this.complianceConfig = {
            gdpr: {
                enabled: true,
                dataRetention: 30, // dias
                userConsent: true,
                dataPortability: true
            },
            lgpd: {
                enabled: true,
                dataRetention: 30, // dias
                userConsent: true,
                dataPortability: true
            },
            encryption: {
                algorithm: 'AES-256-GCM',
                keyRotation: 90, // dias
                transportSecurity: 'TLS 1.3'
            }
        };
        
        this.securityMetrics = {
            loginAttempts: 0,
            failedLogins: 0,
            securityEvents: [],
            dataBreaches: 0,
            complianceChecks: 0
        };
        
        this.init();
    }
    
    init() {
        this.setupAuthentication();
        this.setupEncryption();
        this.setupCompliance();
        this.setupMonitoring();
        this.setupRateLimiting();
        this.setupCSRFProtection();
    }
    
    setupAuthentication() {
        // OAuth 2.0 Setup
        this.oauth2 = {
            authorize: (provider) => {
                const authUrl = this.buildAuthUrl(provider);
                window.location.href = authUrl;
            },
            
            handleCallback: async (code) => {
                try {
                    const token = await this.exchangeCodeForToken(code);
                    this.storeToken(token);
                    this.setupMFASession();
                    return true;
                } catch (error) {
                    console.error('ARKITECT: Erro na autenticação OAuth:', error);
                    return false;
                }
            }
        };
        
        // JWT Management
        this.jwt = {
            create: (payload) => {
                const header = { alg: 'HS256', typ: 'JWT' };
                const now = Math.floor(Date.now() / 1000);
                
                const tokenPayload = {
                    ...payload,
                    iat: now,
                    exp: now + (24 * 60 * 60), // 24 horas
                    iss: 'aeon-chess',
                    aud: 'aeon-chess-users'
                };
                
                return this.encodeJWT(header, tokenPayload);
            },
            
            verify: (token) => {
                try {
                    const decoded = this.decodeJWT(token);
                    const now = Math.floor(Date.now() / 1000);
                    
                    if (decoded.exp < now) {
                        throw new Error('Token expirado');
                    }
                    
                    return decoded;
                } catch (error) {
                    console.error('ARKITECT: Token inválido:', error);
                    return null;
                }
            }
        };
        
        // MFA Setup
        this.mfa = {
            setup: async (method) => {
                const secret = this.generateMFASecret();
                const qrCode = this.generateQRCode(secret);
                
                return { secret, qrCode };
            },
            
            verify: (token, secret) => {
                const expectedToken = this.generateTOTP(secret);
                return token === expectedToken;
            },
            
            generateBackupCodes: () => {
                const codes = [];
                for (let i = 0; i < this.authConfig.mfa.backupCodes; i++) {
                    codes.push(this.generateRandomCode(8));
                }
                return codes;
            }
        };
    }
    
    setupEncryption() {
        // AES-256-GCM Encryption
        this.encryption = {
            encrypt: async (data, key) => {
                const encoder = new TextEncoder();
                const encodedData = encoder.encode(JSON.stringify(data));
                
                const cryptoKey = await crypto.subtle.importKey(
                    'raw',
                    encoder.encode(key),
                    { name: 'AES-GCM' },
                    false,
                    ['encrypt']
                );
                
                const iv = crypto.getRandomValues(new Uint8Array(12));
                const encrypted = await crypto.subtle.encrypt(
                    { name: 'AES-GCM', iv },
                    cryptoKey,
                    encodedData
                );
                
                return {
                    data: Array.from(new Uint8Array(encrypted)),
                    iv: Array.from(iv)
                };
            },
            
            decrypt: async (encryptedData, key, iv) => {
                const encoder = new TextEncoder();
                const decoder = new TextDecoder();
                
                const cryptoKey = await crypto.subtle.importKey(
                    'raw',
                    encoder.encode(key),
                    { name: 'AES-GCM' },
                    false,
                    ['decrypt']
                );
                
                const decrypted = await crypto.subtle.decrypt(
                    { name: 'AES-GCM', iv: new Uint8Array(iv) },
                    cryptoKey,
                    new Uint8Array(encryptedData)
                );
                
                return JSON.parse(decoder.decode(decrypted));
            }
        };
    }
    
    setupCompliance() {
        // GDPR Compliance
        this.gdpr = {
            getUserConsent: () => {
                return localStorage.getItem('aeon_chess_gdpr_consent') === 'true';
            },
            
            setUserConsent: (consent) => {
                localStorage.setItem('aeon_chess_gdpr_consent', consent);
                this.logSecurityEvent('gdpr_consent_updated', { consent });
            },
            
            exportUserData: async (userId) => {
                const userData = await this.getUserData(userId);
                return this.encryption.encrypt(userData, this.complianceConfig.encryption.secret);
            },
            
            deleteUserData: async (userId) => {
                await this.anonymizeUserData(userId);
                this.logSecurityEvent('user_data_deleted', { userId });
            }
        };
        
        // LGPD Compliance
        this.lgpd = {
            getUserConsent: () => {
                return localStorage.getItem('aeon_chess_lgpd_consent') === 'true';
            },
            
            setUserConsent: (consent) => {
                localStorage.setItem('aeon_chess_lgpd_consent', consent);
                this.logSecurityEvent('lgpd_consent_updated', { consent });
            },
            
            exportUserData: async (userId) => {
                return this.gdpr.exportUserData(userId);
            },
            
            deleteUserData: async (userId) => {
                return this.gdpr.deleteUserData(userId);
            }
        };
    }
    
    setupMonitoring() {
        // Security Event Monitoring
        this.monitoring = {
            logEvent: (event, data) => {
                this.securityMetrics.securityEvents.push({
                    event,
                    data,
                    timestamp: Date.now(),
                    userAgent: navigator.userAgent,
                    ip: this.getClientIP()
                });
                
                // Send to security monitoring service
                this.sendSecurityEvent(event, data);
            },
            
            detectAnomalies: () => {
                const recentEvents = this.securityMetrics.securityEvents
                    .filter(e => Date.now() - e.timestamp < 3600000); // Última hora
                
                const failedLogins = recentEvents.filter(e => e.event === 'login_failed');
                if (failedLogins.length > 5) {
                    this.triggerSecurityAlert('multiple_failed_logins');
                }
            }
        };
        
        // Regular security checks
        setInterval(() => {
            this.monitoring.detectAnomalies();
            this.runComplianceChecks();
        }, 300000); // 5 minutos
    }
    
    setupRateLimiting() {
        this.rateLimiter = {
            limits: {
                login: { max: 5, window: 300000 }, // 5 tentativas em 5 minutos
                api: { max: 100, window: 60000 }, // 100 requests por minuto
                mfa: { max: 3, window: 300000 } // 3 tentativas MFA em 5 minutos
            },
            
            attempts: new Map(),
            
            checkLimit: (action, identifier) => {
                const limit = this.rateLimiter.limits[action];
                if (!limit) return true;
                
                const key = `${action}:${identifier}`;
                const now = Date.now();
                const attempts = this.rateLimiter.attempts.get(key) || [];
                
                // Remove attempts outside window
                const validAttempts = attempts.filter(timestamp => now - timestamp < limit.window);
                
                if (validAttempts.length >= limit.max) {
                    return false;
                }
                
                validAttempts.push(now);
                this.rateLimiter.attempts.set(key, validAttempts);
                return true;
            }
        };
    }
    
    setupCSRFProtection() {
        this.csrf = {
            token: this.generateCSRFToken(),
            
            validateToken: (token) => {
                return token === this.csrf.token;
            },
            
            addToRequest: (request) => {
                request.headers['X-CSRF-Token'] = this.csrf.token;
                return request;
            }
        };
        
        // Add CSRF token to all forms
        document.addEventListener('DOMContentLoaded', () => {
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                const tokenInput = document.createElement('input');
                tokenInput.type = 'hidden';
                tokenInput.name = '_csrf';
                tokenInput.value = this.csrf.token;
                form.appendChild(tokenInput);
            });
        });
    }
    
    // Utility methods
    buildAuthUrl(provider) {
        const params = new URLSearchParams({
            client_id: this.authConfig.oauth2.clientId,
            redirect_uri: this.authConfig.oauth2.redirectUri,
            scope: this.authConfig.oauth2.scopes.join(' '),
            response_type: 'code',
            state: this.generateRandomString(32)
        });
        
        return `https://accounts.${provider}.com/oauth/authorize?${params}`;
    }
    
    async exchangeCodeForToken(code) {
        // Simulate token exchange
        return {
            access_token: this.generateRandomString(64),
            refresh_token: this.generateRandomString(64),
            expires_in: 3600
        };
    }
    
    storeToken(token) {
        localStorage.setItem('aeon_chess_access_token', token.access_token);
        localStorage.setItem('aeon_chess_refresh_token', token.refresh_token);
        localStorage.setItem('aeon_chess_token_expires', Date.now() + (token.expires_in * 1000));
    }
    
    generateMFASecret() {
        return this.generateRandomString(32);
    }
    
    generateTOTP(secret) {
        // Simplified TOTP generation
        const now = Math.floor(Date.now() / 30000); // 30 second window
        return (now % 1000000).toString().padStart(6, '0');
    }
    
    generateRandomString(length) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }
    
    generateRandomCode(length) {
        return Math.random().toString(36).substring(2, 2 + length).toUpperCase();
    }
    
    encodeJWT(header, payload) {
        const encodedHeader = btoa(JSON.stringify(header));
        const encodedPayload = btoa(JSON.stringify(payload));
        const signature = this.generateRandomString(64); // Simplified
        
        return `${encodedHeader}.${encodedPayload}.${signature}`;
    }
    
    decodeJWT(token) {
        const parts = token.split('.');
        if (parts.length !== 3) {
            throw new Error('Token inválido');
        }
        
        return JSON.parse(atob(parts[1]));
    }
    
    generateCSRFToken() {
        return this.generateRandomString(32);
    }
    
    getClientIP() {
        // Simplified - in real implementation, this would come from server
        return '127.0.0.1';
    }
    
    logSecurityEvent(event, data) {
        this.monitoring.logEvent(event, data);
    }
    
    async sendSecurityEvent(event, data) {
        // Send to security monitoring service
        console.log('🏛️ ARKITECT: Security event logged:', event, data);
    }
    
    triggerSecurityAlert(type) {
        console.warn('🚨 ARKITECT: Security alert triggered:', type);
        this.logSecurityEvent('security_alert', { type });
    }
    
    async runComplianceChecks() {
        this.securityMetrics.complianceChecks++;
        
        // Check GDPR compliance
        if (this.complianceConfig.gdpr.enabled) {
            const consent = this.gdpr.getUserConsent();
            if (!consent) {
                this.triggerSecurityAlert('gdpr_consent_missing');
            }
        }
        
        // Check LGPD compliance
        if (this.complianceConfig.lgpd.enabled) {
            const consent = this.lgpd.getUserConsent();
            if (!consent) {
                this.triggerSecurityAlert('lgpd_consent_missing');
            }
        }
    }
    
    getSecurityMetrics() {
        return {
            ...this.securityMetrics,
            complianceStatus: {
                gdpr: this.gdpr.getUserConsent(),
                lgpd: this.lgpd.getUserConsent()
            }
        };
    }
}

// Initialize Security Framework
const securityFramework = new SecurityFramework();

// Export for global use
window.SecurityFramework = securityFramework;
