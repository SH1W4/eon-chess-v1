export interface AIProfile {
  userId: string;
  playstyle: 'aggressive' | 'defensive' | 'balanced' | 'positional' | 'tactical';
  strengths: string[];
  weaknesses: string[];
  preferredOpenings: string[];
  learningProgress: {
    totalGames: number;
    winRate: number;
    avgAccuracy: number;
    improvementRate: number;
  };
}

export interface AIInsight {
  type: 'mistake' | 'blunder' | 'good_move' | 'excellent_move' | 'missed_opportunity';
  move: number;
  description: string;
  suggestedMove?: string;
  evaluation: number;
}

export interface AIExercise {
  id: string;
  type: 'tactics' | 'endgame' | 'opening' | 'positional';
  difficulty: number;
  position: string; // FEN notation
  solution: string[];
  hints: string[];
}

export interface AIFeedback {
  timestamp: number;
  message: string;
  type: 'encouragement' | 'suggestion' | 'warning' | 'analysis';
  context?: any;
}

export interface AICoachingSession {
  id: string;
  userId: string;
  type: 'realtime' | 'post_game' | 'training';
  startTime: number;
  endTime?: number;
  insights: AIInsight[];
  exercises: AIExercise[];
  feedback: AIFeedback[];
  overallRating?: number;
  improvementAreas?: string[];
}
