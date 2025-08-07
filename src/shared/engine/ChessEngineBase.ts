import { Chess } from 'chess.js';
import { 
  ChessEngine, 
  EngineOptions, 
  EngineAnalysis,
  EngineEvent 
} from '../types/engine';
import { 
  ChessPosition, 
  ChessPiece, 
  ChessMove,
  PieceType
} from '../types/chess';
import { INITIAL_FEN } from '../constants/game';
import { EventEmitter } from 'events';

export class ChessEngineBase implements ChessEngine {
  protected game: Chess;
  protected options: EngineOptions;
  protected eventEmitter: EventEmitter;
  protected positionCache: Map<string, EngineAnalysis>;

  constructor(options: EngineOptions = {}) {
    this.game = new Chess(options.startPosition || INITIAL_FEN);
    this.options = options;
    this.eventEmitter = new EventEmitter();
    this.positionCache = new Map();
  }

  // Estado do jogo
  getBoard(): ChessPiece[][] {
    const board = this.game.board();
    return board.map(row => 
      row.map(square => 
        square ? {
          type: square.type as PieceType,
          color: square.color === 'w' ? 'white' : 'black'
        } : null
      )
    );
  }

  getFEN(): string {
    return this.game.fen();
  }

  setFEN(fen: string): void {
    try {
      // Na nova versão do chess.js, load() já valida o FEN
      this.game.load(fen);
      this.emitEvent({ 
        type: 'POSITION_CHANGED', 
        fen 
      });
    } catch (e) {
      throw new Error('Invalid FEN string');
    }
  }

  // Movimentos
  getPossibleMoves(position: ChessPosition): ChessMove[] {
    try {
      const moves = this.game.moves({ 
        square: this.positionToSquare(position),
        verbose: true 
      });

      return moves.map(move => ({
        from: this.squareToPosition(move.from),
        to: this.squareToPosition(move.to),
        piece: {
          type: move.piece as PieceType,
          color: move.color === 'w' ? 'white' : 'black'
        },
        captured: move.captured ? {
          type: move.captured as PieceType,
          color: move.color === 'w' ? 'black' : 'white'
        } : undefined,
        promotion: move.promotion as PieceType | undefined,
      }));
    } catch (e) {
      // Se houver erro na geração de movimentos, retorna lista vazia
      return [];
    }
  }

  makeMove(from: ChessPosition, to: ChessPosition): boolean {
    try {
      const move = this.game.move({
        from: this.positionToSquare(from),
        to: this.positionToSquare(to),
        promotion: 'q' // Auto-promove para rainha por padrão
      });

      if (move) {
        const chessMove: ChessMove = {
          from,
          to,
          piece: {
            type: move.piece,
            color: move.color === 'w' ? 'white' : 'black'
          },
          captured: move.captured ? {
            type: move.captured,
            color: move.color === 'w' ? 'black' : 'white'
          } : undefined,
          promotion: move.promotion,
        };

        this.emitEvent({ type: 'MOVE_MADE', move: chessMove });

        if (this.isCheck()) {
          this.emitEvent({ 
            type: 'CHECK',
            kingPosition: this.findKing(this.getCurrentPlayer())
          });
        }

        if (this.isGameOver()) {
          let result = 'draw';
          if (this.isCheckmate()) {
            result = this.getCurrentPlayer() === 'white' ? 'black' : 'white';
          }
          this.emitEvent({ type: 'GAME_OVER', result });
        }

        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  undoLastMove(): boolean {
    const move = this.game.undo();
    if (move) {
      this.emitEvent({ 
        type: 'POSITION_CHANGED',
        fen: this.getFEN()
      });
      return true;
    }
    return false;
  }

  // Estado do jogo
  isCheck(): boolean {
    return this.game.isCheck();
  }

  isCheckmate(): boolean {
    return this.game.isCheckmate();
  }

  isDraw(): boolean {
    return this.game.isDraw();
  }

  isGameOver(): boolean {
    return this.game.isGameOver();
  }

  getCurrentPlayer(): 'white' | 'black' {
    const turn = this.game.turn();
    return turn === 'w' ? 'white' : 'black';
  }

  // Avaliação e análise
  evaluatePosition(): number {
    // Implementação básica de avaliação
    const weights = this.options.evaluationParameters || {
      materialWeight: 1,
      positionWeight: 0.1,
      mobilityWeight: 0.1,
      kingSafetyWeight: 0.2,
      pawnStructureWeight: 0.1
    };

    let score = 0;

    // Material
    score += this.evaluateMaterial() * weights.materialWeight;

    // Posição das peças
    score += this.evaluatePiecePositions() * weights.positionWeight;

    // Mobilidade
    score += this.evaluateMobility() * weights.mobilityWeight;

    // Segurança do rei
    score += this.evaluateKingSafety() * weights.kingSafetyWeight;

    // Estrutura de peões
    score += this.evaluatePawnStructure() * weights.pawnStructureWeight;

    return score;
  }

  private evaluatePiecePositions(): number {
    // Simple piece-square tables evaluation
    const pieceSquareValues = {
      p: [ // Pawns
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
      ],
      n: [ // Knights
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
      ],
      b: [ // Bishops
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
      ]
    };

    let score = 0;
    const board = this.game.board();

    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece) {
          const pieceTable = pieceSquareValues[piece.type as keyof typeof pieceSquareValues];
          if (pieceTable) {
            const positionValue = pieceTable[piece.color === 'w' ? row : 7 - row][col];
            score += piece.color === 'w' ? positionValue : -positionValue;
          }
        }
      }
    }

    return score;
  }

