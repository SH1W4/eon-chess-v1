"""
Testes para movimentos especiais: En Passant e Promoção
"""

import pytest
from src.core.special_moves import (
    SpecialMovesHandler, 
    SpecialMoveType,
    MoveValidator
)
from src.core.board.board import Board, Position, Piece, PieceType, Color


class TestEnPassant:
    """Testes para captura en passant"""
    
    def test_en_passant_setup_white(self):
        """Testa configuração de en passant para peão branco"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão branco move 2 casas
        from_pos = Position(2, 4)  # e2
        to_pos = Position(4, 4)    # e4
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = from_pos
        
        handler.update_en_passant_state(from_pos, to_pos, pawn, board)
        
        # Verifica que en passant foi configurado
        assert handler.en_passant_state.target_square == Position(3, 4)  # e3
        assert handler.en_passant_state.vulnerable_pawn == to_pos
        
    def test_en_passant_setup_black(self):
        """Testa configuração de en passant para peão preto"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão preto move 2 casas
        from_pos = Position(7, 4)  # e7
        to_pos = Position(5, 4)    # e5
        pawn = Piece(PieceType.PAWN, Color.BLACK)
        pawn.position = from_pos
        
        handler.update_en_passant_state(from_pos, to_pos, pawn, board)
        
        # Verifica que en passant foi configurado
        assert handler.en_passant_state.target_square == Position(6, 4)  # e6
        assert handler.en_passant_state.vulnerable_pawn == to_pos
    
    def test_en_passant_capture_validation(self):
        """Testa validação de captura en passant"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Setup: peão preto vulnerável
        black_pawn_pos = Position(5, 4)  # e5
        black_pawn = Piece(PieceType.PAWN, Color.BLACK)
        black_pawn.position = black_pawn_pos
        board.pieces[black_pawn_pos] = black_pawn
        
        # Configura estado en passant
        handler.en_passant_state.target_square = Position(6, 4)  # e6
        handler.en_passant_state.vulnerable_pawn = black_pawn_pos
        handler.en_passant_state.expires_on_move = 10
        
        # Peão branco tenta capturar
        white_pawn_pos = Position(5, 5)  # f5
        white_pawn = Piece(PieceType.PAWN, Color.WHITE)
        white_pawn.position = white_pawn_pos
        board.pieces[white_pawn_pos] = white_pawn
        
        # Verifica que é captura en passant válida
        assert handler.is_en_passant_capture(
            white_pawn_pos, 
            Position(6, 4),  # e6 (casa en passant)
            white_pawn, 
            board
        )
    
    def test_en_passant_execution(self):
        """Testa execução de captura en passant"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Setup
        black_pawn_pos = Position(5, 4)  # e5
        white_pawn_pos = Position(5, 5)  # f5
        
        black_pawn = Piece(PieceType.PAWN, Color.BLACK)
        black_pawn.position = black_pawn_pos
        board.pieces[black_pawn_pos] = black_pawn
        
        white_pawn = Piece(PieceType.PAWN, Color.WHITE)
        white_pawn.position = white_pawn_pos
        board.pieces[white_pawn_pos] = white_pawn
        
        handler.en_passant_state.target_square = Position(6, 4)  # e6
        handler.en_passant_state.vulnerable_pawn = black_pawn_pos
        
        # Executa en passant
        captured = handler.execute_en_passant(white_pawn_pos, Position(6, 4), board)
        
        # Verifica resultado
        assert captured.type == PieceType.PAWN
        assert captured.color == Color.BLACK
        assert Position(6, 4) in board.pieces  # Peão branco na casa en passant
        assert black_pawn_pos not in board.pieces  # Peão preto removido
        assert white_pawn_pos not in board.pieces  # Posição original vazia
    
    def test_en_passant_expiration(self):
        """Testa expiração do en passant"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Configura en passant
        handler.en_passant_state.target_square = Position(6, 4)
        handler.en_passant_state.expires_on_move = 2
        handler.move_count = 2
        
        # Atualiza com movimento qualquer (expira en passant)
        piece = Piece(PieceType.KNIGHT, Color.WHITE)
        piece.position = Position(1, 1)
        handler.update_en_passant_state(Position(1, 1), Position(3, 2), piece, board)
        
        # Verifica que en passant expirou
        assert handler.en_passant_state.target_square is None


class TestPromotion:
    """Testes para promoção de peão"""
    
    def test_promotion_detection_white(self):
        """Testa detecção de promoção para peão branco"""
        handler = SpecialMovesHandler()
        
        # Peão branco chegando na rank 8
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = Position(7, 4)
        
        assert handler.is_promotion_move(Position(7, 4), Position(8, 4), pawn)
        assert not handler.is_promotion_move(Position(6, 4), Position(7, 4), pawn)
    
    def test_promotion_detection_black(self):
        """Testa detecção de promoção para peão preto"""
        handler = SpecialMovesHandler()
        
        # Peão preto chegando na rank 1
        pawn = Piece(PieceType.PAWN, Color.BLACK)
        pawn.position = Position(2, 4)
        
        assert handler.is_promotion_move(Position(2, 4), Position(1, 4), pawn)
        assert not handler.is_promotion_move(Position(3, 4), Position(2, 4), pawn)
    
    def test_promotion_choices(self):
        """Testa opções de promoção"""
        handler = SpecialMovesHandler()
        choices = handler.get_promotion_choices()
        
        assert PieceType.QUEEN in choices
        assert PieceType.ROOK in choices
        assert PieceType.BISHOP in choices
        assert PieceType.KNIGHT in choices
        assert PieceType.KING not in choices
        assert PieceType.PAWN not in choices
    
    def test_promotion_execution_to_queen(self):
        """Testa execução de promoção para rainha"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão branco na rank 8
        pawn_pos = Position(8, 4)  # e8
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = pawn_pos
        board.pieces[pawn_pos] = pawn
        
        # Promove para rainha
        new_piece = handler.execute_promotion(pawn_pos, PieceType.QUEEN, board)
        
        # Verifica resultado
        assert new_piece.type == PieceType.QUEEN
        assert new_piece.color == Color.WHITE
        assert board.get_piece(pawn_pos).type == PieceType.QUEEN
    
    def test_promotion_execution_to_knight(self):
        """Testa execução de promoção para cavalo"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão preto na rank 1
        pawn_pos = Position(1, 4)  # e1
        pawn = Piece(PieceType.PAWN, Color.BLACK)
        pawn.position = pawn_pos
        board.pieces[pawn_pos] = pawn
        
        # Promove para cavalo
        new_piece = handler.execute_promotion(pawn_pos, PieceType.KNIGHT, board)
        
        # Verifica resultado
        assert new_piece.type == PieceType.KNIGHT
        assert new_piece.color == Color.BLACK
        assert board.get_piece(pawn_pos).type == PieceType.KNIGHT
    
    def test_invalid_promotion_position(self):
        """Testa promoção em posição inválida"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão branco na rank 7 (não pode promover ainda)
        pawn_pos = Position(7, 4)  # e7
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = pawn_pos
        board.pieces[pawn_pos] = pawn
        
        # Tenta promover
        with pytest.raises(ValueError, match="rank 8"):
            handler.execute_promotion(pawn_pos, PieceType.QUEEN, board)
    
    def test_invalid_promotion_piece_type(self):
        """Testa promoção para tipo inválido"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Peão branco na rank 8
        pawn_pos = Position(8, 4)
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = pawn_pos
        board.pieces[pawn_pos] = pawn
        
        # Tenta promover para rei
        with pytest.raises(ValueError, match="inválido"):
            handler.execute_promotion(pawn_pos, PieceType.KING, board)


class TestMoveValidator:
    """Testes para validador de movimentos com movimentos especiais"""
    
    def test_pawn_normal_move(self):
        """Testa movimento normal de peão"""
        board = Board()
        validator = MoveValidator()
        
        # Peão branco
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = Position(2, 4)
        board.pieces[Position(2, 4)] = pawn
        
        # Movimento simples válido
        assert validator.is_valid_pawn_move(
            Position(2, 4), Position(3, 4), pawn, board
        )
        
        # Movimento duplo inicial válido
        assert validator.is_valid_pawn_move(
            Position(2, 4), Position(4, 4), pawn, board
        )
    
    def test_pawn_capture_move(self):
        """Testa captura de peão"""
        board = Board()
        validator = MoveValidator()
        
        # Setup
        white_pawn = Piece(PieceType.PAWN, Color.WHITE)
        white_pawn.position = Position(4, 4)
        black_pawn = Piece(PieceType.PAWN, Color.BLACK)
        black_pawn.position = Position(5, 5)
        
        board.pieces[Position(4, 4)] = white_pawn
        board.pieces[Position(5, 5)] = black_pawn
        
        # Captura diagonal válida
        assert validator.is_valid_pawn_move(
            Position(4, 4), Position(5, 5), white_pawn, board
        )
    
    def test_special_move_detection(self):
        """Testa detecção de movimentos especiais"""
        board = Board()
        handler = SpecialMovesHandler()
        
        # Testa detecção de promoção
        pawn = Piece(PieceType.PAWN, Color.WHITE)
        pawn.position = Position(7, 4)
        board.pieces[Position(7, 4)] = pawn
        
        special_type = handler.validate_special_move(
            Position(7, 4), Position(8, 4), pawn, board
        )
        
        assert special_type == SpecialMoveType.PROMOTION
