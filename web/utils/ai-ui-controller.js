// AEON CHESS - Controlador de UI para Sistema de IA Generativa
// Versão: 2.0 - Interface Avançada e Interativa

class AIUIController {
    constructor() {
        this.currentTheme = 'creative';
        this.currentDifficulty = 'auto';
        this.currentCreativity = 70;
        this.currentCulturalContext = 'aztec';
        this.isGenerating = false;
        this.notifications = [];

        // Inicializar controlador de geração
        this.generationController = new GenerationController();

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeUI();
        this.updateProviderStatus();
        this.setupFloatingActionButton();
        this.setupNotificationSystem();
    }

    setupEventListeners() {
        // Theme selector
        const themeSelect = document.getElementById('ai-theme');
        if (themeSelect) {
            themeSelect.addEventListener('change', (e) => {
                this.currentTheme = e.target.value;
                this.updateThemeInfo();
                this.updateUI();
            });
        }

        // Difficulty selector
        const difficultySelect = document.getElementById('ai-difficulty');
        if (difficultySelect) {
            difficultySelect.addEventListener('change', (e) => {
                this.currentDifficulty = e.target.value;
                this.updateUI();
            });
        }

        // Creativity slider
        const creativitySlider = document.getElementById('ai-creativity');
        if (creativitySlider) {
            creativitySlider.addEventListener('input', (e) => {
                this.currentCreativity = e.target.value;
                this.updateCreativityDisplay();
            });
        }

        // Cultural Narrative status updater
        this.updateCulturalNarrativeStatus();

        // Cultural context selector
        const culturalSelect = document.getElementById('cultural-context');
        if (culturalSelect) {
            culturalSelect.addEventListener('change', (e) => {
                this.currentCulturalContext = e.target.value;
                this.updateCulturalContext();
                this.updateUI();
            });
        }

        // System evaluation button
        const evaluationBtn = document.getElementById('system-evaluation-btn');
        if (evaluationBtn) {
            evaluationBtn.addEventListener('click', () => {
                this.runSystemEvaluation();
            });
        }

        // Generation buttons
        const generateBtn = document.getElementById('generate-board');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.startGeneration('single');
            });
        }

        const batchBtn = document.getElementById('batch-generate');
        if (batchBtn) {
            batchBtn.addEventListener('click', () => {
                this.startGeneration('batch');
            });
        }

        const smartBtn = document.getElementById('smart-generate');
        if (smartBtn) {
            smartBtn.addEventListener('click', () => {
                this.startGeneration('smart');
            });
        }

        // Quick action buttons
        this.setupQuickActionButtons();
    }

    setupQuickActionButtons() {
        const exportBtn = document.getElementById('export-data');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportData());
        }

        const resetBtn = document.getElementById('reset-models');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetModels());
        }

        const trainBtn = document.getElementById('train-models');
        if (trainBtn) {
            trainBtn.addEventListener('click', () => this.trainModels());
        }

        const refreshBtn = document.getElementById('refresh-gallery');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshGallery());
        }
    }

    initializeUI() {
        this.updateThemeInfo();
        this.updateCreativityDisplay();
        this.updateStats();
        this.updateMLPerformance();
        this.updateProviderStatus();
    }

    updateThemeInfo() {
        const themeInfo = document.getElementById('theme-info');
        if (!themeInfo) return;

        const themes = {
            'creative': {
                name: '🎨 Criativo',
                description: 'Posições únicas e inovadoras que desafiam convenções',
                complexity: 'Média',
                creativity: 'Alta',
                bestFor: 'Jogadores que buscam experiências únicas',
                examples: ['Desenvolvimento acelerado', 'Estruturas não convencionais', 'Padrões criativos']
            },
            'tactical': {
                name: '⚡ Tático',
                description: 'Combinações forçadas e sacrifícios calculados',
                complexity: 'Alta',
                creativity: 'Média',
                bestFor: 'Treinar cálculo e combinações',
                examples: ['Sacrifícios de qualidade', 'Combinações forçadas', 'Táticas de mate']
            },
            'strategic': {
                name: '🧠 Estratégico',
                description: 'Planos de longo prazo e estruturas posicionais',
                complexity: 'Média',
                creativity: 'Média',
                bestFor: 'Desenvolver pensamento estratégico',
                examples: ['Controle de colunas', 'Estrutura de peões', 'Planejamento de longo prazo']
            },
            'artistic': {
                name: '✨ Artístico',
                description: 'Padrões visuais únicos e simetrias impressionantes',
                complexity: 'Baixa',
                creativity: 'Muito Alta',
                bestFor: 'Apreciar a beleza do xadrez',
                examples: ['Simetrias perfeitas', 'Padrões visuais', 'Configurações artísticas']
            }
        };

        const theme = themes[this.currentTheme];
        if (!theme) return;

        themeInfo.innerHTML = `
            <div class="bg-gradient-to-br from-[#1a1a1a] to-[#0f0f0f] border border-[#2a2a2a] rounded-xl p-6">
                <div class="flex items-start space-x-4">
                    <div class="flex-shrink-0">
                        <div class="w-16 h-16 bg-gradient-to-br from-green-500/20 to-emerald-600/20 rounded-xl flex items-center justify-center">
                            <span class="text-3xl">${theme.name.split(' ')[0]}</span>
                        </div>
                    </div>
                    <div class="flex-1">
                        <h4 class="text-xl font-bold text-white mb-2">${theme.name}</h4>
                        <p class="text-gray-300 text-sm mb-4">${theme.description}</p>
                        
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <span class="text-xs text-gray-400">Complexidade:</span>
                                <div class="text-sm font-medium text-white">${theme.complexity}</div>
                            </div>
                            <div>
                                <span class="text-xs text-gray-400">Criatividade:</span>
                                <div class="text-sm font-medium text-white">${theme.creativity}</div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <span class="text-xs text-gray-400">Ideal para:</span>
                            <div class="text-sm text-white">${theme.bestFor}</div>
                        </div>
                        
                        <div>
                            <span class="text-xs text-gray-400">Exemplos:</span>
                            <div class="flex flex-wrap gap-2 mt-1">
                                ${theme.examples.map(ex => 
                                    `<span class="px-2 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs">${ex}</span>`
                                ).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    updateCreativityDisplay() {
        const creativityValue = document.getElementById('ai-creativity');
        if (creativityValue) {
            // Atualizar valor do slider se necessário
            creativityValue.value = this.currentCreativity;
        }
    }

    updateCulturalNarrativeStatus() {
        const statusContainer = document.getElementById('cultural-narrative-status');
        if (!statusContainer) return;

        // Status do Sistema Cultural e Narrativo
        const culturalStatus = {
            system: {
                name: 'AEON Brain Cultural',
                icon: '🌍',
                status: 'online',
                features: ['10 Culturas', 'Narrativas Emergentes', 'Gamificação Cultural']
            },
            current: {
                name: 'Contexto Atual',
                icon: this.getCulturalIcon(this.currentCulturalContext),
                status: 'active',
                features: [this.getCulturalName(this.currentCulturalContext), 'Narrativa Contextual', 'IA Adaptativa']
            },
            progress: {
                name: 'Progresso Cultural',
                icon: '📚',
                status: 'tracking',
                features: ['XP Cultural', 'Níveis', 'Histórico Narrativo']
            },
            integration: {
                name: 'Integração IA',
                icon: '🤖',
                status: 'connected',
                features: ['AEON Brain', 'Seleção Inteligente', 'Contexto Cultural']
            }
        };

        const statusHTML = Object.values(culturalStatus).map(component => `
            <div class="flex items-center justify-between p-3 bg-[#0f0f0f] rounded-lg border border-[#2a2a2a]">
                <div class="flex items-center space-x-3">
                    <span class="text-lg">${component.icon}</span>
                    <div>
                        <div class="text-sm font-medium text-white">${component.name}</div>
                        <div class="text-xs text-gray-400">Sistema Cultural</div>
                        <div class="flex flex-wrap gap-1 mt-1">
                            ${component.features.map(feature => 
                                `<span class="px-1.5 py-0.5 bg-green-500/20 text-green-300 rounded text-xs">${feature}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
                <div class="ai-status ${component.status}">
                    <i class="fas fa-circle mr-2"></i>
                    ${this.getStatusText(component.status)}
                </div>
            </div>
        `).join('');

        statusContainer.innerHTML = statusHTML;
    }

    getCulturalIcon(cultureId) {
        const icons = {
            'aztec': '🏛️',
            'nordic': '⚔️',
            'egyptian': '👑',
            'japanese': '🗡️',
            'celtic': '🌿',
            'neo-tokyo-2050': '🌃',
            'mars-colony': '🚀',
            'quantum-realm': '⚛️',
            'steampunk-victoria': '⚙️',
            'digital-nomad': '💻'
        };
        return icons[cultureId] || '🌍';
    }

    getCulturalName(cultureId) {
        const names = {
            'aztec': 'Civilização Asteca',
            'nordic': 'Mitologia Nórdica',
            'egyptian': 'Antigo Egito',
            'japanese': 'Japão Feudal',
            'celtic': 'Mitologia Celta',
            'neo-tokyo-2050': 'Neo Tokyo 2050',
            'mars-colony': 'Colônia Marciana',
            'quantum-realm': 'Reino Quântico',
            'steampunk-victoria': 'Victoria Steampunk',
            'digital-nomad': 'Nômades Digitais'
        };
        return names[cultureId] || 'Cultura';
    }

    /**
     * Executar avaliação completa do sistema
     */
    async runSystemEvaluation() {
        try {
            // Mostrar loading
            const evaluationBtn = document.getElementById('system-evaluation-btn');
            const originalText = evaluationBtn.innerHTML;
            evaluationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Avaliando...</span>';
            evaluationBtn.disabled = true;

            // Executar avaliação
            const evaluator = new AEONBrainEvaluator();
            const report = await evaluator.evaluateCompleteSystem();

            // Exibir resultados
            this.displayEvaluationResults(report);

            // Restaurar botão
            evaluationBtn.innerHTML = originalText;
            evaluationBtn.disabled = false;

        } catch (error) {
            console.error('Erro na avaliação:', error);
            this.showNotification('Erro na avaliação do sistema', 'error');

            // Restaurar botão
            const evaluationBtn = document.getElementById('system-evaluation-btn');
            evaluationBtn.innerHTML = '<i class="fas fa-clipboard-check"></i><span>Avaliar Sistema</span>';
            evaluationBtn.disabled = false;
        }
    }

    /**
     * Exibir resultados da avaliação
     */
    displayEvaluationResults(report) {
        // Mostrar seção de resultados
        const resultsSection = document.getElementById('system-evaluation-results');
        resultsSection.classList.remove('hidden');

        // Atualizar grade e score
        const gradeElement = document.getElementById('evaluation-grade');
        const scoreElement = document.getElementById('evaluation-score');
        gradeElement.textContent = report.summary.grade;
        scoreElement.textContent = `Score: ${report.summary.overallScore}`;

        // Atualizar resumo
        this.updateEvaluationSummary(report.summary);

        // Atualizar scores detalhados
        this.updateDetailedScores(report.detailedScores);

        // Atualizar recomendações
        this.updateRecommendations(report.recommendations);

        // Atualizar próximos passos
        this.updateNextSteps(report.nextSteps);

        // Scroll para resultados
        resultsSection.scrollIntoView({
            behavior: 'smooth'
        });

        // Mostrar notificação de sucesso
        this.showNotification('Avaliação do sistema concluída com sucesso!', 'success');
    }

    /**
     * Atualizar resumo da avaliação
     */
    updateEvaluationSummary(summary) {
        const summaryContainer = document.getElementById('evaluation-summary');

        const summaryHTML = `
            <div class="bg-gradient-to-r from-green-500/20 to-blue-500/20 border border-green-500/30 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                    <h5 class="text-lg font-semibold text-white">Status: ${summary.status}</h5>
                    <span class="text-sm text-gray-400">${summary.overallScore}</span>
                </div>
                <div class="space-y-2">
                    <div class="text-sm text-gray-300">
                        <strong>Destaques:</strong>
                        <ul class="list-disc list-inside mt-1 space-y-1">
                            ${summary.highlights.map(highlight => `<li>${highlight}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="text-sm text-gray-300">
                        <strong>Áreas para Melhoria:</strong>
                        <ul class="list-disc list-inside mt-1 space-y-1">
                            ${summary.areasForImprovement.map(area => `<li>${area}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;

        summaryContainer.innerHTML = summaryHTML;
    }

    /**
     * Atualizar scores detalhados
     */
    updateDetailedScores(scores) {
        // Arquitetura
        const architectureContainer = document.getElementById('evaluation-architecture');
        architectureContainer.innerHTML = this.createScoreCard('🏗️ Arquitetura', scores.architecture, 'blue');

        // IA
        const aiContainer = document.getElementById('evaluation-ai');
        aiContainer.innerHTML = this.createScoreCard('🤖 Sistema de IA', scores.ai, 'green');

        // Cultural
        const culturalContainer = document.getElementById('evaluation-cultural');
        culturalContainer.innerHTML = this.createScoreCard('🌍 Sistema Cultural', scores.cultural, 'purple');

        // Adicionar mais sistemas se necessário
        const container = document.querySelector('#evaluation-architecture').parentElement;

        // Gamificação
        if (scores.gamification) {
            const gamificationContainer = document.createElement('div');
            gamificationContainer.id = 'evaluation-gamification';
            gamificationContainer.className = 'bg-[#0f0f0f] rounded-lg p-4 border border-[#2a2a2a]';
            gamificationContainer.innerHTML = this.createScoreCard('🎮 Gamificação', scores.gamification, 'orange');
            container.appendChild(gamificationContainer);
        }

        // Interface
        if (scores.interface) {
            const interfaceContainer = document.createElement('div');
            interfaceContainer.id = 'evaluation-interface';
            interfaceContainer.className = 'bg-[#0f0f0f] rounded-lg p-4 border border-[#2a2a2a]';
            interfaceContainer.innerHTML = this.createScoreCard('🎨 Interface', scores.interface, 'pink');
            container.appendChild(interfaceContainer);
        }

        // Integração
        if (scores.integration) {
            const integrationContainer = document.createElement('div');
            integrationContainer.id = 'evaluation-integration';
            integrationContainer.className = 'bg-[#0f0f0f] rounded-lg p-4 border border-[#2a2a2a]';
            integrationContainer.innerHTML = this.createScoreCard('🔗 Integração', scores.integration, 'cyan');
            container.appendChild(integrationContainer);
        }
    }

    /**
     * Criar card de score
     */
    createScoreCard(title, scores, color) {
        const colorClasses = {
            blue: 'from-blue-500/20 to-blue-600/20 border-blue-500/30 text-blue-400',
            green: 'from-green-500/20 to-green-600/20 border-green-500/30 text-green-400',
            purple: 'from-purple-500/20 to-purple-600/20 border-purple-500/30 text-purple-400',
            orange: 'from-orange-500/20 to-orange-600/20 border-orange-500/30 text-orange-400',
            pink: 'from-pink-500/20 to-pink-600/20 border-pink-500/30 text-pink-400',
            cyan: 'from-cyan-500/20 to-cyan-600/20 border-cyan-500/30 text-cyan-400'
        };

        const colorClass = colorClasses[color];

        // Determinar quais métricas mostrar baseado no tipo de score
        let metrics = [];
        if (scores.modularity !== undefined) {
            // Arquitetura
            metrics = [{
                    label: 'Modularidade',
                    value: scores.modularity
                },
                {
                    label: 'Escalabilidade',
                    value: scores.scalability
                },
                {
                    label: 'Manutenibilidade',
                    value: scores.maintainability
                },
                {
                    label: 'Extensibilidade',
                    value: scores.extensibility
                }
            ];
        } else if (scores.integration !== undefined) {
            // IA
            metrics = [{
                    label: 'Integração',
                    value: scores.integration
                },
                {
                    label: 'Provedores',
                    value: scores.providers
                },
                {
                    label: 'Orquestração',
                    value: scores.orchestration
                },
                {
                    label: 'Aprendizado',
                    value: scores.learning
                }
            ];
        } else if (scores.diversity !== undefined) {
            // Cultural
            metrics = [{
                    label: 'Diversidade',
                    value: scores.diversity
                },
                {
                    label: 'Narrativas',
                    value: scores.narratives
                },
                {
                    label: 'Gamificação',
                    value: scores.gamification
                },
                {
                    label: 'Integração',
                    value: scores.integration
                }
            ];
        } else if (scores.mechanics !== undefined) {
            // Gamificação
            metrics = [{
                    label: 'Mecânicas',
                    value: scores.mechanics
                },
                {
                    label: 'Progressão',
                    value: scores.progression
                },
                {
                    label: 'Recompensas',
                    value: scores.rewards
                },
                {
                    label: 'Engajamento',
                    value: scores.engagement
                }
            ];
        } else if (scores.design !== undefined) {
            // Interface
            metrics = [{
                    label: 'Design',
                    value: scores.design
                },
                {
                    label: 'Responsividade',
                    value: scores.responsiveness
                },
                {
                    label: 'Acessibilidade',
                    value: scores.accessibility
                },
                {
                    label: 'UX',
                    value: scores.userExperience
                }
            ];
        } else if (scores.connectivity !== undefined) {
            // Integração
            metrics = [{
                    label: 'Conectividade',
                    value: scores.connectivity
                },
                {
                    label: 'Performance',
                    value: scores.performance
                },
                {
                    label: 'Confiabilidade',
                    value: scores.reliability
                },
                {
                    label: 'Monitoramento',
                    value: scores.monitoring
                }
            ];
        }

        return `
            <div class="bg-gradient-to-br ${colorClass} rounded-lg p-3 border">
                <h6 class="font-semibold text-white mb-2">${title}</h6>
                <div class="space-y-2">
                    ${metrics.map(metric => `
                        <div class="flex justify-between text-sm">
                            <span class="text-gray-300">${metric.label}:</span>
                            <span class="text-white">${(metric.value * 100).toFixed(0)}%</span>
                        </div>
                    `).join('')}
                    <div class="pt-2 border-t border-white/20">
                        <div class="flex justify-between text-sm font-semibold">
                            <span class="text-gray-300">Score Geral:</span>
                            <span class="text-white">${(scores.overall * 100).toFixed(0)}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Atualizar recomendações
     */
    updateRecommendations(recommendations) {
        const container = document.getElementById('evaluation-recommendations');

        if (recommendations.length === 0) {
            container.innerHTML = `
                <div class="bg-gradient-to-r from-green-500/20 to-green-600/20 border border-green-500/30 rounded-lg p-4">
                    <h5 class="text-lg font-semibold text-white mb-2">🎉 Excelente!</h5>
                    <p class="text-gray-300">Sistema está funcionando perfeitamente. Nenhuma recomendação crítica.</p>
                </div>
            `;
            return;
        }

        const recommendationsHTML = `
            <h5 class="text-lg font-semibold text-white mb-3">📋 Recomendações</h5>
            <div class="space-y-3">
                ${recommendations.map(rec => `
                    <div class="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-lg p-3">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm font-medium text-white">${rec.category}</span>
                            <span class="px-2 py-1 text-xs rounded-full ${
                                rec.priority === 'Alta' ? 'bg-red-500/20 text-red-300' :
                                rec.priority === 'Média' ? 'bg-yellow-500/20 text-yellow-300' :
                                'bg-blue-500/20 text-blue-300'
                            }">${rec.priority}</span>
                        </div>
                        <p class="text-sm text-gray-300 mb-2">${rec.description}</p>
                        <p class="text-xs text-gray-400"><strong>Ação:</strong> ${rec.action}</p>
                    </div>
                `).join('')}
            </div>
        `;

        container.innerHTML = recommendationsHTML;
    }

    /**
     * Atualizar próximos passos
     */
    updateNextSteps(nextSteps) {
        const container = document.getElementById('evaluation-next-steps');

        const nextStepsHTML = `
            <h5 class="text-lg font-semibold text-white mb-3">🚀 Próximos Passos</h5>
            <div class="space-y-3">
                ${nextSteps.map(step => `
                    <div class="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30 rounded-lg p-3">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm font-medium text-white">${step.action}</span>
                            <span class="px-2 py-1 text-xs rounded-full ${
                                step.priority === 'Alta' ? 'bg-red-500/20 text-red-300' :
                                step.priority === 'Média' ? 'bg-yellow-500/20 text-yellow-300' :
                                'bg-blue-500/20 text-blue-300'
                            }">${step.priority}</span>
                        </div>
                        <div class="flex items-center justify-between text-xs text-gray-400">
                            <span><strong>Timeline:</strong> ${step.timeline}</span>
                            <span><strong>Impacto:</strong> ${step.impact}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        container.innerHTML = nextStepsHTML;
    }

    getProviderDescription(providerId) {
        const descriptions = {
            'openai': 'GPT-5 - IA mais avançada do mundo',
            'anthropic': 'Claude 3.5 - Análise contextual profunda',
            'google': 'Gemini 2.0 - Multimodal e matemática',
            'groq': 'Llama 3.2 - Ultra rápido e eficiente',
            'together': 'Llama 3.2 - Open source e customizável',
            'chessai': 'Chess AI v2 - Especializado em xadrez',
            'local': 'Modelos locais treinados e privados'
        };
        return descriptions[providerId] || 'Provedor de IA';
    }

    getStatusText(status) {
        const statusTexts = {
            'online': 'Online',
            'offline': 'Offline',
            'loading': 'Conectando...'
        };
        return statusTexts[status] || 'Desconhecido';
    }

    async startGeneration(type) {
        if (this.isGenerating) {
            this.showNotification('Geração já em andamento', 'warning');
            return;
        }

        // Verificar permissão de geração
        const canGenerate = this.generationController.canGenerate(type);
        if (!canGenerate.allowed) {
            this.showNotification(canGenerate.reason, 'error');
            return;
        }

        this.isGenerating = true;
        this.showProgressBar();
        this.updateButtonStates();

        try {
            let result;
            switch (type) {
                case 'single':
                    result = await this.generateSingleBoard();
                    break;
                case 'batch':
                    result = await this.generateBatchBoards();
                    break;
                case 'smart':
                    result = await this.generateSmartBoard();
                    break;
            }

            if (result) {
                // Registrar geração bem-sucedida
                const count = type === 'batch' ? 5 : 1;
                this.generationController.recordGeneration(type, count);

                this.showNotification(`Tabuleiro${type === 'batch' ? 's' : ''} gerado${type === 'batch' ? 's' : ''} com sucesso!`, 'success');
                this.updateStats();
            }
        } catch (error) {
            console.error('Erro na geração:', error);
            this.showNotification('Erro ao gerar tabuleiro', 'error');
        } finally {
            this.isGenerating = false;
            this.hideProgressBar();
            this.updateButtonStates();
        }
    }

    async generateSingleBoard() {
        // Simular geração com progresso
        await this.simulateProgress();

        // Usar AEON Brain Cultural Narrative para geração contextualizada
        if (window.aeonBrainCultural) {
            const userId = 'user_' + Date.now(); // Simular ID de usuário
            const cultureId = this.currentCulturalContext || 'aztec';
            const narrativeId = this.selectNarrativeForTheme(this.currentTheme);

            const userProfile = {
                level: 'intermediate',
                preferences: ['creative', 'strategic'],
                culturalAffinity: cultureId
            };

            return await window.aeonBrainCultural.generateCulturalNarrativePosition(
                userId,
                cultureId,
                narrativeId,
                userProfile
            );
        }

        // Fallback para AEON Brain padrão
        if (window.aeonBrain) {
            const task = {
                type: 'chess_position_generation',
                theme: {
                    name: this.currentTheme,
                    description: this.themes[this.currentTheme] ? .description || 'Posição de xadrez',
                    complexity: this.currentDifficulty
                },
                requirements: ['high_quality', 'unique', 'valid'],
                complexity: this.currentDifficulty
            };

            const userProfile = {
                level: 'intermediate',
                preferences: ['creative', 'strategic']
            };

            const preferences = {
                urgency: 'normal',
                costSensitive: false
            };

            return await window.aeonBrain.generateChessPosition(task, userProfile, preferences);
        }

        return {
            success: true
        };
    }

    async generateBatchBoards() {
        // Simular geração em lote
        for (let i = 0; i < 5; i++) {
            await this.simulateProgress(20);
        }

        // Usar AEON Brain para geração em lote otimizada
        if (window.aeonBrain) {
            const results = [];

            for (let i = 0; i < 5; i++) {
                const task = {
                    type: 'chess_position_generation',
                    theme: {
                        name: this.currentTheme,
                        description: this.themes[this.currentTheme] ? .description || 'Posição de xadrez',
                        complexity: this.currentDifficulty
                    },
                    requirements: ['high_quality', 'unique', 'valid'],
                    complexity: this.currentDifficulty
                };

                const userProfile = {
                    level: 'intermediate',
                    preferences: ['creative', 'strategic']
                };

                const preferences = {
                    urgency: 'normal',
                    costSensitive: true // Para lote, otimizar custos
                };

                const result = await window.aeonBrain.generateChessPosition(task, userProfile, preferences);
                results.push(result);
            }

            return {
                success: true,
                count: results.length,
                results: results
            };
        }

        return {
            success: true,
            count: 5
        };
    }

    async generateSmartBoard() {
        // Simular geração inteligente
        await this.simulateProgress(30);

        // Usar AEON Brain para orquestração inteligente
        if (window.aeonBrain) {
            const task = {
                type: 'complex_strategy_analysis',
                theme: {
                    name: this.currentTheme,
                    description: this.themes[this.currentTheme] ? .description || 'Posição de xadrez',
                    complexity: 'high'
                },
                requirements: ['high_quality', 'unique', 'valid', 'strategic_depth', 'mathematical_optimization'],
                complexity: 'high'
            };

            const userProfile = {
                level: 'expert',
                preferences: ['strategic', 'mathematical', 'creative']
            };

            const preferences = {
                urgency: 'low', // Tarefas complexas podem demorar
                costSensitive: false // Qualidade é prioridade
            };

            return await window.aeonBrain.generateChessPosition(task, userProfile, preferences);
        }

        return {
            success: true,
            smart: true
        };
    }

    async simulateProgress(duration = 1000) {
        const progressBar = document.getElementById('progress-bar');
        const progressPercentage = document.getElementById('progress-percentage');

        if (!progressBar || !progressPercentage) return;

        const startTime = Date.now();
        const endTime = startTime + duration;

        return new Promise((resolve) => {
            const updateProgress = () => {
                const currentTime = Date.now();
                const elapsed = currentTime - startTime;
                const progress = Math.min((elapsed / duration) * 100, 100);

                progressBar.style.width = `${progress}%`;
                progressPercentage.textContent = `${Math.round(progress)}%`;

                if (currentTime < endTime) {
                    requestAnimationFrame(updateProgress);
                } else {
                    resolve();
                }
            };

            requestAnimationFrame(updateProgress);
        });
    }

    showProgressBar() {
        const progressContainer = document.getElementById('generation-progress');
        if (progressContainer) {
            progressContainer.classList.remove('hidden');
        }
    }

    hideProgressBar() {
        const progressContainer = document.getElementById('generation-progress');
        if (progressContainer) {
            progressContainer.classList.add('hidden');
        }
    }

    updateButtonStates() {
        const buttons = ['generate-board', 'batch-generate', 'smart-generate'];

        buttons.forEach(buttonId => {
            const button = document.getElementById(buttonId);
            if (button) {
                if (this.isGenerating) {
                    button.disabled = true;
                    button.classList.add('opacity-50', 'cursor-not-allowed');
                } else {
                    button.disabled = false;
                    button.classList.remove('opacity-50', 'cursor-not-allowed');
                }
            }
        });
    }

    updateStats() {
        // Atualizar estatísticas na interface
        const stats = {
            'total-generated': Math.floor(Math.random() * 100) + 50,
            'total-favorites': Math.floor(Math.random() * 30) + 10,
            'total-played': Math.floor(Math.random() * 80) + 20,
            'avg-rating': (Math.random() * 2 + 3).toFixed(1)
        };

        Object.entries(stats).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });

        // Atualizar barra de performance
        const performanceScore = document.getElementById('ai-performance-score');
        const performanceBar = document.getElementById('ai-performance-bar');

        if (performanceScore && performanceBar) {
            const score = Math.floor(Math.random() * 30) + 70; // 70-100%
            performanceScore.textContent = `${score}%`;
            performanceBar.style.width = `${score}%`;
        }
    }

    updateMLPerformance() {
        const metrics = ['accuracy', 'recall', 'f1score'];

        metrics.forEach(metric => {
            const bar = document.getElementById(`ml-${metric}`);
            const text = document.getElementById(`ml-${metric}-text`);

            if (bar && text) {
                const value = Math.floor(Math.random() * 40) + 60; // 60-100%
                bar.style.width = `${value}%`;
                text.textContent = `${value}%`;
            }
        });
    }

    setupFloatingActionButton() {
        const fab = document.getElementById('ai-fab');
        if (fab) {
            fab.addEventListener('click', () => {
                this.scrollToAISection();
            });
        }
    }

    scrollToAISection() {
        const aiSection = document.getElementById('ai-generation');
        if (aiSection) {
            aiSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    setupNotificationSystem() {
        // Sistema de notificações já configurado
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="fas ${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        // Mostrar notificação
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Remover após 5 segundos
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    // Métodos para ações rápidas
    async exportData() {
        try {
            // Simular exportação
            await new Promise(resolve => setTimeout(resolve, 1000));
            this.showNotification('Dados exportados com sucesso!', 'success');
        } catch (error) {
            this.showNotification('Erro ao exportar dados', 'error');
        }
    }

    async resetModels() {
        if (confirm('Tem certeza que deseja resetar os modelos? Isso apagará todo o aprendizado.')) {
            try {
                // Simular reset
                await new Promise(resolve => setTimeout(resolve, 2000));
                this.showNotification('Modelos resetados com sucesso!', 'success');
                this.updateMLPerformance();
            } catch (error) {
                this.showNotification('Erro ao resetar modelos', 'error');
            }
        }
    }

    async trainModels() {
        try {
            this.showNotification('Iniciando treinamento dos modelos...', 'info');

            // Simular treinamento
            await new Promise(resolve => setTimeout(resolve, 3000));

            this.showNotification('Modelos treinados com sucesso!', 'success');
            this.updateMLPerformance();

            // Atualizar status
            const modelStatus = document.getElementById('model-status');
            const lastTraining = document.getElementById('last-training');

            if (modelStatus) modelStatus.textContent = 'Treinando...';
            if (lastTraining) lastTraining.textContent = 'Agora';

            setTimeout(() => {
                if (modelStatus) modelStatus.textContent = 'Ativo';
            }, 1000);

        } catch (error) {
            this.showNotification('Erro ao treinar modelos', 'error');
        }
    }

    async refreshGallery() {
        try {
            const refreshBtn = document.getElementById('refresh-gallery');
            if (refreshBtn) {
                refreshBtn.classList.add('animate-spin');
            }

            // Simular atualização
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.showNotification('Galeria atualizada!', 'success');

            if (refreshBtn) {
                refreshBtn.classList.remove('animate-spin');
            }
        } catch (error) {
            this.showNotification('Erro ao atualizar galeria', 'error');
        }
    }

    updateUI() {
        // Atualizar interface baseada nas configurações atuais
        this.updateThemeInfo();
        this.updateCulturalNarrativeStatus();
        this.updateCulturalContext();

        // Atualizar classes dos botões ativos
        this.updateActiveButtonStates();
    }

    updateCulturalContext() {
        const culturalSelect = document.getElementById('cultural-context');
        if (culturalSelect && this.currentCulturalContext) {
            culturalSelect.value = this.currentCulturalContext;
        }
    }

    selectNarrativeForTheme(theme) {
        // Mapear temas para narrativas culturais
        const themeToNarrative = {
            'creative': 'pyramid_ascension', // Asteca - criatividade
            'tactical': 'valkyrie_quest', // Nórdica - combate tático
            'strategic': 'pharaoh_journey', // Egípcia - estratégia real
            'artistic': 'fae_encounter', // Celta - arte e magia
            'futuristic': 'digital_ascension', // Neo Tokyo - tecnologia
            'space': 'terraforming_mars', // Marte - exploração espacial
            'quantum': 'probability_manipulation', // Quântico - probabilidade
            'steampunk': 'industrial_revolution', // Victoria - revolução industrial
            'digital': 'global_connectivity' // Nômades - conectividade
        };

        return themeToNarrative[theme] || 'pyramid_ascension';
    }

    updateActiveButtonStates() {
        // Atualizar estado dos botões baseado na seleção atual
        const buttons = {
            'ai-theme': this.currentTheme,
            'ai-difficulty': this.currentDifficulty,
            'ai-provider': this.currentProvider
        };

        Object.entries(buttons).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.value = value;
            }
        });
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.aiUIController = new AIUIController();
});