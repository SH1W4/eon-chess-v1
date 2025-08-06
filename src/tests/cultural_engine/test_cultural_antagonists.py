"""
Testes para o sistema de antagonistas culturais
"""
import pytest
from cultural.culture_framework import ChessCulture
from cultural.style_analyzer import CulturalStyleAnalyzer
from cultural.memory import CulturalMemory

class TestAntagonistProfiles:
    """Testes para perfis de antagonistas"""
    
    @pytest.fixture
    def memory(self):
        """Fixture para memória cultural"""
        return CulturalMemory()
    
    @pytest.fixture
    def analyzer(self):
        """Fixture para analisador de estilo"""
        return CulturalStyleAnalyzer()
    
    def test_mongol_antagonist(self, memory, analyzer):
        """Testa perfil do antagonista mongol"""
        # Configurar perfil mongol
        mongol_profile = {
            "name": "Khan",
            "era": "1206-1368 D.C.",
            "style": {
                "aggression": 0.9,
                "mobility": 0.95,
                "tactical": 0.85
            },
            "characteristics": [
                "Mobilidade extrema",
                "Ataques coordenados",
                "Táticas de cerco"
            ]
        }
        
        # Simular contexto de jogo
        context = {
            "piece_mobility": 0.8,
            "attack_coordination": 0.85,
            "tactical_advantage": 0.75
        }
        
        # Analisar comportamento
        analysis = analyzer.analyze_antagonist_behavior(mongol_profile, context)
        
        # Verificar características esperadas
        assert analysis.aggression_level >= 0.8
        assert analysis.mobility_score >= 0.9
        assert analysis.tactical_rating >= 0.8
        
        # Verificar adaptação cultural
        cultural_fit = analyzer.evaluate_cultural_fit(analysis, "mongol")
        assert cultural_fit >= 0.85
    
    def test_byzantine_antagonist(self, memory, analyzer):
        """Testa perfil do antagonista bizantino"""
        # Configurar perfil bizantino
        byzantine_profile = {
            "name": "Basileus",
            "era": "330-1453 D.C.",
            "style": {
                "defense": 0.95,
                "diplomacy": 0.90,
                "strategy": 0.85
            },
            "characteristics": [
                "Defesa em profundidade",
                "Contra-ataques calculados",
                "Manobras diplomáticas"
            ]
        }
        
        # Simular contexto de jogo
        context = {
            "defensive_formation": 0.9,
            "counter_attack_opportunity": 0.8,
            "strategic_advantage": 0.85
        }
        
        # Analisar comportamento
        analysis = analyzer.analyze_antagonist_behavior(byzantine_profile, context)
        
        # Verificar características esperadas
        assert analysis.defense_level >= 0.9
        assert analysis.strategic_score >= 0.8
        assert analysis.counter_attack_rating >= 0.8
        
        # Verificar adaptação cultural
        cultural_fit = analyzer.evaluate_cultural_fit(analysis, "byzantine")
        assert cultural_fit >= 0.85
    
    def test_modern_antagonist(self, memory, analyzer):
        """Testa perfil de antagonista moderno (Kasparov)"""
        # Configurar perfil Kasparov
        kasparov_profile = {
            "name": "Agressivo Dinâmico",
            "style": {
                "aggression": 0.95,
                "calculation": 0.90,
                "pressure": 0.85
            },
            "characteristics": [
                "Ataques diretos ao rei",
                "Sacrifícios posicionais",
                "Pressão psicológica constante"
            ]
        }
        
        # Simular contexto de jogo
        context = {
            "attacking_chances": 0.9,
            "tactical_complexity": 0.85,
            "position_dynamics": 0.9
        }
        
        # Analisar comportamento
        analysis = analyzer.analyze_antagonist_behavior(kasparov_profile, context)
        
        # Verificar características esperadas
        assert analysis.aggression_level >= 0.9
        assert analysis.tactical_score >= 0.85
        assert analysis.dynamic_rating >= 0.85
        
        # Verificar adaptação ao estilo moderno
        style_fit = analyzer.evaluate_style_fit(analysis, "modern_aggressive")
        assert style_fit >= 0.85
    
    def test_cultural_antagonist(self, memory, analyzer):
        """Testa perfil de antagonista cultural (Samurai)"""
        # Configurar perfil Samurai
        samurai_profile = {
            "name": "Samurai",
            "culture": "Japonesa Feudal",
            "style": {
                "honor": 0.95,
                "discipline": 0.90,
                "technique": 0.85
            },
            "characteristics": [
                "Ataques precisos",
                "Sacrifícios honoráveis",
                "Disciplina rigorosa"
            ]
        }
        
        # Simular contexto de jogo
        context = {
            "technical_precision": 0.9,
            "positional_discipline": 0.85,
            "tactical_sacrifice": 0.8
        }
        
        # Analisar comportamento
        analysis = analyzer.analyze_antagonist_behavior(samurai_profile, context)
        
        # Verificar características esperadas
        assert analysis.precision_level >= 0.85
        assert analysis.discipline_score >= 0.85
        assert analysis.honor_rating >= 0.9
        
        # Verificar expressão cultural
        cultural_expression = analyzer.evaluate_cultural_expression(analysis, "samurai")
        assert cultural_expression >= 0.85
    
    def test_antagonist_adaptation(self, memory, analyzer):
        """Testa adaptação do antagonista ao estilo do jogador"""
        # Configurar perfil inicial
        initial_profile = {
            "name": "Adaptativo",
            "style": {
                "aggression": 0.5,
                "defense": 0.5,
                "tactical": 0.5
            }
        }
        
        # Simular histórico de jogador agressivo
        player_history = {
            "style": "aggressive",
            "moves": [
                {"type": "attack", "success": True},
                {"type": "sacrifice", "success": True},
                {"type": "pressure", "success": True}
            ]
        }
        
        # Adaptar perfil
        adapted_profile = analyzer.adapt_antagonist_profile(
            initial_profile,
            player_history
        )
        
        # Verificar adaptação
        assert adapted_profile.style["defense"] > initial_profile["style"]["defense"]
        assert adapted_profile.counter_measures["aggressive"] >= 0.7
        
    def test_narrative_generation(self, memory, analyzer):
        """Testa geração de narrativas do antagonista"""
        # Configurar perfil
        profile = {
            "name": "Vizir",
            "culture": "Persa Clássica",
            "narratives": [
                "Com a sabedoria dos antigos reis",
                "Seguindo as tradições do shatranj",
                "Como nos jardins de Persépolis"
            ]
        }
        
        # Simular evento
        event = {
            "type": "strategic_move",
            "context": "middle_game",
            "importance": "high"
        }
        
        # Gerar narrativa
        narrative = analyzer.generate_antagonist_narrative(profile, event)
        
        # Verificar qualidade da narrativa
        assert len(narrative) > 0
        assert any(template in narrative for template in profile["narratives"])
        assert analyzer.evaluate_narrative_quality(narrative) >= 0.8
    
    def test_antagonist_evolution(self, memory, analyzer):
        """Testa evolução do antagonista ao longo do tempo"""
        # Configurar perfil inicial
        initial_profile = {
            "name": "Evolutivo",
            "learning_rate": 0.05,
            "adaptation_threshold": 0.7,
            "metrics": {
                "success_rate": 0.5,
                "adaptation_score": 0.5,
                "complexity": 0.5
            }
        }
        
        # Simular série de jogos
        game_results = [
            {"outcome": "win", "performance": 0.8},
            {"outcome": "loss", "performance": 0.6},
            {"outcome": "win", "performance": 0.9}
        ]
        
        # Evoluir perfil
        evolved_profile = analyzer.evolve_antagonist_profile(
            initial_profile,
            game_results
        )
        
        # Verificar evolução
        assert evolved_profile.metrics["success_rate"] > initial_profile["metrics"]["success_rate"]
        assert evolved_profile.metrics["adaptation_score"] > initial_profile["metrics"]["adaptation_score"]
        assert evolved_profile.complexity_level > initial_profile["metrics"]["complexity"]
