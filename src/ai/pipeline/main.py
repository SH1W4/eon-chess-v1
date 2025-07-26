import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.game import game_bp
from src.routes.ai import ai_bp
from src.routes.cultural import cultural_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'xadrezmaster_secret_key_2024'

# Enable CORS for all routes
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(game_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')
app.register_blueprint(cultural_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import all models to ensure they're registered
from src.models.game import Game, GameAnalysis
from src.models.ai_profile import AIProfile, LearningSession
from src.models.cultural_content import CulturalContent, UserContentProgress, CulturalEvent

with app.app_context():
    # Create all tables first
    db.create_all()
    
    # Then create sample data if database is empty
    try:
        if not db.session.query(CulturalContent).first():
            create_sample_data()
    except Exception as e:
        print(f"Error checking/creating sample data: {e}")
        # Create sample data anyway
        create_sample_data()

def create_sample_data():
    """Create sample cultural content and events"""
    from datetime import datetime, timedelta
    import json
    
    # Sample cultural content
    sample_contents = [
        {
            'title': 'O Xadrez na Corte de Carlos Magno',
            'content_type': 'story',
            'category': 'general',
            'description': 'Uma fascinante história sobre como o xadrez chegou à Europa medieval.',
            'content_body': '''
# O Xadrez na Corte de Carlos Magno

No século VIII, quando Carlos Magno governava o Sacro Império Romano, o xadrez começou sua jornada pela Europa. Trazido pelos mouros através da Península Ibérica, este jogo misterioso rapidamente capturou a imaginação da nobreza europeia.

## A Chegada do Jogo dos Reis

O xadrez, conhecido então como "shatranj", era muito diferente do jogo que conhecemos hoje. As peças tinham nomes e movimentos distintos, mas a essência estratégica já estava presente.

## Lições para o Jogador Moderno

Assim como Carlos Magno precisava pensar estrategicamente para governar seu vasto império, o jogador de xadrez deve:

- Planejar com antecedência
- Proteger seus recursos mais valiosos
- Coordenar suas forças
- Adaptar-se às mudanças no "campo de batalha"
            ''',
            'historical_period': 'medieval',
            'cultural_theme': 'medieval',
            'geographical_origin': 'Europa',
            'related_openings': json.dumps(['Italian Game', 'Spanish Opening']),
            'chess_concepts': json.dumps(['strategy', 'planning', 'piece_coordination']),
            'difficulty_level': 2,
            'author': 'Dr. Maria Santos',
            'tags': json.dumps(['história', 'medieval', 'estratégia']),
            'is_published': True,
            'is_premium': False
        },
        {
            'title': 'A Dama Poderosa: Evolução da Rainha no Xadrez',
            'content_type': 'historical',
            'category': 'general',
            'description': 'Como a peça mais poderosa do xadrez evoluiu ao longo dos séculos.',
            'content_body': '''
# A Evolução da Rainha no Xadrez

A rainha do xadrez nem sempre foi a peça mais poderosa do tabuleiro. Sua transformação reflete mudanças sociais e culturais fascinantes.

## Do Conselheiro à Rainha

Originalmente, a peça era chamada de "firzan" (conselheiro) e tinha movimentos muito limitados. A transformação para "rainha" aconteceu na Europa medieval.

## O Poder Feminino no Tabuleiro

A evolução da rainha coincidiu com o período de rainhas poderosas como Isabel de Castela, refletindo o crescente reconhecimento do poder feminino.

## Aplicação Prática

No jogo moderno, a rainha ensina:
- O valor da versatilidade
- A importância do timing
- Como usar o poder com responsabilidade
            ''',
            'historical_period': 'renaissance',
            'cultural_theme': 'renaissance',
            'geographical_origin': 'Europa',
            'related_openings': json.dumps(['Queen\'s Gambit', 'Queen\'s Indian']),
            'chess_concepts': json.dumps(['piece_value', 'queen_power', 'tactics']),
            'difficulty_level': 3,
            'author': 'Prof. João Silva',
            'tags': json.dumps(['história', 'rainha', 'evolução']),
            'is_published': True,
            'is_premium': True
        },
        {
            'title': 'Filosofia do Xadrez: Lições de Vida no Tabuleiro',
            'content_type': 'philosophical',
            'category': 'general',
            'description': 'Como o xadrez pode ensinar importantes lições de vida e filosofia.',
            'content_body': '''
# Filosofia do Xadrez: Lições de Vida

O xadrez é mais que um jogo - é uma metáfora da vida, repleta de lições profundas sobre estratégia, paciência e crescimento pessoal.

## A Arte da Paciência

Cada movimento no xadrez requer reflexão. Assim como na vida, as decisões precipitadas frequentemente levam a consequências indesejadas.

## Aceitando as Perdas

No xadrez, às vezes devemos sacrificar peças para alcançar um objetivo maior. Esta lição se aplica diretamente às escolhas que fazemos na vida.

## O Crescimento Através dos Erros

Cada partida perdida é uma oportunidade de aprendizado. Os grandes mestres não nasceram perfeitos - eles aprenderam com cada erro.

## Aplicação Prática

- Desenvolva paciência através da análise cuidadosa
- Aprenda a ver oportunidades em situações difíceis
- Cultive a resiliência através da prática constante
            ''',
            'historical_period': 'contemporary',
            'cultural_theme': 'philosophical',
            'geographical_origin': 'Universal',
            'related_openings': json.dumps(['any']),
            'chess_concepts': json.dumps(['philosophy', 'life_lessons', 'mindset']),
            'difficulty_level': 1,
            'author': 'Mestre Ana Costa',
            'tags': json.dumps(['filosofia', 'vida', 'crescimento']),
            'is_published': True,
            'is_premium': False
        }
    ]
    
    for content_data in sample_contents:
        content = CulturalContent(**content_data)
        db.session.add(content)
    
    # Sample cultural events
    now = datetime.utcnow()
    sample_events = [
        {
            'title': 'Noite Medieval de Xadrez',
            'description': 'Uma noite especial jogando xadrez com regras e peças medievais.',
            'event_type': 'tournament',
            'cultural_theme': 'medieval',
            'difficulty_level': 2,
            'max_participants': 20,
            'start_time': now + timedelta(days=7),
            'end_time': now + timedelta(days=7, hours=3),
            'content_data': json.dumps({
                'rules': 'Regras medievais adaptadas',
                'prizes': 'Certificados temáticos',
                'dress_code': 'Opcional: trajes medievais'
            }),
            'host_name': 'Mestre Carlos Medieval',
            'is_premium': False
        },
        {
            'title': 'Masterclass: Estratégias Renascentistas',
            'description': 'Aprenda estratégias inspiradas nos grandes pensadores do Renascimento.',
            'event_type': 'masterclass',
            'cultural_theme': 'renaissance',
            'difficulty_level': 4,
            'max_participants': 15,
            'start_time': now + timedelta(days=14),
            'end_time': now + timedelta(days=14, hours=2),
            'content_data': json.dumps({
                'topics': ['Estratégia de Leonardo da Vinci', 'Táticas de Maquiavel'],
                'materials': 'Apostila digital incluída'
            }),
            'host_name': 'GM Isabella Renaissance',
            'is_premium': True
        }
    ]
    
    for event_data in sample_events:
        event = CulturalEvent(**event_data)
        db.session.add(event)
    
    db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'XadrezMaster API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

