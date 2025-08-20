// AEON CHESS - Sistema de Gamificação
// Versão: 1.0 - Sistema Completo de Progressão

class AeonGamification {
    constructor() {
        this.player = {
            id: null,
            name: '',
            level: 1,
            experience: 0,
            totalPoints: 0,
            achievements: [],
            badges: [],
            dailyStreak: 0,
            lastPlayed: null,
            missions: [],
            ranking: 0,
            stats: {
                gamesPlayed: 0,
                gamesWon: 0,
                gamesLost: 0,
                gamesDrawn: 0,
                bestMoveCount: 0,
                tacticalMoves: 0,
                blunders: 0,
                averageAccuracy: 0,
                totalPlayTime: 0
            }
        };

        this.levels = [{
                level: 1,
                name: "Novato",
                xpRequired: 0,
                badge: "🥉"
            },
            {
                level: 2,
                name: "Aprendiz",
                xpRequired: 100,
                badge: "🥉"
            },
            {
                level: 3,
                name: "Iniciante",
                xpRequired: 250,
                badge: "🥉"
            },
            {
                level: 4,
                name: "Jogador",
                xpRequired: 500,
                badge: "🥈"
            },
            {
                level: 5,
                name: "Tático",
                xpRequired: 1000,
                badge: "🥈"
            },
            {
                level: 6,
                name: "Estratégico",
                xpRequired: 2000,
                badge: "🥈"
            },
            {
                level: 7,
                name: "Mestre",
                xpRequired: 4000,
                badge: "🥇"
            },
            {
                level: 8,
                name: "Grande Mestre",
                xpRequired: 8000,
                badge: "🥇"
            },
            {
                level: 9,
                name: "Lenda",
                xpRequired: 15000,
                badge: "👑"
            },
            {
                level: 10,
                name: "Aeon Master",
                xpRequired: 30000,
                badge: "👑"
            }
        ];

        this.achievements = [{
                id: 'first_game',
                name: 'Primeira Partida',
                description: 'Jogue sua primeira partida',
                icon: '🎮',
                xpReward: 50
            },
            {
                id: 'first_win',
                name: 'Primeira Vitória',
                description: 'Ganhe sua primeira partida',
                icon: '🏆',
                xpReward: 100
            },
            {
                id: 'win_streak_3',
                name: 'Sequência de Vitórias',
                description: 'Ganhe 3 partidas seguidas',
                icon: '🔥',
                xpReward: 200
            },
            {
                id: 'win_streak_5',
                name: 'Invencível',
                description: 'Ganhe 5 partidas seguidas',
                icon: '⚡',
                xpReward: 500
            },
            {
                id: 'perfect_game',
                name: 'Jogo Perfeito',
                description: 'Jogue uma partida com 100% de precisão',
                icon: '💎',
                xpReward: 1000
            },
            {
                id: 'tactical_master',
                name: 'Mestre Tático',
                description: 'Execute 10 movimentos táticos',
                icon: '🎯',
                xpReward: 300
            },
            {
                id: 'daily_streak_7',
                name: 'Jogador Dedicado',
                description: 'Jogue 7 dias seguidos',
                icon: '📅',
                xpReward: 400
            },
            {
                id: 'daily_streak_30',
                name: 'Viciado em Xadrez',
                description: 'Jogue 30 dias seguidos',
                icon: '📆',
                xpReward: 2000
            },
            {
                id: 'level_5',
                name: 'Nível 5',
                description: 'Alcance o nível 5',
                icon: '⭐',
                xpReward: 500
            },
            {
                id: 'level_10',
                name: 'Aeon Master',
                description: 'Alcance o nível máximo',
                icon: '👑',
                xpReward: 5000
            }
        ];

        this.dailyMissions = [{
                id: 'play_3_games',
                name: 'Jogador Ativo',
                description: 'Jogue 3 partidas hoje',
                target: 3,
                reward: 100,
                type: 'games'
            },
            {
                id: 'win_2_games',
                name: 'Vencedor',
                description: 'Ganhe 2 partidas hoje',
                target: 2,
                reward: 150,
                type: 'wins'
            },
            {
                id: 'accuracy_80',
                name: 'Preciso',
                description: 'Mantenha 80% de precisão em uma partida',
                target: 80,
                reward: 200,
                type: 'accuracy'
            },
            {
                id: 'tactical_moves',
                name: 'Tático',
                description: 'Execute 5 movimentos táticos',
                target: 5,
                reward: 120,
                type: 'tactical'
            },
            {
                id: 'no_blunders',
                name: 'Sem Erros',
                description: 'Jogue uma partida sem blunders',
                target: 0,
                reward: 300,
                type: 'blunders'
            }
        ];

        this.badges = [{
                id: 'speed_demon',
                name: 'Demônio da Velocidade',
                icon: '⚡',
                description: 'Jogue 10 partidas rápidas'
            },
            {
                id: 'accuracy_king',
                name: 'Rei da Precisão',
                icon: '🎯',
                description: 'Mantenha 90%+ precisão por 5 partidas'
            },
            {
                id: 'tactical_genius',
                name: 'Gênio Tático',
                icon: '🧠',
                description: 'Execute 50 movimentos táticos'
            },
            {
                id: 'endurance',
                name: 'Resistência',
                icon: '💪',
                description: 'Jogue por 2 horas seguidas'
            },
            {
                id: 'social_butterfly',
                name: 'Borboleta Social',
                icon: '🦋',
                description: 'Jogue contra 10 jogadores diferentes'
            }
        ];

        this.init();
    }

