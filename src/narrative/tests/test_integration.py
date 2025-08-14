#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes de integração do Sistema Narrativo AEON
"""

import unittest
import json
from pathlib import Path
import sys
from os.path import dirname, abspath

# Adiciona os diretórios necessários ao path
root_dir = dirname(dirname(dirname(abspath(__file__))))
src_dir = dirname(dirname(abspath(__file__)))
sys.path.extend([root_dir, src_dir])

from narrative.engine.engine import NarrativeEngine, NarrativeConfig
from narrative.engine.cultural_processor import CulturalProcessor, CultureConfig
from narrative.engine.quantum_processor import AdvancedProcessor, ProcessorConfig
from narrative.engine.monitor import Monitor, MonitorConfig

class TestNarrativeIntegration(unittest.TestCase):
    """Testes de integração do sistema narrativo"""
    
    def setUp(self):
        """Configura ambiente de teste"""
        self.config = NarrativeConfig(
            mode="test",
            language="pt-BR",
            cultural_integration=True,
            quantum_processing=True,
            adaptation_rate=0.75
        )
        self.engine = NarrativeEngine(config=self.config)
        self.engine.initialize()
    
    def tearDown(self):
        """Limpa recursos após os testes"""
        if hasattr(self, 'engine'):
            if self.engine.monitor:
                self.engine.monitor.cleanup()
            if self.engine.quantum_processor:
                self.engine.quantum_processor.cleanup()
    
    def test_engine_initialization(self):
        """Testa inicialização do motor"""
        self.assertTrue(self.engine.initialized)
        self.assertIsNotNone(self.engine.cultural_processor)
        self.assertIsNotNone(self.engine.quantum_processor)
        self.assertIsNotNone(self.engine.monitor)
    
    def test_process_event(self):
        """Testa processamento de eventos"""
        event = {
            "type": "move",
            "data": {
                "piece": "knight",
                "from": "b1",
                "to": "c3",
                "player": "white"
            }
        }
        
        result = self.engine.process_event(event)
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "processed")
        self.assertEqual(result["event"], event)
        
        # Verifica métricas
        status = self.engine.get_status()
        self.assertIn("metrics", status)
        self.assertIn("performance", status["metrics"])
    
    def test_generate_narrative(self):
        """Testa geração de narrativa"""
        context = {
            "game_phase": "opening",
            "moves": [
                {"piece": "pawn", "from": "e2", "to": "e4"},
                {"piece": "pawn", "from": "e7", "to": "e5"}
            ],
            "cultural_context": {
                "style": "classical",
                "opening": "king's pawn game"
            }
        }
        
        narrative = self.engine.generate_narrative(context)
        self.assertIsNotNone(narrative)
        self.assertIsInstance(narrative, str)
        self.assertNotEqual(narrative, "")
        
        # Verifica métricas
        status = self.engine.get_status()
        self.assertIn("metrics", status)
        self.assertIn("quality", status["metrics"])
    
    def test_monitoring_integration(self):
        """Testa integração do monitoramento"""
        # Gera algumas atividades
        self.engine.process_event({"type": "test"})
        self.engine.generate_narrative({"phase": "test"})
        
        # Verifica métricas e alertas
        status = self.engine.get_status()
        self.assertIn("metrics", status)
        self.assertIn("alerts", status)
        
        # Verifica categorias específicas
        metrics = status["metrics"]
        self.assertIn("performance", metrics)
        self.assertIn("quality", metrics)
        self.assertIn("system", metrics)
    
    def test_quantum_processing(self):
        """Testa integração do processamento quântico"""
        data = {
            "complexity": "high",
            "patterns": ["sicilian", "dragon"],
            "evaluation": 0.45
        }
        
        # Testa otimização
        optimized = self.engine.quantum_processor.optimize_processing(data)
        self.assertIsNotNone(optimized)
        self.assertIn("data", optimized)
        
        # Testa análise de padrões
        patterns = self.engine.quantum_processor.analyze_patterns(data)
        self.assertIsNotNone(patterns)
        self.assertIsInstance(patterns, list)
    
    def test_cultural_integration(self):
        """Testa integração cultural"""
        context = {
            "style": "modern",
            "region": "eastern_europe",
            "period": "contemporary"
        }
        
        # Testa análise cultural
        cultural_context = self.engine.cultural_processor.analyze_cultural_context(context)
        self.assertIsNotNone(cultural_context)
        self.assertIn("culture", cultural_context)
        
        # Testa adaptação narrativa
        narrative = "Test narrative"
        adapted = self.engine.cultural_processor.adapt_narrative(
            narrative=narrative,
            culture=cultural_context["culture"]
        )
        self.assertIsNotNone(adapted)
        self.assertIsInstance(adapted, str)
    
    def test_error_handling(self):
        """Testa tratamento de erros"""
        # Testa com contexto inválido
        invalid_context = None
        narrative = self.engine.generate_narrative(invalid_context)
        self.assertEqual(narrative, "Erro na geração da narrativa")
        
        # Verifica se erro foi registrado
        status = self.engine.get_status()
        self.assertIn("metrics", status)
        self.assertIn("system", status["metrics"])
        self.assertGreater(status["metrics"]["system"]["error_count"], 0)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
