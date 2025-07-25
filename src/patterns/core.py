"""
Módulo de análise de padrões.
Detecta padrões táticos e estratégicos em posições de xadrez.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Set
import chess
import numpy as np

@dataclass
class ChessPattern:
    """Padrão de xadrez identificado."""
    name: str
    type: str  # tactical, strategic
    description: str
    significance: float  # 0.0 to 1.0

class PatternAnalyzer:
    """Analisador de padrões de xadrez."""
    
    def __init__(self):
        """Inicializa analisador."""
        self.tactical_patterns = {
            'fork': self._detect_fork,
            'pin': self._detect_pin,
            'discovery': self._detect_discovery,
            'overload': self._detect_overload,
            'interference': self._detect_interference
        }
        
        self.strategic_patterns = {
            'center_control': self._detect_center_control,
            'pawn_structure': self._detect_pawn_structure,
            'king_safety': self._detect_king_safety,
            'piece_coordination': self._detect_piece_coordination,
            'space_advantage': self._detect_space_advantage
        }
    
    def analyze_position(self, board: chess.Board) -> Dict:
        """
        Analisa posição em busca de padrões.
        
        Args:
            board: Posição atual
            
        Returns:
            Análise com padrões identificados
        """
        patterns = []
        
        # Análise tática
        for name, detector in self.tactical_patterns.items():
            if detector(board):
                patterns.append(
                    ChessPattern(
                        name=name,
                        type='tactical',
                        description=self._get_pattern_description(name),
                        significance=self._calculate_significance(name, board)
                    )
                )
        
        # Análise estratégica
        for name, detector in self.strategic_patterns.items():
            if detector(board):
                patterns.append(
                    ChessPattern(
                        name=name,
                        type='strategic',
                        description=self._get_pattern_description(name),
                        significance=self._calculate_significance(name, board)
                    )
                )
        
        return {
            'patterns': [p.name for p in patterns],
            'details': [
                {
                    'name': p.name,
                    'type': p.type,
                    'description': p.description,
                    'significance': p.significance
                }
                for p in patterns
            ]
        }
    
    def get_config(self) -> Dict:
        """Retorna configuração atual."""
        return {
            'tactical_patterns': list(self.tactical_patterns.keys()),
            'strategic_patterns': list(self.strategic_patterns.keys())
        }
    
    def _detect_fork(self, board: chess.Board) -> bool:
        """Detecta garfo."""
        for move in board.legal_moves:
            board.push(move)
            attacked = set()
            
            # Verifica peças atacadas
            for square in chess.SQUARES:
                piece = board.piece_at(square)
                if piece and piece.color != board.turn:
                    if board.is_attacked_by(board.turn, square):
                        attacked.add(square)
            
            board.pop()
            
            # Garfo: ataca duas ou mais peças valiosas
            valuable_pieces = sum(
                1 for sq in attacked
                if board.piece_at(sq) and
                board.piece_at(sq).piece_type in [chess.QUEEN, chess.ROOK, chess.KING]
            )
            if valuable_pieces >= 2:
                return True
        
        return False
    
    def _detect_pin(self, board: chess.Board) -> bool:
        """Detecta pregadura."""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece or piece.color != board.turn:
                continue
            
            # Verifica ataques de longa distância
            if piece.piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP]:
                attacks = board.attacks(square)
                for attack in attacks:
                    if self._is_pin_ray(board, square, attack):
                        return True
        
        return False
    
    def _detect_discovery(self, board: chess.Board) -> bool:
        """Detecta xeque descoberto."""
        for move in board.legal_moves:
            board.push(move)
            is_check = board.is_check()
            board.pop()
            
            if is_check:
                return True
        
        return False
    
    def _detect_overload(self, board: chess.Board) -> bool:
        """Detecta sobrecarga."""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
            
            # Conta responsabilidades defensivas
            defenders = len(list(board.attackers(piece.color, square)))
            if defenders == 1:  # Única peça defendendo
                defender_square = next(iter(board.attackers(piece.color, square)))
                defender = board.piece_at(defender_square)
                
                # Verifica se defensor tem outras responsabilidades
                other_defenses = sum(
                    1 for sq in chess.SQUARES
                    if board.piece_at(sq) and
                    board.piece_at(sq).color == piece.color and
                    sq != square and
                    defender_square in board.attackers(piece.color, sq)
                )
                
                if other_defenses > 0:
                    return True
        
        return False
    
    def _detect_interference(self, board: chess.Board) -> bool:
        """Detecta interferência."""
        for move in board.legal_moves:
            board.push(move)
            
            # Verifica se movimento bloqueia defesa importante
            blocked_defenses = sum(
                1 for sq in chess.SQUARES
                if board.piece_at(sq) and
                board.piece_at(sq).color == board.turn and
                len(list(board.attackers(not board.turn, sq))) > 
                len(list(board.attackers(board.turn, sq)))
            )
            
            board.pop()
            
            if blocked_defenses > 0:
                return True
        
        return False
    
    def _detect_center_control(self, board: chess.Board) -> bool:
        """Detecta controle do centro."""
        center_squares = {chess.E4, chess.D4, chess.E5, chess.D5}
        controlled = sum(
            1 for sq in center_squares
            if len(list(board.attackers(board.turn, sq))) >
            len(list(board.attackers(not board.turn, sq)))
        )
        return controlled >= 2
    
    def _detect_pawn_structure(self, board: chess.Board) -> bool:
        """Detecta estrutura de peões forte."""
        pawns = board.pieces(chess.PAWN, board.turn)
        if not pawns:
            return False
        
        # Verifica peões conectados
        connected = sum(
            1 for sq in pawns
            if any(
                abs(chess.square_file(sq) - chess.square_file(other)) == 1
                for other in pawns
                if chess.square_rank(sq) == chess.square_rank(other)
            )
        )
        
        return connected >= 2
    
    def _detect_king_safety(self, board: chess.Board) -> bool:
        """Detecta rei bem protegido."""
        king_square = board.king(board.turn)
        if not king_square:
            return False
        
        # Conta proteção ao rei
        protection = len(list(board.attackers(board.turn, king_square)))
        pawn_shield = sum(
            1 for sq in chess.SQUARES
            if board.piece_at(sq) and
            board.piece_at(sq).piece_type == chess.PAWN and
            board.piece_at(sq).color == board.turn and
            abs(chess.square_file(sq) - chess.square_file(king_square)) <= 1 and
            chess.square_rank(sq) > chess.square_rank(king_square)
        )
        
        return protection >= 2 and pawn_shield >= 2
    
    def _detect_piece_coordination(self, board: chess.Board) -> bool:
        """Detecta peças bem coordenadas."""
        pieces = [sq for sq in chess.SQUARES if board.piece_at(sq) and 
                 board.piece_at(sq).color == board.turn and
                 board.piece_at(sq).piece_type != chess.PAWN]
        
        if len(pieces) < 2:
            return False
        
        # Verifica peças se apoiando
        coordinated = sum(
            1 for i, sq1 in enumerate(pieces)
            for sq2 in pieces[i+1:]
            if sq1 in board.attackers(board.turn, sq2) or
            sq2 in board.attackers(board.turn, sq1)
        )
        
        return coordinated >= 2
    
    def _detect_space_advantage(self, board: chess.Board) -> bool:
        """Detecta vantagem de espaço."""
        our_control = sum(
            1 for sq in chess.SQUARES
            if len(list(board.attackers(board.turn, sq))) >
            len(list(board.attackers(not board.turn, sq)))
        )
        
        their_control = sum(
            1 for sq in chess.SQUARES
            if len(list(board.attackers(not board.turn, sq))) >
            len(list(board.attackers(board.turn, sq)))
        )
        
        return our_control > their_control + 5
    
    def _is_pin_ray(self, board: chess.Board, from_square: int, to_square: int) -> bool:
        """Verifica se existe pregadura entre duas casas."""
        ray = chess.SquareSet.between(from_square, to_square)
        pieces_in_ray = sum(1 for sq in ray if board.piece_at(sq))
        
        if pieces_in_ray != 1:
            return False
        
        pinned_square = next(sq for sq in ray if board.piece_at(sq))
        pinned_piece = board.piece_at(pinned_square)
        
        return (
            pinned_piece.color != board.turn and
            board.piece_at(to_square) and
            board.piece_at(to_square).color != board.turn and
            board.piece_at(to_square).piece_type == chess.KING
        )
    
    def _get_pattern_description(self, pattern: str) -> str:
        """Retorna descrição do padrão."""
        descriptions = {
            'fork': "Ataque simultâneo a múltiplas peças",
            'pin': "Peça impossibilitada de mover devido a ameaça mais valiosa",
            'discovery': "Ataque revelado ao mover uma peça",
            'overload': "Peça defensora com múltiplas responsabilidades",
            'interference': "Bloqueio de linha defensiva importante",
            'center_control': "Domínio das casas centrais",
            'pawn_structure': "Estrutura de peões forte e conectada",
            'king_safety': "Rei bem protegido por peças e peões",
            'piece_coordination': "Peças trabalhando em conjunto",
            'space_advantage': "Maior controle territorial do tabuleiro"
        }
        return descriptions.get(pattern, "Padrão não documentado")
    
    def _calculate_significance(self, pattern: str, board: chess.Board) -> float:
        """Calcula significância do padrão."""
        # Pesos base por tipo de padrão
        base_weights = {
            'fork': 0.8,
            'pin': 0.7,
            'discovery': 0.9,
            'overload': 0.6,
            'interference': 0.5,
            'center_control': 0.7,
            'pawn_structure': 0.6,
            'king_safety': 0.8,
            'piece_coordination': 0.6,
            'space_advantage': 0.5
        }
        
        # Ajusta peso pelo contexto
        base_weight = base_weights.get(pattern, 0.5)
        context_multiplier = 1.0
        
        # Fase da partida
        moves = len(list(board.move_stack))
        if moves < 10:  # Abertura
            context_multiplier *= 1.2 if pattern in ['center_control', 'development'] else 0.8
        elif moves > 40:  # Final
            context_multiplier *= 1.2 if pattern in ['king_safety', 'pawn_structure'] else 0.8
        
        # Material
        material_count = sum(1 for _ in board.pieces(chess.QUEEN, chess.WHITE)) + \
                        sum(1 for _ in board.pieces(chess.QUEEN, chess.BLACK))
        if material_count < 2:  # Pouco material
            context_multiplier *= 1.2 if pattern in ['king_safety', 'pawn_structure'] else 0.8
        
        return min(1.0, base_weight * context_multiplier)
