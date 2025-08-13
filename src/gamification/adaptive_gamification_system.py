"""
Sistema de Gamificação Adaptativa para CHESS
Integração completa com narrativa Ink e IA adaptativa
"""

import json
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import numpy as np

class AchievementTier(Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    LEGENDARY = "legendary"

class SkillDomain(Enum):
    OPENING = "opening"
    MIDDLEGAME = "middlegame"
    ENDGAME = "endgame"
    TACTICS = "tactics"
    STRATEGY = "strategy"
    TIME_MANAGEMENT = "time_management"
    PSYCHOLOGICAL = "psychological"

class EmotionalState(Enum):
    CONFIDENT = "confident"
    FOCUSED = "focused"
    ANXIOUS = "anxious"
    DETERMINED = "determined"
    ENLIGHTENED = "enlightened"
    FRUSTRATED = "frustrated"
    INSPIRED = "inspired"

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    tier: AchievementTier
    xp_reward: int
    rating_bonus: int
    cultural_bonus: Dict[str, int]
    unlock_condition: str
    icon: str
    narrative_unlock: str
    is_hidden: bool = False
    is_unlocked: bool = False
    unlock_date: Optional[datetime] = None
    progress: float = 0.0

@dataclass
class PlayerProfile:
    player_id: str
    name: str
    level: int = 1
    xp: int = 0
    rating: int = 1200
    culture: str = ""
    style: str = ""
    total_games: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    current_streak: int = 0
    best_streak: int = 0
    achievements: List[str] = field(default_factory=list)
    cultural_mastery: Dict[str, float] = field(default_factory=dict)
    skill_levels: Dict[SkillDomain, float] = field(default_factory=dict)
    emotional_state: EmotionalState = EmotionalState.FOCUSED
    last_game_timestamp: Optional[datetime] = None
    daily_goals_progress: Dict[str, float] = field(default_factory=dict)
    season_rank: Optional[str] = None
    mentor_level: int = 0

class AdaptiveGamificationSystem:
    def __init__(self):
        self.achievements = self._initialize_achievements()
        self.daily_challenges = []
        self.weekly_quests = []
        self.seasonal_events = []
        self.narrative_state = {}
        self.ai_adaptation_parameters = self._initialize_ai_parameters()
        
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """Inicializa o sistema completo de conquistas"""
        achievements = {
            # Conquistas de Progressão
            "first_victory": Achievement(
                id="first_victory",
                name="Primeira Vitória",
                description="Vença sua primeira partida",
                tier=AchievementTier.BRONZE,
                xp_reward=100,
                rating_bonus=0,
                cultural_bonus={},
                unlock_condition="wins >= 1",
                icon="🏆",
                narrative_unlock="first_victory_story"
            ),
            
            "streak_master": Achievement(
                id="streak_master",
                name="Mestre das Sequências",
                description="Vença 10 partidas consecutivas",
                tier=AchievementTier.GOLD,
                xp_reward=500,
                rating_bonus=25,
                cultural_bonus={"all": 5},
                unlock_condition="current_streak >= 10",
                icon="🔥",
                narrative_unlock="streak_master_story"
            ),
            
            # Conquistas Culturais
            "cultural_initiate": Achievement(
                id="cultural_initiate",
                name="Iniciado Cultural",
                description="Alcance 25% de maestria em uma cultura",
                tier=AchievementTier.BRONZE,
                xp_reward=200,
                rating_bonus=0,
                cultural_bonus={"selected": 10},
                unlock_condition="any_cultural_mastery >= 25",
                icon="🌍",
                narrative_unlock="cultural_initiate_story"
            ),
            
            "cultural_master": Achievement(
                id="cultural_master",
                name="Mestre Cultural",
                description="Alcance 100% de maestria em uma cultura",
                tier=AchievementTier.LEGENDARY,
                xp_reward=2000,
                rating_bonus=100,
                cultural_bonus={"selected": 50},
                unlock_condition="any_cultural_mastery >= 100",
                icon="👑",
                narrative_unlock="cultural_master_story",
                is_hidden=True
            ),
            
            # Conquistas de Habilidade
            "tactical_genius": Achievement(
                id="tactical_genius",
                name="Gênio Tático",
                description="Complete 50 puzzles táticos com 90% de precisão",
                tier=AchievementTier.PLATINUM,
                xp_reward=750,
                rating_bonus=30,
                cultural_bonus={"Samurai": 15},
                unlock_condition="tactical_puzzles_solved >= 50 AND tactical_accuracy >= 0.9",
                icon="🧩",
                narrative_unlock="tactical_genius_story"
            ),
            
            # Conquistas Emocionais/Psicológicas
            "zen_master": Achievement(
                id="zen_master",
                name="Mestre Zen",
                description="Mantenha estado 'Focado' por 20 partidas consecutivas",
                tier=AchievementTier.GOLD,
                xp_reward=600,
                rating_bonus=20,
                cultural_bonus={"Samurai": 20, "Maia": 15},
                unlock_condition="focused_games_streak >= 20",
                icon="🧘",
                narrative_unlock="zen_master_story"
            ),
            
            # Conquistas Épicas
            "grandmaster_ascension": Achievement(
                id="grandmaster_ascension",
                name="Ascensão do Grão-Mestre",
                description="Alcance rating 2500",
                tier=AchievementTier.LEGENDARY,
                xp_reward=5000,
                rating_bonus=200,
                cultural_bonus={"all": 25},
                unlock_condition="rating >= 2500",
                icon="♔",
                narrative_unlock="grandmaster_story",
                is_hidden=True
            )
        }
        
        return achievements
    
    def _initialize_ai_parameters(self) -> Dict:
        """Inicializa parâmetros de adaptação da IA"""
        return {
            "difficulty_adaptation_rate": 0.1,
            "style_learning_rate": 0.05,
            "emotional_influence_factor": 0.3,
            "cultural_bias_strength": 0.2,
            "narrative_coherence_weight": 0.8,
            "player_modeling_depth": 5,
            "adaptation_momentum": 0.7
        }
    
    def update_player_state(self, player: PlayerProfile, game_result: Dict) -> Dict:
        """Atualiza o estado do jogador após uma partida"""
        updates = {
            "xp_gained": 0,
            "rating_change": 0,
            "achievements_unlocked": [],
            "level_up": False,
            "emotional_shift": None,
            "narrative_triggers": [],
            "ai_adaptations": {}
        }
        
        # Atualiza estatísticas básicas
        player.total_games += 1
        
        if game_result["outcome"] == "win":
            player.wins += 1
            player.current_streak += 1
            player.best_streak = max(player.best_streak, player.current_streak)
            updates["xp_gained"] = self._calculate_xp_reward(player, game_result)
            updates["rating_change"] = self._calculate_rating_change(player, game_result)
        elif game_result["outcome"] == "draw":
            player.draws += 1
            player.current_streak = 0
            updates["xp_gained"] = self._calculate_xp_reward(player, game_result) // 2
            updates["rating_change"] = 0
        else:  # loss
            player.losses += 1
            player.current_streak = 0
            updates["xp_gained"] = self._calculate_xp_reward(player, game_result) // 4
            updates["rating_change"] = -self._calculate_rating_change(player, game_result, loss=True)
        
        # Atualiza XP e verifica level up
        player.xp += updates["xp_gained"]
        if player.xp >= self._xp_for_next_level(player.level):
            player.level += 1
            player.xp = player.xp - self._xp_for_next_level(player.level - 1)
            updates["level_up"] = True
            updates["narrative_triggers"].append("level_up")
        
        # Atualiza rating
        player.rating += updates["rating_change"]
        
        # Atualiza maestria cultural
        if player.culture:
            culture_progress = self._calculate_cultural_progress(player, game_result)
            player.cultural_mastery[player.culture] = min(100, 
                player.cultural_mastery.get(player.culture, 0) + culture_progress)
        
        # Verifica conquistas
        updates["achievements_unlocked"] = self._check_achievements(player)
        
        # Atualiza estado emocional
        new_emotional_state = self._calculate_emotional_state(player, game_result)
        if new_emotional_state != player.emotional_state:
            updates["emotional_shift"] = (player.emotional_state, new_emotional_state)
            player.emotional_state = new_emotional_state
            updates["narrative_triggers"].append(f"emotional_shift_{new_emotional_state.value}")
        
        # Adapta parâmetros da IA
        updates["ai_adaptations"] = self._adapt_ai_parameters(player, game_result)
        
        # Atualiza timestamp
        player.last_game_timestamp = datetime.now()
        
        return updates
    
    def _calculate_xp_reward(self, player: PlayerProfile, game_result: Dict) -> int:
        """Calcula recompensa de XP com base em múltiplos fatores"""
        base_xp = 100
        
        # Multiplicadores
        multipliers = []
        
        # Dificuldade do oponente
        rating_diff = game_result.get("opponent_rating", player.rating) - player.rating
        difficulty_multiplier = 1 + (rating_diff / 1000)
        multipliers.append(max(0.5, min(2.0, difficulty_multiplier)))
        
        # Duração da partida
        game_duration = game_result.get("duration_minutes", 10)
        if game_duration > 30:
            multipliers.append(1.5)
        elif game_duration > 15:
            multipliers.append(1.2)
        
        # Performance
        accuracy = game_result.get("accuracy", 0.7)
        if accuracy > 0.9:
            multipliers.append(1.5)
        elif accuracy > 0.8:
            multipliers.append(1.2)
        
        # Bônus cultural
        if game_result.get("cultural_style_used"):
            multipliers.append(1.3)
        
        # Estado emocional
        if player.emotional_state == EmotionalState.INSPIRED:
            multipliers.append(1.5)
        elif player.emotional_state == EmotionalState.CONFIDENT:
            multipliers.append(1.2)
        elif player.emotional_state == EmotionalState.FRUSTRATED:
            multipliers.append(0.8)
        
        # Calcula XP final
        total_multiplier = 1
        for mult in multipliers:
            total_multiplier *= mult
        
        return int(base_xp * total_multiplier)
    
    def _calculate_rating_change(self, player: PlayerProfile, game_result: Dict, loss=False) -> int:
        """Calcula mudança de rating usando sistema ELO adaptativo"""
        opponent_rating = game_result.get("opponent_rating", player.rating)
        
        # K-factor adaptativo baseado no nível do jogador
        if player.level < 10:
            k_factor = 40
        elif player.level < 20:
            k_factor = 30
        elif player.level < 30:
            k_factor = 20
        else:
            k_factor = 15
        
        # Cálculo ELO padrão
        expected_score = 1 / (1 + 10 ** ((opponent_rating - player.rating) / 400))
        actual_score = 0 if loss else 1
        
        rating_change = k_factor * (actual_score - expected_score)
        
        # Ajustes adicionais
        if player.emotional_state == EmotionalState.ENLIGHTENED:
            rating_change *= 1.2
        
        return int(rating_change)
    
    def _calculate_cultural_progress(self, player: PlayerProfile, game_result: Dict) -> float:
        """Calcula progresso na maestria cultural"""
        base_progress = 1.0
        
        if game_result["outcome"] == "win":
            base_progress *= 2.0
        
        # Bônus por usar estilo cultural
        if game_result.get("cultural_moves_percentage", 0) > 0.7:
            base_progress *= 1.5
        
        # Bônus por precisão
        accuracy = game_result.get("accuracy", 0.7)
        base_progress *= (0.5 + accuracy * 0.5)
        
        return base_progress
    
    def _check_achievements(self, player: PlayerProfile) -> List[Achievement]:
        """Verifica e desbloqueia novas conquistas"""
        unlocked = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement.is_unlocked or achievement_id in player.achievements:
                continue
            
            # Avalia condição de desbloqueio
            if self._evaluate_achievement_condition(achievement, player):
                achievement.is_unlocked = True
                achievement.unlock_date = datetime.now()
                player.achievements.append(achievement_id)
                
                # Aplica recompensas
                player.xp += achievement.xp_reward
                player.rating += achievement.rating_bonus
                
                # Aplica bônus cultural
                for culture, bonus in achievement.cultural_bonus.items():
                    if culture == "all":
                        for c in ["Viking", "Maia", "Samurai", "Azteca"]:
                            player.cultural_mastery[c] = min(100,
                                player.cultural_mastery.get(c, 0) + bonus)
                    elif culture == "selected":
                        player.cultural_mastery[player.culture] = min(100,
                            player.cultural_mastery.get(player.culture, 0) + bonus)
                    else:
                        player.cultural_mastery[culture] = min(100,
                            player.cultural_mastery.get(culture, 0) + bonus)
                
                unlocked.append(achievement)
        
        return unlocked
    
    def _evaluate_achievement_condition(self, achievement: Achievement, player: PlayerProfile) -> bool:
        """Avalia se a condição de uma conquista foi atendida"""
        # Este seria um parser mais complexo em produção
        condition = achievement.unlock_condition
        
        # Exemplos simples de avaliação
        if "wins >=" in condition:
            required_wins = int(condition.split(">=")[1].strip())
            return player.wins >= required_wins
        
        elif "current_streak >=" in condition:
            required_streak = int(condition.split(">=")[1].strip())
            return player.current_streak >= required_streak
        
        elif "rating >=" in condition:
            required_rating = int(condition.split(">=")[1].strip())
            return player.rating >= required_rating
        
        elif "any_cultural_mastery >=" in condition:
            required_mastery = float(condition.split(">=")[1].strip())
            return any(mastery >= required_mastery 
                      for mastery in player.cultural_mastery.values())
        
        return False
    
    def _calculate_emotional_state(self, player: PlayerProfile, game_result: Dict) -> EmotionalState:
        """Calcula novo estado emocional baseado em performance e histórico"""
        # Fatores que influenciam o estado emocional
        win_rate = player.wins / max(1, player.total_games)
        recent_performance = game_result["outcome"] == "win"
        accuracy = game_result.get("accuracy", 0.7)
        time_pressure = game_result.get("time_pressure", 0.5)
        
        # Sistema de pontuação emocional
        emotional_scores = {
            EmotionalState.CONFIDENT: 0,
            EmotionalState.FOCUSED: 0,
            EmotionalState.ANXIOUS: 0,
            EmotionalState.DETERMINED: 0,
            EmotionalState.ENLIGHTENED: 0,
            EmotionalState.FRUSTRATED: 0,
            EmotionalState.INSPIRED: 0
        }
        
        # Calcula pontuações
        if recent_performance:
            emotional_scores[EmotionalState.CONFIDENT] += 3
            emotional_scores[EmotionalState.INSPIRED] += 2
        else:
            emotional_scores[EmotionalState.FRUSTRATED] += 2
            emotional_scores[EmotionalState.DETERMINED] += 1
        
        if accuracy > 0.85:
            emotional_scores[EmotionalState.FOCUSED] += 3
            emotional_scores[EmotionalState.ENLIGHTENED] += 1
        
        if time_pressure > 0.7:
            emotional_scores[EmotionalState.ANXIOUS] += 2
        
        if player.current_streak > 5:
            emotional_scores[EmotionalState.CONFIDENT] += 2
            emotional_scores[EmotionalState.INSPIRED] += 1
        
        if win_rate > 0.7:
            emotional_scores[EmotionalState.ENLIGHTENED] += 2
        
        # Continuidade emocional (tendência a manter estado atual)
        emotional_scores[player.emotional_state] += 1.5
        
        # Retorna estado com maior pontuação
        return max(emotional_scores.items(), key=lambda x: x[1])[0]
    
    def _adapt_ai_parameters(self, player: PlayerProfile, game_result: Dict) -> Dict:
        """Adapta parâmetros da IA baseado no perfil do jogador"""
        adaptations = {}
        
        # Ajusta dificuldade
        if game_result["outcome"] == "win" and game_result.get("accuracy", 0) > 0.9:
            adaptations["difficulty_increase"] = 0.1
        elif game_result["outcome"] == "loss" and game_result.get("accuracy", 0) < 0.5:
            adaptations["difficulty_decrease"] = 0.1
        
        # Ajusta estilo de jogo da IA
        player_moves = game_result.get("move_patterns", {})
        if player_moves:
            adaptations["style_adjustments"] = self._analyze_play_style(player_moves)
        
        # Ajusta baseado no estado emocional
        if player.emotional_state == EmotionalState.FRUSTRATED:
            adaptations["encouragement_mode"] = True
            adaptations["difficulty_decrease"] = 0.05
        elif player.emotional_state == EmotionalState.ENLIGHTENED:
            adaptations["challenge_mode"] = True
            adaptations["complexity_increase"] = 0.1
        
        # Ajusta narrativa
        adaptations["narrative_tone"] = self._get_narrative_tone(player.emotional_state)
        
        return adaptations
    
    def _analyze_play_style(self, move_patterns: Dict) -> Dict:
        """Analisa padrões de movimento para identificar estilo de jogo"""
        style_profile = {
            "aggressive": 0,
            "defensive": 0,
            "tactical": 0,
            "positional": 0,
            "balanced": 0
        }
        
        # Análise simplificada (seria mais complexa em produção)
        if move_patterns.get("captures_percentage", 0) > 0.3:
            style_profile["aggressive"] += 1
        
        if move_patterns.get("king_safety_moves", 0) > 0.2:
            style_profile["defensive"] += 1
        
        if move_patterns.get("tactical_combinations", 0) > 0:
            style_profile["tactical"] += 1
        
        if move_patterns.get("pawn_structure_focus", 0) > 0.4:
            style_profile["positional"] += 1
        
        # Normaliza
        total = sum(style_profile.values()) or 1
        for key in style_profile:
            style_profile[key] /= total
        
        return style_profile
    
    def _get_narrative_tone(self, emotional_state: EmotionalState) -> str:
        """Retorna tom narrativo baseado no estado emocional"""
        tone_map = {
            EmotionalState.CONFIDENT: "triumphant",
            EmotionalState.FOCUSED: "analytical",
            EmotionalState.ANXIOUS: "supportive",
            EmotionalState.DETERMINED: "motivational",
            EmotionalState.ENLIGHTENED: "philosophical",
            EmotionalState.FRUSTRATED: "encouraging",
            EmotionalState.INSPIRED: "poetic"
        }
        return tone_map.get(emotional_state, "neutral")
    
    def _xp_for_next_level(self, level: int) -> int:
        """Calcula XP necessário para próximo nível"""
        return int(100 * (1.5 ** (level - 1)))
    
    def generate_daily_challenges(self, player: PlayerProfile) -> List[Dict]:
        """Gera desafios diários personalizados"""
        challenges = []
        
        # Desafio baseado em fraqueza
        weakest_skill = min(player.skill_levels.items(), 
                           key=lambda x: x[1], 
                           default=(SkillDomain.TACTICS, 0))
        
        challenges.append({
            "id": f"daily_skill_{datetime.now().date()}",
            "title": f"Melhore suas {weakest_skill[0].value}",
            "description": f"Complete 3 exercícios de {weakest_skill[0].value}",
            "reward_xp": 150,
            "reward_rating": 5,
            "progress": 0,
            "target": 3,
            "expires": datetime.now() + timedelta(days=1)
        })
        
        # Desafio cultural
        challenges.append({
            "id": f"daily_cultural_{datetime.now().date()}",
            "title": f"Honre os {player.culture}",
            "description": f"Vença uma partida usando o estilo {player.culture}",
            "reward_xp": 200,
            "cultural_bonus": {player.culture: 2},
            "progress": 0,
            "target": 1,
            "expires": datetime.now() + timedelta(days=1)
        })
        
        # Desafio de consistência
        challenges.append({
            "id": f"daily_consistency_{datetime.now().date()}",
            "title": "Mestre Consistente",
            "description": "Jogue 5 partidas com precisão acima de 80%",
            "reward_xp": 300,
            "reward_rating": 10,
            "progress": 0,
            "target": 5,
            "expires": datetime.now() + timedelta(days=1)
        })
        
        return challenges
    
    def generate_narrative_event(self, player: PlayerProfile, context: Dict) -> Dict:
        """Gera evento narrativo baseado no estado do jogador"""
        event = {
            "type": "narrative",
            "title": "",
            "description": "",
            "choices": [],
            "consequences": {},
            "ink_knot": ""
        }
        
        # Evento baseado no nível
        if player.level % 10 == 0:
            event["title"] = "Marco Importante"
            event["description"] = f"Você alcançou o nível {player.level}. Um novo caminho se abre."
            event["choices"] = [
                {"text": "Buscar novo conhecimento", "consequence": "skill_boost"},
                {"text": "Fortalecer fundamentos", "consequence": "consistency_boost"},
                {"text": "Explorar nova cultura", "consequence": "cultural_unlock"}
            ]
            event["ink_knot"] = "milestone_event"
        
        # Evento baseado em sequência
        elif player.current_streak == 5:
            event["title"] = "Momento de Glória"
            event["description"] = "Sua sequência de vitórias atrai atenção. Como responder?"
            event["choices"] = [
                {"text": "Manter humildade", "consequence": "wisdom_gain"},
                {"text": "Aceitar o desafio maior", "consequence": "elite_opponent"},
                {"text": "Compartilhar conhecimento", "consequence": "mentor_unlock"}
            ]
            event["ink_knot"] = "streak_event"
        
        # Evento cultural
        elif player.cultural_mastery.get(player.culture, 0) >= 50:
            event["title"] = f"Revelação {player.culture}"
            event["description"] = f"Os segredos dos {player.culture} começam a se revelar..."
            event["choices"] = [
                {"text": "Estudar textos antigos", "consequence": "cultural_knowledge"},
                {"text": "Praticar técnica secreta", "consequence": "special_move"},
                {"text": "Meditar sobre a essência", "consequence": "philosophical_insight"}
            ]
            event["ink_knot"] = "cultural_revelation"
        
        return event
    
    def get_player_insights(self, player: PlayerProfile) -> Dict:
        """Gera insights personalizados sobre o progresso do jogador"""
        insights = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "trends": [],
            "predictions": {}
        }
        
        # Análise de forças
        if player.wins / max(1, player.total_games) > 0.6:
            insights["strengths"].append("Taxa de vitória impressionante")
        
        if player.best_streak > 7:
            insights["strengths"].append("Capacidade de manter momentum")
        
        # Análise de fraquezas
        if player.emotional_state == EmotionalState.Frustrated:
            insights["weaknesses"].append("Controle emocional sob pressão")
            insights["recommendations"].append("Pratique meditação antes das partidas")
        
        # Tendências
        if player.current_streak > 3:
            insights["trends"].append("Em ascensão - aproveite o momento!")
        
        # Predições
        games_to_next_level = math.ceil(
            (self._xp_for_next_level(player.level) - player.xp) / 100
        )
        insights["predictions"]["next_level_games"] = games_to_next_level
        
        return insights
