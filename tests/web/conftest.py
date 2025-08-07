"""
Configuração específica para testes web.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def chrome_options():
    """Configura as opções do Chrome para os testes."""
    options = Options()
    options.add_argument("--headless=new")  # Novo modo headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Chrome no macOS
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    return options

@pytest.fixture(scope="session")
def chrome_service():
    """Configura o serviço do ChromeDriver."""
    service = Service()
    service.path = ChromeDriverManager().install()
    return service

@pytest.fixture(scope="session")
def browser(chrome_options, chrome_service):
    """Cria uma instância do navegador Chrome para os testes."""
    driver = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
    )
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def game_page(browser):
    """Carrega a página do jogo e aguarda ela estar pronta."""
    browser.get("http://localhost:3000")
    try:
        # Espera o tabuleiro carregar
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="chess-board"]'))
            )
            
            # Espera as peças carregarem (verificando uma peça específica)
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="piece-7-4"]'))  # Rei branco
            )
            
            # Espera os controles carregarem
            WebDriverWait(browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="board-controls"]'))
            )
    except Exception as e:
        pytest.fail(f"Página do jogo não carregou corretamente: {str(e)}")
    return browser

@pytest.fixture(scope="function")
def board_squares(game_page):
    """Retorna os quadrados do tabuleiro."""
    return game_page.find_elements(By.CSS_SELECTOR, "[data-testid^='square-']")

@pytest.fixture(scope="function")
def find_square(board_squares):
    """Função helper para encontrar um quadrado específico no tabuleiro."""
    def _find_square(position: str):
        # Converte notação algébrica para índices
        def algebraic_to_indices(pos):
            file = ord(pos[0].lower()) - ord('a')
            rank = 8 - int(pos[1])
            return (rank, file)
        
        row, col = algebraic_to_indices(position)
        try:
            return game_page.find_element(By.CSS_SELECTOR, f'[data-testid="square-{row}-{col}"]')
        except:
            pytest.fail(f"Quadrado {position} não encontrado no tabuleiro")
    return _find_square

@pytest.fixture(scope="function")
def make_move(game_page, find_square):
    """Função helper para fazer um movimento no tabuleiro."""
    def _make_move(from_pos: str, to_pos: str):
        from_square = find_square(from_pos)
        to_square = find_square(to_pos)
        
        # Clica na origem e depois no destino
        from_square.click()
        WebDriverWait(game_page, 5).until(
            EC.element_to_be_clickable(to_square)
        )
        to_square.click()
    return _make_move

@pytest.fixture(scope="function")
def get_piece(find_square):
    """Função helper para obter uma peça em uma posição específica."""
    def _get_piece(position: str):
        # Converte notação algébrica para índices
        def algebraic_to_indices(pos):
            file = ord(pos[0].lower()) - ord('a')
            rank = 8 - int(pos[1])
            return (rank, file)
        
        row, col = algebraic_to_indices(position)
        try:
            return game_page.find_element(By.CSS_SELECTOR, f'[data-testid="piece-{row}-{col}"]')
        except:
            return None
    return _get_piece

@pytest.fixture(scope="function")
def wait_for(game_page):
    """Helper para esperar por elementos na página."""
    def _wait_for(condition, timeout=10):
        return WebDriverWait(game_page, timeout).until(condition)
    return _wait_for
