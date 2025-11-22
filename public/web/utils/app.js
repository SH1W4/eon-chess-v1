// AEON CHESS - Sistema Principal com Alpine.js e Stockfish
// Versão: 3.0 - Interface Avançada + IA Forte

class AeonChessApp {
    constructor() {
        this.currentUser = null;
        this.isLoggedIn = false;
        this.game = null;
        this.board = null;
        this.engine = null;
        this.engineReady = false;
        this.engineBusy = false;
        this.playerAnalysis = {
            moves: [],
            totalMoves: 0,
            accurateMovesCount: 0,
            tacticalMovesCount: 0,
            blundersCount: 0,
            averageThinkingTime: 0,
            openingKnowledge: 0,
            endgameSkill: 0,
            estimatedElo: 1200,
            playStyle: 'balanced',
            weaknesses: [],
            strengths: [],
            sessionStart: null
        };
        this.init();
    }

    init() {
        this.checkAuthStatus();
        this.setupEventListeners();
        this.initChessBoard();
        this.initStockfish();
        this.setupNavigation();
    }

    checkAuthStatus() {
        const token = localStorage.getItem('aeon_chess_token');
        const userData = localStorage.getItem('aeon_chess_user');

        if (token && userData) {
            try {
                this.currentUser = JSON.parse(userData);
                this.isLoggedIn = true;
                this.showAuthenticatedUI();
            } catch (e) {
                this.logout();
            }
        } else {
            this.showLoginModal();
        }
    }

