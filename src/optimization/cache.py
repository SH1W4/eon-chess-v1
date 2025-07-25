from typing import Dict, Optional, Tuple, Any, List
import numpy as np

class TranspositionTable:
    """Tabela de transposição para cache de posições já analisadas"""
    def __init__(self, size: int = 1000000):
        self.size = size
        self.table: Dict[int, Tuple[int, float, Any, str]] = {}
    
    def store(self, hash_key: int, depth: int, value: float, move: Any, flag: str) -> None:
        """Armazena uma posição na tabela
        
        Args:
            hash_key: Hash da posição
            depth: Profundidade da análise
            value: Valor da posição
            move: Melhor movimento encontrado
            flag: Tipo de entrada ('exact', 'alpha', 'beta')
        """
        if len(self.table) >= self.size:
            self.table.clear()  # Reset se cheio
        self.table[hash_key] = (depth, value, move, flag)
    
    def lookup(self, hash_key: int) -> Optional[Tuple[int, float, Any, str]]:
        """Procura uma posição na tabela
        
        Args:
            hash_key: Hash da posição
        
        Returns:
            Tuple com (profundidade, valor, movimento, flag) ou None se não encontrado
        """
        return self.table.get(hash_key)

class EvaluationCache:
    """Cache para avaliações de posição"""
    def __init__(self, size: int = 10000):
        self.size = size
        self.cache: Dict[int, float] = {}
    
    def get(self, position_hash: int) -> Optional[float]:
        """Obtém valor cacheado de uma posição"""
        return self.cache.get(position_hash)
    
    def store(self, position_hash: int, value: float) -> None:
        """Armazena valor de uma posição"""
        if len(self.cache) >= self.size:
            self.cache.clear()  # Reset se cheio
        self.cache[position_hash] = value

class MovementCache:
    """Cache para movimentos legais"""
    def __init__(self, size: int = 5000):
        self.size = size
        self.cache: Dict[int, List[Any]] = {}
    
    def get(self, position_hash: int) -> Optional[List[Any]]:
        """Obtém movimentos legais cacheados"""
        return self.cache.get(position_hash)
    
    def store(self, position_hash: int, moves: List[Any]) -> None:
        """Armazena movimentos legais de uma posição"""
        if len(self.cache) >= self.size:
            self.cache.clear()  # Reset se cheio
        self.cache[position_hash] = moves.copy()  # Copia para evitar modificações

class PositionHasher:
    """Gerador de hashes para posições do tabuleiro usando hashing Zobrist"""
    def __init__(self):
        # Inicializa tabelas Zobrist
        self.piece_table = np.random.randint(
            0, 2**64, size=(2, 6, 8, 8), dtype=np.uint64
        )  # [cor, tipo, linha, coluna]
        self.castle_table = np.random.randint(
            0, 2**64, size=4, dtype=np.uint64
        )  # [branco-K, branco-Q, preto-K, preto-Q]
        self.en_passant_table = np.random.randint(
            0, 2**64, size=8, dtype=np.uint64
        )  # [coluna]
        self.side_table = np.random.randint(
            0, 2**64, dtype=np.uint64
        )  # [lado atual]
    
    def hash_position(self, board: np.ndarray, castle_rights: dict, 
                     en_passant: Optional[int], white_to_move: bool) -> int:
        """Gera hash Zobrist para uma posição
        
        Args:
            board: Array numpy 8x8 representando o tabuleiro
            castle_rights: Dicionário com direitos de roque
            en_passant: Coluna de en passant ou None
            white_to_move: True se é a vez das brancas
        
        Returns:
            Hash da posição como inteiro de 64 bits
        """
        h = 0
        
        # Hash das peças
        piece_map = {
            'pawn': 0, 'knight': 1, 'bishop': 2,
            'rook': 3, 'queen': 4, 'king': 5
        }
        
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece:
                    color_idx = 0 if piece.color == 'white' else 1
                    type_idx = piece_map[piece.type]
                    h ^= self.piece_table[color_idx][type_idx][i][j]
        
        # Hash dos direitos de roque
        if castle_rights.get(('white', 'kingside')):
            h ^= self.castle_table[0]
        if castle_rights.get(('white', 'queenside')):
            h ^= self.castle_table[1]
        if castle_rights.get(('black', 'kingside')):
            h ^= self.castle_table[2]
        if castle_rights.get(('black', 'queenside')):
            h ^= self.castle_table[3]
        
        # Hash do en passant
        if en_passant is not None:
            h ^= self.en_passant_table[en_passant]
        
        # Hash do lado
        if white_to_move:
            h ^= self.side_table
        
        return h
