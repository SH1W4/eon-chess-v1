#!/usr/bin/env python3

"""
Sistema de Análise Preditiva
Analisa tendências e prevê comportamentos futuros no sistema cultural
"""

import logging
import yaml
from pathlib import Path
import datetime
import json
import math

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='predictive_analysis.log'
)

class PredictiveAnalysis:
    def __init__(self):
        self.data_dir = Path('../cultural_data')
        self.metrics_dir = Path('../metrics')
        self.analysis_dir = Path('../analysis')
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        
    def analyze_cultural_trends(self):
        """Analisa tendências culturais"""
        metrics = self.load_historical_metrics()
        predictions = {
            "cultural_evolution": self.predict_cultural_evolution(metrics),
            "behavior_patterns": self.predict_behavior_patterns(metrics),
            "narrative_development": self.predict_narrative_development(metrics)
        }
        return predictions
    
    def load_historical_metrics(self):
        """Carrega métricas históricas"""
        metrics = []
        for metric_file in self.metrics_dir.glob("cultural_metrics_*.yaml"):
            with open(metric_file) as f:
                metrics.append(yaml.safe_load(f))
        return sorted(metrics, key=lambda x: x['timestamp'])
    
    def predict_cultural_evolution(self, metrics):
        """Prevê evolução cultural"""
        if not metrics:
            return {}
            
        latest = metrics[-1]['cultural_metrics']
        trends = {
            "diversity_trend": self.calculate_trend(metrics, 
                                                  lambda x: x['cultural_metrics']['cultural_diversity']['military_diversity']),
            "influence_trend": self.calculate_trend(metrics,
                                                  lambda x: x['cultural_metrics']['cultural_influence']['viking_influence'])
        }
        
        return {
            "predicted_diversity": self.extrapolate_metric(trends["diversity_trend"]),
            "predicted_influence": self.extrapolate_metric(trends["influence_trend"]),
            "cultural_convergence": self.predict_convergence(metrics),
            "expansion_potential": self.calculate_expansion_potential(latest)
        }
    
    def predict_behavior_patterns(self, metrics):
        """Prevê padrões de comportamento"""
        if not metrics:
            return {}
            
        latest = metrics[-1]['antagonist_metrics']
        trends = {
            "complexity_trend": self.calculate_trend(metrics,
                                                   lambda x: x['antagonist_metrics']['behavior_complexity']['strategic_warrior']),
            "adaptation_trend": self.calculate_trend(metrics,
                                                   lambda x: x['antagonist_metrics']['adaptation_rate']['strategic_warrior'])
        }
        
        return {
            "predicted_complexity": self.extrapolate_metric(trends["complexity_trend"]),
            "predicted_adaptation": self.extrapolate_metric(trends["adaptation_trend"]),
            "emergence_likelihood": self.calculate_emergence_likelihood(latest),
            "behavior_stability": self.predict_behavior_stability(metrics)
        }
    
    def predict_narrative_development(self, metrics):
        """Prevê desenvolvimento narrativo"""
        if not metrics:
            return {}
            
        latest = metrics[-1]['narrative_metrics']
        trends = {
            "depth_trend": self.calculate_trend(metrics,
                                              lambda x: x['narrative_metrics']['narrative_depth']['cultural_conflict']),
            "coherence_trend": self.calculate_trend(metrics,
                                                  lambda x: x['narrative_metrics']['story_coherence']['cultural_conflict'])
        }
        
        return {
            "predicted_depth": self.extrapolate_metric(trends["depth_trend"]),
            "predicted_coherence": self.extrapolate_metric(trends["coherence_trend"]),
            "narrative_potential": self.calculate_narrative_potential(latest),
            "integration_quality": self.predict_integration_quality(metrics)
        }
    
    def calculate_trend(self, metrics, metric_accessor):
        """Calcula tendência de uma métrica"""
        if len(metrics) < 2:
            return 0.0
            
        values = [metric_accessor(m) for m in metrics]
        if not values:
            return 0.0
            
        # Cálculo de tendência linear simples
        n = len(values)
        x = list(range(n))
        mean_x = sum(x) / n
        mean_y = sum(values) / n
        
        numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def extrapolate_metric(self, trend, periods=1):
        """Extrapola métrica baseada na tendência"""
        # Limita a extrapolação entre 0 e 1
        return max(0.0, min(1.0, 0.5 + (trend * periods)))
    
    def predict_convergence(self, metrics):
        """Prevê convergência cultural"""
        if not metrics:
            return 0.0
            
        latest = metrics[-1]['cultural_metrics']
        diversity = latest['cultural_diversity']
        influence = latest['cultural_influence']
        
        # Média ponderada de diversidade e influência
        return (
            sum(diversity.values()) / len(diversity) * 0.6 +
            sum(influence.values()) / len(influence) * 0.4
        )
    
    def calculate_expansion_potential(self, metrics):
        """Calcula potencial de expansão cultural"""
        if not metrics:
            return 0.0
            
        diversity = metrics['cultural_diversity']
        influence = metrics['cultural_influence']
        
        # Potencial baseado em diversidade e influência atual
        return (
            max(diversity.values()) * 0.7 +
            max(influence.values()) * 0.3
        )
    
    def calculate_emergence_likelihood(self, metrics):
        """Calcula probabilidade de comportamentos emergentes"""
        if not metrics:
            return 0.0
            
        complexity = metrics['behavior_complexity']
        adaptation = metrics['adaptation_rate']
        
        # Probabilidade baseada em complexidade e adaptação
        return (
            sum(complexity.values()) / len(complexity) * 0.5 +
            sum(adaptation.values()) / len(adaptation) * 0.5
        )
    
    def predict_behavior_stability(self, metrics):
        """Prevê estabilidade comportamental"""
        if len(metrics) < 2:
            return 0.0
            
        # Calcula variação na complexidade comportamental
        latest = metrics[-1]['antagonist_metrics']['behavior_complexity']
        previous = metrics[-2]['antagonist_metrics']['behavior_complexity']
        
        variations = [abs(latest[k] - previous[k]) for k in latest.keys()]
        return 1.0 - (sum(variations) / len(variations))
    
    def calculate_narrative_potential(self, metrics):
        """Calcula potencial narrativo"""
        if not metrics:
            return 0.0
            
        depth = metrics['narrative_depth']
        coherence = metrics['story_coherence']
        
        # Potencial baseado em profundidade e coerência
        return (
            sum(depth.values()) / len(depth) * 0.6 +
            sum(coherence.values()) / len(coherence) * 0.4
        )
    
    def predict_integration_quality(self, metrics):
        """Prevê qualidade de integração narrativa"""
        if len(metrics) < 2:
            return 0.0
            
        # Analisa tendência de coerência narrativa
        latest = metrics[-1]['narrative_metrics']['story_coherence']
        previous = metrics[-2]['narrative_metrics']['story_coherence']
        
        improvements = [latest[k] - previous[k] for k in latest.keys()]
        return sum(improvements) / len(improvements) + 0.5
    
    def generate_report(self, predictions):
        """Gera relatório de previsões"""
        report = f"""
=== Relatório de Análise Preditiva ===
Timestamp: {datetime.datetime.now().isoformat()}

1. Evolução Cultural
   - Diversidade Prevista: {predictions['cultural_evolution']['predicted_diversity']:.2%}
   - Influência Prevista: {predictions['cultural_evolution']['predicted_influence']:.2%}
   - Convergência Cultural: {predictions['cultural_evolution']['cultural_convergence']:.2%}
   - Potencial de Expansão: {predictions['cultural_evolution']['expansion_potential']:.2%}

2. Padrões de Comportamento
   - Complexidade Prevista: {predictions['behavior_patterns']['predicted_complexity']:.2%}
   - Adaptação Prevista: {predictions['behavior_patterns']['predicted_adaptation']:.2%}
   - Probabilidade de Emergência: {predictions['behavior_patterns']['emergence_likelihood']:.2%}
   - Estabilidade Comportamental: {predictions['behavior_patterns']['behavior_stability']:.2%}

3. Desenvolvimento Narrativo
   - Profundidade Prevista: {predictions['narrative_development']['predicted_depth']:.2%}
   - Coerência Prevista: {predictions['narrative_development']['predicted_coherence']:.2%}
   - Potencial Narrativo: {predictions['narrative_development']['narrative_potential']:.2%}
   - Qualidade de Integração: {predictions['narrative_development']['integration_quality']:.2%}

=== Análise de Tendências ===
1. Tendências Culturais
   - {self.analyze_cultural_trend(predictions['cultural_evolution'])}

2. Tendências Comportamentais
   - {self.analyze_behavior_trend(predictions['behavior_patterns'])}

3. Tendências Narrativas
   - {self.analyze_narrative_trend(predictions['narrative_development'])}

=== Recomendações ===
{self.generate_recommendations(predictions)}
"""
        
        # Salvar relatório
        report_file = self.analysis_dir / f"predictive_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        # Salvar previsões em formato JSON para análise futura
        predictions_file = self.analysis_dir / f"predictions_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(predictions_file, 'w') as f:
            json.dump(predictions, f, indent=2)
        
        return report
    
    def analyze_cultural_trend(self, predictions):
        """Analisa tendência cultural"""
        if predictions['predicted_diversity'] > 0.8:
            trend = "Alta diversificação cultural prevista"
        elif predictions['predicted_diversity'] > 0.6:
            trend = "Diversificação cultural moderada"
        else:
            trend = "Possível estagnação cultural"
            
        if predictions['expansion_potential'] > 0.7:
            trend += " com forte potencial de expansão"
        
        return trend
    
    def analyze_behavior_trend(self, predictions):
        """Analisa tendência comportamental"""
        if predictions['emergence_likelihood'] > 0.8:
            trend = "Alta probabilidade de novos comportamentos emergentes"
        elif predictions['emergence_likelihood'] > 0.6:
            trend = "Comportamentos emergentes moderados esperados"
        else:
            trend = "Baixa probabilidade de emergência comportamental"
            
        if predictions['behavior_stability'] < 0.5:
            trend += " com possível instabilidade"
        
        return trend
    
    def analyze_narrative_trend(self, predictions):
        """Analisa tendência narrativa"""
        if predictions['predicted_depth'] > 0.8:
            trend = "Desenvolvimento narrativo profundo previsto"
        elif predictions['predicted_depth'] > 0.6:
            trend = "Desenvolvimento narrativo moderado"
        else:
            trend = "Possível simplificação narrativa"
            
        if predictions['integration_quality'] > 0.7:
            trend += " com boa integração cultural"
        
        return trend
    
    def generate_recommendations(self, predictions):
        """Gera recomendações baseadas nas previsões"""
        recommendations = []
        
        # Recomendações culturais
        if predictions['cultural_evolution']['expansion_potential'] > 0.7:
            recommendations.append("1. Considerar implementação de novas culturas")
        if predictions['cultural_evolution']['cultural_convergence'] < 0.6:
            recommendations.append("2. Fortalecer integração entre culturas existentes")
            
        # Recomendações comportamentais
        if predictions['behavior_patterns']['emergence_likelihood'] > 0.7:
            recommendations.append("3. Preparar para novos comportamentos emergentes")
        if predictions['behavior_patterns']['behavior_stability'] < 0.6:
            recommendations.append("4. Implementar estabilizadores comportamentais")
            
        # Recomendações narrativas
        if predictions['narrative_development']['narrative_potential'] > 0.7:
            recommendations.append("5. Expandir sistema narrativo")
        if predictions['narrative_development']['integration_quality'] < 0.6:
            recommendations.append("6. Melhorar integração narrativa")
            
        return "\n".join(recommendations)

def main():
    analyzer = PredictiveAnalysis()
    predictions = analyzer.analyze_cultural_trends()
    report = analyzer.generate_report(predictions)
    print(report)

if __name__ == "__main__":
    main()
