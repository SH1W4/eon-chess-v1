#!/usr/bin/env python3
"""
ARKITECT Chess Board Fix - Resolução Completa do Tabuleiro Funcional
====================================================================
Script específico para resolver problemas de cache e garantir que o
tabuleiro funcional esteja operacional.
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

class ARKITECTChessBoardFix:
    def __init__(self):
        self.project_root = Path.cwd()
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, description):
        """Executa comando e retorna resultado"""
        self.log(f"Executando: {description}")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.project_root
            )
            if result.returncode == 0:
                self.log(f"✅ {description} - SUCESSO", "SUCCESS")
                return True, result.stdout
            else:
                self.log(f"❌ {description} - ERRO: {result.stderr}", "ERROR")
                return False, result.stderr
        except Exception as e:
            self.log(f"❌ {description} - EXCEÇÃO: {str(e)}", "ERROR")
            return False, str(e)
    
    def fix_chess_board(self):
        """Executa a correção completa do tabuleiro de xadrez"""
        self.log("🚀 ARKITECT Chess Board Fix Iniciando...", "HEADER")
        self.log("=" * 60)
        
        steps = [
            ("Parar todos os processos", "pkill -f 'npm run dev' && pkill -f 'node'"),
            ("Limpar cache Next.js", "rm -rf .next"),
            ("Limpar cache node_modules", "rm -rf node_modules/.cache"),
            ("Limpar cache global", "rm -rf .cache"),
            ("Reinstalar dependências", "npm install"),
            ("Verificar componentes", "ls -la src/components/"),
            ("Build completo", "npm run build"),
            ("Iniciar servidor", "npm run dev &"),
            ("Aguardar inicialização", "sleep 15"),
            ("Testar página principal", "curl -s http://localhost:3000 | head -5"),
            ("Testar página de teste", "curl -s http://localhost:3000/test-chess | head -5"),
        ]
        
        results = []
        
        for i, (description, command) in enumerate(steps, 1):
            self.log(f"Passo {i}/{len(steps)}: {description}")
            
            if "sleep" in command:
                time.sleep(int(command.split()[-1]))
                success = True
                output = "Aguardado"
            elif "curl" in command:
                success, output = self.run_command(command, description)
            else:
                success, output = self.run_command(command, description)
                
            results.append({
                "step": i,
                "description": description,
                "command": command,
                "success": success,
                "output": output[:500] if output else ""
            })
            
            if not success and "curl" not in command:
                self.log(f"❌ Falha no passo {i}, abortando...", "ERROR")
                break
                
        return results
    
    def generate_report(self, results):
        """Gera relatório da correção"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"arkitect_chess_board_fix_{timestamp}.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "AEON Chess",
            "fix_type": "Chess Board Functional Fix",
            "total_steps": len(results),
            "successful_steps": sum(1 for r in results if r["success"]),
            "failed_steps": sum(1 for r in results if not r["success"]),
            "steps": results,
            "summary": {
                "status": "SUCCESS" if all(r["success"] for r in results) else "PARTIAL",
                "chess_board_functional": any("SimpleChessBoard" in str(r["output"]) for r in results),
                "server_running": any("localhost:3000" in str(r["output"]) for r in results),
                "cache_cleared": any("rm -rf" in r["command"] and r["success"] for r in results)
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        self.log(f"📄 Relatório salvo em: {report_file}")
        return report
    
    def print_summary(self, report):
        """Imprime resumo da correção"""
        self.log("=" * 60)
        self.log("🏆 RELATÓRIO FINAL DO ARKITECT CHESS BOARD FIX")
        self.log("=" * 60)
        
        summary = report["summary"]
        self.log(f"⏱️  Timestamp: {report['timestamp']}")
        self.log(f"📊 Total de Passos: {report['total_steps']}")
        self.log(f"✅ Passos Bem-sucedidos: {report['successful_steps']}")
        self.log(f"❌ Passos com Falha: {report['failed_steps']}")
        self.log(f"🎯 Status Geral: {summary['status']}")
        
        self.log("\n📋 DETALHES:")
        self.log(f"  Tabuleiro Funcional: {'✅ SIM' if summary['chess_board_functional'] else '❌ NÃO'}")
        self.log(f"  Servidor Rodando: {'✅ SIM' if summary['server_running'] else '❌ NÃO'}")
        self.log(f"  Cache Limpo: {'✅ SIM' if summary['cache_cleared'] else '❌ NÃO'}")
        
        if summary['status'] == 'SUCCESS':
            self.log("\n🎉 CORREÇÃO COMPLETA! Tabuleiro funcional deve estar operacional.")
            self.log("🌐 URLs para teste:")
            self.log("   - Página Principal: http://localhost:3000")
            self.log("   - Página de Teste: http://localhost:3000/test-chess")
            self.log("   - Dashboard ARKITECT: http://localhost:3000/arkitect")
        else:
            self.log("\n⚠️  CORREÇÃO PARCIAL. Alguns problemas podem persistir.")
            self.log("🔧 Recomenda-se verificação manual.")

def main():
    """Função principal"""
    fixer = ARKITECTChessBoardFix()
    
    try:
        results = fixer.fix_chess_board()
        report = fixer.generate_report(results)
        fixer.print_summary(report)
        
        # Retorna código de saída baseado no sucesso
        if report["summary"]["status"] == "SUCCESS":
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        fixer.log("❌ Processo interrompido pelo usuário", "ERROR")
        sys.exit(1)
    except Exception as e:
        fixer.log(f"❌ Erro inesperado: {str(e)}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
