"""
Testes de Integração Completos - AEON Chess
Valida a integração entre todos os componentes do sistema
"""

import pytest
import asyncio
from typing import Dict, Any
from pathlib import Path
import sys

# Adicionar src ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from traditional.core.board.board import Board
from traditional.core.game_engine import ChessEngine
from ai.adaptive_ai import AdaptiveAI
from cultural.style_analyzer import CulturalStyleAnalyzer
from narrative.engine import NarrativeEngine
from monitoring.system import SystemMonitor

class TestFullSystemIntegration:
    """Testes de integração completa do sistema"""
    
    @pytest.fixture
    def board(self):
        """Fixture para criar um tabuleiro"""
        return Board()
    
    @pytest.fixture
    def engine(self, board):
        """Fixture para criar o motor de xadrez"""
        return ChessEngine(board)
    
    @pytest.fixture
    def ai(self):
        """Fixture para criar a IA adaptativa"""
        return AdaptiveAI()
    
    @pytest.fixture
    def cultural_analyzer(self):
        """Fixture para criar o analisador cultural"""
        return CulturalStyleAnalyzer()
    
    @pytest.fixture
    def narrative_engine(self):
        """Fixture para criar o motor narrativo"""
        return NarrativeEngine()
    
    @pytest.fixture
    def monitor(self):
        """Fixture para criar o monitor do sistema"""
        return SystemMonitor()
    
    def test_complete_game_flow(self, board, engine, ai, cultural_analyzer, narrative_engine, monitor):
        """Testa o fluxo completo de um jogo"""
        # 1. Iniciar monitoramento
        monitor.start_monitoring("game_test")
        
        # 2. Configurar perfil cultural
        cultural_profile = "persian"
        cultural_analyzer.set_active_culture(cultural_profile)
        
        # 3. Gerar narrativa de abertura
        opening_narrative = narrative_engine.generate_opening_narrative(cultural_profile)
        assert opening_narrative is not None
        assert len(opening_narrative) > 0
        
        # 4. Fazer alguns movimentos
        moves_made = []
        for i in range(5):
            # Movimento do jogador humano (brancas)
            valid_moves = engine.get_valid_moves("white")
            assert len(valid_moves) > 0
            
            # Escolher primeiro movimento válido
            human_move = valid_moves[0]
            result = engine.make_move(human_move)
            assert result["success"]
            moves_made.append(human_move)
            
            # Análise cultural do movimento
            cultural_analysis = cultural_analyzer.analyze_move(human_move, board)
            assert cultural_analysis is not None
            
            # Gerar narrativa do movimento
            move_narrative = narrative_engine.generate_move_narrative(
                human_move, 
                cultural_profile,
                board
            )
            assert move_narrative is not None
            
            # Movimento da IA (pretas)
            ai_move = ai.get_best_move(board, "black")
            assert ai_move is not None
            
            result = engine.make_move(ai_move)
            assert result["success"]
            moves_made.append(ai_move)
            
            # Atualizar perfil da IA baseado no jogo
            ai.update_profile(board)
        
        # 5. Verificar métricas do monitor
        metrics = monitor.get_metrics()
        assert metrics["game_moves"] >= 10
        assert metrics["ai_calculations"] > 0
        
        # 6. Verificar estado final
        assert len(moves_made) == 10
        assert board.move_count == 10
        
        monitor.stop_monitoring()
    
    def test_cultural_adaptation(self, board, ai, cultural_analyzer):
        """Testa a adaptação cultural da IA"""
        cultures = ["persian", "mongol", "chinese", "japanese"]
        
        for culture in cultures:
            # Configurar cultura
            cultural_analyzer.set_active_culture(culture)
            ai.set_cultural_profile(culture)
            
            # Fazer movimento com perfil cultural
            move = ai.get_best_move(board, "white")
            assert move is not None
            
            # Analisar se o movimento está alinhado com a cultura
            style_match = cultural_analyzer.evaluate_style_match(move, culture)
            assert style_match > 0.5  # Pelo menos 50% de alinhamento
    
    def test_narrative_consistency(self, narrative_engine, board):
        """Testa a consistência das narrativas geradas"""
        cultures = ["persian", "arabic", "indian"]
        narratives = []
        
        for culture in cultures:
            # Gerar narrativa para mesma posição
            narrative = narrative_engine.generate_position_narrative(
                board,
                culture
            )
            narratives.append(narrative)
            
            # Verificar que cada cultura gera narrativa única
            assert narrative is not None
            assert len(narrative) > 50  # Narrativa substancial
        
        # Verificar que narrativas são diferentes entre culturas
        assert len(set(narratives)) == len(cultures)
    
    def test_performance_under_load(self, board, engine, ai):
        """Testa a performance do sistema sob carga"""
        import time
        
        start_time = time.time()
        moves_evaluated = 0
        
        # Simular análise intensiva
        for _ in range(10):
            valid_moves = engine.get_valid_moves("white")
            for move in valid_moves[:5]:  # Avaliar primeiros 5 movimentos
                # Criar cópia do tabuleiro
                test_board = Board()
                test_board.pieces = board.pieces.copy()
                
                # Fazer movimento temporário
                test_board.make_move(move)
                
                # IA avalia posição
                evaluation = ai.evaluate_position(test_board)
                assert evaluation is not None
                moves_evaluated += 1
        
        elapsed_time = time.time() - start_time
        moves_per_second = moves_evaluated / elapsed_time
        
        # Verificar performance mínima
        assert moves_per_second > 10  # Pelo menos 10 avaliações por segundo
        
    @pytest.mark.asyncio
    async def test_concurrent_games(self, engine, ai):
        """Testa múltiplos jogos simultâneos"""
        async def play_game(game_id: int) -> Dict[str, Any]:
            board = Board()
            game_engine = ChessEngine(board)
            game_ai = AdaptiveAI()
            
            moves = 0
            for _ in range(5):
                # Movimento branco
                valid_moves = game_engine.get_valid_moves("white")
                if valid_moves:
                    move = valid_moves[0]
                    game_engine.make_move(move)
                    moves += 1
                
                # Movimento preto (IA)
                ai_move = game_ai.get_best_move(board, "black")
                if ai_move:
                    game_engine.make_move(ai_move)
                    moves += 1
                
                # Simular delay
                await asyncio.sleep(0.1)
            
            return {
                "game_id": game_id,
                "moves": moves,
                "final_position": len(board.pieces)
            }
        
        # Executar 3 jogos simultâneos
        games = await asyncio.gather(
            play_game(1),
            play_game(2),
            play_game(3)
        )
        
        # Verificar que todos os jogos foram executados
        assert len(games) == 3
        for game in games:
            assert game["moves"] >= 5
            assert game["final_position"] > 0
    
    def test_save_and_load_game(self, board, engine):
        """Testa salvar e carregar estado do jogo"""
        # Fazer alguns movimentos
        original_moves = []
        for _ in range(3):
            valid_moves = engine.get_valid_moves("white")
            if valid_moves:
                move = valid_moves[0]
                engine.make_move(move)
                original_moves.append(move)
        
        # Salvar estado
        game_state = engine.save_game_state()
        assert game_state is not None
        assert "moves" in game_state
        assert "board" in game_state
        
        # Criar novo jogo e carregar estado
        new_board = Board()
        new_engine = ChessEngine(new_board)
        
        success = new_engine.load_game_state(game_state)
        assert success
        
        # Verificar que o estado foi restaurado
        assert new_board.move_count == board.move_count
        assert len(new_board.pieces) == len(board.pieces)
    
    def test_endgame_detection(self, board, engine):
        """Testa detecção de fim de jogo"""
        # Configurar posição de xeque-mate
        board.clear()
        board.add_piece("king", "white", (4, 0))
        board.add_piece("king", "black", (4, 7))
        board.add_piece("queen", "white", (4, 6))
        board.add_piece("rook", "white", (5, 7))
        
        # Verificar detecção
        is_checkmate = engine.is_checkmate("black")
        assert is_checkmate
        
        game_result = engine.get_game_result()
        assert game_result["finished"]
        assert game_result["winner"] == "white"
        assert game_result["reason"] == "checkmate"
    
    def test_special_moves_integration(self, board, engine, narrative_engine):
        """Testa integração de movimentos especiais com narrativa"""
        # Configurar para roque
        board.clear()
        board.add_piece("king", "white", (4, 0))
        board.add_piece("rook", "white", (7, 0))
        
        # Verificar que roque é válido
        valid_moves = engine.get_valid_moves("white")
        castle_move = None
        for move in valid_moves:
            if move.is_castle:
                castle_move = move
                break
        
        assert castle_move is not None
        
        # Executar roque
        result = engine.make_move(castle_move)
        assert result["success"]
        
        # Gerar narrativa especial para roque
        narrative = narrative_engine.generate_special_move_narrative(
            castle_move,
            "persian"
        )
        assert narrative is not None
        assert "roque" in narrative.lower() or "castelo" in narrative.lower()

def test_system_health():
    """Teste rápido de saúde do sistema"""
    try:
        # Tentar importar todos os módulos principais
        from traditional.core.board.board import Board
        from ai.adaptive_ai import AdaptiveAI
        from cultural.style_analyzer import CulturalStyleAnalyzer
        from narrative.engine import NarrativeEngine
        
        # Criar instâncias básicas
        board = Board()
        ai = AdaptiveAI()
        cultural = CulturalStyleAnalyzer()
        narrative = NarrativeEngine()
        
        # Verificar que objetos foram criados
        assert board is not None
        assert ai is not None
        assert cultural is not None
        assert narrative is not None
        
        print("✅ Sistema de xadrez AEON está saudável!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema: {e}")
        return False

if __name__ == "__main__":
    # Executar teste de saúde rápido
    test_system_health()
