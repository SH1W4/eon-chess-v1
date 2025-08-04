from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
import random
import time
from datetime import datetime
from pathlib import Path
from cultural_evolution import CulturalEvolution
from adaptive_decision import CulturalBehavior

@dataclass
class RingPlayer:
    """Jogador no sistema de ring"""
    name: str
    personality: str
    evolution: CulturalEvolution = field(default_factory=CulturalEvolution)
    victories: int = 0
    defeats: int = 0
    draws: int = 0
    matches: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_stats(self):
        total_games = self.victories + self.defeats + self.draws
        return {
            'name': self.name,
            'personality': self.personality,
            'victories': self.victories,
            'defeats': self.defeats,
            'draws': self.draws,
            'win_rate': self.victories / total_games if total_games > 0 else 0,
            'total_games': total_games
        }

class ChessRing:
    """Sistema de ring para batalhas de xadrez culturais"""
    def __init__(self, database_path: str = "data/ring_matches.json"):
        self.players: Dict[str, RingPlayer] = {}
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.load_database()
    
    def add_player(self, name: str, personality: str):
        """Adiciona um novo jogador ao ring"""
        if name not in self.players:
            self.players[name] = RingPlayer(name=name, personality=personality)
    
    def simulate_match(self, player1_name: str, player2_name: str, rounds: int = 50) -> Dict[str, Any]:
        """Simula uma partida entre dois jogadores"""
        player1 = self.players[player1_name]
        player2 = self.players[player2_name]
        
        match_data = {
            'match_id': f"{int(time.time())}_{player1.name}_vs_{player2.name}",
            'date': datetime.now().isoformat(),
            'player1': player1.name,
            'player2': player2.name,
            'rounds': [],
            'final_stats': {}
        }
        
        print(f"\n=== CONFRONTO: {player1.name} vs {player2.name} ===")
        print(f"Personalidades: {player1.personality} vs {player2.personality}\n")
        
        for round_num in range(1, rounds + 1):
            round_data = self._simulate_round(player1, player2, round_num)
            match_data['rounds'].append(round_data)
            
            # Atualiza estatísticas
            if round_data['winner'] == player1.name:
                player1.victories += 1
                player2.defeats += 1
            elif round_data['winner'] == player2.name:
                player2.victories += 1
                player1.defeats += 1
            else:
                player1.draws += 1
                player2.draws += 1
            
            print(f"Rodada {round_num}: {round_data['winner'] or 'Empate'}")
        
        # Registra estatísticas finais
        match_data['final_stats'] = {
            'player1': player1.get_stats(),
            'player2': player2.get_stats()
        }
        
        # Salva o match no histórico dos jogadores
        player1.matches.append(match_data)
        player2.matches.append(match_data)
        
        self.save_match(match_data)
        return match_data
    
    def _simulate_round(self, player1: RingPlayer, player2: RingPlayer, round_num: int) -> Dict[str, Any]:
        """Simula uma rodada entre dois jogadores"""
        context = {
            "under_attack": False,
            "material_advantage": 0,
            "early_game": round_num < 20,
            "equal_position": True,
            "center_control": 0.5,
            "opponent_king_exposed": False
        }
        
        # Comportamentos iniciais
        p1_behavior = player1.evolution.evaluate_context(context)
        
        # Atualiza contexto baseado no comportamento do jogador 1
        context = self._update_context(context, p1_behavior)
        
        # Comportamento do jogador 2 com contexto atualizado
        p2_behavior = player2.evolution.evaluate_context(context)
        
        # Avalia resultado
        result = self._evaluate_round(p1_behavior, p2_behavior, context)
        
        # Registra resultados
        p1_success = 1.0 if result > 0 else (0.5 if result == 0 else 0.0)
        p2_success = 1.0 if result < 0 else (0.5 if result == 0 else 0.0)
        
        player1.evolution.record_outcome(p1_behavior, p1_success, context)
        player2.evolution.record_outcome(p2_behavior, p2_success, context)
        
        return {
            'round': round_num,
            'context': context,
            'player1_behavior': p1_behavior.name,
            'player2_behavior': p2_behavior.name,
            'winner': player1.name if result > 0 else (player2.name if result < 0 else None),
            'narratives': {
                'player1': player1.evolution.get_behavior_narrative(p1_behavior),
                'player2': player2.evolution.get_behavior_narrative(p2_behavior)
            }
        }
    
    def _update_context(self, context: Dict[str, Any], behavior: CulturalBehavior) -> Dict[str, Any]:
        """Atualiza o contexto baseado no comportamento"""
        new_context = context.copy()
        
        if behavior == CulturalBehavior.AGGRESSIVE:
            new_context["opponent_king_exposed"] = random.random() > 0.7
            new_context["equal_position"] = False
            new_context["material_advantage"] = random.randint(-1, 2)
        elif behavior == CulturalBehavior.DEFENSIVE:
            new_context["under_attack"] = False
            new_context["equal_position"] = True
            new_context["material_advantage"] = random.randint(-1, 1)
        elif behavior == CulturalBehavior.STRATEGIC:
            new_context["center_control"] = min(1.0, context["center_control"] + random.uniform(0, 0.3))
            new_context["material_advantage"] = random.randint(-1, 2)
        elif behavior == CulturalBehavior.DIPLOMATIC:
            new_context["equal_position"] = True
            new_context["material_advantage"] = random.randint(-1, 1)
        
        return new_context
    
    def _evaluate_round(self, p1_behavior: CulturalBehavior, p2_behavior: CulturalBehavior, context: Dict[str, Any]) -> int:
        """Avalia o resultado de uma rodada. Retorna: 1 (vitória p1), -1 (vitória p2), 0 (empate)"""
        base_chance = 0.5
        
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
        """Executa um torneio entre todos os jogadores"""
        players = list(self.players.keys())
        results = []
        
        print(f"\n=== INÍCIO DO TORNEIO ===")
        print(f"Jogadores: {', '.join(players)}")
        print(f"Rounds por partida: {rounds_per_match}\n")
        
        for i, player1 in enumerate(players):
            for player2 in players[i+1:]:
                match_data = self.simulate_match(player1, player2, rounds_per_match)
                results.append(match_data)
        
        print("\n=== RESULTADOS DO TORNEIO ===")
        for player_name, player in self.players.items():
            stats = player.get_stats()
            print(f"\n{player_name} ({player.personality}):")
            print(f"  Vitórias: {stats['victories']}")
            print(f"  Derrotas: {stats['defeats']}")
            print(f"  Empates: {stats['draws']}")
            print(f"  Taxa de vitória: {stats['win_rate']:.2%}")
        
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
    
    def get_player_history(self, player_name: str) -> List[Dict[str, Any]]:
        """Retorna o histórico de partidas de um jogador"""
        return [
            match for match in self.matches
            if player_name in [match['player1'], match['player2']]
        ]
    
    def get_player_stats(self, player_name: str) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas de um jogador"""
        if player_name not in self.players:
            return None
        
        player = self.players[player_name]
        stats = player.get_stats()
        
        # Adiciona dados evolutivos
        evolution_summary = player.evolution.get_evolution_summary()
        stats.update({
            'dominant_behavior': evolution_summary['dominant_behavior'].name,
            'success_rate': evolution_summary['success_rate'],
            'cultural_coherence': evolution_summary['cultural_coherence'],
            'adaptation_score': evolution_summary['adaptation_score']
        })
        
        return stats
