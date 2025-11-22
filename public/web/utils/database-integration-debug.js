/**
 * 🔍 Database Integration Debug - Verifica integração da base de dados
 */

class DatabaseIntegrationDebug {
    constructor() {
        this.name = 'Database Integration Debug';
        this.version = '1.0.0';
        
        console.log(`🔍 ${this.name} v${this.version} carregado`);
        this.init();
    }
    
    init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startDebug());
        } else {
            this.startDebug();
        }
    }
    
    startDebug() {
        console.log('🔍 Iniciando debug de integração da base de dados...');
        
        // Verificar imediatamente
        this.checkDatabaseIntegration();
        
        // Verificar periodicamente
        setInterval(() => {
            this.checkDatabaseIntegration();
        }, 5000);
    }
    
    checkDatabaseIntegration() {
        console.log('🔍 === VERIFICAÇÃO DE INTEGRAÇÃO DA BASE DE DADOS ===');
        
        // 1. Verificar se a base de dados está carregada
        this.checkDatabaseLoaded();
        
        // 2. Verificar se o Smart Chess Board está funcionando
        this.checkSmartChessBoard();
        
        // 3. Verificar se as posições estão sendo carregadas
        this.checkPositionsLoading();
        
        // 4. Verificar se o tabuleiro está recebendo as posições
        this.checkBoardIntegration();
        
        console.log('🔍 === FIM DA VERIFICAÇÃO ===');
    }
    
    checkDatabaseLoaded() {
        console.log('🔍 1. Verificando base de dados...');
        
        if (window.chessProDB) {
            const stats = window.chessProDB.getStatistics();
            console.log('✅ Base de dados carregada:', stats);
            
            // Verificar categorias
            const categories = ['openings', 'tacticalPatterns', 'classicEndgames', 'aiAnalysis', 'historicalPositions'];
            categories.forEach(category => {
                if (window.chessProDB[category]) {
                    console.log(`✅ Categoria ${category}: ${window.chessProDB[category].total} posições`);
                } else {
                    console.log(`❌ Categoria ${category}: não encontrada`);
                }
            });
        } else {
            console.log('❌ Base de dados não encontrada (window.chessProDB)');
        }
    }
    
    checkSmartChessBoard() {
        console.log('🔍 2. Verificando Smart Chess Board...');
        
        if (window.smartChessBoard) {
            const status = window.smartChessBoard.getStatus();
            console.log('✅ Smart Chess Board:', status);
            
            // Verificar se tem posições carregadas
            if (status.totalPositions > 0) {
                console.log(`✅ ${status.totalPositions} posições carregadas`);
            } else {
                console.log('❌ Nenhuma posição carregada');
            }
            
            // Verificar categoria atual
            if (status.currentCategory) {
                console.log(`✅ Categoria atual: ${status.currentCategory}`);
            } else {
                console.log('❌ Nenhuma categoria definida');
            }
        } else {
            console.log('❌ Smart Chess Board não encontrado (window.smartChessBoard)');
        }
    }
    
    checkPositionsLoading() {
        console.log('🔍 3. Verificando carregamento de posições...');
        
        if (window.smartChessBoard && window.smartChessBoard.positionHistory) {
            const positions = window.smartChessBoard.positionHistory;
            console.log(`✅ ${positions.length} posições no histórico`);
            
            if (positions.length > 0) {
                const firstPosition = positions[0];
                console.log('✅ Primeira posição:', {
                    name: firstPosition.name,
                    fen: firstPosition.fen,
                    evaluation: firstPosition.evaluation,
                    themes: firstPosition.themes
                });
            }
        } else {
            console.log('❌ Histórico de posições não encontrado');
        }
    }
    
    checkBoardIntegration() {
        console.log('🔍 4. Verificando integração com o tabuleiro...');
        
        const aeonBoard = document.querySelector('#aeon-board');
        if (aeonBoard) {
            console.log('✅ Tabuleiro #aeon-board encontrado');
            
            // Verificar se tem métodos de posição
            if (aeonBoard.setPosition) {
                console.log('✅ Método setPosition disponível');
            } else {
                console.log('❌ Método setPosition não encontrado');
            }
            
            if (aeonBoard.getPosition) {
                console.log('✅ Método getPosition disponível');
            } else {
                console.log('❌ Método getPosition não encontrado');
            }
            
            // Verificar posição atual
            try {
                const currentPosition = aeonBoard.getPosition ? aeonBoard.getPosition() : null;
                if (currentPosition) {
                    console.log('✅ Posição atual do tabuleiro:', currentPosition);
                } else {
                    console.log('⚠️ Posição atual não disponível');
                }
            } catch (error) {
                console.log('❌ Erro ao obter posição atual:', error);
            }
        } else {
            console.log('❌ Tabuleiro #aeon-board não encontrado');
        }
    }
    
    // Método para forçar carregamento de posições
    forceLoadPositions() {
        console.log('🔍 Forçando carregamento de posições...');
        
        if (window.smartChessBoard) {
            // Forçar carregamento de aberturas
            window.smartChessBoard.changeCategory('openings');
            
            // Aguardar um pouco e verificar
            setTimeout(() => {
                this.checkPositionsLoading();
                this.checkBoardIntegration();
            }, 1000);
        }
    }
    
    // Método para testar carregamento de posição específica
    testLoadPosition() {
        console.log('🔍 Testando carregamento de posição...');
        
        if (window.smartChessBoard && window.smartChessBoard.positionHistory.length > 0) {
            const position = window.smartChessBoard.positionHistory[0];
            console.log('🔍 Carregando posição de teste:', position);
            
            window.smartChessBoard.loadPosition(position);
        } else {
            console.log('❌ Nenhuma posição disponível para teste');
        }
    }
    
    // Método público para forçar verificação
    forceCheck() {
        console.log('🔍 Forçando verificação completa...');
        this.checkDatabaseIntegration();
    }
}

// Auto-inicialização
if (typeof window !== 'undefined') {
    window.DatabaseIntegrationDebug = DatabaseIntegrationDebug;
    window.databaseIntegrationDebug = new DatabaseIntegrationDebug();
}

console.log('🔍 Database Integration Debug carregado');

