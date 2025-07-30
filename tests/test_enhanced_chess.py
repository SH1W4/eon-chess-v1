"""Testes do sistema de xadrez aprimorado"""
import pytest
from src.core.models import Position, Piece, PieceType, Color
from src.core.orchestration.chess_orchestrator import ChessOrchestrator
from src.core.quantum.quantum_enhancements import EnhancedQuantumField

def test_enhanced_chess_analysis():
    """Testa análise avançada de posição de xadrez"""
    # Inicializa orquestrador
    orchestrator = ChessOrchestrator()
    
    # Cria posição de teste (Ruy Lopez)
    pieces = {
        # Peças brancas
        Position(1, 5): Piece(PieceType.KING, Color.WHITE, Position(1, 5)),
        Position(1, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(1, 4)),
        Position(4, 3): Piece(PieceType.BISHOP, Color.WHITE, Position(4, 3)),  # Bispo atacando
        Position(2, 4): Piece(PieceType.PAWN, Color.WHITE, Position(2, 4)),    # Peão central
        
        # Peças pretas
        Position(8, 5): Piece(PieceType.KING, Color.BLACK, Position(8, 5)),
        Position(8, 4): Piece(PieceType.QUEEN, Color.BLACK, Position(8, 4)),
        Position(6, 3): Piece(PieceType.KNIGHT, Color.BLACK, Position(6, 3)),  # Cavalo defensivo
        Position(7, 4): Piece(PieceType.PAWN, Color.BLACK, Position(7, 4)),    # Peão central
    }
    
    # Realiza análise
    analysis = orchestrator.analyze_position(pieces, Color.WHITE)
    
    # Validações
    assert analysis.position_evaluation is not None
    assert analysis.position_dynamics is not None
    assert isinstance(analysis.strategic_assessment, str)
    assert len(analysis.strategic_assessment) > 0
    
    # Verifica métricas quânticas
    assert 0 <= analysis.quantum_metrics['field_coherence'] <= 1
    assert 0 <= analysis.quantum_metrics['position_stability'] <= 1
    assert 0 <= analysis.quantum_metrics['tactical_density'] <= 1
    
    # Verifica avaliação posicional
    assert isinstance(analysis.position_evaluation.material_score, float)
    assert isinstance(analysis.position_evaluation.control_score, float)
    assert isinstance(analysis.position_evaluation.mobility_score, float)
    assert isinstance(analysis.position_evaluation.king_safety_score, float)
    assert isinstance(analysis.position_evaluation.pawn_structure_score, float)
    
    # Verifica dinâmicas
    assert 'center_control' in analysis.position_dynamics
    assert 'piece_coordination' in analysis.position_dynamics
    assert 'attacking_potential' in analysis.position_dynamics
    assert 'defensive_solidity' in analysis.position_dynamics

def test_enhanced_quantum_field():
    """Testa funcionalidades avançadas do campo quântico"""
    field = EnhancedQuantumField()
    
    # Cria posição de teste com mais proteção para o rei branco
    pieces = {
        Position(1, 5): Piece(PieceType.KING, Color.WHITE, Position(1, 5)),
        Position(2, 5): Piece(PieceType.PAWN, Color.WHITE, Position(2, 5)),   # Peão protegendo rei
        Position(1, 4): Piece(PieceType.QUEEN, Color.WHITE, Position(1, 4)),  # Dama protetora
        Position(1, 6): Piece(PieceType.BISHOP, Color.WHITE, Position(1, 6)), # Bispo protetor
        Position(8, 5): Piece(PieceType.KING, Color.BLACK, Position(8, 5)),   # Rei preto desprotegido
    }
    
    # Atualiza campo
    field.update_field(pieces)
    
    # Testa análise de segurança do rei
    white_safety = field.analyze_king_safety(Color.WHITE, Position(1, 5))
    black_safety = field.analyze_king_safety(Color.BLACK, Position(8, 5))
    
    # O rei branco deve estar mais seguro por ter um peão de proteção
    assert white_safety > black_safety
    
    # Testa análise de estrutura de peões
    white_structure = field.analyze_pawn_structure(Color.WHITE)
    black_structure = field.analyze_pawn_structure(Color.BLACK)
    
    # Estrutura branca deve ser melhor por ter pelo menos um peão
    assert white_structure > black_structure
    
    # Testa avaliação completa
    evaluation = field.evaluate_position(pieces)
    assert evaluation.total_score != 0  # Deve haver alguma avaliação
    
if __name__ == '__main__':
    pytest.main([__file__])
