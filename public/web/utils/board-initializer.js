/**
 * 🎯 Board Initializer - Inicializador Simples dos Tabuleiros
 * Garante que todos os tabuleiros sejam inicializados corretamente
 * 
 * @author AEON CHESS Team
 * @version 1.0.0
 * @date Janeiro 2025
 */

class BoardInitializer {
    constructor() {
        this.name = 'Board Initializer';
        this.version = '1.0.0';
        this.boards = new Map();

        console.log(`🎯 ${this.name} v${this.version} inicializando...`);
    }

    /**
     * Inicializar todos os tabuleiros
     */
    init() {
        console.log('🎯 Inicializando tabuleiros de xadrez...');

        try {
            // Aguardar DOM estar pronto
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.initializeAllBoards();
                });
            } else {
                this.initializeAllBoards();
            }
        } catch (error) {
            console.error('🎯 Erro na inicialização dos tabuleiros:', error);
        }
    }

    /**
     * Inicializar todos os tabuleiros encontrados
     */
    initializeAllBoards() {
        // Procurar por elementos chess-board
        const chessBoards = document.querySelectorAll('chess-board');
        console.log(`🎯 Encontrados ${chessBoards.length} tabuleiros para inicializar`);

        chessBoards.forEach((boardElement, index) => {
            try {
                this.initializeBoard(boardElement, index);
            } catch (error) {
                console.error(`🎯 Erro ao inicializar tabuleiro ${index}:`, error);
            }
        });

        // Procurar por divs com ID específico
        const boardDivs = document.querySelectorAll('#aeon-board, #narrative-board');
        console.log(`🎯 Encontrados ${boardDivs.length} divs de tabuleiro para inicializar`);

        boardDivs.forEach((boardDiv, index) => {
            try {
                this.initializeBoardDiv(boardDiv, index);
            } catch (error) {
                console.error(`🎯 Erro ao inicializar div de tabuleiro ${index}:`, error);
            }
        });

        // Verificar se há algum problema
        this.checkBoardStatus();
    }

    /**
     * Inicializar elemento chess-board
     */
    initializeBoard(boardElement, index) {
        const boardId = boardElement.id || `chess-board-${index}`;
        console.log(`🎯 Inicializando chess-board: ${boardId}`);

        try {
            // Verificar se o elemento tem as propriedades necessárias
            if (!boardElement.position) {
                boardElement.position = 'start';
            }

            if (!boardElement.draggablePieces) {
                boardElement.draggablePieces = '';
            }

            // Adicionar evento de inicialização
            boardElement.addEventListener('ready', () => {
                console.log(`🎯 Tabuleiro ${boardId} inicializado com sucesso`);
                this.boards.set(boardId, boardElement);
            });

            // Adicionar evento de erro
            boardElement.addEventListener('error', (error) => {
                console.error(`🎯 Erro no tabuleiro ${boardId}:`, error);
            });

            // Adaptador: se não houver web component real, instanciar nosso ChessBoard DENTRO do próprio elemento
            const hasOurBoard = boardElement && boardElement.querySelector('.chess-board-wrapper');
            if (window.ChessBoard && boardElement && !hasOurBoard) {
                console.log(`🎯 Criando instância ChessBoard para ${boardId} no próprio elemento`);
                const options = {
                    position: boardElement.getAttribute('position') || 'start',
                    draggable: true,
                    dropOffBoard: 'snapback'
                };
                try {
                    // Garantir que o elemento tenha dimensões
                    if (!boardElement.style.position) boardElement.style.position = 'relative';
                    if (!boardElement.style.width) boardElement.style.width = '100%';
                    if (!boardElement.style.aspectRatio && !boardElement.style.height) {
                        boardElement.style.aspectRatio = '1 / 1';
                    }

                    const boardInstance = new window.ChessBoard(boardElement, options);
                    // Ajustar wrapper para preencher o container
                    const wrapper = boardElement.querySelector('.chess-board-wrapper');
                    if (wrapper) {
                        wrapper.style.width = '100%';
                        wrapper.style.height = '100%';
                    }
                    // Guardar referência
                    this.boards.set(boardId, boardInstance);
                    // Expor adaptadores no próprio elemento <chess-board>
                    boardElement.setPosition = (fen) => {
                        try {
                            boardInstance.position(fen);
                        } catch (e) {
                            console.warn('🎯 setPosition falhou:', e);
                        }
                    };
                    boardElement.getPosition = () => {
                        try {
                            return boardInstance.position();
                        } catch {
                            return null;
                        }
                    };
                    boardElement.__boardInstance = boardInstance;
                    console.log(`🎯 Adaptador conectado: ${boardId} pronto para receber FEN da base Pro`);
                } catch (e) {
                    console.error('🎯 Erro ao criar instância ChessBoard via adaptador:', e);
                }
            }

            // Forçar inicialização se necessário
            if (boardElement.init) {
                boardElement.init();
            }

        } catch (error) {
            console.error(`🎯 Erro ao inicializar chess-board ${boardId}:`, error);
        }
    }

    /**
     * Inicializar div de tabuleiro
     */
    initializeBoardDiv(boardDiv, index) {
        const boardId = boardDiv.id || `board-div-${index}`;
        console.log(`🎯 Inicializando div de tabuleiro: ${boardId}`);

        try {
            // Verificar se já tem um tabuleiro
            if (boardDiv.querySelector('.chess-board-wrapper')) {
                console.log(`🎯 Tabuleiro ${boardId} já inicializado`);
                return;
            }

            // Criar tabuleiro usando nossa classe ChessBoard
            if (window.ChessBoard) {
                const options = {
                    position: 'start',
                    draggable: true,
                    dropOffBoard: 'snapback'
                };

                const board = new window.ChessBoard(boardDiv, options);
                this.boards.set(boardId, board);
                console.log(`🎯 Tabuleiro ${boardId} criado com sucesso`);
            } else {
                console.warn(`🎯 Classe ChessBoard não encontrada para ${boardId}`);
            }

        } catch (error) {
            console.error(`🎯 Erro ao inicializar div de tabuleiro ${boardId}:`, error);
        }
    }

    /**
     * Verificar status dos tabuleiros
     */
    checkBoardStatus() {
        console.log('🎯 Verificando status dos tabuleiros...');

        const totalBoards = this.boards.size;
        const chessBoardElements = document.querySelectorAll('chess-board').length;
        const boardDivs = document.querySelectorAll('#aeon-board, #narrative-board').length;

        console.log(`🎯 Status dos tabuleiros:`);
        console.log(`   - Total inicializados: ${totalBoards}`);
        console.log(`   - Elementos chess-board: ${chessBoardElements}`);
        console.log(`   - Divs de tabuleiro: ${boardDivs}`);

        if (totalBoards === 0) {
            console.warn('🎯 Nenhum tabuleiro foi inicializado!');
            this.showFallbackBoards();
        } else {
            console.log('🎯 Tabuleiros inicializados com sucesso!');
        }
    }

    /**
     * Mostrar tabuleiros de fallback se necessário
     */
    showFallbackBoards() {
        console.log('🎯 Criando tabuleiros de fallback...');

        // Criar tabuleiro de fallback para o hero
        const heroContainer = document.querySelector('.hero-chess-board');
        if (heroContainer && !heroContainer.querySelector('.chess-board-wrapper')) {
            try {
                if (window.ChessBoard) {
                    new window.ChessBoard(heroContainer, {
                        position: 'start',
                        draggable: true
                    });
                    console.log('🎯 Tabuleiro hero de fallback criado');
                }
            } catch (error) {
                console.error('🎯 Erro ao criar tabuleiro hero de fallback:', error);
            }
        }

        // Criar tabuleiro de fallback para o narrativo
        const narrativeContainer = document.querySelector('#narrative-board');
        if (narrativeContainer && !narrativeContainer.querySelector('.chess-board-wrapper')) {
            try {
                if (window.ChessBoard) {
                    new window.ChessBoard(narrativeContainer, {
                        position: 'start',
                        draggable: true
                    });
                    console.log('🎯 Tabuleiro narrativo de fallback criado');
                }
            } catch (error) {
                console.error('🎯 Erro ao criar tabuleiro narrativo de fallback:', error);
            }
        }
    }

    /**
     * Obter tabuleiro por ID
     */
    getBoard(boardId) {
        return this.boards.get(boardId);
    }

    /**
     * Obter todos os tabuleiros
     */
    getAllBoards() {
        return Array.from(this.boards.values());
    }

    /**
     * Verificar se tabuleiro está funcionando
     */
    isBoardWorking(boardId) {
        const board = this.boards.get(boardId);
        if (!board) return false;

        try {
            // Verificar se o tabuleiro responde
            return board && (board.position || board.game);
        } catch (error) {
            return false;
        }
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.BoardInitializer = BoardInitializer;

    // Inicializar automaticamente
    const boardInitializer = new BoardInitializer();
    boardInitializer.init();

    // Disponibilizar globalmente
    window.boardInitializer = boardInitializer;
}

// Log de inicialização