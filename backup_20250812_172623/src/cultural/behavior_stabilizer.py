#!/usr/bin/env python3

"""
Sistema de Estabilização Comportamental
Gerencia e estabiliza comportamentos emergentes no sistema cultural
"""

import logging
import yaml
from pathlib import Path
import json
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='behavior_stabilizer.log'
)

class BehaviorStabilizer:
    def __init__(self):
        self.data_dir = Path('../cultural_data')
        self.stability_rules = {
            "emergence_threshold": 0.7,
            "stability_threshold": 0.8,
            "adaptation_rate": 0.5,
            "cooldown_period": 3600  # 1 hora em segundos
        }
        
    def stabilize_behavior(self, behavior_pattern):
        """Estabiliza um padrão de comportamento"""
        if not self.needs_stabilization(behavior_pattern):
            return behavior_pattern
            
        stabilized = self.apply_stabilization_rules(behavior_pattern)
        self.log_stabilization(behavior_pattern, stabilized)
        return stabilized
        
    def needs_stabilization(self, behavior_pattern):
        """Verifica se um comportamento precisa de estabilização"""
        return (
            behavior_pattern["volatility_index"] > self.stability_rules["emergence_threshold"] or
            behavior_pattern["stability_score"] < self.stability_rules["stability_threshold"]
        )
        
    def apply_stabilization_rules(self, behavior_pattern):
        """Aplica regras de estabilização"""
        stabilized = behavior_pattern.copy()
        
        # Ajusta taxa de adaptação
        stabilized["adaptation_rate"] = min(
            behavior_pattern["adaptation_rate"],
            self.stability_rules["adaptation_rate"]
        )
        
        # Aplica período de cooldown
        stabilized["cooldown_period"] = self.stability_rules["cooldown_period"]
        
        # Implementa limitadores de comportamento
        stabilized["behavior_limits"] = {
            "max_intensity": 0.8,
            "min_stability": 0.6,
            "max_adaptation_rate": 0.7
        }
        
        # Adiciona mecanismos de auto-regulação
        stabilized["self_regulation"] = {
            "enabled": True,
            "check_interval": 300,  # 5 minutos
            "correction_threshold": 0.2
        }
        
        return stabilized
        
    def log_stabilization(self, original, stabilized):
        """Registra processo de estabilização"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original_pattern": original,
            "stabilized_pattern": stabilized,
            "changes": self.compute_changes(original, stabilized)
        }
        
        log_file = self.data_dir / "logs" / f"stabilization_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(log_entry, f, indent=2)
            
    def compute_changes(self, original, stabilized):
        """Calcula mudanças aplicadas"""
        changes = {
            "adaptation_rate_change": stabilized["adaptation_rate"] - original["adaptation_rate"],
            "stability_improvement": stabilized.get("stability_score", 0) - original.get("stability_score", 0),
            "applied_limits": stabilized["behavior_limits"],
            "self_regulation": stabilized["self_regulation"]
        }
        return changes
        
    def monitor_stability(self, behavior_patterns):
        """Monitora estabilidade dos comportamentos"""
        monitoring_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "patterns_monitored": len(behavior_patterns),
            "stability_metrics": self.calculate_stability_metrics(behavior_patterns),
            "recommendations": self.generate_stability_recommendations(behavior_patterns)
        }
        
        return monitoring_data
        
    def calculate_stability_metrics(self, behavior_patterns):
        """Calcula métricas de estabilidade"""
        metrics = {
            "average_stability": sum(p.get("stability_score", 0) for p in behavior_patterns) / len(behavior_patterns),
            "volatility_index": sum(p.get("volatility_index", 0) for p in behavior_patterns) / len(behavior_patterns),
            "adaptation_rate": sum(p.get("adaptation_rate", 0) for p in behavior_patterns) / len(behavior_patterns)
        }
        
        metrics["overall_stability"] = (
            metrics["average_stability"] * 0.4 +
            (1 - metrics["volatility_index"]) * 0.3 +
            (1 - metrics["adaptation_rate"]) * 0.3
        )
        
        return metrics
        
    def generate_stability_recommendations(self, behavior_patterns):
        """Gera recomendações de estabilidade"""
        metrics = self.calculate_stability_metrics(behavior_patterns)
        recommendations = []
        
        if metrics["volatility_index"] > 0.6:
            recommendations.append({
                "type": "high_volatility",
                "action": "Reduzir taxa de adaptação",
                "target_patterns": [p["name"] for p in behavior_patterns if p.get("volatility_index", 0) > 0.6]
            })
            
        if metrics["average_stability"] < 0.5:
            recommendations.append({
                "type": "low_stability",
                "action": "Aumentar período de cooldown",
                "target_patterns": [p["name"] for p in behavior_patterns if p.get("stability_score", 0) < 0.5]
            })
            
        if metrics["adaptation_rate"] > 0.8:
            recommendations.append({
                "type": "high_adaptation",
                "action": "Implementar limitadores de comportamento",
                "target_patterns": [p["name"] for p in behavior_patterns if p.get("adaptation_rate", 0) > 0.8]
            })
            
        return recommendations
        
    def apply_stability_policy(self, behavior_patterns, policy):
        """Aplica política de estabilidade"""
        stabilized_patterns = []
        
        for pattern in behavior_patterns:
            if pattern["name"] in policy.get("target_patterns", []):
                if policy["type"] == "high_volatility":
                    pattern["adaptation_rate"] *= 0.8
                elif policy["type"] == "low_stability":
                    pattern["cooldown_period"] *= 1.5
                elif policy["type"] == "high_adaptation":
                    pattern["behavior_limits"]["max_intensity"] *= 0.9
                    
            stabilized_patterns.append(pattern)
            
        return stabilized_patterns

def main():
    stabilizer = BehaviorStabilizer()
    
    # Exemplo de padrão de comportamento instável
    unstable_pattern = {
        "name": "aggressive_adaptation",
        "volatility_index": 0.8,
        "stability_score": 0.4,
        "adaptation_rate": 0.9
    }
    
    # Estabilizar comportamento
    stabilized = stabilizer.stabilize_behavior(unstable_pattern)
    
    # Monitorar estabilidade
    monitoring_result = stabilizer.monitor_stability([unstable_pattern, stabilized])
    
    print("\n=== Relatório de Estabilização ===")
    print(f"Comportamento Original: {unstable_pattern}")
    print(f"Comportamento Estabilizado: {stabilized}")
    print("\nMonitoramento:")
    print(json.dumps(monitoring_result, indent=2))

if __name__ == "__main__":
    main()
