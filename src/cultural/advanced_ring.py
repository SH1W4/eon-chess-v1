from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
import json
import random
import time
from datetime import datetime
from pathlib import Path
from cultural_evolution import CulturalEvolution
from adaptive_decision import CulturalBehavior

@dataclass
class HistoricalLeader:
    """Representação de um líder histórico"""
    name: str
    title: str
    personality: str
    strength: float = 1.0
    weakness: float = 0.0
    evolution: CulturalEvolution = field(default_factory=CulturalEvolution)
    victories: int = 0
    defeats: int = 0
    draws: int = 0
    matches: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do líder"""
        total_games = self.victories + self.defeats + self.draws
        win_rate = self.victories / total_games if total_games > 0 else 0
        
        evolution_summary = self.evolution.get_evolution_summary()
        
        return {
            'name': self.name,
            'title': self.title,
            'personality': self.personality,
            'victories': self.victories,
            'defeats': self.defeats,
            'draws': self.draws,
            'win_rate': win_rate,
            'total_games': total_games,
            'dominant_behavior': evolution_summary['dominant_behavior'].name,
            'success_rate': evolution_summary['success_rate'],
            'cultural_coherence': evolution_summary['cultural_coherence'],
            'adaptation_score': evolution_summary['adaptation_score']
        }

class HistoricalRing:
    """Sistema avançado de ring para batalhas históricas"""
    def __init__(self, database_path: str = "data/historical_matches.json"):
        self.leaders: Dict[str, HistoricalLeader] = {}
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.load_database()
    
    def add_leader(self, name: str, title: str, personality: str, strength: float = 1.0):
        """Adiciona um novo líder ao ring"""
        if name not in self.leaders:
            self.leaders[name] = HistoricalLeader(
                name=name,
                title=title,
                personality=personality,
                strength=strength
            )
    
    def simulate_battle(self, leader1_name: str, leader2_name: str, rounds: int = 50) -> Dict[str, Any]:
        """Simula uma batalha entre dois líderes"""
        leader1 = self.leaders[leader1_name]
        leader2 = self.leaders[leader2_name]
        
        match_data = {
            'match_id': f"{int(time.time())}_{leader1.name}_vs_{leader2.name}",
            'date': datetime.now().isoformat(),
            'leader1': leader1.name,
            'leader2': leader2.name,
            'rounds': [],
            'final_stats': {}
        }
        
        print(f"\n=== CONFRONTO HISTÓRICO ===")
        print(f"{leader1.name} ({leader1.title}) vs {leader2.name} ({leader2.title})")
        print(f"Personalidades: {leader1.personality} vs {leader2.personality}\n")
        
        for round_num in range(1, rounds + 1):
            round_data = self._simulate_round(leader1, leader2, round_num)
            match_data['rounds'].append(round_data)
            
            # Atualiza estatísticas
            if round_data['winner'] == leader1.name:
                leader1.victories += 1
                leader2.defeats += 1
            elif round_data['winner'] == leader2.name:
                leader2.victories += 1
                leader1.defeats += 1
            else:
                leader1.draws += 1
                leader2.draws += 1
            
            # Imprime resultado
            print(f"Rodada {round_num}: {round_data['winner'] or 'Empate'}")
            print(f"  {leader1.name}: {round_data['narratives']['leader1']}")
            print(f"  {leader2.name}: {round_data['narratives']['leader2']}\n")
        
        # Registra estatísticas finais
        match_data['final_stats'] = {
            'leader1': leader1.get_stats(),
            'leader2': leader2.get_stats()
        }
        
        # Salva no histórico
        leader1.matches.append(match_data)
        leader2.matches.append(match_data)
        self.save_match(match_data)
        
        return match_data
    
    def _simulate_round(self, leader1: HistoricalLeader, leader2: HistoricalLeader, round_num: int) -> Dict[str, Any]:
        """Simula uma rodada de batalha"""
        context = {
            "under_attack": False,
            "material_advantage": 0,
            "early_game": round_num < 20,
            "equal_position": True,
            "center_control": 0.5,
            "opponent_king_exposed": False,
            "leader1_strength": leader1.strength,
            "leader2_strength": leader2.strength
        }
        
        # Comportamentos
        p1_behavior = leader1.evolution.evaluate_context(context)
        context = self._update_context(context, p1_behavior, leader1.strength)
        
        p2_behavior = leader2.evolution.evaluate_context(context)
        
        # Avalia resultado
        result = self._evaluate_round(p1_behavior, p2_behavior, context)
        
        # Registra resultados
        p1_success = 1.0 if result > 0 else (0.5 if result == 0 else 0.0)
        p2_success = 1.0 if result < 0 else (0.5 if result == 0 else 0.0)
        
        leader1.evolution.record_outcome(p1_behavior, p1_success, context)
        leader2.evolution.record_outcome(p2_behavior, p2_success, context)
        
        return {
            'round': round_num,
            'context': context,
            'leader1_behavior': p1_behavior.name,
            'leader2_behavior': p2_behavior.name,
            'winner': leader1.name if result > 0 else (leader2.name if result < 0 else None),
            'narratives': {
                'leader1': leader1.evolution.get_behavior_narrative(p1_behavior),
                'leader2': leader2.evolution.get_behavior_narrative(p2_behavior)
            }
        }
    
    def _update_context(self, context: Dict[str, Any], behavior: CulturalBehavior, strength: float) -> Dict[str, Any]:
        """Atualiza o contexto baseado no comportamento"""
        new_context = context.copy()
        
        if behavior == CulturalBehavior.AGGRESSIVE:
            new_context["opponent_king_exposed"] = random.random() > (0.7 - strength * 0.1)
            new_context["equal_position"] = False
            new_context["material_advantage"] = random.randint(-1, int(2 * strength))
        elif behavior == CulturalBehavior.DEFENSIVE:
            new_context["under_attack"] = False
            new_context["equal_position"] = True
            new_context["material_advantage"] = random.randint(-1, int(1 * strength))
        elif behavior == CulturalBehavior.STRATEGIC:
            new_context["center_control"] = min(1.0, context["center_control"] + random.uniform(0, 0.3 * strength))
            new_context["material_advantage"] = random.randint(-1, int(2 * strength))
        elif behavior == CulturalBehavior.DIPLOMATIC:
            new_context["equal_position"] = True
            new_context["material_advantage"] = random.randint(-1, int(1 * strength))
        
        return new_context
    
    def _evaluate_round(self, p1_behavior: CulturalBehavior, p2_behavior: CulturalBehavior, context: Dict[str, Any]) -> int:
        """Avalia o resultado de uma rodada"""
        base_chance = 0.5 * (context['leader1_strength'] / context['leader2_strength'])
        
        # Ajusta chance baseado nos comportamentos
        if p1_behavior == CulturalBehavior.AGGRESSIVE:
            if p2_behavior == CulturalBehavior.DEFENSIVE:
                base_chance -= 0.2
            elif p2_behavior == CulturalBehavior.DIPLOMATIC:
                base_chance += 0.1
        elif p1_behavior == CulturalBehavior.STRATEGIC:
            if p2_behavior == CulturalBehavior.AGGRESSIVE:
                base_chance += 0.1
            elif p2_behavior == CulturalBehavior.DEFENSIVE:
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
            return 1
        elif roll > base_chance + 0.1:
            return -1
        return 0
    
    def run_tournament(self, rounds_per_match: int = 50):
        """Executa um torneio entre todos os líderes"""
        leaders = list(self.leaders.keys())
        results = []
        
        print(f"\n=== INÍCIO DO TORNEIO ===")
        print(f"Participantes:")
        for name in leaders:
            leader = self.leaders[name]
            print(f"  {name} ({leader.title})")
        print(f"\nRounds por batalha: {rounds_per_match}\n")
        
        for i, leader1 in enumerate(leaders):
            for leader2 in leaders[i+1:]:
                match_data = self.simulate_battle(leader1, leader2, rounds_per_match)
                results.append(match_data)
        
        print("\n=== RESULTADOS DO TORNEIO ===")
        for name in leaders:
            leader = self.leaders[name]
            stats = leader.get_stats()
            print(f"\n{name} ({leader.title}):")
            print(f"  Vitórias: {stats['victories']}")
            print(f"  Derrotas: {stats['defeats']}")
            print(f"  Empates: {stats['draws']}")
            print(f"  Taxa de vitória: {stats['win_rate']:.2%}")
            print(f"  Comportamento dominante: {stats['dominant_behavior']}")
            print(f"  Coerência cultural: {stats['cultural_coherence']:.2f}")
        
        return results
    
    def load_database(self):
        """Carrega dados do banco de dados"""
        if self.database_path.exists():
            with open(self.database_path, 'r') as f:
                self.matches = json.load(f)
        else:
            self.matches = []
    
    def save_match(self, match_data: Dict[str, Any]):
        """Salva uma partida no banco de dados"""
        self.matches.append(match_data)
        with open(self.database_path, 'w') as f:
            json.dump(self.matches, f, indent=2)
    
    def get_leader_history(self, name: str) -> List[Dict[str, Any]]:
        """Retorna o histórico de batalhas de um líder"""
        return [
            match for match in self.matches
            if name in [match['leader1'], match['leader2']]
        ]
    
    def get_leader_stats(self, name: str) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas de um líder"""
        if name not in self.leaders:
            return None
        return self.leaders[name].get_stats()
