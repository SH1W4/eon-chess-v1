import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestChessStyles:
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        driver.get("http://localhost:3000")
        yield driver
        driver.quit()

    def test_board_colors(self, driver):
        """Testa as cores do tabuleiro para diferentes estilos"""
        styles = ['modern', 'ancient', 'medieval']
        
        for style in styles:
            # Seleciona o estilo
            style_select = driver.find_element(By.CLASS_NAME, "style-select")
            style_select.click()
            option = driver.find_element(By.CSS_SELECTOR, f"option[value='{style}']")
            option.click()
            
            # Verifica as cores das casas
            light_squares = driver.find_elements(By.CLASS_NAME, "square-light")
            dark_squares = driver.find_elements(By.CLASS_NAME, "square-dark")
            
            # Verifica se as cores correspondem ao estilo
            if style == 'modern':
                assert "bg-[#f0d9b5]" in light_squares[0].get_attribute("class")
                assert "bg-[#b58863]" in dark_squares[0].get_attribute("class")
            elif style == 'ancient':
                assert "bg-[#e6d5ac]" in light_squares[0].get_attribute("class")
                assert "bg-[#7c6c54]" in dark_squares[0].get_attribute("class")
            elif style == 'medieval':
                assert "bg-[#eed2a4]" in light_squares[0].get_attribute("class")
                assert "bg-[#8b4513]" in dark_squares[0].get_attribute("class")

    def test_piece_styles(self, driver):
        """Testa os estilos das peças para diferentes temas"""
        styles = ['modern', 'ancient', 'medieval']
        
        for style in styles:
            # Seleciona o estilo
            style_select = driver.find_element(By.CLASS_NAME, "style-select")
            style_select.click()
            option = driver.find_element(By.CSS_SELECTOR, f"option[value='{style}']")
            option.click()
            
            # Verifica o estilo das peças
            white_king = driver.find_element(By.CSS_SELECTOR, "[data-piece='wk']")
            black_queen = driver.find_element(By.CSS_SELECTOR, "[data-piece='bq']")
            
            if style == 'modern':
                assert "traditional" in white_king.get_attribute("class")
            elif style == 'ancient':
                assert "hieroglyphic" in white_king.get_attribute("class")
            elif style == 'medieval':
                assert "artistic" in white_king.get_attribute("class")

    def test_ui_elements_style(self, driver):
        """Testa os estilos dos elementos da interface"""
        styles = ['modern', 'ancient', 'medieval']
        
        for style in styles:
            # Seleciona o estilo
            style_select = driver.find_element(By.CLASS_NAME, "style-select")
            style_select.click()
            option = driver.find_element(By.CSS_SELECTOR, f"option[value='{style}']")
            option.click()
            
            # Verifica os estilos dos botões
            buttons = driver.find_elements(By.CLASS_NAME, "game-button")
            for button in buttons:
                assert f"bg-pattern-{style}" in button.get_attribute("style")
            
            # Verifica o estilo do container do tabuleiro
            board_container = driver.find_element(By.CLASS_NAME, "board-container")
            assert f"bg-gradient-{style}" in board_container.get_attribute("class")

    def test_special_states_style(self, driver):
        """Testa os estilos de estados especiais (seleção, último movimento, movimento possível)"""
        # Seleciona uma peça
        piece = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e2']")
        piece.click()
        
        # Verifica o estilo da casa selecionada
        selected_square = driver.find_element(By.CLASS_NAME, "selected")
        assert "ring-2" in selected_square.get_attribute("class")
        assert "ring-yellow-400" in selected_square.get_attribute("class")
        
        # Verifica o estilo dos movimentos possíveis
        possible_moves = driver.find_elements(By.CLASS_NAME, "possible-move")
        for move in possible_moves:
            assert "bg-yellow-400" in move.get_attribute("class")
            assert "opacity-50" in move.get_attribute("class")
        
        # Faz um movimento e verifica o estilo do último movimento
        target = driver.find_element(By.CSS_SELECTOR, "[data-square='e4']")
        target.click()
        
        last_move_squares = driver.find_elements(By.CLASS_NAME, "last-move")
        for square in last_move_squares:
            assert "ring-2" in square.get_attribute("class")
            assert "ring-green-400" in square.get_attribute("class")

    def test_responsive_design(self, driver):
        """Testa o design responsivo do tabuleiro"""
        # Testa diferentes tamanhos de tela
        screen_sizes = [
            (375, 667),  # iPhone SE
            (768, 1024), # iPad
            (1280, 800), # Desktop
            (1920, 1080) # Full HD
        ]
        
        for width, height in screen_sizes:
            driver.set_window_size(width, height)
            
            # Verifica se o tabuleiro se ajusta ao tamanho da tela
            board = driver.find_element(By.CLASS_NAME, "chess-board")
            board_size = board.size
            
            # O tabuleiro deve ser quadrado
            assert abs(board_size['width'] - board_size['height']) <= 1
            
            # O tabuleiro não deve ultrapassar a largura da tela
            assert board_size['width'] <= width
            
            # Verifica se as peças se ajustam corretamente
            pieces = driver.find_elements(By.CLASS_NAME, "chess-piece")
            piece_size = pieces[0].size
            
            # As peças devem caber nas casas do tabuleiro
            assert piece_size['width'] <= board_size['width'] / 8
            assert piece_size['height'] <= board_size['height'] / 8

    def test_animation_styles(self, driver):
        """Testa as animações do jogo"""
        # Testa animação de movimento de peça
        piece = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e2']")
        target = driver.find_element(By.CSS_SELECTOR, "[data-square='e4']")
        
        # Verifica a transição antes do movimento
        assert "transition-transform" in piece.get_attribute("class")
        assert "duration-150" in piece.get_attribute("class")
        
        # Move a peça
        piece.click()
        target.click()
        
        # Espera a animação completar
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-piece='wp'][data-position='e4']"))
        )
        
        # Testa animação de captura
        # Primeiro, move um peão preto para uma posição de captura
        black_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='bp'][data-position='d7']")
        capture_setup = driver.find_element(By.CSS_SELECTOR, "[data-square='d5']")
        black_pawn.click()
        capture_setup.click()
        
        # Agora move o peão branco para capturar
        white_pawn = driver.find_element(By.CSS_SELECTOR, "[data-piece='wp'][data-position='e4']")
        capture_target = driver.find_element(By.CSS_SELECTOR, "[data-square='d5']")
        
        # Verifica a animação de destaque da captura
        white_pawn.click()
        assert "ring-2" in capture_target.get_attribute("class")
        assert "ring-yellow-400" in capture_target.get_attribute("class")
        
        # Realiza a captura
        capture_target.click()
        
        # Verifica a animação de fade-out da peça capturada
        captured_piece = driver.find_element(By.CLASS_NAME, "captured-animation")
        assert "opacity-0" in captured_piece.get_attribute("class")
        assert "transition-opacity" in captured_piece.get_attribute("class")
