#!/usr/bin/env python3
"""
AEON Chess - Script de Preparação para Acesso GPT Codex
Data: 2025-08-12
Versão: 1.0.0

Este script prepara o repositório para dar acesso otimizado ao GPT Codex,
configurando metadados, documentação e estrutura para análise eficiente.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class CodexAccessPreparation:
    """Preparação do repositório para acesso do GPT Codex"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.github_repo = "NEO-SH1W4/aeon-chess"
        self.setup_time = datetime.now().isoformat()
        
    def run_command(self, command: str) -> tuple[str, int]:
        """Executa comando e retorna output e exit code"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip(), result.returncode
        except Exception as e:
            return f"Erro: {e}", 1
    
    def check_git_status(self) -> Dict[str, Any]:
        """Verifica status do Git"""
        print("🔍 Verificando status do Git...")
        
        status = {}
        
        # Status básico
        output, code = self.run_command("git status --porcelain")
        status['clean_working_tree'] = len(output) == 0
        status['uncommitted_files'] = output.split('\n') if output else []
        
        # Branch atual
        output, code = self.run_command("git branch --show-current")
        status['current_branch'] = output
        
        # Commits à frente
        output, code = self.run_command("git rev-list --count HEAD ^origin/main")
        status['commits_ahead'] = int(output) if output.isdigit() else 0
        
        # Remote
        output, code = self.run_command("git remote get-url origin")
        status['remote_url'] = output
        
        return status
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analisa estrutura do projeto"""
        print("📁 Analisando estrutura do projeto...")
        
        structure = {
            'total_files': 0,
            'python_files': 0,
            'typescript_files': 0,
            'test_files': 0,
            'doc_files': 0,
            'config_files': 0,
            'directories': []
        }
        
        # Conta arquivos por tipo
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                structure['total_files'] += 1
                
                if file_path.suffix == '.py':
                    structure['python_files'] += 1
                    if 'test' in str(file_path):
                        structure['test_files'] += 1
                        
                elif file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                    structure['typescript_files'] += 1
                    
                elif file_path.suffix in ['.md', '.rst', '.txt']:
                    structure['doc_files'] += 1
                    
                elif file_path.suffix in ['.json', '.yaml', '.yml', '.toml', '.cfg']:
                    structure['config_files'] += 1
            
            elif file_path.is_dir() and file_path.parent == self.project_root:
                structure['directories'].append(file_path.name)
        
        return structure
    
    def generate_codex_summary(self) -> Dict[str, Any]:
        """Gera resumo para o GPT Codex"""
        print("📊 Gerando resumo para GPT Codex...")
        
        git_status = self.check_git_status()
        project_structure = self.analyze_project_structure()
        
        summary = {
            'project_info': {
                'name': 'AEON Chess',
                'version': 'v0.3.1-alpha-ready',
                'repository': f"https://github.com/{self.github_repo}",
                'description': 'Motor de xadrez avançado com IA adaptativa e elementos culturais',
                'setup_time': self.setup_time
            },
            'git_status': git_status,
            'project_structure': project_structure,
            'key_features': [
                'IA Adaptativa com aprendizado evolutivo',
                'Sistema cultural dinâmico (Samurai, Viking, Persian)',
                'Simulações quânticas para avaliação de posições',
                'Interface web Next.js responsiva',
                'API REST FastAPI documentada',
                'Automação ARKITECT/TaskMesh/NEXUS',
                'Pipeline CI/CD completo',
                'Deploy Docker otimizado'
            ],
            'priority_files': [
                'src/core/board/board.py',
                'src/ai/adaptive_ai.py', 
                'src/cultural/cultures.py',
                'src/api/main.py',
                'tests/',
                'README_CODEX.md'
            ],
            'automation_scripts': [
                'scripts/arkitect/arkitect_main.py',
                'scripts/taskmesh/taskmesh_core.py',
                'scripts/nexus/nexus_connector.py'
            ],
            'current_metrics': {
                'code_quality': '93.5/100',
                'test_coverage': '77%',
                'total_tests': 243,
                'progress': '98%',
                'technical_debt': '4.2%'
            },
            'immediate_priorities': [
                'Correção dos 23% de testes falhando',
                'Polimento da interface web',
                'Documentação API completa',
                'Preparação para deploy alpha'
            ]
        }
        
        return summary
    
    def create_codex_workspace_config(self):
        """Cria configuração do workspace para Codex"""
        print("⚙️ Criando configuração do workspace...")
        
        config = {
            "name": "AEON Chess",
            "type": "python",
            "rootPath": ".",
            "pythonPath": "venv/bin/python",
            "testFramework": "pytest",
            "linter": "flake8",
            "formatter": "black",
            "directories": {
                "source": "src/",
                "tests": "tests/",
                "docs": "docs/",
                "scripts": "scripts/",
                "config": "config/"
            },
            "entryPoints": {
                "main": "src/api/main.py",
                "ai": "src/ai/adaptive_ai.py",
                "board": "src/core/board/board.py",
                "cultural": "src/cultural/cultures.py"
            },
            "testCommands": {
                "all": "pytest tests/",
                "unit": "pytest tests/unit/",
                "integration": "pytest tests/integration/",
                "ai": "pytest tests/ai/",
                "cultural": "pytest tests/cultural/"
            },
            "buildCommands": {
                "backend": "pip install -r requirements.txt",
                "frontend": "npm install && npm run build",
                "docker": "docker-compose -f docker-compose.production.yml build"
            },
            "runCommands": {
                "api": "uvicorn src.api.main:app --reload",
                "frontend": "npm run dev",
                "tests": "pytest",
                "arkitect": "python3 scripts/arkitect/arkitect_main.py"
            }
        }
        
        config_path = self.project_root / '.vscode' / 'codex_workspace.json'
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config_path
    
    def update_repository_topics(self):
        """Atualiza topics do repositório GitHub"""
        print("🏷️ Atualizando topics do repositório...")
        
        topics = [
            "chess-engine",
            "artificial-intelligence", 
            "adaptive-ai",
            "cultural-chess",
            "quantum-simulation",
            "python",
            "typescript",
            "fastapi",
            "nextjs",
            "machine-learning",
            "game-development",
            "chess-ai",
            "arkitect",
            "taskmesh",
            "nexus"
        ]
        
        # Comando GitHub CLI para atualizar topics
        topics_str = " ".join(topics)
        command = f"gh repo edit {self.github_repo} --add-topic {topics_str}"
        
        print(f"📝 Comando para atualizar topics:")
        print(f"   {command}")
        print(f"   (Execute manualmente se tiver GitHub CLI configurado)")
        
        return topics
    
    def prepare_for_push(self):
        """Prepara arquivos para push no GitHub"""
        print("🚀 Preparando para push no GitHub...")
        
        # Adiciona novos arquivos
        output, code = self.run_command("git add .")
        
        if code == 0:
            print("✅ Arquivos adicionados ao staging")
        else:
            print(f"❌ Erro ao adicionar arquivos: {output}")
            return False
        
        # Verifica se há algo para commit
        output, code = self.run_command("git status --porcelain")
        
        if not output:
            print("ℹ️ Nenhuma mudança para commit")
            return True
        
        # Cria commit
        commit_msg = "feat: Configuração para acesso GPT Codex\n\n- Otimização .gitattributes para análise IA\n- README_CODEX.md com guia completo\n- Configuração de acesso e permissões\n- Workspace config para desenvolvimento\n- Topics e metadados atualizados"
        
        output, code = self.run_command(f'git commit -m "{commit_msg}"')
        
        if code == 0:
            print("✅ Commit criado com sucesso")
            return True
        else:
            print(f"❌ Erro ao criar commit: {output}")
            return False
    
    def generate_access_instructions(self) -> str:
        """Gera instruções de acesso para o usuário"""
        
        instructions = f"""
🎯 INSTRUÇÕES PARA DAR ACESSO AO GPT CODEX

## 1. Push das Configurações
```bash
git push origin main
```

## 2. Configurar Permissões no GitHub
1. Acesse: https://github.com/{self.github_repo}/settings
2. Em "Collaborators and teams" → "Manage access"
3. Clique "Add people" ou "Add teams"
4. Digite o identificador do GPT Codex
5. Selecione nível de permissão:
   - **Read**: Para análise apenas
   - **Write**: Para contribuições diretas
   - **Admin**: Para configuração avançada

## 3. Configurar Topics (Opcional)
Execute se tiver GitHub CLI:
```bash
gh repo edit {self.github_repo} --add-topic chess-engine,artificial-intelligence,adaptive-ai,cultural-chess,quantum-simulation,python,typescript,fastapi,nextjs
```

## 4. Ativar GitHub Features
1. **Code scanning**: Settings → Security → Code scanning
2. **Dependency graph**: Settings → Security → Dependency graph  
3. **Actions**: Settings → Actions → General (ativar workflows)

## 5. Branch Protection (Recomendado)
1. Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Ativar:
   - [x] Require pull request reviews
   - [x] Require status checks
   - [x] Require conversation resolution

## 📋 Checklist de Verificação

### ✅ Arquivos Preparados
- [x] .gitattributes otimizado
- [x] README_CODEX.md criado
- [x] .github/CODEX_ACCESS.md documentado
- [x] Workspace config gerado

### 🔄 Ações Manuais Necessárias
- [ ] Executar `git push origin main`
- [ ] Configurar permissões no GitHub
- [ ] Ativar features de segurança
- [ ] Configurar branch protection

## 🎮 Acesso Direto
**URL do Repositório**: https://github.com/{self.github_repo}
**Branch Principal**: main
**Documentação Codex**: README_CODEX.md

## 📞 Próximos Passos
1. Execute o push das configurações
2. Configure as permissões no GitHub
3. Compartilhe a URL do repositório com o GPT Codex
4. O Codex terá acesso completo para análise e contribuição

---
Configuração gerada em: {self.setup_time}
"""
        
        return instructions.strip()
    
    def execute_preparation(self):
        """Executa preparação completa"""
        print("🚀 AEON Chess - Preparação para Acesso GPT Codex")
        print("=" * 60)
        
        try:
            # 1. Análise inicial
            summary = self.generate_codex_summary()
            print(f"✅ Projeto analisado: {summary['project_structure']['total_files']} arquivos")
            
            # 2. Cria configuração workspace
            config_path = self.create_codex_workspace_config()
            print(f"✅ Workspace config criado: {config_path}")
            
            # 3. Atualiza topics
            topics = self.update_repository_topics()
            print(f"✅ Topics preparados: {len(topics)} tags")
            
            # 4. Prepara para push
            push_ready = self.prepare_for_push()
            
            if push_ready:
                print("✅ Arquivos preparados para push")
            else:
                print("❌ Erro na preparação para push")
                return False
            
            # 5. Gera instruções
            instructions = self.generate_access_instructions()
            
            # Salva instruções
            instructions_path = self.project_root / 'CODEX_SETUP_INSTRUCTIONS.md'
            with open(instructions_path, 'w', encoding='utf-8') as f:
                f.write(instructions)
            
            print(f"✅ Instruções salvas: {instructions_path}")
            
            # 6. Salva resumo JSON
            summary_path = self.project_root / 'codex_project_summary.json'
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Resumo salvo: {summary_path}")
            
            # 7. Resultado final
            print("\n" + "=" * 60)
            print("🎉 PREPARAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print("\n📋 PRÓXIMAS AÇÕES:")
            print("1. Execute: git push origin main")
            print("2. Configure permissões GitHub")
            print(f"3. Compartilhe: https://github.com/{self.github_repo}")
            print("\n📖 Veja CODEX_SETUP_INSTRUCTIONS.md para detalhes")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante preparação: {e}")
            return False

def main():
    """Função principal"""
    preparator = CodexAccessPreparation()
    success = preparator.execute_preparation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
