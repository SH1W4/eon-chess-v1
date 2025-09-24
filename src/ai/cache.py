"""
Sistema de cache para a IA de xadrez.
"""

from typing import Dict, Optional, Tuple
import json
from pathlib import Path

class PositionCache:
    """Cache de posições avaliadas."""
    
    def __init__(self, cache_size: int = 1000000):
        self.cache_size = cache_size
        self.cache: Dict[str, float] = {}
        
    def _get_position_key(self, board_state: str, depth: int) -> str:
        """Gera uma chave única para uma posição e profundidade."""
        return f"{board_state}_{depth}"
        
    def get(self, board_state: str, depth: int) -> Optional[float]:
        """
        Recupera uma avaliação do cache.
        Retorna None se a posição não estiver no cache.
        """
        key = self._get_position_key(board_state, depth)
        return self.cache.get(key)
        
    def put(self, board_state: str, depth: int, evaluation: float):
        """Armazena uma avaliação no cache."""
        key = self._get_position_key(board_state, depth)
        
        # Se o cache estiver cheio, remove 10% das entradas mais antigas
        if len(self.cache) >= self.cache_size:
            num_to_remove = self.cache_size // 10
            keys_to_remove = list(self.cache.keys())[:num_to_remove]
            for k in keys_to_remove:
                del self.cache[k]
                
        self.cache[key] = evaluation
        
    def clear(self):
        """Limpa o cache."""
        self.cache.clear()
        
    def size(self) -> int:
        """Retorna o número de posições no cache."""
        return len(self.cache)
        
    def save_to_disk(self, filepath: str):
        """Salva o cache em disco."""
        cache_data = {
            'cache_size': self.cache_size,
            'positions': self.cache
        }
        
        with open(filepath, 'w') as f:
            json.dump(cache_data, f)
            
    def load_from_disk(self, filepath: str) -> bool:
        """
        Carrega o cache do disco.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r') as f:
                cache_data = json.load(f)
                
            self.cache_size = cache_data['cache_size']
            self.cache = cache_data['positions']
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

class OpeningBookCache:
    """Cache para o livro de aberturas."""
    
    def __init__(self, book_file: Optional[str] = None):
        self.openings: Dict[str, Dict] = {}
        if book_file:
            self.load_book(book_file)
            
    def load_book(self, filepath: str) -> bool:
        """
        Carrega um livro de aberturas do disco.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r') as f:
                self.openings = json.load(f)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
            
    def get_next_move(self, move_history: list) -> Optional[Tuple[int, int]]:
        """
        Recupera o próximo movimento do livro de aberturas.
        Retorna None se a sequência não estiver no livro.
        """
        current_position = '_'.join(str(move) for move in move_history)
        opening_data = self.openings.get(current_position)
        
        if opening_data:
            return opening_data.get('next_move')
        return None
        
    def add_opening(self, move_sequence: list, next_move: Tuple[int, int], name: str = ""):
        """Adiciona uma nova abertura ao livro."""
        position_key = '_'.join(str(move) for move in move_sequence)
        self.openings[position_key] = {
            'next_move': next_move,
            'name': name
        }
        
    def save_book(self, filepath: str):
        """Salva o livro de aberturas em disco."""
        with open(filepath, 'w') as f:
            json.dump(self.openings, f)

class EndgameTablebaseCache:
    """Cache para tabelas de finais."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.tablebase: Dict[str, Dict] = {}
        if cache_dir:
            self.load_tablebase(cache_dir)
            
    def load_tablebase(self, directory: str) -> bool:
        """
        Carrega tabelas de finais do disco.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            directory_path = Path(directory)
            for file in directory_path.glob('*.json'):
                with open(file, 'r') as f:
                    piece_combination = file.stem
                    self.tablebase[piece_combination] = json.load(f)
            return True
        except Exception:
            return False
            
    def get_evaluation(self, position: str, piece_combination: str) -> Optional[int]:
        """
        Recupera a avaliação de uma posição de final.
        Retorna None se a posição não estiver nas tabelas.
        """
        if piece_combination in self.tablebase:
            return self.tablebase[piece_combination].get(position)
        return None
        
    def add_position(self, position: str, piece_combination: str, evaluation: int):
        """Adiciona uma nova posição às tabelas de finais."""
        if piece_combination not in self.tablebase:
            self.tablebase[piece_combination] = {}
        self.tablebase[piece_combination][position] = evaluation
        
    def save_tablebase(self, directory: str):
        """Salva as tabelas de finais em disco."""
        directory_path = Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)
        
        for piece_combination, positions in self.tablebase.items():
            filepath = directory_path / f"{piece_combination}.json"
            with open(filepath, 'w') as f:
                json.dump(positions, f)
