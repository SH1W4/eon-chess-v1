from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from src.core.board.board import Board, Position

@dataclass
class TranspositionEntry:
    """Entrada na tabela de transposição"""
    depth: int
    score: float
    flag: str  # 'exact', 'lowerbound', 'upperbound'
    best_move: Optional[Tuple[Position, Position]]

class TranspositionTable:
    """Tabela de transposição para cache de posições avaliadas"""
    
    def __init__(self, max_size: int = 1_000_000):
        self.max_size = max_size
        self.table: Dict[str, TranspositionEntry] = {}
        
    def store(self, board: Board, depth: int, score: float, 
             flag: str, best_move: Optional[Tuple[Position, Position]] = None) -> None:
        """Armazena uma entrada na tabela"""
        # Limpa a tabela se exceder o tamanho máximo
        if len(self.table) >= self.max_size:
            self.table.clear()
            
        key = self._get_hash(board)
        self.table[key] = TranspositionEntry(depth, score, flag, best_move)
        
    def lookup(self, board: Board) -> Optional[TranspositionEntry]:
        """Busca uma entrada na tabela"""
        key = self._get_hash(board)
        return self.table.get(key)
    
    def _get_hash(self, board: Board) -> str:
        """Gera uma chave hash para a posição do tabuleiro"""
        # Hash simplificado baseado na posição das peças
        pieces = []
        for piece in board.piece_list:
            pieces.append(f"{piece.type.value}{piece.color.value}{piece.position.rank}{piece.position.file}")
        return "_".join(sorted(pieces))

    def clear(self) -> None:
        """Limpa a tabela"""
        self.table.clear()

    def get_size(self) -> int:
        """Retorna o número de entradas na tabela"""
        return len(self.table)

    def get_statistics(self) -> Dict[str, int]:
        """Retorna estatísticas sobre a tabela"""
        stats = {
            'total_entries': len(self.table),
            'exact_scores': 0,
            'lowerbound_scores': 0,
            'upperbound_scores': 0
        }
        
        for entry in self.table.values():
            if entry.flag == 'exact':
                stats['exact_scores'] += 1
            elif entry.flag == 'lowerbound':
                stats['lowerbound_scores'] += 1
            elif entry.flag == 'upperbound':
                stats['upperbound_scores'] += 1
                
        return stats
