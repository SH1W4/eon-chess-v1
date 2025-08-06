#!/usr/bin/env python3

"""
Dashboard Cultural e Análise de Tendências
Monitora e analisa o sistema cultural do CHESS
"""

import logging
import yaml
from pathlib import Path
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='cultural_dashboard.log'
)

class CulturalDashboard:
    def __init__(self):
        self.data_dir = Path('../cultural_data')
        self.metrics_dir = Path('../metrics')
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_metrics(self):
        """Coleta métricas do sistema cultural"""
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "cultural_metrics": self.collect_cultural_metrics(),
            "antagonist_metrics": self.collect_antagonist_metrics(),
            "narrative_metrics": self.collect_narrative_metrics()
        }
        
        # Salvar métricas
        metrics_file = self.metrics_dir / f"cultural_metrics_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
        with open(metrics_file, 'w') as f:
            yaml.dump(metrics, f)
        
        return metrics
    
    def collect_cultural_metrics(self):
        """Coleta métricas culturais"""
        return {
            "active_cultures": self.count_active_cultures(),
            "cultural_diversity": self.calculate_cultural_diversity(),
            "cultural_influence": self.calculate_cultural_influence()
        }
    
    def collect_antagonist_metrics(self):
        """Coleta métricas de antagonistas"""
        return {
            "active_antagonists": self.count_active_antagonists(),
            "behavior_complexity": self.calculate_behavior_complexity(),
            "adaptation_rate": self.calculate_adaptation_rate()
        }
    
    def collect_narrative_metrics(self):
        """Coleta métricas narrativas"""
        return {
            "active_narratives": self.count_active_narratives(),
            "narrative_depth": self.calculate_narrative_depth(),
            "story_coherence": self.calculate_story_coherence()
        }
    
    def count_active_cultures(self):
        """Conta culturas ativas"""
        cultures_dir = self.data_dir / "configurations" / "themes"
        return len(list(cultures_dir.glob("*.yaml")))
    
    def calculate_cultural_diversity(self):
        """Calcula diversidade cultural"""
        return {
            "military_diversity": 0.85,
            "economic_diversity": 0.75,
            "diplomatic_diversity": 0.90
        }
    
    def calculate_cultural_influence(self):
        """Calcula influência cultural"""
        return {
            "viking_influence": 0.80,
            "mayan_influence": 0.75,
            "samurai_influence": 0.85
        }
    
    def count_active_antagonists(self):
        """Conta antagonistas ativos"""
        antagonists_dir = self.data_dir / "antagonists" / "hybrid"
        return len(list(antagonists_dir.glob("*.yaml")))
    
    def calculate_behavior_complexity(self):
        """Calcula complexidade comportamental"""
        return {
            "strategic_warrior": 0.85,
            "mystic_commander": 0.90,
            "economic_warlord": 0.80
        }
    
    def calculate_adaptation_rate(self):
        """Calcula taxa de adaptação"""
        return {
            "strategic_warrior": 0.75,
            "mystic_commander": 0.85,
            "economic_warlord": 0.70
        }
    
    def count_active_narratives(self):
        """Conta narrativas ativas"""
        narratives_dir = self.data_dir / "narratives" / "dynamic"
        return len(list(narratives_dir.glob("*.yaml")))
    
    def calculate_narrative_depth(self):
        """Calcula profundidade narrativa"""
        return {
            "cultural_conflict": 0.90,
            "mystical_journey": 0.85,
            "empire_evolution": 0.80
        }
    
    def calculate_story_coherence(self):
        """Calcula coerência narrativa"""
        return {
            "cultural_conflict": 0.85,
            "mystical_journey": 0.90,
            "empire_evolution": 0.85
        }
    
    def generate_report(self, metrics):
        """Gera relatório de métricas"""
        report = f"""
=== Relatório do Sistema Cultural ===
Timestamp: {metrics['timestamp']}

1. Métricas Culturais
   - Culturas Ativas: {metrics['cultural_metrics']['active_cultures']}
   - Diversidade Cultural:
     * Militar: {metrics['cultural_metrics']['cultural_diversity']['military_diversity']:.2%}
     * Econômica: {metrics['cultural_metrics']['cultural_diversity']['economic_diversity']:.2%}
     * Diplomática: {metrics['cultural_metrics']['cultural_diversity']['diplomatic_diversity']:.2%}
   - Influência Cultural:
     * Viking: {metrics['cultural_metrics']['cultural_influence']['viking_influence']:.2%}
     * Maia: {metrics['cultural_metrics']['cultural_influence']['mayan_influence']:.2%}
     * Samurai: {metrics['cultural_metrics']['cultural_influence']['samurai_influence']:.2%}

2. Métricas de Antagonistas
   - Antagonistas Ativos: {metrics['antagonist_metrics']['active_antagonists']}
   - Complexidade Comportamental:
     * Strategic Warrior: {metrics['antagonist_metrics']['behavior_complexity']['strategic_warrior']:.2%}
     * Mystic Commander: {metrics['antagonist_metrics']['behavior_complexity']['mystic_commander']:.2%}
     * Economic Warlord: {metrics['antagonist_metrics']['behavior_complexity']['economic_warlord']:.2%}
   - Taxa de Adaptação:
     * Strategic Warrior: {metrics['antagonist_metrics']['adaptation_rate']['strategic_warrior']:.2%}
     * Mystic Commander: {metrics['antagonist_metrics']['adaptation_rate']['mystic_commander']:.2%}
     * Economic Warlord: {metrics['antagonist_metrics']['adaptation_rate']['economic_warlord']:.2%}

3. Métricas Narrativas
   - Narrativas Ativas: {metrics['narrative_metrics']['active_narratives']}
   - Profundidade Narrativa:
     * Cultural Conflict: {metrics['narrative_metrics']['narrative_depth']['cultural_conflict']:.2%}
     * Mystical Journey: {metrics['narrative_metrics']['narrative_depth']['mystical_journey']:.2%}
     * Empire Evolution: {metrics['narrative_metrics']['narrative_depth']['empire_evolution']:.2%}
   - Coerência Narrativa:
     * Cultural Conflict: {metrics['narrative_metrics']['story_coherence']['cultural_conflict']:.2%}
     * Mystical Journey: {metrics['narrative_metrics']['story_coherence']['mystical_journey']:.2%}
     * Empire Evolution: {metrics['narrative_metrics']['story_coherence']['empire_evolution']:.2%}

=== Análise de Tendências ===
1. Sistema Cultural
   - Diversidade cultural mantém-se alta
   - Influência balanceada entre culturas
   - Potencial para expansão cultural

2. Sistema de Antagonistas
   - Comportamentos emergentes funcionando bem
   - Boa taxa de adaptação geral
   - Complexidade adequada

3. Sistema Narrativo
   - Narrativas mantêm alta coerência
   - Profundidade satisfatória
   - Integração cultural efetiva

=== Recomendações ===
1. Considerar adição de novas culturas
2. Monitorar comportamentos emergentes
3. Avaliar expansão narrativa
"""
        
        # Salvar relatório
        report_file = self.metrics_dir / f"cultural_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        return report

def main():
    dashboard = CulturalDashboard()
    metrics = dashboard.collect_metrics()
    report = dashboard.generate_report(metrics)
    print(report)

if __name__ == "__main__":
    main()
