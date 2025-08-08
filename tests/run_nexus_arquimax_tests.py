#!/usr/bin/env python3
"""
Script principal para execução dos testes via NEXUS-ARQUIMAX.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

# Diretórios importantes
PROJECT_ROOT = Path(__file__).parent
TEST_DIR = PROJECT_ROOT / "tests"
ARTIFACTS_DIR = PROJECT_ROOT / "test_artifacts"

def setup_environment():
    """Configura o ambiente de testes."""
    print("=== Iniciando Integração NEXUS-ARQUIMAX ===")
    
    # Cria diretórios necessários
    for dir_path in ["screenshots", "reports", "coverage"]:
        (ARTIFACTS_DIR / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Configura variáveis de ambiente
    os.environ["PYTHONPATH"] = str(PROJECT_ROOT)
    os.environ["TEST_ARTIFACTS"] = str(ARTIFACTS_DIR)
    os.environ["NEXUS_ARQUIMAX_ACTIVE"] = "true"

def start_server():
    """Inicia o servidor Next.js em background."""
    print("\n--- Iniciando servidor Next.js ---")
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(10)  # Aguarda o servidor iniciar
    return process

def run_tests():
    """Executa os testes com monitoramento."""
    print("\n--- Executando testes ---")
    start_time = time.time()
    
    # Executa os testes
    result = subprocess.run([
        "pytest",
        "tests/web",
        "-v",
        "--html=test_artifacts/reports/report.html",
        "--self-contained-html",
        "--capture=no"
    ])
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Gera relatório
    report = {
        "summary": {
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(end_time).isoformat(),
            "duration": duration,
            "exit_code": result.returncode
        },
        "metrics": {
            "test_count": 8,  # Número fixo de testes
            "passed": result.returncode == 0,
            "performance": {
                "avg_response_time": duration / 8,  # Média por teste
                "total_time": duration
            }
        }
    }
    
    # Salva relatório
    report_path = ARTIFACTS_DIR / "reports/nexus_arquimax_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    return result.returncode

def main():
    """Função principal de execução."""
    setup_environment()
    server_process = None
    
    try:
        server_process = start_server()
        exit_code = run_tests()
        
        print("\n=== Execução concluída ===")
        print(f"Resultados disponíveis em: {ARTIFACTS_DIR}/reports/")
        
        return exit_code
        
    finally:
        if server_process:
            print("\n--- Finalizando servidor ---")
            server_process.terminate()

if __name__ == "__main__":
    sys.exit(main())
