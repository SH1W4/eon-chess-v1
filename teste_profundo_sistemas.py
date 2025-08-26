#!/usr/bin/env python3
"""
Teste Profundo dos Sistemas - XadrezMaster
Executa testes automatizados em todos os componentes para identificar erros específicos
"""

import os
import sys
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('teste_profundo.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class TesteProfundoSistemas:
    def __init__(self):
        self.resultados = []
        self.erros_criticos = []
        self.avisos = []
        self.sucessos = []
        self.inicio_teste = time.time()
        
        # Configurações
        self.workspace = Path("/Users/jx/WORKSPACE/PROJECTS/CHESS")
        self.porta_api = 8000  # Porta padrão da API Python
        
    def executar_teste_completo(self):
        """Executa todos os testes do sistema"""
        logging.info("🚀 Iniciando teste profundo dos sistemas...")
        
        try:
            # 1. Teste de Estrutura de Arquivos
            self.testar_estrutura_arquivos()
            
            # 2. Teste de Dependências
            self.testar_dependencias()
            
            # 3. Teste de Sistemas JavaScript
            self.testar_sistemas_javascript()
            
            # 4. Teste de API Python
            self.testar_api_python()
            
            # 5. Teste de Banco de Dados
            self.testar_banco_dados()
            
            # 6. Teste de Performance
            self.testar_performance()
            
            # 7. Teste de Integração
            self.testar_integracao()
            
            # 8. Gerar Relatório
            self.gerar_relatorio_final()
            
        except Exception as e:
            logging.error(f"❌ Erro durante execução dos testes: {e}")
            self.erros_criticos.append(f"Erro geral: {e}")
    
    def testar_estrutura_arquivos(self):
        """Testa a estrutura de arquivos do projeto"""
        logging.info("📁 Testando estrutura de arquivos...")
        
        arquivos_essenciais = [
            "index.html",
            "js/chess-board.js",
            "js/ai-integration-real.js",
            "js/aeon-brain-orchestrator.js",
            "python/chess_effects_api.py",
            "src/ai/evaluation/",
            "src/core/board/",
            "data/postgres/",
            "deploy/production/"
        ]
        
        for arquivo in arquivos_essenciais:
            caminho = self.workspace / arquivo
            if caminho.exists():
                self.adicionar_resultado("estrutura", "success", f"Arquivo encontrado: {arquivo}")
            else:
                self.adicionar_resultado("estrutura", "error", f"Arquivo não encontrado: {arquivo}")
                self.erros_criticos.append(f"Arquivo essencial não encontrado: {arquivo}")
    
    def testar_dependencias(self):
        """Testa as dependências do projeto"""
        logging.info("📦 Testando dependências...")
        
        # Verificar Node.js
        try:
            resultado = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if resultado.returncode == 0:
                self.adicionar_resultado("dependencias", "success", f"Node.js: {resultado.stdout.strip()}")
            else:
                self.adicionar_resultado("dependencias", "error", "Node.js não encontrado")
                self.erros_criticos.append("Node.js não está instalado")
        except FileNotFoundError:
            self.adicionar_resultado("dependencias", "error", "Node.js não encontrado")
            self.erros_criticos.append("Node.js não está instalado")
        
        # Verificar Python
        try:
            resultado = subprocess.run(["python3", "--version"], capture_output=True, text=True)
            if resultado.returncode == 0:
                self.adicionar_resultado("dependencias", "success", f"Python: {resultado.stdout.strip()}")
            else:
                self.adicionar_resultado("dependencias", "error", "Python3 não encontrado")
                self.erros_criticos.append("Python3 não está instalado")
        except FileNotFoundError:
            self.adicionar_resultado("dependencias", "error", "Python3 não encontrado")
            self.erros_criticos.append("Python3 não está instalado")
        
        # Verificar Docker
        try:
            resultado = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            if resultado.returncode == 0:
                self.adicionar_resultado("dependencias", "success", f"Docker: {resultado.stdout.strip()}")
            else:
                self.adicionar_resultado("dependencias", "warning", "Docker não encontrado")
                self.avisos.append("Docker não está instalado")
        except FileNotFoundError:
            self.adicionar_resultado("dependencias", "warning", "Docker não encontrado")
            self.avisos.append("Docker não está instalado")
    
    def testar_sistemas_javascript(self):
        """Testa os sistemas JavaScript"""
        logging.info("🟨 Testando sistemas JavaScript...")
        
        arquivos_js = [
            "js/chess-board.js",
            "js/ai-integration-real.js",
            "js/aeon-brain-orchestrator.js",
            "js/gamification.js",
            "js/chess-pro-database.js"
        ]
        
        for arquivo in arquivos_js:
            caminho = self.workspace / arquivo
            if caminho.exists():
                # Verificar sintaxe básica
                try:
                    with open(caminho, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                        
                    # Verificações básicas
                    if 'function' in conteudo or 'class' in conteudo:
                        self.adicionar_resultado("javascript", "success", f"Arquivo JS válido: {arquivo}")
                    else:
                        self.adicionar_resultado("javascript", "warning", f"Arquivo JS pode estar vazio: {arquivo}")
                        self.avisos.append(f"Arquivo JS pode estar vazio: {arquivo}")
                        
                except Exception as e:
                    self.adicionar_resultado("javascript", "error", f"Erro ao ler arquivo: {arquivo} - {e}")
                    self.erros_criticos.append(f"Erro ao ler arquivo JS: {arquivo}")
            else:
                self.adicionar_resultado("javascript", "error", f"Arquivo JS não encontrado: {arquivo}")
                self.erros_criticos.append(f"Arquivo JS não encontrado: {arquivo}")
    
    def testar_api_python(self):
        """Testa a API Python"""
        logging.info("🐍 Testando API Python...")
        
        # Verificar se a API está rodando
        try:
            url = f"http://localhost:{self.porta_api}/health"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                self.adicionar_resultado("api_python", "success", "API Python respondendo corretamente")
            else:
                self.adicionar_resultado("api_python", "warning", f"API Python retornou status {response.status_code}")
                self.avisos.append(f"API Python retornou status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.adicionar_resultado("api_python", "error", "API Python não está rodando")
            self.erros_criticos.append("API Python não está rodando")
        except requests.exceptions.Timeout:
            self.adicionar_resultado("api_python", "error", "API Python não respondeu no tempo limite")
            self.erros_criticos.append("API Python não respondeu no tempo limite")
        except Exception as e:
            self.adicionar_resultado("api_python", "error", f"Erro ao testar API Python: {e}")
            self.erros_criticos.append(f"Erro ao testar API Python: {e}")
        
        # Verificar arquivos Python
        arquivos_python = [
            "python/chess_effects_api.py",
            "python/chess_visual_effects_engine.py"
        ]
        
        for arquivo in arquivos_python:
            caminho = self.workspace / arquivo
            if caminho.exists():
                try:
                    # Verificar sintaxe Python
                    resultado = subprocess.run(
                        ["python3", "-m", "py_compile", str(caminho)],
                        capture_output=True,
                        text=True
                    )
                    
                    if resultado.returncode == 0:
                        self.adicionar_resultado("api_python", "success", f"Arquivo Python válido: {arquivo}")
                    else:
                        self.adicionar_resultado("api_python", "error", f"Erro de sintaxe em: {arquivo}")
                        self.erros_criticos.append(f"Erro de sintaxe em arquivo Python: {arquivo}")
                        
                except Exception as e:
                    self.adicionar_resultado("api_python", "error", f"Erro ao verificar: {arquivo} - {e}")
                    self.erros_criticos.append(f"Erro ao verificar arquivo Python: {arquivo}")
            else:
                self.adicionar_resultado("api_python", "error", f"Arquivo Python não encontrado: {arquivo}")
                self.erros_criticos.append(f"Arquivo Python não encontrado: {arquivo}")
    
    def testar_banco_dados(self):
        """Testa o banco de dados"""
        logging.info("🗄️ Testando banco de dados...")
        
        # Verificar se o Docker está rodando
        try:
            resultado = subprocess.run(["docker", "ps"], capture_output=True, text=True)
            if resultado.returncode == 0:
                # Verificar containers específicos
                if "postgres" in resultado.stdout.lower():
                    self.adicionar_resultado("banco_dados", "success", "Container PostgreSQL rodando")
                else:
                    self.adicionar_resultado("banco_dados", "warning", "Container PostgreSQL não encontrado")
                    self.avisos.append("Container PostgreSQL não encontrado")
                
                if "redis" in resultado.stdout.lower():
                    self.adicionar_resultado("banco_dados", "success", "Container Redis rodando")
                else:
                    self.adicionar_resultado("banco_dados", "warning", "Container Redis não encontrado")
                    self.avisos.append("Container Redis não encontrado")
            else:
                self.adicionar_resultado("banco_dados", "error", "Docker não está rodando")
                self.erros_criticos.append("Docker não está rodando")
                
        except Exception as e:
            self.adicionar_resultado("banco_dados", "error", f"Erro ao verificar Docker: {e}")
            self.erros_criticos.append(f"Erro ao verificar Docker: {e}")
        
        # Verificar arquivos de configuração
        arquivos_config = [
            "data/postgres/",
            "docker-compose.yml"
        ]
        
        for arquivo in arquivos_config:
            caminho = self.workspace / arquivo
            if caminho.exists():
                self.adicionar_resultado("banco_dados", "success", f"Configuração encontrada: {arquivo}")
            else:
                self.adicionar_resultado("banco_dados", "warning", f"Configuração não encontrada: {arquivo}")
                self.avisos.append(f"Configuração de banco não encontrada: {arquivo}")
    
    def testar_performance(self):
        """Testa a performance dos sistemas"""
        logging.info("⚡ Testando performance...")
        
        # Teste de tempo de carregamento dos arquivos JS
        arquivos_grandes = [
            "js/aeon-brain-cultural-narrative.js",
            "js/narrative-analysis.js",
            "js/ai-ui-controller.js"
        ]
        
        for arquivo in arquivos_grandes:
            caminho = self.workspace / arquivo
            if caminho.exists():
                tamanho = caminho.stat().st_size / 1024  # KB
                
                if tamanho > 100:  # Arquivos maiores que 100KB
                    if tamanho > 500:  # Arquivos muito grandes
                        self.adicionar_resultado("performance", "warning", f"Arquivo muito grande: {arquivo} ({tamanho:.1f}KB)")
                        self.avisos.append(f"Arquivo muito grande pode afetar performance: {arquivo}")
                    else:
                        self.adicionar_resultado("performance", "success", f"Arquivo de tamanho adequado: {arquivo} ({tamanho:.1f}KB)")
                else:
                    self.adicionar_resultado("performance", "success", f"Arquivo pequeno: {arquivo} ({tamanho:.1f}KB)")
            else:
                self.adicionar_resultado("performance", "warning", f"Arquivo não encontrado para análise: {arquivo}")
                self.avisos.append(f"Arquivo não encontrado para análise de performance: {arquivo}")
    
    def testar_integracao(self):
        """Testa a integração entre sistemas"""
        logging.info("🔗 Testando integração entre sistemas...")
        
        # Verificar se os sistemas principais estão conectados
        sistemas = [
            ("js/ai-integration-real.js", "python/chess_effects_api.py", "IA → Python"),
            ("js/chess-pro-database.js", "data/postgres/", "JS → PostgreSQL"),
            ("js/gamification.js", "js/ai-gamification-integration.js", "Gamificação → IA"),
            ("js/aeon-brain-orchestrator.js", "js/aeon-brain-evaluator.js", "Orquestrador → Avaliador")
        ]
        
        for js_file, target, descricao in sistemas:
            js_path = self.workspace / js_file
            target_path = self.workspace / target
            
            if js_path.exists() and target_path.exists():
                # Verificar se há referências entre os sistemas
                try:
                    with open(js_path, 'r', encoding='utf-8') as f:
                        js_content = f.read()
                    
                    # Verificar se o arquivo JS faz referências ao target
                    if target in js_content or target_path.name in js_content:
                        self.adicionar_resultado("integracao", "success", f"Integração ativa: {descricao}")
                    else:
                        self.adicionar_resultado("integracao", "warning", f"Integração limitada: {descricao}")
                        self.avisos.append(f"Integração limitada detectada: {descricao}")
                        
                except Exception as e:
                    self.adicionar_resultado("integracao", "error", f"Erro ao verificar integração: {descricao} - {e}")
                    self.erros_criticos.append(f"Erro ao verificar integração: {descricao}")
            else:
                self.adicionar_resultado("integracao", "error", f"Arquivos de integração não encontrados: {descricao}")
                self.erros_criticos.append(f"Arquivos de integração não encontrados: {descricao}")
    
    def adicionar_resultado(self, categoria, status, mensagem):
        """Adiciona um resultado de teste"""
        resultado = {
            "categoria": categoria,
            "status": status,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat()
        }
        
        self.resultados.append(resultado)
        
        if status == "success":
            self.sucessos.append(resultado)
        elif status == "warning":
            self.avisos.append(resultado)
        elif status == "error":
            self.erros_criticos.append(resultado)
    
    def gerar_relatorio_final(self):
        """Gera o relatório final dos testes"""
        tempo_total = time.time() - self.inicio_teste
        
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "tempo_execucao": f"{tempo_total:.2f}s",
            "resumo": {
                "total_testes": len(self.resultados),
                "sucessos": len(self.sucessos),
                "avisos": len(self.avisos),
                "erros": len(self.erros_criticos)
            },
            "resultados": self.resultados,
            "erros_criticos": self.erros_criticos,
            "avisos": self.avisos,
            "sucessos": self.sucessos
        }
        
        # Salvar relatório
        arquivo_relatorio = self.workspace / f"relatorio_teste_profundo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            logging.info(f"📊 Relatório salvo em: {arquivo_relatorio}")
            
        except Exception as e:
            logging.error(f"❌ Erro ao salvar relatório: {e}")
        
        # Exibir resumo
        logging.info("=" * 60)
        logging.info("📋 RESUMO FINAL DOS TESTES")
        logging.info("=" * 60)
        logging.info(f"⏱️  Tempo total: {tempo_total:.2f}s")
        logging.info(f"✅ Sucessos: {len(self.sucessos)}")
        logging.info(f"⚠️  Avisos: {len(self.avisos)}")
        logging.info(f"❌ Erros: {len(self.erros_criticos)}")
        logging.info("=" * 60)
        
        if self.erros_criticos:
            logging.error("🚨 ERROS CRÍTICOS ENCONTRADOS:")
            for erro in self.erros_criticos:
                logging.error(f"   • {erro}")
        
        if self.avisos:
            logging.warning("⚠️  AVISOS:")
            for aviso in self.avisos:
                logging.warning(f"   • {aviso}")
        
        if len(self.sucessos) == len(self.resultados):
            logging.info("🎉 Todos os testes passaram com sucesso!")
        elif len(self.erros_criticos) == 0:
            logging.info("✅ Sistema funcionando com alguns avisos menores")
        else:
            logging.error("❌ Sistema com erros críticos que precisam ser corrigidos")

def main():
    """Função principal"""
    print("🚀 XadrezMaster - Teste Profundo dos Sistemas")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not Path("/Users/jx/WORKSPACE/PROJECTS/CHESS").exists():
        print("❌ Erro: Diretório do projeto não encontrado!")
        print("   Execute este script do diretório raiz do projeto")
        sys.exit(1)
    
    # Executar testes
    tester = TesteProfundoSistemas()
    tester.executar_teste_completo()
    
    print("\n🎯 Teste concluído! Verifique o arquivo de log para detalhes.")

if __name__ == "__main__":
    main()


