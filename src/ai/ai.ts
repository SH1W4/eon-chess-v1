import { ChessMove, GameAnalysis, PieceColor } from './chess';

export interface AIProfile {
  userId: string;
  playingStyle: PlayingStyle;
  strengths: ChessSkill[];
  weaknesses: ChessSkill[];
  preferredOpenings: string[];
  learningGoals: LearningGoal[];
  personalityType: AIPersonality;
  coachingPreferences: CoachingPreferences;
  progressMetrics: ProgressMetrics;
  culturalInterests: CulturalInterest[];
}

export type PlayingStyle = 
  | 'aggressive' 
  | 'positional' 
  | 'tactical' 
  | 'defensive' 
  | 'creative' 
  | 'classical';

export type ChessSkill = 
  | 'opening' 
  | 'middlegame' 
  | 'endgame' 
  | 'tactics' 
  | 'strategy' 
  | 'calculation' 
  | 'time_management';

export interface LearningGoal {
  id: string;
  type: ChessSkill;
  description: string;
  targetDate: number;
  progress: number; // 0-100
  isActive: boolean;
}

export type AIPersonality = 
  | 'encouraging' 
  | 'analytical' 
  | 'philosophical' 
  | 'competitive' 
  | 'patient' 
  | 'inspiring';

export interface CoachingPreferences {
  frequency: 'minimal' | 'moderate' | 'frequent';
  timing: 'real_time' | 'post_game' | 'both';
  style: 'hints' | 'explanations' | 'questions';
  culturalIntegration: boolean;
  voiceEnabled: boolean;
  visualAids: boolean;
}

export interface ProgressMetrics {
  gamesPlayed: number;
  winRate: number;
  averageAccuracy: number;
  ratingProgress: number[];
  skillProgress: Record<ChessSkill, number>;
  timeSpentLearning: number;
  culturalContentConsumed: number;
  achievementsUnlocked: string[];
}

export interface CulturalInterest {
  category: CulturalCategory;
  level: 'beginner' | 'intermediate' | 'advanced';
  topics: string[];
  preferredFormat: 'text' | 'video' | 'interactive' | 'audio';
}

export type CulturalCategory = 
  | 'history' 
  | 'philosophy' 
  | 'famous_games' 
  | 'masters' 
  | 'openings_history' 
  | 'cultural_impact';

export interface AICoachingSession {
  id: string;
  userId: string;
  gameId?: string;
  type: CoachingType;
  startTime: number;
  endTime?: number;
  insights: CoachingInsight[];
  exercises: CoachingExercise[];
  culturalContent?: CulturalContent[];
  feedback: UserFeedback[];
}

export type CoachingType = 
  | 'game_analysis' 
  | 'tactical_training' 
  | 'opening_study' 
  | 'endgame_practice' 
  | 'cultural_exploration';

export interface CoachingInsight {
  id: string;
  type: 'strength' | 'weakness' | 'improvement' | 'pattern';
  title: string;
  description: string;
  evidence: ChessMove[];
  recommendation: string;
  priority: 'low' | 'medium' | 'high';
  culturalContext?: string;
}

export interface CoachingExercise {
  id: string;
  type: 'puzzle' | 'position' | 'opening' | 'endgame';
  title: string;
  description: string;
  difficulty: number; // 1-10
  position: string; // FEN notation
  solution: ChessMove[];
  hints: string[];
  culturalStory?: string;
  timeLimit?: number;
}

export interface UserFeedback {
  timestamp: number;
  type: 'rating' | 'comment' | 'preference';
  value: number | string;
  context: string;
}

export interface AIResponse {
  message: string;
  type: 'coaching' | 'analysis' | 'cultural' | 'encouragement';
  confidence: number;
  suggestions?: string[];
  relatedContent?: CulturalContent[];
  nextSteps?: string[];
}

export interface CulturalContent {
  id: string;
  title: string;
  category: CulturalCategory;
  type: 'story' | 'lesson' | 'biography' | 'game_analysis' | 'philosophy';
  content: string;
  mediaUrls?: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedReadTime: number;
  tags: string[];
  relatedGames?: string[];
  relatedMasters?: string[];
  culturalPeriod?: string;
  geographicalOrigin?: string;
  chessOpenings?: string[];
  philosophicalThemes?: string[];
}

export interface LearningSession {
  id: string;
  userId: string;
  type: CoachingType;
  startTime: number;
  endTime?: number;
  activitiesCompleted: string[];
  skillsImproved: ChessSkill[];
  culturalContentViewed: string[];
  performanceMetrics: {
    accuracy: number;
    timeSpent: number;
    exercisesCompleted: number;
    mistakesMade: number;
  };
  aiInsights: AIResponse[];
  userSatisfaction?: number;
}

