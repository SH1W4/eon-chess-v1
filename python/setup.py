#!/usr/bin/env python3
"""
🚀 Setup Script - Motor Python de Efeitos Visuais para Xadrez
Script de instalação e configuração automática

@author AEON CHESS Team
@version 1.0.0
@date Janeiro 2025
"""

import subprocess
import sys
import os
from pathlib import Path
import platform

def check_python_version():
    """Verificar versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_requirements():
    """Instalar dependências Python"""
    print("📦 Instalando dependências...")
    
    try:
        # Atualizar pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar dependências
        requirements_file = Path(__file__).parent / "requirements.txt"
        if requirements_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                          check=True, capture_output=True)
            print("✅ Dependências instaladas com sucesso!")
        else:
            print("⚠️ Arquivo requirements.txt não encontrado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    
    return True

def create_directories():
    """Criar diretórios necessários"""
    print("📁 Criando diretórios...")
    
    directories = [
        "output",
        "output/effects",
        "output/frames",
        "logs",
        "models",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def test_imports():
    """Testar importações das bibliotecas"""
    print("🧪 Testando importações...")
    
    test_imports = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("torch", "PyTorch"),
        ("chess", "Python-Chess"),
        ("PIL", "Pillow"),
        ("matplotlib", "Matplotlib"),
        ("sklearn", "Scikit-learn")
    ]
    
    all_good = True
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            all_good = False
    
    return all_good

def test_chess_engine():
    """Testar motor de xadrez"""
    print("♟️ Testando motor de xadrez...")
    
    try:
        import chess
        board = chess.Board()
        print(f"   ✅ Tabuleiro criado: {board.fen()}")
        
        # Testar movimento
        move = chess.Move.from_uci("e2e4")
        board.push(move)
        print(f"   ✅ Movimento executado: {board.fen()}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no motor de xadrez: {e}")
        return False

def test_opencv():
    """Testar OpenCV"""
    print("👁️ Testando OpenCV...")
    
    try:
        import cv2
        import numpy as np
        
        # Criar imagem de teste
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(img, (10, 10), (90, 90), (0, 255, 0), 2)
        
        # Salvar imagem
        output_path = "output/test_opencv.png"
        cv2.imwrite(output_path, img)
        
        if Path(output_path).exists():
            print(f"   ✅ Imagem de teste criada: {output_path}")
            return True
        else:
            print("   ❌ Falha ao criar imagem de teste")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no OpenCV: {e}")
        return False

def test_pytorch():
    """Testar PyTorch"""
    print("🔥 Testando PyTorch...")
    
    try:
        import torch
        
        # Testar GPU
        if torch.cuda.is_available():
            print(f"   ✅ GPU disponível: {torch.cuda.get_device_name(0)}")
            device = torch.device("cuda")
        else:
            print("   ℹ️ GPU não disponível, usando CPU")
            device = torch.device("cpu")
        
        # Testar tensor básico
        x = torch.randn(3, 3).to(device)
        y = torch.randn(3, 3).to(device)
        z = torch.mm(x, y)
        
        print(f"   ✅ Operação de tensor executada: {z.shape}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no PyTorch: {e}")
        return False

def run_basic_test():
    """Executar teste básico do motor"""
    print("🎯 Executando teste básico...")
    
    try:
        # Importar nosso motor
        sys.path.append(str(Path(__file__).parent))
        from chess_visual_effects_engine import ChessEffectsEngine
        
        # Criar instância
        engine = ChessEffectsEngine()
        print("   ✅ Motor de efeitos criado")
        
        # Testar análise de posição
        test_fen = "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR w KQkq - 0 1"
        patterns = engine.analyze_position(test_fen)
        
        print(f"   ✅ Análise executada: {len(patterns)} padrões encontrados")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste básico: {e}")
        return False

def create_startup_script():
    """Criar script de inicialização"""
    print("🚀 Criando script de inicialização...")
    
    if platform.system() == "Windows":
        script_content = """@echo off
echo Iniciando Chess Effects API...
cd /d "%~dp0"
python chess_effects_api.py
pause
"""
        script_name = "start_api.bat"
    else:
        script_content = """#!/bin/bash
echo "🎯 Iniciando Chess Effects API..."
cd "$(dirname "$0")"
python3 chess_effects_api.py
"""
        script_name = "start_api.sh"
        
        # Tornar executável
        os.chmod(script_name, 0o755)
    
    with open(script_name, "w") as f:
        f.write(script_content)
    
    print(f"   ✅ Script criado: {script_name}")
    return True

def main():
    """Função principal de setup"""
    print("🎯 Chess Visual Effects Engine - Setup")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependências
    if not install_requirements():
        print("❌ Falha na instalação das dependências")
        sys.exit(1)
    
    # Criar diretórios
    if not create_directories():
        print("❌ Falha na criação dos diretórios")
        sys.exit(1)
    
    # Testar importações
    if not test_imports():
        print("❌ Falha nos testes de importação")
        sys.exit(1)
    
    # Testar componentes
    if not test_chess_engine():
        print("❌ Falha no teste do motor de xadrez")
        sys.exit(1)
    
    if not test_opencv():
        print("❌ Falha no teste do OpenCV")
        sys.exit(1)
    
    if not test_pytorch():
        print("❌ Falha no teste do PyTorch")
        sys.exit(1)
    
    # Teste básico do motor
    if not run_basic_test():
        print("❌ Falha no teste básico")
        sys.exit(1)
    
    # Criar script de inicialização
    create_startup_script()
    
    print("\n" + "=" * 50)
    print("🎉 Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute o script de inicialização:")
    if platform.system() == "Windows":
        print("   start_api.bat")
    else:
        print("   ./start_api.sh")
    
    print("2. A API estará disponível em: http://localhost:5000")
    print("3. Teste os endpoints:")
    print("   - GET  /health")
    print("   - GET  /demo/position")
    print("   - POST /analyze")
    print("\n🔗 Documentação completa disponível nos comentários dos arquivos")
    print("🎯 Para integração com o frontend, use a API REST")

if __name__ == "__main__":
    main()
