from locust import HttpUser, task, between
from random import choice
import json

class ChessMasterUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Autenticação do usuário"""
        response = self.client.post("/auth/login", json={
            "username": "test_user",
            "password": "test_password"
        })
        self.token = response.json()["token"]
        self.client.headers = {'Authorization': f'Bearer {self.token}'}
    
    @task(3)
    def get_move(self):
        """Solicita próximo movimento"""
        board_state = {
            "position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "culture": choice(["medieval", "futuristic"])
        }
        
        self.client.post("/api/v1/move", json=board_state)
    
    @task(2)
    def evaluate_position(self):
        """Avalia uma posição"""
        position = {
            "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            "depth": 4
        }
        
        self.client.post("/api/v1/evaluate", json=position)
    
    @task(1)
    def get_narrative(self):
        """Solicita narrativa cultural"""
        move = {
            "from": "e2",
            "to": "e4",
            "piece": "P",
            "culture": "medieval"
        }
        
        self.client.post("/api/v1/narrative", json=move)

class ArquimaxUser(HttpUser):
    wait_time = between(2, 5)
    
    def on_start(self):
        """Inicialização do ARQUIMAX"""
        response = self.client.post("/arquimax/init", json={
            "capabilities": ["project_management", "monitoring", "analysis"]
        })
        self.session_id = response.json()["session_id"]
    
    @task(2)
    def analyze_architecture(self):
        """Solicita análise arquitetural"""
        self.client.post(f"/arquimax/analyze/{self.session_id}", json={
            "type": "architecture",
            "depth": "full"
        })
    
    @task(1)
    def get_metrics(self):
        """Obtém métricas do sistema"""
        self.client.get(f"/arquimax/metrics/{self.session_id}")

class NexusUser(HttpUser):
    wait_time = between(1, 4)
    
    def on_start(self):
        """Inicialização do NEXUS"""
        response = self.client.post("/nexus/connect", json={
            "mode": "adaptive",
            "features": ["sync", "monitoring"]
        })
        self.connection_id = response.json()["connection_id"]
    
    @task(3)
    def sync_data(self):
        """Sincroniza dados"""
        self.client.post(f"/nexus/sync/{self.connection_id}", json={
            "type": "full",
            "timestamp": "2025-07-24T22:00:00Z"
        })
    
    @task(2)
    def check_status(self):
        """Verifica status da conexão"""
        self.client.get(f"/nexus/status/{self.connection_id}")

def run():
    """Executa teste de carga"""
    import os
    from locust import runners
    from locust.env import Environment
    from locust.stats import stats_printer, stats_history
    import gevent
    
    # Configuração do ambiente
    env = Environment(
        user_classes=[ChessMasterUser, ArquimaxUser, NexusUser],
        host="http://localhost:8080"
    )
    
    # Inicia o teste
    env.create_local_runner()
    
    # Inicia o web monitor
    gevent.spawn(stats_printer(env.stats))
    
    # Inicia a carga
    env.runner.start(100, spawn_rate=10)
    
    # Aguarda
    gevent.spawn_later(3600, lambda: env.runner.quit())
    
    # Aguarda finalização
    env.runner.greenlet.join()
    
    # Gera relatório
    env.create_web_ui("127.0.0.1", 8089)

if __name__ == "__main__":
    run()
