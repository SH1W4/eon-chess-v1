// AEON CHESS - Integração de Gamificação com IA Generativa
// Versão: 1.0 - Sistema de Recompensas para Tabuleiros IA

class AIGamificationIntegration {
    constructor() {
        this.achievements = {
            'first-ai-board': {
                id: 'first-ai-board',
                name: 'Primeiro Tabuleiro IA',
                description: 'Gerou seu primeiro tabuleiro com inteligência artificial',
                icon: 'fas fa-robot',
                points: 100,
                category: 'ai-generation',
                unlocked: false
            },
            'ai-master': {
                id: 'ai-master',
                name: 'Mestre da IA',
                description: 'Gerou 50 tabuleiros únicos com IA',
                icon: 'fas fa-crown',
                points: 500,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 50
            },
            'creative-genius': {
                id: 'creative-genius',
                name: 'Gênio Criativo',
                description: 'Gerou 20 tabuleiros com tema criativo',
                icon: 'fas fa-lightbulb',
                points: 300,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 20
            },
            'tactical-expert': {
                id: 'tactical-expert',
                name: 'Especialista Tático',
                description: 'Gerou 20 tabuleiros com tema tático',
                icon: 'fas fa-bolt',
                points: 300,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 20
            },
            'strategic-mind': {
                id: 'strategic-mind',
                name: 'Mente Estratégica',
                description: 'Gerou 20 tabuleiros com tema estratégico',
                icon: 'fas fa-chess-king',
                points: 300,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 20
            },
            'artistic-soul': {
                id: 'artistic-soul',
                name: 'Alma Artística',
                description: 'Gerou 20 tabuleiros com tema artístico',
                icon: 'fas fa-palette',
                points: 300,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 20
            },
            'ai-collector': {
                id: 'ai-collector',
                name: 'Colecionador IA',
                description: 'Salvou 25 tabuleiros nos favoritos',
                icon: 'fas fa-heart',
                points: 400,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 25
            },
            'ai-player': {
                id: 'ai-player',
                name: 'Jogador IA',
                description: 'Jogou 30 tabuleiros gerados por IA',
                icon: 'fas fa-play',
                points: 400,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 30
            },
            'ai-analyzer': {
                id: 'ai-analyzer',
                name: 'Analisador IA',
                description: 'Analisou 20 tabuleiros com IA',
                icon: 'fas fa-brain',
                points: 350,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 20
            },
            'ai-batch-master': {
                id: 'ai-batch-master',
                name: 'Mestre do Lote',
                description: 'Gerou 10 lotes de tabuleiros',
                icon: 'fas fa-layer-group',
                points: 600,
                category: 'ai-generation',
                unlocked: false,
                progress: 0,
                target: 10
            }
        };

        this.dailyMissions = {
            'daily-ai-generation': {
                id: 'daily-ai-generation',
                name: 'Gerador Diário',
                description: 'Gere 3 tabuleiros hoje',
                icon: 'fas fa-magic',
                points: 50,
                category: 'ai-generation',
                progress: 0,
                target: 3,
                completed: false,
                expiresAt: null
            },
            'daily-ai-play': {
                id: 'daily-ai-play',
                name: 'Jogador Diário',
                description: 'Jogue 2 tabuleiros gerados por IA',
                icon: 'fas fa-chess',
                points: 40,
                category: 'ai-generation',
                progress: 0,
                target: 2,
                completed: false,
                expiresAt: null
            },
            'daily-ai-analysis': {
                id: 'daily-ai-analysis',
                name: 'Analisador Diário',
                description: 'Analise 2 tabuleiros com IA',
                icon: 'fas fa-search',
                points: 45,
                category: 'ai-generation',
                progress: 0,
                target: 2,
                completed: false,
                expiresAt: null
            }
        };

        this.stats = {
            totalGenerated: 0,
            totalFavorites: 0,
            totalPlayed: 0,
            totalAnalyzed: 0,
            totalBatches: 0,
            themeStats: {
                creative: 0,
                tactical: 0,
                strategic: 0,
                artistic: 0
            },
            dailyStats: {
                generated: 0,
                played: 0,
                analyzed: 0
            }
        };

        this.init();
    }

    init() {
        this.loadStats();
        this.loadAchievements();
        this.loadDailyMissions();
        this.setupEventListeners();
        this.updateUI();
    }

    setupEventListeners() {
        // Integrar com eventos do gerador de tabuleiros
        if (window.aiBoardGenerator) {
            // Escutar eventos de geração
            this.listenToAIGenerator();
        }
    }

