import time
import statistics
from typing import Dict, List, Tuple
from core.board.board import Board, PieceType, Color, Piece
from cultural.memory import CulturalMemory
from cultural.events import CulturalEventSystem
from cultural.style_analyzer import CulturalStyleAnalyzer
from cultural.cultures import persian_culture, mongol_culture, chinese_culture

class CulturalBenchmark:
    """Benchmark para medir performance do sistema cultural"""
    
    def __init__(self):
        self.results = {}
        
    def run_benchmark(self, num_iterations: int = 100):
        """Executa uma série de benchmarks"""
        print("\n=== Iniciando Benchmark Cultural ===\n")
        
        # Benchmark de Memória Cultural
        self.benchmark_memory(num_iterations)
        
        # Benchmark de Eventos
        self.benchmark_events(num_iterations)
        
        # Benchmark de Análise de Estilo
        self.benchmark_style_analysis(num_iterations)
        
        # Benchmark de Integração
        self.benchmark_integration(num_iterations)
        
        # Exibe resultados
        self.print_results()
    
    def benchmark_memory(self, iterations: int):
        """Benchmark das operações de memória"""
        memory = CulturalMemory()
        piece = Piece(PieceType.PAWN, Color.WHITE)
        
        # Teste de registro de movimentos
        times = []
        for _ in range(iterations):
            start = time.time()
            memory.record_move(piece, "e2", "e4", 0.5)
            end = time.time()
            times.append(end - start)
        
        self.results['memory_record'] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
        
    def benchmark_events(self, iterations: int):
        """Benchmark do sistema de eventos"""
        event_system = CulturalEventSystem()
        board_state = {
            'position': 'test position',
            'current_move': ('e2', 'e4'),
            'piece': Piece(PieceType.PAWN, Color.WHITE)
        }
        
        # Teste de verificação de eventos
        times = []
        for _ in range(iterations):
            start = time.time()
            event_system.check_event_triggers(board_state, persian_culture)
            end = time.time()
            times.append(end - start)
        
        self.results['event_check'] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
        
    def benchmark_style_analysis(self, iterations: int):
        """Benchmark da análise de estilo"""
        analyzer = CulturalStyleAnalyzer()
        memory = CulturalMemory()
        piece = Piece(PieceType.PAWN, Color.WHITE)
        
        # Prepara dados
        for _ in range(10):  # Simula 10 movimentos
            memory.record_move(piece, "e2", "e4", 0.5)
        
        # Teste de análise de estilo
        times = []
        for _ in range(iterations):
            start = time.time()
            analyzer.analyze_game_style(memory, persian_culture)
            end = time.time()
            times.append(end - start)
        
        self.results['style_analysis'] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
        
    def benchmark_integration(self, iterations: int):
        """Benchmark de integração completa"""
        times = []
        
        for _ in range(iterations):
            start = time.time()
            
            # Setup
            board = Board()
            memory = CulturalMemory()
            event_system = CulturalEventSystem()
            analyzer = CulturalStyleAnalyzer()
            
            # Executa uma sequência de movimentos
            moves = [
                ("e2", "e4", persian_culture),
                ("e7", "e5", mongol_culture),
                ("g1", "f3", persian_culture),
                ("b8", "c6", mongol_culture)
            ]
            
            for from_pos, to_pos, culture in moves:
                piece = board.get_piece(from_pos)
                if piece:
                    # Verifica eventos
                    board_state = {
                        'position': board.display(),
                        'current_move': (from_pos, to_pos),
                        'piece': piece
                    }
                    events = event_system.check_event_triggers(board_state, culture)
                    
                    # Executa movimento
                    board.move_piece(from_pos, to_pos)
                    
                    # Registra na memória
                    memory.record_move(piece, from_pos, to_pos, 0.5)
            
            # Análise final
            analyzer.analyze_game_style(memory, persian_culture)
            analyzer.analyze_game_style(memory, mongol_culture)
            
            end = time.time()
            times.append(end - start)
        
        self.results['full_integration'] = {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0
        }
    
    def print_results(self):
        """Imprime os resultados do benchmark"""
        print("\n=== Resultados do Benchmark ===\n")
        
        for test_name, metrics in self.results.items():
            print(f"Teste: {test_name}")
            print(f"- Média: {metrics['mean']*1000:.2f}ms")
            print(f"- Mediana: {metrics['median']*1000:.2f}ms")
            print(f"- Desvio Padrão: {metrics['std_dev']*1000:.2f}ms")
            print()
        
        # Análise de gargalos
        slowest_test = max(self.results.items(), key=lambda x: x[1]['mean'])
        print("Análise de Performance:")
        print(f"- Operação mais lenta: {slowest_test[0]}")
        print(f"- Tempo médio: {slowest_test[1]['mean']*1000:.2f}ms")
        
        # Recomendações
        print("\nRecomendações de Otimização:")
        for test_name, metrics in self.results.items():
            if metrics['mean'] > 0.001:  # mais de 1ms
                print(f"- Considerar otimização de {test_name}")
                if metrics['std_dev'] > metrics['mean'] * 0.5:
                    print(f"  * Alta variabilidade em {test_name}")

def run_benchmark():
    """Executa o benchmark completo"""
    benchmark = CulturalBenchmark()
    benchmark.run_benchmark(num_iterations=100)

if __name__ == "__main__":
    run_benchmark()
