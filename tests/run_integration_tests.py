#!/usr/bin/env python3
"""
Script para executar testes de integração web.
"""    """





t os
import sys
import time
import json
import signal
import subprocess
from pathlib import Path
from datetime import datetime

def setup_environment():
    \"\"\"Configura o ambiente de teste.\"\"\"
    # Configura variáveis de ambiente
    os.environ["TEST_ENV"] = "testing"
    os.environ["NODE_ENV"] = "test"
    
    # Cria diretórios para artefatos
    for dir_path in ["test_artifacts/screenshots", "test_artifacts/reports", "test_artifacts/logs"]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def start_server():
    \"\"\"Inicia o servidor Next.js em background.\"\"\"\n
    print("\\n=== Iniciando servidor Next.js ===")
    server = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguarda o servidor inicializar
    print("Aguardando servidor inicializar...")
    time.sleep(10)
    return server

def stop_server(server):
    \"\"\"Para o servidor Next.js.\"\"\"
    if server:
        os.kill(server.pid, signal.SIGTERM)
        print("\\n=== Servidor finalizado ===")

def run_tests():
    \"\"\"Executa os testes web.\"\"\"
    print("\\n=== Executando testes web ===")
    result = subprocess.run(
        ["pytest", "tests/web/test_chess_components.py", "-v"],
        capture_output=True,
        text=True
    )
    return result

def save_report(start_time, end_time, test_result):
    \"\"\"Salva relatório de execução.\"\"\"
    report = {
        "test_run": {
            "status": "success" if test_result.returncode == 0 else "failure",
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(end_time).isoformat(),
            "duration": end_time - start_time,
            "stdout": test_result.stdout,
            "stderr": test_result.stderr
        }
    }
    
    report_file = Path("test_artifacts/reports/integration_report.json")
    report_file.write_text(json.dumps(report, indent=2))

def main():
    \"\"\"Função principal.\"\"\"
    setup_environment()
    server = None
    start_time = time.time()
    
    try:
        server = start_server()
        result = run_tests()
        
        end_time = time.time()
        save_report(start_time, end_time, result)
        
        print("\\n=== Execução finalizada ===")
        print(f"Relatório disponível em: {os.path.abspath('test_artifacts/reports/integration_report.json')}")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\\n=== Execução interrompida pelo usuário ===")
        return 1
        
    finally:
        if server:
            stop_server(server)

if __name__ == "__main__":
    sys.exit(main())
