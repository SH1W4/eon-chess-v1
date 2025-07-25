"""
Módulo de integração com Lichess e visualização de dados.
"""
import chess
import chess.pgn
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional
import networkx as nx
from dataclasses import dataclass
import io

@dataclass
class GameMetrics:
    """Métricas de uma partida."""
    moves: int
    material_balance: List[float]
    position_scores: List[float]
    piece_activity: List[float]
    tactical_opportunities: List[int]
    strategic_patterns: List[str]

class LichessIntegration:
    """Integração com a API do Lichess."""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Inicializa integração com Lichess.
        
        Args:
            api_token: Token de API do Lichess (opcional)
        """
        self.api_base = "https://lichess.org/api"
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
    
    def get_master_games(self, 
                        opening: Optional[str] = None,
                        player: Optional[str] = None,
                        max_games: int = 100) -> List[Dict]:
        """
        Obtém partidas da base de mestres.
        
        Args:
            opening: ECO ou nome da abertura
            player: Nome do jogador
            max_games: Número máximo de partidas
        
        Returns:
            Lista de partidas
        """
        params = {"max": max_games}
        if opening:
            params["opening"] = opening
        if player:
            params["player"] = player
        
        response = requests.get(
            f"{self.api_base}/games/master",
            params=params,
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")
        
        return self._parse_pgn(response.text)
    
    def _parse_pgn(self, pgn_text: str) -> List[Dict]:
        """Processa texto PGN em lista de partidas."""
        games = []
        pgn = io.StringIO(pgn_text)
        
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            
            games.append({
                'event': game.headers.get('Event'),
                'white': game.headers.get('White'),
                'black': game.headers.get('Black'),
                'result': game.headers.get('Result'),
                'eco': game.headers.get('ECO'),
                'moves': list(game.mainline_moves())
            })
        
        return games

class ChessVisualizer:
    """Visualizador de dados de xadrez."""
    
    def create_opening_tree(self, games: List[Dict]) -> go.Figure:
        """
        Cria árvore de aberturas.
        
        Args:
            games: Lista de partidas
        
        Returns:
            Figura Plotly
        """
        # Constrói grafo
        G = nx.DiGraph()
        for game in games:
            board = chess.Board()
            prev_fen = board.fen()
            
            for move in game['moves'][:10]:  # Primeiros 10 lances
                board.push(move)
                curr_fen = board.fen()
                
                if not G.has_edge(prev_fen, curr_fen):
                    G.add_edge(prev_fen, curr_fen, weight=0)
                G[prev_fen][curr_fen]['weight'] += 1
                
                prev_fen = curr_fen
        
        # Cria layout
        pos = nx.spring_layout(G)
        
        # Cria visualização
        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=[], y=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                )
            ))

        # Adiciona edges
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        # Adiciona nodes
        node_trace['x'] = [pos[node][0] for node in G.nodes()]
        node_trace['y'] = [pos[node][1] for node in G.nodes()]
        
        # Cria figura
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Árvore de Aberturas',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
        
        return fig
    
    def plot_material_balance(self, metrics: GameMetrics) -> go.Figure:
        """
        Plota balanço material ao longo da partida.
        
        Args:
            metrics: Métricas da partida
        
        Returns:
            Figura Plotly
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=metrics.material_balance,
            mode='lines+markers',
            name='Material Balance',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Material Balance Over Time',
            xaxis_title='Move Number',
            yaxis_title='Material Advantage (pawns)',
            showlegend=True
        )
        
        return fig
    
    def plot_position_evolution(self, metrics: GameMetrics) -> go.Figure:
        """
        Plota evolução posicional da partida.
        
        Args:
            metrics: Métricas da partida
        
        Returns:
            Figura Plotly
        """
        fig = go.Figure()
        
        # Score
        fig.add_trace(go.Scatter(
            y=metrics.position_scores,
            mode='lines',
            name='Position Score',
            line=dict(color='green', width=2)
        ))
        
        # Activity
        fig.add_trace(go.Scatter(
            y=metrics.piece_activity,
            mode='lines',
            name='Piece Activity',
            line=dict(color='red', width=2)
        ))
        
        # Tactical opportunities
        fig.add_trace(go.Scatter(
            y=metrics.tactical_opportunities,
            mode='markers',
            name='Tactical Opportunities',
            marker=dict(
                size=10,
                color='yellow',
                symbol='star'
            )
        ))
        
        fig.update_layout(
            title='Position Evolution',
            xaxis_title='Move Number',
            yaxis_title='Score',
            showlegend=True
        )
        
        return fig
    
    def create_pattern_heatmap(self, metrics: GameMetrics) -> go.Figure:
        """
        Cria heatmap de padrões estratégicos.
        
        Args:
            metrics: Métricas da partida
        
        Returns:
            Figura Plotly
        """
        # Conta ocorrências de padrões
        pattern_counts = pd.Series(metrics.strategic_patterns).value_counts()
        
        # Cria matriz para heatmap
        matrix = pattern_counts.values.reshape(-1, 1)
        
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=['Frequency'],
            y=pattern_counts.index,
            colorscale='Viridis'
        ))
        
        fig.update_layout(
            title='Strategic Pattern Distribution',
            xaxis_title='',
            yaxis_title='Pattern Type',
            showlegend=False
        )
        
        return fig
    
    def create_dashboard(self, metrics: GameMetrics) -> go.Figure:
        """
        Cria dashboard completo da partida.
        
        Args:
            metrics: Métricas da partida
        
        Returns:
            Figura Plotly
        """
        fig = go.Figure()
        
        # Material balance subplot
        fig.add_trace(go.Scatter(
            y=metrics.material_balance,
            name='Material',
            xaxis='x1',
            yaxis='y1'
        ))
        
        # Position score subplot
        fig.add_trace(go.Scatter(
            y=metrics.position_scores,
            name='Position',
            xaxis='x2',
            yaxis='y2'
        ))
        
        # Pattern heatmap subplot
        pattern_counts = pd.Series(metrics.strategic_patterns).value_counts()
        fig.add_trace(go.Heatmap(
            z=[pattern_counts.values],
            y=[pattern_counts.index],
            name='Patterns',
            xaxis='x3',
            yaxis='y3'
        ))
        
        # Update layout
        fig.update_layout(
            title='Game Analysis Dashboard',
            grid=dict(
                rows=2,
                columns=2,
                pattern='independent'
            ),
            showlegend=True
        )
        
        return fig
