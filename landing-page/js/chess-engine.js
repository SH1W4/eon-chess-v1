// Chess Engine Aeon - Sistema Completo de Xadrez com IA
class ChessEngine {
  constructor() {
    this.game = null;
    this.board = null;
    this.isReady = false;
    this.difficulty = 1300; // Elo padrão
    this.thinking = false;
    this.engineName = 'Aeon Chess AI';
    this.version = '1.0.0';
    
    this.init();
  }
  
  init() {
    // Verificar se Chess.js está disponível
    if (typeof Chess !== 'undefined') {
      this.game = new Chess();
      this.isReady = true;
      console.log(`${this.engineName} v${this.version} initialized`);
    } else {
      console.error('Chess.js library not found. Loading from CDN...');
      this.loadChessJS();
    }
  }
  
  loadChessJS() {
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/chess.js@1.0.0/chess.min.js';
    script.onload = () => {
      this.game = new Chess();
      this.isReady = true;
      console.log(`${this.engineName} loaded Chess.js and initialized`);
    };
    script.onerror = () => {
      console.error('Failed to load Chess.js');
    };
    document.head.appendChild(script);
  }
  
  // Fazer movimento da IA
  async makeMove(timeLimit = 1000) {
    if (!this.isReady || this.thinking) return null;
    
    this.thinking = true;
    
    // Simular tempo de pensamento
    await this.delay(Math.min(timeLimit, 800));
    
    try {
      const move = this.getBestMove();
      if (move) {
        const result = this.game.move(move);
        this.thinking = false;
        return result;
      }
    } catch (error) {
      console.error('Error making AI move:', error);
    }
    
    this.thinking = false;
    return null;
  }
  
  // Obter melhor movimento usando algoritmo minimax simplificado
  getBestMove() {
    if (!this.game || this.game.game_over()) return null;
    
    const moves = this.game.moves({ verbose: true });
    if (moves.length === 0) return null;
    
    // Para demonstração, usar diferentes estratégias baseadas na dificuldade
    if (this.difficulty < 1000) {
      // Nível iniciante - movimentos semi-aleatórios
      return this.getRandomMove(moves);
    } else if (this.difficulty < 1500) {
      // Nível intermediário - priorizar capturas
      return this.getIntermediateMove(moves);
    } else {
      // Nível avançado - análise mais profunda
      return this.getAdvancedMove(moves);
    }
  }
  
  getRandomMove(moves) {
    // 70% chance de movimento sensato, 30% aleatório
    const sensibleMoves = moves.filter(move => 
      move.captured || // Capturas
      move.promotion || // Promoções
      this.isPieceDeveloping(move) // Desenvolvimento
    );
    
    if (sensibleMoves.length > 0 && Math.random() > 0.3) {
      return sensibleMoves[Math.floor(Math.random() * sensibleMoves.length)];
    }
    
    return moves[Math.floor(Math.random() * moves.length)];
  }
  
  getIntermediateMove(moves) {
    // Prioridades: 1) Capturas, 2) Desenvolvimento, 3) Controle central
    const captures = moves.filter(move => move.captured);
    if (captures.length > 0) {
      return this.getBestCapture(captures);
    }
    
    const developments = moves.filter(move => this.isPieceDeveloping(move));
    if (developments.length > 0) {
      return developments[Math.floor(Math.random() * developments.length)];
    }
    
    const centralMoves = moves.filter(move => this.isCentralMove(move));
    if (centralMoves.length > 0) {
      return centralMoves[Math.floor(Math.random() * centralMoves.length)];
    }
    
    return moves[Math.floor(Math.random() * moves.length)];
  }
  
  getAdvancedMove(moves) {
    // Análise mais profunda com scoring
    let bestMove = null;
    let bestScore = -Infinity;
    
    for (const move of moves.slice(0, 20)) { // Limitar para performance
      const score = this.evaluateMove(move);
      if (score > bestScore) {
        bestScore = score;
        bestMove = move;
      }
    }
    
    return bestMove || moves[0];
  }
  
  evaluateMove(move) {
    let score = 0;
    
    // Valores das peças
    const pieceValues = {
      'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0
    };
    
    // Pontuação por captura
    if (move.captured) {
      score += pieceValues[move.captured.toLowerCase()] * 10;
    }
    
    // Bonificação por promoção
    if (move.promotion) {
      score += pieceValues[move.promotion.toLowerCase()] * 8;
    }
    
    // Penalidade por colocar peça em perigo
    if (this.isPieceInDanger(move.to)) {
      score -= pieceValues[move.piece.toLowerCase()] * 5;
    }
    
    // Bonificação por controle central
    if (this.isCentralMove(move)) {
      score += 2;
    }
    
    // Bonificação por desenvolvimento
    if (this.isPieceDeveloping(move)) {
      score += 3;
    }
    
    // Verificar se o movimento dá xeque
    const tempGame = new Chess(this.game.fen());
    tempGame.move(move);
    if (tempGame.in_check()) {
      score += 5;
    }
    
    return score + (Math.random() * 2); // Pequena randomização
  }
  
