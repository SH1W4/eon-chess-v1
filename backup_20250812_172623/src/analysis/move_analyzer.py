from typing import List, Dict, Set
from dataclasses import dataclass
from collections import defaultdict
import numpy as np

@dataclass
class MoveMetrics:
    execution_time: float  # Tempo de execução do movimento
    position_score: float  # Pontuação da posição resultante
    branching_factor: int  # Fator de ramificação da árvore de busca

class MoveAnalyzer:
    def __init__(self):
        self.move_cache = {}  # Cache de movimentos analisados
        self.position_cache = {}  # Cache de avaliações de posição
        self.pattern_database = defaultdict(int)  # Database de padrões comuns
        
    def analyze_move(self, position: str, move: str) -> MoveMetrics:
        """Analisa um movimento específico com cache e otimizações."""
        # Verificar cache primeiro
        cache_key = f"{position}:{move}"
        if cache_key in self.move_cache:
            return self.move_cache[cache_key]
            
        # Análise vetorizada usando numpy para performance
        pos_array = np.array([ord(c) for c in position])
        move_array = np.array([ord(c) for c in move])
        
        # Cálculos vetorizados
        execution_time = self._calculate_execution_time(pos_array, move_array)
        position_score = self._evaluate_position(pos_array, move_array)
        branching_factor = self._calculate_branching(pos_array)
        
        # Criar e cachear resultado
        metrics = MoveMetrics(
            execution_time=execution_time,
            position_score=position_score,
            branching_factor=branching_factor
        )
        self.move_cache[cache_key] = metrics
        return metrics
    
    def _calculate_execution_time(self, pos_array: np.ndarray, move_array: np.ndarray) -> float:
        """Calcula tempo de execução usando operações vetorizadas."""
        # Implementação otimizada usando numpy
        return float(np.sum(np.abs(pos_array - move_array)) * 0.001)
    
    def _evaluate_position(self, pos_array: np.ndarray, move_array: np.ndarray) -> float:
        """Avalia posição resultante usando operações vetorizadas."""
        # Implementação otimizada usando numpy
        return float(np.mean(pos_array) * np.std(move_array))
    
    def _calculate_branching(self, pos_array: np.ndarray) -> int:
        """Calcula fator de ramificação usando operações vetorizadas."""
        # Implementação otimizada usando numpy
        return int(np.count_nonzero(pos_array > 97))
    
    def update_pattern_database(self, position: str, move: str, success: bool):
        """Atualiza database de padrões para aprendizado."""
        pattern = self._extract_pattern(position, move)
        self.pattern_database[pattern] += 1 if success else -1
    
    def _extract_pattern(self, position: str, move: str) -> str:
        """Extrai padrão de movimento para análise futura."""
        return f"{position[:4]}:{move[:4]}"
    
    def clear_caches(self):
        """Limpa caches quando necessário para gerenciar memória."""
        self.move_cache.clear()
        self.position_cache.clear()
