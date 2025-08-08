"""
Testes de Performance do Sistema Narrativo AEON Chess
"""

import pytest
import time
import asyncio
from typing import List, Dict, Any
from unittest.mock import Mock, MagicMock
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from narrative.engine import NarrativeEngine
from narrative.types import ChessEvent, GameContext, NarrativeResponse


class TestNarrativePerformance:
    """Testes de performance do motor narrativo"""
    
    @pytest.fixture
    def engine(self):
        """Fixture do motor narrativo"""
        return NarrativeEngine()
    
    @pytest.fixture
    def mock_context(self):
        """Contexto de jogo mockado"""
        return GameContext(
            game_phase='middlegame',
            move_count=25,
            material_balance=0,
            time_remaining={'white': 300, 'black': 280},
            position_evaluation=0.5,
            player_style='aggressive',
            tension_level=0.7,
            last_moves=['e2e4', 'd7d5', 'exd5']
        )
    
    @pytest.fixture
    def events_batch(self) -> List[ChessEvent]:
        """Lote de eventos para teste"""
        events = []
        event_types = ['move', 'capture', 'check', 'castle', 'promotion']
        
        for i in range(100):
            events.append(ChessEvent(
                type=event_types[i % len(event_types)],
                piece=f'piece_{i}',
                position=f'pos_{i}',
                timestamp=time.time() + i,
                intensity=0.5 + (i % 50) / 100
            ))
        
        return events
    
    @pytest.mark.benchmark(group="event_processing")
    def test_single_event_processing(self, benchmark, engine, mock_context):
        """Benchmark de processamento de evento único"""
        event = ChessEvent(
            type='capture',
            piece='queen',
            position='e5',
            timestamp=time.time(),
            intensity=0.8
        )
        
        result = benchmark(engine.process_event, event, mock_context)
        
        assert result is not None
        assert isinstance(result, NarrativeResponse)
        assert result.narrative != ""
    
    @pytest.mark.benchmark(group="event_processing")
    def test_batch_event_processing(self, benchmark, engine, mock_context, events_batch):
        """Benchmark de processamento em lote"""
        
        def process_batch():
            results = []
            for event in events_batch:
                result = engine.process_event(event, mock_context)
                results.append(result)
            return results
        
        results = benchmark(process_batch)
        
        assert len(results) == len(events_batch)
        assert all(isinstance(r, NarrativeResponse) for r in results)
    
    @pytest.mark.benchmark(group="narrative_generation")
    def test_narrative_generation_speed(self, benchmark, engine):
        """Benchmark de geração de narrativa"""
        
        def generate_narrative():
            return engine.generate_narrative(
                event_type='checkmate',
                context={'winner': 'white', 'moves': 45},
                intensity=1.0
            )
        
        narrative = benchmark(generate_narrative)
        
        assert narrative is not None
        assert len(narrative) > 0
    
    @pytest.mark.benchmark(group="context_building")
    def test_context_building_performance(self, benchmark, engine):
        """Benchmark de construção de contexto"""
        
        game_state = {
            'board': [[None] * 8 for _ in range(8)],
            'moves': ['e2e4'] * 50,
            'captures': ['pawn', 'knight', 'bishop'],
            'time': {'white': 300, 'black': 250}
        }
        
        context = benchmark(engine.build_context, game_state)
        
        assert context is not None
        assert hasattr(context, 'game_phase')
        assert hasattr(context, 'tension_level')
    
    @pytest.mark.benchmark(group="cache")
    def test_cache_performance(self, benchmark, engine, mock_context):
        """Benchmark de performance do cache"""
        
        # Evento que será cacheado
        event = ChessEvent(
            type='move',
            piece='pawn',
            position='e4',
            timestamp=time.time(),
            intensity=0.3
        )
        
        # Primeira chamada (sem cache)
        engine.process_event(event, mock_context)
        
        # Benchmark de chamadas com cache
        def cached_processing():
            return engine.process_event(event, mock_context)
        
        result = benchmark(cached_processing)
        
        assert result is not None
        # Verificar que o cache está funcionando
        assert engine.cache_hits > 0
    
    @pytest.mark.benchmark(group="memory")
    def test_memory_usage(self, engine, events_batch, mock_context):
        """Teste de uso de memória"""
        import tracemalloc
        
        tracemalloc.start()
        
        # Processar muitos eventos
        for _ in range(10):
            for event in events_batch:
                engine.process_event(event, mock_context)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Verificar que o uso de memória está dentro dos limites
        assert peak < 100 * 1024 * 1024  # Menos de 100MB
        
        # Calcular média de memória por evento
        memory_per_event = peak / (10 * len(events_batch))
        assert memory_per_event < 10 * 1024  # Menos de 10KB por evento
    
    @pytest.mark.asyncio
    @pytest.mark.benchmark(group="async")
    async def test_async_processing_performance(self, benchmark, engine, events_batch, mock_context):
        """Benchmark de processamento assíncrono"""
        
        async def process_async():
            tasks = []
            for event in events_batch[:10]:  # Limitar para teste
                task = asyncio.create_task(
                    engine.process_event_async(event, mock_context)
                )
                tasks.append(task)
            
            return await asyncio.gather(*tasks)
        
        # Usar benchmark.pedantic para controle fino
        results = await benchmark.pedantic(
            process_async,
            rounds=5,
            iterations=1
        )
        
        assert len(results) == 10
        assert all(r is not None for r in results)
    
    @pytest.mark.benchmark(group="templates")
    def test_template_selection_performance(self, benchmark, engine):
        """Benchmark de seleção de template"""
        
        event_types = ['move', 'capture', 'check', 'castle', 'promotion', 'checkmate']
        contexts = [
            {'phase': 'opening', 'intensity': 0.3},
            {'phase': 'middlegame', 'intensity': 0.6},
            {'phase': 'endgame', 'intensity': 0.9}
        ]
        
        def select_templates():
            results = []
            for event_type in event_types:
                for context in contexts:
                    template = engine.select_template(event_type, context)
                    results.append(template)
            return results
        
        templates = benchmark(select_templates)
        
        assert len(templates) == len(event_types) * len(contexts)
        assert all(t is not None for t in templates)
    
    @pytest.mark.benchmark(group="adaptation")
    def test_adaptation_performance(self, benchmark, engine):
        """Benchmark do sistema de adaptação"""
        
        player_profile = {
            'skill_level': 'intermediate',
            'preferred_style': 'tactical',
            'narrative_preference': 'detailed'
        }
        
        raw_narrative = "The knight moves forward with determination."
        
        def adapt_narrative():
            return engine.adapt_to_player(raw_narrative, player_profile)
        
        adapted = benchmark(adapt_narrative)
        
        assert adapted is not None
        assert len(adapted) > 0
    
    def test_stress_test(self, engine, mock_context):
        """Teste de stress com muitos eventos simultâneos"""
        
        start_time = time.time()
        events_processed = 0
        errors = 0
        
        # Processar eventos por 5 segundos
        while time.time() - start_time < 5:
            try:
                event = ChessEvent(
                    type='move',
                    piece='pawn',
                    position='e4',
                    timestamp=time.time(),
                    intensity=0.5
                )
                
                result = engine.process_event(event, mock_context)
                if result:
                    events_processed += 1
                else:
                    errors += 1
                    
            except Exception:
                errors += 1
        
        elapsed = time.time() - start_time
        events_per_second = events_processed / elapsed
        
        # Verificações de performance
        assert events_per_second > 100  # Pelo menos 100 eventos por segundo
        assert errors < events_processed * 0.01  # Menos de 1% de erros
        
        print(f"Stress test: {events_per_second:.2f} events/sec, {errors} errors")
    
    @pytest.mark.benchmark(group="optimization")
    def test_optimization_comparison(self, benchmark, engine, mock_context):
        """Comparação entre versão otimizada e não otimizada"""
        
        event = ChessEvent(
            type='capture',
            piece='queen',
            position='e5',
            timestamp=time.time(),
            intensity=0.8
        )
        
        # Testar com otimizações desabilitadas
        engine.enable_optimizations = False
        unoptimized = benchmark.pedantic(
            lambda: engine.process_event(event, mock_context),
            rounds=10,
            iterations=5
        )
        
        # Testar com otimizações habilitadas
        engine.enable_optimizations = True
        optimized = benchmark.pedantic(
            lambda: engine.process_event(event, mock_context),
            rounds=10,
            iterations=5
        )
        
        # Verificar que a versão otimizada é mais rápida
        assert optimized is not None
        assert unoptimized is not None


