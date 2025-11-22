#!/usr/bin/env python3
"""
Servidor Integrado AEON CHESS (Frontend + Backend)
Versão: 2.0 - Ignição Completa
"""

import subprocess
import sys
import time
import threading
import signal
import os

class SystemIgnition:
    def __init__(self):
        self.processes = []
        self.running = True
        
        # Configurar sinais
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def start_backend(self):
        """Inicia o Motor (FastAPI)"""
        print("🏎️  Ligando o Motor (Backend/FastAPI)...")
        try:
            # Instalar dependências se necessário (simplificado)
            # subprocess.run([sys.executable, "-m", "pip", "install", "-r", "src/api/requirements.txt"], check=True)
            
            # Iniciar servidor
            cmd = [sys.executable, "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
            process = subprocess.Popen(cmd, cwd=os.getcwd())
            self.processes.append(process)
            print("✅ Motor ligado na porta 8000")
        except Exception as e:
            print(f"❌ Falha no Motor: {e}")

    def start_frontend(self):
        """Inicia a Carroceria (Next.js)"""
        print("🎨 Polindo a Carroceria (Frontend/Next.js)...")
        try:
            # Iniciar servidor dev
            cmd = ["npm", "run", "dev"]
            process = subprocess.Popen(cmd, cwd=os.getcwd())
            self.processes.append(process)
            print("✅ Painel aceso na porta 3000")
        except Exception as e:
            print(f"❌ Falha no Painel: {e}")

    def monitor(self):
        """Monitora os sistemas"""
        print("\n🚀 AEON CHESS SYSTEM ONLINE")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000/health")
        print("   Proxy:    http://localhost:3000/health (Via Frontend)")
        print("\n🛑 Pressione Ctrl+C para desligar os motores\n")
        
        while self.running:
            time.sleep(1)
            # Verificar se processos ainda estão vivos
            for p in self.processes:
                if p.poll() is not None:
                    print(f"⚠️ Um sistema parou inesperadamente (PID {p.pid})")
                    self.shutdown(None, None)

    def shutdown(self, signum, frame):
        """Desliga tudo"""
        print("\n🛑 Desligando sistemas...")
        self.running = False
        for p in self.processes:
            p.terminate()
        sys.exit(0)

def main():
    system = SystemIgnition()
    
    # Iniciar threads para não bloquear
    system.start_backend()
    time.sleep(2) # Esperar motor esquentar
    system.start_frontend()
    
    system.monitor()

if __name__ == "__main__":
    main()