    init() {
        this.loadPlayerData();
        this.generateDailyMissions();
        this.checkDailyStreak();
        this.updateUI();
    }

    loadPlayerData() {
        const savedData = localStorage.getItem('aeon_gamification');
        if (savedData) {
            const data = JSON.parse(savedData);
            this.player = {
                ...this.player,
                ...data
            };
        } else {
            this.player.id = 'player_' + Date.now();
            this.savePlayerData();
        }
    }

    savePlayerData() {
        localStorage.setItem('aeon_gamification', JSON.stringify(this.player));
    }

    addExperience(amount, reason = '') {
        const oldLevel = this.player.level;
        this.player.experience += amount;
        this.player.totalPoints += amount;

        // Verificar level up
        const newLevel = this.calculateLevel();
        if (newLevel > oldLevel) {
            this.levelUp(newLevel);
        }

        // Verificar conquistas
        this.checkAchievements();

        // Salvar dados
        this.savePlayerData();
        this.updateUI();

        // Mostrar notificação
        this.showNotification(`+${amount} XP`, reason);
    }

    calculateLevel() {
        for (let i = this.levels.length - 1; i >= 0; i--) {
            if (this.player.experience >= this.levels[i].xpRequired) {
                return this.levels[i].level;
            }
        }
        return 1;
    }

    levelUp(newLevel) {
        const levelData = this.levels.find(l => l.level === newLevel);
        this.player.level = newLevel;

        // Mostrar animação de level up
        this.showLevelUpAnimation(levelData);

        // Verificar conquista de nível
        this.checkLevelAchievement(newLevel);
    }

    checkLevelAchievement(newLevel) {
        // Verificar conquista de nível
        if (newLevel === 5) {
            const achievement = this.achievements.find(a => a.id === 'level_5');
            if (achievement && !this.player.achievements.includes(achievement.id)) {
                this.earnAchievement(achievement);
            }
        } else if (newLevel === 10) {
            const achievement = this.achievements.find(a => a.id === 'level_10');
            if (achievement && !this.player.achievements.includes(achievement.id)) {
                this.earnAchievement(achievement);
            }
        }
    }

