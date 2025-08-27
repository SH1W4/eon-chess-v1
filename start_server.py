#!/usr/bin/env python3
"""
Servidor HTTP Robusto para AEON CHESS
Versão: 1.0 - Monitoramento e Reinicialização Automática
"""

import http.server
import socketserver
import os
import sys
import time
import threading
import signal
from pathlib import Path

class RobustHTTPServer:
    def __init__(self, port=8000, directory="web/pages"):
        self.port = port
        self.directory = Path(directory)
        self.server = None
        self.is_running = False
        self.restart_count = 0
        self.max_restarts = 5
        self.restart_delay = 2
        
        # Configurar tratamento de sinais
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Verificar se o diretório existe
        if not self.directory.exists():
            print(f"❌ Diretório não encontrado: {self.directory}")
            sys.exit(1)
    
    def start(self):
        """Iniciar servidor com monitoramento"""
        print(f"🚀 Iniciando servidor HTTP robusto...")
        print(f"📁 Diretório: {self.directory.absolute()}")
        print(f"🌐 Porta: {self.port}")
        print(f"🔗 URL: http://localhost:{self.port}")
        
        self.is_running = True
        
        # Iniciar thread de monitoramento
        monitor_thread = threading.Thread(target=self.monitor_server, daemon=True)
        monitor_thread.start()
        
        try:
            self.run_server()
        except KeyboardInterrupt:
            print("\n🛑 Servidor interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro no servidor: {e}")
            if self.restart_count < self.max_restarts:
                self.restart_server()
            else:
                print(f"❌ Máximo de reinicializações atingido ({self.max_restarts})")
                sys.exit(1)
    
    def run_server(self):
        """Executar servidor HTTP"""
        os.chdir(self.directory)
        
        # Configurar handler personalizado
        handler = self.create_handler()
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            self.server = httpd
            print(f"✅ Servidor rodando em http://localhost:{self.port}")
            print(f"📊 Status: Ativo | Restarts: {self.restart_count}")
            print("🔄 Pressione Ctrl+C para parar")
            
            try:
                httpd.serve_forever()
            except Exception as e:
                print(f"⚠️ Erro no servidor: {e}")
                raise
    
    def create_handler(self):
        """Criar handler HTTP personalizado"""
        class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                # Log personalizado com timestamp
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {format % args}")
            
            def end_headers(self):
                # Adicionar headers de segurança
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('X-Frame-Options', 'DENY')
                self.send_header('X-XSS-Protection', '1; mode=block')
                super().end_headers()
        
        return CustomHTTPRequestHandler
    
    def monitor_server(self):
        """Monitorar saúde do servidor"""
        while self.is_running:
            time.sleep(30)  # Verificar a cada 30 segundos
            
            if self.server and not self.is_server_healthy():
                print("⚠️ Servidor não está respondendo, reiniciando...")
                self.restart_server()
    
    def is_server_healthy(self):
        """Verificar se o servidor está saudável"""
        try:
            import urllib.request
            response = urllib.request.urlopen(f"http://localhost:{self.port}", timeout=5)
            return response.getcode() == 200
        except:
            return False
    
    def restart_server(self):
        """Reiniciar servidor"""
        if self.restart_count >= self.max_restarts:
            print(f"❌ Máximo de reinicializações atingido ({self.max_restarts})")
            self.stop()
            return
        
        self.restart_count += 1
        print(f"🔄 Reiniciando servidor... (tentativa {self.restart_count}/{self.max_restarts})")
        
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
            
            time.sleep(self.restart_delay)
            self.run_server()
            
        except Exception as e:
            print(f"❌ Falha ao reiniciar: {e}")
            if self.restart_count < self.max_restarts:
                time.sleep(self.restart_delay * 2)
                self.restart_server()
    
    def stop(self):
        """Parar servidor"""
        self.is_running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        print("🛑 Servidor parado")
    
    def signal_handler(self, signum, frame):
        """Tratar sinais do sistema"""
        print(f"\n🛑 Sinal {signum} recebido, parando servidor...")
        self.stop()
        sys.exit(0)

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Servidor HTTP Robusto para AEON CHESS")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Porta do servidor (padrão: 8000)")
    parser.add_argument("-d", "--directory", default="web/pages", help="Diretório para servir (padrão: web/pages)")
    
    args = parser.parse_args()
    
    # Criar e iniciar servidor
    server = RobustHTTPServer(args.port, args.directory)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
