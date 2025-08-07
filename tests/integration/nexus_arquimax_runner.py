"""
Gerenciador de execução de testes integrado com NEXUS-ARQUIMAX.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from ..config.nexus_arquimax_config import get_config, TestCapability

class NexusArquimaxRunner:
    def __init__(self):
        self.config = get_config()
        self.test_suite = self.config.initialize_test_suite()
        self.results: Dict[str, Any] = {}
        self.start_time = None
        self.end_time = None

    def _setup_environment(self):
        """Configura o ambiente de testes."""
        env = self.test_suite["environment"]
        
        # Configura variáveis de ambiente
        os.environ["NEXUS_ARQUIMAX_ACTIVE"] = "true"
        os.environ["SELENIUM_BROWSER"] = env["browser_config"]["browser"]
        os.environ["TEST_ENVIRONMENT"] = "testing"
        
        # Garante que os diretórios existem
        Path(env["test_data"]["screenshot_dir"]).mkdir(parents=True, exist_ok=True)
        Path(env["test_data"]["report_dir"]).mkdir(parents=True, exist_ok=True)

    def _start_server(self):
        """Inicia o servidor Next.js em background."""
        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(10)  # Aguarda o servidor iniciar
            return process
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
            sys.exit(1)

    def _run_capability_tests(self, capability: TestCapability) -> Dict[str, Any]:
        """Executa os testes para uma capability específica."""
        print(f"\nExecutando testes para: {capability.name}")
        
        result = {
            "name": capability.name,
            "type": capability.type,
            "start_time": datetime.now().isoformat(),
            "status": "pending",
            "metrics": {},
            "errors": []
        }

        try:
            # Executa os testes baseado no tipo
            if capability.type == "selenium":
                subprocess.run(
                    ["pytest", "tests/web/test_chess_components.py", "-v"],
                    check=True
                )
            elif capability.type == "visual":
                subprocess.run(
                    ["pytest", "tests/web/test_chess_styles.py", "-v"],
                    check=True
                )
            elif capability.type == "unit":
                subprocess.run(
                    ["pytest", "tests/web/test_chess_logic.py", "-v"],
                    check=True
                )
            elif capability.type == "e2e":
                subprocess.run(
                    ["pytest", "tests/web/test_chess_interactions.py", "-v"],
                    check=True
                )

            result["status"] = "success"
            
        except subprocess.CalledProcessError as e:
            result["status"] = "failed"
            result["errors"].append(str(e))
        
        result["end_time"] = datetime.now().isoformat()
        return result

    def _collect_metrics(self, capability: TestCapability) -> Dict[str, Any]:
        """Coleta métricas de execução dos testes."""
        return {
            "duration": time.time() - self.start_time,
            "coverage": self._get_coverage(),
            "performance": self._get_performance_metrics()
        }

    def _get_coverage(self) -> Dict[str, float]:
        """Obtém métricas de cobertura de código."""
        try:
            coverage_file = Path("test_artifacts/reports/coverage.json")
            if coverage_file.exists():
                with open(coverage_file) as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {
            "statements": 0.0,
            "branches": 0.0,
            "functions": 0.0,
            "lines": 0.0
        }

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de performance dos testes."""
        return {
            "average_response_time": 0,
            "peak_memory_usage": 0,
            "total_requests": 0
        }

    def _generate_report(self):
        """Gera relatório final dos testes."""
        report = {
            "summary": {
                "start_time": self.start_time,
                "end_time": self.end_time,
                "duration": self.end_time - self.start_time,
                "total_tests": len(self.results),
                "passed": len([r for r in self.results.values() if r["status"] == "success"]),
                "failed": len([r for r in self.results.values() if r["status"] == "failed"])
            },
            "results": self.results,
            "metrics": {
                "coverage": self._get_coverage(),
                "performance": self._get_performance_metrics()
            }
        }

        # Salva o relatório
        report_path = Path("test_artifacts/reports/nexus_arquimax_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def run(self):
        """Executa a suite de testes completa."""
        print("=== Iniciando execução NEXUS-ARQUIMAX ===")
        
        self.start_time = time.time()
        self._setup_environment()
        
        # Inicia o servidor
        server_process = self._start_server()
        
        try:
            # Executa os testes em ordem de prioridade
            for capability in self.test_suite["test_order"]:
                # Verifica dependências
                if not all(self.results.get(dep, {}).get("status") == "success" 
                          for dep in capability.dependencies):
                    print(f"Pulando {capability.name} - dependências não satisfeitas")
                    continue
                
                # Executa os testes
                result = self._run_capability_tests(capability)
                
                # Coleta métricas
                result["metrics"] = self._collect_metrics(capability)
                
                # Armazena resultados
                self.results[capability.name] = result
        
        finally:
            # Finaliza o servidor
            if server_process:
                server_process.terminate()
            
            self.end_time = time.time()
            
            # Gera relatório
            report = self._generate_report()
            
            # Exibe resumo
            print("\n=== Resumo da Execução ===")
            print(f"Duração total: {report['summary']['duration']:.2f}s")
            print(f"Testes executados: {report['summary']['total_tests']}")
            print(f"Sucesso: {report['summary']['passed']}")
            print(f"Falhas: {report['summary']['failed']}")
            print("\nRelatório completo disponível em: test_artifacts/reports/nexus_arquimax_report.json")

def main():
    runner = NexusArquimaxRunner()
    runner.run()

if __name__ == "__main__":
    main()
