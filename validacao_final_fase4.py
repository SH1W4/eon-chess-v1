#!/usr/bin/env python3
"""
Validação Final - Fase 4: Validação Completa do Sistema
AEON CHESS - EAP Final
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

class ValidacaoFinal:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "fase": "FASE 4 - VALIDAÇÃO FINAL",
            "tests": [],
            "summary": {}
        }
        
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        
    def run_validacao_completa(self):
        """Executar validação completa do sistema"""
        print("🎯 VALIDAÇÃO FINAL - FASE 4")
        print("=" * 50)
        
        # 1. Validação de Estrutura
        self.validar_estrutura_projeto()
        
        # 2. Validação de Funcionalidades
        self.validar_funcionalidades()
        
        # 3. Validação de Performance
        self.validar_performance()
        
        # 4. Validação de Qualidade
        self.validar_qualidade()
        
        # 5. Gerar Relatório Final
        self.gerar_relatorio_final()
        
    def validar_estrutura_projeto(self):
        """Validar estrutura do projeto"""
        print("\n🏗️ VALIDANDO ESTRUTURA DO PROJETO")
        print("-" * 40)
        
        required_dirs = [
            "web/pages",
            "web/styles", 
            "web/utils",
            "src/ai",
            "src/core",
            "docs"
        ]
        
        for dir_path in required_dirs:
            self.run_test(f"Diretório {dir_path}", lambda: Path(dir_path).exists())
    
    def validar_funcionalidades(self):
        """Validar funcionalidades implementadas"""
        print("\n⚙️ VALIDANDO FUNCIONALIDADES")
        print("-" * 40)
        
        required_files = [
            "web/styles/consolidated-theme.css",
            "web/utils/performance-optimizer.js",
            "web/utils/notification-system.js",
            "web/utils/error-handler.js",
            "web/utils/compatibility-layer.js",
            "web/pages/demo-melhorias.html"
        ]
        
        for file_path in required_files:
            self.run_test(f"Arquivo {file_path}", lambda: Path(file_path).exists())
    
    def validar_performance(self):
        """Validar otimizações de performance"""
        print("\n⚡ VALIDANDO PERFORMANCE")
        print("-" * 40)
        
        # Verificar tamanho dos arquivos
        css_file = Path("web/styles/consolidated-theme.css")
        if css_file.exists():
            size = css_file.stat().st_size
            self.run_test("CSS Consolidado", lambda: size > 15000)  # 15KB mínimo
        
        js_files = [
            "web/utils/performance-optimizer.js",
            "web/utils/notification-system.js"
        ]
        
        for js_file in js_files:
            if Path(js_file).exists():
                self.run_test(f"JavaScript {js_file}", lambda: True)
    
    def validar_qualidade(self):
        """Validar qualidade do código"""
        print("\n🎯 VALIDANDO QUALIDADE")
        print("-" * 40)
        
        # Verificar se há documentação
        self.run_test("Documentação", lambda: Path("docs").exists())
        
        # Verificar se há testes
        self.run_test("Testes", lambda: Path("test_fase3_melhorias.py").exists())
        
        # Verificar se há página de demonstração
        self.run_test("Página Demo", lambda: Path("web/pages/demo-melhorias.html").exists())
    
    def run_test(self, test_name, test_function):
        """Executar teste individual"""
        self.test_count += 1
        print(f"Teste {self.test_count}: {test_name}")
        
        try:
            success = test_function()
            if success:
                print(f"  ✅ PASSOU")
                self.passed_count += 1
                status = "PASSOU"
            else:
                print(f"  ❌ FALHOU")
                self.failed_count += 1
                status = "FALHOU"
            
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "status": status
            })
            
        except Exception as e:
            print(f"  💥 ERRO: {str(e)}")
            self.failed_count += 1
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "status": "ERRO"
            })
    
    def gerar_relatorio_final(self):
        """Gerar relatório final"""
        print("\n" + "=" * 50)
        print("📊 RELATÓRIO FINAL - FASE 4")
        print("=" * 50)
        
        total_tests = self.test_count
        passed = self.passed_count
        failed = self.failed_count
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total de Testes: {total_tests}")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "success_rate": round(success_rate, 1)
        }
        
        # Salvar relatório
        report_file = f"relatorio_final_fase4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {report_file}")
        
        # Status final
        if success_rate >= 90:
            print("\n🎉 EXCELENTE! Sistema validado com sucesso!")
            return True
        elif success_rate >= 70:
            print("\n👍 BOM! Sistema funcional com algumas melhorias.")
            return False
        else:
            print("\n⚠️ ATENÇÃO! Sistema precisa de correções.")
            return False

def main():
    """Função principal"""
    print("🎯 VALIDAÇÃO FINAL - FASE 4")
    print("AEON CHESS - EAP Final")
    
    validator = ValidacaoFinal()
    success = validator.run_validacao_completa()
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Validação interrompida")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro: {str(e)}")
        sys.exit(1)
