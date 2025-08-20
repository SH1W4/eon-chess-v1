/**
 * 🎓 Unified AI Teacher System - AEON CHESS
 * Sistema unificado de IA que ensina, interage e analisa o estilo do jogador
 * Substitui múltiplos botões laterais por uma interface inteligente única
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class UnifiedAITeacherSystem {
    constructor() {
        this.isActive = false;
        this.currentContext = null;
        this.userProfile = {
            gamesPlayed: 0,
            algebraicData: [],
            playStyle: null,
            weaknesses: [],
            strengths: [],
            preferredOpenings: [],
            learningGoals: []
        };

        this.conversationFlow = {
            intro: 'introduction',
            teaching: 'history_lesson',
            analyzing: 'style_analysis',
            suggesting: 'improvement_suggestions',
            training: 'personalized_training'
        };

        this.currentFlow = 'intro';
        this.messageHistory = [];

        this.init();
    }

    async init() {
        console.log('🎓 Inicializando Sistema Unificado de IA Professor...');

        try {
            await this.waitForDOM();
            this.replaceOldButtons();
            this.createAITeacherInterface();
            this.setupEventListeners();
            this.loadUserProfile();

            console.log('✅ Sistema de IA Professor inicializado!');

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
        await new Promise(resolve => setTimeout(resolve, 200));
    }

    replaceOldButtons() {
        console.log('🔄 Substituindo botões antigos pelo sistema unificado...');

        // Encontrar e remover botões laterais repetitivos
        const redundantButtons = document.querySelectorAll(`
            #ai-fab:not(.main-ai-button),
            .btn-secondary[onclick*="showDemo"],
            .btn-secondary[onclick*="analyze"],
            .btn-primary[onclick*="generate"]
        `);

        redundantButtons.forEach(button => {
            if (button.id !== 'ai-fab') { // Manter o FAB principal
                button.remove();
                console.log('🗑️ Botão redundante removido:', button);
            }
        });

        // Identificar o FAB principal e marcá-lo
        const mainFab = document.getElementById('ai-fab');
        if (mainFab) {
            mainFab.classList.add('main-ai-button');
            console.log('✅ FAB principal identificado e preservado');
        }
    }

    createAITeacherInterface() {
        // Interface será criada dinamicamente quando necessário
        this.addAITeacherStyles();

        // Integrar com sistema de batalhas históricas
        this.setupBattleIntegration();
    }

    addAITeacherStyles() {
        if (document.getElementById('ai-teacher-styles')) return;

        const style = document.createElement('style');
        style.id = 'ai-teacher-styles';
        style.textContent = `
            .ai-teacher-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
                backdrop-filter: blur(20px);
            }

            .ai-teacher-modal.active {
                opacity: 1;
                visibility: visible;
            }

            .ai-teacher-container {
                background: linear-gradient(145deg, #1a202c 0%, #2d3748 100%);
                border-radius: 20px;
                max-width: 800px;
                width: 90%;
                max-height: 90vh;
                overflow: hidden;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                transform: scale(0.9);
                transition: transform 0.3s ease;
            }

            .ai-teacher-modal.active .ai-teacher-container {
                transform: scale(1);
            }

            .ai-teacher-header {
                background: linear-gradient(135deg, var(--accent, #3b82f6), var(--complement, #2563eb));
                padding: 20px;
                text-align: center;
                position: relative;
            }

            .ai-teacher-avatar {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                margin: 0 auto 12px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }

            .ai-teacher-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: white;
                margin: 0 0 8px 0;
            }

            .ai-teacher-subtitle {
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.9);
                margin: 0;
            }

            .ai-teacher-close {
                position: absolute;
                top: 15px;
                right: 15px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.2s ease;
            }

            .ai-teacher-close:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: scale(1.1);
            }

            .ai-teacher-content {
                padding: 0;
                height: 400px;
                display: flex;
                flex-direction: column;
            }

            .ai-conversation {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: rgba(0, 0, 0, 0.2);
            }

            .ai-message {
                margin-bottom: 16px;
                padding: 12px 16px;
                border-radius: 12px;
                animation: messageSlideIn 0.3s ease-out;
            }

            .ai-message.ai {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2));
                border-left: 4px solid var(--accent, #3b82f6);
                color: #e2e8f0;
            }

            .ai-message.user {
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.2));
                border-left: 4px solid #10b981;
                color: #e2e8f0;
                margin-left: 40px;
            }

            .ai-message-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 8px;
                font-size: 0.875rem;
                opacity: 0.8;
            }

            .ai-message-content {
                line-height: 1.6;
            }

            .ai-input-area {
                padding: 20px;
                background: rgba(0, 0, 0, 0.3);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }

            .ai-quick-actions {
                display: flex;
                gap: 8px;
                margin-bottom: 12px;
                flex-wrap: wrap;
            }

            .ai-quick-btn {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #e2e8f0;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 0.875rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .ai-quick-btn:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: translateY(-1px);
            }

            .ai-input-container {
                display: flex;
                gap: 12px;
                align-items: flex-end;
            }

            .ai-input {
                flex: 1;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 12px 16px;
                color: white;
                font-size: 1rem;
                resize: none;
                min-height: 48px;
                max-height: 120px;
            }

            .ai-input:focus {
                outline: none;
                border-color: var(--accent, #3b82f6);
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
            }

            .ai-send-btn {
                background: linear-gradient(135deg, var(--accent, #3b82f6), var(--complement, #2563eb));
                border: none;
                color: white;
                width: 48px;
                height: 48px;
                border-radius: 12px;
                cursor: pointer;
                font-size: 1.2rem;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .ai-send-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            }

            .ai-send-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            @keyframes messageSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 768px) {
                .ai-teacher-container {
                    width: 95%;
                    max-height: 95vh;
                }
                
                .ai-teacher-content {
                    height: 350px;
                }
                
                .ai-quick-actions {
                    flex-direction: column;
                }
                
                .ai-quick-btn {
                    text-align: center;
                }
            }
        `;

        document.head.appendChild(style);
    }

    setupBattleIntegration() {
        // Aguardar sistema de batalhas carregar
        const checkBattleSystem = () => {
            if (window.historicalBattlesUI) {
                this.integrateBattleSystem();
            } else {
                setTimeout(checkBattleSystem, 500);
            }
        };
        checkBattleSystem();
    }

    integrateBattleSystem() {
        // Interceptar cliques nos botões de IA Professor das batalhas
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-ai-teacher')) {
                e.preventDefault();
                const battleKey = e.target.closest('.btn-ai-teacher').dataset.battle;
                this.openAITeacher(battleKey);
            }
        });

        console.log('🔗 Integração com sistema de batalhas ativa');
    }

    setupEventListeners() {
        // Event listeners serão adicionados dinamicamente
    }

    openAITeacher(battleContext = null) {
        this.currentContext = battleContext;

        // Obter dados da batalha se fornecido contexto
        let battleData = null;
        if (battleContext && window.historicalBattlesUI) {
            battleData = window.historicalBattlesUI.getBattleData(battleContext);
        }

        this.createModal(battleData);
        this.startConversation(battleData);
    }

    createModal(battleData = null) {
        // Remover modal existente se houver
        const existingModal = document.getElementById('ai-teacher-modal');
        if (existingModal) {
            existingModal.remove();
        }

        const modal = document.createElement('div');
        modal.id = 'ai-teacher-modal';
        modal.className = 'ai-teacher-modal';

        const avatar = battleData ? battleData.symbolism.icon : '🎓';
        const title = battleData ? `Professor ${battleData.name}` : 'AEON Chess Professor';
        const subtitle = battleData ?
            `Especialista em ${battleData.era} • ${battleData.year}` :
            'Seu mentor pessoal de xadrez';

        modal.innerHTML = `
            <div class="ai-teacher-container">
                <div class="ai-teacher-header">
                    <div class="ai-teacher-avatar">${avatar}</div>
                    <h3 class="ai-teacher-title">${title}</h3>
                    <p class="ai-teacher-subtitle">${subtitle}</p>
                    <button class="ai-teacher-close" onclick="this.closest('.ai-teacher-modal').remove()">×</button>
                </div>
                
                <div class="ai-teacher-content">
                    <div class="ai-conversation" id="ai-conversation">
                        <!-- Mensagens aparecerão aqui -->
                    </div>
                    
                    <div class="ai-input-area">
                        <div class="ai-quick-actions" id="ai-quick-actions">
                            <button class="ai-quick-btn" data-action="history">📚 Ensine história</button>
                            <button class="ai-quick-btn" data-action="analyze">🔍 Analise meu estilo</button>
                            <button class="ai-quick-btn" data-action="improve">💡 Como melhorar?</button>
                            <button class="ai-quick-btn" data-action="openings">🌟 Melhores aberturas</button>
                        </div>
                        
                        <div class="ai-input-container">
                            <textarea 
                                class="ai-input" 
                                id="ai-input"
                                placeholder="Digite sua pergunta ou carregue dados algébricos de suas partidas..."
                                rows="2"></textarea>
                            <button class="ai-send-btn" id="ai-send-btn">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Aplicar cores da batalha se disponível
        if (battleData) {
            this.applyBattleTheme(modal, battleData);
        }

        // Ativar modal
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);

        // Setup event listeners para este modal
        this.setupModalEventListeners(modal);
    }

    applyBattleTheme(modal, battleData) {
        const header = modal.querySelector('.ai-teacher-header');
        const sendBtn = modal.querySelector('.ai-send-btn');

        if (header) {
            header.style.background = `linear-gradient(135deg, ${battleData.colors.accent}, ${battleData.colors.complement})`;
        }

        if (sendBtn) {
            sendBtn.style.background = `linear-gradient(135deg, ${battleData.colors.accent}, ${battleData.colors.complement})`;
        }

        // Aplicar cores CSS customizadas
        modal.style.setProperty('--accent', battleData.colors.accent);
        modal.style.setProperty('--complement', battleData.colors.complement);
    }

    setupModalEventListeners(modal) {
        const input = modal.querySelector('#ai-input');
        const sendBtn = modal.querySelector('#ai-send-btn');
        const quickBtns = modal.querySelectorAll('.ai-quick-btn');

        // Enviar mensagem
        const sendMessage = () => {
            const message = input.value.trim();
            if (message) {
                this.processUserMessage(message);
                input.value = '';
                input.style.height = 'auto';
            }
        };

        sendBtn.addEventListener('click', sendMessage);

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 120) + 'px';
        });

        // Botões rápidos
        quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }

    startConversation(battleData = null) {
        const conversation = document.getElementById('ai-conversation');
        if (!conversation) return;

        let welcomeMessage = '';

        if (battleData) {
            welcomeMessage = `
                Olá! Sou seu professor especializado em <strong>${battleData.name}</strong> 
                (${battleData.year}). Esta batalha representa a era <strong>${battleData.era}</strong> 
                e é famosa por: <em>${battleData.significance}</em>.
                
                <br><br>Posso te ensinar sobre:
                <br>📚 A história fascinante desta partida
                <br>🎯 As estratégias usadas pelos mestres
                <br>🔍 Como analisar seu próprio estilo de jogo
                <br>💡 Sugestões personalizadas para melhorar
                
                <br><br>O que gostaria de explorar primeiro?
            `;
        } else {
            welcomeMessage = `
                Olá! Sou o AEON Chess Professor, sua IA pessoal de xadrez! 🎓
                
                <br><br>Posso ajudá-lo com:
                <br>📚 História do xadrez e partidas famosas
                <br>🔍 Análise do seu estilo de jogo
                <br>💡 Sugestões personalizadas de melhoria
                <br>🎯 Treinamento adaptativo baseado em seus dados
                
                <br><br>Você pode me enviar dados algébricos de suas partidas 
                (formato PGN) para uma análise personalizada do seu estilo!
                
                <br><br>Como posso ajudá-lo hoje?
            `;
        }

        this.addMessage('ai', welcomeMessage, 'Professor AEON');
    }

    addMessage(type, content, sender = null) {
        const conversation = document.getElementById('ai-conversation');
        if (!conversation) return;

        const message = document.createElement('div');
        message.className = `ai-message ${type}`;

        const timestamp = new Date().toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit'
        });

        const icon = type === 'ai' ? '🤖' : '👤';
        const name = sender || (type === 'ai' ? 'Professor AEON' : 'Você');

        message.innerHTML = `
            <div class="ai-message-header">
                <span>${icon}</span>
                <span>${name}</span>
                <span style="margin-left: auto; opacity: 0.6;">${timestamp}</span>
            </div>
            <div class="ai-message-content">${content}</div>
        `;

        conversation.appendChild(message);
        conversation.scrollTop = conversation.scrollHeight;

        // Salvar no histórico
        this.messageHistory.push({
            type,
            content,
            sender,
            timestamp: new Date()
        });
    }

    processUserMessage(message) {
        // Adicionar mensagem do usuário
        this.addMessage('user', message);

        // Simular processamento
        setTimeout(() => {
            this.generateAIResponse(message);
        }, 500);
    }

    generateAIResponse(userMessage) {
        const lowerMessage = userMessage.toLowerCase();
        let response = '';

        // Detectar dados algébricos (formato PGN)
        if (this.isPGNData(userMessage)) {
            response = this.analyzeAlgebraicData(userMessage);
        }
        // Detectar perguntas sobre história
        else if (lowerMessage.includes('história') || lowerMessage.includes('historic')) {
            response = this.generateHistoryResponse();
        }
        // Detectar pedidos de análise
        else if (lowerMessage.includes('analise') || lowerMessage.includes('estilo') || lowerMessage.includes('style')) {
            response = this.generateStyleAnalysisResponse();
        }
        // Detectar pedidos de melhoria
        else if (lowerMessage.includes('melhor') || lowerMessage.includes('improve') || lowerMessage.includes('dica')) {
            response = this.generateImprovementResponse();
        }
        // Detectar perguntas sobre aberturas
        else if (lowerMessage.includes('abertura') || lowerMessage.includes('opening')) {
            response = this.generateOpeningResponse();
        }
        // Resposta geral inteligente
        else {
            response = this.generateContextualResponse(userMessage);
        }

        this.addMessage('ai', response);
    }

    handleQuickAction(action) {
        const actions = {
            'history': () => this.processUserMessage('Me ensine sobre a história desta partida'),
            'analyze': () => this.processUserMessage('Analise meu estilo de jogo'),
            'improve': () => this.processUserMessage('Como posso melhorar meu jogo?'),
            'openings': () => this.processUserMessage('Quais são as melhores aberturas para mim?')
        };

        if (actions[action]) {
            actions[action]();
        }
    }

    isPGNData(message) {
        // Detectar formato PGN simples
        return message.includes('1.') && (message.includes('e4') || message.includes('d4') || message.includes('Nf3'));
    }

    analyzeAlgebraicData(pgnData) {
        // Análise básica de dados PGN
        this.userProfile.algebraicData.push(pgnData);
        this.userProfile.gamesPlayed++;

        // Análise simples
        const moves = pgnData.match(/\d+\.\s*[a-zA-Z0-9#+\-=]+/g) || [];
        const gameLength = moves.length;

        let analysis = `
            📊 <strong>Análise da Partida Recebida:</strong>
            <br><br>🎮 <strong>Movimentos analisados:</strong> ${gameLength}
            <br>📈 <strong>Total de jogos no perfil:</strong> ${this.userProfile.gamesPlayed}
        `;

        // Detectar estilo baseado em movimentos
        if (pgnData.includes('O-O') || pgnData.includes('O-O-O')) {
            analysis += `<br>🏰 <strong>Roque detectado:</strong> Boa segurança do rei!`;
        }

        if (pgnData.includes('x')) {
            const captures = (pgnData.match(/x/g) || []).length;
            analysis += `<br>⚔️ <strong>Capturas:</strong> ${captures} (estilo ${captures > 5 ? 'agressivo' : 'posicional'})`;
        }

        analysis += `
            <br><br>💡 <strong>Próximos passos:</strong>
            <br>• Continue enviando partidas para análise mais profunda
            <br>• Vou identificar padrões em suas aberturas favoritas
            <br>• Posso sugerir melhorias específicas baseadas em seus dados
            
            <br><br>🎯 <strong>Dica personalizada:</strong> Com mais dados, poderei 
            identificar seus pontos fortes e criar um plano de treinamento específico para você!
        `;

        return analysis;
    }

    generateHistoryResponse() {
        if (this.currentContext && window.historicalBattlesUI) {
            const battle = window.historicalBattlesUI.getBattleData(this.currentContext);
            return `
                📚 <strong>História de ${battle.name} (${battle.year})</strong>
                
                <br><br>🌍 <strong>Contexto:</strong> ${battle.location}
                <br>🎭 <strong>Era:</strong> ${battle.era}
                <br>⭐ <strong>Significado:</strong> ${battle.significance}
                
                <br><br>👥 <strong>Protagonistas:</strong>
                <br>${battle.players.white.flag} <strong>${battle.players.white.name}</strong> (${battle.players.white.country})
                <br>${battle.players.black.flag} <strong>${battle.players.black.name}</strong> (${battle.players.black.country})
                
                <br><br>🎨 <strong>Atmosfera da época:</strong> ${battle.symbolism.atmosphere}
                
                <br><br>Esta partida é um marco na história do xadrez e representa 
                perfeitamente os valores e estilo de jogo da era ${battle.era}.
                
                <br><br>Gostaria que eu explique alguma jogada específica ou 
                conte mais sobre as estratégias utilizadas?
            `;
        }

        return `
            📚 <strong>História do Xadrez Fascinante!</strong>
            
            <br><br>O xadrez tem mais de 1500 anos de história, evoluindo desde o 
            <strong>Chaturanga</strong> indiano até o jogo moderno que conhecemos.
            
            <br><br>🏛️ <strong>Eras Principais:</strong>
            <br>• <strong>Romântica (1850-1900):</strong> Sacrifícios brilhantes
            <br>• <strong>Clássica (1900-1945):</strong> Fundamentos posicionais  
            <br>• <strong>Moderna (1945-1990):</strong> Teoria profunda
            <br>• <strong>Digital (1990+):</strong> Era dos computadores
            
            <br><br>Cada era trouxe inovações únicas. Qual período mais te interessa?
        `;
    }

    generateStyleAnalysisResponse() {
        const games = this.userProfile.gamesPlayed;

        if (games === 0) {
            return `
                🔍 <strong>Análise de Estilo Personalizada</strong>
                
                <br><br>Para analisar seu estilo, preciso de dados de suas partidas! 
                
                <br><br>📝 <strong>Como enviar:</strong>
                <br>• Cole aqui movimentos em notação algébrica (1.e4 e5 2.Nf3...)
                <br>• Ou dados PGN de sites como Chess.com ou Lichess
                <br>• Quanto mais partidas, melhor a análise!
                
                <br><br>🎯 <strong>O que eu analiso:</strong>
                <br>• Preferências de abertura
                <br>• Estilo posicional vs tático
                <br>• Padrões de erro comuns
                <br>• Tempo de jogo ideal
                <br>• Sugestões de melhoria específicas
                
                <br><br>Envie uma partida para começarmos!
            `;
        }

        return `
            🔍 <strong>Análise do Seu Estilo (${games} jogos analisados)</strong>
            
            <br><br>📊 <strong>Perfil atual:</strong>
            <br>• <strong>Estilo:</strong> ${this.userProfile.playStyle || 'Em análise...'}
            <br>• <strong>Jogos analisados:</strong> ${games}
            
            <br><br>💪 <strong>Pontos fortes identificados:</strong>
            <br>• Boa aplicação de fundamentos básicos
            <br>• Crescente conhecimento posicional
            
            <br><br>📈 <strong>Áreas de melhoria:</strong>
            <br>• Continue enviando partidas para análise mais profunda
            <br>• Foque em aberturas consistentes
            
            <br><br>Envie mais partidas para uma análise ainda mais detalhada!
        `;
    }

    generateImprovementResponse() {
        return `
            💡 <strong>Plano Personalizado de Melhoria</strong>
            
            <br><br>🎯 <strong>Recomendações baseadas em IA:</strong>
            
            <br><br>📚 <strong>1. Estude partidas históricas</strong>
            <br>• Analise as batalhas disponíveis no sistema
            <br>• Entenda os padrões de cada era
            <br>• Absorva a sabedoria dos mestres
            
            <br><br>🔄 <strong>2. Treinamento adaptativo</strong>
            <br>• Envie suas partidas para análise
            <br>• Receba feedback específico
            <br>• Pratique pontos fracos identificados
            
            <br><br>🎮 <strong>3. Jogue consistentemente</strong>
            <br>• 15-30 minutos diários
            <br>• Foque em uma abertura por vez
            <br>• Analise cada partida após jogar
            
            <br><br>📈 <strong>4. Desenvolva visão tática</strong>
            <br>• Resolva puzzles diariamente
            <br>• Pratique padrões de mate
            <br>• Treine cálculo de variantes
            
            <br><br>Qual área gostaria de focar primeiro?
        `;
    }

    generateOpeningResponse() {
        return `
            🌟 <strong>Guia de Aberturas Inteligente</strong>
            
            <br><br>🎯 <strong>Baseado no seu nível, recomendo:</strong>
            
            <br><br>⚪ <strong>Com as brancas:</strong>
            <br>• <strong>1.e4</strong> - Abertura do Rei (princípios claros)
            <br>• <strong>1.d4</strong> - Abertura da Dama (controle posicional)
            <br>• <strong>1.Nf3</strong> - Sistema Réti (flexível)
            
            <br><br>⚫ <strong>Com as pretas:</strong>
            <br>• Contra 1.e4: <strong>Siciliana</strong> ou <strong>Francesa</strong>
            <br>• Contra 1.d4: <strong>Índia do Rei</strong> ou <strong>Nimzo-Índia</strong>
            
            <br><br>💡 <strong>Dica personalizada:</strong>
            <br>Escolha UMA abertura para cada cor e domine completamente 
            antes de expandir seu repertório.
            
            <br><br>📊 <strong>Para recomendações específicas:</strong>
            <br>Envie suas partidas e identificarei quais aberturas 
            combinam melhor com seu estilo natural!
            
            <br><br>Qual abertura gostaria de estudar primeiro?
        `;
    }

    generateContextualResponse(message) {
        const responses = [
            `Interessante pergunta! Com base no contexto da nossa conversa, acredito que você está buscando melhorar seu jogo. Que tal começarmos analisando uma partida histórica para entender os padrões dos mestres?`,

            `Vejo que está curioso sobre xadrez! Posso te ajudar de várias formas. O que mais te interessa no momento: história, análise de jogadas, ou desenvolvimento de habilidades específicas?`,

            `Ótima questão! Para te dar a melhor resposta possível, gostaria de entender melhor seu nível atual. Já joga há quanto tempo? Tem alguma área específica que gostaria de melhorar?`,

            `Entendo sua curiosidade! O xadrez é realmente fascinante. Se me enviar algumas de suas partidas (em notação algébrica), posso fazer uma análise personalizada e dar sugestões mais específicas para seu estilo.`
        ];

        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        return `${randomResponse}<br><br>🤔 <strong>Sua mensagem:</strong> "${message}"<br><br>Como posso ajudar mais especificamente?`;
    }

    loadUserProfile() {
        // Carregar perfil do localStorage se existir
        const saved = localStorage.getItem('aeon_chess_user_profile');
        if (saved) {
            try {
                this.userProfile = {
                    ...this.userProfile,
                    ...JSON.parse(saved)
                };
                console.log('📊 Perfil do usuário carregado:', this.userProfile);
            } catch (error) {
                console.warn('⚠️ Erro ao carregar perfil do usuário:', error);
            }
        }
    }

    saveUserProfile() {
        localStorage.setItem('aeon_chess_user_profile', JSON.stringify(this.userProfile));
        console.log('💾 Perfil do usuário salvo');
    }

    // Métodos públicos para integração
    getConversationHistory() {
        return this.messageHistory;
    }

    getUserProfile() {
        return this.userProfile;
    }

    isModalOpen() {
        const modal = document.getElementById('ai-teacher-modal');
        return modal && modal.classList.contains('active');
    }
}

// ===============================
// 🚀 INICIALIZAÇÃO AUTOMÁTICA
// ===============================

// Criar instância global
window.aiTeacher = new UnifiedAITeacherSystem();

// Expor métodos para console
console.log(`
🎓 Sistema Unificado de IA Professor carregado!

Comandos disponíveis:
• aiTeacher.openAITeacher() - Abrir professor geral
• aiTeacher.openAITeacher('fischer-spassky') - Professor específico
• aiTeacher.getUserProfile() - Ver perfil do usuário
• aiTeacher.getConversationHistory() - Ver histórico de conversas

O sistema substitui os botões laterais repetitivos por uma interface 
inteligente que pode ensinar história e analisar seu estilo de jogo!
`);