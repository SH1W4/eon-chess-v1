import pytest
import numpy as np
from typing import List, Optional
from src.core.engine import ChessEngine
from src.core.board.board import Board, Position, Piece, Color
from src.core.board.move import Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile, EvaluationWeights

# Mock para ChessEngine nos testes
class MockMove:
    def __init__(self, from_pos: Position, to_pos: Position, piece: Piece):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece = piece
        self.captured_piece = None
        self.is_castling = False
        self.is_en_passant = False
        self.promotion_piece = None

class MockChessEngine:
    def __init__(self):
        self.current_player = 'white'
        self.board = Board()  # Use actual Board class
        self.move_history = []
        self._setup_initial_position()
    
    def _setup_initial_position(self):
        # Board will handle the initial setup
        pass
    
    def get_piece(self, pos: Position) -> Optional[Piece]:
        return self.board.get_piece(pos)
    
    def make_move(self, move: MockMove) -> bool:
        if not self._is_legal_move(move):
            return False
        
        # Mock move execution
        from_pos = move.from_pos
        to_pos = move.to_pos
        piece = self.get_piece(from_pos)
        self.board.squares[(from_pos.file, from_pos.rank)] = None
        self.board.squares[(to_pos.file, to_pos.rank)] = piece
        if piece:
            piece.position = to_pos
        self.move_history.append(move)
        return True
    
    def get_legal_moves(self, pos: Position) -> List[Position]:
        piece = self.get_piece(pos)
        if not piece:
            return []
        
        moves = []
        for rank in range(8):
            for file in range(8):
                to_pos = Position(file=file, rank=rank)
                move = MockMove(from_pos=pos, to_pos=to_pos, piece=piece)
                if self._is_legal_move(move):
                    moves.append(to_pos)
        return moves
    
    def _is_legal_move(self, move: MockMove) -> bool:
        return True

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
    
    # Initial position evaluation from White's perspective
    initial_score = ai.evaluate_position(engine.board, Color.WHITE)
    assert isinstance(initial_score, float)
    
    # Move e2 to e4 and evaluate new position
    move = Move(
        Position(6, 4),  # e2
        Position(4, 4),  # e4
        engine.get_piece(Position(6, 4))
    )
    engine.make_move(move)
    
    # New position evaluation after e4
    new_score = ai.evaluate_position(engine.board, Color.WHITE)
    assert isinstance(new_score, float)
    assert new_score > initial_score  # Score should improve after e4 due to center control
    
    # Verify position evaluation for Black's perspective
    black_score = ai.evaluate_position(engine.board, Color.BLACK)
    assert black_score < 0  # Black should have negative score due to White's advantage

def test_get_best_move():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Obter melhor movimento na posição inicial
    move = ai.get_best_move(engine.board)
    assert isinstance(move, Move)
    assert engine._is_legal_move(move)
    
    # Verificar se o movimento é executável
    assert engine.make_move(move)

def test_evaluate_components():
    engine = ChessEngine()
    ai = AdaptiveAI()
    
    # Testar avaliação de mobilidade
    mobility = ai._evaluate_mobility(engine.board, Color.WHITE)
    assert isinstance(mobility, float)
    assert mobility > 0  # Na posição inicial, deve haver movimentos disponíveis
    
    # Testar avaliação de segurança do rei
    king_safety = ai._evaluate_king_safety(engine.board)
    assert isinstance(king_safety, float)
    assert king_safety > 0  # Na posição inicial, o rei deve estar relativamente seguro
    
    # Testar avaliação de estrutura de peões
    pawn_structure = ai._evaluate_pawn_structure(engine.board, Color.WHITE)
    assert isinstance(pawn_structure, float)
    
    # Testar avaliação de controle do centro
    center_control = ai._evaluate_center_control(engine.board, Color.WHITE)
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
    aggressive_move = ai.get_best_move(engine.board)
    
    # Configurar perfil mais defensivo
    ai.profile.aggression = 0.2
    ai.profile.risk_taking = 0.3
    
    # Obter movimento com perfil defensivo
    defensive_move = ai.get_best_move(engine.board)
    
    # Os movimentos devem ser diferentes devido aos diferentes perfis
    assert (aggressive_move.from_pos != defensive_move.from_pos or 
            aggressive_move.to_pos != defensive_move.to_pos)
