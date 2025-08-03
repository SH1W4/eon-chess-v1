import unittest
from pathlib import Path
import json
from typing import Dict, Any

from cultural_engine.cache.lru_cache import LRUCache
from cultural_engine.cache.profile_cache_manager import ProfileCacheManager
from cultural_engine.processors.leadership_profile_processor import LeadershipProfileProcessor
from cultural_engine.processors.narrative_generator import NarrativeGenerator

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(capacity=2)

    def test_put_and_get(self):
        self.cache.put("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_capacity_limit(self):
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")  # Deve remover key1
        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")

    def test_update_existing(self):
        self.cache.put("key1", "value1")
        self.cache.put("key1", "updated_value")
        self.assertEqual(self.cache.get("key1"), "updated_value")

class TestProfileCacheManager(unittest.TestCase):
    def setUp(self):
        self.cache_manager = ProfileCacheManager()

    def test_profile_caching(self):
        profile_data = {
            "name": "Test Leader",
            "era": "2000-present",
            "domain": "Test Domain"
        }
        self.cache_manager.cache_profile("test_profile", profile_data)
        cached_profile = self.cache_manager.get_profile("test_profile")
        self.assertEqual(cached_profile, profile_data)

    def test_pattern_caching(self):
        pattern_data = {
            "name": "Test Pattern",
            "type": "strategic"
        }
        self.cache_manager.cache_pattern("test_pattern", pattern_data)
        cached_pattern = self.cache_manager.get_pattern("test_pattern")
        self.assertEqual(cached_pattern, pattern_data)

    def test_narrative_caching(self):
        narrative_text = "Test narrative text"
        self.cache_manager.cache_narrative("test_narrative", narrative_text)
        cached_narrative = self.cache_manager.get_narrative("test_narrative")
        self.assertEqual(cached_narrative, narrative_text)

class TestLeadershipProfileProcessor(unittest.TestCase):
    def setUp(self):
        # Cria um perfil de teste
        self.test_profile = {
            "test_leader": {
                "name": "Test Leader",
                "era": "2000-present",
                "domain": "Test Domain",
                "strategic_elements": ["element1", "element2"],
                "leadership_style": "strategic",
                "cultural_impact": "Test impact",
                "narrative_elements": ["element1", "element2"]
            }
        }
        
        # Salva o perfil em um arquivo temporário
        self.test_file = Path("test_profiles.yaml")
        with open(self.test_file, "w") as f:
            json.dump(self.test_profile, f)
        
        self.processor = LeadershipProfileProcessor(str(self.test_file))

    def tearDown(self):
        # Limpa o arquivo temporário
        if self.test_file.exists():
            self.test_file.unlink()

    def test_profile_loading(self):
        profiles = self.processor.load_profiles()
        self.assertEqual(profiles, self.test_profile)

    def test_pattern_matching(self):
        game_state = {
            "position_type": "element1",
            "game_phase": "middlegame",
            "material_advantage": 1
        }
        matched_profiles = self.processor.match_strategy(game_state)
        self.assertTrue(len(matched_profiles) > 0)

    def test_strategic_advice_generation(self):
        game_state = {
            "position_type": "central",
            "phase": "middlegame"
        }
        advice = self.processor.generate_strategic_advice("test_leader", game_state)
        self.assertIsInstance(advice, str)
        self.assertTrue(len(advice) > 0)

class TestNarrativeGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = NarrativeGenerator()
        self.test_profile = {
            "name": "Test Leader",
            "era": "2000-present",
            "domain": "Test Domain",
            "leadership_style": "strategic",
            "cultural_impact": "Test impact",
            "achievements": ["Achievement 1"],
            "strategic_elements": ["element1", "element2"]
        }

    def test_narrative_generation(self):
        game_state = {
            "move_number": 5,
            "material_count": 32
        }
        move_info = {
            "is_capture": False,
            "is_central": True,
            "is_development": True
        }
        
        narrative = self.generator.generate_narrative(
            self.test_profile,
            game_state,
            move_info
        )
        
        self.assertIsInstance(narrative, str)
        self.assertTrue(len(narrative) > 0)
        self.assertIn(self.test_profile["name"], narrative)

    def test_strategic_insight_generation(self):
        game_state = {
            "position_type": "central",
            "phase": "middlegame"
        }
        
        insight = self.generator.generate_strategic_insight(
            self.test_profile,
            game_state
        )
        
        self.assertIsInstance(insight, str)
        self.assertTrue(len(insight) > 0)
        self.assertIn(self.test_profile["name"], insight)

    def test_cultural_perspective_generation(self):
        game_state = {
            "position_type": "central",
            "phase": "middlegame"
        }
        
        perspective = self.generator.generate_cultural_perspective(
            self.test_profile,
            game_state
        )
        
        self.assertIsInstance(perspective, str)
        self.assertTrue(len(perspective) > 0)
        self.assertIn(self.test_profile["name"], perspective)

    def test_game_phase_determination(self):
        # Teste para fase de abertura
        opening_state = {"move_number": 5, "material_count": 32}
        self.assertEqual(
            self.generator._determine_game_phase(opening_state),
            "opening"
        )
        
        # Teste para final
        endgame_state = {"move_number": 30, "material_count": 15}
        self.assertEqual(
            self.generator._determine_game_phase(endgame_state),
            "endgame"
        )
        
        # Teste para meio-jogo
        middlegame_state = {"move_number": 15, "material_count": 28}
        self.assertEqual(
            self.generator._determine_game_phase(middlegame_state),
            "middlegame"
        )

if __name__ == '__main__':
    unittest.main()
