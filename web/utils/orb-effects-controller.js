/**
 * 🎛️ Orb Effects Controller - Controlador de Efeitos das Bolas
 * Sistema para controlar a intensidade e estilo das bolas de fundo
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class OrbEffectsController {
    constructor() {
        this.currentEffect = 'subtle';
        this.currentIntensity = 'subtle';
        this.currentColor = 'white';
        this.isActive = true;

        this.init();
    }

    init() {
        console.log('🎨 Inicializando controlador de efeitos de bolas...');

        // Aplicar efeito padrão
        this.applyEffect('subtle');

        // Criar controles de debug (opcional)
        if (window.location.search.includes('debug=orbs')) {
            this.createDebugControls();
        }

        // Expor métodos globalmente para teste
        window.orbController = this;

        console.log('✅ Controlador de bolas inicializado!');
    }

    applyEffect(effectType = 'subtle') {
        const body = document.body;

        // Remover classes anteriores
        this.removeAllOrbClasses(body);

        // Aplicar nova classe
        switch (effectType) {
            case 'subtle':
                // Efeito já está no CSS principal
                break;
            case 'dramatic':
                body.classList.add('orb-effect-dramatic');
                break;
            case 'multiple':
                body.classList.add('orb-effect-multiple');
                this.createExtraOrbs();
                break;
            case 'none':
                this.isActive = false;
                body.style.setProperty('--orb-display', 'none');
                break;
        }

        this.currentEffect = effectType;
        console.log(`🎨 Efeito aplicado: ${effectType}`);
    }

    setIntensity(intensity = 'subtle') {
        const body = document.body;

        // Remover classes de intensidade anteriores
        body.classList.remove('orb-intensity-minimal', 'orb-intensity-subtle', 'orb-intensity-medium', 'orb-intensity-strong');

        // Aplicar nova intensidade
        body.classList.add(`orb-intensity-${intensity}`);

        this.currentIntensity = intensity;
        console.log(`✨ Intensidade aplicada: ${intensity}`);
    }

    setColor(color = 'white') {
        const body = document.body;

        // Remover classes de cor anteriores
        body.classList.remove('orb-color-blue', 'orb-color-gold');

        // Aplicar nova cor (se não for branca)
        if (color !== 'white') {
            body.classList.add(`orb-color-${color}`);
        }

        this.currentColor = color;
        console.log(`🎨 Cor aplicada: ${color}`);
    }

    removeAllOrbClasses(element) {
        const orbClasses = [
            'orb-effect-subtle',
            'orb-effect-dramatic',
            'orb-effect-multiple',
            'orb-intensity-minimal',
            'orb-intensity-subtle',
            'orb-intensity-medium',
            'orb-intensity-strong',
            'orb-color-blue',
            'orb-color-gold'
        ];

        orbClasses.forEach(className => {
            element.classList.remove(className);
        });
    }

    createExtraOrbs() {
        // Remover bolas extras existentes
        document.querySelectorAll('.orb-extra').forEach(orb => orb.remove());

        // Criar bolas extras para efeito múltiplo
        const extraOrb1 = document.createElement('div');
        extraOrb1.className = 'orb-extra orb-extra-1';
        document.body.appendChild(extraOrb1);

        const extraOrb2 = document.createElement('div');
        extraOrb2.className = 'orb-extra orb-extra-2';
        document.body.appendChild(extraOrb2);

        console.log('🌟 Bolas extras criadas');
    }

    createDebugControls() {
        // Criar painel de controle para debug
        const debugPanel = document.createElement('div');
        debugPanel.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            z-index: 10000;
            font-family: monospace;
            font-size: 12px;
            border: 1px solid #333;
            backdrop-filter: blur(10px);
        `;

        debugPanel.innerHTML = `
            <div style="margin-bottom: 15px;">
                <strong>🎨 Orb Effects Debug</strong>
            </div>
            
            <div style="margin-bottom: 10px;">
                <label>Efeito:</label><br>
                <select id="orb-effect-select" style="width: 100%; padding: 5px; margin-top: 5px; background: #333; color: white; border: 1px solid #555;">
                    <option value="subtle">Sutil</option>
                    <option value="dramatic">Dramático</option>
                    <option value="multiple">Múltiplas</option>
                    <option value="none">Nenhum</option>
                </select>
            </div>
            
            <div style="margin-bottom: 10px;">
                <label>Intensidade:</label><br>
                <select id="orb-intensity-select" style="width: 100%; padding: 5px; margin-top: 5px; background: #333; color: white; border: 1px solid #555;">
                    <option value="minimal">Mínima</option>
                    <option value="subtle">Sutil</option>
                    <option value="medium">Média</option>
                    <option value="strong">Forte</option>
                </select>
            </div>
            
            <div style="margin-bottom: 10px;">
                <label>Cor:</label><br>
                <select id="orb-color-select" style="width: 100%; padding: 5px; margin-top: 5px; background: #333; color: white; border: 1px solid #555;">
                    <option value="white">Branca</option>
                    <option value="blue">Azul</option>
                    <option value="gold">Dourada</option>
                </select>
            </div>
            
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #555; font-size: 10px; opacity: 0.7;">
                Current: ${this.currentEffect} / ${this.currentIntensity} / ${this.currentColor}
            </div>
        `;

        document.body.appendChild(debugPanel);

        // Adicionar event listeners
        document.getElementById('orb-effect-select').addEventListener('change', (e) => {
            this.applyEffect(e.target.value);
        });

        document.getElementById('orb-intensity-select').addEventListener('change', (e) => {
            this.setIntensity(e.target.value);
        });

        document.getElementById('orb-color-select').addEventListener('change', (e) => {
            this.setColor(e.target.value);
        });

        console.log('🛠️ Painel de debug criado - Adicione ?debug=orbs na URL para ver');
    }

    // Métodos de conveniência para testes rápidos
    subtle() {
        this.applyEffect('subtle');
    }
    dramatic() {
        this.applyEffect('dramatic');
    }
    multiple() {
        this.applyEffect('multiple');
    }
    none() {
        this.applyEffect('none');
    }

    minimal() {
        this.setIntensity('minimal');
    }
    medium() {
        this.setIntensity('medium');
    }
    strong() {
        this.setIntensity('strong');
    }

    blue() {
        this.setColor('blue');
    }
    gold() {
        this.setColor('gold');
    }
    white() {
        this.setColor('white');
    }

    // Status atual
    status() {
        console.log(`🎨 Status das bolas:
        - Efeito: ${this.currentEffect}
        - Intensidade: ${this.currentIntensity}
        - Cor: ${this.currentColor}
        - Ativo: ${this.isActive}`);
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO AUTOMÁTICA
// ===============================

// Inicializar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.orbEffects = new OrbEffectsController();
    });
} else {
    window.orbEffects = new OrbEffectsController();
}

// Comandos de console para testes rápidos
console.log(`
🎨 Orb Effects Controller carregado!

Comandos de teste disponíveis:
• orbController.dramatic() - Efeito dramático
• orbController.subtle() - Efeito sutil  
• orbController.multiple() - Múltiplas bolas
• orbController.none() - Desativar

• orbController.minimal() - Intensidade mínima
• orbController.medium() - Intensidade média
• orbController.strong() - Intensidade forte

• orbController.blue() - Cor azul
• orbController.gold() - Cor dourada
• orbController.white() - Cor branca

• orbController.status() - Ver status atual

Para painel visual: adicione ?debug=orbs na URL
`);

export default OrbEffectsController;