  getBestCapture(captures) {
    const pieceValues = {
      'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9
    };
    
    return captures.reduce((best, move) => {
      const captureValue = pieceValues[move.captured.toLowerCase()] || 0;
      const bestValue = pieceValues[best.captured.toLowerCase()] || 0;
      return captureValue > bestValue ? move : best;
    });
  }
  
  isPieceDeveloping(move) {
    const startRanks = {
      'white': { 'n': ['g1', 'b1'], 'b': ['c1', 'f1'] },
      'black': { 'n': ['g8', 'b8'], 'b': ['c8', 'f8'] }
    };
    
    const color = move.color;
    const piece = move.piece.toLowerCase();
    
    if (!startRanks[color] || !startRanks[color][piece]) return false;
    
    return startRanks[color][piece].includes(move.from);
  }
  
  isCentralMove(move) {
    const centralSquares = ['e4', 'e5', 'd4', 'd5'];
    return centralSquares.includes(move.to);
  }
  
  isPieceInDanger(square) {
    // Simples verificação se a casa está sendo atacada
    const tempGame = new Chess(this.game.fen());
    const attackers = tempGame.attackers(square, tempGame.turn() === 'w' ? 'b' : 'w');
    return attackers.length > 0;
  }
  
  // Análise de posição
  evaluatePosition() {
    if (!this.game) return { score: 0, evaluation: 'Equal' };
    
    const material = this.getMaterialBalance();
    const position = this.getPositionalScore();
    const safety = this.getKingSafety();
    
    const totalScore = material + position + safety;
    
    let evaluation = 'Equal';
    if (totalScore > 1) evaluation = 'White is better';
    else if (totalScore > 0.5) evaluation = 'White is slightly better';
    else if (totalScore < -1) evaluation = 'Black is better';
    else if (totalScore < -0.5) evaluation = 'Black is slightly better';
    
    return {
      score: totalScore,
      evaluation: evaluation,
      material: material,
      positional: position,
      safety: safety
    };
  }
  
  getMaterialBalance() {
    const pieceValues = { 'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9 };
    let whitePoints = 0;
    let blackPoints = 0;
    
    const board = this.game.board();
    
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 8; j++) {
        const piece = board[i][j];
        if (piece) {
          const value = pieceValues[piece.type.toLowerCase()] || 0;
          if (piece.color === 'w') {
            whitePoints += value;
          } else {
            blackPoints += value;
          }
        }
      }
    }
    
    return whitePoints - blackPoints;
  }
  
  getPositionalScore() {
    // Análise posicional básica
    let score = 0;
    
    // Controle central
    const centralSquares = ['e4', 'e5', 'd4', 'd5'];
    for (const square of centralSquares) {
      const piece = this.game.get(square);
      if (piece) {
        score += piece.color === 'w' ? 0.1 : -0.1;
      }
    }
    
    return score;
  }
  
  getKingSafety() {
    let score = 0;
    
    // Verificar se reis estão em xeque
    if (this.game.in_check()) {
      score += this.game.turn() === 'w' ? -0.5 : 0.5;
    }
    
    return score;
  }
  
  // Utilitários
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  // Métodos públicos para controle
  newGame() {
    if (this.game) {
      this.game.reset();
    }
  }
  
  makeHumanMove(move) {
    if (!this.isReady) return null;
    
    try {
      return this.game.move(move);
    } catch (error) {
      console.error('Invalid move:', error);
      return null;
    }
  }
  
  undo() {
    if (!this.game) return null;
    return this.game.undo();
  }
  
  getFEN() {
    return this.game ? this.game.fen() : null;
  }
  
  getPGN() {
    return this.game ? this.game.pgn() : null;
  }
  
  isGameOver() {
    return this.game ? this.game.game_over() : false;
  }
  
  getGameStatus() {
    if (!this.game) return 'Not initialized';
    
    if (this.game.in_checkmate()) {
      return `Checkmate - ${this.game.turn() === 'w' ? 'Black' : 'White'} wins`;
    } else if (this.game.in_draw()) {
      return 'Draw';
    } else if (this.game.in_stalemate()) {
      return 'Stalemate';
    } else if (this.game.in_check()) {
      return `${this.game.turn() === 'w' ? 'White' : 'Black'} is in check`;
    } else {
      return `${this.game.turn() === 'w' ? 'White' : 'Black'} to move`;
    }
  }
  
  setDifficulty(elo) {
    this.difficulty = Math.max(800, Math.min(2800, elo));
    console.log(`AI difficulty set to ${this.difficulty} Elo`);
  }
  
  // Análise de movimento para sistema de rating
  analyzeMove(move) {
    if (!move) return { quality: 'invalid', score: 0 };
    
    const evaluation = this.evaluatePosition();
    const moveScore = this.evaluateMove(move);
    
    let quality = 'average';
    if (moveScore > 8) quality = 'excellent';
    else if (moveScore > 5) quality = 'good';
    else if (moveScore < -5) quality = 'poor';
    else if (moveScore < -8) quality = 'blunder';
    
    return {
      quality: quality,
      score: moveScore,
      evaluation: evaluation
    };
  }
}

