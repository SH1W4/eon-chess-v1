"""
Adaptive Learning Module - Implementação Real
Sistema de aprendizado adaptativo para AEON Chess
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import json
from datetime import datetime

class PlayerProfile:
    """Perfil real do jogador com análise profunda"""
    
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.games_played = 0
        self.style_vector = np.zeros(10)  # 10 dimensões de estilo
        self.opening_preferences = defaultdict(int)
        self.time_management = {'fast': 0, 'medium': 0, 'slow': 0}
        self.tactical_preference = 0.5  # 0 = posicional, 1 = tático
        self.risk_tolerance = 0.5  # 0 = conservador, 1 = agressivo
        self.learning_rate = 0.1
        
    def update_profile(self, game_data: Dict):
        """Atualiza perfil baseado em nova partida"""
        self.games_played += 1
        
        # Atualiza preferências de abertura
        if 'opening' in game_data:
            self.opening_preferences[game_data['opening']] += 1
        
        # Atualiza gestão de tempo
        if 'avg_move_time' in game_data:
            if game_data['avg_move_time'] < 10:
                self.time_management['fast'] += 1
            elif game_data['avg_move_time'] < 30:
                self.time_management['medium'] += 1
            else:
                self.time_management['slow'] += 1
        
        # Ajusta preferências táticas vs posicionais
        if 'tactical_moves' in game_data:
            tactical_ratio = game_data['tactical_moves'] / max(game_data.get('total_moves', 1), 1)
            self.tactical_preference = (1 - self.learning_rate) * self.tactical_preference +                                       self.learning_rate * tactical_ratio
        
        # Ajusta tolerância ao risco
        if 'sacrifices' in game_data:
            risk_factor = game_data['sacrifices'] / max(game_data.get('total_moves', 1), 1)
            self.risk_tolerance = (1 - self.learning_rate) * self.risk_tolerance +                                  self.learning_rate * risk_factor
        
        # Atualiza vetor de estilo
        self._update_style_vector(game_data)
    
    def _update_style_vector(self, game_data: Dict):
        """Atualiza vetor de estilo multidimensional"""
        new_features = np.array([
            self.tactical_preference,
            self.risk_tolerance,
            game_data.get('aggression', 0.5),
            game_data.get('complexity_preference', 0.5),
            game_data.get('endgame_skill', 0.5),
            game_data.get('time_pressure_handling', 0.5),
            game_data.get('sacrifice_tendency', 0.5),
            game_data.get('defensive_skill', 0.5),
            game_data.get('positional_understanding', 0.5),
            game_data.get('calculation_depth', 0.5)
        ])
        
        self.style_vector = (1 - self.learning_rate) * self.style_vector +                            self.learning_rate * new_features
    
    def get_style_summary(self) -> Dict:
        """Retorna resumo do estilo do jogador"""
        return {
            'games_analyzed': self.games_played,
            'style': 'Tático' if self.tactical_preference > 0.6 else 'Posicional' if self.tactical_preference < 0.4 else 'Equilibrado',
            'risk_profile': 'Agressivo' if self.risk_tolerance > 0.6 else 'Conservador' if self.risk_tolerance < 0.4 else 'Moderado',
            'favorite_opening': max(self.opening_preferences.items(), key=lambda x: x[1])[0] if self.opening_preferences else 'None',
            'time_style': max(self.time_management.items(), key=lambda x: x[1])[0],
            'style_vector': self.style_vector.tolist()
        }

class AdaptiveLearningEngine:
    """Motor de aprendizado adaptativo real"""
    
    def __init__(self):
        self.player_profiles = {}
        self.global_patterns = defaultdict(list)
        self.adaptation_history = []
        self.learning_enabled = True
        
    def get_or_create_profile(self, player_id: str) -> PlayerProfile:
        """Obtém ou cria perfil do jogador"""
        if player_id not in self.player_profiles:
            self.player_profiles[player_id] = PlayerProfile(player_id)
        return self.player_profiles[player_id]
    
    def learn_from_game(self, player_id: str, game_data: Dict):
        """Aprende com uma partida jogada"""
        if not self.learning_enabled:
            return
        
        profile = self.get_or_create_profile(player_id)
        profile.update_profile(game_data)
        
        # Registra no histórico
        self.adaptation_history.append({
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'game_data': game_data,
            'profile_state': profile.get_style_summary()
        })
        
        # Atualiza padrões globais
        self._update_global_patterns(game_data)
    
    def _update_global_patterns(self, game_data: Dict):
        """Atualiza padrões globais aprendidos"""
        if 'key_positions' in game_data:
            for position in game_data['key_positions']:
                self.global_patterns['critical_positions'].append(position)
        
        if 'successful_tactics' in game_data:
            self.global_patterns['tactics'].extend(game_data['successful_tactics'])
    
    def adapt_to_player(self, player_id: str) -> Dict:
        """Adapta engine ao estilo do jogador"""
        profile = self.get_or_create_profile(player_id)
        
        adaptations = {
            'search_depth': self._calculate_search_depth(profile),
            'evaluation_weights': self._adjust_evaluation_weights(profile),
            'opening_book': self._select_opening_book(profile),
            'time_allocation': self._adjust_time_management(profile),
            'tactical_alertness': profile.tactical_preference,
            'risk_parameters': {
                'sacrifice_threshold': 0.3 if profile.risk_tolerance > 0.7 else 0.7,
                'defensive_priority': 1.0 - profile.risk_tolerance
            }
        }
        
        return adaptations
    
    def _calculate_search_depth(self, profile: PlayerProfile) -> int:
        """Calcula profundidade de busca baseada no perfil"""
        base_depth = 10
        if profile.tactical_preference > 0.7:
            base_depth += 2  # Mais profundidade para jogadores táticos
        if profile.games_played > 50:
            base_depth += 1  # Jogadores experientes
        return base_depth
    
    def _adjust_evaluation_weights(self, profile: PlayerProfile) -> Dict[str, float]:
        """Ajusta pesos da função de avaliação"""
        return {
            'material': 1.0,
            'position': 0.5 + (1 - profile.tactical_preference) * 0.5,
            'mobility': 0.3 + profile.risk_tolerance * 0.2,
            'king_safety': 0.8 - profile.risk_tolerance * 0.3,
            'pawn_structure': 0.4 + (1 - profile.tactical_preference) * 0.3
        }
    
    def _select_opening_book(self, profile: PlayerProfile) -> List[str]:
        """Seleciona repertório de aberturas"""
        if profile.risk_tolerance > 0.6:
            return ['Kings Gambit', 'Sicilian Dragon', 'Benoni Defense']
        elif profile.risk_tolerance < 0.4:
            return ['Italian Game', 'Queens Gambit', 'French Defense']
        else:
            return ['Ruy Lopez', 'Nimzo Indian', 'English Opening']
    
    def _adjust_time_management(self, profile: PlayerProfile) -> Dict[str, float]:
        """Ajusta gestão de tempo"""
        time_style = profile.time_management
        total = sum(time_style.values()) or 1
        
        return {
            'opening_ratio': 0.15 if time_style['fast'] / total > 0.5 else 0.25,
            'middle_ratio': 0.60,
            'endgame_ratio': 0.25 if time_style['fast'] / total > 0.5 else 0.15,
            'increment_usage': 0.8 if time_style['slow'] / total > 0.5 else 0.5
        }

# Função de teste
def test_adaptive_learning():
    """Testa o sistema de aprendizado adaptativo"""
    engine = AdaptiveLearningEngine()
    
    # Simula algumas partidas
    test_games = [
        {
            'opening': 'Sicilian Defense',
            'avg_move_time': 15,
            'tactical_moves': 12,
            'total_moves': 40,
            'sacrifices': 2,
            'aggression': 0.7,
            'complexity_preference': 0.8
        },
        {
            'opening': 'Kings Indian',
            'avg_move_time': 25,
            'tactical_moves': 8,
            'total_moves': 45,
            'sacrifices': 1,
            'aggression': 0.5,
            'complexity_preference': 0.6
        }
    ]
    
    # Aprende com as partidas
    for game in test_games:
        engine.learn_from_game('test_player', game)
    
    # Obtém adaptações
    profile = engine.get_or_create_profile('test_player')
    adaptations = engine.adapt_to_player('test_player')
    
    return {
        'profile_created': profile.games_played > 0,
        'style_learned': profile.get_style_summary(),
        'adaptations_generated': len(adaptations) > 0,
        'adaptation_details': adaptations
    }

if __name__ == "__main__":
    test_results = test_adaptive_learning()
    print("Adaptive Learning Test Results:", json.dumps(test_results, indent=2))
