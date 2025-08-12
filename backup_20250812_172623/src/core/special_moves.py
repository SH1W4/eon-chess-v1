"""
Implementação de movimentos especiais: En Passant e Promoção de Peões
Seguindo o workflow SYMBIOTIC_ARQUIMAX_NEXUS
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

from src.core.board.board import Position, PieceType, Color, Piece


class SpecialMoveType(Enum):
    """Tipos de movimentos especiais"""
    EN_PASSANT = "en_passant"
    PROMOTION = "promotion"
    CASTLE_KINGSIDE = "castle_kingside"
    CASTLE_QUEENSIDE = "castle_queenside"


@dataclass
class EnPassantState:
    """Estado do en passant"""
    target_square: Optional[Position] = None  # Casa onde o peão pode ser capturado
    vulnerable_pawn: Optional[Position] = None  # Posição do peão vulnerável
    expires_on_move: int = 0  # Movimento em que expira


class SpecialMovesHandler:
    """Gerenciador de movimentos especiais do xadrez"""
    
    def __init__(self):
        self.en_passant_state = EnPassantState()
        self.move_count = 0
        
    def update_en_passant_state(self, from_pos: Position, to_pos: Position, 
                                piece: Piece, board) -> None:
        """
        Atualiza o estado do en passant após um movimento
        
        En passant é possível quando:
        1. Um peão move 2 casas da posição inicial
        2. Passa por uma casa onde poderia ser capturado por peão adversário
        """
        # Limpa estado anterior se expirou
        if self.move_count >= self.en_passant_state.expires_on_move:
            self.en_passant_state = EnPassantState()
        
        # Verifica se é movimento de peão de 2 casas
        if piece.type == PieceType.PAWN:
            rank_diff = abs(to_pos.rank - from_pos.rank)
            
            if rank_diff == 2:
                # Peão moveu 2 casas, pode ser vulnerável a en passant
                if piece.color == Color.WHITE:
                    # Peão branco subiu 2 casas (rank 2 -> 4)
                    if from_pos.rank == 2 and to_pos.rank == 4:
                        # Casa de captura en passant é rank 3
                        self.en_passant_state.target_square = Position(3, to_pos.file)
                        self.en_passant_state.vulnerable_pawn = to_pos
                        self.en_passant_state.expires_on_move = self.move_count + 2
                else:
                    # Peão preto desceu 2 casas (rank 7 -> 5)
                    if from_pos.rank == 7 and to_pos.rank == 5:
                        # Casa de captura en passant é rank 6
                        self.en_passant_state.target_square = Position(6, to_pos.file)
                        self.en_passant_state.vulnerable_pawn = to_pos
                        self.en_passant_state.expires_on_move = self.move_count + 2
        
        self.move_count += 1
    
    def is_en_passant_capture(self, from_pos: Position, to_pos: Position, 
                              piece: Piece, board) -> bool:
        """
        Verifica se um movimento é captura en passant válida
        
        Condições:
        1. Peça movendo é um peão
        2. Movimento é diagonal
        3. Casa destino está vazia
        4. Casa destino é a casa de en passant atual
        5. Há um peão adversário na posição vulnerável
        """
        if piece.type != PieceType.PAWN:
            return False
            
        # Verifica se é movimento diagonal
        file_diff = abs(to_pos.file - from_pos.file)
        rank_diff = abs(to_pos.rank - from_pos.rank)
        
        if file_diff != 1 or rank_diff != 1:
            return False
        
        # Verifica se a casa destino está vazia
        if board.get_piece(to_pos) is not None:
            return False
        
        # Verifica se é a casa de en passant atual
        if (self.en_passant_state.target_square and 
            to_pos == self.en_passant_state.target_square):
            
            # Verifica se há peão vulnerável
            if self.en_passant_state.vulnerable_pawn:
                vulnerable_piece = board.get_piece(self.en_passant_state.vulnerable_pawn)
                if (vulnerable_piece and 
                    vulnerable_piece.type == PieceType.PAWN and
                    vulnerable_piece.color != piece.color):
                    return True
        
        return False
    
    def execute_en_passant(self, from_pos: Position, to_pos: Position, board) -> Piece:
        """
        Executa captura en passant
        
        Returns:
            Peça capturada
        """
        # Move o peão para a casa de destino
        moving_pawn = board.get_piece(from_pos)
        board.pieces[to_pos] = moving_pawn
        moving_pawn.position = to_pos
        del board.pieces[from_pos]
        
        # Remove o peão capturado
        captured_pawn = board.get_piece(self.en_passant_state.vulnerable_pawn)
        del board.pieces[self.en_passant_state.vulnerable_pawn]
        
        # Limpa estado en passant
        self.en_passant_state = EnPassantState()
        
        return captured_pawn
    
    def is_promotion_move(self, from_pos: Position, to_pos: Position, 
                         piece: Piece) -> bool:
        """
        Verifica se um movimento resulta em promoção de peão
        
        Promoção ocorre quando:
        - Peão branco chega na rank 8
        - Peão preto chega na rank 1
        """
        if piece.type != PieceType.PAWN:
            return False
        
        if piece.color == Color.WHITE and to_pos.rank == 8:
            return True
        elif piece.color == Color.BLACK and to_pos.rank == 1:
            return True
        
        return False
    
    def get_promotion_choices(self) -> List[PieceType]:
        """
        Retorna as opções de promoção disponíveis
        
        Padrão: Rainha, Torre, Bispo, Cavalo
        """
        return [
            PieceType.QUEEN,
            PieceType.ROOK,
            PieceType.BISHOP,
            PieceType.KNIGHT
        ]
    
    def execute_promotion(self, pawn_pos: Position, new_piece_type: PieceType, 
                         board) -> Piece:
        """
        Executa promoção de peão
        
        Args:
            pawn_pos: Posição do peão a ser promovido
            new_piece_type: Tipo da nova peça
            board: Tabuleiro
            
        Returns:
            Nova peça criada
        """
        pawn = board.get_piece(pawn_pos)
        if not pawn or pawn.type != PieceType.PAWN:
            raise ValueError("Não há peão na posição especificada")
        
        # Valida que é posição de promoção
        if pawn.color == Color.WHITE and pawn_pos.rank != 8:
            raise ValueError("Peão branco deve estar na rank 8 para promoção")
        elif pawn.color == Color.BLACK and pawn_pos.rank != 1:
            raise ValueError("Peão preto deve estar na rank 1 para promoção")
        
        # Valida tipo de peça
        if new_piece_type not in self.get_promotion_choices():
            raise ValueError(f"Tipo de peça inválido para promoção: {new_piece_type}")
        
        # Cria nova peça
        new_piece = Piece(new_piece_type, pawn.color, pawn_pos)
        
        # Substitui peão pela nova peça
        board.pieces[pawn_pos] = new_piece
        
        return new_piece
    
    def validate_special_move(self, from_pos: Position, to_pos: Position, 
                             piece: Piece, board) -> Optional[SpecialMoveType]:
        """
        Valida e identifica movimentos especiais
        
        Returns:
            Tipo do movimento especial ou None
        """
        # Verifica en passant
        if self.is_en_passant_capture(from_pos, to_pos, piece, board):
            return SpecialMoveType.EN_PASSANT
        
        # Verifica promoção
        if self.is_promotion_move(from_pos, to_pos, piece):
            return SpecialMoveType.PROMOTION
        
        # Verifica roque (já implementado em outro lugar)
        if piece.type == PieceType.KING:
            file_diff = abs(to_pos.file - from_pos.file)
            if file_diff == 2:
                if to_pos.file > from_pos.file:
                    return SpecialMoveType.CASTLE_KINGSIDE
                else:
                    return SpecialMoveType.CASTLE_QUEENSIDE
        
        return None


class MoveValidator:
    """Validador de movimentos com suporte a movimentos especiais"""
    
    def __init__(self, special_handler: Optional[SpecialMovesHandler] = None):
        self.special_handler = special_handler or SpecialMovesHandler()
    
    def is_valid_pawn_move(self, from_pos: Position, to_pos: Position, 
                           piece: Piece, board, check_special: bool = True) -> bool:
        """
        Valida movimento de peão incluindo movimentos especiais
        """
        direction = 1 if piece.color == Color.WHITE else -1
        start_rank = 2 if piece.color == Color.WHITE else 7
        
        file_diff = abs(to_pos.file - from_pos.file)
        rank_diff = to_pos.rank - from_pos.rank
        
        # Movimento para frente
        if file_diff == 0:
            # Movimento simples
            if rank_diff == direction:
                return board.get_piece(to_pos) is None
            
            # Movimento duplo inicial
            if from_pos.rank == start_rank and rank_diff == 2 * direction:
                # Verifica se ambas as casas estão vazias
                middle_pos = Position(from_pos.rank + direction, from_pos.file)
                return (board.get_piece(middle_pos) is None and 
                       board.get_piece(to_pos) is None)
        
        # Captura diagonal
        elif file_diff == 1 and rank_diff == direction:
            target_piece = board.get_piece(to_pos)
            
            # Captura normal
            if target_piece and target_piece.color != piece.color:
                return True
            
            # En passant
            if check_special and self.special_handler:
                return self.special_handler.is_en_passant_capture(
                    from_pos, to_pos, piece, board
                )
        
        return False