    listenToAIGenerator() {
        // Sobrescrever métodos para adicionar gamificação
        const originalGenerateNewBoard = window.aiBoardGenerator.generateNewBoard.bind(window.aiBoardGenerator);
        const originalPlayBoard = window.aiBoardGenerator.playBoard.bind(window.aiBoardGenerator);
        const originalAnalyzeBoard = window.aiBoardGenerator.analyzeBoard.bind(window.aiBoardGenerator);
        const originalSaveBoard = window.aiBoardGenerator.saveBoard.bind(window.aiBoardGenerator);
        const originalGenerateBatchBoards = window.aiBoardGenerator.generateBatchBoards.bind(window.aiBoardGenerator);

        // Geração de tabuleiro único
        window.aiBoardGenerator.generateNewBoard = async function() {
            const result = await originalGenerateNewBoard();
            if (result) {
                window.aiGamification.onBoardGenerated(result);
            }
            return result;
        };

        // Jogar tabuleiro
        window.aiBoardGenerator.playBoard = function(boardId) {
            const result = originalPlayBoard(boardId);
            if (result) {
                window.aiGamification.onBoardPlayed(boardId);
            }
            return result;
        };

        // Analisar tabuleiro
        window.aiBoardGenerator.analyzeBoard = function(boardId) {
            const result = originalAnalyzeBoard(boardId);
            if (result) {
                window.aiGamification.onBoardAnalyzed(boardId);
            }
            return result;
        };

        // Salvar tabuleiro
        window.aiBoardGenerator.saveBoard = function(boardId) {
            const result = originalSaveBoard(boardId);
            if (result) {
                window.aiGamification.onBoardSaved(boardId);
            }
            return result;
        };

        // Geração em lote
        window.aiBoardGenerator.generateBatchBoards = async function() {
            const result = await originalGenerateBatchBoards();
            if (result) {
                window.aiGamification.onBatchGenerated(result);
            }
            return result;
        };
    }

    onBoardGenerated(board) {
        // Atualizar estatísticas
        this.stats.totalGenerated++;
        this.stats.themeStats[board.theme]++;
        this.stats.dailyStats.generated++;

        // Verificar conquistas
        this.checkAchievements('generation', board);

        // Atualizar missões diárias
        this.updateDailyMissions('generation');

        // Salvar e atualizar UI
        this.saveStats();
        this.updateUI();

        // Mostrar notificação de conquista se aplicável
        this.showAchievementNotification();
    }

    onBoardPlayed(boardId) {
        this.stats.totalPlayed++;
        this.stats.dailyStats.played++;

        this.checkAchievements('play', {
            id: boardId
        });
        this.updateDailyMissions('play');
        this.saveStats();
        this.updateUI();
    }

    onBoardAnalyzed(boardId) {
        this.stats.totalAnalyzed++;
        this.stats.dailyStats.analyzed++;

        this.checkAchievements('analysis', {
            id: boardId
        });
        this.updateDailyMissions('analysis');
        this.saveStats();
        this.updateUI();
    }

    onBoardSaved(boardId) {
        this.stats.totalFavorites++;

        this.checkAchievements('favorite', {
            id: boardId
        });
        this.saveStats();
        this.updateUI();
    }

    onBatchGenerated(boards) {
        this.stats.totalBatches++;

        this.checkAchievements('batch', {
            count: boards.length
        });
        this.saveStats();
        this.updateUI();
    }

    checkAchievements(action, data) {
        const achievementsToCheck = Object.values(this.achievements).filter(a => !a.unlocked);

        achievementsToCheck.forEach(achievement => {
            let shouldUnlock = false;

            switch (achievement.id) {
                case 'first-ai-board':
                    shouldUnlock = this.stats.totalGenerated >= 1;
                    break;
                case 'ai-master':
                    achievement.progress = this.stats.totalGenerated;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'creative-genius':
                    achievement.progress = this.stats.themeStats.creative;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'tactical-expert':
                    achievement.progress = this.stats.themeStats.tactical;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'strategic-mind':
                    achievement.progress = this.stats.themeStats.strategic;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'artistic-soul':
                    achievement.progress = this.stats.themeStats.artistic;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'ai-collector':
                    achievement.progress = this.stats.totalFavorites;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'ai-player':
                    achievement.progress = this.stats.totalPlayed;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'ai-analyzer':
                    achievement.progress = this.stats.totalAnalyzed;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
                case 'ai-batch-master':
                    achievement.progress = this.stats.totalBatches;
                    shouldUnlock = achievement.progress >= achievement.target;
                    break;
            }

            if (shouldUnlock) {
                this.unlockAchievement(achievement);
            }
        });
    }

    unlockAchievement(achievement) {
        achievement.unlocked = true;
        achievement.unlockedAt = new Date().toISOString();

        // Adicionar pontos ao usuário
        this.addPoints(achievement.points);

        // Salvar conquista
        this.saveAchievements();

        // Mostrar notificação
        this.showAchievementUnlocked(achievement);

        // Atualizar UI
        this.updateUI();
    }

    updateDailyMissions(action) {
        const today = new Date().toDateString();

        Object.values(this.dailyMissions).forEach(mission => {
            if (mission.completed) return;

            // Verificar se a missão expirou
            if (mission.expiresAt && new Date(mission.expiresAt) < new Date()) {
                this.resetDailyMission(mission);
                return;
            }

            // Atualizar progresso baseado na ação
            switch (action) {
                case 'generation':
                    if (mission.id === 'daily-ai-generation') {
                        mission.progress++;
                    }
                    break;
                case 'play':
                    if (mission.id === 'daily-ai-play') {
                        mission.progress++;
                    }
                    break;
                case 'analysis':
                    if (mission.id === 'daily-ai-analysis') {
                        mission.progress++;
                    }
                    break;
            }

            // Verificar se a missão foi completada
            if (mission.progress >= mission.target) {
                this.completeDailyMission(mission);
            }
        });

        this.saveDailyMissions();
        this.updateUI();
    }