    showLoginModal() {
        const modal = document.createElement('div');
        modal.className = 'login-modal';
        modal.innerHTML = `
            <div class="login-form">
                <h2>🎯 AEON CHESS PRO</h2>
                <p style="text-align: center; margin-bottom: 20px; color: #666;">
                    Faça login para acessar sua análise personalizada com Stockfish
                </p>
                <form id="loginForm">
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Senha</label>
                        <input type="password" id="password" required>
                    </div>
                    <button type="submit" class="btn-primary">Entrar</button>
                </form>
                <div style="text-align: center; margin-top: 20px;">
                    <a href="#" id="demoMode" class="nav-link">🎮 Modo Demonstração</a>
                </div>
                <div id="loginMessage"></div>
                
                <!-- Credenciais de Teste -->
                <div style="margin-top: 20px; padding: 15px; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.3);">
                    <h4 style="margin: 0 0 10px 0; color: #3b82f6; font-size: 14px; font-weight: 600;">
                        <i class="fas fa-info-circle mr-1"></i>
                        Credenciais de Teste
                    </h4>
                    <div style="font-size: 12px; color: #666; line-height: 1.4;">
                        <div><strong>Admin:</strong> admin@aeonchess.com / admin123</div>
                        <div><strong>Jogador:</strong> jogador@teste.com / 123456</div>
                        <div><strong>Demo:</strong> demo@aeonchess.com / demo123</div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Event listeners
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('demoMode').addEventListener('click', (e) => {
            e.preventDefault();
            this.enterDemoMode();
        });
    }

    handleLogin() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const messageDiv = document.getElementById('loginMessage');

        // Validação básica
        if (!email || !password) {
            messageDiv.innerHTML = '<div class="message error">❌ Preencha todos os campos</div>';
            return;
        }

        // Validação de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            messageDiv.innerHTML = '<div class="message error">❌ Email inválido</div>';
            return;
        }

        // Validação de senha
        if (password.length < 6) {
            messageDiv.innerHTML = '<div class="message error">❌ Senha deve ter pelo menos 6 caracteres</div>';
            return;
        }

        messageDiv.innerHTML = '<div class="message">🔄 Autenticando...</div>';

        // Simular autenticação com delay
        setTimeout(() => {
            // Em produção, aqui seria uma chamada para API
            const users = [{
                    email: 'admin@aeonchess.com',
                    password: 'admin123',
                    name: 'Administrador',
                    level: 'master',
                    elo: 2200
                },
                {
                    email: 'jogador@teste.com',
                    password: '123456',
                    name: 'Jogador Teste',
                    level: 'intermediate',
                    elo: 1500
                },
                {
                    email: 'demo@aeonchess.com',
                    password: 'demo123',
                    name: 'Usuário Demo',
                    level: 'beginner',
                    elo: 1200
                }
            ];

            const user = users.find(u => u.email === email && u.password === password);

            if (user) {
                this.currentUser = {
                    id: 'user_' + Date.now(),
                    email: user.email,
                    name: user.name,
                    level: user.level,
                    elo: user.elo,
                    joinDate: new Date().toISOString(),
                    isPremium: user.level === 'master'
                };

                localStorage.setItem('aeon_chess_token', 'token_' + Date.now());
                localStorage.setItem('aeon_chess_user', JSON.stringify(this.currentUser));

                this.isLoggedIn = true;
                this.hideLoginModal();
                this.showAuthenticatedUI();
                this.startPlayerAnalysis();

                messageDiv.innerHTML = '<div class="message success">✅ Login realizado com sucesso!</div>';

                // Mostrar mensagem de boas-vindas
                setTimeout(() => {
                    this.showMessage(`Bem-vindo, ${user.name}! ELO atual: ${user.elo}`);
                }, 500);
            } else {
                messageDiv.innerHTML = '<div class="message error">❌ Email ou senha incorretos</div>';
            }
        }, 1500);
    }

    enterDemoMode() {
        this.currentUser = {
            id: 'demo_guest',
            name: 'Jogador Demo',
            level: 'demo',
            elo: 1200
        };
        this.isLoggedIn = true;
        this.hideLoginModal();
        this.showAuthenticatedUI();
        this.startPlayerAnalysis();
    }

    hideLoginModal() {
        const modal = document.querySelector('.login-modal');
        if (modal) {
            modal.remove();
        }
    }

    showAuthenticatedUI() {
        const header = document.querySelector('header');
        if (header) {
            const userInfo = document.createElement('div');
            userInfo.className = 'flex items-center space-x-4';
            userInfo.innerHTML = `
                <div class="text-sm text-gray-300">
                    Olá, ${this.currentUser.name}
                </div>
                <button id="logoutBtn" class="text-gray-400 hover:text-white">
                    Sair
                </button>
            `;
            header.querySelector('.flex').appendChild(userInfo);

            document.getElementById('logoutBtn').addEventListener('click', () => {
                this.logout();
            });
        }

        const authSections = document.querySelectorAll('[data-auth="true"]');
        authSections.forEach(section => {
            section.style.display = 'block';
        });
    }

    logout() {
        localStorage.removeItem('aeon_chess_token');
        localStorage.removeItem('aeon_chess_user');
        this.currentUser = null;
        this.isLoggedIn = false;
        location.reload();
    }

    initChessBoard() {
        if (typeof Chess === 'undefined') {
            console.warn('Chess.js não carregado');
            return;
        }

        this.game = new Chess();

        const board = document.getElementById('aeon-board');
        if (!board) {
            console.warn('Tabuleiro não encontrado');
            return;
        }

        this.setupBoardEvents();
        this.updateBoard();
    }

    initStockfish() {
        try {
            if (typeof Stockfish === 'undefined') {
                console.warn('Stockfish não disponível');
                return;
            }

            this.engine = Stockfish();
            this.engine.onmessage = (e) => {
                const line = (typeof e === 'string') ? e : (e && e.data);
                if (!line) return;

                if (/uciok/.test(line)) {
                    this.engineReady = true;
                    console.log('Stockfish pronto');
                }

                if (/bestmove\s(\w{4,5})/.test(line)) {
                    this.engineBusy = false;
                    const m = /bestmove\s(\w{4,5})/.exec(line)[1];
                    this.applyBestmoveUci(m);
                }
            };

            this.engine.postMessage('uci');
        } catch (error) {
            console.warn('Erro ao inicializar Stockfish:', error);
        }
    }

    engineGo(fen, level) {
        if (!this.engine || !this.engineReady) return false;

        this.engineBusy = true;
        this.engine.postMessage('ucinewgame');
        this.engine.postMessage('isready');
        this.engine.postMessage('position fen ' + fen);

        let movetime = 200;
        if (level === 'beginner') {
            movetime = 150;
        } else if (level === 'club') {
            movetime = 400;
        } else if (level === 'master') {
            movetime = 800;
        }

        this.engine.postMessage('go movetime ' + movetime);
        return true;
    }

    applyBestmoveUci(uci) {
        const from = uci.slice(0, 2);
        const to = uci.slice(2, 4);
        const promo = uci.length === 5 ? uci[4] : undefined;
        const mv = this.game.move({
            from,
            to,
            promotion: promo || 'q'
        });

        if (mv) {
            this.updateBoard();
            const sideName = (mv.color === 'w') ? 'Brancas' : 'Pretas';
            const styleTag = (mv.color === 'w') ? 'Clássica' : 'Ataque';
            this.setNarration(`${sideName} (${styleTag}) jogam ${mv.san}.`);
            this.updateStatus();
        }
    }

    setupBoardEvents() {
        const board = document.getElementById('aeon-board');

        board.addEventListener('click', (e) => {
            const square = e.target.getAttribute('square');
            if (!square) return;

            this.handleSquareClick(square);
        });

        board.addEventListener('drop', (e) => {
            const detail = e.detail || {};
            const from = detail.source;
            const to = detail.target;

            this.handleMove(from, to);
        });
    }

    handleSquareClick(square) {
        const piece = this.game.get(square);
        const turn = this.game.turn();

        if (piece && piece.color === turn) {
            this.highlightPossibleMoves(square);
        } else if (this.selectedSquare && this.possibleMoves.includes(square)) {
            this.handleMove(this.selectedSquare, square);
        } else {
            this.clearHighlights();
        }
    }

    handleMove(from, to) {
        const positionBefore = this.game.fen();

        const move = this.game.move({
            from,
            to,
            promotion: 'q'
        });
        if (move) {
            this.analyzePlayerMove(move, positionBefore, this.game.fen());

            this.updateBoard();
            this.updateStatus();

            // Verificar fim do jogo para gamificação
            if (this.game.game_over()) {
                this.handleGameEnd();
            } else if (this.gameMode === 'vs-ai') {
                setTimeout(() => {
                    this.makeAIMove();
                }, 500);
            }
        }

        this.clearHighlights();
    }

    handleGameEnd() {
        // Determinar resultado do jogo
        let result = 'draw';
        let accuracy = this.playerAnalysis.accurateMovesCount / this.playerAnalysis.totalMoves * 100;
        let tacticalMoves = this.playerAnalysis.tacticalMovesCount;
        let blunders = this.playerAnalysis.blundersCount;

        if (this.game.in_checkmate()) {
            result = this.game.turn() === 'w' ? 'loss' : 'win'; // Se é vez das brancas, pretas venceram
        } else if (this.game.in_draw()) {
            result = 'draw';
        }

        // Integração com gamificação
        if (window.aeonGamification) {
            window.aeonGamification.onGameEnd(result, accuracy, tacticalMoves, blunders);
        }

        // Mostrar resultado
        if (result === 'win') {
            this.showMessage('🎉 Parabéns! Você venceu!');
        } else if (result === 'loss') {
            this.showMessage('💪 Boa tentativa! Continue praticando!');
        } else {
            this.showMessage('🤝 Empate! Jogo equilibrado!');
        }
    }

    analyzePlayerMove(move, positionBefore, positionAfter) {
        if (!this.isLoggedIn) return;

        const startTime = Date.now();

        if (this.playerAnalysis.moves.length === 0) {
            this.playerAnalysis.sessionStart = new Date();
        }

        const evaluation = this.evaluateMove(move, positionBefore, positionAfter);

        this.playerAnalysis.moves.push({
            move: move.san,
            from: move.from,
            to: move.to,
            thinkingTime: Date.now() - startTime,
            evaluation,
            ply: this.game.ply(),
            timestamp: new Date().toISOString()
        });

        this.playerAnalysis.totalMoves++;

        if (evaluation.score >= 0.8) this.playerAnalysis.accurateMovesCount++;
        if (evaluation.isTactical) this.playerAnalysis.tacticalMovesCount++;
        if (evaluation.score <= 0.3) this.playerAnalysis.blundersCount++;

        this.updateEstimatedElo();
        this.updateAnalysisDisplay();
        this.savePlayerAnalysis();
    }

    evaluateMove(move, posBefore, posAfter) {
        let score = 0.5;
        let isTactical = false;
        let reasoning = [];

        if (move.captured) {
            score += 0.3;
            isTactical = true;
            reasoning.push('captura');
        }

        if (move.san.includes('+')) {
            score += 0.2;
            isTactical = true;
            reasoning.push('xeque');
        }

        if ((move.piece === 'n' || move.piece === 'b') &&
            (move.from[1] === '1' || move.from[1] === '8')) {
            score += 0.2;
            reasoning.push('desenvolvimento');
        }

        const centralSquares = ['d4', 'd5', 'e4', 'e5'];
        if (centralSquares.includes(move.to)) {
            score += 0.15;
            reasoning.push('controle central');
        }

        if (move.san.includes('O')) {
            score += 0.25;
            reasoning.push('roque');
        }

        return {
            score: Math.max(0, Math.min(1, score)),
            isTactical,
            reasoning
        };
    }

    updateEstimatedElo() {
        if (this.playerAnalysis.totalMoves < 6) return;

        let baseElo = 1200;
        const accuracy = this.playerAnalysis.accurateMovesCount / this.playerAnalysis.totalMoves;
        const tacticalRatio = this.playerAnalysis.tacticalMovesCount / this.playerAnalysis.totalMoves;
        const blunderRatio = this.playerAnalysis.blundersCount / this.playerAnalysis.totalMoves;

        if (accuracy > 0.8) baseElo += 400;
        else if (accuracy > 0.7) baseElo += 200;
        else if (accuracy > 0.6) baseElo += 100;
        else if (accuracy < 0.4) baseElo -= 100;

        if (tacticalRatio > 0.3) baseElo += 150;
        else if (tacticalRatio < 0.1) baseElo -= 100;

        if (blunderRatio > 0.2) baseElo -= 200;

        this.playerAnalysis.estimatedElo = Math.max(800, Math.min(2400, baseElo));

        if (this.currentUser) {
            this.currentUser.elo = this.playerAnalysis.estimatedElo;
            localStorage.setItem('aeon_chess_user', JSON.stringify(this.currentUser));
        }
    }

    updateAnalysisDisplay() {
        const analysisContainer = document.getElementById('player-analysis');
        if (!analysisContainer) return;

        const elo = this.playerAnalysis.estimatedElo;
        const accuracy = (this.playerAnalysis.accurateMovesCount / this.playerAnalysis.totalMoves * 100).toFixed(0);
        const style = this.playerAnalysis.playStyle;

        analysisContainer.innerHTML = `
            <h3 class="text-lg font-bold mb-4">📊 Análise da Sessão</h3>
            <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="text-center">
                    <div class="text-2xl font-bold text-blue-400">${elo}</div>
                    <div class="text-sm text-gray-300">ELO Estimado</div>
                </div>
                <div class="text-center">
                    <div class="text-2xl font-bold text-green-400">${accuracy}%</div>
                    <div class="text-sm text-gray-300">Precisão</div>
                </div>
            </div>
            <div class="analysis-metric">
                <span>Estilo de Jogo:</span>
                <span class="capitalize">${style}</span>
            </div>
            <div class="analysis-metric">
                <span>Movimentos Analisados:</span>
                <span>${this.playerAnalysis.totalMoves}</span>
            </div>
            <div class="mt-4">
                <button onclick="aeonApp.showDetailedAnalysis()" class="btn-primary">
                    📈 Ver Análise Detalhada
                </button>
            </div>
        `;
    }

    showDetailedAnalysis() {
        const modal = document.createElement('div');
        modal.className = 'login-modal';
        modal.innerHTML = `
            <div class="login-form" style="max-width: 600px;">
                <h2>📊 Análise Detalhada com Stockfish</h2>
                <div id="detailed-analysis">
                    ${this.generateDetailedAnalysisHTML()}
                </div>
                <button onclick="this.closest('.login-modal').remove()" class="btn-primary">
                    Fechar
                </button>
            </div>
        `;
        document.body.appendChild(modal);
    }

    generateDetailedAnalysisHTML() {
        const analysis = this.playerAnalysis;
        const elo = analysis.estimatedElo;
        const accuracy = (analysis.accurateMovesCount / analysis.totalMoves * 100).toFixed(0);

        return `
            <div class="space-y-4">
                <div class="grid grid-cols-3 gap-4">
                    <div class="text-center p-4 bg-blue-100 rounded">
                        <div class="text-2xl font-bold text-blue-600">${elo}</div>
                        <div class="text-sm text-gray-600">ELO Estimado</div>
                    </div>
                    <div class="text-center p-4 bg-green-100 rounded">
                        <div class="text-2xl font-bold text-green-600">${accuracy}%</div>
                        <div class="text-sm text-gray-600">Precisão</div>
                    </div>
                    <div class="text-center p-4 bg-purple-100 rounded">
                        <div class="text-2xl font-bold text-purple-600">${analysis.totalMoves}</div>
                        <div class="text-sm text-gray-600">Movimentos</div>
                    </div>
                </div>
                
                <div class="space-y-2">
                    <h4 class="font-bold">🎯 Estatísticas</h4>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        <div>Movimentos Precisos: ${analysis.accurateMovesCount}</div>
                        <div>Movimentos Táticos: ${analysis.tacticalMovesCount}</div>
                        <div>Erros Críticos: ${analysis.blundersCount}</div>
                        <div>IA Stockfish: ${this.engineReady ? '✅ Ativo' : '❌ Inativo'}</div>
                    </div>
                </div>
                
                <div class="space-y-2">
                    <h4 class="font-bold">📈 Recomendações</h4>
                    ${this.generateRecommendations()}
                </div>
            </div>
        `;
    }

    generateRecommendations() {
        const analysis = this.playerAnalysis;
        const elo = analysis.estimatedElo;
        const accuracy = analysis.accurateMovesCount / analysis.totalMoves;

        let recommendations = [];

        if (accuracy < 0.6) {
            recommendations.push('🎯 Pratique táticas básicas diariamente');
        }

        if (analysis.tacticalMovesCount / analysis.totalMoves < 0.2) {
            recommendations.push('⚡ Trabalhe em reconhecimento de padrões táticos');
        }

        if (elo < 1400) {
            recommendations.push('🏆 Foque em consistência antes de complexidade');
        } else if (elo > 1800) {
            recommendations.push('🌟 Considere treinamento avançado com coach');
        }

        return recommendations.map(rec => `<div class="text-sm">• ${rec}</div>`).join('');
    }

    savePlayerAnalysis() {
        if (this.currentUser) {
            const analysisData = {
                userId: this.currentUser.id,
                sessionId: this.playerAnalysis.sessionStart,
                analysis: this.playerAnalysis,
                timestamp: new Date().toISOString()
            };

            const savedAnalyses = JSON.parse(localStorage.getItem('aeon_analyses') || '[]');
            savedAnalyses.push(analysisData);
            localStorage.setItem('aeon_analyses', JSON.stringify(savedAnalyses));
        }
    }

    startPlayerAnalysis() {
        this.playerAnalysis = {
            moves: [],
            totalMoves: 0,
            accurateMovesCount: 0,
            tacticalMovesCount: 0,
            blundersCount: 0,
            averageThinkingTime: 0,
            openingKnowledge: 0,
            endgameSkill: 0,
            estimatedElo: this.currentUser ? .elo || 1200,
            playStyle: 'balanced',
            weaknesses: [],
            strengths: [],
            sessionStart: new Date()
        };

        this.updateAnalysisDisplay();
    }

    setupEventListeners() {
        // Botão Jogar Agora funcional
        document.addEventListener('click', (e) => {
            if (e.target.id === 'cta-play' || e.target.id === 'nav-play') {
                this.startGameMode('vs-ai');
                // Scroll para o tabuleiro
                const board = document.getElementById('aeon-board');
                if (board) {
                    board.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }

            if (e.target.id === 'cta-demo') {
                this.startGameMode('demo');
                // Scroll para o tabuleiro
                const board = document.getElementById('aeon-board');
                if (board) {
                    board.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }

            // Botões do tabuleiro
            if (e.target.id === 'aeon-undo') {
                this.undoMove();
            }

            if (e.target.id === 'aeon-reset') {
                this.resetGame();
            }
        });

        // Terminal cultural
        document.addEventListener('click', (e) => {
            if (e.target.hasAttribute('data-terminal-continue')) {
                this.startTerminalExperience();
            }
        });
    }

    setupNavigation() {
        const nav = document.querySelector('nav');
        if (nav) {
            const additionalLinks = document.createElement('div');
            additionalLinks.className = 'flex items-center space-x-6';
            additionalLinks.innerHTML = `
                <a href="/analysis" class="nav-link">📊 Análises</a>
                <a href="/training" class="nav-link">🎯 Treinamento</a>
                <a href="/profile" class="nav-link">👤 Perfil</a>
            `;
            nav.appendChild(additionalLinks);
        }
    }

    startGameMode(mode) {
        this.gameMode = mode;
        this.game.reset();
        this.updateBoard();
        this.updateStatus();

        // Integração com gamificação
        if (window.aeonGamification) {
            window.aeonGamification.onGameStart();
        }

        if (mode === 'vs-ai') {
            this.showMessage('🎮 Modo vs IA ativado. Você joga com as Brancas!');
        } else if (mode === 'demo') {
            this.showMessage('🎯 Modo demonstração. Analisando seus movimentos...');
        }
    }

    makeAIMove() {
        if (!this.game || this.game.game_over()) return;

        const strong = document.getElementById('ai-strong') ? .checked;
        const level = document.getElementById('ai-level') ? .value || 'club';

        if (strong && this.engine && this.engineReady && !this.engineBusy) {
            this.engineGo(this.game.fen(), level);
            return;
        }

        const moves = this.game.moves({
            verbose: true
        });
        if (moves.length === 0) return;

        let bestMove = null;
        let bestScore = -Infinity;

        for (const move of moves) {
            this.game.move(move);
            const score = this.evaluatePosition();
            this.game.undo();

            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }

        if (bestMove) {
            this.game.move(bestMove);
            this.updateBoard();
            this.updateStatus();
        }
    }

    evaluatePosition() {
        const pieceValues = {
            p: 1,
            n: 3,
            b: 3,
            r: 5,
            q: 9,
            k: 0
        };
        const fen = this.game.fen().split(' ')[0];
        let score = 0;

        for (const ch of fen) {
            if (ch === '/' || !isNaN(Number(ch))) continue;
            const isUpper = ch === ch.toUpperCase();
            const val = pieceValues[ch.toLowerCase()] ? ? 0;
            score += isUpper ? val : -val;
        }

        return score;
    }

    updateBoard() {
        if (this.board && typeof this.board.setPosition === 'function') {
            this.board.setPosition(this.game.fen());
        }
    }

    updateStatus() {
        const status = document.getElementById('aeon-status');
        if (!status) return;

        let msg = '';
        if (this.game.in_checkmate()) {
            msg = 'Xeque-mate! ' + (this.game.turn() === 'w' ? 'Pretas' : 'Brancas') + ' venceram.';
        } else if (this.game.in_draw()) {
            msg = 'Empate.';
        } else {
            msg = (this.game.turn() === 'w' ? 'Brancas' : 'Pretas') + ' para jogar' + (this.game.in_check() ? ' (em xeque)' : '');
        }
        status.textContent = msg;
    }

    setNarration(text) {
        const narration = document.getElementById('aeon-narration');
        if (narration) {
            narration.textContent = text;
        }
    }

    highlightPossibleMoves(square) {
        this.clearHighlights();
        this.selectedSquare = square;

        const moves = this.game.moves({
            square: square,
            verbose: true
        });
        this.possibleMoves = moves.map(m => m.to);

        const selectedElement = this.board.querySelector(`[square="${square}"]`);
        if (selectedElement) {
            selectedElement.classList.add('selected');
        }

        moves.forEach(move => {
            const targetElement = this.board.querySelector(`[square="${move.to}"]`);
            if (targetElement) {
                if (move.captured) {
                    targetElement.classList.add('highlight-capture');
                } else {
                    targetElement.classList.add('highlight-move');
                }
            }
        });
    }

    clearHighlights() {
        this.selectedSquare = null;
        this.possibleMoves = [];

        const highlighted = this.board.querySelectorAll('.selected, .highlight-move, .highlight-capture');
        highlighted.forEach(el => {
            el.classList.remove('selected', 'highlight-move', 'highlight-capture');
        });
    }

    showMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message success';
        messageDiv.textContent = text;
        messageDiv.style.position = 'fixed';
        messageDiv.style.top = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.zIndex = '1000';

        document.body.appendChild(messageDiv);

        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    undoMove() {
        if (this.game && this.game.history().length > 0) {
            this.game.undo();
            this.game.undo(); // Desfazer movimento da IA também
            this.updateBoard();
            this.updateStatus();
            this.setNarration('Movimento desfeito.');
        }
    }

    resetGame() {
        if (this.game) {
            this.game.reset();
            this.updateBoard();
            this.updateStatus();
            this.setNarration('Jogo reiniciado.');
            this.clearHighlights();
        }
    }

    startTerminalExperience() {
        if (window.aeonTerminal) {
            window.aeonTerminal.startExperience();
        } else {
            console.log('Terminal cultural não disponível');
        }
    }
}

// Inicializar aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.aeonApp = new AeonChessApp();
});