    showLevelUpAnimation(levelData) {
        const modal = document.createElement('div');
        modal.className = 'level-up-modal';
        modal.innerHTML = `
            <div class="level-up-content">
                <div class="level-up-icon">${levelData.badge}</div>
                <h2>Nível ${levelData.level}!</h2>
                <h3>${levelData.name}</h3>
                <div class="level-up-rewards">
                    <div class="reward">+100 XP</div>
                    <div class="reward">+1 Badge</div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()">Continuar</button>
            </div>
        `;
        document.body.appendChild(modal);

        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (modal.parentElement) {
                modal.remove();
            }
        }, 5000);
    }

    checkAchievements() {
        this.achievements.forEach(achievement => {
            if (!this.player.achievements.includes(achievement.id)) {
                if (this.hasEarnedAchievement(achievement)) {
                    this.earnAchievement(achievement);
                }
            }
        });
    }

    hasEarnedAchievement(achievement) {
        switch (achievement.id) {
            case 'first_game':
                return this.player.stats.gamesPlayed >= 1;
            case 'first_win':
                return this.player.stats.gamesWon >= 1;
            case 'win_streak_3':
                return this.getCurrentWinStreak() >= 3;
            case 'win_streak_5':
                return this.getCurrentWinStreak() >= 5;
            case 'perfect_game':
                return this.player.stats.averageAccuracy >= 100;
            case 'tactical_master':
                return this.player.stats.tacticalMoves >= 10;
            case 'daily_streak_7':
                return this.player.dailyStreak >= 7;
            case 'daily_streak_30':
                return this.player.dailyStreak >= 30;
            case 'level_5':
                return this.player.level >= 5;
            case 'level_10':
                return this.player.level >= 10;
            default:
                return false;
        }
    }

    earnAchievement(achievement) {
        this.player.achievements.push(achievement.id);
        this.addExperience(achievement.xpReward, `Conquista: ${achievement.name}`);
        this.showAchievementNotification(achievement);
    }

    showAchievementNotification(achievement) {
        const notification = document.createElement('div');
        notification.className = 'achievement-notification';
        notification.innerHTML = `
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-info">
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
                <span class="xp-reward">+${achievement.xpReward} XP</span>
            </div>
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    generateDailyMissions() {
        if (!this.player.missions.length || this.isNewDay()) {
            this.player.missions = this.dailyMissions
                .sort(() => Math.random() - 0.5)
                .slice(0, 3)
                .map(mission => ({
                    ...mission,
                    progress: 0,
                    completed: false,
                    claimed: false
                }));
        }
    }

    isNewDay() {
        const lastPlayed = new Date(this.player.lastPlayed);
        const today = new Date();
        return lastPlayed.getDate() !== today.getDate() ||
            lastPlayed.getMonth() !== today.getMonth() ||
            lastPlayed.getFullYear() !== today.getFullYear();
    }

    checkDailyStreak() {
        if (this.isNewDay()) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            const lastPlayed = new Date(this.player.lastPlayed);

            if (lastPlayed.getDate() === yesterday.getDate()) {
                this.player.dailyStreak++;
            } else {
                this.player.dailyStreak = 0;
            }
        }
    }

    updateMissionProgress(type, amount = 1) {
        this.player.missions.forEach(mission => {
            if (mission.type === type && !mission.completed) {
                mission.progress += amount;
                if (mission.progress >= mission.target) {
                    mission.completed = true;
                    this.completeMission(mission);
                }
            }
        });
    }

    completeMission(mission) {
        this.addExperience(mission.reward, `Missão: ${mission.name}`);
        this.showMissionNotification(mission);
    }

    showMissionNotification(mission) {
        const notification = document.createElement('div');
        notification.className = 'mission-notification';
        notification.innerHTML = `
            <div class="mission-icon">🎯</div>
            <div class="mission-info">
                <h4>Missão Completa!</h4>
                <p>${mission.name}</p>
                <span class="xp-reward">+${mission.reward} XP</span>
            </div>
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    getCurrentWinStreak() {
        // Implementação simplificada - em produção seria mais complexa
        return Math.min(this.player.stats.gamesWon, 5);
    }

    showNotification(message, reason = '') {
        const notification = document.createElement('div');
        notification.className = 'xp-notification';
        notification.innerHTML = `
            <div class="xp-amount">${message}</div>
            ${reason ? `<div class="xp-reason">${reason}</div>` : ''}
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    updateUI() {
        this.updateProgressBar();
        this.updateStats();
        this.updateMissions();
        this.updateAchievements();
    }

    updateProgressBar() {
        const progressBar = document.getElementById('gamification-progress');
        if (!progressBar) return;

        const currentLevel = this.levels.find(l => l.level === this.player.level);
        const nextLevel = this.levels.find(l => l.level === this.player.level + 1);

        if (nextLevel) {
            const progress = ((this.player.experience - currentLevel.xpRequired) /
                (nextLevel.xpRequired - currentLevel.xpRequired)) * 100;

            progressBar.innerHTML = `
                <div class="flex items-center justify-between mb-6">
                    <div class="flex items-center space-x-4">
                        <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-full flex items-center justify-center text-2xl font-bold text-white shadow-lg">
                            ${currentLevel.badge}
                        </div>
                        <div>
                            <h4 class="text-2xl font-bold text-white">Nível ${this.player.level}</h4>
                            <p class="text-gray-400">${currentLevel.name}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-3xl font-bold text-yellow-500">${this.player.experience}</div>
                        <div class="text-sm text-gray-400">XP Total</div>
                    </div>
                </div>
                
                <div class="mb-4">
                    <div class="flex justify-between text-sm text-gray-400 mb-2">
                        <span>Progresso para o próximo nível</span>
                        <span>${Math.round(progress)}%</span>
                    </div>
                    <div class="gaming-progress">
                        <div class="gaming-progress-fill" style="width: ${progress}%"></div>
                    </div>
                </div>
                
                <div class="flex justify-between text-sm">
                    <span class="text-gray-400">Nível ${this.player.level}: ${currentLevel.xpRequired} XP</span>
                    <span class="text-blue-400">Nível ${nextLevel.level}: ${nextLevel.xpRequired} XP</span>
                </div>
            `;
        }
    }

    updateStats() {
        const statsContainer = document.getElementById('gamification-stats');
        if (!statsContainer) return;

        const winRate = this.player.stats.gamesPlayed > 0 ?
            (this.player.stats.gamesWon / this.player.stats.gamesPlayed * 100).toFixed(1) : 0;

        statsContainer.innerHTML = `
            <div class="stats-card gaming-glow">
                <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="fas fa-chess-board text-white text-xl"></i>
                </div>
                <div class="text-2xl font-bold text-blue-400 mb-1">${this.player.stats.gamesPlayed}</div>
                <div class="text-sm text-gray-400">Partidas</div>
            </div>
            <div class="stats-card gaming-glow">
                <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="fas fa-trophy text-white text-xl"></i>
                </div>
                <div class="text-2xl font-bold text-green-400 mb-1">${winRate}%</div>
                <div class="text-sm text-gray-400">Vitórias</div>
            </div>
            <div class="stats-card gaming-glow">
                <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="fas fa-fire text-white text-xl"></i>
                </div>
                <div class="text-2xl font-bold text-orange-400 mb-1">${this.player.dailyStreak}</div>
                <div class="text-sm text-gray-400">Dias Seguidos</div>
            </div>
            <div class="stats-card gaming-glow">
                <div class="w-12 h-12 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <i class="fas fa-medal text-white text-xl"></i>
                </div>
                <div class="text-2xl font-bold text-yellow-400 mb-1">${this.player.achievements.length}</div>
                <div class="text-sm text-gray-400">Conquistas</div>
            </div>
        `;

        // Update additional stats
        const currentStreak = document.getElementById('current-streak');
        if (currentStreak) {
            currentStreak.textContent = this.player.dailyStreak;
        }

        const dailyGoalProgress = document.getElementById('daily-goal-progress');
        if (dailyGoalProgress) {
            const gamesToday = this.player.missions.find(m => m.id === 'play_3_games') ? .progress || 0;
            dailyGoalProgress.textContent = `${gamesToday}/3`;
        }
    }

    updateMissions() {
        const missionsContainer = document.getElementById('gamification-missions');
        if (!missionsContainer) return;

        missionsContainer.innerHTML = this.player.missions.map(mission => `
            <div class="mission-item-gaming ${mission.completed ? 'completed' : ''}">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center">
                            <i class="fas fa-target text-white text-sm"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold text-white">${mission.name}</h4>
                            <p class="text-sm text-gray-400">${mission.description}</p>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="text-lg font-bold text-purple-400">+${mission.reward}</div>
                        <div class="text-xs text-gray-500">XP</div>
                    </div>
                </div>
                <div class="relative">
                    <div class="flex justify-between text-xs text-gray-400 mb-1">
                        <span>Progresso</span>
                        <span>${mission.progress}/${mission.target}</span>
                    </div>
                    <div class="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                        <div class="bg-gradient-to-r from-purple-500 to-blue-600 h-2 rounded-full transition-all duration-300" 
                             style="width: ${(mission.progress / mission.target) * 100}%"></div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    updateAchievements() {
        const achievementsContainer = document.getElementById('gamification-achievements');
        if (!achievementsContainer) return;

        const recentAchievements = this.player.achievements.slice(-5);
        achievementsContainer.innerHTML = recentAchievements.map(achievementId => {
            const achievement = this.achievements.find(a => a.id === achievementId);
            return `
                <div class="achievement-item-gaming">
                    <div class="achievement-icon-gaming">
                        ${achievement.icon}
                    </div>
                    <div class="flex-1">
                        <h4 class="font-semibold text-white mb-1">${achievement.name}</h4>
                        <p class="text-sm text-gray-400 mb-2">${achievement.description}</p>
                        <div class="flex items-center space-x-2">
                            <span class="text-xs text-yellow-500 font-medium">+${achievement.xpReward} XP</span>
                            <span class="text-xs text-green-500">✓ Desbloqueado</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Update next achievement info
        const nextAchievement = this.achievements.find(a => !this.player.achievements.includes(a.id));
        if (nextAchievement) {
            const nextAchievementName = document.getElementById('next-achievement-name');
            const nextAchievementDesc = document.getElementById('next-achievement-desc');
            const nextAchievementProgress = document.getElementById('next-achievement-progress');

            if (nextAchievementName) nextAchievementName.textContent = nextAchievement.name;
            if (nextAchievementDesc) nextAchievementDesc.textContent = nextAchievement.description;

            // Calculate progress for next achievement
            let progress = 0;
            switch (nextAchievement.id) {
                case 'first_game':
                    progress = this.player.stats.gamesPlayed > 0 ? 100 : 0;
                    break;
                case 'first_win':
                    progress = this.player.stats.gamesWon > 0 ? 100 : 0;
                    break;
                case 'win_streak_3':
                    progress = Math.min((this.getCurrentWinStreak() / 3) * 100, 100);
                    break;
                case 'tactical_master':
                    progress = Math.min((this.player.stats.tacticalMoves / 10) * 100, 100);
                    break;
                default:
                    progress = 0;
            }

            if (nextAchievementProgress) {
                nextAchievementProgress.style.width = `${progress}%`;
            }
        }
    }

    // Métodos para integração com o jogo
    onGameStart() {
        this.updateMissionProgress('games');
    }

    onGameEnd(result, accuracy, tacticalMoves, blunders) {
        this.player.stats.gamesPlayed++;

        if (result === 'win') {
            this.player.stats.gamesWon++;
            this.addExperience(100, 'Vitória');
        } else if (result === 'loss') {
            this.player.stats.gamesLost++;
            this.addExperience(25, 'Participação');
        } else {
            this.player.stats.gamesDrawn++;
            this.addExperience(50, 'Empate');
        }

        if (accuracy >= 80) {
            this.updateMissionProgress('accuracy', accuracy);
        }

        if (tacticalMoves > 0) {
            this.player.stats.tacticalMoves += tacticalMoves;
            this.updateMissionProgress('tactical', tacticalMoves);
        }

        if (blunders === 0) {
            this.updateMissionProgress('blunders', 0);
        }

        this.player.stats.averageAccuracy =
            (this.player.stats.averageAccuracy * (this.player.stats.gamesPlayed - 1) + accuracy) /
            this.player.stats.gamesPlayed;

        this.player.lastPlayed = new Date().toISOString();
        this.savePlayerData();
    }
}

// Inicializar gamificação
document.addEventListener('DOMContentLoaded', function() {
    window.aeonGamification = new AeonGamification();
});