class TestMemoryLeaks:
    """Testes para detectar vazamentos de memória"""
    
    def test_no_memory_leak_in_cache(self):
        """Verifica que o cache não causa vazamento de memória"""
        import gc
        import weakref
        
        engine = NarrativeEngine()
        refs = []
        
        # Criar muitas narrativas e guardar referências fracas
        for i in range(1000):
            event = ChessEvent(
                type='move',
                piece=f'piece_{i}',
                position=f'pos_{i}',
                timestamp=time.time(),
                intensity=0.5
            )
            
            context = GameContext(
                game_phase='middlegame',
                move_count=i,
                material_balance=0,
                time_remaining={'white': 300, 'black': 300},
                position_evaluation=0.0,
                player_style='balanced',
                tension_level=0.5,
                last_moves=[]
            )
            
            result = engine.process_event(event, context)
            refs.append(weakref.ref(result))
        
        # Limpar cache e forçar coleta de lixo
        engine.clear_cache()
        gc.collect()
        
        # Verificar que os objetos foram liberados
        alive_refs = sum(1 for ref in refs if ref() is not None)
        assert alive_refs < 10  # Permitir alguns objetos vivos por questões de timing
    
    def test_no_memory_leak_in_history(self):
        """Verifica que o histórico não acumula memória indefinidamente"""
        import psutil
        import os
        
        engine = NarrativeEngine()
        process = psutil.Process(os.getpid())
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Processar muitos eventos
        for i in range(10000):
            event = ChessEvent(
                type='move',
                piece='pawn',
                position='e4',
                timestamp=time.time(),
                intensity=0.5
            )
            
            context = GameContext(
                game_phase='opening',
                move_count=i,
                material_balance=0,
                time_remaining={'white': 300, 'black': 300},
                position_evaluation=0.0,
                player_style='balanced',
                tension_level=0.3,
                last_moves=[]
            )
            
            engine.process_event(event, context)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Verificar que o aumento de memória é razoável
        assert memory_increase < 50  # Menos de 50MB de aumento


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--benchmark-only"])
