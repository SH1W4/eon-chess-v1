from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from hybrid_database import HybridDatabase, ChessGame, GameType
from advanced_ring import HistoricalRing, HistoricalLeader
from ring_system import ChessRing

class HybridRingIntegrator:
    """Integrador entre sistema de ring e base de dados híbrida"""
    def __init__(self, database_path: str = "data/hybrid_chess.db"):
        self.database = HybridDatabase(database_path)
        self.historical_ring = HistoricalRing()
        self.chess_ring = ChessRing()
        
    def register_historical_game(self, 
                               white_player: str, 
                               black_player: str,
                               moves: List[str],
                               result: str,
                               date: datetime,
                               metadata: Dict[str, Any] = None):
        """Registra uma partida histórica"""
        game_id = str(uuid.uuid4())
        
        game = ChessGame(
            game_id=game_id,
            white_player=white_player,
            black_player=black_player,
            game_type=GameType.HISTORICAL,
            moves=moves,
            result=result,
            date=date,
            metadata=metadata or {}
        )
        
        self.database.add_game(game)
        return game_id
        
    def simulate_match(self,
                      white_player: str,
                      black_player: str,
                      rounds: int = 50,
                      cultural_context: Dict[str, Any] = None) -> str:
        """Simula uma partida entre dois jogadores e registra no banco"""
        # Garante que os jogadores existem no ring
        if white_player not in self.historical_ring.leaders:
            self.historical_ring.add_leader(white_player, "Player", "Unknown")
        if black_player not in self.historical_ring.leaders:
            self.historical_ring.add_leader(black_player, "Player", "Unknown")
            
        # Simula a partida
        match_data = self.historical_ring.simulate_battle(white_player, black_player, rounds)
        
        # Converte dados da simulação para formato de jogo
        game_id = str(uuid.uuid4())
        moves = []
        result = "1-0" if match_data['final_stats']['leader1']['victories'] > match_data['final_stats']['leader2']['victories'] else (
            "0-1" if match_data['final_stats']['leader1']['victories'] < match_data['final_stats']['leader2']['victories'] else "1/2-1/2"
        )
        
        # Registra cada round como um movimento
        for round_data in match_data['rounds']:
            moves.append(f"{round_data['leader1_behavior']} vs {round_data['leader2_behavior']}")
        
        game = ChessGame(
            game_id=game_id,
            white_player=white_player,
            black_player=black_player,
            game_type=GameType.SIMULATED,
            moves=moves,
            result=result,
            date=datetime.now(),
            cultural_context=cultural_context or {},
            simulation_params={
                'rounds': rounds,
                'final_stats': match_data['final_stats']
            }
        )
        
        self.database.add_game(game)
        return game_id
    
    def create_cultural_variation(self,
                                original_game_id: str,
                                cultural_modifiers: Dict[str, Any]) -> Optional[str]:
        """Cria uma variação cultural de uma partida existente"""
        original_game = self.database.get_game(original_game_id)
        if not original_game:
            return None
            
        # Cria nova partida com modificações culturais
        game_id = str(uuid.uuid4())
        
        # Aplica modificadores culturais
        cultural_context = original_game.cultural_context.copy()
        cultural_context.update(cultural_modifiers)
        
        # Simula nova partida com contexto cultural modificado
        match_data = self.historical_ring.simulate_battle(
            original_game.white_player,
            original_game.black_player,
            rounds=len(original_game.moves)
        )
        
        # Registra nova partida como variação híbrida
        game = ChessGame(
            game_id=game_id,
            white_player=original_game.white_player,
            black_player=original_game.black_player,
            game_type=GameType.HYBRID,
            moves=match_data['rounds'],
            result=match_data['final_stats']['winner'] if 'winner' in match_data['final_stats'] else "1/2-1/2",
            date=datetime.now(),
            cultural_context=cultural_context,
            simulation_params={
                'original_game_id': original_game_id,
                'cultural_modifiers': cultural_modifiers,
                'final_stats': match_data['final_stats']
            },
            metadata={
                'variation_type': 'cultural',
                'based_on': original_game_id
            }
        )
        
        self.database.add_game(game)
        return game_id
    
    def analyze_player_evolution(self, player_name: str) -> Dict[str, Any]:
        """Analisa a evolução de um jogador através de partidas históricas e simuladas"""
        stats = self.database.get_player_stats(player_name)
        
        # Análise temporal
        historical_games = self.database.find_games(
            player=player_name,
            game_type=GameType.HISTORICAL
        )
        
        simulated_games = self.database.find_games(
            player=player_name,
            game_type=GameType.SIMULATED
        )
        
        # Organiza jogos por período
        historical_by_period = {}
        simulated_by_period = {}
        
        for game in historical_games:
            year = game.date.year
            if year not in historical_by_period:
                historical_by_period[year] = []
            historical_by_period[year].append(game)
            
        for game in simulated_games:
            year = game.date.year
            if year not in simulated_by_period:
                simulated_by_period[year] = []
            simulated_by_period[year].append(game)
        
        # Análise de evolução
        evolution_analysis = {
            'historical_progression': {
                year: {
                    'games': len(games),
                    'win_rate': sum(1 for g in games if 
                        (g.white_player == player_name and g.result == '1-0') or
                        (g.black_player == player_name and g.result == '0-1')
                    ) / len(games) if games else 0
                }
                for year, games in historical_by_period.items()
            },
            'simulated_progression': {
                year: {
                    'games': len(games),
                    'win_rate': sum(1 for g in games if 
                        (g.white_player == player_name and g.result == '1-0') or
                        (g.black_player == player_name and g.result == '0-1')
                    ) / len(games) if games else 0
                }
                for year, games in simulated_by_period.items()
            },
            'cultural_adaptability': {
                'historical_styles': self._analyze_cultural_styles(historical_games),
                'simulated_styles': self._analyze_cultural_styles(simulated_games)
            }
        }
        
        return evolution_analysis
    
    def _analyze_cultural_styles(self, games: List[ChessGame]) -> Dict[str, Any]:
        """Analisa estilos culturais em um conjunto de jogos"""
        styles = {
            'aggressive': 0,
            'defensive': 0,
            'strategic': 0,
            'diplomatic': 0
        }
        
        for game in games:
            context = game.cultural_context
            if 'dominant_style' in context:
                style = context['dominant_style'].lower()
                if style in styles:
                    styles[style] += 1
        
        total = sum(styles.values()) or 1
        return {
            'style_distribution': {
                style: count / total
                for style, count in styles.items()
            },
            'total_games_analyzed': total
        }
