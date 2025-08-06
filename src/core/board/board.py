from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

class Color(Enum):
    WHITE = auto()
    BLACK = auto()

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Position:
    def __init__(self, file: str, rank: int):
        self.file = file
        self.rank = rank
    
    def __str__(self):
        return f"{self.file}{self.rank}"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False

class Board:
    def __init__(self):
        self.pieces: Dict[str, Piece] = {}
        self.setup_initial_position()
        self.current_turn = Color.WHITE
        self.last_move = None
        self._setup_piece_symbols()

    def _setup_piece_symbols(self):
        self.piece_symbols = {
            (PieceType.KING, Color.WHITE): "♔",
            (PieceType.QUEEN, Color.WHITE): "♕",
            (PieceType.ROOK, Color.WHITE): "♖",
            (PieceType.BISHOP, Color.WHITE): "♗",
            (PieceType.KNIGHT, Color.WHITE): "♘",
            (PieceType.PAWN, Color.WHITE): "♙",
            (PieceType.KING, Color.BLACK): "♚",
            (PieceType.QUEEN, Color.BLACK): "♛",
            (PieceType.ROOK, Color.BLACK): "♜",
            (PieceType.BISHOP, Color.BLACK): "♝",
            (PieceType.KNIGHT, Color.BLACK): "♞",
            (PieceType.PAWN, Color.BLACK): "♟"
        }

    def setup_initial_position(self):
        # Setup white pieces
        self.pieces["a1"] = Piece(PieceType.ROOK, Color.WHITE)
        self.pieces["b1"] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.pieces["c1"] = Piece(PieceType.BISHOP, Color.WHITE)
        self.pieces["d1"] = Piece(PieceType.QUEEN, Color.WHITE)
        self.pieces["e1"] = Piece(PieceType.KING, Color.WHITE)
        self.pieces["f1"] = Piece(PieceType.BISHOP, Color.WHITE)
        self.pieces["g1"] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.pieces["h1"] = Piece(PieceType.ROOK, Color.WHITE)
        
        # Setup black pieces
        self.pieces["a8"] = Piece(PieceType.ROOK, Color.BLACK)
        self.pieces["b8"] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.pieces["c8"] = Piece(PieceType.BISHOP, Color.BLACK)
        self.pieces["d8"] = Piece(PieceType.QUEEN, Color.BLACK)
        self.pieces["e8"] = Piece(PieceType.KING, Color.BLACK)
        self.pieces["f8"] = Piece(PieceType.BISHOP, Color.BLACK)
        self.pieces["g8"] = Piece(PieceType.KNIGHT, Color.BLACK)
        self.pieces["h8"] = Piece(PieceType.ROOK, Color.BLACK)
        
        # Setup pawns
        for file in "abcdefgh":
            self.pieces[f"{file}2"] = Piece(PieceType.PAWN, Color.WHITE)
            self.pieces[f"{file}7"] = Piece(PieceType.PAWN, Color.BLACK)

    def get_piece(self, pos: str) -> Optional[Piece]:
        return self.pieces.get(pos)

    def display(self) -> str:
        board = []
        board.append("  a b c d e f g h")
        board.append("  ---------------")
        
        for rank in range(8, 0, -1):
            row = [f"{rank}|"]
            for file in "abcdefgh":
                pos = f"{file}{rank}"
                piece = self.pieces.get(pos)
                if piece:
                    symbol = self.piece_symbols.get((piece.type, piece.color), "?")
                    row.append(symbol)
                else:
                    row.append(".")
            row.append(f"|{rank}")
            board.append(" ".join(row))
        
        board.append("  ---------------")
        board.append("  a b c d e f g h")
        return "\n".join(board)

    def move_piece(self, from_pos: str, to_pos: str) -> dict:
        """Move uma peça com validação completa."""
        # Validações básicas
        piece = self.pieces.get(from_pos)
        if not piece:
            return {"success": False, "error": "Não há peça na posição inicial"}
            
        if piece.color != self.current_turn:
            return {"success": False, "error": "Não é a vez desta cor"}
            
        # Verifica se há peça própria no destino
        target_piece = self.pieces.get(to_pos)
        if target_piece and target_piece.color == piece.color:
            return {"success": False, "error": "Posição ocupada por peça própria"}
        
        # Validação específica por tipo de peça
        if not self._is_valid_move(piece, from_pos, to_pos):
            return {"success": False, "error": "Movimento inválido para esta peça"}
            
        # Verifica se o movimento expõe o rei ao xeque
        if self._move_exposes_check(piece, from_pos, to_pos):
            return {"success": False, "error": "Movimento expõe o rei ao xeque"}
        
        # Executa o movimento
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        piece.has_moved = True
        
        # Alterna o turno
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        self.last_move = (from_pos, to_pos)
        
        return {"success": True}
        
    def _is_valid_move(self, piece: Piece, from_pos: str, to_pos: str) -> bool:
        """Verifica se o movimento é válido para o tipo de peça."""
        # Obtém coordenadas e diferenças
        coords = self._get_move_coordinates(from_pos, to_pos)
        if not coords:
            return False
            
        # Valida se o movimento básico da peça é válido
        if not self._validate_piece_move(piece, from_pos, to_pos, coords):
            return False
            
        # Se o movimento é válido e não é um cavalo, verifica se o caminho está livre
        if piece.type != PieceType.KNIGHT:
            return self._is_path_clear(from_pos, to_pos)
            
        return True
        
    def _validate_piece_move(self, piece: Piece, from_pos: str, to_pos: str, coords: dict) -> bool:
        """Valida o movimento específico para cada tipo de peça.
        
        A validação considera apenas o tipo básico de movimento que a peça pode fazer,
        sem considerar outras peças no caminho (isso é feito em _is_path_clear).
        
        Para a captura, também não considera aqui se há uma peça para capturar,
        apenas se o movimento em si seria válido para captura.
        
        Args:
            piece: A peça que está se movendo
            from_pos: Posição inicial (ex: 'e2')
            to_pos: Posição final (ex: 'e4')
            coords: Dicionário com coordenadas e diferenças calculadas
            
        Returns:
            bool: True se o movimento é válido para o tipo de peça, False caso contrário
        """
        """Valida o movimento específico para cada tipo de peça."""
        dx, dy = coords['dx'], coords['dy']
        abs_dx, abs_dy = coords['abs_dx'], coords['abs_dy']
        
        if piece.type == PieceType.PAWN:
            direction = 1 if piece.color == Color.WHITE else -1
            from_rank = coords['from_rank']
            
            # Movimento para frente
            if abs_dx == 0:
                # Movimento simples
                if dy == direction and not self.pieces.get(to_pos):
                    return True
                # Movimento duplo inicial
                if not piece.has_moved and dy == 2 * direction:
                    middle_pos = f"{from_pos[0]}{from_rank + direction}"
                    return not self.pieces.get(middle_pos) and not self.pieces.get(to_pos)
            
            # Captura diagonal
            if abs_dx == 1 and dy == direction:
                return bool(self.pieces.get(to_pos)) or self._is_en_passant_target(to_pos)
            
            return False
            
        elif piece.type == PieceType.KNIGHT:
            return (abs_dx == 2 and abs_dy == 1) or (abs_dx == 1 and abs_dy == 2)
            
        elif piece.type == PieceType.BISHOP:
            return abs_dx == abs_dy
            
        elif piece.type == PieceType.ROOK:
            return abs_dx == 0 or abs_dy == 0
            
        elif piece.type == PieceType.QUEEN:
            # Rainha pode mover como bispo (diagonal) ou torre (linha reta)
            return abs_dx == abs_dy or abs_dx == 0 or abs_dy == 0
            
        elif piece.type == PieceType.KING:
            return abs_dx <= 1 and abs_dy <= 1
            
        return False
        
    def _get_move_coordinates(self, from_pos: str, to_pos: str) -> dict:
        """Calcula todas as coordenadas e diferenças necessárias para validação de movimento."""
        try:
            # Converte posições para coordenadas
            from_file = ord(from_pos[0]) - ord('a')
            from_rank = int(from_pos[1])
            to_file = ord(to_pos[0]) - ord('a')
            to_rank = int(to_pos[1])
            
            # Calcula diferenças
            dx = to_file - from_file
            dy = to_rank - from_rank
            abs_dx = abs(dx)
            abs_dy = abs(dy)
            
            print(f"DEBUG: Calculando coordenadas: {from_pos} -> {to_pos}")
            print(f"DEBUG: Arquivo: {from_file}->{to_file} ({dx})")
            print(f"DEBUG: Rank: {from_rank}->{to_rank} ({dy})")
            
            return {
                'from_file': from_file,
                'from_rank': from_rank,
                'to_file': to_file,
                'to_rank': to_rank,
                'dx': dx,
                'dy': dy,
                'abs_dx': abs_dx,
                'abs_dy': abs_dy
            }
        except (IndexError, ValueError):
            return None
        
        
    def _is_valid_pawn_move(self, piece: Piece, from_pos: str, to_pos: str, coords: dict) -> bool:
        """Valida movimento específico de peão."""
        direction = 1 if piece.color == Color.WHITE else -1
        from_rank = int(from_pos[1])
        
        dx, dy = coords['dx'], coords['dy']
        abs_dx = coords['abs_dx']
        
        # Movimento para frente
        if abs_dx == 0:
            # Simples movimento para frente
            if dy == direction:
                return not self.pieces.get(to_pos)
            # Movimento duplo inicial
            if not piece.has_moved and dy == 2 * direction:
                middle_pos = f"{from_pos[0]}{from_rank + direction}"
                return not (self.pieces.get(middle_pos) or self.pieces.get(to_pos))
                
        # Captura diagonal
        elif abs_dx == 1 and dy == direction:
            # Captura normal ou en passant
            target = self.pieces.get(to_pos)
            if target and target.color != piece.color:
                return True
            if self._is_en_passant_target(to_pos):
                return True
                
        return False
        
    def _is_path_clear(self, from_pos: str, to_pos: str) -> bool:
        """Verifica se o caminho entre duas posições está livre."""
        from_file = ord(from_pos[0]) - ord('a')
        from_rank = int(from_pos[1])
        to_file = ord(to_pos[0]) - ord('a')
        to_rank = int(to_pos[1])
        
        print(f"DEBUG: Verificando caminho de {from_pos} para {to_pos} (diferença: {to_file - from_file}, {to_rank - from_rank})")
        
        # Determina a direção do movimento
        file_step = 0 if from_file == to_file else (1 if to_file > from_file else -1)
        rank_step = 0 if from_rank == to_rank else (1 if to_rank > from_rank else -1)
        
        current_file = from_file + file_step
        current_rank = from_rank + rank_step
        
        while True:
            # Se passar do destino, termina a verificação
            if file_step > 0 and current_file > to_file: break
            if file_step < 0 and current_file < to_file: break
            if rank_step > 0 and current_rank > to_rank: break
            if rank_step < 0 and current_rank < to_rank: break
            if file_step == 0 and rank_step == 0: break
            
            # Se chegar ao destino, termina a verificação
            if current_file == to_file and current_rank == to_rank:
                break
            
            pos = f"{chr(current_file + ord('a'))}{current_rank}"
            print(f"DEBUG: Verificando posição {pos}")
            
            if self.pieces.get(pos):
                return False
                
            current_file += file_step
            current_rank += rank_step
        
        return True
        
    def _move_exposes_check(self, piece: Piece, from_pos: str, to_pos: str) -> bool:
        """Verifica se um movimento expõe o rei ao xeque."""
        # Salva estado atual
        original_target_piece = self.pieces.get(to_pos)
        
        # Simula o movimento
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        
        # Verifica se o rei está em xeque
        king_in_check = self._is_king_in_check(piece.color)
        
        # Reverte o movimento
        self.pieces[from_pos] = piece
        if original_target_piece:
            self.pieces[to_pos] = original_target_piece
        else:
            del self.pieces[to_pos]
        
        return king_in_check
        
    def _is_king_in_check(self, color: Color) -> bool:
        """Verifica se o rei de uma cor está em xeque."""
        # Encontra posição do rei
        king_pos = None
        for pos, piece in self.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                king_pos = pos
                print(f"DEBUG: Rei {color} encontrado em {king_pos}")
                break
        
        if not king_pos:
            return False
        
        # Verifica se alguma peça adversária pode capturar o rei
        for pos, piece in self.pieces.items():
            if piece.color != color:
                print(f"DEBUG: Verificando ameaça da peça {piece.type} em {pos} contra rei em {king_pos}")
                if self._is_valid_move(piece, pos, king_pos):
                    print(f"DEBUG: Peça {piece.type} em {pos} está dando xeque")
                    return True
        
        return False
        
    def _is_en_passant_target(self, pos: str) -> bool:
        """Verifica se uma posição é alvo válido para en passant."""
        if not self.last_move:
            return False
            
        from_pos, to_pos = self.last_move
        last_piece = self.pieces.get(to_pos)
        
        if not last_piece or last_piece.type != PieceType.PAWN:
            return False
            
        # Verifica se o último movimento foi um avanço duplo de peão
        from_rank = int(from_pos[1])
        to_rank = int(to_pos[1])
        return abs(to_rank - from_rank) == 2 and pos[0] == to_pos[0]

    def castle_kingside(self) -> dict:
        if self.current_turn == Color.WHITE:
            king_pos, rook_pos = "e1", "h1"
            king_target, rook_target = "g1", "f1"
        else:
            king_pos, rook_pos = "e8", "h8"
            king_target, rook_target = "g8", "f8"
            
        king = self.pieces.get(king_pos)
        rook = self.pieces.get(rook_pos)
        
        if not king or not rook:
            return {"success": False, "error": "Rei ou torre não encontrados"}
            
        if king.has_moved or rook.has_moved:
            return {"success": False, "error": "Rei ou torre já se moveram"}
            
        # TODO: Implementar verificação de caminho livre e xeque
        
        # Executa o roque
        self.pieces[king_target] = king
        self.pieces[rook_target] = rook
        del self.pieces[king_pos]
        del self.pieces[rook_pos]
        
        king.has_moved = True
        rook.has_moved = True
        
        return {"success": True}

    def is_en_passant_possible(self) -> bool:
        if not self.last_move:
            return False
            
        from_pos, to_pos = self.last_move
        piece = self.pieces.get(to_pos)
        
        if not piece or piece.type != PieceType.PAWN:
            return False
            
        # TODO: Implementar lógica completa de en passant
        return False

    def promote_pawn(self, from_pos: str, to_pos: str, promotion: str) -> dict:
        piece = self.pieces.get(from_pos)
        if not piece or piece.type != PieceType.PAWN:
            return {"success": False, "error": "Não há peão na posição inicial"}
            
        promotion_types = {
            "queen": PieceType.QUEEN,
            "rook": PieceType.ROOK,
            "bishop": PieceType.BISHOP,
            "knight": PieceType.KNIGHT
        }
        
        if promotion not in promotion_types:
            return {"success": False, "error": "Promoção inválida"}
            
        # Executa a promoção
        self.pieces[to_pos] = Piece(promotion_types[promotion], piece.color)
        del self.pieces[from_pos]
        
        return {"success": True}

    def is_in_check(self) -> bool:
        """Verifica se o jogador atual está em xeque."""
        return self._is_king_in_check(self.current_turn)

    def is_checkmate(self) -> bool:
        """Verifica se o jogador atual está em xeque-mate."""
        # Se não está em xeque, não pode ser xeque-mate
        if not self.is_in_check():
            print("DEBUG: Rei não está em xeque")
            return False
        
        print("DEBUG: Verificando movimentos legais...")
        has_legal = self._has_legal_moves()
        print(f"DEBUG: Tem movimentos legais? {has_legal}")
        
        # Se está em xeque e não tem movimentos legais, é xeque-mate
        return not has_legal

    def is_stalemate(self) -> bool:
        """Verifica se a posição atual é um empate."""
        # Se está em xeque, não é empate
        if self.is_in_check():
            return False
        
        # Se não tem movimentos legais, é empate
        if not self._has_legal_moves():
            return True
        
        # Verifica material insuficiente
        return self._has_insufficient_material()

    def _is_under_attack(self, pos: str, color: Color) -> bool:
        """Verifica se uma posição está sob ataque por peças de uma cor.

        Args:
            pos: A posição a ser verificada
            color: A cor das peças atacantes
            
        Returns:
            bool: True se a posição está sob ataque, False caso contrário
        """
        for piece_pos, piece in self.pieces.items():
            if piece.color == color:
                print(f"DEBUG: Verificando se {piece.type} em {piece_pos} pode atacar {pos}")
                # Simula o movimento diretamente sem verificações adicionais
                coords = self._get_move_coordinates(piece_pos, pos)
                if coords:
                    print(f"DEBUG: Diferenças dx={coords['dx']}, dy={coords['dy']}, abs_dx={coords['abs_dx']}, abs_dy={coords['abs_dy']}")
                    if self._validate_piece_move(piece, piece_pos, pos, coords):
                        print(f"DEBUG: Movimento é válido para a peça")
                        # Para peças que não são cavalos, verifica se o caminho está livre
                        if piece.type == PieceType.KNIGHT:
                            print(f"DEBUG: Posição {pos} está sob ataque por {piece.type} em {piece_pos} (cavalo não precisa verificar caminho)")
                            return True
                        if self._is_path_clear(piece_pos, pos):
                            print(f"DEBUG: Posição {pos} está sob ataque por {piece.type} em {piece_pos} (caminho está livre)")
                            return True
                        else:
                            print(f"DEBUG: Caminho de {piece_pos} para {pos} está bloqueado")
                    else:
                        print(f"DEBUG: Movimento não é válido para {piece.type}")
        return False

    def _has_legal_moves(self) -> bool:
        """Verifica se o jogador atual tem movimentos legais disponíveis."""
        print("DEBUG: Verificando movimentos legais para cada peça...")
        for from_pos, piece in self.pieces.items():
            if piece.color != self.current_turn:
                continue
            print(f"DEBUG: Analisando peça em {from_pos}")
                
            # Gera todos os possíveis movimentos para a peça
            for to_pos in self._generate_possible_moves(from_pos):
                # Salva estado atual
                target_piece = self.pieces.get(to_pos)
                
                # Simula o movimento
                self.pieces[to_pos] = piece
                del self.pieces[from_pos]
                
                # Verifica se o rei não está em xeque após o movimento
                king_safe = not self._is_king_in_check(self.current_turn)
                
                # Reverte o movimento
                self.pieces[from_pos] = piece
                if target_piece:
                    self.pieces[to_pos] = target_piece
                else:
                    del self.pieces[to_pos]
                
                # Se encontrar um movimento que salva o rei, retorna True
                if king_safe:
                    print(f"DEBUG: Movimento válido encontrado: {from_pos} -> {to_pos}")
                    return True
            
            print(f"DEBUG: Nenhum movimento válido para peça em {from_pos}")
        
        print("DEBUG: Nenhuma peça tem movimentos válidos")
        return False

    def _generate_possible_moves(self, from_pos: str) -> List[str]:
        """Gera todas as possíveis posições de destino para uma peça."""
        piece = self.pieces[from_pos]
        possible_moves = []
        
        # Para cada posição no tabuleiro
        for file in 'abcdefgh':
            for rank in range(1, 9):
                to_pos = f"{file}{rank}"
                
                # Pula a posição atual
                if to_pos == from_pos:
                    continue
                
                # Se o movimento é válido, adiciona à lista
                if self._is_valid_move(piece, from_pos, to_pos):
                    target_piece = self.pieces.get(to_pos)
                    if not target_piece or target_piece.color != piece.color:
                        # Para o rei, verifica se a posição alvo não está sob ataque
                        if piece.type == PieceType.KING:
                            opposite_color = Color.BLACK if piece.color == Color.WHITE else Color.WHITE
                            if not self._is_under_attack(to_pos, opposite_color):
                                possible_moves.append(to_pos)
                        else:
                            possible_moves.append(to_pos)
        
        return possible_moves

    def _has_insufficient_material(self) -> bool:
        """Verifica se há material insuficiente para mate."""
        white_pieces = [p for p in self.pieces.values() if p.color == Color.WHITE]
        black_pieces = [p for p in self.pieces.values() if p.color == Color.BLACK]
        
        # Rei contra rei
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True
        
        # Rei contra rei e bispo/cavalo
        if (len(white_pieces) == 1 and len(black_pieces) == 2) or \
           (len(white_pieces) == 2 and len(black_pieces) == 1):
            for pieces in [white_pieces, black_pieces]:
                if len(pieces) == 2:
                    minor_piece = [p for p in pieces if p.type != PieceType.KING][0]
                    if minor_piece.type in [PieceType.BISHOP, PieceType.KNIGHT]:
                        return True
        
        # Rei e bispo contra rei e bispo (mesma cor)
        if len(white_pieces) == 2 and len(black_pieces) == 2:
            white_bishop = next((p for p in white_pieces if p.type == PieceType.BISHOP), None)
            black_bishop = next((p for p in black_pieces if p.type == PieceType.BISHOP), None)
            if white_bishop and black_bishop:
                # Verifica se os bispos estão na mesma cor de casa
                white_bishop_pos = next(pos for pos, p in self.pieces.items() if p == white_bishop)
                black_bishop_pos = next(pos for pos, p in self.pieces.items() if p == black_bishop)
                white_square = (ord(white_bishop_pos[0]) + int(white_bishop_pos[1])) % 2 == 0
                black_square = (ord(black_bishop_pos[0]) + int(black_bishop_pos[1])) % 2 == 0
                if white_square == black_square:
                    return True
        
        return False
