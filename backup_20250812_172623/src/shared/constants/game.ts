// Constantes do jogo de xadrez

// Configurações do tabuleiro
export const BOARD_SIZE = 8;
export const INITIAL_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';

// Peças do jogo
export const PIECES = {
  KING: 'k',
  QUEEN: 'q',
  ROOK: 'r',
  BISHOP: 'b',
  KNIGHT: 'n',
  PAWN: 'p',
} as const;

// Símbolos Unicode das peças
export const PIECE_SYMBOLS = {
  // Peças brancas
  'K': '♔',
  'Q': '♕',
  'R': '♖',
  'B': '♗',
  'N': '♘',
  'P': '♙',
  // Peças pretas
  'k': '♚',
  'q': '♛',
  'r': '♜',
  'b': '♝',
  'n': '♞',
  'p': '♟',
} as const;

// Status do jogo
export const GAME_STATUS = {
  WAITING: 'waiting',
  ACTIVE: 'active',
  PAUSED: 'paused',
  COMPLETED: 'completed',
  ABORTED: 'aborted',
} as const;

// Tipos de movimento
export const MOVE_TYPES = {
  NORMAL: 'normal',
  CAPTURE: 'capture',
  CASTLE_KINGSIDE: 'castle_kingside',
  CASTLE_QUEENSIDE: 'castle_queenside',
  EN_PASSANT: 'en_passant',
  PROMOTION: 'promotion',
} as const;

// Resultados do jogo
export const GAME_RESULTS = {
  WHITE_WIN: 'white_win',
  BLACK_WIN: 'black_win',
  DRAW: 'draw',
  STALEMATE: 'stalemate',
  INSUFFICIENT_MATERIAL: 'insufficient_material',
  THREEFOLD_REPETITION: 'threefold_repetition',
  FIFTY_MOVE_RULE: 'fifty_move_rule',
  ABANDONED: 'abandoned',
} as const;

// Controles de tempo
export const TIME_CONTROLS = {
  BULLET: {
    initial: 60 * 1,      // 1 minuto
    increment: 0,
  },
  BLITZ: {
    initial: 60 * 3,      // 3 minutos
    increment: 2,
  },
  RAPID: {
    initial: 60 * 10,     // 10 minutos
    increment: 5,
  },
  CLASSICAL: {
    initial: 60 * 30,     // 30 minutos
    increment: 10,
  },
} as const;

// Níveis de dificuldade da IA
export const AI_LEVELS = {
  BEGINNER: 1,
  CASUAL: 3,
  INTERMEDIATE: 5,
  ADVANCED: 7,
  EXPERT: 9,
} as const;

// Estilos culturais
export const CULTURAL_STYLES = {
  MEDIEVAL: 'medieval',
  RENAISSANCE: 'renaissance',
  MODERN: 'modern',
  ANCIENT: 'ancient',
} as const;

// Eventos culturais
export const CULTURAL_EVENTS = {
  BRILLIANT_MOVE: 'brilliant_move',
  CRITICAL_POSITION: 'critical_position',
  WINNING_SEQUENCE: 'winning_sequence',
  TACTICAL_OPPORTUNITY: 'tactical_opportunity',
  STRATEGIC_ADVANTAGE: 'strategic_advantage',
} as const;

// Configurações de análise
export const ANALYSIS_CONFIG = {
  DEPTH_DEFAULT: 20,
  DEPTH_DEEP: 30,
  MIN_TIME: 100,    // ms
  MAX_TIME: 5000,   // ms
  NODES_LIMIT: 1000000,
} as const;

// Métricas de qualidade
export const MOVE_QUALITY = {
  BRILLIANT: {
    threshold: 0.95,
    color: '#FFD700',
  },
  GREAT: {
    threshold: 0.85,
    color: '#32CD32',
  },
  GOOD: {
    threshold: 0.70,
    color: '#90EE90',
  },
  INACCURACY: {
    threshold: 0.50,
    color: '#FFD700',
  },
  MISTAKE: {
    threshold: 0.30,
    color: '#FFA500',
  },
  BLUNDER: {
    threshold: 0.15,
    color: '#FF0000',
  },
} as const;

// Configurações de cache
export const CACHE_CONFIG = {
  POSITION_TTL: 60 * 60,    // 1 hora
  ANALYSIS_TTL: 24 * 60 * 60, // 1 dia
  MAX_CACHE_SIZE: 1000,     // entradas
  WARMUP_DEPTH: 2,          // níveis de profundidade para pré-carregar
} as const;

// Configurações de monitoramento
export const MONITORING_CONFIG = {
  METRICS_INTERVAL: 5000,   // 5 segundos
  HEALTH_CHECK_INTERVAL: 30000, // 30 segundos
  ERROR_THRESHOLD: 0.05,    // 5% de erro máximo
  PERFORMANCE_THRESHOLD: 1000, // 1 segundo máximo de resposta
} as const;