    completeDailyMission(mission) {
        mission.completed = true;
        mission.completedAt = new Date().toISOString();

        // Adicionar pontos
        this.addPoints(mission.points);

        // Salvar
        this.saveDailyMissions();

        // Mostrar notificação
        this.showMissionCompleted(mission);

        // Atualizar UI
        this.updateUI();
    }

    resetDailyMission(mission) {
        mission.progress = 0;
        mission.completed = false;
        mission.completedAt = null;
        mission.expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24 horas
    }

    addPoints(points) {
        // Integrar com sistema de gamificação existente
        if (window.gamification && window.gamification.addPoints) {
            window.gamification.addPoints(points);
        }
    }

    showAchievementUnlocked(achievement) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-gradient-to-r from-yellow-500 to-orange-600 text-white px-6 py-4 rounded-xl shadow-2xl z-50 transform transition-all duration-500 translate-x-full';
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                    <i class="${achievement.icon} text-2xl"></i>
                </div>
                <div>
                    <h4 class="font-bold text-lg">Conquista Desbloqueada!</h4>
                    <p class="text-sm opacity-90">${achievement.name}</p>
                    <p class="text-xs opacity-75">+${achievement.points} pontos</p>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // Animar entrada
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // Remover após 5 segundos
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 5000);
    }

    showMissionCompleted(mission) {
        const notification = document.createElement('div');
        notification.className = 'fixed top-20 right-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-xl shadow-2xl z-50 transform transition-all duration-500 translate-x-full';
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="${mission.icon} text-xl"></i>
                <div>
                    <p class="font-semibold">Missão Completa!</p>
                    <p class="text-sm opacity-90">+${mission.points} pontos</p>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // Animar entrada
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // Remover após 3 segundos
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }

    updateUI() {
        // Atualizar estatísticas na interface
        this.updateStatsDisplay();

        // Atualizar conquistas na interface
        this.updateAchievementsDisplay();

        // Atualizar missões diárias na interface
        this.updateDailyMissionsDisplay();
    }

    updateStatsDisplay() {
        const elements = {
            'total-generated': this.stats.totalGenerated,
            'total-favorites': this.stats.totalFavorites,
            'total-played': this.stats.totalPlayed,
            'avg-rating': this.calculateAverageRating()
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    updateAchievementsDisplay() {
        // Atualizar conquistas na interface de gamificação
        if (window.gamification && window.gamification.updateAchievements) {
            const aiAchievements = Object.values(this.achievements).filter(a => a.unlocked);
            window.gamification.updateAchievements(aiAchievements);
        }
    }

    updateDailyMissionsDisplay() {
        // Atualizar missões diárias na interface de gamificação
        if (window.gamification && window.gamification.updateDailyMissions) {
            const aiMissions = Object.values(this.dailyMissions);
            window.gamification.updateDailyMissions(aiMissions);
        }
    }

    calculateAverageRating() {
        // Implementar cálculo de rating médio se necessário
        return '4.2';
    }

    // Métodos de persistência
    saveStats() {
        localStorage.setItem('aiGamificationStats', JSON.stringify(this.stats));
    }

    loadStats() {
        const saved = localStorage.getItem('aiGamificationStats');
        if (saved) {
            this.stats = {
                ...this.stats,
                ...JSON.parse(saved)
            };
        }
    }

    saveAchievements() {
        localStorage.setItem('aiGamificationAchievements', JSON.stringify(this.achievements));
    }

    loadAchievements() {
        const saved = localStorage.getItem('aiGamificationAchievements');
        if (saved) {
            this.achievements = {
                ...this.achievements,
                ...JSON.parse(saved)
            };
        }
    }

    saveDailyMissions() {
        localStorage.setItem('aiGamificationDailyMissions', JSON.stringify(this.dailyMissions));
    }

    loadDailyMissions() {
        const saved = localStorage.getItem('aiGamificationDailyMissions');
        if (saved) {
            this.dailyMissions = {
                ...this.dailyMissions,
                ...JSON.parse(saved)
            };
        } else {
            // Inicializar missões diárias com expiração
            Object.values(this.dailyMissions).forEach(mission => {
                mission.expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
            });
        }
    }

    // Métodos públicos para integração
    getStats() {
        return this.stats;
    }

    getAchievements() {
        return Object.values(this.achievements);
    }

    getDailyMissions() {
        return Object.values(this.dailyMissions);
    }

    resetDailyProgress() {
        Object.values(this.dailyMissions).forEach(mission => {
            this.resetDailyMission(mission);
        });
        this.stats.dailyStats = {
            generated: 0,
            played: 0,
            analyzed: 0
        };
        this.saveDailyMissions();
        this.saveStats();
        this.updateUI();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
            window.aiGamification = new AIGamificationIntegration();