from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Union

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
    def __init__(self, file: Union[str, int], rank: int):
        # Convert file from string ('a'-'h') to int (0-7) if needed
        if isinstance(file, str):
            self.file = ord(file) - ord('a')
        else:
            self.file = file
        # Convert from 1-8 to 0-7 if needed
        if isinstance(rank, str):
            rank = int(rank)
        if rank > 8:
            self.rank = rank - 1
        else:
            self.rank = rank
    
    def __str__(self):
        # Convert back to chess notation
        return f"{chr(self.file + ord('a'))}{self.rank + 1}"
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.file == other.file and self.rank == other.rank
    
    def __hash__(self):
        return hash((self.file, self.rank))

@dataclass
class Move:
    """Representa um movimento no tabuleiro"""
    from_pos: Position
    to_pos: Position
    piece: Optional['Piece'] = None

class Piece:
    def __init__(self, piece_type: PieceType, color: Color, position: str = None):
        self.type = piece_type
        self.color = color
        self.has_moved = False
        self._position = None
        if position:
            self.position = Position(
                file=ord(position[0]) - ord('a'),
                rank=int(position[1]) - 1
            )
    
    @property
    def position(self) -> Position:
        return self._position
    
    @position.setter
    def position(self, value: Position):
        self._position = value

class Board:
    def __init__(self):
        self.pieces: Dict[str, Piece] = {}
        self.captured_pieces: List[Piece] = []
        self.move_history: List[Tuple[Position, Position]] = []
        self.setup_initial_position()
        self.current_turn = Color.WHITE
        self.last_move = None
        self._setup_piece_symbols()


    @property
    def piece_list(self):
        """Retorna lista de peças para compatibilidade"""
        return list(self.pieces.values())

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
        self.pieces["a1"] = Piece(PieceType.ROOK, Color.WHITE, "a1")
        self.pieces["b1"] = Piece(PieceType.KNIGHT, Color.WHITE, "b1")
        self.pieces["c1"] = Piece(PieceType.BISHOP, Color.WHITE, "c1")
        self.pieces["d1"] = Piece(PieceType.QUEEN, Color.WHITE, "d1")
        self.pieces["e1"] = Piece(PieceType.KING, Color.WHITE, "e1")
        self.pieces["f1"] = Piece(PieceType.BISHOP, Color.WHITE, "f1")
        self.pieces["g1"] = Piece(PieceType.KNIGHT, Color.WHITE, "g1")
        self.pieces["h1"] = Piece(PieceType.ROOK, Color.WHITE, "h1")
        
        # Setup black pieces
        self.pieces["a8"] = Piece(PieceType.ROOK, Color.BLACK, "a8")
        self.pieces["b8"] = Piece(PieceType.KNIGHT, Color.BLACK, "b8")
        self.pieces["c8"] = Piece(PieceType.BISHOP, Color.BLACK, "c8")
        self.pieces["d8"] = Piece(PieceType.QUEEN, Color.BLACK, "d8")
        self.pieces["e8"] = Piece(PieceType.KING, Color.BLACK, "e8")
        self.pieces["f8"] = Piece(PieceType.BISHOP, Color.BLACK, "f8")
        self.pieces["g8"] = Piece(PieceType.KNIGHT, Color.BLACK, "g8")
        self.pieces["h8"] = Piece(PieceType.ROOK, Color.BLACK, "h8")
        
        # Setup pawns
        for file in "abcdefgh":
            white_pos = f"{file}2"
            black_pos = f"{file}7"
            self.pieces[white_pos] = Piece(PieceType.PAWN, Color.WHITE, white_pos)
            self.pieces[black_pos] = Piece(PieceType.PAWN, Color.BLACK, black_pos)

    def get_piece(self, pos: Union[str, tuple, Position]) -> Optional[Piece]:
        """Get piece at position, accepting string, tuple or Position"""
        if isinstance(pos, tuple):
            # Se for tupla, usa diretamente (já que pieces pode ter tuplas como chaves)
            return self.pieces.get(pos)
        elif isinstance(pos, Position):
            # Se for Position, converte para string
            pos = str(pos)
        # Se for string, tenta como está
        piece = self.pieces.get(pos)
        if piece:
            return piece
        # Se não encontrou como string, tenta converter para tupla
        if isinstance(pos, str) and len(pos) == 2:
            file_idx = ord(pos[0]) - ord('a')
            rank = int(pos[1])
            return self.pieces.get((file_idx, rank))
        return None

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
        """Move uma peça com validação completa.
        
        Suporta movimentos especiais:
        - Roque (rei de e1->g1/c1 ou e8->g8/c8 com validações completas)
        - En passant (captura diagonal de peões com base no último movimento adversário)
        """
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
        
        # Trata roque (movimento do rei de duas colunas na mesma fileira)
        if piece.type == PieceType.KING and from_pos[0] == 'e' and abs(ord(to_pos[0]) - ord(from_pos[0])) == 2 and from_pos[1] == to_pos[1]:
            castle_result = self._attempt_castle(from_pos, to_pos)
            if not castle_result["success"]:
                return castle_result
            return {"success": True}
        
        # Validação específica por tipo de peça
        if not self._is_valid_move(piece, from_pos, to_pos):
            return {"success": False, "error": "Movimento inválido para esta peça"}
            
        # Verifica en passant (captura de peão em diagonal com casa de destino vazia)
        if piece.type == PieceType.PAWN:
            if self._is_en_passant_capture(from_pos, to_pos):
                ep_result = self._execute_en_passant(from_pos, to_pos)
                if not ep_result["success"]:
                    return ep_result
                self._post_move_update(from_pos, to_pos, captured_piece=ep_result.get("captured"))
                return {"success": True}
        
        # Verifica se o movimento expõe o rei ao xeque
        if self._move_exposes_check(piece, from_pos, to_pos):
            return {"success": False, "error": "Movimento expõe o rei ao xeque"}
        
        # Executa o movimento normal
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        piece.has_moved = True
        
        # Pós-atualizações
        self._post_move_update(from_pos, to_pos, captured_piece=target_piece)
        
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
            # A rainha pode mover-se como uma torre ou um bispo
            is_diagonal = abs_dx == abs_dy
            is_straight = abs_dx == 0 or abs_dy == 0
            print(f"DEBUG: Rainha movendo de {from_pos} para {to_pos} -> diagonal? {is_diagonal}, straight? {is_straight}")
            return is_diagonal or is_straight
            
        elif piece.type == PieceType.KING:
            # Movimento normal do rei (uma casa) — roque é tratado em move_piece
            return abs_dx <= 1 and abs_dy <= 1
            
        return False
        
    def _get_move_coordinates(self, from_pos: Union[str, tuple], to_pos: Union[str, tuple]) -> dict:
        """Calcula todas as coordenadas e diferenças necessárias para validação de movimento."""
        try:
            # Converte posições para coordenadas
            if isinstance(from_pos, str):
                from_file = ord(from_pos[0]) - ord('a')
                from_rank = int(from_pos[1])
            else:
                rank, file = from_pos
                from_rank = rank
                from_file = file - 1
                
            if isinstance(to_pos, str):
                to_file = ord(to_pos[0]) - ord('a')
                to_rank = int(to_pos[1])
            else:
                rank, file = to_pos
                to_rank = rank
                to_file = file - 1
            
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
        
    def get_valid_moves(self, pos: Union[str, Position, tuple]) -> List[Position]:
        """Get all valid moves for a piece at the given position"""
        # Guarda a posição original para usar consistentemente
        original_pos = pos
        
        # Converte para string para uso interno se necessário
        if isinstance(pos, tuple):
            file_idx, rank = pos
            pos_str = f"{chr(ord('a') + file_idx)}{rank}"
        elif isinstance(pos, Position):
            pos_str = str(pos)
        else:
            pos_str = pos
        
        # Usa original_pos para buscar a peça (mantém consistência com o dicionário)
        piece = self.get_piece(original_pos)
        if not piece:
            return []
            
        # Generate all possible destination squares
        valid_moves = []
        for file in "abcdefgh":
            for rank in range(1, 9):
                to_pos = f"{file}{rank}"
                if to_pos != pos_str:
                    coords = self._get_move_coordinates(pos_str, to_pos)
                    if coords:
                        if self._validate_piece_move(piece, pos_str, to_pos, coords):
                            if piece.type == PieceType.KNIGHT or self._is_path_clear(pos_str, to_pos):
                                # Usa to_pos para verificar peça de destino
                                target_piece = self.get_piece(to_pos)
                                if not target_piece or target_piece.color != piece.color:
                                    valid_moves.append(Position(file, rank))
        return valid_moves
            
    def _is_path_clear(self, from_pos: Union[str, tuple], to_pos: Union[str, tuple]) -> bool:
        """Verifica se o caminho entre duas posições está livre."""
        # Converte tuplas para coordenadas
        if isinstance(from_pos, tuple):
            from_file, from_rank = from_pos
        else:
            from_file = ord(from_pos[0]) - ord('a')
            from_rank = int(from_pos[1])
            
        if isinstance(to_pos, tuple):
            to_file, to_rank = to_pos
        else:
            to_file = ord(to_pos[0]) - ord('a')
            to_rank = int(to_pos[1])
        
        # Determina a direção do movimento
        file_step = 0 if from_file == to_file else (1 if to_file > from_file else -1)
        rank_step = 0 if from_rank == to_rank else (1 if to_rank > from_rank else -1)
        
        print(f"DEBUG: Verificando caminho de {from_pos} para {to_pos}")
        print(f"DEBUG: Movimento: File {from_file}->{to_file} (step: {file_step}), Rank {from_rank}->{to_rank} (step: {rank_step})")
        
        current_file = from_file + file_step
        current_rank = from_rank + rank_step
        
        # Enquanto não chegar ao destino
        while current_file != to_file or current_rank != to_rank:
            # Valida limites do tabuleiro
            if current_file < 0 or current_file > 7 or current_rank < 1 or current_rank > 8:
                print(f"DEBUG: Movimento fora dos limites do tabuleiro")
                return False
            
            # Verifica posição intermediária
            pos = f"{chr(current_file + ord('a'))}{current_rank}"
            print(f"DEBUG: Verificando posição intermediária {pos}")
            if self.pieces.get(pos):
                print(f"DEBUG: Peça encontrada em {pos}, caminho bloqueado")
                return False
            
            # Avança para próxima posição
            current_file += file_step
            current_rank += rank_step
        
        return True
        
    def _move_exposes_check(self, piece: Piece, from_pos: str, to_pos: str) -> bool:
        """Verifica se um movimento expõe o rei ao xeque."""
        original_target_piece = self.pieces.get(to_pos)
        # Simula
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        king_in_check = self._is_king_in_check(piece.color)
        # Reverte
        self.pieces[from_pos] = piece
        if original_target_piece is not None:
            self.pieces[to_pos] = original_target_piece
        else:
            self.pieces.pop(to_pos, None)
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
        """Verifica se uma posição é alvo válido para en passant (casa atrás do peão que avançou dois)."""
        if not self.last_move:
            return False
        from_pos, to_pos = self.last_move
        last_piece = self.pieces.get(to_pos)
        if not last_piece or last_piece.type != PieceType.PAWN:
            return False
        # Último lance foi avanço duplo?
        from_rank = int(from_pos[1])
        to_rank = int(to_pos[1])
        if abs(to_rank - from_rank) != 2:
            return False
        # A casa alvo precisa estar imediatamente atrás do peão que avançou
        direction = -1 if last_piece.color == Color.WHITE else 1
        behind_pos = f"{to_pos[0]}{to_rank + direction}"
        return pos == behind_pos

    def _attempt_castle(self, king_from: str, king_to: str) -> dict:
        """Tenta executar o roque (rei se move duas casas). Valida todas as condições.
        king_from: e1/e8, king_to: g1/g8 (lado rei) ou c1/c8 (lado dama)
        """
        king = self.pieces.get(king_from)
        if not king or king.type != PieceType.KING:
            return {"success": False, "error": "Rei não encontrado"}
        if king.has_moved:
            return {"success": False, "error": "Rei já se moveu"}
        color = king.color
        is_white = color == Color.WHITE
        back_rank = '1' if is_white else '8'
        opponent = Color.BLACK if is_white else Color.WHITE
        # Determina lado e posições
        if king_to[0] == 'g':
            rook_pos = f"h{back_rank}"
            rook_target = f"f{back_rank}"
            path_squares = [f"f{back_rank}", f"g{back_rank}"]
            between_for_clear = [f"f{back_rank}", f"g{back_rank}"]
        elif king_to[0] == 'c':
            rook_pos = f"a{back_rank}"
            rook_target = f"d{back_rank}"
            path_squares = [f"d{back_rank}", f"c{back_rank}"]
            between_for_clear = [f"b{back_rank}", f"c{back_rank}", f"d{back_rank}"]
        else:
            return {"success": False, "error": "Destino de roque inválido"}
        rook = self.pieces.get(rook_pos)
        if not rook or rook.type != PieceType.ROOK or rook.has_moved:
            return {"success": False, "error": "Torre inválida para roque"}
        # Casas entre rei e torre devem estar vazias
        for sq in between_for_clear:
            if self.pieces.get(sq):
                return {"success": False, "error": "Caminho do roque bloqueado"}
        # Rei não pode estar em xeque, nem passar por casas atacadas, nem terminar em casa atacada
        if self._is_king_in_check(color):
            return {"success": False, "error": "Rei está em xeque"}
        for sq in path_squares:
            if self._is_under_attack(sq, opponent):
                return {"success": False, "error": "Casa de passagem do roque atacada"}
        # Executa o roque
        self.pieces[king_to] = king
        del self.pieces[king_from]
        self.pieces[rook_target] = rook
        del self.pieces[rook_pos]
        king.has_moved = True
        rook.has_moved = True
        # Atualiza turno e histórico
        self._post_move_update(king_from, king_to)
        return {"success": True}

    def castle_kingside(self) -> dict:
        if self.current_turn == Color.WHITE:
            return self._attempt_castle("e1", "g1")
        else:
            return self._attempt_castle("e8", "g8")

    def is_en_passant_possible(self) -> bool:
        if not self.last_move:
            return False
        from_pos, to_pos = self.last_move
        last_piece = self.pieces.get(to_pos)
        if not last_piece or last_piece.type != PieceType.PAWN:
            return False
        # Avanço duplo no último lance
        return abs(int(to_pos[1]) - int(from_pos[1])) == 2

    def _post_move_update(self, from_pos: str, to_pos: str, captured_piece: Optional[Piece] = None) -> None:
        """Atualiza estado comum pós-movimento (turno, histórico, capturas)."""
        # Alterna o turno
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        # Histórico
        from_position = Position(from_pos[0], int(from_pos[1]))
        to_position = Position(to_pos[0], int(to_pos[1]))
        self.last_move = (from_pos, to_pos)
        self.move_history.append((from_position, to_position))
        # Capturas
        if captured_piece:
            self.captured_pieces.append(captured_piece)

    def _is_en_passant_capture(self, from_pos: str, to_pos: str) -> bool:
        """Retorna True se o movimento candidato é uma captura en passant válida."""
        piece = self.pieces.get(from_pos)
        if not piece or piece.type != PieceType.PAWN:
            return False
        # Movimento diagonal para casa vazia
        if self.pieces.get(to_pos):
            return False
        dx = ord(to_pos[0]) - ord(from_pos[0])
        dy = int(to_pos[1]) - int(from_pos[1])
        direction = 1 if piece.color == Color.WHITE else -1
        if abs(dx) != 1 or dy != direction:
            return False
        # Verifica se casa alvo é a casa atrás do peão que avançou 2 no último lance
        return self._is_en_passant_target(to_pos)

    def _execute_en_passant(self, from_pos: str, to_pos: str) -> dict:
        """Executa a captura en passant removendo o peão capturado corretamente."""
        piece = self.pieces.get(from_pos)
        if not piece or piece.type != PieceType.PAWN:
            return {"success": False, "error": "Peão não encontrado para en passant"}
        if not self._is_en_passant_target(to_pos):
            return {"success": False, "error": "Destino não é válido para en passant"}
        # Determina a posição do peão capturado (a casa do peão que moveu 2)
        assert self.last_move is not None
        _, last_to = self.last_move
        captured_pos = last_to
        captured_piece = self.pieces.get(captured_pos)
        if not captured_piece or captured_piece.type != PieceType.PAWN:
            return {"success": False, "error": "Nenhum peão para capturar en passant"}
        # Executa: move peão atacante para to_pos e remove o capturado
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        self.pieces.pop(captured_pos, None)
        piece.has_moved = True
        return {"success": True, "captured": captured_piece}

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

    def _is_under_attack(self, pos: Union[str, Position], color: Color) -> bool:
        """Verifica se uma posição está sob ataque por peças de uma cor.

        Args:
            pos: A posição a ser verificada (str ou Position)
            color: A cor das peças atacantes
            
        Returns:
            bool: True se a posição está sob ataque, False caso contrário
        """
        if isinstance(pos, Position):
            pos = str(pos)
            
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
        
    def is_square_attacked(self, pos: Union[str, Position], color: Color) -> bool:
        """Alias for _is_under_attack to match AI expectations"""
        return self._is_under_attack(pos, color)

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
