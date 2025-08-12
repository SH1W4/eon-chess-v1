
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

# Patch board.py para adicionar logs
try:
    with open('src/core/board/board.py', 'r') as f:
        content = f.read()

    # Adiciona logs na função move_piece
    if 'DEBUG_LOG_MOVE_PIECE' not in content:
        patched = content.replace(
            'def move_piece(self, from_pos, to_pos):',
            '''def move_piece(self, from_pos, to_pos):
        print(f"DEBUG_LOG_MOVE_PIECE: from_pos={from_pos} (type={type(from_pos)}), to_pos={to_pos} (type={type(to_pos)})")
        print(f"DEBUG_LOG_PIECES_KEYS: {list(self.pieces.keys())[:10]}...")
        
        # Tenta diferentes formatos de chave
        piece_found = None
        key_used = None
        for key_format in [from_pos, str(from_pos), tuple(from_pos) if hasattr(from_pos, '__iter__') else None]:
            if key_format and key_format in self.pieces:
                piece_found = self.pieces[key_format]
                key_used = key_format
                break
        
        print(f"DEBUG_LOG_KEY_RESOLUTION: piece_found={piece_found is not None}, key_used={key_used}")'''
        )
        
        with open('src/core/board/board.py', 'w') as f:
            f.write(patched)
        
        print("✅ Board instrumentado")
    else:
        print("⚠️ Board já instrumentado")
except Exception as e:
    print(f"❌ Erro na instrumentação: {e}")
