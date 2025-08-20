/**
 * 🧪 Board Test - Teste dos Tabuleiros
 * Verifica se os tabuleiros estão funcionando corretamente
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class BoardTest {
    constructor() {
        this.name = 'Board Test';
        this.version = '1.0.0';

        console.log(`🧪 ${this.name} v${this.version} inicializando...`);
    }

    /**
     * Executar todos os testes
     */
    runAllTests() {
        console.log('🧪 Executando testes dos tabuleiros...');

        this.testChessBoardClass();
        this.testBoardElements();
        this.testBoardInitialization();
        this.testBoardFunctionality();

        console.log('🧪 Todos os testes concluídos!');
    }

    /**
     * Testar se a classe ChessBoard está disponível
     */
    testChessBoardClass() {
        console.log('🧪 Testando classe ChessBoard...');

        if (window.ChessBoard) {
            console.log('✅ Classe ChessBoard encontrada');

            try {
                const testBoard = new window.ChessBoard(document.createElement('div'), {
                    position: 'start',
                    draggable: true
                });
                console.log('✅ Instância de ChessBoard criada com sucesso');

                // Testar métodos básicos
                if (typeof testBoard.position === 'function') {
                    console.log('✅ Método position() disponível');
                }

                if (typeof testBoard.move === 'function') {
                    console.log('✅ Método move() disponível');
                }

                if (typeof testBoard.reset === 'function') {
                    console.log('✅ Método reset() disponível');
                }

            } catch (error) {
                console.error('❌ Erro ao criar instância de ChessBoard:', error);
            }
        } else {
            console.error('❌ Classe ChessBoard não encontrada!');
        }
    }

    /**
     * Testar elementos de tabuleiro no DOM
     */
    testBoardElements() {
        console.log('🧪 Testando elementos de tabuleiro no DOM...');

        // Procurar por elementos chess-board
        const chessBoards = document.querySelectorAll('chess-board');
        console.log(`📊 Elementos chess-board encontrados: ${chessBoards.length}`);

        chessBoards.forEach((board, index) => {
            console.log(`   - chess-board ${index}:`, {
                id: board.id,
                position: board.position,
                draggablePieces: board.draggablePieces,
                className: board.className
            });
        });

        // Procurar por divs de tabuleiro
        const boardDivs = document.querySelectorAll('#aeon-board, #narrative-board');
        console.log(`📊 Divs de tabuleiro encontrados: ${boardDivs.length}`);

        boardDivs.forEach((div, index) => {
            console.log(`   - div ${index}:`, {
                id: div.id,
                className: div.className,
                innerHTML: div.innerHTML.substring(0, 100) + '...'
            });
        });
    }

    /**
     * Testar inicialização dos tabuleiros
     */
    testBoardInitialization() {
        console.log('🧪 Testando inicialização dos tabuleiros...');

        // Verificar se o BoardInitializer está funcionando
        if (window.boardInitializer) {
            console.log('✅ BoardInitializer encontrado');

            const boards = window.boardInitializer.getAllBoards();
            console.log(`📊 Tabuleiros inicializados: ${boards.length}`);

            boards.forEach((board, index) => {
                console.log(`   - Tabuleiro ${index}:`, {
                    type: board.constructor.name,
                    working: window.boardInitializer.isBoardWorking(board.id || index)
                });
            });
        } else {
            console.error('❌ BoardInitializer não encontrado!');
        }
    }

    /**
     * Testar funcionalidade dos tabuleiros
     */
    testBoardFunctionality() {
        console.log('🧪 Testando funcionalidade dos tabuleiros...');

        // Testar tabuleiro hero
        const heroBoard = document.querySelector('#aeon-board');
        if (heroBoard) {
            console.log('🧪 Testando tabuleiro hero...');
            this.testBoardElement(heroBoard, 'hero');
        }

        // Testar tabuleiro narrativo
        const narrativeBoard = document.querySelector('#narrative-board');
        if (narrativeBoard) {
            console.log('🧪 Testando tabuleiro narrativo...');
            this.testBoardElement(narrativeBoard, 'narrativo');
        }
    }

    /**
     * Testar elemento de tabuleiro específico
     */
    testBoardElement(boardElement, name) {
        try {
            console.log(`🧪 Testando ${name}...`);

            // Verificar se tem conteúdo
            if (boardElement.innerHTML.trim() === '') {
                console.log(`   - ${name}: Container vazio`);
            } else {
                console.log(`   - ${name}: Tem conteúdo`);
            }

            // Verificar se tem tabuleiro renderizado
            const chessBoardWrapper = boardElement.querySelector('.chess-board-wrapper');
            if (chessBoardWrapper) {
                console.log(`   - ${name}: Tabuleiro renderizado encontrado`);

                // Verificar se tem peças
                const pieces = chessBoardWrapper.querySelectorAll('.chess-piece');
                console.log(`   - ${name}: ${pieces.length} peças encontradas`);

                // Verificar se tem casas
                const squares = chessBoardWrapper.querySelectorAll('.chess-square');
                console.log(`   - ${name}: ${squares.length} casas encontradas`);

            } else {
                console.log(`   - ${name}: Tabuleiro não renderizado`);
            }

        } catch (error) {
            console.error(`❌ Erro ao testar ${name}:`, error);
        }
    }

    /**
     * Criar tabuleiro de teste se necessário
     */
    createTestBoard() {
        console.log('🧪 Criando tabuleiro de teste...');

        try {
            // Criar container de teste
            const testContainer = document.createElement('div');
            testContainer.id = 'test-board';
            testContainer.style.cssText = 'width: 400px; height: 400px; border: 2px solid red; margin: 20px;';
            document.body.appendChild(testContainer);

            // Criar tabuleiro
            if (window.ChessBoard) {
                const testBoard = new window.ChessBoard(testContainer, {
                    position: 'start',
                    draggable: true
                });

                console.log('✅ Tabuleiro de teste criado com sucesso!');
                return testBoard;
            } else {
                console.error('❌ Não foi possível criar tabuleiro de teste');
                return null;
            }

        } catch (error) {
            console.error('❌ Erro ao criar tabuleiro de teste:', error);
            return null;
        }
    }

    /**
     * Mostrar relatório de teste
     */
    showTestReport() {
        console.log('🧪 === RELATÓRIO DE TESTE ===');

        const report = {
            chessBoardClass: !!window.ChessBoard,
            boardInitializer: !!window.boardInitializer,
            chessBoardElements: document.querySelectorAll('chess-board').length,
            boardDivs: document.querySelectorAll('#aeon-board, #narrative-board').length,
            initializedBoards: window.boardInitializer ? window.boardInitializer.getAllBoards().length : 0
        };

        console.log('📊 Status dos componentes:', report);

        if (report.chessBoardClass && report.boardInitializer && report.initializedBoards > 0) {
            console.log('🎉 Todos os componentes estão funcionando!');
        } else {
            console.log('⚠️ Alguns componentes têm problemas:');

            if (!report.chessBoardClass) console.log('   - Classe ChessBoard não encontrada');
            if (!report.boardInitializer) console.log('   - BoardInitializer não encontrado');
            if (report.initializedBoards === 0) console.log('   - Nenhum tabuleiro inicializado');
        }
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.BoardTest = BoardTest;

    // Criar instância de teste
    const boardTest = new BoardTest();

    // Executar testes após um delay para garantir que tudo carregou
    setTimeout(() => {
        boardTest.runAllTests();
        boardTest.showTestReport();
    }, 2000);

    // Disponibilizar globalmente
    window.boardTest = boardTest;
}

// Log de inicialização