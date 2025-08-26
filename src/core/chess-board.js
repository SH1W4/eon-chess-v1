// AEON CHESS Board - Mecânica idêntica ao chess.com
// Versão: 1.0 - Chess.com Clone

class ChessBoard {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            position: 'start',
            draggable: true,
            dropOffBoard: 'snapback',
            moveSpeed: 200,
            snapbackSpeed: 500,
            trashSpeed: 100,
            appearSpeed: 200,
            ...options
        };
        
        this.game = null;
        this.board = null;
        this.squareSize = 60;
        this.draggedPiece = null;
        this.sourceSquare = null;
        this.orientation = 'white';
        this.highlightedSquares = new Set();
        this.selectedSquare = null;
        
        this.init();
    }

    init() {
        this.createBoard();
        this.setupEventListeners();
        this.updatePosition();
    }

    createBoard() {
        // Limpar container
        this.container.innerHTML = '';
        
        // Criar wrapper do tabuleiro
        this.board = document.createElement('div');
        this.board.className = 'chess-board-wrapper';
        this.board.style.cssText = `
            width: ${this.squareSize * 8}px;
            height: ${this.squareSize * 8}px;
            position: relative;
            border: 2px solid #8b4513;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        `;
        
        // Criar grid do tabuleiro
        this.board.innerHTML = this.generateBoardHTML();
        
        this.container.appendChild(this.board);
        
        // Adicionar notação
        this.addNotation();
    }

    generateBoardHTML() {
        let html = '<div class="chess-board-grid" style="display: grid; grid-template-columns: repeat(8, 1fr); width: 100%; height: 100%;">';
        
        for (let rank = 7; rank >= 0; rank--) {
            for (let file = 0; file < 8; file++) {
                const square = this.getSquareName(file, rank);
                const isLight = (rank + file) % 2 === 0;
                const piece = this.getPieceAtSquare(square);
                
                html += `
                    <div class="chess-square ${isLight ? 'light' : 'dark'}" 
                         data-square="${square}"
                         style="
                            width: 100%;
                            height: 100%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            position: relative;
                            cursor: pointer;
                            transition: all 0.2s ease;
                            background-color: ${isLight ? '#f0d9b5' : '#b58863'};
                            color: ${isLight ? '#8b4513' : '#f0d9b5'};
                         "
                    >
                        ${piece ? `<div class="chess-piece" data-piece="${piece}" style="font-size: 2.5rem; user-select: none;">${this.getPieceSymbol(piece)}</div>` : ''}
                        <div class="square-highlight" style="
                            position: absolute;
                            top: 0;
                            left: 0;
                            right: 0;
                            bottom: 0;
                            opacity: 0;
                            transition: opacity 0.2s ease;
                            pointer-events: none;
                        "></div>
                    </div>
                `;
            }
        }
        
        html += '</div>';
        return html;
    }

    addNotation() {
        // Notação dos ranks (1-8)
        const rankNotation = document.createElement('div');
        rankNotation.className = 'rank-notation';
        rankNotation.style.cssText = `
            position: absolute;
            left: -20px;
            top: 0;
            bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            font-size: 12px;
            font-weight: bold;
            color: #666;
            pointer-events: none;
        `;
        
        for (let rank = 8; rank >= 1; rank--) {
            const rankElement = document.createElement('div');
            rankElement.textContent = rank;
            rankElement.style.cssText = `
                width: 20px;
                height: ${this.squareSize}px;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            rankNotation.appendChild(rankElement);
        }
        
        // Notação dos files (a-h)
        const fileNotation = document.createElement('div');
        fileNotation.className = 'file-notation';
        fileNotation.style.cssText = `
            position: absolute;
            bottom: -20px;
            left: 0;
            right: 0;
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: bold;
            color: #666;
            pointer-events: none;
        `;
        
        for (let file = 0; file < 8; file++) {
            const fileElement = document.createElement('div');
            fileElement.textContent = String.fromCharCode(97 + file);
            fileElement.style.cssText = `
                width: ${this.squareSize}px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            fileNotation.appendChild(fileElement);
        }
        
        this.board.appendChild(rankNotation);
        this.board.appendChild(fileNotation);
    }

    setupEventListeners() {
        // Mouse events para drag & drop
        this.board.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));
        
        // Touch events para mobile
        this.board.addEventListener('touchstart', this.handleTouchStart.bind(this));
        document.addEventListener('touchmove', this.handleTouchMove.bind(this));
        document.addEventListener('touchend', this.handleTouchEnd.bind(this));
        
        // Click events para seleção
        this.board.addEventListener('click', this.handleClick.bind(this));
    }

    handleMouseDown(e) {
        const square = e.target.closest('.chess-square');
        if (!square) return;
        
        const piece = square.querySelector('.chess-piece');
        if (!piece) return;
        
        this.startDrag(e, square, piece);
    }

    handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const square = document.elementFromPoint(touch.clientX, touch.clientY)?.closest('.chess-square');
        if (!square) return;
        
        const piece = square.querySelector('.chess-piece');
        if (!piece) return;
        
        this.startDrag(touch, square, piece);
    }

    startDrag(e, square, piece) {
        this.sourceSquare = square.dataset.square;
        this.draggedPiece = piece;
        
        // Criar elemento de drag
        this.dragElement = piece.cloneNode(true);
        this.dragElement.style.cssText = `
            position: fixed;
            pointer-events: none;
            z-index: 1000;
            font-size: 2.5rem;
            opacity: 0.8;
            transform: translate(-50%, -50%);
        `;
        
        document.body.appendChild(this.dragElement);
        
        // Esconder peça original
        piece.style.opacity = '0.3';
        
        // Atualizar posição do drag
        this.updateDragPosition(e);
        
        // Adicionar classe de drag
        document.body.classList.add('dragging');
    }

    handleMouseMove(e) {
        if (!this.draggedPiece) return;
        this.updateDragPosition(e);
    }

    handleTouchMove(e) {
        if (!this.draggedPiece) return;
        e.preventDefault();
        const touch = e.touches[0];
        this.updateDragPosition(touch);
    }

    updateDragPosition(e) {
        if (!this.dragElement) return;
        
        const rect = this.board.getBoundingClientRect();
        const x = e.clientX || e.touches[0].clientX;
        const y = e.clientY || e.touches[0].clientY;
        
        this.dragElement.style.left = x + 'px';
        this.dragElement.style.top = y + 'px';
        
        // Highlight do quadrado sob o mouse
        const square = document.elementFromPoint(x, y)?.closest('.chess-square');
        if (square) {
            this.highlightSquare(square.dataset.square, 'drag');
        }
    }

    handleMouseUp(e) {
        if (!this.draggedPiece) return;
        this.endDrag(e);
    }

    handleTouchEnd(e) {
        if (!this.draggedPiece) return;
        const touch = e.changedTouches[0];
        this.endDrag(touch);
    }

    endDrag(e) {
        if (!this.draggedPiece || !this.sourceSquare) return;
        
        const targetSquare = document.elementFromPoint(
            e.clientX || e.changedTouches[0].clientX,
            e.clientY || e.changedTouches[0].clientY
        )?.closest('.chess-square');
        
        if (targetSquare) {
            const targetSquareName = targetSquare.dataset.square;
            this.makeMove(this.sourceSquare, targetSquareName);
        } else {
            // Snapback se soltou fora do tabuleiro
            this.snapback();
        }
        
        this.cleanupDrag();
    }

    handleClick(e) {
        const square = e.target.closest('.chess-square');
        if (!square) return;
        
        const squareName = square.dataset.square;
        const piece = square.querySelector('.chess-piece');
        
        if (this.selectedSquare) {
            if (this.selectedSquare === squareName) {
                // Desselecionar
                this.clearSelection();
            } else if (piece) {
                // Selecionar nova peça
                this.selectSquare(squareName);
            } else {
                // Tentar mover para quadrado vazio
                this.makeMove(this.selectedSquare, squareName);
            }
        } else if (piece) {
            // Selecionar peça
            this.selectSquare(squareName);
        }
    }

    selectSquare(squareName) {
        this.clearSelection();
        this.selectedSquare = squareName;
        this.highlightSquare(squareName, 'selected');
        
        // Mostrar movimentos possíveis
        if (this.game) {
            const moves = this.game.moves({ square: squareName, verbose: true });
            moves.forEach(move => {
                this.highlightSquare(move.to, 'move');
            });
        }
    }

    clearSelection() {
        this.selectedSquare = null;
        this.clearHighlights();
    }

    highlightSquare(squareName, type) {
        const square = this.board.querySelector(`[data-square="${squareName}"]`);
        if (!square) return;
        
        const highlight = square.querySelector('.square-highlight');
        if (!highlight) return;
        
        let color = '';
        switch (type) {
            case 'selected':
                color = 'rgba(123, 97, 255, 0.8)';
                break;
            case 'move':
                color = 'rgba(123, 97, 255, 0.4)';
                break;
            case 'capture':
                color = 'rgba(255, 97, 97, 0.4)';
                break;
            case 'check':
                color = 'rgba(255, 0, 0, 0.8)';
                break;
            case 'drag':
                color = 'rgba(123, 97, 255, 0.6)';
                break;
        }
        
        highlight.style.backgroundColor = color;
        highlight.style.opacity = '1';
        this.highlightedSquares.add(squareName);
    }

    clearHighlights() {
        this.highlightedSquares.forEach(squareName => {
            const square = this.board.querySelector(`[data-square="${squareName}"]`);
            if (square) {
                const highlight = square.querySelector('.square-highlight');
                if (highlight) {
                    highlight.style.opacity = '0';
                }
            }
        });
        this.highlightedSquares.clear();
    }

    makeMove(from, to) {
        if (!this.game) return false;
        
        const move = this.game.move({ from, to, promotion: 'q' });
        if (move) {
            this.updatePosition();
            this.clearSelection();
            
            // Trigger move event
            if (this.options.onMove) {
                this.options.onMove(move, this.game.fen());
            }
            
            return true;
        }
        
        return false;
    }

    snapback() {
        if (this.draggedPiece) {
            this.draggedPiece.style.opacity = '1';
        }
    }

    cleanupDrag() {
        if (this.dragElement) {
            document.body.removeChild(this.dragElement);
            this.dragElement = null;
        }
        
        if (this.draggedPiece) {
            this.draggedPiece.style.opacity = '1';
            this.draggedPiece = null;
        }
        
        this.sourceSquare = null;
        document.body.classList.remove('dragging');
        this.clearHighlights();
    }

    updatePosition() {
        if (!this.game) return;
        
        const fen = this.game.fen().split(' ')[0];
        let rank = 7;
        let file = 0;
        
        for (let char of fen) {
            if (char === '/') {
                rank--;
                file = 0;
                continue;
            }
            
            if (!isNaN(Number(char))) {
                file += parseInt(char);
                continue;
            }
            
            const square = this.getSquareName(file, rank);
            const squareElement = this.board.querySelector(`[data-square="${square}"]`);
            
            if (squareElement) {
                const pieceContainer = squareElement.querySelector('.chess-piece');
                if (pieceContainer) {
                    pieceContainer.remove();
                }
                
                if (char !== ' ') {
                    const pieceElement = document.createElement('div');
                    pieceElement.className = 'chess-piece';
                    pieceElement.dataset.piece = char;
                    pieceElement.style.cssText = 'font-size: 2.5rem; user-select: none;';
                    pieceElement.textContent = this.getPieceSymbol(char);
                    squareElement.appendChild(pieceElement);
                }
            }
            
            file++;
        }
    }

    getSquareName(file, rank) {
        return String.fromCharCode(97 + file) + (rank + 1);
    }

    getPieceAtSquare(square) {
        if (!this.game) return null;
        const piece = this.game.get(square);
        if (!piece) return null;
        
        const color = piece.color === 'w' ? 'white' : 'black';
        const type = piece.type;
        return color + type;
    }

    getPieceSymbol(piece) {
        const symbols = {
            'whiteking': '♔',
            'whitequeen': '♕',
            'whiterook': '♖',
            'whitebishop': '♗',
            'whiteknight': '♘',
            'whitepawn': '♙',
            'blackking': '♚',
            'blackqueen': '♛',
            'blackrook': '♜',
            'blackbishop': '♝',
            'blackknight': '♞',
            'blackpawn': '♟'
        };
        
        return symbols[piece] || piece;
    }

    // API Methods
    position(fen = null) {
        if (fen) {
            if (!this.game) {
                this.game = new Chess(fen);
            } else {
                this.game.load(fen);
            }
            this.updatePosition();
        } else {
            return this.game ? this.game.fen() : 'start';
        }
    }

    move(move) {
        if (!this.game) return null;
        const result = this.game.move(move);
        if (result) {
            this.updatePosition();
        }
        return result;
    }

    undo() {
        if (!this.game) return null;
        const result = this.game.undo();
        if (result) {
            this.updatePosition();
        }
        return result;
    }

    reset() {
        if (this.game) {
            this.game.reset();
            this.updatePosition();
        }
    }

    clear() {
        if (this.game) {
            this.game.clear();
            this.updatePosition();
        }
    }

    destroy() {
        // Cleanup event listeners
        document.removeEventListener('mousemove', this.handleMouseMove.bind(this));
        document.removeEventListener('mouseup', this.handleMouseUp.bind(this));
        document.removeEventListener('touchmove', this.handleTouchMove.bind(this));
        document.removeEventListener('touchend', this.handleTouchEnd.bind(this));
        
        // Remove board
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}

// Export for global use
window.ChessBoard = ChessBoard;
