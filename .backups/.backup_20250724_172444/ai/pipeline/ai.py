from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.ai_profile import AIProfile, LearningSession
import json
from datetime import datetime, timedelta
import random

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/profile/<int:user_id>', methods=['GET'])
def get_ai_profile(user_id):
    """Get AI profile for a user"""
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            # Create default AI profile
            ai_profile = AIProfile(user_id=user_id)
            db.session.add(ai_profile)
            db.session.commit()
        
        return jsonify({'ai_profile': ai_profile.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/profile/<int:user_id>', methods=['PUT'])
def update_ai_profile(user_id):
    """Update AI profile preferences"""
    data = request.get_json()
    
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            ai_profile = AIProfile(user_id=user_id)
            db.session.add(ai_profile)
        
        # Update allowed fields
        updatable_fields = [
            'learning_style', 'preferred_difficulty', 'coaching_tone',
            'session_duration_preference', 'cultural_interests',
            'adaptation_speed', 'challenge_level', 'support_level',
            'narrative_engagement'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field in ['cultural_interests']:
                    setattr(ai_profile, field, json.dumps(data[field]))
                else:
                    setattr(ai_profile, field, data[field])
        
        ai_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'AI profile updated successfully',
            'ai_profile': ai_profile.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/recommendations/<int:user_id>', methods=['GET'])
def get_personalized_recommendations(user_id):
    """Get personalized recommendations from EstrategiX"""
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            return jsonify({'error': 'AI profile not found'}), 404
        
        recommendations = generate_personalized_recommendations(ai_profile)
        
        return jsonify({
            'recommendations': recommendations,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/coaching/<int:user_id>', methods=['POST'])
def get_coaching_advice():
    """Get personalized coaching advice"""
    user_id = request.view_args['user_id']
    data = request.get_json()
    
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            return jsonify({'error': 'AI profile not found'}), 404
        
        context = data.get('context', 'general')  # 'game', 'lesson', 'analysis', 'general'
        specific_data = data.get('data', {})
        
        coaching_advice = generate_coaching_advice(ai_profile, context, specific_data)
        
        return jsonify({
            'coaching_advice': coaching_advice,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/learning-session', methods=['POST'])
def create_learning_session():
    """Create a new learning session"""
    data = request.get_json()
    
    required_fields = ['user_id', 'session_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        ai_profile = AIProfile.query.filter_by(user_id=data['user_id']).first()
        
        # Generate personalized session content
        session_content = generate_session_content(ai_profile, data['session_type'], data.get('topic'))
        
        session = LearningSession(
            user_id=data['user_id'],
            session_type=data['session_type'],
            topic=session_content['topic'],
            difficulty_level=session_content['difficulty_level'],
            content_data=json.dumps(session_content['content'])
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Learning session created successfully',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/learning-session/<int:session_id>/complete', methods=['POST'])
def complete_learning_session(session_id):
    """Complete a learning session with results"""
    data = request.get_json()
    
    try:
        session = LearningSession.query.get_or_404(session_id)
        
        completion_rate = data.get('completion_rate', 100.0)
        accuracy_score = data.get('accuracy_score')
        
        session.complete_session(completion_rate, accuracy_score)
        
        # Generate AI feedback
        ai_feedback = generate_session_feedback(session, completion_rate, accuracy_score)
        session.ai_feedback = ai_feedback['feedback']
        session.recommended_next_steps = json.dumps(ai_feedback['next_steps'])
        
        # Update AI profile based on session results
        update_ai_profile_from_session(session)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Learning session completed successfully',
            'session': session.to_dict(),
            'ai_feedback': ai_feedback
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/adaptive-difficulty/<int:user_id>', methods=['GET'])
def get_adaptive_difficulty(user_id):
    """Get adaptive difficulty settings for user"""
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            return jsonify({'error': 'AI profile not found'}), 404
        
        difficulty_settings = calculate_adaptive_difficulty(ai_profile)
        
        return jsonify({
            'difficulty_settings': difficulty_settings,
            'calculated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/ai/cultural-narrative/<int:user_id>', methods=['GET'])
def get_cultural_narrative(user_id):
    """Get personalized cultural narrative"""
    try:
        ai_profile = AIProfile.query.filter_by(user_id=user_id).first()
        if not ai_profile:
            return jsonify({'error': 'AI profile not found'}), 404
        
        context = request.args.get('context', 'general')
        narrative = generate_cultural_narrative(ai_profile, context)
        
        return jsonify({
            'narrative': narrative,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_personalized_recommendations(ai_profile):
    """Generate personalized recommendations based on AI profile"""
    recommendations = {
        'training_focus': [],
        'content_suggestions': [],
        'difficulty_adjustments': {},
        'cultural_content': []
    }
    
    # Training focus based on weak areas
    weak_areas = ai_profile.struggling_concepts
    if weak_areas:
        weak_list = json.loads(weak_areas) if isinstance(weak_areas, str) else weak_areas
        for area in weak_list[:3]:  # Top 3 weak areas
            recommendations['training_focus'].append({
                'area': area,
                'priority': 'high',
                'estimated_sessions': random.randint(3, 8),
                'description': f'Foque em melhorar {area} com exercícios específicos'
            })
    
    # Content suggestions based on learning style
    if ai_profile.learning_style == 'visual':
        recommendations['content_suggestions'].extend([
            'Diagramas interativos de posições',
            'Vídeos de análise de partidas',
            'Visualizações de padrões táticos'
        ])
    elif ai_profile.learning_style == 'analytical':
        recommendations['content_suggestions'].extend([
            'Análises profundas de aberturas',
            'Estudos de finais teóricos',
            'Estatísticas de performance'
        ])
    
    # Difficulty adjustments
    recommendations['difficulty_adjustments'] = {
        'current_level': ai_profile.get_personalized_difficulty(),
        'suggested_increase': ai_profile.improvement_rate > 0.1,
        'next_milestone': ai_profile.current_rating + 100
    }
    
    # Cultural content based on interests
    cultural_interests = ai_profile.cultural_interests
    if cultural_interests:
        interests = json.loads(cultural_interests) if isinstance(cultural_interests, str) else cultural_interests
        for interest in interests:
            recommendations['cultural_content'].append({
                'theme': interest,
                'content_type': 'story',
                'estimated_duration': '15-20 minutos'
            })
    
    return recommendations

def generate_coaching_advice(ai_profile, context, specific_data):
    """Generate personalized coaching advice"""
    advice = {
        'message': '',
        'tone': ai_profile.coaching_tone,
        'specific_tips': [],
        'encouragement': '',
        'next_steps': []
    }
    
    # Adjust message based on coaching tone
    if ai_profile.coaching_tone == 'encouraging':
        advice['encouragement'] = "Você está progredindo muito bem! Continue assim!"
    elif ai_profile.coaching_tone == 'analytical':
        advice['encouragement'] = "Vamos analisar seus pontos de melhoria de forma objetiva."
    elif ai_profile.coaching_tone == 'challenging':
        advice['encouragement'] = "Hora de elevar o nível! Você pode fazer melhor."
    else:  # patient
        advice['encouragement'] = "Vamos com calma, cada passo é importante no seu aprendizado."
    
    # Context-specific advice
    if context == 'game':
        if specific_data.get('accuracy_score', 0) < 0.7:
            advice['specific_tips'].append("Dedique mais tempo para calcular as jogadas")
            advice['specific_tips'].append("Verifique se há táticas antes de mover")
        
        advice['next_steps'].append("Pratique posições similares")
        advice['next_steps'].append("Revise a abertura jogada")
    
    elif context == 'lesson':
        topic = specific_data.get('topic', '')
        advice['specific_tips'].append(f"Continue praticando {topic} regularmente")
        advice['next_steps'].append("Aplique o conceito em partidas práticas")
    
    # General advice based on profile
    if ai_profile.games_played < 10:
        advice['message'] = "Foque em jogar mais partidas para ganhar experiência prática."
    elif ai_profile.win_rate < 0.4:
        advice['message'] = "Trabalhe nos fundamentos: controle do centro e desenvolvimento de peças."
    else:
        advice['message'] = "Você está no caminho certo! Vamos refinar sua técnica."
    
    return advice

def generate_session_content(ai_profile, session_type, topic=None):
    """Generate personalized session content"""
    difficulty = ai_profile.get_personalized_difficulty() if ai_profile else 0.5
    
    content = {
        'topic': topic or 'Fundamentos do Xadrez',
        'difficulty_level': difficulty,
        'content': {}
    }
    
    if session_type == 'lesson':
        content['content'] = {
            'introduction': 'Bem-vindo à sua lição personalizada!',
            'objectives': ['Entender conceitos básicos', 'Aplicar na prática'],
            'exercises': [
                {'type': 'position', 'description': 'Encontre a melhor jogada'},
                {'type': 'pattern', 'description': 'Identifique o padrão tático'}
            ],
            'summary': 'Revisão dos pontos principais'
        }
    
    elif session_type == 'practice':
        content['content'] = {
            'warm_up': 'Exercícios de aquecimento',
            'main_practice': 'Prática focada em suas áreas de melhoria',
            'challenges': [
                {'difficulty': 'easy', 'count': 3},
                {'difficulty': 'medium', 'count': 2},
                {'difficulty': 'hard', 'count': 1}
            ]
        }
    
    elif session_type == 'cultural':
        cultural_interests = ai_profile.cultural_interests if ai_profile else '[]'
        interests = json.loads(cultural_interests) if isinstance(cultural_interests, str) else []
        
        theme = random.choice(interests) if interests else 'medieval'
        content['content'] = {
            'theme': theme,
            'story': f'Uma história fascinante sobre o xadrez na era {theme}',
            'historical_context': 'Contexto histórico relevante',
            'chess_connection': 'Como isso se relaciona com o jogo moderno'
        }
    
    return content

def generate_session_feedback(session, completion_rate, accuracy_score):
    """Generate AI feedback for completed session"""
    feedback = {
        'feedback': '',
        'next_steps': []
    }
    
    if completion_rate >= 90:
        feedback['feedback'] = "Excelente! Você completou a sessão com dedicação."
    elif completion_rate >= 70:
        feedback['feedback'] = "Bom trabalho! Continue assim para melhorar ainda mais."
    else:
        feedback['feedback'] = "Não desista! Cada sessão é um passo no seu aprendizado."
    
    if accuracy_score:
        if accuracy_score >= 0.8:
            feedback['feedback'] += " Sua precisão foi impressionante!"
            feedback['next_steps'].append("Tente um nível de dificuldade maior")
        elif accuracy_score >= 0.6:
            feedback['feedback'] += " Boa precisão, continue praticando."
            feedback['next_steps'].append("Revise os conceitos principais")
        else:
            feedback['feedback'] += " Vamos trabalhar mais nesses conceitos."
            feedback['next_steps'].append("Pratique exercícios similares")
            feedback['next_steps'].append("Revise o material teórico")
    
    feedback['next_steps'].append("Continue sua jornada de aprendizado")
    
    return feedback

def calculate_adaptive_difficulty(ai_profile):
    """Calculate adaptive difficulty settings"""
    base_difficulty = ai_profile.get_personalized_difficulty()
    
    settings = {
        'overall_difficulty': base_difficulty,
        'tactical_difficulty': base_difficulty,
        'positional_difficulty': base_difficulty,
        'endgame_difficulty': base_difficulty,
        'time_pressure': base_difficulty * 0.8,
        'hint_frequency': 1.0 - base_difficulty,
        'explanation_detail': ai_profile.support_level
    }
    
    # Adjust based on strong/weak areas
    strong_areas = ai_profile.strong_areas
    weak_areas = ai_profile.weak_areas
    
    if strong_areas:
        strong_list = json.loads(strong_areas) if isinstance(strong_areas, str) else strong_areas
        for area in strong_list:
            if 'tactical' in area.lower():
                settings['tactical_difficulty'] = min(1.0, base_difficulty + 0.2)
            elif 'endgame' in area.lower():
                settings['endgame_difficulty'] = min(1.0, base_difficulty + 0.2)
    
    if weak_areas:
        weak_list = json.loads(weak_areas) if isinstance(weak_areas, str) else weak_areas
        for area in weak_list:
            if 'tactical' in area.lower():
                settings['tactical_difficulty'] = max(0.1, base_difficulty - 0.2)
            elif 'endgame' in area.lower():
                settings['endgame_difficulty'] = max(0.1, base_difficulty - 0.2)
    
    return settings

def generate_cultural_narrative(ai_profile, context):
    """Generate personalized cultural narrative"""
    cultural_interests = ai_profile.cultural_interests if ai_profile else '[]'
    interests = json.loads(cultural_interests) if isinstance(cultural_interests, str) else []
    
    theme = random.choice(interests) if interests else 'renaissance'
    
    narratives = {
        'medieval': {
            'title': 'O Xadrez nas Cortes Medievais',
            'content': 'No período medieval, o xadrez era conhecido como o "jogo dos reis"...',
            'lesson': 'Assim como os cavaleiros medievais, cada peça tem seu papel único no tabuleiro.'
        },
        'renaissance': {
            'title': 'O Renascimento do Xadrez',
            'content': 'Durante o Renascimento, o xadrez evoluiu significativamente...',
            'lesson': 'A criatividade renascentista nos ensina a pensar fora da caixa no xadrez.'
        },
        'modern': {
            'title': 'O Xadrez na Era Moderna',
            'content': 'Com o advento da tecnologia, o xadrez ganhou novas dimensões...',
            'lesson': 'A tecnologia moderna nos permite estudar o jogo com precisão científica.'
        }
    }
    
    selected_narrative = narratives.get(theme, narratives['renaissance'])
    
    return {
        'theme': theme,
        'title': selected_narrative['title'],
        'content': selected_narrative['content'],
        'chess_lesson': selected_narrative['lesson'],
        'engagement_level': ai_profile.narrative_engagement if ai_profile else 0.5
    }

def update_ai_profile_from_session(session):
    """Update AI profile based on learning session results"""
    ai_profile = AIProfile.query.filter_by(user_id=session.user_id).first()
    if not ai_profile:
        return
    
    # Update learning progress
    if session.completion_rate >= 80:
        ai_profile.add_completed_lesson(session.id)
        
        if session.accuracy_score and session.accuracy_score >= 0.8:
            if session.topic:
                ai_profile.add_mastered_concept(session.topic)
    
    elif session.completion_rate < 50:
        if session.topic:
            ai_profile.add_struggling_concept(session.topic)
    
    # Update session preferences
    if session.time_spent_seconds > 0:
        preferred_duration = session.time_spent_seconds // 60  # Convert to minutes
        # Gradually adjust preferred session duration
        current_pref = ai_profile.session_duration_preference
        ai_profile.session_duration_preference = int((current_pref + preferred_duration) / 2)
    
    ai_profile.last_interaction = datetime.utcnow()
    db.session.commit()

