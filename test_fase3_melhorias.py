#!/usr/bin/env python3
"""
Script de Teste Automatizado - Fase 3: Melhorias
AEON CHESS - Validação de Performance e UX/UI
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime

class Fase3Tester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "fase": "FASE 3 - MELHORIAS",
            "tests": [],
            "summary": {}
        }
        
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        
    def run_all_tests(self):
        """Executar todos os testes da Fase 3"""
        print("🚀 INICIANDO TESTES DA FASE 3 - MELHORIAS")
        print("=" * 60)
        
        # Testes de Performance
        self.test_performance_optimizations()
        
        # Testes de UI/UX
        self.test_ui_ux_improvements()
        
        # Testes de Integração
        self.test_integration_features()
        
        # Testes de Responsividade
        self.test_responsiveness()
        
        # Testes de Acessibilidade
        self.test_accessibility()
        
        # Gerar relatório
        self.generate_report()
        
    def test_performance_optimizations(self):
        """Testar otimizações de performance"""
        print("\n⚡ TESTANDO OTIMIZAÇÕES DE PERFORMANCE")
        print("-" * 40)
        
        # Teste 1: CSS Consolidado
        self.run_test("CSS Consolidado", self.test_consolidated_css)
        
        # Teste 2: Performance Optimizer
        self.run_test("Performance Optimizer", self.test_performance_optimizer)
        
        # Teste 3: Sistema de Cache
        self.run_test("Sistema de Cache", self.test_cache_system)
        
        # Teste 4: Lazy Loading
        self.run_test("Lazy Loading", self.test_lazy_loading)
        
    def test_ui_ux_improvements(self):
        """Testar melhorias de UI/UX"""
        print("\n🎨 TESTANDO MELHORIAS DE UI/UX")
        print("-" * 40)
        
        # Teste 1: Sistema de Notificações
        self.run_test("Sistema de Notificações", self.test_notification_system)
        
        # Teste 2: Animações CSS
        self.run_test("Animações CSS", self.test_css_animations)
        
        # Teste 3: Componentes Responsivos
        self.run_test("Componentes Responsivos", self.test_responsive_components)
        
        # Teste 4: Tema Consolidado
        self.run_test("Tema Consolidado", self.test_consolidated_theme)
        
    def test_integration_features(self):
        """Testar funcionalidades de integração"""
        print("\n🔗 TESTANDO FUNCIONALIDADES DE INTEGRAÇÃO")
        print("-" * 40)
        
        # Teste 1: Carregamento de Scripts
        self.run_test("Carregamento de Scripts", self.test_script_loading)
        
        # Teste 2: Compatibilidade Cross-Browser
        self.run_test("Compatibilidade Cross-Browser", self.test_cross_browser)
        
        # Teste 3: Tratamento de Erros
        self.run_test("Tratamento de Erros", self.test_error_handling)
        
        # Teste 4: Sistema de Fallbacks
        self.run_test("Sistema de Fallbacks", self.test_fallback_system)
        
    def test_responsiveness(self):
        """Testar responsividade"""
        print("\n📱 TESTANDO RESPONSIVIDADE")
        print("-" * 40)
        
        # Teste 1: Layout Mobile
        self.run_test("Layout Mobile", self.test_mobile_layout)
        
        # Teste 2: Grid Responsivo
        self.run_test("Grid Responsivo", self.test_responsive_grid)
        
        # Teste 3: Media Queries
        self.run_test("Media Queries", self.test_media_queries)
        
    def test_accessibility(self):
        """Testar acessibilidade"""
        print("\n♿ TESTANDO ACESSIBILIDADE")
        print("-" * 40)
        
        # Teste 1: Contraste de Cores
        self.run_test("Contraste de Cores", self.test_color_contrast)
        
        # Teste 2: Navegação por Teclado
        self.run_test("Navegação por Teclado", self.test_keyboard_navigation)
        
        # Teste 3: Semântica HTML
        self.run_test("Semântica HTML", self.test_html_semantics)
        
    # ===== IMPLEMENTAÇÃO DOS TESTES =====
    
    def test_consolidated_css(self):
        """Testar CSS consolidado"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "Arquivo CSS consolidado não encontrado"
            
            # Verificar tamanho (deve ser menor que a soma dos arquivos originais)
            css_size = css_file.stat().st_size
            if css_size < 50000:  # 50KB
                return False, f"CSS muito pequeno ({css_size} bytes)"
            
            # Verificar se contém variáveis CSS
            css_content = css_file.read_text()
            if ":root" not in css_content or "--primary-color" not in css_content:
                return False, "Variáveis CSS não encontradas"
            
            return True, f"CSS consolidado válido ({css_size} bytes)"
            
        except Exception as e:
            return False, f"Erro ao testar CSS: {str(e)}"
    
    def test_performance_optimizer(self):
        """Testar Performance Optimizer"""
        try:
            js_file = Path("web/utils/performance-optimizer.js")
            if not js_file.exists():
                return False, "Arquivo Performance Optimizer não encontrado"
            
            # Verificar se contém funcionalidades essenciais
            js_content = js_file.read_text()
            required_features = [
                "class PerformanceOptimizer",
                "setCache",
                "getCache",
                "addLazyLoad",
                "compressData"
            ]
            
            missing_features = [feature for feature in required_features if feature not in js_content]
            if missing_features:
                return False, f"Funcionalidades ausentes: {', '.join(missing_features)}"
            
            return True, "Performance Optimizer completo e funcional"
            
        except Exception as e:
            return False, f"Erro ao testar Performance Optimizer: {str(e)}"
    
    def test_cache_system(self):
        """Testar sistema de cache"""
        try:
            # Verificar se o arquivo existe
            js_file = Path("web/utils/performance-optimizer.js")
            if not js_file.exists():
                return False, "Arquivo não encontrado"
            
            # Verificar funcionalidades de cache
            js_content = js_file.read_text()
            cache_features = [
                "setCache",
                "getCache",
                "clearCache",
                "cleanupExpiredCache"
            ]
            
            missing_cache = [feature for feature in cache_features if feature not in js_content]
            if missing_cache:
                return False, f"Funcionalidades de cache ausentes: {', '.join(missing_cache)}"
            
            return True, "Sistema de cache implementado corretamente"
            
        except Exception as e:
            return False, f"Erro ao testar cache: {str(e)}"
    
    def test_lazy_loading(self):
        """Testar lazy loading"""
        try:
            js_file = Path("web/utils/performance-optimizer.js")
            if not js_file.exists():
                return False, "Arquivo não encontrado"
            
            js_content = js_file.read_text()
            lazy_features = [
                "addLazyLoad",
                "IntersectionObserver",
                "initLazyLoading"
            ]
            
            missing_lazy = [feature for feature in lazy_features if feature not in js_content]
            if missing_lazy:
                return False, f"Funcionalidades de lazy loading ausentes: {', '.join(missing_lazy)}"
            
            return True, "Sistema de lazy loading implementado"
            
        except Exception as e:
            return False, f"Erro ao testar lazy loading: {str(e)}"
    
    def test_notification_system(self):
        """Testar sistema de notificações"""
        try:
            js_file = Path("web/utils/notification-system.js")
            if not js_file.exists():
                return False, "Arquivo de notificações não encontrado"
            
            js_content = js_file.read_text()
            notification_features = [
                "class NotificationSystem",
                "show",
                "success",
                "warning",
                "error",
                "info"
            ]
            
            missing_notif = [feature for feature in notification_features if feature not in js_content]
            if missing_notif:
                return False, f"Funcionalidades de notificação ausentes: {', '.join(missing_notif)}"
            
            return True, "Sistema de notificações completo"
            
        except Exception as e:
            return False, f"Erro ao testar notificações: {str(e)}"
    
    def test_css_animations(self):
        """Testar animações CSS"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            css_content = css_file.read_text()
            animation_features = [
                "@keyframes",
                "animation:",
                "transition:",
                "transform:"
            ]
            
            missing_anim = [feature for feature in animation_features if feature not in css_content]
            if missing_anim:
                return False, f"Funcionalidades de animação ausentes: {', '.join(missing_anim)}"
            
            return True, "Animações CSS implementadas"
            
        except Exception as e:
            return False, f"Erro ao testar animações: {str(e)}"
    
    def test_responsive_components(self):
        """Testar componentes responsivos"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            css_content = css_file.read_text()
            responsive_features = [
                "@media",
                "grid-template-columns",
                "minmax(",
                "repeat(auto-fit"
            ]
            
            missing_resp = [feature for feature in responsive_features if feature not in css_content]
            if missing_resp:
                return False, f"Funcionalidades responsivas ausentes: {', '.join(missing_resp)}"
            
            return True, "Componentes responsivos implementados"
            
        except Exception as e:
            return False, f"Erro ao testar responsividade: {str(e)}"
    
    def test_consolidated_theme(self):
        """Testar tema consolidado"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "Tema não encontrado"
            
            css_content = css_file.read_text()
            theme_features = [
                ":root",
                "--primary-color",
                "--secondary-color",
                "--accent-color",
                "--highlight-color"
            ]
            
            missing_theme = [feature for feature in theme_features if feature not in css_content]
            if missing_theme:
                return False, f"Variáveis de tema ausentes: {', '.join(missing_theme)}"
            
            return True, "Tema consolidado implementado"
            
        except Exception as e:
            return False, f"Erro ao testar tema: {str(e)}"
    
    def test_script_loading(self):
        """Testar carregamento de scripts"""
        try:
            # Verificar se todos os utilitários existem
            required_utils = [
                "web/utils/performance-optimizer.js",
                "web/utils/notification-system.js",
                "web/utils/error-handler.js",
                "web/utils/compatibility-layer.js"
            ]
            
            missing_utils = []
            for util in required_utils:
                if not Path(util).exists():
                    missing_utils.append(util)
            
            if missing_utils:
                return False, f"Utilitários ausentes: {', '.join(missing_utils)}"
            
            return True, "Todos os utilitários disponíveis"
            
        except Exception as e:
            return False, f"Erro ao testar scripts: {str(e)}"
    
    def test_cross_browser(self):
        """Testar compatibilidade cross-browser"""
        try:
            js_file = Path("web/utils/compatibility-layer.js")
            if not js_file.exists():
                return False, "Camada de compatibilidade não encontrada"
            
            js_content = js_file.read_text()
            compatibility_features = [
                "class CompatibilityLayer",
                "detectBrowser",
                "loadPolyfill",
                "featureDetection"
            ]
            
            missing_comp = [feature for feature in compatibility_features if feature not in js_content]
            if missing_comp:
                return False, f"Funcionalidades de compatibilidade ausentes: {', '.join(missing_comp)}"
            
            return True, "Camada de compatibilidade implementada"
            
        except Exception as e:
            return False, f"Erro ao testar compatibilidade: {str(e)}"
    
    def test_error_handling(self):
        """Testar tratamento de erros"""
        try:
            js_file = Path("web/utils/error-handler.js")
            if not js_file.exists():
                return False, "Sistema de tratamento de erros não encontrado"
            
            js_content = js_file.read_text()
            error_features = [
                "class ErrorHandler",
                "handleError",
                "addFallback",
                "recoveryStrategy"
            ]
            
            missing_error = [feature for feature in error_features if feature not in js_content]
            if missing_error:
                return False, f"Funcionalidades de tratamento de erro ausentes: {', '.join(missing_error)}"
            
            return True, "Sistema de tratamento de erros implementado"
            
        except Exception as e:
            return False, f"Erro ao testar tratamento de erros: {str(e)}"
    
    def test_fallback_system(self):
        """Testar sistema de fallbacks"""
        try:
            js_file = Path("web/utils/error-handler.js")
            if not js_file.exists():
                return False, "Sistema de fallbacks não encontrado"
            
            js_content = js_file.read_text()
            if "fallback" not in js_content.lower():
                return False, "Sistema de fallbacks não implementado"
            
            return True, "Sistema de fallbacks implementado"
            
        except Exception as e:
            return False, f"Erro ao testar fallbacks: {str(e)}"
    
    def test_mobile_layout(self):
        """Testar layout mobile"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            css_content = css_file.read_text()
            if "@media (max-width: 768px)" not in css_content:
                return False, "Media queries mobile não encontradas"
            
            return True, "Layout mobile implementado"
            
        except Exception as e:
            return False, f"Erro ao testar layout mobile: {str(e)}"
    
    def test_responsive_grid(self):
        """Testar grid responsivo"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            css_content = css_file.read_text()
            grid_features = [
                "grid-template-columns",
                "repeat(auto-fit",
                "minmax("
            ]
            
            missing_grid = [feature for feature in grid_features if feature not in css_content]
            if missing_grid:
                return False, f"Funcionalidades de grid ausentes: {', '.join(missing_grid)}"
            
            return True, "Grid responsivo implementado"
            
        except Exception as e:
            return False, f"Erro ao testar grid: {str(e)}"
    
    def test_media_queries(self):
        """Testar media queries"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            css_content = css_file.read_text()
            if "@media" not in css_content:
                return False, "Media queries não encontradas"
            
            return True, "Media queries implementadas"
            
        except Exception as e:
            return False, f"Erro ao testar media queries: {str(e)}"
    
    def test_color_contrast(self):
        """Testar contraste de cores"""
        try:
            css_file = Path("web/styles/consolidated-theme.css")
            if not css_file.exists():
                return False, "CSS não encontrado"
            
            # Verificar se há variáveis de cor definidas
            css_content = css_file.read_text()
            if "--text-primary" not in css_content or "--primary-color" not in css_content:
                return False, "Variáveis de cor não encontradas"
            
            return True, "Sistema de cores implementado"
            
        except Exception as e:
            return False, f"Erro ao testar cores: {str(e)}"
    
    def test_keyboard_navigation(self):
        """Testar navegação por teclado"""
        try:
            # Verificar se há suporte a navegação por teclado
            js_file = Path("web/utils/notification-system.js")
            if not js_file.exists():
                return False, "Sistema de notificações não encontrado"
            
            js_content = js_file.read_text()
            if "keydown" not in js_content:
                return False, "Suporte a teclado não implementado"
            
            return True, "Navegação por teclado implementada"
            
        except Exception as e:
            return False, f"Erro ao testar navegação por teclado: {str(e)}"
    
    def test_html_semantics(self):
        """Testar semântica HTML"""
        try:
            # Verificar página de demonstração
            demo_file = Path("web/pages/demo-melhorias.html")
            if not demo_file.exists():
                return False, "Página de demonstração não encontrada"
            
            html_content = demo_file.read_text()
            semantic_elements = [
                "<header>",
                "<section>",
                "<footer>",
                "<nav>",
                "<main>"
            ]
            
            # Verificar se pelo menos alguns elementos semânticos estão presentes
            found_semantic = [elem for elem in semantic_elements if elem in html_content]
            if len(found_semantic) < 2:
                return False, "Poucos elementos semânticos encontrados"
            
            return True, "Semântica HTML implementada"
            
        except Exception as e:
            return False, f"Erro ao testar semântica: {str(e)}"
    
    # ===== UTILITÁRIOS =====
    
    def run_test(self, test_name, test_function):
        """Executar um teste individual"""
        self.test_count += 1
        print(f"Teste {self.test_count}: {test_name}")
        
        try:
            start_time = time.time()
            success, message = test_function()
            end_time = time.time()
            
            duration = round((end_time - start_time) * 1000, 2)
            
            if success:
                print(f"  ✅ PASSOU - {message} ({duration}ms)")
                self.passed_count += 1
                status = "PASSOU"
            else:
                print(f"  ❌ FALHOU - {message} ({duration}ms)")
                self.failed_count += 1
                status = "FALHOU"
            
            # Adicionar resultado
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "status": status,
                "message": message,
                "duration_ms": duration
            })
            
        except Exception as e:
            print(f"  💥 ERRO - Exceção: {str(e)}")
            self.failed_count += 1
            
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "status": "ERRO",
                "message": f"Exceção: {str(e)}",
                "duration_ms": 0
            })
    
    def generate_report(self):
        """Gerar relatório final"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL - FASE 3")
        print("=" * 60)
        
        # Estatísticas
        total_tests = self.test_count
        passed = self.passed_count
        failed = self.failed_count
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total de Testes: {total_tests}")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")
        
        # Resumo
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "success_rate": round(success_rate, 1)
        }
        
        # Salvar relatório
        report_file = f"relatorio_fase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Relatório salvo em: {report_file}")
        
        # Status final
        if success_rate >= 90:
            print("\n🎉 EXCELENTE! Fase 3 implementada com sucesso!")
            return True
        elif success_rate >= 70:
            print("\n👍 BOM! Fase 3 implementada com algumas melhorias necessárias.")
            return False
        else:
            print("\n⚠️ ATENÇÃO! Fase 3 precisa de correções significativas.")
            return False

def main():
    """Função principal"""
    print("🧪 TESTE AUTOMATIZADO - FASE 3: MELHORIAS")
    print("AEON CHESS - Validação de Performance e UX/UI")
    print("=" * 60)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        print("✅ Servidor local detectado e funcionando")
    except:
        print("⚠️ Servidor local não detectado. Certifique-se de que está rodando na porta 8000")
        print("   Execute: python3 -m http.server 8000")
        return False
    
    # Executar testes
    tester = Fase3Tester()
    success = tester.run_all_tests()
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Testes interrompidos pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro fatal: {str(e)}")
        sys.exit(1)
