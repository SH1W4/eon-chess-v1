#!/usr/bin/env python3
"""Script de instalação para integração simbiótica ARQUIMAX-NEXUS"""
import os
import sys
from pathlib import Path
import subprocess
import json

def check_dependencies():
    """Verifica dependências necessárias"""
    dependencies = ["python3", "pip", "git"]
    missing = []
    
    for dep in dependencies:
        try:
            subprocess.run([dep, "--version"], capture_output=True)
        except FileNotFoundError:
            missing.append(dep)
    
    return missing

def install_python_packages():
    """Instala pacotes Python necessários"""
    packages = [
        "click",
        "pyyaml",
        "rich",
        "aiohttp",
        "asyncio"
    ]
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", *packages])
        return True
    except Exception as e:
        print(f"Erro ao instalar pacotes Python: {str(e)}")
        return False

def setup_symbiotic_environment():
    """Configura ambiente simbiótico"""
    current_dir = Path(__file__).parent
    
    # Cria diretório de configuração
    config_dir = Path.home() / ".symbiotic"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Cria configuração inicial
    config = {
        "version": "1.0.0",
        "install_path": str(current_dir),
        "warp_integration": True,
        "auto_update": True
    }
    
    with open(config_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    return True

def setup_cli():
    """Configura CLI do sistema"""
    try:
        # Cria link simbólico para CLI
        cli_path = Path.home() / ".local" / "bin" / "aeon"
        cli_source = Path(__file__).parent / "src" / "cli" / "symbiotic_init.py"
        
        if cli_path.exists():
            cli_path.unlink()
        
        cli_path.parent.mkdir(parents=True, exist_ok=True)
        cli_path.symlink_to(cli_source)
        
        # Torna executável
        os.chmod(cli_path, 0o755)
        
        return True
    except Exception as e:
        print(f"Erro ao configurar CLI: {str(e)}")
        return False

def main():
    """Função principal de instalação"""
    print("=== Instalação ARQUIMAX-NEXUS Simbiótico ===\n")
    
    # Verifica dependências
    print("Verificando dependências...")
    missing = check_dependencies()
    if missing:
        print(f"Dependências faltando: {', '.join(missing)}")
        print("Por favor, instale as dependências e tente novamente")
        return False
    print("✓ Dependências OK")
    
    # Instala pacotes Python
    print("\nInstalando pacotes Python...")
    if not install_python_packages():
        print("× Erro ao instalar pacotes Python")
        return False
    print("✓ Pacotes instalados")
    
    # Configura ambiente
    print("\nConfigurando ambiente simbiótico...")
    if not setup_symbiotic_environment():
        print("× Erro ao configurar ambiente")
        return False
    print("✓ Ambiente configurado")
    
    # Configura CLI
    print("\nConfigurando CLI...")
    if not setup_cli():
        print("× Erro ao configurar CLI")
        return False
    print("✓ CLI configurada")
    
    # Configura integração com Warp
    print("\nConfigurando integração com Warp...")
    from src.cli.warp_integration import setup_warp_integration
    if not setup_warp_integration():
        print("× Erro ao configurar integração com Warp")
        return False
    print("✓ Integração com Warp configurada")
    
    print("\n=== Instalação concluída com sucesso! ===")
    print("\nPara começar, use:")
    print("  aeon symbiotic init --project-path=/seu/projeto")
    print("\nPara mais informações:")
    print("  aeon symbiotic --help")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
