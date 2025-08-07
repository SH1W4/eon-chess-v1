#!/usr/bin/env python3
"""
Script para executar testes de integração web.
"""

import os
import sys
import time
import json
import signal
import subprocess
from pathlib import Path
from datetime import datetime

# Diretórios importantes
PROJECT_ROOT = Path(__file__).parent.parent
TEST_DIR = PROJECT_ROOT / "tests"
ARTIFACTS_DIR = TEST_DIR / "test_artifacts"

def setup_environment():
    """Configura o ambiente de teste."""
    # Configura variáveis de ambiente
    os.environ["TEST_ENV"] = "testing"
    os.environ["NODE_ENV"] = "test"
    
    # Cria diretórios para artefatos
    for dir_path in ["screenshots", "reports", "logs"]:
        (ARTIFACTS_DIR / dir_path).mkdir(parents=True, exist_ok=True)

def start_server():
    """Inicia o servidor Next.js em background."""
    print("\n=== Verificando servidor Next.js ===")
    
    # Verifica se o servidor anterior está rodando
    import requests
    from urllib3.exceptions import RequestError
    
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("Servidor já está rodando na porta 3000")
            return None
    except (requests.exceptions.ConnectionError, RequestError):
        print("Nenhum servidor encontrado na porta 3000, iniciando novo servidor...")
    
        server = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            bufsize=1,
            universal_newlines=True
        )
        
        # Aguarda o servidor inicializar
        print("Aguardando servidor inicializar...")
        
        ready = False
        start_time = time.time()
        while not ready and time.time() - start_time < 30:
            output = server.stdout.readline()
            if output:
                print(f"Server: {output.strip()}")
                if "ready - started server on" in output:
                    ready = True
            
            error = server.stderr.readline()
            if error:
                print(f"Error: {error.strip()}", file=sys.stderr)
            
            # Verifica também se a página está acessível
            try:
                response = requests.get("http://localhost:3000")
                if response.status_code == 200:
                    ready = True
                    break
            except:
                pass
        
        if not ready:
            raise Exception("Servidor não iniciou em 30 segundos")
        
        return server
    
    except Exception as e:
        print(f"Erro ao verificar/iniciar servidor: {e}")
        return None

def stop_server(server):
    """Para o servidor Next.js."""
    if server:
        os.kill(server.pid, signal.SIGTERM)
        print("\n=== Servidor finalizado ===")

def run_tests():
    """Executa os testes web."""
    print("\n=== Executando testes web ===")
    result = subprocess.run(
        ["pytest", "web/test_chess_components.py", "-v"],
        cwd=str(TEST_DIR),
        capture_output=True,
        text=True
    )
    return result

def save_report(start_time, end_time, test_result):
    """Salva relatório de execução."""
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
    
    report_file = ARTIFACTS_DIR / "reports" / "integration_report.json"
    report_file.write_text(json.dumps(report, indent=2))

def main():
    """Função principal."""
    setup_environment()
    server = None
    start_time = time.time()
    
    try:
        server = start_server()
        result = run_tests()
        
        end_time = time.time()
        save_report(start_time, end_time, result)
        
        # Exibe saída dos testes
        print(result.stdout)
        if result.stderr:
            print("\nErros:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
        
        print("\n=== Execução finalizada ===")
        print(f"Relatório disponível em: {ARTIFACTS_DIR}/reports/integration_report.json")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n=== Execução interrompida pelo usuário ===")
        return 1
        
    finally:
        if server:
            stop_server(server)

if __name__ == "__main__":
    sys.exit(main())
