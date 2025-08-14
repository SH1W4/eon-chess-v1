#!/usr/bin/env python3
"""
Teste final para validar a correção do bug h8->g8
"""
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

from src.core.board.board import Board, Position, PieceType, Color
from src.ai.adaptive_ai import AdaptiveAI

def test_position_consistency():
    """Testa se as posições das peças são consistentes"""
    print("🧪 Teste 1: Consistência de Position")
    
    board = Board()
    
    # Verifica algumas peças críticas
    test_positions = ["h8", "a1", "e1", "e8", "d1", "d8"]
    
    all_consistent = True
    for pos_str in test_positions:
        piece = board.get_piece(pos_str)
        if piece:
            expected_pos = Position.from_algebraic(pos_str)
            actual_pos = piece.position
            
            if str(actual_pos) != pos_str:
                print(f"❌ {pos_str}: Esperado {pos_str}, obtido {actual_pos}")
                all_consistent = False
            else:
                print(f"✅ {pos_str}: {piece.type.name} {piece.color.name} - Position OK")
    
    return all_consistent

def test_ai_move_selection():
    """Testa se a IA consegue selecionar movimentos válidos"""
    print("\n🤖 Teste 2: Seleção de movimento pela IA")
    
    board = Board()
    ai = AdaptiveAI()
    
    # Configura o turno para BLACK para testar h8->g8
    board.current_turn = Color.BLACK
    
    # Tenta obter um movimento da IA
    move = ai.get_best_move(board, Color.BLACK, depth=1)
    
    if move is None:
        print("❌ IA não conseguiu selecionar um movimento")
        return False
    
    print(f"✅ IA selecionou: {move.from_pos} -> {move.to_pos} ({move.piece.type.name})")
    
    # Verifica se o movimento é executável
    try:
        from_str = str(move.from_pos)
        to_str = str(move.to_pos)
        result = board.move_piece(from_str, to_str)
        
        if result.get("success", False):
            print(f"✅ Movimento executado com sucesso")
            return True
        else:
            print(f"❌ Movimento falhou: {result.get('error', 'Erro desconhecido')}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar movimento: {e}")
        return False

def test_specific_h8_to_g8():
    """Testa especificamente o movimento problemático h8->g8"""
    print("\n🎯 Teste 3: Movimento específico h8->g8")
    
    board = Board()
    
    # Verifica peças iniciais
    h8_piece = board.get_piece("h8")
    g8_piece = board.get_piece("g8")
    
    print(f"h8: {h8_piece.type.name} {h8_piece.color.name} - Position: {h8_piece.position}")
    print(f"g8: {g8_piece.type.name} {g8_piece.color.name} - Position: {g8_piece.position}")
    
    # Configura turno para BLACK
    board.current_turn = Color.BLACK
    
    # Tenta o movimento h8->g8 (torre captura cavalo)
    result = board.move_piece("h8", "g8")
    
    if result.get("success", False):
        print("✅ Movimento h8->g8 executado com sucesso")
        
        # Verifica o estado final
        new_h8 = board.get_piece("h8")
        new_g8 = board.get_piece("g8")
        
        print(f"Depois - h8: {new_h8}, g8: {new_g8.type.name if new_g8 else None}")
        return True
    else:
        print(f"❌ Movimento h8->g8 falhou: {result.get('error', 'Erro desconhecido')}")
        return False

def main():
    """Executa todos os testes de validação"""
    print("🔍 VALIDAÇÃO DA CORREÇÃO DO BUG")
    print("=" * 60)
    
    tests = [
        test_position_consistency,
        test_ai_move_selection,
        test_specific_h8_to_g8
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
                print("✅ PASSOU")
            else:
                print("❌ FALHOU")
        except Exception as e:
            print(f"💥 ERRO: {e}")
        
        print("-" * 40)
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Bug corrigido com sucesso!")
        return True
    else:
        print("⚠️  Alguns testes falharam. Investigação adicional necessária.")
        return False

if __name__ == "__main__":
    main()
