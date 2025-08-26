/**
 * 🎨 Battle Theme Demo - Demonstração do Sistema de Cores
 * Sistema para demonstrar e controlar temas de batalhas históricas
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class BattleThemeDemo {
    constructor() {
        this.isActive = false;
        this.demoInterval = null;
        this.currentIndex = 0;
        this.battles = [
            'fischer-spassky',
            'immortal-game',
            'morphy-opera',
            'capablanca-marshall',
            'kasparov-karpov',
            'carlsen-anand',
            'deep-blue-kasparov'
        ];

        this.init();
    }

    init() {
        console.log('🎨 Inicializando Demo de Temas de Batalha...');

        // Aguardar o sistema principal carregar
        this.waitForHistoricalSystem();

        // Criar controles de demo
        this.createDemoControls();

        console.log('✅ Demo de Temas inicializado!');
    }

    waitForHistoricalSystem() {
        const checkSystem = () => {
            if (window.historicalBattlesUI && window.historicalBattlesUI.isInitialized) {
                console.log('🔗 Sistema histórico detectado, ativando demo');
                this.setupDemo();
            } else {
                setTimeout(checkSystem, 500);
            }
        };
        checkSystem();
    }

    setupDemo() {
        // Expor métodos globalmente para teste
        window.battleDemo = this;

        // Adicionar comandos de console
        console.log(`
🎨 Demo de Temas de Batalha ativo!

Comandos disponíveis:
• battleDemo.startAutoDemo() - Demo automático
• battleDemo.stopAutoDemo() - Parar demo
• battleDemo.nextBattle() - Próxima batalha
• battleDemo.selectBattle('fischer-spassky') - Batalha específica
• battleDemo.showColorPalette() - Mostrar paleta de cores
• battleDemo.createColorComparison() - Comparar todas as cores

Batalhas disponíveis:
${this.battles.map(b => `• ${b}`).join('\n')}
        `);
    }

    createDemoControls() {
        // Verificar se deve mostrar controles de debug
        if (window.location.search.includes('demo=battle')) {
            this.createVisualControls();
        }
    }

    createVisualControls() {
        const controlPanel = document.createElement('div');
        controlPanel.id = 'battle-demo-controls';
        controlPanel.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 20px;
            border-radius: 12px;
            z-index: 10000;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            border: 1px solid #333;
            backdrop-filter: blur(20px);
            min-width: 280px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        `;

        controlPanel.innerHTML = `
            <div style="margin-bottom: 15px; text-align: center;">
                <strong>🎨 Demo de Temas de Batalha</strong>
            </div>
            
            <div style="margin-bottom: 12px;">
                <button id="demo-auto-start" class="demo-btn demo-btn-primary">
                    ▶️ Iniciar Demo Automático
                </button>
                <button id="demo-auto-stop" class="demo-btn demo-btn-secondary" disabled>
                    ⏹️ Parar Demo
                </button>
            </div>
            
            <div style="margin-bottom: 12px;">
                <label style="display: block; margin-bottom: 6px;">Batalha:</label>
                <select id="demo-battle-select" class="demo-select">
                    <option value="">Selecione uma batalha</option>
                    <option value="fischer-spassky">Fischer vs Spassky (1972)</option>
                    <option value="immortal-game">Jogo Imortal (1851)</option>
                    <option value="morphy-opera">Morphy na Ópera (1858)</option>
                    <option value="capablanca-marshall">Capablanca vs Marshall (1909)</option>
                    <option value="kasparov-karpov">Kasparov vs Karpov (1984)</option>
                    <option value="carlsen-anand">Carlsen vs Anand (2013)</option>
                    <option value="deep-blue-kasparov">Deep Blue vs Kasparov (1997)</option>
                </select>
            </div>
            
            <div style="margin-bottom: 12px;">
                <button id="demo-next" class="demo-btn demo-btn-accent">
                    ⏭️ Próxima Batalha
                </button>
                <button id="demo-colors" class="demo-btn demo-btn-accent">
                    🎨 Mostrar Cores
                </button>
            </div>
            
            <div style="margin-top: 15px; padding-top: 12px; border-top: 1px solid #444; font-size: 12px; opacity: 0.8;">
                <div id="demo-status">Aguardando...</div>
                <div id="demo-current-battle">Nenhuma batalha selecionada</div>
            </div>
        `;

        document.body.appendChild(controlPanel);
        this.addDemoStyles();
        this.setupDemoEventListeners();
    }

    addDemoStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .demo-btn {
                width: 100%;
                padding: 8px 12px;
                margin: 2px 0;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 12px;
                font-weight: 600;
                transition: all 0.2s ease;
            }
            
            .demo-btn-primary {
                background: linear-gradient(135deg, #10b981, #059669);
                color: white;
            }
            
            .demo-btn-secondary {
                background: linear-gradient(135deg, #6b7280, #4b5563);
                color: white;
            }
            
            .demo-btn-accent {
                background: linear-gradient(135deg, #3b82f6, #2563eb);
                color: white;
            }
            
            .demo-btn:hover:not(:disabled) {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }
            
            .demo-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .demo-select {
                width: 100%;
                padding: 8px;
                border: 1px solid #555;
                border-radius: 6px;
                background: #333;
                color: white;
                font-size: 12px;
            }
        `;
        document.head.appendChild(style);
    }

    setupDemoEventListeners() {
        document.getElementById('demo-auto-start').addEventListener('click', () => {
            this.startAutoDemo();
        });

        document.getElementById('demo-auto-stop').addEventListener('click', () => {
            this.stopAutoDemo();
        });

        document.getElementById('demo-next').addEventListener('click', () => {
            this.nextBattle();
        });

        document.getElementById('demo-colors').addEventListener('click', () => {
            this.showColorPalette();
        });

        document.getElementById('demo-battle-select').addEventListener('change', (e) => {
            if (e.target.value) {
                this.selectBattle(e.target.value);
            }
        });
    }

    startAutoDemo() {
        if (this.isActive) return;

        this.isActive = true;
        this.currentIndex = 0;

        // Atualizar interface
        document.getElementById('demo-auto-start').disabled = true;
        document.getElementById('demo-auto-stop').disabled = false;
        document.getElementById('demo-status').textContent = 'Demo automático ativo';

        // Iniciar ciclo
        this.demoInterval = setInterval(() => {
            this.nextBattle();
        }, 4000); // Troca a cada 4 segundos

        // Mostrar primeira batalha
        this.nextBattle();

        console.log('🎨 Demo automático iniciado');
    }

    stopAutoDemo() {
        if (!this.isActive) return;

        this.isActive = false;

        if (this.demoInterval) {
            clearInterval(this.demoInterval);
            this.demoInterval = null;
        }

        // Atualizar interface
        document.getElementById('demo-auto-start').disabled = false;
        document.getElementById('demo-auto-stop').disabled = true;
        document.getElementById('demo-status').textContent = 'Demo pausado';

        console.log('🎨 Demo automático parado');
    }

    nextBattle() {
        const battleKey = this.battles[this.currentIndex];
        this.selectBattle(battleKey);

        this.currentIndex = (this.currentIndex + 1) % this.battles.length;
    }

    selectBattle(battleKey) {
        if (!window.historicalBattlesUI) {
            console.warn('⚠️ Sistema histórico não disponível');
            return;
        }

        window.historicalBattlesUI.selectBattle(battleKey);

        // Atualizar interface
        const statusElement = document.getElementById('demo-current-battle');
        const selectElement = document.getElementById('demo-battle-select');

        if (statusElement) {
            const battle = window.historicalBattlesUI.getBattleData(battleKey);
            statusElement.textContent = `${battle.name} (${battle.year})`;
        }

        if (selectElement) {
            selectElement.value = battleKey;
        }

        console.log(`🎨 Batalha selecionada via demo: ${battleKey}`);
    }

    showColorPalette() {
        const battles = window.historicalBattlesUI ? .getAllBattles();
        if (!battles) {
            console.warn('⚠️ Dados de batalhas não disponíveis');
            return;
        }

        console.log('🎨 PALETA DE CORES DAS BATALHAS HISTÓRICAS:');
        console.log('');

        Object.entries(battles).forEach(([key, battle]) => {
            console.log(`🏛️ ${battle.name} (${battle.year}):`);
            console.log(`   Era: ${battle.era}`);
            console.log(`   Primária: ${battle.colors.primary}`);
            console.log(`   Accent: ${battle.colors.accent}`);
            console.log(`   Complementar: ${battle.colors.complement}`);
            console.log(`   Simbolismo: ${battle.symbolism.icon} - ${battle.symbolism.atmosphere}`);
            console.log('');
        });
    }

    createColorComparison() {
        const battles = window.historicalBattlesUI ? .getAllBattles();
        if (!battles) return;

        // Criar janela de comparação
        const comparisonWindow = document.createElement('div');
        comparisonWindow.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 30px;
            border-radius: 16px;
            z-index: 10001;
            max-width: 90vw;
            max-height: 90vh;
            overflow-y: auto;
            backdrop-filter: blur(20px);
            border: 1px solid #333;
        `;

        const colorsGrid = Object.entries(battles).map(([key, battle]) => `
            <div class="color-comparison-item" style="
                margin: 16px 0;
                padding: 16px;
                border-radius: 12px;
                background: linear-gradient(135deg, ${battle.colors.primary}, ${battle.colors.secondary});
                border: 1px solid ${battle.colors.accent};
            ">
                <h4 style="margin: 0 0 8px 0; color: ${battle.colors.text};">
                    ${battle.symbolism.icon} ${battle.name} (${battle.year})
                </h4>
                <p style="margin: 0 0 12px 0; opacity: 0.9; font-size: 14px;">
                    ${battle.era} • ${battle.location}
                </p>
                <div style="display: flex; gap: 8px; margin-top: 12px;">
                    <div style="
                        width: 40px; 
                        height: 20px; 
                        background: ${battle.colors.primary}; 
                        border-radius: 4px;
                        border: 1px solid rgba(255,255,255,0.3);
                    " title="Primária"></div>
                    <div style="
                        width: 40px; 
                        height: 20px; 
                        background: ${battle.colors.accent}; 
                        border-radius: 4px;
                        border: 1px solid rgba(255,255,255,0.3);
                    " title="Accent"></div>
                    <div style="
                        width: 40px; 
                        height: 20px; 
                        background: ${battle.colors.complement}; 
                        border-radius: 4px;
                        border: 1px solid rgba(255,255,255,0.3);
                    " title="Complementar"></div>
                </div>
            </div>
        `).join('');

        comparisonWindow.innerHTML = `
            <div style="text-align: center; margin-bottom: 24px;">
                <h3 style="margin: 0 0 8px 0;">🎨 Comparação de Cores das Batalhas</h3>
                <p style="margin: 0; opacity: 0.8; font-size: 14px;">
                    Cada batalha histórica tem sua paleta de cores única
                </p>
            </div>
            
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 16px;
            ">
                ${colorsGrid}
            </div>
            
            <div style="text-align: center; margin-top: 24px;">
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: linear-gradient(135deg, #ef4444, #dc2626);
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                ">Fechar</button>
            </div>
        `;

        document.body.appendChild(comparisonWindow);
    }

    // Métodos públicos para integração
    getBattlesList() {
        return this.battles;
    }

    getCurrentBattle() {
        return window.historicalBattlesUI ? .getCurrentBattle();
    }

    isRunning() {
        return this.isActive;
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO
// ===============================

// Inicializar automaticamente
document.addEventListener('DOMContentLoaded', () => {
    window.battleThemeDemo = new BattleThemeDemo();
});

// Log de carregamento
console.log('🎨 Demo de Temas de Batalha carregado!');