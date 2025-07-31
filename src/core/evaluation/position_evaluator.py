"""
Sistema unificado de avaliação de posição
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from src.traditional.core.board.board import Board
from src.traditional.models.models import Position, Piece, PieceType, Color
from src.quantum.core.quantum.quantum_enhancements import EnhancedQuantumField

@dataclass
class AvaliacaoPosicao:
    """Resultado completo da avaliação de uma posição"""
    pontuacao_material: float = 0.0
    pontuacao_posicional: float = 0.0
    pontuacao_mobilidade: float = 0.0
    pontuacao_estrutura_peoes: float = 0.0
    pontuacao_seguranca_rei: float = 0.0
    pontuacao_controle_centro: float = 0.0
    pontuacao_desenvolvimento: float = 0.0
    influencia_quantica: float = 0.0
    pontuacao_total: float = 0.0

class AvaliadorPosicao:
    """Avaliador unificado de posição"""
    
    def __init__(self):
        self.valores_base = {
            PieceType.PAWN: 1.0,    # Peão
            PieceType.KNIGHT: 3.0,  # Cavalo
            PieceType.BISHOP: 3.0,  # Bispo
            PieceType.ROOK: 5.0,    # Torre
            PieceType.QUEEN: 9.0,   # Dama
            PieceType.KING: 0.0     # Rei (não usado na avaliação)
        }
        
        self.pesos = {
            'material': 1.0,
            'posicao': 0.6,
            'mobilidade': 0.4,
            'estrutura_peoes': 0.5,
            'seguranca_rei': 0.7,
            'controle_centro': 0.6,
            'desenvolvimento': 0.4,
            'influencia_quantica': 0.3
        }
        
        self.quantum_field = EnhancedQuantumField()
        self.tabelas_posicionais = self._init_tabelas_posicionais()
    
    def _init_tabelas_posicionais(self) -> Dict[str, np.ndarray]:
        """Inicializa tabelas de valor posicional para cada peça"""
        tabelas = {}
        
        # Tabela para peões
        tabelas['pawn'] = np.array([
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
            [0.1,  0.1,  0.2,  0.3,  0.3,  0.2,  0.1,  0.1],
            [0.05, 0.05, 0.1,  0.25, 0.25, 0.1,  0.05, 0.05],
            [0.0,  0.0,  0.0,  0.2,  0.2,  0.0,  0.0,  0.0],
            [0.05,-0.05,-0.1,  0.0,  0.0, -0.1, -0.05, 0.05],
            [0.05, 0.1,  0.1, -0.2, -0.2,  0.1,  0.1,  0.05],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ])
        
        # Tabela para cavalos
        tabelas['knight'] = np.array([
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
            [-0.4, -0.2,  0.0,  0.0,  0.0,  0.0, -0.2, -0.4],
            [-0.3,  0.0,  0.1,  0.15, 0.15, 0.1,  0.0, -0.3],
            [-0.3,  0.05, 0.15, 0.2,  0.2,  0.15, 0.05,-0.3],
            [-0.3,  0.0,  0.15, 0.2,  0.2,  0.15, 0.0, -0.3],
            [-0.3,  0.05, 0.1,  0.15, 0.15, 0.1,  0.05,-0.3],
            [-0.4, -0.2,  0.0,  0.05, 0.05, 0.0, -0.2, -0.4],
            [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
        ])
        
        # Tabela para bispos
        tabelas['bishop'] = np.array([
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2],
            [-0.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.1],
            [-0.1,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0, -0.1],
            [-0.1,  0.05, 0.05, 0.2,  0.2,  0.05, 0.05,-0.1],
            [-0.1,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.1],
            [-0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.1, -0.1],
            [-0.1,  0.05, 0.0,  0.0,  0.0,  0.0,  0.05,-0.1],
            [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
        ])
        
        # Tabela para torres
        tabelas['rook'] = np.array([
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [0.05, 0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.05],
            [-0.05,0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.05],
            [-0.05,0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.05],
            [-0.05,0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.05],
            [-0.05,0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.05],
            [-0.05,0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.05],
            [0.0,  0.0,  0.0,  0.05, 0.05, 0.0,  0.0,  0.0]
        ])
        
        # Tabela para dama
        tabelas['queen'] = np.array([
            [-0.2, -0.1, -0.1, -0.05,-0.05,-0.1, -0.1, -0.2],
            [-0.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.1],
            [-0.1,  0.0,  0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
            [-0.05, 0.0,  0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
            [0.0,   0.0,  0.05, 0.05, 0.05, 0.05, 0.0, -0.05],
            [-0.1,  0.05, 0.05, 0.05, 0.05, 0.05, 0.0, -0.1],
            [-0.1,  0.0,  0.05, 0.0,  0.0,  0.0,  0.0, -0.1],
            [-0.2, -0.1, -0.1, -0.05,-0.05,-0.1, -0.1, -0.2]
        ])
        
        # Tabelas para rei (meio-jogo e fim de jogo)
        tabelas['king_midgame'] = np.array([
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
            [-0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2],
            [-0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1],
            [0.2,   0.2,  0.0,  0.0,  0.0,  0.0,  0.2,  0.2],
            [0.2,   0.3,  0.1,  0.0,  0.0,  0.1,  0.3,  0.2]
        ])
        
        tabelas['king_endgame'] = np.array([
            [-0.5, -0.4, -0.3, -0.2, -0.2, -0.3, -0.4, -0.5],
            [-0.3, -0.2, -0.1,  0.0,  0.0, -0.1, -0.2, -0.3],
            [-0.3, -0.1,  0.2,  0.3,  0.3,  0.2, -0.1, -0.3],
            [-0.3, -0.1,  0.3,  0.4,  0.4,  0.3, -0.1, -0.3],
            [-0.3, -0.1,  0.3,  0.4,  0.4,  0.3, -0.1, -0.3],
            [-0.3, -0.1,  0.2,  0.3,  0.3,  0.2, -0.1, -0.3],
            [-0.3, -0.3,  0.0,  0.0,  0.0,  0.0, -0.3, -0.3],
            [-0.5, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.5]
        ])
        
        return tabelas

    def avaliar(self, board: Board) -> AvaliacaoPosicao:
        """Avalia uma posição de forma completa"""
        avaliacao = AvaliacaoPosicao()
        
        # Avaliação material
        avaliacao.pontuacao_material = self._avaliar_material(board)
        
        # Avaliação posicional
        avaliacao.pontuacao_posicional = self._avaliar_posicional(board)
        
        # Avaliação de mobilidade
        avaliacao.pontuacao_mobilidade = self._avaliar_mobilidade(board)
        
        # Avaliação da estrutura de peões
        avaliacao.pontuacao_estrutura_peoes = self._avaliar_estrutura_peoes(board)
        
        # Avaliação da segurança do rei
        avaliacao.pontuacao_seguranca_rei = self._avaliar_seguranca_rei(board)
        
        # Avaliação do controle do centro
        avaliacao.pontuacao_controle_centro = self._avaliar_controle_centro(board)
        
        # Avaliação do desenvolvimento
        avaliacao.pontuacao_desenvolvimento = self._avaliar_desenvolvimento(board)
        
        # Influência quântica
        avaliacao.influencia_quantica = self._avaliar_influencia_quantica(board)
        
        # Calcula pontuação total
        avaliacao.pontuacao_total = (
            avaliacao.pontuacao_material * self.pesos['material'] +
            avaliacao.pontuacao_posicional * self.pesos['posicao'] +
            avaliacao.pontuacao_mobilidade * self.pesos['mobilidade'] +
            avaliacao.pontuacao_estrutura_peoes * self.pesos['estrutura_peoes'] +
            avaliacao.pontuacao_seguranca_rei * self.pesos['seguranca_rei'] +
            avaliacao.pontuacao_controle_centro * self.pesos['controle_centro'] +
            avaliacao.pontuacao_desenvolvimento * self.pesos['desenvolvimento'] +
            avaliacao.influencia_quantica * self.pesos['influencia_quantica']
        )
        
        return avaliacao

    def _avaliar_material(self, board: Board) -> float:
        """Avalia o balanço material"""
        white_material = sum(self.valores_base[p.type] for p in board.get_pieces(Color.WHITE))
        black_material = sum(self.valores_base[p.type] for p in board.get_pieces(Color.BLACK))
        return white_material - black_material

    def _avaliar_posicional(self, board: Board) -> float:
        """Avalia aspectos posicionais usando tabelas de peça-quadrado"""
        score = 0.0
        for piece in board.get_all_pieces():
            x, y = piece.position.rank - 1, piece.position.file - 1
            if piece.color == Color.BLACK:
                x, y = 7 - x, 7 - y
            
            # Mapear o tipo de peça para a chave da tabela
            table_key_map = {
                PieceType.PAWN: 'pawn',
                PieceType.KNIGHT: 'knight',
                PieceType.BISHOP: 'bishop',
                PieceType.ROOK: 'rook',
                PieceType.QUEEN: 'queen',
                PieceType.KING: 'king_midgame'
            }
            table_key = table_key_map[piece.type]
            if piece.type == PieceType.KING:
                table_key = 'king_midgame' if not self._is_endgame(board) else 'king_endgame'
            
            score += self.tabelas_posicionais[table_key][x][y] * (1 if piece.color == Color.WHITE else -1)
        
        return score

    def _avaliar_mobilidade(self, board: Board) -> float:
        """Avalia a mobilidade das peças"""
        white_mobility = sum(len(board.get_valid_moves(p.position)) for p in board.get_pieces(Color.WHITE))
        black_mobility = sum(len(board.get_valid_moves(p.position)) for p in board.get_pieces(Color.BLACK))
        return (white_mobility - black_mobility) * 0.1

    def _avaliar_estrutura_peoes(self, board: Board) -> float:
        """Avalia a estrutura de peões"""
        return self.quantum_field.analyze_pawn_structure(Color.WHITE) - \
               self.quantum_field.analyze_pawn_structure(Color.BLACK)

    def _avaliar_seguranca_rei(self, board: Board) -> float:
        """Avalia a segurança dos reis"""
        white_king = next((p for p in board.get_pieces(Color.WHITE) if p.type == PieceType.KING), None)
        black_king = next((p for p in board.get_pieces(Color.BLACK) if p.type == PieceType.KING), None)
        
        if not white_king or not black_king:
            return 0.0
            
        white_safety = self.quantum_field.analyze_king_safety(Color.WHITE, white_king.position)
        black_safety = self.quantum_field.analyze_king_safety(Color.BLACK, black_king.position)
        
        return white_safety - black_safety

    def _avaliar_controle_centro(self, board: Board) -> float:
        """Avalia o controle do centro do tabuleiro"""
        return self.quantum_field._analyze_center_control()

    def _avaliar_desenvolvimento(self, board: Board) -> float:
        """Avalia o desenvolvimento das peças"""
        white_dev = sum(1 for p in board.get_pieces(Color.WHITE) 
                       if p.type != PieceType.PAWN and p.position.rank != 1)
        black_dev = sum(1 for p in board.get_pieces(Color.BLACK) 
                       if p.type != PieceType.PAWN and p.position.rank != 8)
        return (white_dev - black_dev) * 0.1

    def _avaliar_influencia_quantica(self, board: Board) -> float:
        """Avalia a influência quântica na posição"""
        pieces_dict = {p.position: p for p in board.get_all_pieces()}
        dynamics = self.quantum_field.get_position_dynamics(pieces_dict)
        return sum(dynamics.values()) / len(dynamics)

    def _is_endgame(self, board: Board) -> bool:
        """Determina se a posição está no final do jogo"""
        total_material = sum(self.valores_base[p.type] for p in board.get_all_pieces())
        return total_material <= 30  # Valor aproximado para determinar final de jogo
