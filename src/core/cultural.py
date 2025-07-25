from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.cultural_content import CulturalContent, UserContentProgress, CulturalEvent
from src.models.ai_profile import AIProfile
import json
from datetime import datetime, timedelta

cultural_bp = Blueprint('cultural', __name__)

@cultural_bp.route('/cultural/content', methods=['GET'])
def get_cultural_content():
    """Get cultural content with filtering and personalization"""
    user_id = request.args.get('user_id')
    content_type = request.args.get('type')
    category = request.args.get('category')
    theme = request.args.get('theme')
    difficulty = request.args.get('difficulty', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    try:
        # Build query
        query = CulturalContent.query.filter_by(is_published=True)
        
        if content_type:
            query = query.filter_by(content_type=content_type)
        if category:
            query = query.filter_by(category=category)
        if theme:
            query = query.filter_by(cultural_theme=theme)
        if difficulty:
            query = query.filter_by(difficulty_level=difficulty)
        
        # Get user's AI profile for personalization
        personalized_content = []
        if user_id:
            ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
            if ai_profile:
                # Personalize content based on user preferences
                cultural_interests = ai_profile.cultural_interests
                if cultural_interests:
                    interests = json.loads(cultural_interests) if isinstance(cultural_interests, str) else cultural_interests
                    if interests:
                        personalized_query = query.filter(CulturalContent.cultural_theme.in_(interests))
                        personalized_content = personalized_query.limit(5).all()
        
        # Get paginated results
        pagination = query.order_by(CulturalContent.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        content_list = []
        for content in pagination.items:
            content_dict = content.to_dict()
            
            # Add user progress if user_id provided
            if user_id:
                progress = UserContentProgress.query.filter_by(
                    user_id=user_id, content_id=content.id
                ).first()
                if progress:
                    content_dict['user_progress'] = progress.to_dict()
            
            content_list.append(content_dict)
        
        return jsonify({
            'content': content_list,
            'personalized_content': [c.to_dict() for c in personalized_content],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/content/<int:content_id>', methods=['GET'])
def get_content_detail(content_id):
    """Get detailed cultural content"""
    user_id = request.args.get('user_id')
    
    try:
        content = CulturalContent.query.get_or_404(content_id)
        
        if not content.is_published:
            return jsonify({'error': 'Content not available'}), 404
        
        # Check if user has access (premium content)
        if content.is_premium and user_id:
            user = User.query.get(user_id)
            if not user or not user.is_premium():
                return jsonify({'error': 'Premium subscription required'}), 403
        
        # Increment view count
        content.add_view()
        
        content_dict = content.to_dict()
        
        # Add user progress if user_id provided
        if user_id:
            progress = UserContentProgress.query.filter_by(
                user_id=user_id, content_id=content_id
            ).first()
            
            if not progress:
                # Create new progress entry
                progress = UserContentProgress(user_id=user_id, content_id=content_id)
                db.session.add(progress)
            
            content_dict['user_progress'] = progress.to_dict()
        
        # Get related content
        related_content = CulturalContent.query.filter(
            CulturalContent.id != content_id,
            CulturalContent.cultural_theme == content.cultural_theme,
            CulturalContent.is_published == True
        ).limit(3).all()
        
        content_dict['related_content'] = [c.to_dict() for c in related_content]
        
        db.session.commit()
        
        return jsonify({'content': content_dict})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/content/<int:content_id>/progress', methods=['POST'])
def update_content_progress():
    """Update user's progress on cultural content"""
    content_id = request.view_args['content_id']
    data = request.get_json()
    
    required_fields = ['user_id', 'progress_percentage']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        progress = UserContentProgress.query.filter_by(
            user_id=data['user_id'], content_id=content_id
        ).first()
        
        if not progress:
            progress = UserContentProgress(
                user_id=data['user_id'], 
                content_id=content_id
            )
            db.session.add(progress)
        
        # Update progress
        progress.update_progress(data['progress_percentage'])
        
        # Update optional fields
        if 'last_position' in data:
            progress.last_position = data['last_position']
        if 'notes' in data:
            progress.notes = data['notes']
        if 'time_spent' in data:
            progress.add_time_spent(data['time_spent'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress updated successfully',
            'progress': progress.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/content/<int:content_id>/like', methods=['POST'])
def like_content():
    """Like/unlike cultural content"""
    content_id = request.view_args['content_id']
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        content = CulturalContent.query.get_or_404(content_id)
        
        progress = UserContentProgress.query.filter_by(
            user_id=data['user_id'], content_id=content_id
        ).first()
        
        if not progress:
            progress = UserContentProgress(
                user_id=data['user_id'], 
                content_id=content_id
            )
            db.session.add(progress)
        
        # Toggle like status
        if not progress.is_liked:
            progress.is_liked = True
            content.add_like()
            message = 'Content liked successfully'
        else:
            progress.is_liked = False
            content.like_count = max(0, content.like_count - 1)
            message = 'Content unliked successfully'
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'is_liked': progress.is_liked,
            'total_likes': content.like_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/events', methods=['GET'])
def get_cultural_events():
    """Get upcoming cultural events"""
    user_id = request.args.get('user_id')
    event_type = request.args.get('type')
    theme = request.args.get('theme')
    
    try:
        # Get upcoming events
        query = CulturalEvent.query.filter(
            CulturalEvent.start_time > datetime.utcnow(),
            CulturalEvent.status == 'scheduled'
        )
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if theme:
            query = query.filter_by(cultural_theme=theme)
        
        events = query.order_by(CulturalEvent.start_time).limit(20).all()
        
        # Personalize events based on user preferences
        personalized_events = []
        if user_id:
            ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
            if ai_profile:
                cultural_interests = ai_profile.cultural_interests
                if cultural_interests:
                    interests = json.loads(cultural_interests) if isinstance(cultural_interests, str) else cultural_interests
                    personalized_events = [e for e in events if e.cultural_theme in interests]
        
        return jsonify({
            'events': [event.to_dict() for event in events],
            'personalized_events': [event.to_dict() for event in personalized_events[:5]]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/events/<int:event_id>/join', methods=['POST'])
def join_cultural_event(event_id):
    """Join a cultural event"""
    data = request.get_json()
    
    if 'user_id' not in data:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        event = CulturalEvent.query.get_or_404(event_id)
        
        # Check if event is premium and user has access
        if event.is_premium:
            user = User.query.get(data['user_id'])
            if not user or not user.is_premium():
                return jsonify({'error': 'Premium subscription required'}), 403
        
        # Check if event can accept more participants
        if not event.can_join():
            return jsonify({'error': 'Event is full'}), 400
        
        # Add participant
        if event.add_participant():
            db.session.commit()
            return jsonify({
                'message': 'Successfully joined event',
                'event': event.to_dict()
            })
        else:
            return jsonify({'error': 'Could not join event'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/themes', methods=['GET'])
def get_cultural_themes():
    """Get available cultural themes"""
    try:
        # Get distinct themes from content
        themes_query = db.session.query(CulturalContent.cultural_theme).distinct().all()
        themes = [theme[0] for theme in themes_query if theme[0]]
        
        # Add theme metadata
        theme_data = []
        for theme in themes:
            content_count = CulturalContent.query.filter_by(
                cultural_theme=theme, is_published=True
            ).count()
            
            theme_data.append({
                'name': theme,
                'display_name': theme.replace('_', ' ').title(),
                'content_count': content_count,
                'description': get_theme_description(theme)
            })
        
        return jsonify({'themes': theme_data})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cultural_bp.route('/cultural/user-library/<int:user_id>', methods=['GET'])
def get_user_library(user_id):
    """Get user's personal cultural content library"""
    try:
        # Get user's progress on all content
        progress_query = db.session.query(
            UserContentProgress, CulturalContent
        ).join(
            CulturalContent, UserContentProgress.content_id == CulturalContent.id
        ).filter(
            UserContentProgress.user_id == user_id
        ).all()
        
        library = {
            'completed': [],
            'in_progress': [],
            'liked': [],
            'bookmarked': []
        }
        
        for progress, content in progress_query:
            content_dict = content.to_dict()
            content_dict['user_progress'] = progress.to_dict()
            
            if progress.is_completed:
                library['completed'].append(content_dict)
            elif progress.progress_percentage > 0:
                library['in_progress'].append(content_dict)
            
            if progress.is_liked:
                library['liked'].append(content_dict)
            
            if progress.is_bookmarked:
                library['bookmarked'].append(content_dict)
        
        # Get user's cultural statistics
        stats = {
            'total_content_viewed': len(progress_query),
            'total_completed': len(library['completed']),
            'total_time_spent': sum(p.time_spent_seconds for p, c in progress_query),
            'favorite_themes': get_user_favorite_themes(user_id)
        }
        
        return jsonify({
            'library': library,
            'statistics': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_theme_description(theme):
    """Get description for cultural theme"""
    descriptions = {
        'medieval': 'Explore o xadrez na era medieval, com histórias de cavaleiros e cortes reais.',
        'renaissance': 'Descubra como o xadrez evoluiu durante o Renascimento europeu.',
        'modern': 'Conheça a história moderna do xadrez e seus grandes mestres.',
        'ancient': 'Viaje às origens do xadrez na Índia e Pérsia antigas.',
        'romantic': 'Mergulhe na era romântica do xadrez, com jogos brilhantes e sacrifícios audaciosos.',
        'contemporary': 'Explore o xadrez contemporâneo e suas inovações tecnológicas.'
    }
    return descriptions.get(theme, 'Uma fascinante jornada através da história do xadrez.')

def get_user_favorite_themes(user_id):
    """Get user's favorite cultural themes based on engagement"""
    try:
        theme_engagement = db.session.query(
            CulturalContent.cultural_theme,
            db.func.count(UserContentProgress.id).label('engagement_count'),
            db.func.avg(UserContentProgress.progress_percentage).label('avg_progress')
        ).join(
            UserContentProgress, CulturalContent.id == UserContentProgress.content_id
        ).filter(
            UserContentProgress.user_id == user_id
        ).group_by(
            CulturalContent.cultural_theme
        ).order_by(
            db.desc('engagement_count'), db.desc('avg_progress')
        ).limit(3).all()
        
        return [
            {
                'theme': theme,
                'engagement_count': count,
                'average_progress': float(avg_progress) if avg_progress else 0
            }
            for theme, count, avg_progress in theme_engagement
        ]
    except:
        return []

