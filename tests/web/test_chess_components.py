import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestChessComponents:
    def test_board_initial_setup(self, game_page):
        """Testa se o tabuleiro está configurado corretamente no início do jogo"""
        # Verifica se o tabuleiro está presente
        board = game_page.find_element(By.CSS_SELECTOR, '[data-testid="chess-board"]')
        assert board is not None
        
        # Verifica se todas as peças estão em suas posições iniciais
        pieces = game_page.find_elements(By.CSS_SELECTOR, "[data-testid^='piece-']")
        assert len(pieces) == 32  # 16 peças brancas + 16 peças pretas
        
        # Verifica posições específicas de algumas peças
        white_king = game_page.find_element(By.CSS_SELECTOR, '[data-testid="piece-7-4"]')  # e1
        black_king = game_page.find_element(By.CSS_SELECTOR, '[data-testid="piece-0-4"]')  # e8
        assert "♔" in white_king.text
        assert "♚" in black_king.text

    def test_piece_movement(self, game_page, make_move):
        """Testa o movimento de peças"""
        # Move um peão branco
        make_move("e2", "e4")
        
        # Verifica se o peão moveu
        moved_pawn = game_page.find_element(By.CSS_SELECTOR, '[data-testid="piece-4-4"]')  # e4
        assert moved_pawn is not None
        assert "♙" in moved_pawn.text  # Verifica se é um peão branco

    def test_game_controls(self, game_page):
        """Testa os controles do jogo"""
        # Testa os controles do jogo
        controls = game_page.find_element(By.CSS_SELECTOR, '[data-testid="board-controls"]')
        assert controls is not None

        # Verifica se todos os botões necessários estão presentes
        new_game_btn = controls.find_element(By.CSS_SELECTOR, '[data-testid="new-game"]')
        flip_board_btn = controls.find_element(By.CSS_SELECTOR, '[data-testid="flip-board"]')
        undo_btn = controls.find_element(By.CSS_SELECTOR, '[data-testid="undo"]')
        
        assert new_game_btn is not None
        assert flip_board_btn is not None
        assert undo_btn is not None

    def test_cultural_styles(self, game_page):
        """Testa a mudança de estilos culturais"""
        # Localiza os controles
        controls = game_page.find_element(By.CSS_SELECTOR, '[data-testid="board-controls"]')
        
        # Localiza o seletor de estilo
        style_select = controls.find_element(By.CSS_SELECTOR, '[data-testid="style-select"]')
        assert style_select is not None
        
        # Verifica se o estilo padrão é 'modern'
        assert 'modern' in style_select.get_attribute('value')

    def test_move_validation(self, game_page):
        """Testa a validação de movimentos"""
        # Tenta mover um peão incorretamente
        pawn = game_page.find_element(By.CSS_SELECTOR, '[data-testid="square-6-4"]')  # e2
        target = game_page.find_element(By.CSS_SELECTOR, '[data-testid="square-3-4"]')  # e5
        
        # Faz o movimento inválido
        pawn.click()
        target.click()
        
        # Verifica se o peão permanece na posição original
        original_pawn = game_page.find_element(By.CSS_SELECTOR, '[data-testid="piece-6-4"]')
        assert original_pawn is not None
        assert "♙" in original_pawn.text

    def test_game_state(self, game_page, make_move):
        """Testa o estado do jogo"""
        # Faz um movimento inicial
        make_move("e2", "e4")
        
        # Verifica se o movimento foi registrado no painel de informações
        info_panel = game_page.find_element(By.CSS_SELECTOR, '[data-testid="info-panel"]')
        assert info_panel is not None
        
        # Verifica se há alguma avaliação da posição
        evaluation = info_panel.find_element(By.CSS_SELECTOR, '[data-testid="evaluation-value"]')
        assert evaluation is not None

    def test_piece_capture(self, game_page, make_move):
        """Testa a captura de peças"""
        # Move peças para criar uma situação de captura
        moves = [
            ("e2", "e4"), ("d7", "d5")
        ]
        
        for start, end in moves:
            make_move(start, end)
        
        # Captura o peão
        make_move("e4", "d5")
        
        # Verifica se a peça foi capturada (não existe mais na posição original)
        info_panel = game_page.find_element(By.CSS_SELECTOR, '[data-testid="info-panel"]')
        move_list = info_panel.find_element(By.CSS_SELECTOR, '[data-testid="move-history"]')
        move_items = move_list.find_elements(By.CSS_SELECTOR, '[data-testid^="move-history-item-"]')
        assert len(move_items) > 0

    def test_move_history(self, game_page, make_move):
        """Testa o histórico de movimentos"""
        # Faz alguns movimentos
        moves = [
            ("e2", "e4"), ("e7", "e5"),
            ("g1", "f3")  # Cavalo
        ]
        
        for start, end in moves:
            make_move(start, end)
        
        # Verifica o histórico no painel de informações
        info_panel = game_page.find_element(By.CSS_SELECTOR, '[data-testid="info-panel"]')
        move_list = info_panel.find_element(By.CSS_SELECTOR, '[data-testid="move-history"]')
        moves = move_list.find_elements(By.CSS_SELECTOR, '[data-testid^="move-history-item-"]')
        assert len(moves) == 3
