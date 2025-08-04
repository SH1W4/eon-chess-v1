from cultural_evolution import CulturalEvolution
from adaptive_decision import CulturalBehavior
import random

def simulate_game():
    evolution = CulturalEvolution()
    
    # Simular várias rodadas
    for round in range(100):
        context = {
            "under_attack": random.choice([True, False]),
            "material_advantage": random.randint(-3, 3),
            "early_game": round < 20,
            "equal_position": random.choice([True, False]),
            "center_control": random.uniform(0, 1),
            "opponent_king_exposed": random.choice([True, False])
        }
        
        behavior = evolution.evaluate_context(context)
        success_rate = random.uniform(0.0, 1.0)  # Simular sucesso aleatório
        evolution.record_outcome(behavior, success_rate, context)
    
    # Imprimir resumo da evolução
    summary = evolution.get_evolution_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    simulate_game()
