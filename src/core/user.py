from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    
    # Profile information
    full_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    country = db.Column(db.String(50))
    language = db.Column(db.String(10), default='pt-BR')
    
    # Chess profile
    chess_experience = db.Column(db.String(20), default='beginner')  # 'beginner', 'intermediate', 'advanced', 'expert'
    preferred_time_control = db.Column(db.String(20), default='standard')  # 'bullet', 'blitz', 'rapid', 'standard'
    favorite_piece = db.Column(db.String(10))
    
    # Subscription and features
    subscription_type = db.Column(db.String(20), default='free')  # 'free', 'premium', 'pro'
    subscription_expires = db.Column(db.DateTime)
    features_enabled = db.Column(db.Text)  # JSON array of enabled features
    
    # Hardware connection
    board_serial_number = db.Column(db.String(50))
    board_connected = db.Column(db.Boolean, default=False)
    last_board_sync = db.Column(db.DateTime)
    
    # Privacy and preferences
    privacy_level = db.Column(db.String(20), default='public')  # 'public', 'friends', 'private'
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_active = db.Column(db.DateTime)
    
    # Relationships
    games = db.relationship('Game', backref='user', lazy=True, foreign_keys='Game.user_id')
    ai_profile = db.relationship('AIProfile', backref='user', uselist=False)
    learning_sessions = db.relationship('LearningSession', backref='user', lazy=True)
    
    def __init__(self, username, email, **kwargs):
        self.username = username
        self.email = email
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def is_premium(self):
        """Check if user has premium subscription"""
        if self.subscription_type in ['premium', 'pro']:
            if self.subscription_expires and self.subscription_expires > datetime.utcnow():
                return True
        return False
    
    def get_enabled_features(self):
        """Get list of enabled features for user"""
        if self.features_enabled:
            return json.loads(self.features_enabled)
        
        # Default features based on subscription
        if self.is_premium():
            return ['ai_analysis', 'cultural_content', 'advanced_training', 'community_features']
        else:
            return ['basic_play', 'simple_analysis']
    
    def enable_feature(self, feature):
        """Enable a feature for the user"""
        features = self.get_enabled_features()
        if feature not in features:
            features.append(feature)
            self.features_enabled = json.dumps(features)
    
    def update_last_active(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
    
    def connect_board(self, serial_number):
        """Connect physical chess board"""
        self.board_serial_number = serial_number
        self.board_connected = True
        self.last_board_sync = datetime.utcnow()
    
    def disconnect_board(self):
        """Disconnect physical chess board"""
        self.board_connected = False
    
    def to_dict(self, include_private=False):
        data = {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'country': self.country,
            'language': self.language,
            'chess_experience': self.chess_experience,
            'preferred_time_control': self.preferred_time_control,
            'favorite_piece': self.favorite_piece,
            'subscription_type': self.subscription_type,
            'features_enabled': self.get_enabled_features(),
            'board_connected': self.board_connected,
            'privacy_level': self.privacy_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }
        
        if include_private:
            data.update({
                'email': self.email,
                'subscription_expires': self.subscription_expires.isoformat() if self.subscription_expires else None,
                'board_serial_number': self.board_serial_number,
                'last_board_sync': self.last_board_sync.isoformat() if self.last_board_sync else None,
                'email_notifications': self.email_notifications,
                'push_notifications': self.push_notifications,
                'last_login': self.last_login.isoformat() if self.last_login else None
            })
        
        return data

