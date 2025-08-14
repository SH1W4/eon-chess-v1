import pytest
from core.board.board import Board, Color, PieceType, Piece

@pytest.fixture
def board():
    return Board()

def test_check_detection(board):
    """Testa detecção de xeque."""
    # Setup: posição de xeque simples
    # Rei branco em e1, Rainha preta em e7
    board.pieces.clear()
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["e7"] = Piece(PieceType.QUEEN, Color.BLACK)
    board.current_turn = Color.WHITE
    
    assert board.is_in_check()

def test_checkmate_detection(board):
    """Testa detecção de xeque-mate.
    Cenário mínimo: Rei branco em h1, rainha preta em g2 (xeque), protegida por bispo em b7.
    Todas as casas de fuga (g1, h2) estão sob ataque; capturar g2 é ilegal (protegida).
    """
    board.pieces.clear()
    board.pieces["h1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["g2"] = Piece(PieceType.QUEEN, Color.BLACK)
    board.pieces["b7"] = Piece(PieceType.BISHOP, Color.BLACK)
    board.pieces["a8"] = Piece(PieceType.KING, Color.BLACK)
    board.current_turn = Color.WHITE

    assert board.is_checkmate()

def test_stalemate_detection(board):
    """Testa detecção de empate por afogamento."""
    # Setup: rei branco afogado
    board.pieces.clear()
    board.pieces["h8"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["f7"] = Piece(PieceType.QUEEN, Color.BLACK)
    board.pieces["g6"] = Piece(PieceType.KING, Color.BLACK)
    board.current_turn = Color.WHITE
    
    assert board.is_stalemate()

def test_insufficient_material(board):
    """Testa detecção de empate por material insuficiente."""
    # Setup: rei vs rei
    board.pieces.clear()
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["e8"] = Piece(PieceType.KING, Color.BLACK)
    
    assert board.is_stalemate()
    
    # Setup: rei e bispo vs rei
    board.pieces["c1"] = Piece(PieceType.BISHOP, Color.WHITE)
    assert board.is_stalemate()

def test_valid_moves_under_check(board):
    """Testa geração de movimentos válidos sob xeque."""
    # Setup: rei branco em xeque pela rainha
    board.pieces.clear()
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["e7"] = Piece(PieceType.QUEEN, Color.BLACK)
    board.pieces["d2"] = Piece(PieceType.PAWN, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Deve haver movimentos válidos para escapar do xeque
    assert board._has_legal_moves()

def test_move_into_check(board):
    """Testa prevenção de movimento que expõe ao xeque."""
    # Setup
    board.pieces.clear()
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["d1"] = Piece(PieceType.ROOK, Color.WHITE)
    board.pieces["e8"] = Piece(PieceType.ROOK, Color.BLACK)
    board.current_turn = Color.WHITE
    
    # Tentar mover a torre deve falhar pois expõe o rei
    result = board.move_piece("d1", "d4")
    assert not result["success"]
    assert "expõe o rei ao xeque" in result["error"]

def test_pawn_moves(board):
    """Testa validação de movimentos de peão."""
    # Setup: posição inicial
    board.pieces.clear()
    board.pieces["e2"] = Piece(PieceType.PAWN, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimento simples para frente
    assert board._is_valid_move(board.pieces["e2"], "e2", "e3")
    
    # Movimento duplo inicial
    assert board._is_valid_move(board.pieces["e2"], "e2", "e4")
    
    # Movimento diagonal sem captura (inválido)
    assert not board._is_valid_move(board.pieces["e2"], "e2", "d3")
    
    # Movimento diagonal com captura
    board.pieces["d3"] = Piece(PieceType.PAWN, Color.BLACK)
    assert board._is_valid_move(board.pieces["e2"], "e2", "d3")

def test_knight_moves(board):
    """Testa validação de movimentos de cavalo."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.KNIGHT, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimentos em L válidos
    valid_moves = ["f6", "g5", "g3", "f2", "d2", "c3", "c5", "d6"]
    for move in valid_moves:
        assert board._is_valid_move(board.pieces["e4"], "e4", move)
    
    # Movimento inválido
    assert not board._is_valid_move(board.pieces["e4"], "e4", "e5")

def test_bishop_moves(board):
    """Testa validação de movimentos de bispo."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.BISHOP, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimento diagonal válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "c6")
    
    # Movimento bloqueado
    board.pieces["d5"] = Piece(PieceType.PAWN, Color.WHITE)
    assert not board._is_valid_move(board.pieces["e4"], "e4", "c6")
    
    # Movimento não diagonal
    assert not board._is_valid_move(board.pieces["e4"], "e4", "e5")

def test_rook_moves(board):
    """Testa validação de movimentos de torre."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.ROOK, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimento vertical válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "e8")
    
    # Movimento horizontal válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "a4")
    
    # Movimento bloqueado
    board.pieces["e6"] = Piece(PieceType.PAWN, Color.WHITE)
    assert not board._is_valid_move(board.pieces["e4"], "e4", "e8")
    
    # Movimento diagonal (inválido)
    assert not board._is_valid_move(board.pieces["e4"], "e4", "f5")

def test_queen_moves(board):
    """Testa validação de movimentos de rainha."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.QUEEN, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimento diagonal válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "h7")
    
    # Movimento vertical válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "e8")
    
    # Movimento horizontal válido
    assert board._is_valid_move(board.pieces["e4"], "e4", "a4")
    
    # Movimento bloqueado
    board.pieces["f5"] = Piece(PieceType.PAWN, Color.WHITE)
    assert not board._is_valid_move(board.pieces["e4"], "e4", "h7")

def test_king_moves(board):
    """Testa validação de movimentos de rei."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.KING, Color.WHITE)
    board.current_turn = Color.WHITE
    
    # Movimentos válidos (uma casa em qualquer direção)
    valid_moves = ["e5", "f5", "f4", "f3", "e3", "d3", "d4", "d5"]
    for move in valid_moves:
        assert board._is_valid_move(board.pieces["e4"], "e4", move)
    
    # Movimento inválido (duas casas)
    assert not board._is_valid_move(board.pieces["e4"], "e4", "e6")

def test_path_clear(board):
    """Testa verificação de caminho livre."""
    # Setup
    board.pieces.clear()
    board.pieces["e4"] = Piece(PieceType.QUEEN, Color.WHITE)
    
    # Caminho livre
    assert board._is_path_clear("e4", "e8")
    
    # Caminho bloqueado
    board.pieces["e6"] = Piece(PieceType.PAWN, Color.BLACK)
    assert not board._is_path_clear("e4", "e8")

def test_en_passant(board):
    """Testa validação de en passant (alvo)."""
    # Setup
    board.pieces.clear()
    board.pieces["e5"] = Piece(PieceType.PAWN, Color.WHITE)
    board.pieces["d5"] = Piece(PieceType.PAWN, Color.BLACK)
    board.current_turn = Color.WHITE
    board.last_move = ("d7", "d5")  # Peão preto acabou de mover duas casas
    
    # En passant deve ser possível na casa atrás do peão que avançou
    assert board._is_en_passant_target("d6")
    
    # Após outro movimento, en passant não deve ser mais possível
    board.last_move = ("e5", "e6")
    assert not board._is_en_passant_target("d6")

def test_en_passant_execution(board):
    """Testa execução de en passant."""
    board.pieces.clear()
    # Peão branco em e5, peão preto em d5 acabou de avançar de d7 para d5
    board.pieces["e5"] = Piece(PieceType.PAWN, Color.WHITE)
    board.pieces["d5"] = Piece(PieceType.PAWN, Color.BLACK)
    board.current_turn = Color.WHITE
    board.last_move = ("d7", "d5")
    
    # Executa en passant: e5 -> d6
    result = board.move_piece("e5", "d6")
    assert result["success"], result
    # Verifica que o peão preto de d5 foi capturado
    assert "d5" not in board.pieces
    # Verifica posição do peão branco
    assert "d6" in board.pieces and board.pieces["d6"].type == PieceType.PAWN and board.pieces["d6"].color == Color.WHITE


def test_castle_kingside_blocked_by_attack(board):
    """Roque deve falhar se a casa de passagem/chegada estiver sob ataque."""
    board.pieces.clear()
    # Rei e torre brancos prontos para roque
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["h1"] = Piece(PieceType.ROOK, Color.WHITE)
    # Bispo preto ataca f1
    board.pieces["c4"] = Piece(PieceType.BISHOP, Color.BLACK)
    board.current_turn = Color.WHITE
    
    result = board.move_piece("e1", "g1")
    assert not result["success"]
    assert "atacada" in result["error"] or "xeque" in result["error"]


def test_castle_kingside_success(board):
    """Roque do lado do rei deve funcionar com caminho livre e sem ataques."""
    board.pieces.clear()
    board.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
    board.pieces["h1"] = Piece(PieceType.ROOK, Color.WHITE)
    board.pieces["e8"] = Piece(PieceType.KING, Color.BLACK)  # evitar estados estranhos de xeque por ausência de rei adversário
    board.current_turn = Color.WHITE
    
    result = board.move_piece("e1", "g1")
    assert result["success"], result
    # Rei deve estar em g1 e torre em f1
    assert "g1" in board.pieces and board.pieces["g1"].type == PieceType.KING and board.pieces["g1"].color == Color.WHITE
    assert "f1" in board.pieces and board.pieces["f1"].type == PieceType.ROOK and board.pieces["f1"].color == Color.WHITE
    # Antigas casas devem estar vazias
    assert "e1" not in board.pieces and "h1" not in board.pieces
    
