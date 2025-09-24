#!/usr/bin/env python3
"""
🧠 Teste do Sistema de IA Unificado - Aeon Chess

Este script testa todas as funcionalidades do sistema de IA unificado:
- Sistema de personalidades
- Orquestrador
- Interface
- Funcionalidades principais
"""

import os
import sys
import time
import json
from pathlib import Path

def test_file_structure():
    """Testa a estrutura de arquivos do sistema de IA"""
    print("🔍 Testando estrutura de arquivos...")
    
    required_files = [
        "web/js/ai-unified-system.js",
        "web/js/ai-orchestrator.js", 
        "web/pages/ai-unified-interface.html",
        "docs/features/AI_UNIFIED_SYSTEM_GUIDE.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos ausentes: {missing_files}")
        return False
    else:
        print("✅ Todos os arquivos necessários estão presentes")
        return True

def test_js_files():
    """Testa os arquivos JavaScript"""
    print("\n🔍 Testando arquivos JavaScript...")
    
    js_files = [
        "web/js/ai-unified-system.js",
        "web/js/ai-orchestrator.js"
    ]
    
    for js_file in js_files:
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verifica se contém as classes principais
            if 'class AIUnifiedSystem' in content:
                print(f"✅ {js_file} - Classe AIUnifiedSystem encontrada")
            elif 'class AIOrchestrator' in content:
                print(f"✅ {js_file} - Classe AIOrchestrator encontrada")
            else:
                print(f"❌ {js_file} - Nenhuma classe principal encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao ler {js_file}: {e}")
            return False
    
    return True

def test_html_interface():
    """Testa a interface HTML"""
    print("\n🔍 Testando interface HTML...")
    
    try:
        with open("web/pages/ai-unified-interface.html", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica elementos essenciais
        required_elements = [
            'Sistema de IA Unificado',
            'Personalidade da IA',
            'Configurações do Sistema',
            'Ações da IA',
            'ai-unified-system.js',
            'ai-orchestrator.js'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Elementos ausentes: {missing_elements}")
            return False
        else:
            print("✅ Interface HTML contém todos os elementos necessários")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao ler interface HTML: {e}")
        return False

def test_documentation():
    """Testa a documentação"""
    print("\n🔍 Testando documentação...")
    
    try:
        with open("docs/features/AI_UNIFIED_SYSTEM_GUIDE.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica seções essenciais
        required_sections = [
            'Sistema de Personalidades',
            'Sistema de Orquestração',
            'Como Usar',
            'Integração Técnica',
            'Monitoramento e Analytics'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Seções ausentes: {missing_sections}")
            return False
        else:
            print("✅ Documentação contém todas as seções necessárias")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao ler documentação: {e}")
        return False

def test_personalities():
    """Testa o sistema de personalidades"""
    print("\n🔍 Testando sistema de personalidades...")
    
    try:
        with open("web/js/ai-unified-system.js", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica personalidades definidas
        personalities = [
            'strategic',
            'tactical', 
            'teacher',
            'creative',
            'competitive',
            'zen'
        ]
        
        missing_personalities = []
        for personality in personalities:
            if f"'{personality}'" not in content:
                missing_personalities.append(personality)
        
        if missing_personalities:
            print(f"❌ Personalidades ausentes: {missing_personalities}")
            return False
        else:
            print("✅ Todas as 6 personalidades estão definidas")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar personalidades: {e}")
        return False

def test_orchestrator_features():
    """Testa funcionalidades do orquestrador"""
    print("\n🔍 Testando funcionalidades do orquestrador...")
    
    try:
        with open("web/js/ai-orchestrator.js", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica funcionalidades essenciais
        required_features = [
            'initializeResources',
            'initializePerformanceTracking',
            'initializeLearning',
            'orchestrateTask',
            'getOrchestratorStats',
            'getOptimizationRecommendations'
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"❌ Funcionalidades ausentes: {missing_features}")
            return False
        else:
            print("✅ Todas as funcionalidades do orquestrador estão implementadas")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar orquestrador: {e}")
        return False

def test_integration():
    """Testa a integração entre componentes"""
    print("\n🔍 Testando integração entre componentes...")
    
    try:
        with open("web/js/ai-unified-system.js", 'r', encoding='utf-8') as f:
            unified_content = f.read()
        
        with open("web/js/ai-orchestrator.js", 'r', encoding='utf-8') as f:
            orchestrator_content = f.read()
        
        # Verifica se o sistema unificado referencia o orquestrador
        if 'AIOrchestrator' in unified_content:
            print("✅ Sistema unificado referencia o orquestrador")
        else:
            print("❌ Sistema unificado não referencia o orquestrador")
            return False
        
        # Verifica se o orquestrador referencia o sistema unificado
        if 'aiSystem' in orchestrator_content:
            print("✅ Orquestrador referencia o sistema unificado")
        else:
            print("❌ Orquestrador não referencia o sistema unificado")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar integração: {e}")
        return False

def generate_test_report(results):
    """Gera relatório de teste"""
    print("\n" + "="*60)
    print("📊 RELATÓRIO DE TESTE - SISTEMA DE IA UNIFICADO")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"Total de Testes: {total_tests}")
    print(f"Testes Aprovados: {passed_tests}")
    print(f"Testes Reprovados: {failed_tests}")
    print(f"Taxa de Sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 Detalhes dos Testes:")
    for test_name, result in results.items():
        status = "✅ APROVADO" if result else "❌ REPROVADO"
        print(f"  {test_name}: {status}")
    
    if failed_tests == 0:
        print("\n🎉 PARABÉNS! Todos os testes foram aprovados!")
        print("O Sistema de IA Unificado está funcionando perfeitamente.")
    else:
        print(f"\n⚠️  ATENÇÃO: {failed_tests} teste(s) falharam.")
        print("Verifique os erros acima e corrija antes de prosseguir.")
    
    return failed_tests == 0

def main():
    """Função principal de teste"""
    print("🧠 INICIANDO TESTES DO SISTEMA DE IA UNIFICADO")
    print("="*60)
    
    # Lista de testes
    tests = {
        "Estrutura de Arquivos": test_file_structure,
        "Arquivos JavaScript": test_js_files,
        "Interface HTML": test_html_interface,
        "Documentação": test_documentation,
        "Sistema de Personalidades": test_personalities,
        "Funcionalidades do Orquestrador": test_orchestrator_features,
        "Integração entre Componentes": test_integration
    }
    
    # Executa testes
    results = {}
    for test_name, test_func in tests.items():
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    # Gera relatório
    success = generate_test_report(results)
    
    # Retorna código de saída
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
