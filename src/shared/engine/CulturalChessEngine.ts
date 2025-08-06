import { ChessEngineBase } from './ChessEngineBase';
import { CulturalEngineExtension, EngineOptions } from '../types/engine';
import { ChessMove } from '../types/chess';
import { CULTURAL_STYLES, CULTURAL_EVENTS } from '../constants/game';

export class CulturalChessEngine extends ChessEngineBase implements CulturalEngineExtension {
  private currentStyle: string;
  private culturalEvents: {
    type: string;
    timestamp: number;
    description: string;
  }[];
  private playStyleHistory: ChessMove[];

  constructor(options: EngineOptions = {}) {
    super(options);
    this.currentStyle = 'modern';
    this.culturalEvents = [];
    this.playStyleHistory = [];

    // Registra movimentos para análise de estilo
    this.on('engine-event', (event) => {
      if (event.type === 'MOVE_MADE') {
        this.playStyleHistory.push(event.move);
        this.analyzeMoveStyle(event.move);
      }
    });
  }

  // Implementação da interface CulturalEngineExtension
  setCulturalStyle(style: string): void {
    if (!(style in CULTURAL_STYLES)) {
      throw new Error(`Estilo cultural inválido: ${style}`);
    }
    this.currentStyle = style;
    this.triggerCulturalEvent('STYLE_CHANGED');
  }

  getCulturalNarrative(): string[] {
    const narratives: string[] = [];
    const recentMoves = this.playStyleHistory.slice(-5);
    const styleAnalysis = this.analyzePlayStyle();

    // Narrativa baseada no estilo dominante
    narratives.push(
      `Seu jogo reflete o estilo ${styleAnalysis.dominantStyle}, ` +
      `com ênfase em ${this.getStyleCharacteristics(styleAnalysis.dominantStyle)}.`
    );

    // Narrativa baseada nos movimentos recentes
    if (recentMoves.length > 0) {
      const recentStyle = this.analyzeMoveSequence(recentMoves);
      narratives.push(
        `Nos últimos movimentos, você demonstrou uma tendência a ` +
        `${this.getStyleTendency(recentStyle)}.`
      );
    }

    // Narrativa cultural específica
    narratives.push(this.getCulturalStyleNarrative());

    return narratives;
  }

  getStyleBasedEvaluation(): {
    style: string;
    evaluation: number;
    explanation: string;
  } {
    const baseEvaluation = super.evaluatePosition();
    const styleModifier = this.getStyleModifier();
    const modifiedEvaluation = baseEvaluation * styleModifier;

    return {
      style: this.currentStyle,
      evaluation: modifiedEvaluation,
      explanation: this.getStyleEvaluation()
    };
  }

  triggerCulturalEvent(type: string): void {
    if (!(type in CULTURAL_EVENTS)) {
      throw new Error(`Tipo de evento cultural inválido: ${type}`);
    }

    const event = {
      type,
      timestamp: Date.now(),
      description: this.getEventDescription(type)
    };

    this.culturalEvents.push(event);
    this.emitEvent({
      type: 'CULTURAL_EVENT',
      event: {
        type: event.type,
        description: event.description
      }
    });
  }

  getCulturalEventHistory(): {
    type: string;
    timestamp: number;
    description: string;
  }[] {
    return [...this.culturalEvents];
  }

  analyzePlayStyle(): {
    dominantStyle: string;
    styleMetrics: Record<string, number>;
    recommendations: string[];
  } {
    const metrics = this.calculateStyleMetrics();
    const dominantStyle = this.findDominantStyle(metrics);
    const recommendations = this.generateRecommendations(metrics);

    return {
      dominantStyle,
      styleMetrics: metrics,
      recommendations
    };
  }

  // Métodos auxiliares privados
  private analyzeMoveStyle(move: ChessMove): void {
    const isAggressive = this.isAggressiveMove(move);
    const isPositional = this.isPositionalMove(move);
    const isTactical = this.isTacticalMove(move);

    if (isAggressive) {
      this.triggerCulturalEvent('AGGRESSIVE_MOVE');
    } else if (isPositional) {
      this.triggerCulturalEvent('POSITIONAL_MOVE');
    } else if (isTactical) {
      this.triggerCulturalEvent('TACTICAL_MOVE');
    }
  }

