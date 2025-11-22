/**
 * 🐛 Smart Chess Board Debug - Sistema de Debug
 * Verifica e corrige problemas de conexão entre base de dados e automação
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class SmartChessBoardDebug {
    constructor() {
        this.name = 'Smart Chess Board Debug';
        this.version = '1.0.0';
        this.debugMode = true;

        console.log(`🐛 ${this.name} v${this.version} inicializando...`);
        this.init();
    }

    init() {
        // Verificar sistemas após carregamento
        setTimeout(() => {
            this.checkAllSystems();
        }, 2000);

        // Verificar periodicamente
        setInterval(() => {
            this.monitorSystems();
        }, 5000);
    }

    checkAllSystems() {
        console.log('🐛 === VERIFICAÇÃO COMPLETA DOS SISTEMAS ===');

        // 1. Verificar tabuleiro
        this.checkBoard();

        // 2. Verificar base de dados
        this.checkDatabase();

        // 3. Verificar ARKITECT
        this.checkArkitect();

        // 4. Verificar Smart Chess Board
        this.checkSmartBoard();

        // 5. Verificar interface
        this.checkInterface();

        // 6. Verificar automação
        this.checkAutomation();

        console.log('🐛 === VERIFICAÇÃO CONCLUÍDA ===');
    }

    checkBoard() {
        console.log('🐛 Verificando tabuleiro...');

        const board = document.querySelector('#aeon-board');
        const wrapper = document.querySelector('#aeon-board .chess-board-wrapper');

        if (board) {
            console.log('✅ Tabuleiro encontrado:', board);
            console.log('   - ID:', board.id);
            console.log('   - Display:', board.style.display);
            console.log('   - Visibility:', board.style.visibility);
            console.log('   - Opacity:', board.style.opacity);
        } else {
            console.error('❌ Tabuleiro não encontrado!');
        }

        if (wrapper) {
            console.log('✅ Wrapper encontrado:', wrapper);
        } else {
            console.error('❌ Wrapper não encontrado!');
        }
    }

    checkDatabase() {
        console.log('🐛 Verificando base de dados...');

        if (window.chessProDB) {
            console.log('✅ Base de dados encontrada:', window.chessProDB);

            try {
                const stats = window.chessProDB.getStatistics();
                console.log('   - Total de posições:', stats.totalPositions);
                console.log('   - Categorias:', Object.keys(stats.categories));

                // Verificar categorias específicas
                this.checkDatabaseCategories();
            } catch (error) {
                console.error('❌ Erro ao obter estatísticas:', error);
            }
        } else {
            console.error('❌ Base de dados não encontrada!');
        }
    }

    checkDatabaseCategories() {
        const categories = ['openings', 'tacticalPatterns', 'classicEndgames', 'historicalPositions', 'grandmasterGames'];

        categories.forEach(category => {
            if (window.chessProDB[category]) {
                const catData = window.chessProDB[category];
                console.log(`   - ${category}: ${catData.total} posições`);

                if (catData.subcategories) {
                    const subcats = Object.keys(catData.subcategories);
                    console.log(`     Subcategorias: ${subcats.length}`);

                    // Verificar se há posições
                    let totalPositions = 0;
                    subcats.forEach(subcat => {
                        if (catData.subcategories[subcat].positions) {
                            totalPositions += catData.subcategories[subcat].positions.length;
                        }
                    });
                    console.log(`     Total de posições reais: ${totalPositions}`);
                }
            } else {
                console.error(`❌ Categoria ${category} não encontrada!`);
            }
        });
    }

    checkArkitect() {
        console.log('🐛 Verificando sistema ARKITECT...');

        if (window.arkitectSolution) {
            console.log('✅ ARKITECT encontrado:', window.arkitectSolution);

            try {
                const status = window.arkitectSolution.getStatus();
                console.log('   - Nome:', status.name);
                console.log('   - Versão:', status.version);
                console.log('   - Ativo:', status.isActive);
                console.log('   - Tabuleiro:', status.board);
            } catch (error) {
                console.error('❌ Erro ao obter status do ARKITECT:', error);
            }
        } else {
            console.error('❌ ARKITECT não encontrado!');
        }
    }

    checkSmartBoard() {
        console.log('🐛 Verificando Smart Chess Board...');

        if (window.smartChessBoard) {
            console.log('✅ Smart Chess Board encontrado:', window.smartChessBoard);

            try {
                const status = window.smartChessBoard.getStatus();
                console.log('   - Nome:', status.name);
                console.log('   - Versão:', status.version);
                console.log('   - Tabuleiro:', status.board);
                console.log('   - Base de dados:', status.database);
                console.log('   - Categoria atual:', status.currentCategory);
                console.log('   - Posição atual:', status.currentPosition);
                console.log('   - Total de posições:', status.totalPositions);
                console.log('   - Demo automático:', status.autoDemo);
                console.log('   - ARKITECT ativo:', status.arkitectActive);
            } catch (error) {
                console.error('❌ Erro ao obter status do Smart Board:', error);
            }
        } else {
            console.error('❌ Smart Chess Board não encontrado!');
            this.forceCreateSmartBoard();
        }
    }

    checkInterface() {
        console.log('🐛 Verificando interface...');

        const smartInterface = document.querySelector('.smart-interface');
        if (smartInterface) {
            console.log('✅ Interface encontrada:', smartInterface);

            // Verificar elementos da interface
            const elements = [
                'smart-prev', 'smart-next', 'smart-play', 'smart-arkitect',
                'smart-position-title', 'smart-position-desc', 'smart-position-analysis',
                'smart-progress-fill', 'smart-position-counter'
            ];

            elements.forEach(elementId => {
                const element = document.getElementById(elementId);
                if (element) {
                    console.log(`   ✅ ${elementId}: encontrado`);
                } else {
                    console.error(`   ❌ ${elementId}: não encontrado`);
                }
            });
        } else {
            console.error('❌ Interface não encontrada!');
            this.forceCreateInterface();
        }
    }

    checkAutomation() {
        console.log('🐛 Verificando automação...');

        if (window.smartChessBoard) {
            const status = window.smartChessBoard.getStatus();

            if (status.autoDemo) {
                console.log('✅ Demo automático está ativo');
            } else {
                console.log('⚠️ Demo automático não está ativo');
                this.forceStartAutomation();
            }

            if (status.totalPositions > 0) {
                console.log('✅ Posições disponíveis para automação');
            } else {
                console.error('❌ Nenhuma posição disponível para automação!');
                this.forceLoadPositions();
            }
        }
    }

    forceCreateSmartBoard() {
        console.log('🐛 Forçando criação do Smart Chess Board...');

        if (window.SmartChessBoard) {
            window.smartChessBoard = new window.SmartChessBoard();
            console.log('✅ Smart Chess Board criado forçadamente');
        } else {
            console.error('❌ Classe SmartChessBoard não encontrada!');
        }
    }

    forceCreateInterface() {
        console.log('🐛 Forçando criação da interface...');

        if (window.smartChessBoard) {
            window.smartChessBoard.createSmartInterface();
            console.log('✅ Interface criada forçadamente');
        }
    }

    forceStartAutomation() {
        console.log('🐛 Forçando início da automação...');

        if (window.smartChessBoard) {
            window.smartChessBoard.startAutoDemo();
            console.log('✅ Automação iniciada forçadamente');
        }
    }

    forceLoadPositions() {
        console.log('🐛 Forçando carregamento de posições...');

        if (window.smartChessBoard) {
            window.smartChessBoard.changeCategory('openings');
            console.log('✅ Posições carregadas forçadamente');
        }
    }

    monitorSystems() {
        if (!this.debugMode) return;

        // Verificar se a automação está funcionando
        if (window.smartChessBoard) {
            const status = window.smartChessBoard.getStatus();

            if (status.autoDemo && status.totalPositions === 0) {
                console.warn('🐛 ALERTA: Demo ativo mas sem posições!');
                this.forceLoadPositions();
            }

            if (!status.autoDemo && status.totalPositions > 0) {
                console.warn('🐛 ALERTA: Posições disponíveis mas demo inativo!');
                this.forceStartAutomation();
            }
        }
    }

    // Métodos de teste
    testDatabaseConnection() {
        console.log('🧪 Testando conexão com base de dados...');

        if (window.chessProDB) {
            const positions = this.getAllPositions('openings');
            console.log(`🧪 Posições encontradas: ${positions.length}`);

            if (positions.length > 0) {
                const firstPosition = positions[0];
                console.log('🧪 Primeira posição:', firstPosition);

                // Testar carregamento no tabuleiro
                if (window.smartChessBoard) {
                    window.smartChessBoard.loadPosition(firstPosition);
                    console.log('🧪 Posição carregada no tabuleiro');
                }
            }
        }
    }

    getAllPositions(category) {
        if (!window.chessProDB) return [];

        const categoryData = window.chessProDB[category];
        if (!categoryData || !categoryData.subcategories) return [];

        const allPositions = [];
        Object.values(categoryData.subcategories).forEach(subcategory => {
            if (subcategory.positions) {
                allPositions.push(...subcategory.positions);
            }
        });

        return allPositions;
    }

    // Métodos de correção
    fixDatabaseConnection() {
        console.log('🔧 Corrigindo conexão com base de dados...');

        // Forçar recriação do Smart Chess Board
        if (window.smartChessBoard) {
            delete window.smartChessBoard;
        }

        setTimeout(() => {
            if (window.SmartChessBoard) {
                window.smartChessBoard = new window.SmartChessBoard();
                console.log('🔧 Smart Chess Board recriado');
            }
        }, 1000);
    }

    fixAutomation() {
        console.log('🔧 Corrigindo automação...');

        if (window.smartChessBoard) {
            // Parar demo atual
            window.smartChessBoard.stopAutoDemo();

            // Recarregar posições
            window.smartChessBoard.changeCategory('openings');

            // Reiniciar demo
            setTimeout(() => {
                window.smartChessBoard.startAutoDemo();
                console.log('🔧 Automação corrigida');
            }, 1000);
        }
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.SmartChessBoardDebug = SmartChessBoardDebug;

    // Inicializar automaticamente
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🐛 Inicializando Smart Chess Board Debug...');
        window.smartChessBoardDebug = new SmartChessBoardDebug();
    });
}

console.log('🐛 Smart Chess Board Debug carregado');