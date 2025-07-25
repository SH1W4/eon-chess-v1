from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AIProfile(db.Model):
    __tablename__ = 'ai_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Learning preferences
    learning_style = db.Column(db.String(20), default='balanced')  # 'visual', 'analytical', 'tactical', 'positional', 'balanced'
    preferred_difficulty = db.Column(db.String(20), default='adaptive')  # 'easy', 'medium', 'hard', 'adaptive'
    coaching_tone = db.Column(db.String(20), default='encouraging')  # 'encouraging', 'analytical', 'challenging', 'patient'
    
    # Playing style analysis
    playing_style = db.Column(db.String(20))  # 'aggressive', 'positional', 'tactical', 'defensive', 'balanced'
    favorite_openings = db.Column(db.Text)  # JSON array
    weak_areas = db.Column(db.Text)  # JSON array
    strong_areas = db.Column(db.Text)  # JSON array
    
    # Performance metrics
    current_rating = db.Column(db.Integer, default=1200)
    peak_rating = db.Column(db.Integer, default=1200)
    games_played = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0.0)
    
    # Learning progress
    completed_lessons = db.Column(db.Text)  # JSON array
    current_learning_path = db.Column(db.String(50))
    mastered_concepts = db.Column(db.Text)  # JSON array
    struggling_concepts = db.Column(db.Text)  # JSON array
    
    # Behavioral patterns
    session_duration_preference = db.Column(db.Integer, default=30)  # minutes
    best_performance_time = db.Column(db.String(20))  # 'morning', 'afternoon', 'evening', 'night'
    mistake_patterns = db.Column(db.Text)  # JSON array
    improvement_rate = db.Column(db.Float, default=0.0)
    
    # Cultural preferences
    preferred_themes = db.Column(db.Text)  # JSON array
    cultural_interests = db.Column(db.Text)  # JSON array
    narrative_engagement = db.Column(db.Float, default=0.5)  # 0-1 scale
    
    # AI adaptation settings
    adaptation_speed = db.Column(db.Float, default=0.5)  # How quickly AI adapts to user
    challenge_level = db.Column(db.Float, default=0.5)  # How much AI challenges user
    support_level = db.Column(db.Float, default=0.7)  # How much help AI provides
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_interaction = db.Column(db.DateTime)
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_performance(self, game_result, accuracy_score):
        """Update performance metrics based on game result"""
        self.games_played += 1
        
        if game_result == 'win':
            self.current_rating += max(10, int(20 * accuracy_score))
        elif game_result == 'loss':
            self.current_rating -= max(5, int(15 * (1 - accuracy_score)))
        
        self.peak_rating = max(self.peak_rating, self.current_rating)
        self.last_interaction = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def add_completed_lesson(self, lesson_id):
        """Add a completed lesson to the profile"""
        completed = json.loads(self.completed_lessons) if self.completed_lessons else []
        if lesson_id not in completed:
            completed.append(lesson_id)
            self.completed_lessons = json.dumps(completed)
    
    def add_mastered_concept(self, concept):
        """Add a mastered concept"""
        mastered = json.loads(self.mastered_concepts) if self.mastered_concepts else []
        if concept not in mastered:
            mastered.append(concept)
            self.mastered_concepts = json.dumps(mastered)
            
        # Remove from struggling concepts if present
        struggling = json.loads(self.struggling_concepts) if self.struggling_concepts else []
        if concept in struggling:
            struggling.remove(concept)
            self.struggling_concepts = json.dumps(struggling)
    
    def add_struggling_concept(self, concept):
        """Add a concept the user is struggling with"""
        struggling = json.loads(self.struggling_concepts) if self.struggling_concepts else []
        if concept not in struggling:
            struggling.append(concept)
            self.struggling_concepts = json.dumps(struggling)
    
    def get_personalized_difficulty(self):
        """Calculate personalized difficulty based on performance"""
        base_difficulty = 0.5
        
        # Adjust based on win rate
        if self.win_rate > 0.7:
            base_difficulty += 0.2
        elif self.win_rate < 0.3:
            base_difficulty -= 0.2
            
        # Adjust based on improvement rate
        base_difficulty += self.improvement_rate * 0.1
        
        return max(0.1, min(0.9, base_difficulty))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_style': self.learning_style,
            'preferred_difficulty': self.preferred_difficulty,
            'coaching_tone': self.coaching_tone,
            'playing_style': self.playing_style,
            'favorite_openings': json.loads(self.favorite_openings) if self.favorite_openings else [],
            'weak_areas': json.loads(self.weak_areas) if self.weak_areas else [],
            'strong_areas': json.loads(self.strong_areas) if self.strong_areas else [],
            'current_rating': self.current_rating,
            'peak_rating': self.peak_rating,
            'games_played': self.games_played,
            'win_rate': self.win_rate,
            'completed_lessons': json.loads(self.completed_lessons) if self.completed_lessons else [],
            'current_learning_path': self.current_learning_path,
            'mastered_concepts': json.loads(self.mastered_concepts) if self.mastered_concepts else [],
            'struggling_concepts': json.loads(self.struggling_concepts) if self.struggling_concepts else [],
            'session_duration_preference': self.session_duration_preference,
            'best_performance_time': self.best_performance_time,
            'mistake_patterns': json.loads(self.mistake_patterns) if self.mistake_patterns else [],
            'improvement_rate': self.improvement_rate,
            'preferred_themes': json.loads(self.preferred_themes) if self.preferred_themes else [],
            'cultural_interests': json.loads(self.cultural_interests) if self.cultural_interests else [],
            'narrative_engagement': self.narrative_engagement,
            'adaptation_speed': self.adaptation_speed,
            'challenge_level': self.challenge_level,
            'support_level': self.support_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None
        }

class LearningSession(db.Model):
    __tablename__ = 'learning_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_type = db.Column(db.String(20), nullable=False)  # 'lesson', 'practice', 'analysis', 'cultural'
    
    # Session content
    topic = db.Column(db.String(100))
    difficulty_level = db.Column(db.Float)
    content_data = db.Column(db.Text)  # JSON data specific to session type
    
    # Performance tracking
    completion_rate = db.Column(db.Float, default=0.0)
    accuracy_score = db.Column(db.Float)
    time_spent_seconds = db.Column(db.Integer, default=0)
    
    # AI feedback
    ai_feedback = db.Column(db.Text)
    recommended_next_steps = db.Column(db.Text)  # JSON array
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __init__(self, user_id, session_type, **kwargs):
        self.user_id = user_id
        self.session_type = session_type
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def complete_session(self, completion_rate, accuracy_score=None):
        """Mark session as completed with performance metrics"""
        self.completion_rate = completion_rate
        self.accuracy_score = accuracy_score
        self.completed_at = datetime.utcnow()
        self.time_spent_seconds = int((self.completed_at - self.started_at).total_seconds())
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_type': self.session_type,
            'topic': self.topic,
            'difficulty_level': self.difficulty_level,
            'content_data': json.loads(self.content_data) if self.content_data else {},
            'completion_rate': self.completion_rate,
            'accuracy_score': self.accuracy_score,
            'time_spent_seconds': self.time_spent_seconds,
            'ai_feedback': self.ai_feedback,
            'recommended_next_steps': json.loads(self.recommended_next_steps) if self.recommended_next_steps else [],
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