  private analyzeMoveSequence(moves: ChessMove[]): string {
    let aggressiveCount = 0;
    let positionalCount = 0;
    let tacticalCount = 0;

    moves.forEach(move => {
      if (this.isAggressiveMove(move)) aggressiveCount++;
      if (this.isPositionalMove(move)) positionalCount++;
      if (this.isTacticalMove(move)) tacticalCount++;
    });

    const total = moves.length;
    const scores = {
      aggressive: aggressiveCount / total,
      positional: positionalCount / total,
      tactical: tacticalCount / total
    };

    return Object.entries(scores)
      .reduce((a, b) => a[1] > b[1] ? a : b)[0];
  }

  private isAggressiveMove(move: ChessMove): boolean {
    return Boolean(
      move.captured || // Captura
      this.isCheck() || // Xeque
      this.isAttackingCenterPieces(move) // Ataque ao centro
    );
  }

  private isPositionalMove(move: ChessMove): boolean {
    return Boolean(
      this.improvesPosition(move) ||
      this.controlsImportantSquares(move) ||
      this.improvesPawnStructure(move)
    );
  }

  private isTacticalMove(move: ChessMove): boolean {
    return Boolean(
      this.createsThreat(move) ||
      this.createsFork(move) ||
      this.createsPin(move)
    );
  }

  private calculateStyleMetrics(): Record<string, number> {
    const metrics: Record<string, number> = {
      aggressive: 0,
      defensive: 0,
      positional: 0,
      tactical: 0
    };

    this.playStyleHistory.forEach(move => {
      if (this.isAggressiveMove(move)) metrics.aggressive++;
      if (this.isPositionalMove(move)) metrics.positional++;
      if (this.isTacticalMove(move)) metrics.tactical++;
      // Movimento defensivo é calculado de forma diferente
      if (this.isDefensiveMove(move)) metrics.defensive++;
    });

    // Normaliza as métricas
    const total = Object.values(metrics).reduce((a, b) => a + b, 0);
    if (total > 0) {
      Object.keys(metrics).forEach(key => {
        metrics[key] = metrics[key] / total;
      });
    }

    return metrics;
  }

  private findDominantStyle(metrics: Record<string, number>): string {
    return Object.entries(metrics)
      .reduce((a, b) => a[1] > b[1] ? a : b)[0];
  }

  private generateRecommendations(metrics: Record<string, number>): string[] {
    const recommendations: string[] = [];
    const dominantStyle = this.findDominantStyle(metrics);

    // Recomendações baseadas no estilo dominante
    recommendations.push(
      `Continue explorando seu estilo ${dominantStyle}, mas considere também:`
    );

    // Recomendações para equilibrar o jogo
    Object.entries(metrics)
      .filter(([style]) => style !== dominantStyle)
      .sort(([,a], [,b]) => a - b)
      .forEach(([style, value]) => {
        if (value < 0.2) {
          recommendations.push(
            this.getStyleRecommendation(style as keyof typeof metrics)
          );
        }
      });

    return recommendations;
  }

  private getStyleModifier(): number {
    // Modifica a avaliação baseada no estilo cultural
    const modifiers: Record<string, number> = {
      medieval: 1.1, // Valoriza material e posição
      renaissance: 1.2, // Valoriza mobilidade e desenvolvimento
      modern: 1.0, // Balanceado
      ancient: 0.9 // Valoriza sacrifícios e ataques
    };

    return modifiers[this.currentStyle] || 1.0;
  }

  private getStyleEvaluation(): string {
    const evaluation = super.evaluatePosition();
    const style = this.currentStyle;

    switch (style) {
      case 'medieval':
        return evaluation > 0
          ? 'Vantagem material e posicional sólida'
          : 'Necessidade de consolidar posição e material';
      case 'renaissance':
        return evaluation > 0
          ? 'Excelente desenvolvimento e mobilidade'
          : 'Oportunidade para melhorar desenvolvimento';
      case 'modern':
        return evaluation > 0
          ? 'Posição equilibrada com vantagem'
          : 'Posição requer atenção estratégica';
      case 'ancient':
        return evaluation > 0
          ? 'Potencial para sacrifícios decisivos'
          : 'Momento para sacrifícios táticos';
      default:
        return 'Avaliação padrão da posição';
    }
  }