// Sistema de análise de jogador
class PlayerAnalyzer {
  constructor() {
    this.moves = [];
    this.startTime = Date.now();
    this.engine = new ChessEngine();
  }
  
  analyzeMove(move, thinkingTime = 1000) {
    if (!move) return;
    
    const analysis = this.engine.analyzeMove(move);
    const moveData = {
      move: move,
      thinkingTime: thinkingTime,
      quality: analysis.quality,
      score: analysis.score,
      timestamp: Date.now()
    };
    
    this.moves.push(moveData);
    
    return this.getPlayerStats();
  }
  
  getPlayerStats() {
    if (this.moves.length === 0) return this.getDefaultStats();
    
    const totalMoves = this.moves.length;
    const accurateMoves = this.moves.filter(m => ['excellent', 'good'].includes(m.quality)).length;
    const blunders = this.moves.filter(m => m.quality === 'blunder').length;
    const averageTime = this.moves.reduce((sum, m) => sum + m.thinkingTime, 0) / totalMoves;
    
    // Cálculo de Elo estimado baseado na qualidade dos movimentos
    const accuracy = (accurateMoves / totalMoves) * 100;
    const blunderRate = (blunders / totalMoves) * 100;
    
    let estimatedElo = 1200;
    estimatedElo += (accuracy - 50) * 10; // Base de 50% de precisão
    estimatedElo -= blunderRate * 50; // Penalidade por blunders
    estimatedElo = Math.max(800, Math.min(2800, Math.round(estimatedElo)));
    
    // Determinar estilo de jogo
    const avgThinkingTime = averageTime / 1000;
    let playStyle = 'balanced';
    if (avgThinkingTime > 15) playStyle = 'positional';
    else if (avgThinkingTime < 5) playStyle = 'tactical';
    
    return {
      totalMoves: totalMoves,
      accuracy: Math.round(accuracy),
      blunders: blunders,
      averageThinkingTime: Math.round(avgThinkingTime),
      estimatedElo: estimatedElo,
      playStyle: playStyle,
      lastMoveQuality: this.moves[this.moves.length - 1]?.quality || 'unknown'
    };
  }
  
  getDefaultStats() {
    return {
      totalMoves: 0,
      accuracy: 50,
      blunders: 0,
      averageThinkingTime: 10,
      estimatedElo: 1200,
      playStyle: 'balanced',
      lastMoveQuality: 'unknown'
    };
  }
  
  reset() {
    this.moves = [];
    this.startTime = Date.now();
  }
  
  getRecommendations() {
    const stats = this.getPlayerStats();
    const recommendations = [];
    
    if (stats.accuracy < 60) {
      recommendations.push('Focus on tactical training to improve move accuracy');
    }
    
    if (stats.blunders > 2) {
      recommendations.push('Take more time to calculate before moving');
    }
    
    if (stats.averageThinkingTime < 3) {
      recommendations.push('Slow down and analyze positions more deeply');
    }
    
    if (stats.estimatedElo < 1400) {
      recommendations.push('Study basic endgames and opening principles');
    }
    
    return recommendations.length > 0 ? recommendations : ['Keep playing and analyzing your games!'];
  }
}

// Exportar para uso global
if (typeof window !== 'undefined') {
  window.ChessEngine = ChessEngine;
  window.PlayerAnalyzer = PlayerAnalyzer;
}

// Inicializar engine global
document.addEventListener('DOMContentLoaded', function() {
  if (!window.aeonChessEngine) {
    window.aeonChessEngine = new ChessEngine();
    window.aeonPlayerAnalyzer = new PlayerAnalyzer();
    console.log('Aeon Chess Engine and Player Analyzer initialized');
  }
});
