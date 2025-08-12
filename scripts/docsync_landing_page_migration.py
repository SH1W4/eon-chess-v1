#!/usr/bin/env python3
"""
DOCSYNC - Script de Migração e Adaptação de Landing Page
Reutiliza elementos do github-mastery para o projeto chess
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class LandingPageMigrator:
    def __init__(self, source_project, target_project):
        self.source_project = source_project
        self.target_project = target_project
        self.migration_map = {
            'colors': {
                '#111827': '#1a1a2e',  # Fundo escuro mais azulado para xadrez
                '#1f2937': '#16213e',  # Secundário
                '#3b82f6': '#0f4c75',  # Azul principal
                '#60a5fa': '#3282b8',  # Azul claro
                '#9ca3af': '#e8e8e8',  # Texto secundário
            },
            'content': {
                'title': 'ChessMaster',
                'subtitle': 'Domine o Jogo dos Reis com IA',
                'description': 'Sistema avançado de xadrez com análise por inteligência artificial, aprendizado adaptativo e torneios online.',
                'features': [
                    {
                        'title': 'Análise por IA',
                        'description': 'Motor de xadrez com deep learning para análise de posições e sugestões de jogadas',
                        'icon': '♔'
                    },
                    {
                        'title': 'Aprendizado Adaptativo',
                        'description': 'Sistema que se adapta ao seu nível e estilo de jogo',
                        'icon': '♗'
                    },
                    {
                        'title': 'Torneios Online',
                        'description': 'Participe de torneios e competições com jogadores de todo o mundo',
                        'icon': '♘'
                    },
                    {
                        'title': 'Análise de Partidas',
                        'description': 'Revise suas partidas com comentários detalhados da IA',
                        'icon': '♖'
                    },
                    {
                        'title': 'Biblioteca de Aberturas',
                        'description': 'Acesso a milhares de aberturas e variantes catalogadas',
                        'icon': '♕'
                    },
                    {
                        'title': 'Treinamento Tático',
                        'description': 'Puzzles e exercícios táticos personalizados',
                        'icon': '♙'
                    }
                ]
            }
        }
        
    def adapt_html_content(self, html_content):
        """Adapta o conteúdo HTML para o projeto chess"""
        # Substituir cores
        for old_color, new_color in self.migration_map['colors'].items():
            html_content = html_content.replace(old_color, new_color)
        
        # Substituir título e descrições
        html_content = html_content.replace('GitHub Mastery', self.migration_map['content']['title'])
        html_content = html_content.replace('Domine o GitHub como um profissional', self.migration_map['content']['subtitle'])
        
        # Adaptar o conteúdo específico
        html_content = self._adapt_features_section(html_content)
        html_content = self._add_chess_specific_elements(html_content)
        
        return html_content
    
    def _adapt_features_section(self, html_content):
        """Adapta a seção de recursos para xadrez"""
        # Criar novo HTML para features
        features_html = ''
        for feature in self.migration_map['content']['features']:
            features_html += f'''
                <div class="feature-card">
                    <div class="feature-icon">{feature['icon']}</div>
                    <h3>{feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>
            '''
        
        # Encontrar e substituir a seção de features
        features_pattern = r'<div class="features-grid">.*?</div>\s*</div>'
        replacement = f'<div class="features-grid">{features_html}</div>'
        
        return re.sub(features_pattern, replacement, html_content, flags=re.DOTALL)
    
    def _add_chess_specific_elements(self, html_content):
        """Adiciona elementos específicos do xadrez"""
        chess_styles = '''
        <style>
            /* Estilos específicos para xadrez */
            .chessboard-preview {
                width: 300px;
                height: 300px;
                margin: 2rem auto;
                background: repeating-conic-gradient(#e8e8e8 0% 25%, #1a1a2e 0% 50%) 50% / 75px 75px;
                border: 2px solid #0f4c75;
                border-radius: 8px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }
            
            .chess-piece {
                font-size: 32px;
                position: absolute;
                animation: float 3s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
            
            .feature-icon {
                font-size: 48px;
                margin-bottom: 1rem;
                color: #3282b8;
            }
            
            .game-modes {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 3rem;
            }
            
            .game-mode-card {
                background: rgba(22, 33, 62, 0.5);
                border: 1px solid #3282b8;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .game-mode-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(50, 130, 184, 0.3);
            }
        </style>
        '''
        
        # Adicionar tabuleiro de preview na hero section
        chessboard_html = '''
        <div class="chessboard-preview">
            <div class="chess-piece" style="top: 10%; left: 10%;">♔</div>
            <div class="chess-piece" style="top: 20%; left: 80%;">♕</div>
            <div class="chess-piece" style="top: 70%; left: 30%;">♘</div>
            <div class="chess-piece" style="top: 80%; left: 60%;">♗</div>
        </div>
        '''
        
        # Adicionar seção de modos de jogo
        game_modes_html = '''
        <section class="game-modes-section">
            <div class="container">
                <h2>Modos de Jogo</h2>
                <div class="game-modes">
                    <div class="game-mode-card">
                        <h3>Blitz</h3>
                        <p>3-5 minutos por jogador</p>
                    </div>
                    <div class="game-mode-card">
                        <h3>Rápidas</h3>
                        <p>10-15 minutos por jogador</p>
                    </div>
                    <div class="game-mode-card">
                        <h3>Clássicas</h3>
                        <p>30+ minutos por jogador</p>
                    </div>
                    <div class="game-mode-card">
                        <h3>Puzzles</h3>
                        <p>Resolva problemas táticos</p>
                    </div>
                </div>
            </div>
        </section>
        '''
        
        # Inserir os novos elementos
        html_content = html_content.replace('</head>', f'{chess_styles}</head>')
        html_content = html_content.replace('</h1>', f'</h1>{chessboard_html}')
        html_content = html_content.replace('</main>', f'{game_modes_html}</main>')
        
        return html_content
    
    def adapt_javascript(self, js_content):
        """Adapta o JavaScript para funcionalidades de xadrez"""
        # Adicionar funcionalidades específicas de xadrez
        chess_js = '''
        // Funcionalidades específicas do ChessMaster
        class ChessFeatures {
            constructor() {
                this.initChessAnimations();
                this.initGameModeSelection();
            }
            
            initChessAnimations() {
                // Animação das peças no preview
                const pieces = document.querySelectorAll('.chess-piece');
                pieces.forEach((piece, index) => {
                    piece.style.animationDelay = `${index * 0.5}s`;
                });
            }
            
            initGameModeSelection() {
                const gameModes = document.querySelectorAll('.game-mode-card');
                gameModes.forEach(mode => {
                    mode.addEventListener('click', function() {
                        // Destacar modo selecionado
                        gameModes.forEach(m => m.classList.remove('selected'));
                        this.classList.add('selected');
                        
                        // Adicionar ao lead scoring
                        if (window.leadScoring) {
                            window.leadScoring.updateScore('gameMode', 10);
                        }
                    });
                });
            }
        }
        
        // Inicializar funcionalidades de xadrez
        document.addEventListener('DOMContentLoaded', () => {
            new ChessFeatures();
        });
        '''
        
        return js_content + '\n\n' + chess_js
    
    def adapt_lead_scoring(self, scoring_content):
        """Adapta o sistema de lead scoring para xadrez"""
        # Modificar critérios de scoring para xadrez
        chess_scoring = '''
        // Critérios específicos para ChessMaster
        const chessInterests = {
            'iniciante': { score: 15, category: 'learner' },
            'intermediário': { score: 25, category: 'player' },
            'avançado': { score: 35, category: 'master' },
            'torneios': { score: 30, category: 'competitive' },
            'análise': { score: 25, category: 'analytical' },
            'ensino': { score: 20, category: 'teacher' }
        };
        
        // Adicionar aos critérios existentes
        Object.assign(this.scoringCriteria.interests, chessInterests);
        '''
        
        # Inserir após a definição de scoringCriteria
        pattern = r'(this\.scoringCriteria = {[^}]+})'
        replacement = r'\1\n' + chess_scoring
        
        return re.sub(pattern, replacement, scoring_content, flags=re.DOTALL)
    
    def migrate_landing_page(self):
        """Executa a migração completa da landing page"""
        print("🔄 Iniciando migração da landing page com DOCSYNC...")
        
        # Caminhos dos arquivos
        source_path = Path(self.source_project) / 'landing-page'
        target_path = Path(self.target_project) / 'landing-page'
        
        # Migrar HTML
        print("📄 Adaptando HTML...")
        with open(source_path / 'index.html', 'r') as f:
            html_content = f.read()
        
        adapted_html = self.adapt_html_content(html_content)
        
        with open(target_path / 'index.html', 'w') as f:
            f.write(adapted_html)
        
        # Migrar JavaScript principal
        print("📜 Adaptando JavaScript...")
        with open(source_path / 'js/app.js', 'r') as f:
            js_content = f.read()
        
        adapted_js = self.adapt_javascript(js_content)
        
        with open(target_path / 'js/app.js', 'w') as f:
            f.write(adapted_js)
        
        # Migrar Lead Scoring
        print("🎯 Adaptando sistema de lead scoring...")
        with open(source_path / 'js/lead-scoring.js', 'r') as f:
            scoring_content = f.read()
        
        adapted_scoring = self.adapt_lead_scoring(scoring_content)
        
        with open(target_path / 'js/lead-scoring.js', 'w') as f:
            f.write(adapted_scoring)
        
        # Criar arquivo de metadados da migração
        migration_metadata = {
            'source': str(source_path),
            'target': str(target_path),
            'timestamp': datetime.now().isoformat(),
            'adaptations': {
                'colors': self.migration_map['colors'],
                'content_changes': len(self.migration_map['content']['features']),
                'new_elements': ['chessboard-preview', 'game-modes-section']
            }
        }
        
        with open(target_path / '.migration-metadata.json', 'w') as f:
            json.dump(migration_metadata, f, indent=2)
        
        print("✅ Migração concluída com sucesso!")
        print(f"📁 Arquivos criados em: {target_path}")
        
        return True

# Executar migração
if __name__ == "__main__":
    source = "/Users/jx/Desktop/github_mastery"
    target = "/Users/jx/WORKSPACE/PROJECTS/CHESS"
    
    migrator = LandingPageMigrator(source, target)
    migrator.migrate_landing_page()
