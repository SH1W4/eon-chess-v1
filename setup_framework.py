"""Script para configurar o Symbiotic Framework"""
import os
import shutil
from pathlib import Path

def setup_framework():
    """Configura o ambiente do Symbiotic Framework"""
    
    # Caminhos
    source_dir = Path("/Users/jx/WORKSPACE/PROJECTS/CHESS/framework")
    target_dir = Path("/Users/jx/WORKSPACE/FRAMEWORKS/SYMBIOTIC")
    
    try:
        # Cria diretório de frameworks se não existir
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Copia arquivos
        for item in source_dir.glob("*"):
            if item.is_file():
                shutil.copy2(item, target_dir)
            elif item.is_dir():
                shutil.copytree(item, target_dir / item.name, dirs_exist_ok=True)
        
        # Cria estrutura adicional
        (target_dir / "src").mkdir(exist_ok=True)
        (target_dir / "tests").mkdir(exist_ok=True)
        (target_dir / "examples").mkdir(exist_ok=True)
        (target_dir / "docs").mkdir(exist_ok=True)
        
        # Cria arquivo de configuração do ambiente
        with open(target_dir / ".env", "w") as f:
            f.write(f"""SYMBIOTIC_HOME={target_dir}
PYTHONPATH=$PYTHONPATH:{target_dir}/src
""")
        
        # Cria arquivo de ativação
        with open(target_dir / "activate", "w") as f:
            f.write("""#!/bin/bash
export SYMBIOTIC_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PYTHONPATH:$SYMBIOTIC_HOME/src"
echo "Symbiotic Framework ambiente ativado em $SYMBIOTIC_HOME"
""")
        
        # Torna arquivo de ativação executável
        os.chmod(target_dir / "activate", 0o755)
        
        print(f"""
=== Symbiotic Framework Setup ===

Framework instalado em: {target_dir}

Para ativar o ambiente:
source {target_dir}/activate

Estrutura criada:
- src/      (código-fonte)
- tests/    (testes)
- examples/ (exemplos)
- docs/     (documentação)

Arquivos de configuração:
- .env
- activate

Framework pronto para uso!
""")
        
        return True
        
    except Exception as e:
        print(f"Erro durante setup: {str(e)}")
        return False

if __name__ == "__main__":
    setup_framework()