  private getStyleCharacteristics(style: string): string {
    const characteristics: Record<string, string> = {
      aggressive: 'ataques diretos e sacrifícios',
      defensive: 'sólida estrutura defensiva',
      positional: 'controle posicional e estratégico',
      tactical: 'combinações e táticas complexas'
    };

    return characteristics[style] || 'estilo equilibrado';
  }

  private getStyleTendency(style: string): string {
    const tendencies: Record<string, string> = {
      aggressive: 'buscar iniciativas de ataque',
      defensive: 'fortalecer sua posição',
      positional: 'controlar pontos estratégicos',
      tactical: 'criar ameaças táticas'
    };

    return tendencies[style] || 'manter um jogo equilibrado';
  }

  private getEventDescription(type: string): string {
    const descriptions: Record<string, string> = {
      AGGRESSIVE_MOVE: 'Movimento agressivo detectado',
      POSITIONAL_MOVE: 'Melhoria posicional significativa',
      TACTICAL_MOVE: 'Combinação tática identificada',
      STYLE_CHANGED: `Estilo alterado para ${this.currentStyle}`,
      BRILLIANT_MOVE: 'Movimento brilhante executado',
      CRITICAL_POSITION: 'Posição crítica alcançada'
    };

    return descriptions[type] || 'Evento cultural ocorrido';
  }

  private getCulturalStyleNarrative(): string {
    const narratives: Record<string, string> = {
      medieval: 'Seu jogo reflete a solidez e tradição do xadrez medieval.',
      renaissance: 'Você demonstra a criatividade e inovação do período renascentista.',
      modern: 'Seu estilo incorpora princípios modernos de flexibilidade e pragmatismo.',
      ancient: 'Sua abordagem evoca a sabedoria e profundidade do xadrez antigo.'
    };

    return narratives[this.currentStyle] || 'Seu estilo é único e pessoal.';
  }

  private getStyleRecommendation(style: string): string {
    const recommendations: Record<string, string> = {
      aggressive: 'Procure oportunidades de ataque direto ao rei adversário',
      defensive: 'Fortaleça sua estrutura de peões e segurança do rei',
      positional: 'Foque no controle do centro e posicionamento de peças',
      tactical: 'Busque combinações e trocas favoráveis'
    };

    return recommendations[style] || 'Mantenha um jogo equilibrado';
  }

  // Métodos de avaliação específicos
  private isAttackingCenterPieces(move: ChessMove): boolean {
    const centerSquares = [
      { row: 3, col: 3 }, { row: 3, col: 4 },
      { row: 4, col: 3 }, { row: 4, col: 4 }
    ];
    return centerSquares.some(square =>
      square.row === move.to.row && square.col === move.to.col
    );
  }

  private improvesPosition(move: ChessMove): boolean {
    // Verifica se o movimento melhora a posição da peça
    const fromScore = this.getSquareValue(move.from);
    const toScore = this.getSquareValue(move.to);
    return toScore > fromScore;
  }

  private controlsImportantSquares(move: ChessMove): boolean {
    // Verifica se o movimento controla casas importantes
    const attacks = this.getPossibleMoves(move.to);
    return attacks.some(attack => this.isImportantSquare(attack.to));
  }

  private improvesPawnStructure(move: ChessMove): boolean {
    // TODO: Implementar análise de estrutura de peões
    return false;
  }

  private createsThreat(move: ChessMove): boolean {
    const clone = this.clone();
    clone.makeMove(move.from, move.to);
    return clone.isCheck();
  }

  private createsFork(move: ChessMove): boolean {
    // TODO: Implementar detecção de garfo
    return false;
  }

  private createsPin(move: ChessMove): boolean {
    // TODO: Implementar detecção de cravada
    return false;
  }

  private isDefensiveMove(move: ChessMove): boolean {
    // TODO: Implementar detecção de movimento defensivo
    return false;
  }

  private getSquareValue(position: ChessPosition): number {
    // Valores das casas do tabuleiro (centro vale mais)
    const squareValues = [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 1, 1, 1, 1, 1, 0],
      [0, 1, 2, 2, 2, 2, 1, 0],
      [0, 1, 2, 3, 3, 2, 1, 0],
      [0, 1, 2, 3, 3, 2, 1, 0],
      [0, 1, 2, 2, 2, 2, 1, 0],
      [0, 1, 1, 1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]
    ];

    return squareValues[position.row][position.col];
  }

  private isImportantSquare(position: ChessPosition): boolean {
    return this.getSquareValue(position) >= 2;
  }
}
