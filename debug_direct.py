#!/usr/bin/env python3
"""
Diagnóstico direto do problema h8->g8
"""
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

from src.core.board.board import Board, Position, PieceType, Color
from src.core.engine import ChessEngine

print("🔍 DIAGNÓSTICO DIRETO h8->g8")
print("=" * 50)

# 1. Cria board inicial
board = Board()
print(f"✅ Board criado com {len(board.pieces)} peças")

# 2. Verifica se h8 existe
h8_piece = board.get_piece("h8")
print(f"🎯 Peça em h8: {h8_piece}")
if h8_piece:
    print(f"   Tipo: {h8_piece.type.name}")
    print(f"   Cor: {h8_piece.color.name}")
    print(f"   Position: {h8_piece.position}")

# 3. Mostra estrutura do dicionário pieces
print(f"\n📋 Estrutura do dicionário pieces:")
print(f"   Total: {len(board.pieces)} peças")
print(f"   Tipos de chaves: {set(type(k).__name__ for k in board.pieces.keys())}")

# Mostra algumas chaves relevantes
relevant_keys = [k for k in board.pieces.keys() if 'h8' in str(k) or 'h7' in str(k) or 'g8' in str(k)]
print(f"   Chaves relevantes (h8, h7, g8): {relevant_keys}")

# 4. Testa diferentes formatos de acesso
print(f"\n🔑 Testes de acesso para h8:")
test_formats = ["h8", (7, 7), (7, 8), Position.from_algebraic("h8")]
for fmt in test_formats:
    try:
        piece = board.pieces.get(fmt)
        print(f"   {fmt} ({type(fmt).__name__}): {'✅' if piece else '❌'}")
    except Exception as e:
        print(f"   {fmt} ({type(fmt).__name__}): ❌ ERRO: {e}")

# 5. Verifica o movimento via engine
print(f"\n🎮 Teste de movimento via ChessEngine:")
engine = ChessEngine()
engine.board = board  # Use o board que já criamos

# Primeiro, vamos ver o estado atual
print(f"   Current turn: {board.current_turn}")
print(f"   Peça em h8: {board.get_piece('h8')}")
print(f"   Peça em g8: {board.get_piece('g8')}")

# Cria um movimento válido
try:
    from src.core.board.move import Move
    move = Move(
        from_pos=Position.from_algebraic("h8"), 
        to_pos=Position.from_algebraic("g8"),
        piece=board.get_piece("h8")
    )
    result = engine.make_move(move)
    print(f"   Resultado: {result}")
except Exception as e:
    print(f"   ❌ ERRO no movimento: {e}")
    import traceback
    traceback.print_exc()

# 6. Verifica se o método move_piece existe e o que ele faz
print(f"\n🔧 Teste direto do board.move_piece:")
try:
    # Primeiro vamos confirmar que h8 tem uma peça
    before_h8 = board.get_piece("h8")
    before_g8 = board.get_piece("g8")
    
    print(f"   ANTES - h8: {before_h8}, g8: {before_g8}")
    
    # Chama move_piece diretamente
    direct_result = board.move_piece("h8", "g8")
    print(f"   Resultado direto: {direct_result}")
    
    # Verifica o estado depois
    after_h8 = board.get_piece("h8")
    after_g8 = board.get_piece("g8")
    print(f"   DEPOIS - h8: {after_h8}, g8: {after_g8}")
    
except Exception as e:
    print(f"   ❌ ERRO no move_piece: {e}")
    import traceback
    traceback.print_exc()

print(f"\n🎯 DIAGNÓSTICO COMPLETO!")
