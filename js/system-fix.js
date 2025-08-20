/**
 * 🔧 System Fix - Correção Automática dos Sistemas
 * Garante que todos os sistemas funcionem corretamente
 */

class SystemFix {
    constructor() {
        this.name = 'System Fix';
        this.version = '1.0.0';

        console.log(`🔧 ${this.name} v${this.version} carregado`);
        this.init();
    }

    init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startFix());
        } else {
            this.startFix();
        }
    }

    startFix() {
        console.log('🔧 Iniciando correção automática dos sistemas...');

        // Aguardar um pouco para todos os scripts carregarem
        setTimeout(() => {
            this.checkAndFixBoards();
            this.checkAndFixArkitect();
            this.checkAndFixSmartBoard();
            this.checkAndFixDatabase();

            console.log('🔧 Correção automática concluída');
        }, 3000);
    }

    checkAndFixBoards() {
        console.log('🎯 Verificando tabuleiros...');

        const chessBoardElements = document.querySelectorAll('chess-board');
        console.log(`🎯 Encontrados ${chessBoardElements.length} elementos chess-board`);

        chessBoardElements.forEach((element, index) => {
            const hasWrapper = element.querySelector('.chess-board-wrapper');
            if (!hasWrapper) {
                console.log(`🎯 Tabuleiro ${index + 1} (${element.id || 'sem ID'}) não inicializado, corrigindo...`);

                if (window.ChessBoard) {
                    try {
                        // Garantir estilos básicos
                        element.style.position = 'relative';
                        element.style.width = '100%';
                        element.style.aspectRatio = '1 / 1';
                        element.style.display = 'block';
                        element.style.visibility = 'visible';
                        element.style.opacity = '1';

                        // Criar instância do tabuleiro
                        const boardInstance = new window.ChessBoard(element, {
                            position: 'start',
                            draggable: true,
                            dropOffBoard: 'snapback'
                        });

                        // Expor métodos no elemento
                        element.setPosition = (fen) => {
                            try {
                                boardInstance.position(fen);
                            } catch (e) {
                                console.warn('🎯 setPosition falhou:', e);
                            }
                        };

                        element.getPosition = () => {
                            try {
                                return boardInstance.position();
                            } catch (e) {
                                console.warn('🎯 getPosition falhou:', e);
                                return null;
                            }
                        };

                        element.__boardInstance = boardInstance;

                        console.log(`🎯 Tabuleiro ${index + 1} corrigido ✅`);
                    } catch (error) {
                        console.error(`🎯 Erro ao corrigir tabuleiro ${index + 1}:`, error);
                    }
                } else {
                    console.error('🎯 ChessBoard não disponível');
                }
            } else {
                console.log(`🎯 Tabuleiro ${index + 1} (${element.id || 'sem ID'}) OK ✅`);
            }
        });
    }

    checkAndFixArkitect() {
        console.log('🏗️ Verificando ARKITECT...');

        if (window.arkitectSolution) {
            const status = window.arkitectSolution.getStatus();
            console.log('🏗️ Status ARKITECT:', status);

            if (!status.isActive && status.board === '✅') {
                console.log('🏗️ Iniciando ARKITECT automaticamente...');
                setTimeout(() => {
                    try {
                        window.arkitectSolution.start();
                        console.log('🏗️ ARKITECT iniciado ✅');
                    } catch (error) {
                        console.error('🏗️ Erro ao iniciar ARKITECT:', error);
                    }
                }, 2000);
            } else if (status.isActive) {
                console.log('🏗️ ARKITECT já está ativo ✅');
            } else {
                console.warn('🏗️ ARKITECT não pode ser iniciado - tabuleiro não disponível');
            }
        } else {
            console.warn('🏗️ ARKITECT não encontrado - tentando recriar...');
            this.recreateArkitect();
        }
    }

    recreateArkitect() {
        // Tentar recriar o ARKITECT se não existir
        if (window.ArkitectSimpleSolution) {
            try {
                window.arkitectSolution = new window.ArkitectSimpleSolution();
                console.log('🏗️ ARKITECT recriado ✅');
            } catch (error) {
                console.error('🏗️ Erro ao recriar ARKITECT:', error);
            }
        }
    }

    checkAndFixSmartBoard() {
        console.log('🧠 Verificando Smart Chess Board...');

        if (window.smartChessBoard) {
            const status = window.smartChessBoard.getStatus();
            console.log('🧠 Status Smart Chess Board:', status);

            if (!status.autoDemo && status.totalPositions > 0) {
                console.log('🧠 Iniciando demonstração automática...');
                setTimeout(() => {
                    try {
                        window.smartChessBoard.startAutoDemo();
                        console.log('🧠 Demonstração iniciada ✅');
                    } catch (error) {
                        console.error('🧠 Erro ao iniciar demonstração:', error);
                    }
                }, 4000);
            } else if (status.autoDemo) {
                console.log('🧠 Smart Chess Board já está ativo ✅');
            } else {
                console.warn('🧠 Smart Chess Board sem posições disponíveis');
            }
        } else {
            console.warn('🧠 Smart Chess Board não encontrado');
        }
    }

    checkAndFixDatabase() {
        console.log('📊 Verificando Chess Pro Database...');

        if (window.chessProDB) {
            const stats = window.chessProDB.getStatistics();
            console.log('📊 Database stats:', stats);
            console.log('📊 Chess Pro Database OK ✅');
        } else {
            console.warn('📊 Chess Pro Database não encontrado');
        }
    }

    // Métodos públicos para debug
    fixAll() {
        console.log('🔧 Forçando correção de todos os sistemas...');
        this.checkAndFixBoards();
        this.checkAndFixArkitect();
        this.checkAndFixSmartBoard();
        this.checkAndFixDatabase();
    }

    getSystemsStatus() {
        return {
            ChessBoard: window.ChessBoard ? '✅' : '❌',
            BoardInitializer: window.boardInitializer ? '✅' : '❌',
            ARKITECT: window.arkitectSolution ? '✅' : '❌',
            SmartChessBoard: window.smartChessBoard ? '✅' : '❌',
            ChessProDB: window.chessProDB ? '✅' : '❌',
            HistoricalBattles: window.historicalBattlesUI ? '✅' : '❌'
        };
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.SystemFix = SystemFix;
    window.systemFix = new SystemFix();
}

console.log('🔧 System Fix carregado');