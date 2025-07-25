"""
Módulo para análise e identificação de padrões no xadrez.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import yaml
import chess
from .base import ChessPattern

@dataclass
class Position:
    """Posição no tabuleiro."""
    file: str  # a-h
    rank: int  # 1-8

@dataclass
class Piece:
    """Peça de xadrez."""
    type: str  # pawn, knight, bishop, rook, queen, king
    color: str  # white, black
    position: Position

@dataclass
class Board:
    """Estado do tabuleiro."""
    pieces: Dict[Tuple[str, int], Piece]  # (file, rank) -> Piece
    last_move: Optional[Tuple[Position, Position]]
    move_number: int

class PatternMatcher:
    """Identifica padrões táticos e estratégicos no jogo."""
    
    def __init__(self, patterns_path: str):
        self.patterns = self._load_patterns(patterns_path)
    
    def _load_patterns(self, path: str) -> Dict:
        """Carrega padrões do arquivo YAML."""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)['chess_patterns']
    
    def analyze_position(self, board: chess.Board) -> List[ChessPattern]:
        """Analisa a posição atual e identifica padrões."""
        patterns = []
        
        # Análise tática
        patterns.extend(self._find_tactical_patterns(board))
        
        # Análise estratégica
        patterns.extend(self._find_strategic_patterns(board))
        
        return patterns
    
    def _find_tactical_patterns(self, board: chess.Board) -> List[ChessPattern]:
        """Identifica padrões táticos."""
        patterns = []
        
        # Bateria
        battery = self._check_battery(board)
        if battery:
            patterns.append(battery)
        
        # Garfo
        fork = self._check_fork(board)
        if fork:
            patterns.append(fork)
        
        # Pregadura
        pin = self._check_pin(board)
        if pin:
            patterns.append(pin)
        
        return patterns
    
    def _find_strategic_patterns(self, board: chess.Board) -> List[ChessPattern]:
        """Identifica padrões estratégicos."""
        patterns = []
        
        # Estrutura de peões
        pawn_structure = self._analyze_pawn_structure(board)
        if pawn_structure:
            patterns.append(pawn_structure)
        
        # Posicionamento de peças
        piece_placement = self._analyze_piece_placement(board)
        if piece_placement:
            patterns.append(piece_placement)
        
        # Controle do centro
        center_control = self._analyze_center_control(board)
        if center_control:
            patterns.append(center_control)
        
        return patterns
    
    def _check_battery(self, board: chess.Board) -> Optional[ChessPattern]:
        """Verifica alinhamento de peças para ataque."""
        # Verifica baterias verticais
        for file_idx in range(8):
            pieces_in_file = []
            for rank_idx in range(8):
                square = chess.square(file_idx, rank_idx)
                piece = board.piece_at(square)
                if piece and piece.piece_type in [chess.ROOK, chess.QUEEN]:
                    pieces_in_file.append((square, piece))
            
            # Verifica peças alinhadas da mesma cor
            for i in range(len(pieces_in_file)-1):
                sq1, p1 = pieces_in_file[i]
                sq2, p2 = pieces_in_file[i+1]
                if p1.color == p2.color == board.turn:
                    return ChessPattern(
                        name="battery",
                        type="tactical",
                        description="Alinhamento vertical de peças para ataque",
                        significance=0.8
                    )
        
        # Verifica baterias horizontais
        for rank_idx in range(8):
            pieces_in_rank = []
            for file_idx in range(8):
                square = chess.square(file_idx, rank_idx)
                piece = board.piece_at(square)
                if piece and piece.piece_type in [chess.ROOK, chess.QUEEN]:
                    pieces_in_rank.append((square, piece))
            
            # Verifica peças alinhadas da mesma cor
            for i in range(len(pieces_in_rank)-1):
                sq1, p1 = pieces_in_rank[i]
                sq2, p2 = pieces_in_rank[i+1]
                if p1.color == p2.color == board.turn:
                    return ChessPattern(
                        name="battery",
                        type="tactical",
                        description="Alinhamento horizontal de peças para ataque",
                        significance=0.8
                    )
        
        return None
    
    def _check_fork(self, board: chess.Board) -> Optional[ChessPattern]:
        """Verifica ataques duplos."""
        if not board.move_stack:
            return None
        
        last_move = board.peek()
        to_pos = last_move.to_square
        piece = board.piece_at(to_pos)
        
        if not piece:
            return None
        
        # Verifica ataques do cavalo
        if piece.piece_type == chess.KNIGHT:
            attacked = board.attacks(to_pos)
            if sum(1 for sq in attacked if board.piece_at(sq)) >= 2:
                return ChessPattern(
                    name="fork",
                    type="tactical",
                    description="Ataque duplo com cavalo",
                    significance=0.9 if any(board.piece_at(sq).piece_type in [chess.KING, chess.QUEEN] 
                                           for sq in attacked if board.piece_at(sq)) else 0.7
                )
        
        return None
    
    def _check_pin(self, board: chess.Board) -> Optional[ChessPattern]:
        """Verifica pregaduras."""
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece or piece.color != board.turn:
                continue
                
            if piece.piece_type in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
                pinned_square = self._find_pinned_piece(square, board)
                if pinned_square:
                    pinned_piece = board.piece_at(pinned_square)
                    return ChessPattern(
                        name="pin",
                        type="tactical",
                        description="Peça imobilizada protegendo o rei",
                        significance=0.85
                    )
        
        return None
    
    def _analyze_pawn_structure(self, board: chess.Board) -> Optional[ChessPattern]:
        """Analisa estrutura de peões."""
        # Encontra peões do jogador atual no centro
        center_pawns = []
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if (piece and 
                piece.piece_type == chess.PAWN and 
                piece.color == board.turn and
                chess.square_file(square) in [2,3,4,5]):
                center_pawns.append(square)
        
        # Verifica peões conectados
        if len(center_pawns) >= 2:
            connected = False
            for i, sq1 in enumerate(center_pawns[:-1]):
                for sq2 in center_pawns[i+1:]:
                    if abs(chess.square_file(sq1) - chess.square_file(sq2)) == 1:
                        connected = True
                        break
            
            if connected:
                return ChessPattern(
                    name="pawn_structure",
                    type="strategic",
                    description="Estrutura de peões conectados no centro",
                    significance=0.7
                )
        
        return None
    
    def _analyze_piece_placement(self, board: chess.Board) -> Optional[ChessPattern]:
        """Analisa posicionamento das peças."""
        developed_pieces = 0
        total_pieces = 0
        
        # Conta peças desenvolvidas (fora da posição inicial)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                if piece.piece_type not in [chess.PAWN, chess.KING]:
                    total_pieces += 1
                    rank = chess.square_rank(square)
                    if (piece.color == chess.WHITE and rank > 1) or \
                       (piece.color == chess.BLACK and rank < 6):
                        developed_pieces += 1
        
        # Verifica bom desenvolvimento
        if total_pieces >= 3 and developed_pieces/total_pieces >= 0.7:
            return ChessPattern(
                name="piece_development",
                type="strategic",
                description="Bom desenvolvimento de peças",
                significance=0.75
            )
        
        return None
    
    def _analyze_center_control(self, board: chess.Board) -> Optional[ChessPattern]:
        """Analisa controle do centro."""
        # Define casas centrais
        center_squares = [
            chess.E4, chess.D4, chess.E5, chess.D5
        ]
        
        # Conta controle do centro
        controlled = 0
        for square in center_squares:
            # Verifica atacantes das casas centrais
            attackers = board.attackers(board.turn, square)
            if attackers:
                controlled += 1
            
            # Verifica peça própria ocupando casa central
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                controlled += 1
        
        if controlled >= 3:
            return ChessPattern(
                name="center_control",
                type="strategic", 
                description="Forte controle do centro",
                significance=0.8
            )
            
        return None
    
    
    def _find_pinned_piece(self, square: int, board: chess.Board) -> Optional[int]:
        """Encontra peça pregada pela peça na casa fornecida."""
        piece = board.piece_at(square)
        if not piece or piece.piece_type not in [chess.BISHOP, chess.ROOK, chess.QUEEN]:
            return None
            
        # Gera ataques da peça
        attacks = board.attacks(square)
        
        # Verifica cada ataque
        for target_square in attacks:
            # Verifica se há peça adversária no caminho
            between = chess.SquareSet.between(square, target_square)
            pieces_between = sum(1 for sq in between if board.piece_at(sq))
            
            if pieces_between == 1:
                # Encontra a peça pregada
                pinned_square = next(sq for sq in between if board.piece_at(sq))
                pinned_piece = board.piece_at(pinned_square)
                target_piece = board.piece_at(target_square)
                
                if (pinned_piece and target_piece and
                    pinned_piece.color != piece.color and
                    target_piece.color != piece.color and
                    target_piece.piece_type == chess.KING):
                    
                    return pinned_square
        
        return None
