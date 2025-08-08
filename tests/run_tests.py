"""
Script otimizado para execução de testes
"""
import subprocess
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pytest

def run_test_suite(pattern: str) -> dict:
    """Executa uma suíte de testes específica"""
    start_time = time.time()
    result = pytest.main([
        "-v",
        f"tests/{pattern}",
        "--cache-clear",
        "-W", "ignore::DeprecationWarning"
    ])
    end_time = time.time()
    
    return {
        "pattern": pattern,
        "success": result == 0,
        "time": end_time - start_time
    }

def run_parallel_tests():
    """Executa testes em paralelo"""
    test_patterns = [
        "test_board.py",
        "test_engine.py",
        "test_adaptive_ai.py",
        "test_core.py"
    ]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run_test_suite, test_patterns))
    
    return results

def run_sequential_tests():
    """Executa testes que precisam ser sequenciais"""
    patterns = [
        "test_integrated_system.py",
        "test_narrative.py",
        "integration/test_arquimax_nexus.py"
    ]
    
    results = []
    for pattern in patterns:
        results.append(run_test_suite(pattern))
    
    return results

def main():
    """Função principal"""
    print("\n=== Iniciando Execução Otimizada de Testes ===\n")
    
    print("Executando testes paralelos...")
    parallel_results = run_parallel_tests()
    
    print("\nExecutando testes sequenciais...")
    sequential_results = run_sequential_tests()
    
    all_results = parallel_results + sequential_results
    
    # Análise dos resultados
    success_count = sum(1 for r in all_results if r["success"])
    total_time = sum(r["time"] for r in all_results)
    
    print("\n=== Resumo da Execução ===")
    print(f"Total de suítes: {len(all_results)}")
    print(f"Suítes com sucesso: {success_count}")
    print(f"Suítes com falha: {len(all_results) - success_count}")
    print(f"Tempo total: {total_time:.2f}s")
    
    # Detalhes por suíte
    print("\nDetalhes por suíte:")
    for result in sorted(all_results, key=lambda x: x["time"]):
        status = "✓" if result["success"] else "✗"
        print(f"{status} {result['pattern']}: {result['time']:.2f}s")
    
    # Retorna código de erro se algum teste falhou
    if success_count < len(all_results):
        sys.exit(1)

if __name__ == "__main__":
    main()
