from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opponent_type = db.Column(db.String(20), nullable=False)  # 'ai', 'human', 'online'
    opponent_name = db.Column(db.String(100))
    game_mode = db.Column(db.String(20), nullable=False)  # 'casual', 'ranked', 'training', 'cultural'
    difficulty_level = db.Column(db.Integer, default=1)
    
    # Game state
    board_state = db.Column(db.Text)  # FEN notation
    moves_history = db.Column(db.Text)  # JSON array of moves
    current_turn = db.Column(db.String(5), default='white')
    game_status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'paused'
    result = db.Column(db.String(20))  # 'white_wins', 'black_wins', 'draw', 'abandoned'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Game metrics
    total_moves = db.Column(db.Integer, default=0)
    duration_seconds = db.Column(db.Integer, default=0)
    
    # Cultural context
    cultural_theme = db.Column(db.String(50))  # 'medieval', 'renaissance', 'modern', etc.
    narrative_context = db.Column(db.Text)
    
    def __init__(self, user_id, opponent_type, game_mode, **kwargs):
        self.user_id = user_id
        self.opponent_type = opponent_type
        self.game_mode = game_mode
        self.board_state = kwargs.get('board_state', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.moves_history = kwargs.get('moves_history', '[]')
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_move(self, move_data):
        """Add a move to the game history"""
        moves = json.loads(self.moves_history) if self.moves_history else []
        moves.append(move_data)
        self.moves_history = json.dumps(moves)
        self.total_moves = len(moves)
        self.updated_at = datetime.utcnow()
    
    def get_moves(self):
        """Get all moves as a list"""
        return json.loads(self.moves_history) if self.moves_history else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'opponent_type': self.opponent_type,
            'opponent_name': self.opponent_name,
            'game_mode': self.game_mode,
            'difficulty_level': self.difficulty_level,
            'board_state': self.board_state,
            'moves_history': self.get_moves(),
            'current_turn': self.current_turn,
            'game_status': self.game_status,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_moves': self.total_moves,
            'duration_seconds': self.duration_seconds,
            'cultural_theme': self.cultural_theme,
            'narrative_context': self.narrative_context
        }

class GameAnalysis(db.Model):
    __tablename__ = 'game_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Analysis data
    accuracy_score = db.Column(db.Float)
    blunders_count = db.Column(db.Integer, default=0)
    mistakes_count = db.Column(db.Integer, default=0)
    inaccuracies_count = db.Column(db.Integer, default=0)
    brilliant_moves_count = db.Column(db.Integer, default=0)
    
    # Strategic analysis
    opening_name = db.Column(db.String(100))
    opening_accuracy = db.Column(db.Float)
    middlegame_score = db.Column(db.Float)
    endgame_score = db.Column(db.Float)
    
    # Tactical analysis
    tactical_themes = db.Column(db.Text)  # JSON array
    missed_tactics = db.Column(db.Text)  # JSON array
    
    # Time management
    average_move_time = db.Column(db.Float)
    time_pressure_moves = db.Column(db.Integer, default=0)
    
    # AI insights
    ai_commentary = db.Column(db.Text)
    improvement_suggestions = db.Column(db.Text)  # JSON array
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, game_id, user_id, **kwargs):
        self.game_id = game_id
        self.user_id = user_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'game_id': self.game_id,
            'user_id': self.user_id,
            'accuracy_score': self.accuracy_score,
            'blunders_count': self.blunders_count,
            'mistakes_count': self.mistakes_count,
            'inaccuracies_count': self.inaccuracies_count,
            'brilliant_moves_count': self.brilliant_moves_count,
            'opening_name': self.opening_name,
            'opening_accuracy': self.opening_accuracy,
            'middlegame_score': self.middlegame_score,
            'endgame_score': self.endgame_score,
            'tactical_themes': json.loads(self.tactical_themes) if self.tactical_themes else [],
            'missed_tactics': json.loads(self.missed_tactics) if self.missed_tactics else [],
            'average_move_time': self.average_move_time,
            'time_pressure_moves': self.time_pressure_moves,
            'ai_commentary': self.ai_commentary,
            'improvement_suggestions': json.loads(self.improvement_suggestions) if self.improvement_suggestions else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

