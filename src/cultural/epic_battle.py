from cultural_evolution import CulturalEvolution
from adaptive_decision import CulturalBehavior
import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.evolution = CulturalEvolution()
        self.victories = 0
        self.defeats = 0
        self.draws = 0
    
    def get_stats(self):
        return {
            'victories': self.victories,
            'defeats': self.defeats,
            'draws': self.draws,
            'win_rate': self.victories / (self.victories + self.defeats + self.draws) if (self.victories + self.defeats + self.draws) > 0 else 0
        }

def simulate_move(attacker, defender, round_number):
    """Simula um movimento no jogo"""
    # Contexto base
    context = {
        "under_attack": False,
        "material_advantage": 0,
        "early_game": round_number < 20,
        "equal_position": True,
        "center_control": 0.5,
        "opponent_king_exposed": False
    }
    
    # Comportamento do atacante
    attacker_behavior = attacker.evolution.evaluate_context(context)
    
    # Atualiza contexto baseado no comportamento do atacante
    if attacker_behavior == CulturalBehavior.AGGRESSIVE:
        context["opponent_king_exposed"] = random.random() > 0.7
        context["equal_position"] = False
        context["material_advantage"] = random.randint(-1, 2)
    elif attacker_behavior == CulturalBehavior.DEFENSIVE:
        context["under_attack"] = False
        context["equal_position"] = True
        context["material_advantage"] = random.randint(-1, 1)
    elif attacker_behavior == CulturalBehavior.STRATEGIC:
        context["center_control"] = min(1.0, context["center_control"] + random.uniform(0, 0.3))
        context["material_advantage"] = random.randint(-1, 2)
    
    # Comportamento do defensor
    defender_context = context.copy()
    defender_context["under_attack"] = attacker_behavior == CulturalBehavior.AGGRESSIVE
    defender_behavior = defender.evolution.evaluate_context(defender_context)
    
    # Determina resultado do confronto
    result = evaluate_confrontation(attacker_behavior, defender_behavior, context)
    
    return result, attacker_behavior, defender_behavior, context

def evaluate_confrontation(attacker_behavior, defender_behavior, context):
    """Avalia o resultado do confronto entre comportamentos"""
    base_chance = 0.5
    
    # Ajusta chance baseado nos comportamentos
    if attacker_behavior == CulturalBehavior.AGGRESSIVE:
        if defender_behavior == CulturalBehavior.DEFENSIVE:
            base_chance -= 0.2
        elif defender_behavior == CulturalBehavior.DIPLOMATIC:
            base_chance += 0.1
    elif attacker_behavior == CulturalBehavior.STRATEGIC:
        if defender_behavior == CulturalBehavior.AGGRESSIVE:
            base_chance += 0.1
        elif defender_behavior == CulturalBehavior.DEFENSIVE:
            base_chance -= 0.1
    
    # Ajusta baseado no contexto
    if context["material_advantage"] > 0:
        base_chance += 0.1
    elif context["material_advantage"] < 0:
        base_chance -= 0.1
    
    if context["center_control"] > 0.7:
        base_chance += 0.1
    
    if context["opponent_king_exposed"]:
        base_chance += 0.2
    
    # Randomiza resultado final
    roll = random.random()
    if roll < base_chance - 0.1:
        return 1  # Vitória do atacante
    elif roll > base_chance + 0.1:
        return -1  # Vitória do defensor
    else:
        return 0  # Empate

def print_battle_round(round_number, player1, player2, result, p1_behavior, p2_behavior, context):
    """Imprime os detalhes de uma rodada da batalha"""
    print(f"\n=== Rodada {round_number} ===")
    print(f"{player1.name} ({p1_behavior.name}) vs {player2.name} ({p2_behavior.name})")
    
    if result == 1:
        print(f"Vitória para {player1.name}!")
    elif result == -1:
        print(f"Vitória para {player2.name}!")
    else:
        print("Empate!")
    
    # Gera narrativa do comportamento
    p1_narrative = player1.evolution.get_behavior_narrative(p1_behavior)
    p2_narrative = player2.evolution.get_behavior_narrative(p2_behavior)
    print(f"\n{player1.name}: {p1_narrative}")
    print(f"{player2.name}: {p2_narrative}")
    
    # Mostra métricas relevantes
    print("\nContexto da batalha:")
    for key, value in context.items():
        print(f"  {key}: {value}")

def epic_battle():
    """Simula uma batalha épica entre dois jogadores"""
    print("=== CONFRONTO ÉPICO DE XADREZ ===\n")
    
    # Cria jogadores
    player1 = Player("Magnus")
    player2 = Player("Kasparov")
    
    total_rounds = 50
    print(f"Iniciando batalha de {total_rounds} rodadas...\n")
    
    for round in range(1, total_rounds + 1):
        # Simula rodada
        result, p1_behavior, p2_behavior, context = simulate_move(player1, player2, round)
        
        # Atualiza estatísticas
        if result == 1:
            player1.victories += 1
            player2.defeats += 1
        elif result == -1:
            player2.victories += 1
            player1.defeats += 1
        else:
            player1.draws += 1
            player2.draws += 1
        
        # Registra resultados para evolução cultural
        p1_success = 1.0 if result == 1 else (0.5 if result == 0 else 0.0)
        p2_success = 1.0 if result == -1 else (0.5 if result == 0 else 0.0)
        
        player1.evolution.record_outcome(p1_behavior, p1_success, context)
        player2.evolution.record_outcome(p2_behavior, p2_success, context)
        
        # Imprime resultado da rodada
        print_battle_round(round, player1, player2, result, p1_behavior, p2_behavior, context)
        time.sleep(1)  # Pausa dramática
    
    # Imprime estatísticas finais
    print("\n=== RESULTADO FINAL ===")
    print(f"\n{player1.name}:")
    stats1 = player1.get_stats()
    for key, value in stats1.items():
        print(f"  {key}: {value}")
    
    print(f"\n{player2.name}:")
    stats2 = player2.get_stats()
    for key, value in stats2.items():
        print(f"  {key}: {value}")
    
    # Mostra evolução cultural final
    print("\n=== EVOLUÇÃO CULTURAL ===")
    print(f"\n{player1.name}:")
    summary1 = player1.evolution.get_evolution_summary()
    for key, value in summary1.items():
        print(f"  {key}: {value}")
    
    print(f"\n{player2.name}:")
    summary2 = player2.evolution.get_evolution_summary()
    for key, value in summary2.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    epic_battle()
