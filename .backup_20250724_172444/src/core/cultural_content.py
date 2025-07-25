from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class CulturalContent(db.Model):
    __tablename__ = 'cultural_content'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # 'story', 'lesson', 'historical', 'philosophical'
    category = db.Column(db.String(50))  # 'opening', 'middlegame', 'endgame', 'general'
    
    # Content data
    description = db.Column(db.Text)
    content_body = db.Column(db.Text)  # Main content (markdown/html)
    media_urls = db.Column(db.Text)  # JSON array of media URLs
    
    # Cultural context
    historical_period = db.Column(db.String(50))  # 'medieval', 'renaissance', 'modern', etc.
    cultural_theme = db.Column(db.String(50))
    geographical_origin = db.Column(db.String(100))
    
    # Chess context
    related_openings = db.Column(db.Text)  # JSON array
    chess_concepts = db.Column(db.Text)  # JSON array
    difficulty_level = db.Column(db.Integer, default=1)  # 1-5
    
    # Metadata
    author = db.Column(db.String(100))
    language = db.Column(db.String(10), default='pt-BR')
    tags = db.Column(db.Text)  # JSON array
    
    # Engagement metrics
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    completion_rate = db.Column(db.Float, default=0.0)
    
    # Publishing
    is_published = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    def __init__(self, title, content_type, **kwargs):
        self.title = title
        self.content_type = content_type
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_view(self):
        """Increment view count"""
        self.view_count += 1
    
    def add_like(self):
        """Increment like count"""
        self.like_count += 1
    
    def get_tags(self):
        """Get tags as list"""
        return json.loads(self.tags) if self.tags else []
    
    def get_media_urls(self):
        """Get media URLs as list"""
        return json.loads(self.media_urls) if self.media_urls else []
    
    def get_related_openings(self):
        """Get related openings as list"""
        return json.loads(self.related_openings) if self.related_openings else []
    
    def get_chess_concepts(self):
        """Get chess concepts as list"""
        return json.loads(self.chess_concepts) if self.chess_concepts else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content_type': self.content_type,
            'category': self.category,
            'description': self.description,
            'content_body': self.content_body,
            'media_urls': self.get_media_urls(),
            'historical_period': self.historical_period,
            'cultural_theme': self.cultural_theme,
            'geographical_origin': self.geographical_origin,
            'related_openings': self.get_related_openings(),
            'chess_concepts': self.get_chess_concepts(),
            'difficulty_level': self.difficulty_level,
            'author': self.author,
            'language': self.language,
            'tags': self.get_tags(),
            'view_count': self.view_count,
            'like_count': self.like_count,
            'completion_rate': self.completion_rate,
            'is_published': self.is_published,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }

class UserContentProgress(db.Model):
    __tablename__ = 'user_content_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.Integer, db.ForeignKey('cultural_content.id'), nullable=False)
    
    # Progress tracking
    progress_percentage = db.Column(db.Float, default=0.0)
    is_completed = db.Column(db.Boolean, default=False)
    is_liked = db.Column(db.Boolean, default=False)
    is_bookmarked = db.Column(db.Boolean, default=False)
    
    # Engagement data
    time_spent_seconds = db.Column(db.Integer, default=0)
    last_position = db.Column(db.String(50))  # For resuming content
    notes = db.Column(db.Text)  # User's personal notes
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'content_id', name='unique_user_content'),)
    
    def __init__(self, user_id, content_id, **kwargs):
        self.user_id = user_id
        self.content_id = content_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_progress(self, progress_percentage):
        """Update progress and check for completion"""
        self.progress_percentage = progress_percentage
        self.last_accessed = datetime.utcnow()
        
        if progress_percentage >= 100.0 and not self.is_completed:
            self.is_completed = True
            self.completed_at = datetime.utcnow()
    
    def add_time_spent(self, seconds):
        """Add time spent on content"""
        self.time_spent_seconds += seconds
        self.last_accessed = datetime.utcnow()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id,
            'progress_percentage': self.progress_percentage,
            'is_completed': self.is_completed,
            'is_liked': self.is_liked,
            'is_bookmarked': self.is_bookmarked,
            'time_spent_seconds': self.time_spent_seconds,
            'last_position': self.last_position,
            'notes': self.notes,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }

class CulturalEvent(db.Model):
    __tablename__ = 'cultural_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(20), nullable=False)  # 'tournament', 'lesson', 'story_time', 'masterclass'
    
    # Event details
    cultural_theme = db.Column(db.String(50))
    difficulty_level = db.Column(db.Integer, default=1)
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    
    # Scheduling
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    timezone = db.Column(db.String(50), default='UTC')
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(50))  # 'daily', 'weekly', 'monthly'
    
    # Content
    content_data = db.Column(db.Text)  # JSON data specific to event type
    host_name = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='scheduled')  # 'scheduled', 'active', 'completed', 'cancelled'
    is_premium = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, title, event_type, start_time, **kwargs):
        self.title = title
        self.event_type = event_type
        self.start_time = start_time
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def can_join(self):
        """Check if event can accept more participants"""
        if self.max_participants:
            return self.current_participants < self.max_participants
        return True
    
    def add_participant(self):
        """Add a participant to the event"""
        if self.can_join():
            self.current_participants += 1
            return True
        return False
    
    def remove_participant(self):
        """Remove a participant from the event"""
        if self.current_participants > 0:
            self.current_participants -= 1
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'cultural_theme': self.cultural_theme,
            'difficulty_level': self.difficulty_level,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'timezone': self.timezone,
            'is_recurring': self.is_recurring,
            'recurrence_pattern': self.recurrence_pattern,
            'content_data': json.loads(self.content_data) if self.content_data else {},
            'host_name': self.host_name,
            'status': self.status,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

