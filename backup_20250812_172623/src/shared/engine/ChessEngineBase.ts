import { Chess } from 'chess.js';
import { 
  ChessEngine, 
  EngineOptions, 
  EngineAnalysis,
  EngineEvent,
  HealthStatus
} from '../types/engine';
import { 
  ChessPosition, 
  ChessPiece, 
  ChessMove,
  PieceType
} from '../types/chess';
import { ArquimaxMonitor } from './monitoring/ArquimaxMonitor';
import { INITIAL_FEN } from '../constants/game';
import { EventEmitter } from 'events';

/**
 * Implementação base do motor de xadrez.
 * 
 * Esta classe fornece a funcionalidade central para um motor de xadrez,
 * incluindo gerenciamento de estado do jogo, validação de movimentos,
 * avaliação de posição e eventos do jogo.
 * 
 * @implements {ChessEngine}
 */
export class ChessEngineBase implements ChessEngine {
  /** Instância do chess.js que gerencia as regras e estado do jogo */
  protected game: Chess;

  /** Opções de configuração do motor */
  protected options: EngineOptions;

  /** Emissor de eventos para notificar mudanças no estado do jogo */
  protected eventEmitter: EventEmitter;

  /** Cache de análises de posição para otimização */
  protected positionCache: Map<string, EngineAnalysis>;

  private monitor: ArquimaxMonitor;

  /**
   * Cria uma nova instância do motor de xadrez.
   * 
   * @param options - Opções de configuração do motor
   * @param options.startPosition - Posição inicial em notação FEN (opcional)
   * @param options.evaluationParameters - Parâmetros para avaliação de posição (opcional)
   */
  constructor(options: EngineOptions = {}) {
    this.game = new Chess(options.startPosition || INITIAL_FEN);
    this.options = options;
    this.eventEmitter = new EventEmitter();
    this.positionCache = new Map();
    this.monitor = new ArquimaxMonitor();
  }

  // Estado do jogo
  /**
   * Obtém a representação atual do tabuleiro.
   * 
   * @returns Uma matriz 8x8 representando o tabuleiro, onde cada elemento
   * é uma peça de xadrez ou null para casas vazias.
   */
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

  /**
   * Obtém a posição atual em notação FEN.
   * 
   * @returns String FEN representando o estado atual do jogo
   */
  getFEN(): string {
    return this.game.fen();
  }

