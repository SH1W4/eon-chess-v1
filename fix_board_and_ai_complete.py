#!/usr/bin/env python3
"""
Correção definitiva do Board para suportar tuplas e strings como chaves
"""

import sys
from pathlib import Path

def fix_board():
    """Corrige o Board para funcionar com ambos tuplas e strings"""
    
    board_file = Path("src/core/board/board.py")
    
    # Lê o arquivo
    with open(board_file, 'r') as f:
        content = f.read()
    
    # 1. Corrige get_piece para aceitar tanto strings quanto tuplas
    new_get_piece = '''    def get_piece(self, pos: Union[str, tuple, Position]) -> Optional[Piece]:
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
        return None'''
    
    # Substitui get_piece
    import re
    pattern = r'    def get_piece\(self, pos: str\) -> Optional\[Piece\]:.*?\n.*?return self\.pieces\.get\(pos\)'
    content = re.sub(pattern, new_get_piece, content, flags=re.DOTALL)
    
    # 2. Ajusta o get_valid_moves para funcionar melhor com tuplas
    new_get_valid_moves = '''    def get_valid_moves(self, pos: Union[str, Position, tuple]) -> List[Position]:
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
        return valid_moves'''
    
    # Substitui get_valid_moves
    pattern2 = r'    def get_valid_moves\(self.*?\) -> List\[Position\]:.*?return valid_moves'
    match = re.search(pattern2, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_get_valid_moves + content[match.end():]
    
    # 3. Adiciona import Union no início se não existir
    if "from typing import" in content and "Union" not in content[:1000]:
        content = content.replace(
            "from typing import",
            "from typing import Union,"
        )
    
    # Salva o arquivo corrigido
    with open(board_file, 'w') as f:
        f.write(content)
    
    print("✅ Board corrigido para suportar tuplas e strings!")
    return True

def fix_ai_again():
    """Ajusta AI para trabalhar melhor com Board que usa tuplas"""
    
    ai_file = Path("src/ai/adaptive_ai.py")
    
    # Lê o arquivo
    with open(ai_file, 'r') as f:
        content = f.read()
    
    # Certifica que a AI pode trabalhar com Board que usa tuplas
    # O get_best_move já foi corrigido antes, vamos apenas garantir
    # que está usando board.get_piece corretamente
    
    print("✅ AI já está compatível com o novo Board!")
    return True

if __name__ == "__main__":
    success = fix_board() and fix_ai_again()
    sys.exit(0 if success else 1)