  getBestMove(depth: number): ChessMove | null {
    // TODO: Implementar busca minimax com poda alpha-beta
    return null;
  }

  getGameHistory(): ChessMove[] {
    return this.game.history({ verbose: true }).map(move => ({
      from: this.squareToPosition(move.from),
      to: this.squareToPosition(move.to),
      piece: {
        type: move.piece,
        color: move.color === 'w' ? 'white' : 'black'
      },
      captured: move.captured ? {
        type: move.captured,
        color: move.color === 'w' ? 'black' : 'white'
      } : undefined,
      promotion: move.promotion,
    }));
  }

  // Validação
  isValidMove(from: ChessPosition, to: ChessPosition): boolean {
    // Validação básica de posição
    if (!this.isValidPosition(from) || !this.isValidPosition(to)) {
      return false;
    }

    // Verifica se a peça pertence ao jogador atual
    const piece = this.game.board()[from.row][from.col];
    if (!piece || piece.color !== (this.getCurrentPlayer() === 'white' ? 'w' : 'b')) {
      return false;
    }

    // Tenta fazer o movimento no chess.js
    try {
      const move = this.game.move({
        from: this.positionToSquare(from),
        to: this.positionToSquare(to),
        promotion: 'q'
      });

      if (move) {
        // Desfaz o movimento para manter o estado original
        this.game.undo();
        return true;
      }
    } catch (e) {
      // Ignora erros do chess.js
    }

    return false;
  }

  isValidPosition(position: ChessPosition): boolean {
    return position.row >= 0 && position.row < 8 &&
           position.col >= 0 && position.col < 8;
  }

  // Utilidades
  reset(): void {
    this.game.reset();
    this.positionCache.clear();
    this.emitEvent({ 
      type: 'POSITION_CHANGED',
      fen: this.getFEN()
    });
  }

  clone(): ChessEngine {
    const clonedEngine = new ChessEngineBase(this.options);
    clonedEngine.setFEN(this.getFEN());
    return clonedEngine;
  }

  // Métodos protegidos auxiliares
  protected positionToSquare(position: ChessPosition): string {
    const file = String.fromCharCode('a'.charCodeAt(0) + position.col);
    const rank = 8 - position.row;
    return `${file}${rank}`;
  }

  protected squareToPosition(square: string): ChessPosition {
    const col = square.charCodeAt(0) - 'a'.charCodeAt(0);
    const row = 8 - parseInt(square[1]);
    return { row, col };
  }

  protected findKing(color: 'white' | 'black'): ChessPosition {
    const board = this.game.board();
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece && 
            piece.type === 'k' && 
            piece.color === (color === 'white' ? 'w' : 'b')) {
          return { row, col };
        }
      }
    }
    throw new Error('King not found');
  }

  protected emitEvent(event: EngineEvent): void {
    this.eventEmitter.emit('engine-event', event);
  }

  // Métodos de avaliação
  private evaluateMaterial(): number {
    const pieceValues = {
      p: 1,
      n: 3,
      b: 3,
      r: 5,
      q: 9,
      k: 0
    };

    let score = 0;
    const board = this.game.board();

    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = board[row][col];
        if (piece) {
          const value = pieceValues[piece.type as keyof typeof pieceValues];
          score += piece.color === 'w' ? value : -value;
        }
      }
    }

    return score;
  }

  private evaluateMobility(): number {
    const whiteMoves = this.game.moves().length;
    // Clona o jogo para ver os movimentos do oponente
    const tempGame = new Chess(this.game.fen());
    tempGame.load(this.game.fen().replace(' w ', ' b '));
    const blackMoves = tempGame.moves().length;
    
    return whiteMoves - blackMoves;
  }

  private evaluateKingSafety(): number {
    // TODO: Implementar avaliação de segurança do rei
    return 0;
  }

  private evaluatePawnStructure(): number {
    // TODO: Implementar avaliação de estrutura de peões
    return 0;
  }

  // Event handlers
  on(eventName: string, handler: (event: EngineEvent) => void): void {
    this.eventEmitter.on(eventName, handler);
  }

  off(eventName: string, handler: (event: EngineEvent) => void): void {
    this.eventEmitter.off(eventName, handler);
  }
}
