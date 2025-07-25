import pytest
import numpy as np
from src.core.engine import ChessEngine, Position, Piece, Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile, EvaluationWeights

def test_player_profile_initialization():
    profile = PlayerProfile()
    
    assert profile.aggression == 0.5
    assert profile.risk_taking == 0.5
    assert profile.positional == 0.5
    assert profile.games_played == 0
    assert profile.wins == 0
    assert profile.losses == 0
    assert profile.draws == 0
    
    assert isinstance(profile.piece_preferences, dict)
    assert len(profile.piece_preferences) == 5  # pawn, knight, bishop, rook, queen
    assert all(value == 1.0 for value in profile.piece_preferences.values())
    
    assert isinstance(profile.favorite_openings, list)
    assert len(profile.favorite_openings) == 0

def test_ai_initialization():
    ai = AdaptiveAI()
    
    assert isinstance(ai.profile, PlayerProfile)
    assert isinstance(ai.weights, EvaluationWeights)
    assert ai.learning_rate == 0.1
    assert isinstance(ai.position_history, list)
    assert isinstance(ai.move_times, list)
    assert isinstance(ai.position_tables, dict)

def test_position_tables():
    ai = AdaptiveAI()
    
    # Verificar se todas as tabelas necessárias existem
    required_tables = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king_midgame', 'king_endgame']
    for table_name in required_tables:
        assert table_name in ai.position_tables
        assert isinstance(ai.position_tables[table_name], np.ndarray)
        assert ai.position_tables[table_name].shape == (8, 8)

def test_evaluate_position():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Avaliação da posição inicial
    score = ai.evaluate_position(engine, 'white')
    assert isinstance(score, float)
    
    # Fazer um movimento e avaliar nova posição
    move = Move(Position(6, 4), Position(4, 4), engine.get_piece(Position(6, 4)))  # e4
    engine.make_move(move)
    
    new_score = ai.evaluate_position(engine, 'white')
    assert isinstance(new_score, float)
    assert new_score != score  # A avaliação deve mudar após um movimento

def test_get_best_move():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Obter melhor movimento na posição inicial
    move = ai.get_best_move(engine)
    assert isinstance(move, Move)
    assert engine._is_legal_move(move)
    
    # Verificar se o movimento é executável
    assert engine.make_move(move)

def test_evaluate_components():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Testar avaliação de mobilidade
    mobility = ai._evaluate_mobility(engine, 'white')
    assert isinstance(mobility, float)
    assert mobility > 0  # Na posição inicial, deve haver movimentos disponíveis
    
    # Testar avaliação de segurança do rei
    king_safety = ai._evaluate_king_safety(engine, 'white')
    assert isinstance(king_safety, float)
    assert king_safety > 0  # Na posição inicial, o rei deve estar relativamente seguro
    
    # Testar avaliação de estrutura de peões
    pawn_structure = ai._evaluate_pawn_structure(engine, 'white')
    assert isinstance(pawn_structure, float)
    
    # Testar avaliação de controle do centro
    center_control = ai._evaluate_center_control(engine, 'white')
    assert isinstance(center_control, float)

def test_profile_update():
    ai = AdaptiveAI()
    opponent_profile = PlayerProfile(
        aggression=0.8,
        risk_taking=0.7,
        positional=0.6
    )
    
    # Simular uma vitória
    ai.update_profile('win', opponent_profile)
    assert ai.profile.games_played == 1
    assert ai.profile.wins == 1
    
    # Verificar adaptação do perfil
    assert ai.profile.aggression != 0.5  # Deve ter se adaptado ao oponente
    assert ai.profile.risk_taking != 0.5  # Deve ter se adaptado ao oponente

def test_profile_save_load(tmp_path):
    # Criar perfil inicial
    original_ai = AdaptiveAI()
    original_ai.profile.wins = 5
    original_ai.profile.games_played = 10
    original_ai.profile.aggression = 0.7
    
    # Salvar perfil
    save_path = tmp_path / "test_profile.json"
    original_ai.save_profile(str(save_path))
    
    # Carregar perfil
    loaded_ai = AdaptiveAI.load_profile(str(save_path))
    
    # Verificar se os dados foram preservados
    assert loaded_ai.profile.wins == 5
    assert loaded_ai.profile.games_played == 10
    assert loaded_ai.profile.aggression == 0.7

def test_adaptive_behavior():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Configurar perfil mais agressivo
    ai.profile.aggression = 0.8
    ai.profile.risk_taking = 0.7
    
    # Obter movimento com perfil agressivo
    aggressive_move = ai.get_best_move(engine)
    
    # Resetar engine
    engine = ChessEngine()
    
    # Configurar perfil mais defensivo
    ai.profile.aggression = 0.2
    ai.profile.risk_taking = 0.3
    
    # Obter movimento com perfil defensivo
    defensive_move = ai.get_best_move(engine)
    
    # Os movimentos devem ser diferentes devido aos diferentes perfis
    assert (aggressive_move.from_pos != defensive_move.from_pos or 
            aggressive_move.to_pos != defensive_move.to_pos)
