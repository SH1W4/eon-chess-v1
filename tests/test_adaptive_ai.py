import pytest
import numpy as np
from typing import List, Optional
from src.core.engine import ChessEngine
from src.core.board.board import Board, Position, Piece, Color, PieceType
from src.core.board.move import Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile, EvaluationWeights, LearningMode
from src.core.board.board import PieceType

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
    
    def make_move(self, move: MockMove) -> bool:
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
    
    def get_legal_moves(self, pos: Position) -> List[Position]:
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
    for piece_type in [pt for pt in PieceType if pt != PieceType.KING]:
        assert piece_type in ai.position_tables
        assert isinstance(ai.position_tables[piece_type], np.ndarray)
        assert ai.position_tables[piece_type].shape == (8, 8)
    
    # Verificar tabelas especiais do rei
    assert 'king_midgame' in ai.position_tables
    assert 'king_endgame' in ai.position_tables
    assert ai.position_tables['king_midgame'].shape == (8, 8)
    assert ai.position_tables['king_endgame'].shape == (8, 8)

def test_learning_modes():
    # Testar modo passivo
    ai_passive = AdaptiveAI(
        profile=PlayerProfile(learning_mode=LearningMode.PASSIVE)
    )
    assert ai_passive.profile.learning_mode == LearningMode.PASSIVE
    
    # Testar modo ativo
    ai_active = AdaptiveAI(
        profile=PlayerProfile(learning_mode=LearningMode.ACTIVE)
    )
    assert ai_active.profile.learning_mode == LearningMode.ACTIVE
    
    # Testar modo agressivo
    ai_aggressive = AdaptiveAI(
        profile=PlayerProfile(learning_mode=LearningMode.AGGRESSIVE)
    )
    assert ai_aggressive.profile.learning_mode == LearningMode.AGGRESSIVE

def test_evolution_cycles():
    # Criar IA com ciclos evolutivos
    ai = AdaptiveAI(
        profile=PlayerProfile(
            evolution_cycles=3,
            learning_mode=LearningMode.ACTIVE
        )
    )
    
    # Simular alguns jogos
    for _ in range(5):
        ai.game_memory.append({
            'result': 'win',
            'aggression': 0.7,
            'positional': 0.6,
            'risk_taking': 0.8
        })
    
    # Guardar valores iniciais
    initial_aggression = ai.profile.aggression
    initial_positional = ai.profile.positional
    initial_risk_taking = ai.profile.risk_taking
    
    # Atualizar perfil com ciclos evolutivos
    engine = ChessEngine()
    ai.update_profile(engine.board, 'win')
    
    # Verificar se os valores mudaram
    assert ai.profile.aggression != initial_aggression
    assert ai.profile.positional != initial_positional
    assert ai.profile.risk_taking != initial_risk_taking

def test_evaluate_position():
    board = Board()
    ai = AdaptiveAI()

    # Add some pieces for testing
    board.pieces = {
        (4, 4): Piece(PieceType.PAWN, Color.WHITE),
        (3, 3): Piece(PieceType.BISHOP, Color.WHITE),
        (1, 1): Piece(PieceType.KING, Color.BLACK)
    }

    # White should have advantage due to material and position
    score = ai.evaluate_position(board, Color.WHITE)
    assert score > 0

    # From black's perspective, score should be negative
    black_score = ai.evaluate_position(board, Color.BLACK)
    assert black_score < 0

def test_get_best_move():
    board = Board()
    ai = AdaptiveAI()

    # Setup a simple position
    board.pieces = {
        (1, 1): Piece(PieceType.KING, Color.WHITE),
        (3, 3): Piece(PieceType.QUEEN, Color.WHITE),
        (6, 6): Piece(PieceType.KING, Color.BLACK)
    }

    # Get best move for white
    move = ai.get_best_move(board, Color.WHITE)
    assert isinstance(move, Move)
    assert move.piece.type == PieceType.QUEEN  # Queen should move

def test_evaluate_mobility():
    board = Board()
    ai = AdaptiveAI()

    # Setup pieces with known mobility
    board.pieces = {
        (3, 3): Piece(PieceType.QUEEN, Color.WHITE),  # Queen has high mobility
        (0, 0): Piece(PieceType.PAWN, Color.BLACK)   # Pawn has low mobility
    }

    # White should have higher mobility score
    white_mobility = ai._evaluate_mobility(board, Color.WHITE)
    black_mobility = ai._evaluate_mobility(board, Color.BLACK)
    assert white_mobility > black_mobility

def test_profile_update():
    board = Board()
    ai = AdaptiveAI(
        profile=PlayerProfile(
            learning_mode=LearningMode.AGGRESSIVE,
            evolution_cycles=2
        )
    )

    # Add some moves to test aggressive behavior
    board.pieces = {
        (4, 4): Piece(PieceType.QUEEN, Color.WHITE),
        (6, 6): Piece(PieceType.PAWN, Color.BLACK)
    }

    # Record initial values
    initial_aggression = ai.profile.aggression
    initial_risk_taking = ai.profile.risk_taking

    # Update profile with a win
    ai.update_profile(board, 'win')

    # Check that profile was updated
    assert ai.profile.wins == 1
    assert ai.profile.games_played == 1
    assert ai.profile.aggression != initial_aggression
    assert ai.profile.risk_taking != initial_risk_taking

def test_profile_save_load(tmp_path):
    # Criar perfil inicial com modo de aprendizado
    original_ai = AdaptiveAI(
        profile=PlayerProfile(
            aggression=0.7,
            learning_mode=LearningMode.ACTIVE,
            evolution_cycles=3
        )
    )
    original_ai.profile.wins = 5
    original_ai.profile.games_played = 10
    
    # Adicionar alguns jogos à memória
    original_ai.game_memory.append({
        'result': 'win',
        'aggression': 0.8,
        'positional': 0.6,
        'risk_taking': 0.7
    })
    
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
    board = Board()
    
    # Create an aggressive AI
    aggressive_ai = AdaptiveAI(
        profile=PlayerProfile(
            learning_mode=LearningMode.AGGRESSIVE,
            aggression=0.8,
            risk_taking=0.7
        )
    )
    
    # Create a passive AI
    passive_ai = AdaptiveAI(
        profile=PlayerProfile(
            learning_mode=LearningMode.PASSIVE,
            aggression=0.2,
            risk_taking=0.3
        )
    )
    
    # Setup a position with capture opportunities
    board.pieces = {
        (3, 3): Piece(PieceType.QUEEN, Color.WHITE),
        (4, 4): Piece(PieceType.PAWN, Color.BLACK),
        (2, 2): Piece(PieceType.PAWN, Color.BLACK)
    }
    
    # Get moves from both AIs
    aggressive_move = aggressive_ai.get_best_move(board, Color.WHITE)
    passive_move = passive_ai.get_best_move(board, Color.WHITE)
    
    # Moves should be different due to different profiles
    assert (aggressive_move.from_pos != passive_move.from_pos or 
            aggressive_move.to_pos != passive_move.to_pos)
