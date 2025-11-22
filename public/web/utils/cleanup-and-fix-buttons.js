/**
 * 🧹 Cleanup and Fix Buttons - AEON CHESS
 * Script para limpar botões desnecessários e corrigir cores das batalhas
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class CleanupAndFixButtons {
    constructor() {
        this.init();
    }

    async init() {
        console.log('🧹 Iniciando limpeza e correção de botões...');

        await this.waitForDOM();
        this.removeUnnecessaryButtons();
        this.fixBattleButtonColors();
        this.setupButtonObserver();

        console.log('✅ Limpeza e correção concluída!');
    }

    async waitForDOM() {
        if (document.readyState === 'loading') {
            await new Promise(resolve => {
                document.addEventListener('DOMContentLoaded', resolve);
            });
        }
        await new Promise(resolve => setTimeout(resolve, 1000)); // Aguardar sistemas carregarem
    }

    removeUnnecessaryButtons() {
        console.log('🗑️ Removendo botões desnecessários...');

        // Lista de botões para remover (mantendo apenas o FAB principal)
        const selectorsToRemove = [
            '#ai-recognition-test-button',
            '#ai-test-functionality-button',
            'button[title*="Testar"]',
            '.ai-button-discrete:not(#ai-fab)',
            'button[onclick*="showDemo"]:not(#ai-fab)',
            'button[onclick*="analyze"]:not(#ai-fab)',
            '.btn-secondary[onclick*="generate"]:not(#ai-fab)'
        ];

        let removedCount = 0;

        selectorsToRemove.forEach(selector => {
            const buttons = document.querySelectorAll(selector);
            buttons.forEach(button => {
                // Verificar se não é o FAB principal
                if (button.id !== 'ai-fab') {
                    console.log(`🗑️ Removendo botão: ${selector}`, button);
                    button.remove();
                    removedCount++;
                }
            });
        });

        console.log(`✅ ${removedCount} botões desnecessários removidos`);

        // Verificar se ainda existem botões problemáticos
        this.reportRemainingButtons();
    }

    reportRemainingButtons() {
        const fixedPositionButtons = document.querySelectorAll('button[style*="position: fixed"], div[style*="position: fixed"]');
        const fabButtons = document.querySelectorAll('.fab, [id*="fab"], [class*="fab"]');

        console.log('📊 Relatório de botões restantes:');
        console.log(`   • Botões position: fixed: ${fixedPositionButtons.length}`);
        console.log(`   • Botões FAB: ${fabButtons.length}`);

        // Listar botões restantes
        fixedPositionButtons.forEach((btn, index) => {
            if (btn.id !== 'ai-fab') {
                console.log(`   ⚠️ Botão fixo extra #${index + 1}:`, btn.id || btn.className || 'sem id/classe', btn);
            }
        });
    }

    fixBattleButtonColors() {
        console.log('🎨 Corrigindo cores dos botões das batalhas...');

        // Aguardar sistema de batalhas estar pronto
        this.waitForBattleSystem();
    }

    waitForBattleSystem() {
        const checkBattleSystem = () => {
            if (window.historicalBattlesUI && window.historicalBattlesUI.isInitialized) {
                this.applyBattleButtonFixes();
            } else {
                setTimeout(checkBattleSystem, 500);
            }
        };
        checkBattleSystem();
    }

    applyBattleButtonFixes() {
        console.log('🔧 Aplicando correções nos botões das batalhas...');

        // Força a reaplicação das cores quando botões são criados
        const originalShowBattleDetails = window.historicalBattlesUI.showBattleDetails;

        window.historicalBattlesUI.showBattleDetails = function(battle) {
            // Chamar método original
            originalShowBattleDetails.call(this, battle);

            // Aguardar DOM atualizar e aplicar correções
            setTimeout(() => {
                window.cleanupButtons.forceBattleButtonColors(battle);
            }, 100);
        };

        console.log('✅ Correções aplicadas ao sistema de batalhas');
    }

    forceBattleButtonColors(battle) {
        if (!battle) return;

        console.log(`🎨 Forçando cores para batalha: ${battle.name} (${battle.id})`);

        // Encontrar todos os botões de batalha
        const battleButtons = document.querySelectorAll('.btn-battle-action');

        if (battleButtons.length === 0) {
            console.warn('⚠️ Nenhum botão de batalha encontrado');
            return;
        }

        // Aplicar estilos inline como fallback
        battleButtons.forEach(button => {
            const colors = this.getBattleColors(battle.id);
            if (colors) {
                button.style.background = `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`;
                button.style.color = colors.text;
                button.style.border = `1px solid ${colors.accent}`;
                button.style.boxShadow = `0 4px 15px ${colors.shadow}`;

                // Efeito hover
                button.addEventListener('mouseenter', () => {
                    button.style.transform = 'translateY(-2px)';
                    button.style.boxShadow = `0 8px 25px ${colors.shadowHover}`;
                });

                button.addEventListener('mouseleave', () => {
                    button.style.transform = 'translateY(0)';
                    button.style.boxShadow = `0 4px 15px ${colors.shadow}`;
                });

                console.log(`✅ Cores aplicadas ao botão: ${button.textContent.trim()}`);
            }
        });

        // Também aplicar classe de tema ao container pai
        const detailsContainer = document.getElementById('battle-details');
        if (detailsContainer) {
            detailsContainer.classList.add(`battle-${battle.id}`);
            console.log(`🎨 Classe battle-${battle.id} aplicada ao container`);
        }
    }

    getBattleColors(battleId) {
        const colorMap = {
            'fischer': {
                primary: '#3182ce',
                secondary: '#e53e3e',
                accent: '#3182ce',
                text: 'white',
                shadow: 'rgba(49, 130, 206, 0.4)',
                shadowHover: 'rgba(49, 130, 206, 0.6)'
            },
            'immortal': {
                primary: '#d69e2e',
                secondary: '#975a16',
                accent: '#d69e2e',
                text: '#553c0c',
                shadow: 'rgba(214, 158, 46, 0.5)',
                shadowHover: 'rgba(214, 158, 46, 0.7)'
            },
            'romantic': {
                primary: '#9f7aea',
                secondary: '#d6f5d6',
                accent: '#9f7aea',
                text: '#553c9a',
                shadow: 'rgba(159, 122, 234, 0.4)',
                shadowHover: 'rgba(159, 122, 234, 0.6)'
            },
            'hypermodern': {
                primary: '#48bb78',
                secondary: '#38a169',
                accent: '#48bb78',
                text: 'white',
                shadow: 'rgba(72, 187, 120, 0.4)',
                shadowHover: 'rgba(72, 187, 120, 0.6)'
            },
            'soviet': {
                primary: '#ffd700',
                secondary: '#e53e3e',
                accent: '#ffd700',
                text: '#822727',
                shadow: 'rgba(255, 215, 0, 0.5)',
                shadowHover: 'rgba(255, 215, 0, 0.7)'
            },
            'modern': {
                primary: '#06d6a0',
                secondary: '#10b981',
                accent: '#06d6a0',
                text: '#065f46',
                shadow: 'rgba(6, 214, 160, 0.4)',
                shadowHover: 'rgba(6, 214, 160, 0.6)'
            },
            'digital': {
                primary: '#00ffff',
                secondary: '#3b82f6',
                accent: '#00ffff',
                text: 'white',
                shadow: 'rgba(0, 255, 255, 0.5)',
                shadowHover: 'rgba(0, 255, 255, 0.7)'
            }
        };

        return colorMap[battleId];
    }

    setupButtonObserver() {
        // Observar mudanças no DOM para capturar novos botões
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    // Verificar se novos botões de teste foram adicionados
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) { // Element node
                            // Remover botões de teste que possam ter sido adicionados
                            const testButtons = node.querySelectorAll && node.querySelectorAll('[id*="test"], [title*="Testar"]');
                            if (testButtons) {
                                testButtons.forEach(btn => {
                                    if (btn.id !== 'ai-fab') {
                                        console.log('🗑️ Removendo botão de teste adicionado dinamicamente:', btn);
                                        btn.remove();
                                    }
                                });
                            }
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        console.log('👁️ Observer configurado para monitorar novos botões');
    }

    // Método público para forçar limpeza manual
    manualCleanup() {
        console.log('🧹 Limpeza manual ativada...');
        this.removeUnnecessaryButtons();

        // Reaportar status
        setTimeout(() => {
            this.reportRemainingButtons();
        }, 1000);
    }

    // Método público para forçar correção de cores
    manualColorFix() {
        console.log('🎨 Correção manual de cores ativada...');

        if (window.historicalBattlesUI && window.historicalBattlesUI.currentTheme) {
            this.forceBattleButtonColors(window.historicalBattlesUI.currentTheme);
        } else {
            console.warn('⚠️ Nenhuma batalha selecionada para aplicar cores');
        }
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO AUTOMÁTICA
// ===============================

// Criar instância global
window.cleanupButtons = new CleanupAndFixButtons();

// Expor métodos para console
console.log(`
🧹 Sistema de Limpeza e Correção carregado!

Comandos disponíveis:
• cleanupButtons.manualCleanup() - Limpeza manual de botões
• cleanupButtons.manualColorFix() - Correção manual de cores
• cleanupButtons.reportRemainingButtons() - Relatório de botões restantes

O sistema remove automaticamente botões desnecessários e 
garante que os botões das batalhas tenham as cores corretas!
`);