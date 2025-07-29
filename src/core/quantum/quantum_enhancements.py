"""Melhorias do sistema de campo quântico"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from ..models import Position, Piece, Color
from .quantum_field import QuantumField, INFLUENCE_THRESHOLD, ATTACK_THRESHOLD, CONTROL_THRESHOLD

@dataclass
class PositionEvaluation:
    """Avaliação completa de uma posição"""
    material_score: float = 0.0
    control_score: float = 0.0
    mobility_score: float = 0.0
    king_safety_score: float = 0.0
    pawn_structure_score: float = 0.0
    total_score: float = 0.0

class EnhancedQuantumField(QuantumField):
    """Versão aprimorada do campo quântico com análises adicionais"""
    
    def evaluate_position(self, pieces: Dict[Position, Piece]) -> PositionEvaluation:
        """Avalia a posição atual usando o campo quântico"""
        evaluation = PositionEvaluation()
        
        # Controle do tabuleiro
        white_control = float(self.get_control_score(Color.WHITE))
        black_control = float(self.get_control_score(Color.BLACK))
        evaluation.control_score = float(white_control - black_control)
        
        # Mobilidade das peças
        white_mobility = sum(self.get_piece_mobility(p) for p in pieces.values() 
                           if p.color == Color.WHITE)
        black_mobility = sum(self.get_piece_mobility(p) for p in pieces.values() 
                           if p.color == Color.BLACK)
        evaluation.mobility_score = float(0.5 * (white_mobility - black_mobility))
        
        # Segurança dos reis
        white_king = next((p for p in pieces.values() 
                          if p.color == Color.WHITE and p.type.value == "K"), None)
        black_king = next((p for p in pieces.values() 
                          if p.color == Color.BLACK and p.type.value == "K"), None)
        
        if white_king and black_king:
            white_safety = self.analyze_king_safety(Color.WHITE, white_king.position)
            black_safety = self.analyze_king_safety(Color.BLACK, black_king.position)
            evaluation.king_safety_score = float(white_safety - black_safety)
        
        # Estrutura de peões
        evaluation.pawn_structure_score = (
            self.analyze_pawn_structure(Color.WHITE) -
            self.analyze_pawn_structure(Color.BLACK)
        )
        
        # Material (peso básico das peças)
        piece_values = {"K": 0.0, "Q": 9.0, "R": 5.0, "B": 3.0, "N": 3.0, "P": 1.0}
        white_material = sum(piece_values[p.type.value] for p in pieces.values() 
                           if p.color == Color.WHITE)
        black_material = sum(piece_values[p.type.value] for p in pieces.values() 
                           if p.color == Color.BLACK)
        evaluation.material_score = float(white_material - black_material)
        
        # Pontuação total (com pesos)
        evaluation.total_score = (
            evaluation.material_score * 1.0 +
            evaluation.control_score * 0.5 +
            evaluation.mobility_score * 0.3 +
            evaluation.king_safety_score * 0.7 +
            evaluation.pawn_structure_score * 0.4
        )
        
        return evaluation
    
    def analyze_king_safety(self, color: Color, king_pos: Position) -> float:
        """Analisa a segurança do rei usando o campo quântico"""
        rank, file = king_pos.rank - 1, king_pos.file - 1
        enemy_field = self.black_influence if color == Color.WHITE else self.white_influence
        
        # Analisa a pressão inimiga na área do rei
        min_rank, max_rank = max(0, rank-1), min(8, rank+2)
        min_file, max_file = max(0, file-1), min(8, file+2)
        king_zone = enemy_field[min_rank:max_rank, min_file:max_file]
        
        # Calcula diferentes aspectos da segurança
        attack_pressure = -np.sum(king_zone)
        shield_count = np.sum(king_zone > ATTACK_THRESHOLD)
        escape_squares = np.sum(king_zone < INFLUENCE_THRESHOLD)
        
        # Verifica proteção específica do rei
        friendly_field = self.white_influence if color == Color.WHITE else self.black_influence
        enemy_field = self.black_influence if color == Color.WHITE else self.white_influence
        
        # Calcula área ao redor do rei
        king_area = friendly_field[max(0, rank-1):min(8, rank+2),
                                 max(0, file-1):min(8, file+2)]
        enemy_area = enemy_field[max(0, rank-1):min(8, rank+2),
                                max(0, file-1):min(8, file+2)]
        
        # Calcula proteção e ameaças
        protection_score = np.sum(king_area > CONTROL_THRESHOLD) * 0.3
        threat_score = -np.sum(enemy_area > ATTACK_THRESHOLD) * 0.4  # Penalidade por ameaças
        
        return attack_pressure - (shield_count * 0.5) + (escape_squares * 0.3) + protection_score
    
    def analyze_pawn_structure(self, color: Color) -> float:
        """Analisa a estrutura de peões usando o campo de influência"""
        field = self.white_influence if color == Color.WHITE else self.black_influence
        pawn_structure_score = 0.0
        pawn_positions = set()
        
        # Define os limites de busca baseado na cor
        if color == Color.WHITE:
            rank_range = range(1, 7)  # Segunda à sétima fileira para brancas
            direction = 1
        else:
            rank_range = range(6, 0, -1)  # Sétima à segunda fileira para pretas
            direction = -1
        
        # Procura peões em cada coluna
        for file in range(8):
            for rank in rank_range:
                # Verifica influência forte (peões se movem para frente)
                if field[rank, file] >= 0.6:
                    pawn_positions.add((rank, file))
                    break
                # Verifica influência diagonal (ataques)
                elif field[rank, file] >= 0.3:
                    next_rank = rank + direction
                    if 0 <= next_rank < 8:
                        if file > 0 and field[next_rank, file - 1] >= 0.8:
                            pawn_positions.add((rank, file))
                            break
                        if file < 7 and field[next_rank, file + 1] >= 0.8:
                            pawn_positions.add((rank, file))
                            break
                        
                        if has_diagonal:
                            pawn_positions.add((rank, file))
                            break  # Encontrou um peão, passa para próxima coluna
        
        # Analisa colunas
        for file in range(8):
            # Conta peões nesta coluna
            pawns_in_file = [(r, f) for r, f in pawn_positions if f == file]
            pawn_count = len(pawns_in_file)
            
            if pawn_count > 0:
                # Base score for having a pawn (reduzido para equilibrar com penalidades)
                pawn_structure_score += 0.2
                
                if pawn_count > 1:  # Doubled pawns - penalidade muito severa
                    pawn_structure_score -= 0.6 * (pawn_count - 1)  # Penalidade aumentada
                
                # Check for passed and isolated pawns
                adjacent_files = [file-1, file+1] if 0 < file < 7 else [file-1] if file == 7 else [file+1]
                ranks = range(8)
                has_adjacent_pawns = any(any((r, f) in pawn_positions for r in ranks)
                                        for f in adjacent_files)
                
                if not has_adjacent_pawns:
                    # Passed pawn bonus - maior para peões mais avançados
                    rank = pawns_in_file[0][0]  # Pega a posição do peão
                    if color == Color.WHITE:
                        advancement = (rank - 1) / 5.0  # 0.0 para rank 1, 1.0 para rank 6
                    else:
                        advancement = (6 - rank) / 5.0  # 0.0 para rank 6, 1.0 para rank 1
                    pawn_structure_score += 0.2 + (advancement * 0.3)
                elif file > 0 and file < 7:  # Isolated pawn
                    pawn_structure_score -= 0.2
                
                # Central pawn bonus (reduzido)
                if 2 <= file <= 5:
                    pawn_structure_score += 0.1
        
        # Bonus por quantidade total de peões (reduzido)
        total_pawns = len(pawn_positions)
        if total_pawns > 0:
            pawn_structure_score += 0.05 * total_pawns
        
        return pawn_structure_score
    
    def get_position_dynamics(self, pieces: Dict[Position, Piece]) -> Dict[str, float]:
        """Analisa a dinâmica da posição"""
        return {
            'center_control': self._analyze_center_control(),
            'piece_coordination': self._analyze_piece_coordination(pieces),
            'attacking_potential': self._analyze_attacking_potential(pieces),
            'defensive_solidity': self._analyze_defensive_solidity(pieces)
        }
    
    def _analyze_center_control(self) -> float:
        """Analisa o controle do centro do tabuleiro"""
        center_slice = slice(3, 5)
        white_center = np.sum(self.white_influence[center_slice, center_slice])
        black_center = np.sum(self.black_influence[center_slice, center_slice])
        return white_center - black_center
    
    def _analyze_piece_coordination(self, pieces: Dict[Position, Piece]) -> float:
        """Analisa a coordenação entre as peças"""
        coordination_score = 0.0
        for pos, piece in pieces.items():
            field = self.piece_fields.get(pos, np.zeros((8, 8)))
            # Verifica sobreposição com outras peças da mesma cor
            for other_pos, other_piece in pieces.items():
                if pos != other_pos and piece.color == other_piece.color:
                    other_field = self.piece_fields.get(other_pos, np.zeros((8, 8)))
                    coordination_score += np.sum(field * other_field) * 0.1
        return coordination_score
    
    def _analyze_attacking_potential(self, pieces: Dict[Position, Piece]) -> float:
        """Analisa o potencial de ataque"""
        white_attack = np.sum(self.white_influence > ATTACK_THRESHOLD)
        black_attack = np.sum(self.black_influence > ATTACK_THRESHOLD)
        return white_attack - black_attack
    
    def _analyze_defensive_solidity(self, pieces: Dict[Position, Piece]) -> float:
        """Analisa a solidez defensiva"""
        white_defense = np.sum(self.white_influence > CONTROL_THRESHOLD)
        black_defense = np.sum(self.black_influence > CONTROL_THRESHOLD)
        return white_defense - black_defense