  /**
   * Define uma nova posição para o jogo usando notação FEN.
   * 
   * @param fen - String FEN representando a nova posição
   * @throws {Error} Se a string FEN for inválida
   * @emits {POSITION_CHANGED} Quando a posição é alterada com sucesso
   */
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
  /**
   * Obtém todos os movimentos legais possíveis para uma peça em uma determinada posição.
   * 
   * @param position - Posição da peça no tabuleiro
   * @returns Lista de movimentos legais possíveis
   */
  getPossibleMoves(position: ChessPosition): ChessMove[] {
    try {
      const square = this.positionToSquare(position);
      const fen = this.getFEN();
      const cacheKey = `${fen}:${square}`;
      const cacheHit = this.positionCache.has(cacheKey);
      
      let moves;
      if (cacheHit) {
        const cache = this.positionCache.get(cacheKey);
        moves = cache!.bestLine;
      } else {
        moves = this.game.moves({ 
          square,
          verbose: true 
        });
        // Cache the result
        this.positionCache.set(cacheKey, {
          evaluation: 0,
          depth: 0,
          bestLine: moves,
          threats: [],
          positionalFeatures: {
            pawnStructure: 0,
            kingSafety: 0,
            mobility: 0,
            centerControl: 0,
            pieceActivity: 0
          }
        });
      }
      
      this.monitor.recordCacheAccess(cacheHit);

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

  /**
   * Executa um movimento no tabuleiro.
   * 
   * @param from - Posição inicial da peça
   * @param to - Posição final da peça
   * @returns true se o movimento foi executado com sucesso, false caso contrário
   * @emits {MOVE_MADE} Quando um movimento é realizado com sucesso
   * @emits {CHECK} Quando o movimento resulta em xeque
   * @emits {GAME_OVER} Quando o movimento resulta em fim de jogo
   */
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

  /**
   * Desfaz o último movimento realizado.
   * 
   * @returns true se havia um movimento para desfazer, false caso contrário
   * @emits {POSITION_CHANGED} Quando o movimento é desfeito com sucesso
   */
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
  /**
   * Verifica se o jogador atual está em xeque.
   * 
   * @returns true se o jogador atual está em xeque, false caso contrário
   */
  isCheck(): boolean {
    return this.game.isCheck();
  }

  /**
   * Verifica se o jogador atual está em xeque-mate.
   * 
   * @returns true se o jogador atual está em xeque-mate, false caso contrário
   */
  isCheckmate(): boolean {
    return this.game.isCheckmate();
  }

  /**
   * Verifica se o jogo está empatado.
   * 
   * @returns true se o jogo está empatado, false caso contrário
   */
  isDraw(): boolean {
    return this.game.isDraw();
  }

  /**
   * Verifica se o jogo terminou (xeque-mate ou empate).
   * 
   * @returns true se o jogo terminou, false caso contrário
   */
  isGameOver(): boolean {
    return this.game.isGameOver();
  }

  /**
   * Obtém o jogador atual.
   * 
   * @returns 'white' para as brancas, 'black' para as pretas
   */
  getCurrentPlayer(): 'white' | 'black' {
    const turn = this.game.turn();
    return turn === 'w' ? 'white' : 'black';
  }

  // Avaliação e análise
  /**
   * Avalia a posição atual do jogo.
   * 
   * Esta função considera diversos fatores para avaliar a posição:
   * - Material: Valor das peças presentes no tabuleiro
   * - Posição: Qualidade do posicionamento das peças
   * - Mobilidade: Quantidade de movimentos disponíveis
   * - Segurança do Rei: Avaliação da proteção do rei
   * - Estrutura de Peões: Qualidade da estrutura de peões
   * 
   * @returns Um número que representa a avaliação da posição.
   * Valores positivos favorecem as brancas, negativos favorecem as pretas.
   */
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

  /**
   * Encontra o melhor movimento possível para o jogador atual.
   * 
   * @param depth - Profundidade máxima de busca na árvore de movimentos
   * @returns O melhor movimento encontrado, ou null se nenhum movimento for possível
   * @todo Implementar algoritmo minimax com poda alpha-beta
   */
  getBestMove(depth: number): ChessMove | null {
    // TODO: Implementar busca minimax com poda alpha-beta
    return null;
  }

  /**
   * Obtém o histórico completo de movimentos do jogo.
   * 
   * @returns Lista de movimentos realizados desde o início do jogo
   */
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
  /**
   * Verifica se um movimento é válido sem executá-lo.
   * 
   * @param from - Posição inicial da peça
   * @param to - Posição final da peça
   * @returns true se o movimento é legal, false caso contrário
   */
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

  /**
   * Verifica se uma posição está dentro dos limites do tabuleiro.
   * 
   * @param position - Posição a ser verificada
   * @returns true se a posição é válida, false caso contrário
   */
  isValidPosition(position: ChessPosition): boolean {
    return position.row >= 0 && position.row < 8 &&
           position.col >= 0 && position.col < 8;
  }

  // Utilidades
  /**
   * Reinicia o jogo para a posição inicial.
   * 
   * @emits {POSITION_CHANGED} Quando o tabuleiro é reiniciado
   */
  reset(): void {
    this.game.reset();
    this.positionCache.clear();
    this.emitEvent({ 
      type: 'POSITION_CHANGED',
      fen: this.getFEN()
    });
  }

  /**
   * Cria uma cópia independente do motor de xadrez atual.
   * 
   * @returns Uma nova instância do motor com o mesmo estado atual
   */
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

  /**
   * Verifica o status de saúde do motor.
   * 
   * @returns Status atual do motor incluindo métricas de desempenho
   */
  public checkHealth(): HealthStatus {
    return this.monitor.checkHealth();
  }

  /**
   * Emite um evento do motor.
   * 
   * @param event - Evento a ser emitido
   */
  protected emitEvent(event: EngineEvent): void {
    this.eventEmitter.emit('engine-event', event);
    this.monitor.recordEvent(event);
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
