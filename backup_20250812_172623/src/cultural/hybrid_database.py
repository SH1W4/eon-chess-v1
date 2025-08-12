from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path
from enum import Enum
import sqlite3
import pandas as pd

class GameType(Enum):
    HISTORICAL = "historical"  # Partida histórica real
    SIMULATED = "simulated"   # Partida simulada
    HYBRID = "hybrid"         # Partida histórica com variações culturais

@dataclass
class ChessGame:
    """Representação de uma partida de xadrez"""
    game_id: str
    white_player: str
    black_player: str
    game_type: GameType
    moves: List[str]
    result: str
    date: datetime
    cultural_context: Dict[str, Any] = field(default_factory=dict)
    simulation_params: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class HybridDatabase:
    """Sistema de base de dados híbrida para partidas reais e simuladas"""
    def __init__(self, db_path: str = "data/hybrid_chess.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Inicializa a estrutura do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela principal de jogos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            white_player TEXT,
            black_player TEXT,
            game_type TEXT,
            moves TEXT,
            result TEXT,
            date TEXT,
            cultural_context TEXT,
            simulation_params TEXT,
            metadata TEXT
        )
        """)

        # Índices para otimização
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_players ON games(white_player, black_player)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_type ON games(game_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON games(date)")

        conn.commit()
        conn.close()

    def add_game(self, game: ChessGame):
        """Adiciona uma nova partida ao banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO games VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game.game_id,
            game.white_player,
            game.black_player,
            game.game_type.value,
            json.dumps(game.moves),
            game.result,
            game.date.isoformat(),
            json.dumps(game.cultural_context),
            json.dumps(game.simulation_params),
            json.dumps(game.metadata)
        ))

        conn.commit()
        conn.close()

    def get_game(self, game_id: str) -> Optional[ChessGame]:
        """Recupera uma partida específica"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return ChessGame(
            game_id=row[0],
            white_player=row[1],
            black_player=row[2],
            game_type=GameType(row[3]),
            moves=json.loads(row[4]),
            result=row[5],
            date=datetime.fromisoformat(row[6]),
            cultural_context=json.loads(row[7]),
            simulation_params=json.loads(row[8]),
            metadata=json.loads(row[9])
        )

    def find_games(self, **filters) -> List[ChessGame]:
        """Busca partidas com filtros específicos"""
        conn = sqlite3.connect(self.db_path)
        
        # Constrói a query baseada nos filtros
        query = "SELECT * FROM games WHERE 1=1"
        params = []
        
        if 'player' in filters:
            query += " AND (white_player = ? OR black_player = ?)"
            params.extend([filters['player'], filters['player']])
        
        if 'game_type' in filters:
            query += " AND game_type = ?"
            params.append(filters['game_type'].value)
        
        if 'date_from' in filters:
            query += " AND date >= ?"
            params.append(filters['date_from'].isoformat())
        
        if 'date_to' in filters:
            query += " AND date <= ?"
            params.append(filters['date_to'].isoformat())

        # Executa a query
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        # Converte resultados para objetos ChessGame
        games = []
        for _, row in df.iterrows():
            games.append(ChessGame(
                game_id=row['game_id'],
                white_player=row['white_player'],
                black_player=row['black_player'],
                game_type=GameType(row['game_type']),
                moves=json.loads(row['moves']),
                result=row['result'],
                date=datetime.fromisoformat(row['date']),
                cultural_context=json.loads(row['cultural_context']),
                simulation_params=json.loads(row['simulation_params']),
                metadata=json.loads(row['metadata'])
            ))

        return games

    def get_player_stats(self, player_name: str) -> Dict[str, Any]:
        """Retorna estatísticas de um jogador"""
        conn = sqlite3.connect(self.db_path)
        
        # Estatísticas gerais
        stats = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'by_game_type': {},
            'historical_opponents': set(),
            'simulated_opponents': set()
        }
        
        # Carrega dados em um DataFrame
        df = pd.read_sql_query("""
            SELECT * FROM games 
            WHERE white_player = ? OR black_player = ?
        """, conn, params=[player_name, player_name])
        
        for _, game in df.iterrows():
            stats['total_games'] += 1
            
            # Contabiliza resultado
            is_white = game['white_player'] == player_name
            if game['result'] == '1-0':
                stats['wins' if is_white else 'losses'] += 1
            elif game['result'] == '0-1':
                stats['losses' if is_white else 'wins'] += 1
            else:
                stats['draws'] += 1
            
            # Estatísticas por tipo de jogo
            game_type = game['game_type']
            if game_type not in stats['by_game_type']:
                stats['by_game_type'][game_type] = {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0}
            
            stats['by_game_type'][game_type]['games'] += 1
            
            # Registra oponentes
            opponent = game['black_player'] if is_white else game['white_player']
            if game_type == GameType.HISTORICAL.value:
                stats['historical_opponents'].add(opponent)
            else:
                stats['simulated_opponents'].add(opponent)
        
        conn.close()
        
        # Converte sets para listas para serialização
        stats['historical_opponents'] = list(stats['historical_opponents'])
        stats['simulated_opponents'] = list(stats['simulated_opponents'])
        
        return stats

    def export_to_pgn(self, game_id: str, output_path: str):
        """Exporta uma partida para formato PGN"""
        game = self.get_game(game_id)
        if not game:
            return False
        
        pgn = f'''[Event "{'Historical Game' if game.game_type == GameType.HISTORICAL else 'Simulated Game'}"]
[Site "Hybrid Database"]
[Date "{game.date.strftime('%Y.%m.%d')}"]
[White "{game.white_player}"]
[Black "{game.black_player}"]
[Result "{game.result}"]
[GameType "{game.game_type.value}"]

{" ".join(game.moves)}
{game.result}
'''
        
        with open(output_path, 'w') as f:
            f.write(pgn)
        
        return True

    def import_from_pgn(self, pgn_path: str, game_type: GameType = GameType.HISTORICAL):
        """Importa partidas de um arquivo PGN"""
        # Implementar parser PGN aqui
        pass
