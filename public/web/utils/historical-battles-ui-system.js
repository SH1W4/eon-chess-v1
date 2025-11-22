/**
 * 🏛️ Historical Battles UI System - AEON CHESS
 * Sistema avançado de interface para análise narrativa de jogos históricos
 * Gerenciamento dinâmico de cores e temas por batalha
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class HistoricalBattlesUISystem {
    constructor() {
        this.currentBattle = null;
        this.battleThemes = {
            'fischer-spassky': {
                id: 'fischer',
                name: 'Fischer vs Spassky',
                era: 'Guerra Fria',
                year: 1972,
                location: 'Reykjavik, Islândia',
                significance: 'Match do Século',
                colors: {
                    primary: '#1a365d',
                    secondary: '#2d3748',
                    accent: '#e53e3e',
                    complement: '#3182ce',
                    text: '#f7fafc'
                },
                players: {
                    white: {
                        name: 'Bobby Fischer',
                        country: 'USA',
                        flag: '🇺🇸'
                    },
                    black: {
                        name: 'Boris Spassky',
                        country: 'URSS',
                        flag: '🇷🇺'
                    }
                },
                symbolism: {
                    icon: '❄️',
                    pattern: 'cold-war',
                    atmosphere: 'Tensão geopolítica em 64 casas'
                }
            },
            'immortal-game': {
                id: 'immortal',
                name: 'Jogo Imortal',
                era: 'Romântico',
                year: 1851,
                location: 'Londres, Inglaterra',
                significance: 'Primeiro jogo imortal da história',
                colors: {
                    primary: '#744210',
                    secondary: '#553c0c',
                    accent: '#d69e2e',
                    complement: '#975a16',
                    text: '#faf5ff'
                },
                players: {
                    white: {
                        name: 'Adolf Anderssen',
                        country: 'Alemanha',
                        flag: '🇩🇪'
                    },
                    black: {
                        name: 'Lionel Kieseritzky',
                        country: 'França',
                        flag: '🇫🇷'
                    }
                },
                symbolism: {
                    icon: '⚔️',
                    pattern: 'medieval',
                    atmosphere: 'Cavalaria e honra no tabuleiro'
                }
            },
            'morphy-opera': {
                id: 'romantic',
                name: 'Paul Morphy na Ópera',
                era: 'Romântico',
                year: 1858,
                location: 'Paris, França',
                significance: 'Genialidade em consulta',
                colors: {
                    primary: '#553c9a',
                    secondary: '#322659',
                    accent: '#d6f5d6',
                    complement: '#9f7aea',
                    text: '#f4f4f5'
                },
                players: {
                    white: {
                        name: 'Paul Morphy',
                        country: 'USA',
                        flag: '🇺🇸'
                    },
                    black: {
                        name: 'Duque/Conde',
                        country: 'França',
                        flag: '🇫🇷'
                    }
                },
                symbolism: {
                    icon: '🎭',
                    pattern: 'elegant',
                    atmosphere: 'Arte e genialidade em harmonia'
                }
            },
            'capablanca-marshall': {
                id: 'hypermodern',
                name: 'Capablanca vs Marshall',
                era: 'Hipermoderno',
                year: 1909,
                location: 'New York, USA',
                significance: 'Ascensão do estilo posicional',
                colors: {
                    primary: '#2d3748',
                    secondary: '#1a202c',
                    accent: '#48bb78',
                    complement: '#38a169',
                    text: '#e2e8f0'
                },
                players: {
                    white: {
                        name: 'José Capablanca',
                        country: 'Cuba',
                        flag: '🇨🇺'
                    },
                    black: {
                        name: 'Frank Marshall',
                        country: 'USA',
                        flag: '🇺🇸'
                    }
                },
                symbolism: {
                    icon: '🏰',
                    pattern: 'geometric',
                    atmosphere: 'Lógica moderna sobre intuição'
                }
            },
            'kasparov-karpov': {
                id: 'soviet',
                name: 'Kasparov vs Karpov',
                era: 'Soviético',
                year: 1984,
                location: 'Moscou, URSS',
                significance: 'Batalha dos titãs soviéticos',
                colors: {
                    primary: '#c53030',
                    secondary: '#822727',
                    accent: '#ffd700',
                    complement: '#e53e3e',
                    text: '#f7fafc'
                },
                players: {
                    white: {
                        name: 'Garry Kasparov',
                        country: 'URSS',
                        flag: '🇷🇺'
                    },
                    black: {
                        name: 'Anatoly Karpov',
                        country: 'URSS',
                        flag: '🇷🇺'
                    }
                },
                symbolism: {
                    icon: '⭐',
                    pattern: 'communist',
                    atmosphere: 'Poder e ambição vermelha'
                }
            },
            'carlsen-anand': {
                id: 'modern',
                name: 'Carlsen vs Anand',
                era: 'Moderno',
                year: 2013,
                location: 'Chennai, Índia',
                significance: 'Nova geração assume o trono',
                colors: {
                    primary: '#065f46',
                    secondary: '#047857',
                    accent: '#06d6a0',
                    complement: '#10b981',
                    text: '#f0fdfa'
                },
                players: {
                    white: {
                        name: 'Magnus Carlsen',
                        country: 'Noruega',
                        flag: '🇳🇴'
                    },
                    black: {
                        name: 'Viswanathan Anand',
                        country: 'Índia',
                        flag: '🇮🇳'
                    }
                },
                symbolism: {
                    icon: '🌟',
                    pattern: 'nordic',
                    atmosphere: 'Precisão escandinava encontra sabedoria oriental'
                }
            },
            'deep-blue-kasparov': {
                id: 'digital',
                name: 'Deep Blue vs Kasparov',
                era: 'Digital',
                year: 1997,
                location: 'New York, USA',
                significance: 'Máquina vence humano',
                colors: {
                    primary: '#1e3a8a',
                    secondary: '#1e40af',
                    accent: '#00ffff',
                    complement: '#3b82f6',
                    text: '#f8fafc'
                },
                players: {
                    white: {
                        name: 'Deep Blue',
                        country: 'IBM',
                        flag: '🤖'
                    },
                    black: {
                        name: 'Garry Kasparov',
                        country: 'Rússia',
                        flag: '🇷🇺'
                    }
                },
                symbolism: {
                    icon: '💻',
                    pattern: 'circuit',
                    atmosphere: 'O futuro digital nasce'
                }
            }
        };

        this.currentTheme = null;
        this.isInitialized = false;

        this.init();
    }

    async init() {
        console.log('🏛️ Inicializando Sistema de Batalhas Históricas...');

        try {
            await this.waitForDOM();
            this.setupBattleSelector();
            this.createBattleInterface();
            this.setupEventListeners();
            this.loadDefaultBattle();

            this.isInitialized = true;
            console.log('✅ Sistema de Batalhas Históricas inicializado!');

        } catch (error) {
            console.error('❌ Erro na inicialização:', error);
        }
    }

    async waitForDOM() {
        if (document.readyState === 'loading') {
            await new Promise(resolve => {
                document.addEventListener('DOMContentLoaded', resolve);
            });
        }
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    setupBattleSelector() {
        const narrativeSection = document.getElementById('narrative-analysis');
        if (!narrativeSection) {
            console.warn('⚠️ Seção de análise narrativa não encontrada');
            return;
        }

        // Criar seletor de batalhas
        const battleSelector = document.createElement('div');
        battleSelector.className = 'battle-selector-container';
        battleSelector.innerHTML = `
            <div class="battle-selector-header">
                <h3 class="battle-selector-title">
                    <i class="fas fa-chess-king mr-2"></i>
                    Selecione uma Batalha Histórica
                </h3>
                <p class="battle-selector-subtitle">
                    Cada jogo com cores e atmosfera únicos
                </p>
            </div>
            
            <div class="battle-grid" id="battle-grid">
                ${this.generateBattleCards()}
            </div>
            
            <div class="battle-details-container" id="battle-details">
                <!-- Detalhes da batalha selecionada aparecerão aqui -->
            </div>
        `;

        // Inserir após o cabeçalho da seção
        const sectionHeader = narrativeSection.querySelector('.text-center');
        if (sectionHeader) {
            sectionHeader.insertAdjacentElement('afterend', battleSelector);
        }
    }

    generateBattleCards() {
        return Object.entries(this.battleThemes).map(([key, battle]) => `
            <div class="battle-preview-card" 
                 data-battle="${key}"
                 style="--battle-primary: ${battle.colors.primary}; 
                        --battle-accent: ${battle.colors.accent};">
                <div class="battle-preview-header">
                    <span class="battle-icon">${battle.symbolism.icon}</span>
                    <span class="battle-year">${battle.year}</span>
                </div>
                
                <h4 class="battle-preview-title">${battle.name}</h4>
                <p class="battle-preview-era">${battle.era}</p>
                <p class="battle-preview-location">${battle.location}</p>
                
                <div class="battle-preview-players">
                    <div class="player-mini">
                        <span class="player-flag">${battle.players.white.flag}</span>
                        <span class="player-name-mini">${battle.players.white.name}</span>
                    </div>
                    <div class="vs-separator">VS</div>
                    <div class="player-mini">
                        <span class="player-flag">${battle.players.black.flag}</span>
                        <span class="player-name-mini">${battle.players.black.name}</span>
                    </div>
                </div>
                
                <div class="battle-preview-significance">
                    ${battle.significance}
                </div>
                
                <div class="battle-color-preview">
                    <div class="color-dot" style="background: ${battle.colors.primary}"></div>
                    <div class="color-dot" style="background: ${battle.colors.accent}"></div>
                    <div class="color-dot" style="background: ${battle.colors.complement}"></div>
                </div>
            </div>
        `).join('');
    }

    createBattleInterface() {
        this.addBattleSelectorStyles();
    }

    addBattleSelectorStyles() {
        if (document.getElementById('battle-selector-styles')) return;

        const style = document.createElement('style');
        style.id = 'battle-selector-styles';
        style.textContent = `
            .battle-selector-container {
                margin: 40px 0;
                padding: 32px;
                background: rgba(0, 0, 0, 0.4);
                border-radius: 20px;
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .battle-selector-header {
                text-align: center;
                margin-bottom: 32px;
            }

            .battle-selector-title {
                font-size: 2rem;
                font-weight: 700;
                color: #f7fafc;
                margin-bottom: 8px;
            }

            .battle-selector-subtitle {
                color: #a0aec0;
                font-size: 1.1rem;
                margin: 0;
            }

            .battle-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 24px;
                margin-bottom: 32px;
            }

            .battle-preview-card {
                background: linear-gradient(145deg, 
                    rgba(26, 32, 44, 0.9) 0%, 
                    rgba(45, 55, 72, 0.8) 100%);
                border: 2px solid transparent;
                border-radius: 16px;
                padding: 24px;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .battle-preview-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(145deg, 
                    var(--battle-primary) 0%, 
                    var(--battle-accent) 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: -1;
            }

            .battle-preview-card:hover {
                transform: translateY(-8px) scale(1.02);
                border-color: var(--battle-accent);
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.4),
                    0 0 20px var(--battle-accent);
            }

            .battle-preview-card:hover::before {
                opacity: 0.1;
            }

            .battle-preview-card.selected {
                border-color: var(--battle-accent);
                box-shadow: 0 0 30px var(--battle-accent);
                transform: scale(1.05);
            }

            .battle-preview-card.selected::before {
                opacity: 0.2;
            }

            .battle-preview-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
            }

            .battle-icon {
                font-size: 2rem;
                filter: drop-shadow(0 0 10px var(--battle-accent));
            }

            .battle-year {
                background: var(--battle-accent);
                color: var(--battle-primary);
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.875rem;
            }

            .battle-preview-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #f7fafc;
                margin-bottom: 8px;
                background: linear-gradient(135deg, var(--battle-accent), #f7fafc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .battle-preview-era {
                color: var(--battle-accent);
                font-weight: 600;
                font-size: 0.9rem;
                margin-bottom: 4px;
            }

            .battle-preview-location {
                color: #a0aec0;
                font-size: 0.875rem;
                margin-bottom: 16px;
            }

            .battle-preview-players {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin: 16px 0;
                padding: 12px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 12px;
            }

            .player-mini {
                display: flex;
                align-items: center;
                gap: 8px;
                flex: 1;
            }

            .player-flag {
                font-size: 1.5rem;
            }

            .player-name-mini {
                font-size: 0.875rem;
                font-weight: 600;
                color: #e2e8f0;
            }

            .vs-separator {
                font-weight: 700;
                color: var(--battle-accent);
                margin: 0 12px;
                font-size: 0.875rem;
            }

            .battle-preview-significance {
                font-size: 0.875rem;
                color: #cbd5e0;
                font-style: italic;
                text-align: center;
                margin: 16px 0;
                padding: 8px;
                border-left: 3px solid var(--battle-accent);
                background: rgba(0, 0, 0, 0.2);
            }

            .battle-color-preview {
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-top: 16px;
            }

            .color-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            @media (max-width: 768px) {
                .battle-grid {
                    grid-template-columns: 1fr;
                    gap: 16px;
                }
                
                .battle-preview-card {
                    padding: 16px;
                }
                
                .battle-selector-container {
                    margin: 20px 0;
                    padding: 20px;
                }
            }
        `;

        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Event listener para seleção de batalhas
        document.addEventListener('click', (e) => {
            const battleCard = e.target.closest('.battle-preview-card');
            if (battleCard) {
                const battleKey = battleCard.dataset.battle;
                this.selectBattle(battleKey);
            }
        });
    }

    selectBattle(battleKey) {
        const battle = this.battleThemes[battleKey];
        if (!battle) {
            console.warn(`⚠️ Batalha não encontrada: ${battleKey}`);
            return;
        }

        // Remover seleção anterior
        document.querySelectorAll('.battle-preview-card.selected')
            .forEach(card => card.classList.remove('selected'));

        // Adicionar seleção atual
        const selectedCard = document.querySelector(`[data-battle="${battleKey}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }

        // Aplicar tema
        this.applyBattleTheme(battle);

        // Mostrar detalhes
        this.showBattleDetails(battle);

        this.currentBattle = battleKey;
        console.log(`🏛️ Batalha selecionada: ${battle.name}`);
    }

    applyBattleTheme(battle) {
        const narrativeSection = document.getElementById('narrative-analysis');
        if (!narrativeSection) return;

        // Remover classes de tema anteriores
        narrativeSection.className = narrativeSection.className
            .replace(/battle-\w+/g, '');

        // Aplicar novo tema
        narrativeSection.classList.add(`battle-${battle.id}`);

        // Atualizar CSS custom properties
        narrativeSection.style.setProperty('--primary', battle.colors.primary);
        narrativeSection.style.setProperty('--secondary', battle.colors.secondary);
        narrativeSection.style.setProperty('--accent', battle.colors.accent);
        narrativeSection.style.setProperty('--complement', battle.colors.complement);
        narrativeSection.style.setProperty('--text', battle.colors.text);

        this.currentTheme = battle;
        console.log(`🎨 Tema aplicado: ${battle.id}`);
    }

    showBattleDetails(battle) {
        const detailsContainer = document.getElementById('battle-details');
        if (!detailsContainer) return;

        detailsContainer.innerHTML = `
            <div class="battle-details-card battle-card">
                <div class="battle-header">
                    <div class="battle-icon-large">${battle.symbolism.icon}</div>
                    <div class="battle-info">
                        <h3 class="battle-title">${battle.name}</h3>
                        <p class="battle-subtitle">${battle.significance}</p>
                        <span class="battle-year">${battle.year}</span>
                        <p class="battle-location">📍 ${battle.location}</p>
                    </div>
                </div>

                <div class="battle-players">
                    <div class="player-card player-white">
                        <div class="player-flag-large">${battle.players.white.flag}</div>
                        <div class="player-name">${battle.players.white.name}</div>
                        <div class="player-country">${battle.players.white.country}</div>
                        <div class="player-pieces">♔ ♕ ♖ ♗ ♘ ♙</div>
                    </div>
                    
                    <div class="vs-large">
                        <div class="vs-text">VS</div>
                        <div class="vs-icon">⚔️</div>
                    </div>
                    
                    <div class="player-card player-black">
                        <div class="player-flag-large">${battle.players.black.flag}</div>
                        <div class="player-name">${battle.players.black.name}</div>
                        <div class="player-country">${battle.players.black.country}</div>
                        <div class="player-pieces">♚ ♛ ♜ ♝ ♞ ♟</div>
                    </div>
                </div>

                <div class="battle-atmosphere">
                    <div class="atmosphere-icon">${battle.symbolism.icon}</div>
                    <p class="atmosphere-text">${battle.symbolism.atmosphere}</p>
                </div>

                <div class="battle-controls">
                    <button class="btn-battle-action btn-start-analysis" data-battle="${this.currentBattle}">
                        <i class="fas fa-play mr-2"></i>
                        Iniciar Análise
                    </button>
                    <button class="btn-battle-action btn-view-moves" data-battle="${this.currentBattle}">
                        <i class="fas fa-chess-board mr-2"></i>
                        Ver Movimentos
                    </button>
                    <button class="btn-battle-action btn-ai-teacher" data-battle="${this.currentBattle}">
                        <i class="fas fa-graduation-cap mr-2"></i>
                        IA Professor
                    </button>
                </div>
            </div>
        `;

        // Aplicar classe do tema da batalha ao container dos detalhes
        detailsContainer.className = `battle-details-container battle-${battle.id}`;

        // Aplicar classe da batalha ao body para garantir que o CSS funcione
        document.body.classList.remove('battle-fischer', 'battle-immortal', 'battle-romantic', 'battle-hypermodern', 'battle-soviet', 'battle-modern', 'battle-ai');
        document.body.classList.add(`battle-${battle.id}`);

        // Forçar aplicação das cores imediatamente
        setTimeout(() => {
            this.forceApplyBattleColors(battle);
        }, 100);

        // Scroll suave para os detalhes
        detailsContainer.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });

        console.log(`🎨 Tema ${battle.id} aplicado aos botões da batalha`);
    }

    forceApplyBattleColors(battle) {
        console.log(`🎨 Forçando aplicação de cores para: ${battle.name}`);

        const battleButtons = document.querySelectorAll('.btn-battle-action');

        if (battleButtons.length === 0) {
            console.warn('⚠️ Nenhum botão de batalha encontrado para aplicar cores');
            return;
        }

        const colorMap = {
            'fischer-spassky': {
                primary: '#3182ce',
                secondary: '#e53e3e',
                shadow: 'rgba(49, 130, 206, 0.4)'
            },
            'immortal-game': {
                primary: '#d69e2e',
                secondary: '#975a16',
                shadow: 'rgba(214, 158, 46, 0.5)'
            },
            'morphy-opera': {
                primary: '#9f7aea',
                secondary: '#d6f5d6',
                shadow: 'rgba(159, 122, 234, 0.4)'
            },
            'capablanca-marshall': {
                primary: '#48bb78',
                secondary: '#38a169',
                shadow: 'rgba(72, 187, 120, 0.4)'
            },
            'kasparov-karpov': {
                primary: '#ffd700',
                secondary: '#e53e3e',
                shadow: 'rgba(255, 215, 0, 0.5)'
            },
            'carlsen-anand': {
                primary: '#06d6a0',
                secondary: '#10b981',
                shadow: 'rgba(6, 214, 160, 0.4)'
            },
            'deep-blue-kasparov': {
                primary: '#00ffff',
                secondary: '#3b82f6',
                shadow: 'rgba(0, 255, 255, 0.5)'
            }
        };

        const colors = colorMap[battle.id];
        if (!colors) {
            console.warn(`⚠️ Cores não definidas para batalha: ${battle.id}`);
            return;
        }

        battleButtons.forEach((button, index) => {
            // Aplicar estilos inline diretamente (mais forte que CSS)
            button.style.background = `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`;
            button.style.color = 'white';
            button.style.border = `1px solid ${colors.primary}`;
            button.style.boxShadow = `0 4px 15px ${colors.shadow}`;

            // Adicionar classe específica da batalha
            button.classList.add(`battle-${battle.id}-btn`);

            // Remover classes antigas de outras batalhas
            button.classList.remove('battle-fischer-btn', 'battle-immortal-btn', 'battle-romantic-btn', 'battle-hypermodern-btn', 'battle-soviet-btn', 'battle-modern-btn', 'battle-ai-btn');

            // Efeitos hover
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'translateY(-2px)';
                button.style.boxShadow = `0 8px 25px ${colors.shadow.replace('0.4', '0.6').replace('0.5', '0.7')}`;
            });

            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translateY(0)';
                button.style.boxShadow = `0 4px 15px ${colors.shadow}`;
            });

            console.log(`✅ Cores aplicadas ao botão ${index + 1}: ${button.textContent.trim()}`);
        });

        console.log(`🎨 Cores forçadas aplicadas a ${battleButtons.length} botões da batalha ${battle.name}`);

        // Verificar se as cores foram aplicadas corretamente
        setTimeout(() => {
            this.verifyBattleColors(battle);
        }, 200);
    }

    verifyBattleColors(battle) {
        console.log(`🔍 Verificando cores da batalha: ${battle.name}`);

        const battleButtons = document.querySelectorAll('.btn-battle-action');
        let colorsApplied = 0;

        battleButtons.forEach((button, index) => {
            const computedStyle = window.getComputedStyle(button);
            const background = computedStyle.background;
            const color = computedStyle.color;

            if (background && background !== 'rgba(0, 0, 0, 0)' && color && color !== 'rgba(0, 0, 0, 0)') {
                colorsApplied++;
                console.log(`✅ Botão ${index + 1} com cores aplicadas:`, {
                    background: background.substring(0, 50) + '...',
                    color: color
                });
            } else {
                console.warn(`⚠️ Botão ${index + 1} sem cores:`, {
                    background: background,
                    color: color
                });
            }
        });

        console.log(`🎨 Verificação concluída: ${colorsApplied}/${battleButtons.length} botões com cores aplicadas`);

        // Se algum botão não tiver cores, tentar aplicar novamente
        if (colorsApplied < battleButtons.length) {
            console.log(`🔄 Aplicando cores novamente...`);
            setTimeout(() => {
                this.forceApplyBattleColors(battle);
            }, 500);
        }
    }

    loadDefaultBattle() {
        // Carregar Fischer vs Spassky como padrão
        this.selectBattle('fischer-spassky');
    }

    // Métodos públicos para integração
    getCurrentBattle() {
        return this.currentBattle;
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    getBattleData(battleKey) {
        return this.battleThemes[battleKey];
    }

    getAllBattles() {
        return this.battleThemes;
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO E EXPORTAÇÃO
// ===============================

// Criar instância global
window.historicalBattlesUI = new HistoricalBattlesUISystem();

// Exportar para módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HistoricalBattlesUISystem;
}

// Log de carregamento
console.log('🏛️ Sistema de Interface de Batalhas Históricas carregado!');

export default HistoricalBattlesUISystem;