#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 TESTE DO SISTEMA DE ANTAGONISTAS DE IA - Aeon Chess
======================================================

Este script testa o sistema completo de antagonistas de IA:
- Verificação de arquivos
- Teste de funcionalidades
- Validação de integração
- Verificação de interface

@version 1.0.0
@author Aeon Chess Team
"""

import os
import sys
import json
import time
from datetime import datetime

def print_header():
    """Imprime o cabeçalho do teste"""
    print("🧠 INICIANDO TESTES DO SISTEMA DE ANTAGONISTAS DE IA")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sistema: {sys.platform}")
    print("=" * 60)

def test_file_structure():
    """Testa a estrutura de arquivos do sistema de antagonistas"""
    print("🔍 Testando estrutura de arquivos...")
    
    required_files = [
        'web/js/ai-antagonists-system.js',
        'web/pages/ai-antagonists-interface.html'
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
    """Testa os arquivos JavaScript do sistema de antagonistas"""
    print("🔍 Testando arquivos JavaScript...")
    
    # Testa ai-antagonists-system.js
    try:
        with open('web/js/ai-antagonists-system.js', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'class AIAntagonistsSystem' in content:
            print("✅ web/js/ai-antagonists-system.js - Classe AIAntagonistsSystem encontrada")
        else:
            print("❌ web/js/ai-antagonists-system.js - Classe AIAntagonistsSystem não encontrada")
            return False
            
        # Verifica se tem antagonistas definidos
        if 'initializeAntagonists' in content:
            print("✅ web/js/ai-antagonists-system.js - Método initializeAntagonists encontrado")
        else:
            print("❌ web/js/ai-antagonists-system.js - Método initializeAntagonists não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler web/js/ai-antagonists-system.js: {e}")
        return False
    
    return True

def test_html_interface():
    """Testa a interface HTML do sistema de antagonistas"""
    print("🔍 Testando interface HTML...")
    
    try:
        with open('web/pages/ai-antagonists-interface.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica elementos essenciais
        required_elements = [
            'antagonist-indicator',
            'antagonist-description',
            'antagonist-grid',
            'difficulty-selector',
            'antagonist-output'
        ]
        
        missing_elements = []
        for element in required_elements:
            if f'id="{element}"' not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Elementos HTML ausentes: {missing_elements}")
            return False
        
        # Verifica inclusão de scripts
        if 'ai-antagonists-system.js' in content:
            print("✅ Interface HTML inclui script do sistema de antagonistas")
        else:
            print("❌ Interface HTML não inclui script do sistema de antagonistas")
            return False
        
        # Verifica antagonistas na interface
        antagonist_names = [
            'O Mestre Implacável',
            'O Psicólogo Sombrio',
            'O Artista Destrutivo',
            'O Calculador Máquina',
            'O Predador Noturno',
            'O Imperador Tirano',
            'O Ilusionista Mestre',
            'O Berserker Furioso'
        ]
        
        missing_antagonists = []
        for name in antagonist_names:
            if name not in content:
                missing_antagonists.append(name)
        
        if missing_antagonists:
            print(f"❌ Antagonistas ausentes na interface: {missing_antagonists}")
            return False
        
        print("✅ Interface HTML contém todos os elementos necessários")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler interface HTML: {e}")
        return False

def test_antagonists_definition():
    """Testa a definição dos antagonistas no JavaScript"""
    print("🔍 Testando definição dos antagonistas...")
    
    try:
        with open('web/js/ai-antagonists-system.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Lista de antagonistas esperados
        expected_antagonists = [
            'implacable_master',
            'dark_psychologist', 
            'destructive_artist',
            'machine_calculator',
            'night_predator',
            'tyrant_emperor',
            'master_illusionist',
            'furious_berserker'
        ]
        
        missing_antagonists = []
        for antagonist in expected_antagonists:
            if f"'{antagonist}'" not in content and f'"{antagonist}"' not in content:
                missing_antagonists.append(antagonist)
        
        if missing_antagonists:
            print(f"❌ Antagonistas não definidos: {missing_antagonists}")
            return False
        
        print(f"✅ Todos os {len(expected_antagonists)} antagonistas estão definidos")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar definição dos antagonistas: {e}")
        return False

def test_antagonist_features():
    """Testa as funcionalidades dos antagonistas"""
    print("🔍 Testando funcionalidades dos antagonistas...")
    
    try:
        with open('web/js/ai-antagonists-system.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica métodos essenciais
        required_methods = [
            'analyzePosition',
            'changeAntagonist',
            'setDifficulty',
            'getAntagonistStats',
            'getAntagonists'
        ]
        
        missing_methods = []
        for method in required_methods:
            if method not in content:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Métodos ausentes: {missing_methods}")
            return False
        
        # Verifica propriedades dos antagonistas
        required_properties = [
            'name',
            'description',
            'style',
            'difficulty',
            'color',
            'strengths',
            'weaknesses',
            'preferredOpenings',
            'motivationalQuotes',
            'behavior'
        ]
        
        # Verifica se pelo menos um antagonista tem todas as propriedades
        for prop in required_properties:
            if prop not in content:
                print(f"❌ Propriedade ausente: {prop}")
                return False
        
        print("✅ Todas as funcionalidades dos antagonistas estão implementadas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar funcionalidades: {e}")
        return False

def test_interface_functionality():
    """Testa a funcionalidade da interface"""
    print("🔍 Testando funcionalidade da interface...")
    
    try:
        with open('web/pages/ai-antagonists-interface.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica métodos da interface
        required_interface_methods = [
            'selectAntagonist',
            'selectDifficulty',
            'analyzePosition',
            'showStats',
            'updateUI'
        ]
        
        missing_methods = []
        for method in required_interface_methods:
            if method not in content:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"❌ Métodos da interface ausentes: {missing_methods}")
            return False
        
        # Verifica event listeners
        if 'addEventListener' in content:
            print("✅ Event listeners estão implementados")
        else:
            print("❌ Event listeners não encontrados")
            return False
        
        print("✅ Interface tem todas as funcionalidades necessárias")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar funcionalidade da interface: {e}")
        return False

def test_integration():
    """Testa a integração entre componentes"""
    print("🔍 Testando integração entre componentes...")
    
    try:
        with open('web/js/ai-antagonists-system.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        with open('web/pages/ai-antagonists-interface.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verifica se a interface referencia o sistema
        if 'antagonistSystem' in html_content:
            print("✅ Interface referencia o sistema de antagonistas")
        else:
            print("❌ Interface não referencia o sistema de antagonistas")
            return False
        
        # Verifica se o sistema tem métodos de UI
        if 'updateUI' in js_content:
            print("✅ Sistema tem métodos de atualização de UI")
        else:
            print("❌ Sistema não tem métodos de atualização de UI")
            return False
        
        print("✅ Integração entre componentes está funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar integração: {e}")
        return False

def generate_test_report(results):
    """Gera relatório de teste"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE TESTE - SISTEMA DE ANTAGONISTAS")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total de Testes: {total_tests}")
    print(f"Testes Aprovados: {passed_tests}")
    print(f"Testes Reprovados: {failed_tests}")
    print(f"Taxa de Sucesso: {success_rate:.1f}%")
    print()
    
    print("📋 Detalhes dos Testes:")
    for test_name, result in results.items():
        status = "✅ APROVADO" if result else "❌ REPROVADO"
        print(f"  {test_name}: {status}")
    
    print()
    if success_rate == 100:
        print("🎉 PARABÉNS! Todos os testes foram aprovados!")
        print("O Sistema de Antagonistas está funcionando perfeitamente.")
    elif success_rate >= 80:
        print("👍 BOM TRABALHO! A maioria dos testes foi aprovada.")
        print("Alguns ajustes menores podem ser necessários.")
    else:
        print("⚠️ ATENÇÃO! Vários testes falharam.")
        print("Revisão e correções são necessárias.")
    
    print("=" * 60)

def main():
    """Função principal do teste"""
    print_header()
    
    # Executa todos os testes
    test_results = {
        'Estrutura de Arquivos': test_file_structure(),
        'Arquivos JavaScript': test_js_files(),
        'Interface HTML': test_html_interface(),
        'Definição dos Antagonistas': test_antagonists_definition(),
        'Funcionalidades dos Antagonistas': test_antagonist_features(),
        'Funcionalidade da Interface': test_interface_functionality(),
        'Integração entre Componentes': test_integration()
    }
    
    # Gera relatório
    generate_test_report(test_results)
    
    # Retorna código de saída baseado no sucesso
    success_rate = (sum(1 for result in test_results.values() if result) / len(test_results)) * 100
    return 0 if success_rate == 100 else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
