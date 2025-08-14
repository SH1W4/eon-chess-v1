import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class TestChessInteractions:
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.get("http://localhost:3000")
        yield driver
        driver.quit()

    def test_drag_and_drop(self, driver):
        """Testa a funcionalidade de arrastar e soltar peças"""
        # Pega um peão branco
        pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e2']")
        target = driver.find_element(By.CSS_SELECTOR, "[data-square='e4']")
        
        # Testa arrastar e soltar
        ActionChains(driver).drag_and_drop(pawn, target).perform()
        
        # Verifica se o peão moveu
        moved_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e4']")
        assert moved_pawn is not None
        
        # Verifica se o movimento foi registrado no histórico
        move_history = driver.find_element(By.CLASS_NAME, "move-history")
        assert "e2-e4" in move_history.text

    def test_click_to_move(self, driver):
        """Testa o movimento por cliques"""
        # Seleciona um peão branco
        pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='d2']")
        pawn.click()
        
        # Verifica se as casas de movimento possível foram destacadas
        possible_moves = driver.find_elements(By.CLASS_NAME, "possible-move")
        assert len(possible_moves) > 0
        
        # Clica na casa de destino
        target = driver.find_element(By.CSS_SELECTOR, "[data-square='d4']")
        target.click()
        
        # Verifica se o peão moveu
        moved_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='d4']")
        assert moved_pawn is not None

    def test_invalid_moves(self, driver):
        """Testa a validação de movimentos inválidos"""
        # Tenta mover um peão três casas
        pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='c2']")
        invalid_target = driver.find_element(By.CSS_SELECTOR, "[data-square='c5']")
        
        pawn.click()
        invalid_target.click()
        
        # Verifica se o peão permaneceu na posição original
        original_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='c2']")
        assert original_pawn is not None
        
        # Verifica se uma mensagem de erro foi exibida
        error_message = driver.find_element(By.CLASS_NAME, "error-message")
        assert "Movimento inválido" in error_message.text

    def test_game_controls(self, driver):
        """Testa os controles do jogo"""
        # Testa o botão de novo jogo
        new_game_btn = driver.find_element(By.CLASS_NAME, "new-game-btn")
        new_game_btn.click()
        
        # Verifica se o tabuleiro foi resetado
        pieces = driver.find_elements(By.CLASS_NAME, "chess-piece")
        assert len(pieces) == 32
        
        # Testa o botão de inverter tabuleiro
        flip_board_btn = driver.find_element(By.CLASS_NAME, "flip-board-btn")
        flip_board_btn.click()
        
        # Verifica se o tabuleiro foi invertido
        board = driver.find_element(By.CLASS_NAME, "chess-board")
        assert "rotated" in board.get_attribute("class")
        
        # Testa o botão de desfazer
        pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e2']")
        target = driver.find_element(By.CSS_SELECTOR, "[data-square='e4']")
        pawn.click()
        target.click()
        
        undo_btn = driver.find_element(By.CLASS_NAME, "undo-btn")
        undo_btn.click()
        
        # Verifica se o movimento foi desfeito
        original_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e2']")
        assert original_pawn is not None

    def test_keyboard_navigation(self, driver):
        """Testa a navegação por teclado"""
        # Foca no tabuleiro
        board = driver.find_element(By.CLASS_NAME, "chess-board")
        board.click()
        
        # Move o foco usando as setas
        ActionChains(driver).send_keys(Keys.RIGHT).perform()
        
        # Verifica se a casa foi focada
        focused_square = driver.find_element(By.CLASS_NAME, "focused")
        assert focused_square is not None
        
        # Seleciona a peça com Enter
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        
        # Verifica se a peça foi selecionada
        selected_piece = driver.find_element(By.CLASS_NAME, "selected")
        assert selected_piece is not None
        
        # Move para uma casa válida
        ActionChains(driver).send_keys(Keys.UP).send_keys(Keys.UP).perform()
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        
        # Verifica se o movimento foi realizado
        move_history = driver.find_element(By.CLASS_NAME, "move-history")
        assert len(move_history.text) > 0

    def test_special_moves(self, driver):
        """Testa movimentos especiais (roque, en passant, promoção)"""
        # Prepara o tabuleiro para roque
        moves = [
            ("e2", "e4"), ("e7", "e6"),
            ("g1", "f3"), ("d7", "d6"),
            ("f1", "c4"), ("g8", "f6")
        ]
        
        for start, end in moves:
            piece = driver.find_element(By.CSS_SELECTOR, f"[data-square='{start}']")
            target = driver.find_element(By.CSS_SELECTOR, f"[data-square='{end}']")
            piece.click()
            target.click()
        
        # Testa o roque
        king = driver.find_element(By.CSS_SELECTOR, "[data-piece='wk'][data-position='e1']")
        king.click()
        
        castle_square = driver.find_element(By.CSS_SELECTOR, "[data-square='g1']")
        castle_square.click()
        
        # Verifica se o roque foi realizado
        castled_king = driver.find_element(By.CSS_SELECTOR, "[data-piece='wk'][data-position='g1']")
        castled_rook = driver.find_element(By.CSS_SELECTOR, "[data-piece='wr'][data-position='f1']")
        assert castled_king is not None
        assert castled_rook is not None

    def test_game_state_indicators(self, driver):
        """Testa os indicadores de estado do jogo"""
        # Move para criar um xeque
        moves = [
            ("f2", "f3"), ("e7", "e6"),
            ("g2", "g4"), ("Qd8", "h4")
        ]
        
        for start, end in moves:
            piece = driver.find_element(By.CSS_SELECTOR, f"[data-square='{start}']")
            target = driver.find_element(By.CSS_SELECTOR, f"[data-square='{end}']")
            piece.click()
            target.click()
        
        # Verifica o indicador de xeque-mate
        checkmate_indicator = driver.find_element(By.CLASS_NAME, "checkmate-indicator")
        assert checkmate_indicator.is_displayed()
        assert "Xeque-mate" in checkmate_indicator.text
        
        # Inicia um novo jogo
        new_game_btn = driver.find_element(By.CLASS_NAME, "new-game-btn")
        new_game_btn.click()
        
        # Move para criar um xeque
        moves = [
            ("e2", "e4"), ("f7", "f6"),
            ("Qd1", "h5")
        ]
        
        for start, end in moves:
            piece = driver.find_element(By.CSS_SELECTOR, f"[data-square='{start}']")
            target = driver.find_element(By.CSS_SELECTOR, f"[data-square='{end}']")
            piece.click()
            target.click()
        
        # Verifica o indicador de xeque
        check_indicator = driver.find_element(By.CLASS_NAME, "check-indicator")
        assert check_indicator.is_displayed()
        assert "Xeque" in check_indicator.text

    def test_game_history(self, driver):
        """Testa a funcionalidade do histórico de movimentos"""
        # Faz alguns movimentos
        moves = [
            ("e2", "e4"), ("e7", "e5"),
            ("g1", "f3"), ("b8", "c6")
        ]
        
        for start, end in moves:
            piece = driver.find_element(By.CSS_SELECTOR, f"[data-square='{start}']")
            target = driver.find_element(By.CSS_SELECTOR, f"[data-square='{end}']")
            piece.click()
            target.click()
        
        # Abre o histórico
        history_btn = driver.find_element(By.CLASS_NAME, "history-btn")
        history_btn.click()
        
        # Verifica se todos os movimentos estão listados
        move_list = driver.find_elements(By.CLASS_NAME, "move-history-item")
        assert len(move_list) == 4
        
        # Clica em um movimento anterior
        move_list[1].click()
        
        # Verifica se o tabuleiro voltou para aquela posição
        board_state = driver.find_element(By.CLASS_NAME, "board-state")
        assert "1. e4 e5" in board_state.text
