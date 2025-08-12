"""Orquestrador do sistema de xadrez integrado com ARQUIMAX e NEXUS"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from ..models import Position, Piece, Color
from ..quantum.quantum_enhancements import EnhancedQuantumField, PositionEvaluation
from ..quantum.quantum_field import CONTROL_THRESHOLD
from ...nexus.core import NexusCore
from ...arquimax.config import ArquimaxConfigManager

@dataclass
class ChessAnalysis:
    """Análise completa de uma posição de xadrez"""
    position_evaluation: PositionEvaluation
    position_dynamics: Dict[str, float]
    suggested_moves: List[Tuple[Position, Position]]
    strategic_assessment: str
    quantum_metrics: Dict[str, float]

class ChessOrchestrator:
    """Orquestrador do sistema de xadrez com integração ARQUIMAX-NEXUS"""
    
    def __init__(self):
        """Inicializa o orquestrador"""
        self.quantum_field = EnhancedQuantumField()
        self.nexus = NexusCore()
        self.config_manager = ArquimaxConfigManager()
        
        # Ativa sistemas
        self.nexus.activate()
        self._setup_arquimax()
    
    def _setup_arquimax(self):
        """Configura sistema ARQUIMAX"""
        monitoring_config = {
            'accuracy_threshold': 0.75,
            'adaptation_rate': 0.2,
            'sampling_rate': 2.0,
            'metrics_collection': True
        }
        self.config_manager.update_config(monitoring=monitoring_config)
    
    def analyze_position(self, pieces: Dict[Position, Piece], current_turn: Color) -> ChessAnalysis:
        """Realiza análise completa da posição"""
        # Atualiza campo quântico
        self.quantum_field.update_field(pieces)
        
        # Avalia posição
        position_eval = self.quantum_field.evaluate_position(pieces)
        
        # Analisa dinâmica
        dynamics = self.quantum_field.get_position_dynamics(pieces)
        
        # Gera sugestões de movimento
        suggested_moves = self._generate_move_suggestions(pieces, current_turn)
        
        # Avaliação estratégica
        assessment = self._generate_strategic_assessment(position_eval, dynamics)
        
        # Métricas quânticas
        quantum_metrics = {
            'field_coherence': self._calculate_field_coherence(),
            'position_stability': self._calculate_position_stability(),
            'tactical_density': self._calculate_tactical_density()
        }
        
        return ChessAnalysis(
            position_evaluation=position_eval,
            position_dynamics=dynamics,
            suggested_moves=suggested_moves,
            strategic_assessment=assessment,
            quantum_metrics=quantum_metrics
        )
    
    def _generate_move_suggestions(
        self, 
        pieces: Dict[Position, Piece], 
        current_turn: Color
    ) -> List[Tuple[Position, Position]]:
        """Gera sugestões de movimentos ordenadas por qualidade"""
        suggestions = []
        
        # Coleta todos os movimentos possíveis
        for pos, piece in pieces.items():
            if piece.color == current_turn:
                # Simula cada movimento possível
                for new_pos in self._get_valid_moves(pos, pieces):
                    # Faz movimento temporário
                    temp_pieces = pieces.copy()
                    temp_pieces[new_pos] = piece
                    del temp_pieces[pos]
                    
                    # Avalia nova posição
                    self.quantum_field.update_field(temp_pieces)
                    eval_after = self.quantum_field.evaluate_position(temp_pieces)
                    
                    # Adiciona à lista de sugestões
                    suggestions.append((
                        pos, 
                        new_pos, 
                        eval_after.total_score if current_turn == Color.WHITE 
                        else -eval_after.total_score
                    ))
        
        # Ordena por avaliação
        suggestions.sort(key=lambda x: x[2], reverse=True)
        
        # Retorna apenas as posições, sem o score
        return [(s[0], s[1]) for s in suggestions[:5]]  # Top 5 movimentos
    
    def _generate_strategic_assessment(
        self, 
        eval: PositionEvaluation,
        dynamics: Dict[str, float]
    ) -> str:
        """Gera avaliação estratégica em linguagem natural"""
        assessment = []
        
        # Avalia vantagem material
        if abs(eval.material_score) > 1.5:
            side = "Brancas" if eval.material_score > 0 else "Pretas"
            assessment.append(f"{side} têm vantagem material significativa")
        
        # Avalia controle posicional
        if abs(eval.control_score) > 0.5:
            side = "Brancas" if eval.control_score > 0 else "Pretas"
            assessment.append(f"{side} controlam mais território")
        
        # Avalia segurança dos reis
        if abs(eval.king_safety_score) > 1.0:
            side = "Brancas" if eval.king_safety_score > 0 else "Pretas"
            assessment.append(f"Rei das {side} está mais seguro")
        
        # Avalia estrutura de peões
        if abs(eval.pawn_structure_score) > 0.3:
            side = "Brancas" if eval.pawn_structure_score > 0 else "Pretas"
            assessment.append(f"{side} têm melhor estrutura de peões")
        
        # Avalia dinâmica da posição
        if dynamics['center_control'] > 0.5:
            assessment.append("Brancas controlam o centro")
        elif dynamics['center_control'] < -0.5:
            assessment.append("Pretas controlam o centro")
        
        if dynamics['attacking_potential'] > 1.0:
            assessment.append("Brancas têm potencial de ataque")
        elif dynamics['attacking_potential'] < -1.0:
            assessment.append("Pretas têm potencial de ataque")
        
        return ". ".join(assessment) + "."
    
    def _calculate_field_coherence(self) -> float:
        """Calcula coerência do campo quântico"""
        white_coherence = np.sum(self.quantum_field.white_influence > 0.5)
        black_coherence = np.sum(self.quantum_field.black_influence > 0.5)
        return (white_coherence + black_coherence) / 128  # Normalizado
    
    def _calculate_position_stability(self) -> float:
        """Calcula estabilidade da posição"""
        # Média das influências fortes (acima do threshold)
        white_stable = np.mean(self.quantum_field.white_influence > CONTROL_THRESHOLD)
        black_stable = np.mean(self.quantum_field.black_influence > CONTROL_THRESHOLD)
        return (white_stable + black_stable) / 2
    
    def _calculate_tactical_density(self) -> float:
        """Calcula densidade tática da posição"""
        # Soma das áreas com sobreposição de influências
        overlap = (self.quantum_field.white_influence > 0) & (self.quantum_field.black_influence > 0)
        return np.sum(overlap) / 64  # Normalizado
    
    def _get_valid_moves(self, pos: Position, pieces: Dict[Position, Piece]) -> List[Position]:
        """Obtém movimentos válidos para uma posição"""
        # TODO: Implementar lógica de movimentos válidos
        # Por enquanto retorna lista vazia para exemplo
        return []
