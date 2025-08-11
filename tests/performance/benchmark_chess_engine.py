"""
Performance benchmarks for CHESS engine
Tests engine speed, memory usage, and scalability
"""

import time
import memory_profiler
import asyncio
from typing import List, Dict, Any
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core.board import Board
from src.ai.engine import ChessEngine
from src.cultural.manager import CulturalManager

class ChessPerformanceBenchmark:
    """Performance benchmark suite for CHESS engine"""
    
    def __init__(self):
        self.results = {
            "board_operations": {},
            "ai_performance": {},
            "cultural_system": {},
            "memory_usage": {},
            "scalability": {}
        }
        
    def benchmark_board_operations(self, iterations: int = 1000):
        """Benchmark basic board operations"""
        print(f"Running board operations benchmark ({iterations} iterations)...")
        
        # Board initialization
        start = time.perf_counter()
        for _ in range(iterations):
            board = Board()
        init_time = (time.perf_counter() - start) / iterations
        self.results["board_operations"]["initialization"] = init_time * 1000  # ms
        
        # Move generation
        board = Board()
        start = time.perf_counter()
        for _ in range(iterations):
            moves = board.get_legal_moves()
        move_gen_time = (time.perf_counter() - start) / iterations
        self.results["board_operations"]["move_generation"] = move_gen_time * 1000
        
        # Move execution
        moves_to_test = ["e2", "e4", "e7", "e5", "g1", "f3"]
        board = Board()
        start = time.perf_counter()
        for _ in range(iterations // 10):
            test_board = Board()
            for i in range(0, len(moves_to_test), 2):
                test_board.move_piece(moves_to_test[i], moves_to_test[i+1])
        move_exec_time = (time.perf_counter() - start) / (iterations // 10)
        self.results["board_operations"]["move_execution"] = move_exec_time * 1000
        
        # Check detection
        board = Board()
        board.move_piece("e2", "e4")
        board.move_piece("e7", "e5")
        board.move_piece("d1", "h5")
        board.move_piece("b8", "c6")
        board.move_piece("f1", "c4")
        board.move_piece("g8", "f6")
        board.move_piece("h5", "f7")  # Check
        
        start = time.perf_counter()
        for _ in range(iterations):
            is_check = board.is_in_check('black')
        check_time = (time.perf_counter() - start) / iterations
        self.results["board_operations"]["check_detection"] = check_time * 1000
        
        print(f"  Board initialization: {self.results['board_operations']['initialization']:.3f} ms")
        print(f"  Move generation: {self.results['board_operations']['move_generation']:.3f} ms")
        print(f"  Move execution: {self.results['board_operations']['move_execution']:.3f} ms")
        print(f"  Check detection: {self.results['board_operations']['check_detection']:.3f} ms")
    
    def benchmark_ai_performance(self, depth_levels: List[int] = [1, 2, 3]):
        """Benchmark AI engine at different depths"""
        print(f"Running AI performance benchmark (depths: {depth_levels})...")
        
        for depth in depth_levels:
            board = Board()
            engine = ChessEngine(depth=depth)
            
            # Measure time for best move calculation
            start = time.perf_counter()
            try:
                best_move = engine.get_best_move(board)
                elapsed = time.perf_counter() - start
                self.results["ai_performance"][f"depth_{depth}"] = {
                    "time": elapsed * 1000,  # ms
                    "nodes_per_second": engine.nodes_evaluated / elapsed if elapsed > 0 else 0
                }
                print(f"  Depth {depth}: {elapsed*1000:.1f} ms, {engine.nodes_evaluated} nodes")
            except Exception as e:
                print(f"  Depth {depth}: Error - {e}")
                self.results["ai_performance"][f"depth_{depth}"] = {
                    "time": None,
                    "error": str(e)
                }
    
    def benchmark_cultural_system(self, iterations: int = 100):
        """Benchmark cultural narrative system"""
        print(f"Running cultural system benchmark ({iterations} iterations)...")
        
        try:
            manager = CulturalManager()
            
            # Narrative generation
            start = time.perf_counter()
            for _ in range(iterations):
                narrative = manager.generate_move_narrative("e2", "e4", "pawn")
            narrative_time = (time.perf_counter() - start) / iterations
            self.results["cultural_system"]["narrative_generation"] = narrative_time * 1000
            
            # Event processing
            start = time.perf_counter()
            for _ in range(iterations):
                event = manager.process_cultural_event("capture", "knight", "bishop")
            event_time = (time.perf_counter() - start) / iterations
            self.results["cultural_system"]["event_processing"] = event_time * 1000
            
            print(f"  Narrative generation: {narrative_time*1000:.3f} ms")
            print(f"  Event processing: {event_time*1000:.3f} ms")
            
        except Exception as e:
            print(f"  Cultural system error: {e}")
            self.results["cultural_system"]["error"] = str(e)
    
    @memory_profiler.profile
    def benchmark_memory_usage(self):
        """Benchmark memory usage"""
        print("Running memory usage benchmark...")
        
        # Create multiple boards
        boards = []
        for i in range(100):
            board = Board()
            boards.append(board)
        
        # Create AI engines
        engines = []
        for i in range(10):
            engine = ChessEngine(depth=2)
            engines.append(engine)
        
        # Simulate gameplay
        for board in boards[:10]:
            board.move_piece("e2", "e4")
            board.move_piece("e7", "e5")
        
        # Memory stats will be printed by memory_profiler
        self.results["memory_usage"]["boards_created"] = len(boards)
        self.results["memory_usage"]["engines_created"] = len(engines)
    
    def benchmark_scalability(self):
        """Test scalability with concurrent games"""
        print("Running scalability benchmark...")
        
        async def play_game():
            """Simulate a game"""
            board = Board()
            moves = 0
            max_moves = 20
            
            while moves < max_moves and not board.is_game_over():
                legal_moves = board.get_legal_moves()
                if legal_moves:
                    # Make a random move
                    import random
                    move = random.choice(legal_moves)
                    board.make_move(move)
                    moves += 1
                else:
                    break
            
            return moves
        
        async def run_concurrent_games(num_games: int):
            """Run multiple games concurrently"""
            tasks = [play_game() for _ in range(num_games)]
            start = time.perf_counter()
            results = await asyncio.gather(*tasks)
            elapsed = time.perf_counter() - start
            return elapsed, results
        
        # Test different concurrency levels
        for num_games in [1, 10, 50, 100]:
            elapsed, moves = asyncio.run(run_concurrent_games(num_games))
            self.results["scalability"][f"games_{num_games}"] = {
                "total_time": elapsed,
                "time_per_game": elapsed / num_games,
                "avg_moves": sum(moves) / len(moves)
            }
            print(f"  {num_games} concurrent games: {elapsed:.2f}s ({elapsed/num_games:.3f}s per game)")
    
    def run_all_benchmarks(self):
        """Run all benchmarks"""
        print("=" * 60)
        print("CHESS ENGINE PERFORMANCE BENCHMARK")
        print("=" * 60)
        
        self.benchmark_board_operations()
        print()
        
        self.benchmark_ai_performance()
        print()
        
        self.benchmark_cultural_system()
        print()
        
        self.benchmark_memory_usage()
        print()
        
        self.benchmark_scalability()
        print()
        
        self.save_results()
        self.print_summary()
    
    def save_results(self):
        """Save benchmark results to file"""
        os.makedirs("performance_results", exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"performance_results/benchmark_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Results saved to {filename}")
    
    def print_summary(self):
        """Print performance summary"""
        print("=" * 60)
        print("PERFORMANCE SUMMARY")
        print("=" * 60)
        
        # Board operations
        if self.results["board_operations"]:
            print("Board Operations:")
            for op, time_ms in self.results["board_operations"].items():
                print(f"  {op}: {time_ms:.3f} ms")
        
        # AI performance
        if self.results["ai_performance"]:
            print("\nAI Performance:")
            for depth, data in self.results["ai_performance"].items():
                if data.get("time"):
                    print(f"  {depth}: {data['time']:.1f} ms")
        
        # Scalability
        if self.results["scalability"]:
            print("\nScalability:")
            for games, data in self.results["scalability"].items():
                print(f"  {games}: {data['time_per_game']:.3f}s per game")
        
        print("=" * 60)

def main():
    """Main benchmark runner"""
    benchmark = ChessPerformanceBenchmark()
    
    # Check for specific benchmark argument
    if len(sys.argv) > 1:
        if sys.argv[1] == "board":
            benchmark.benchmark_board_operations()
        elif sys.argv[1] == "ai":
            benchmark.benchmark_ai_performance()
        elif sys.argv[1] == "cultural":
            benchmark.benchmark_cultural_system()
        elif sys.argv[1] == "memory":
            benchmark.benchmark_memory_usage()
        elif sys.argv[1] == "scale":
            benchmark.benchmark_scalability()
        else:
            print(f"Unknown benchmark: {sys.argv[1]}")
            print("Available: board, ai, cultural, memory, scale")
    else:
        # Run all benchmarks
        benchmark.run_all_benchmarks()

if __name__ == "__main__":
    main()
