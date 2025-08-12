
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

try:
    from src.core.board.board import Board, Position

    print("=== ANÁLISE DE ESTRUTURA ===")

    board = Board()
    board.setup_board()

    # Analisa consistência de Position
    pos_h8 = Position.from_algebraic("h8")
    print(f"Position.from_algebraic('h8'): {pos_h8}")
    print(f"str(pos_h8): {str(pos_h8)}")
    print(f"pos_h8.file: {pos_h8.file}, pos_h8.rank: {pos_h8.rank}")

    # Verifica se __str__ e from_algebraic são inversos
    pos_test = Position.from_algebraic("a1")
    pos_str = str(pos_test)
    pos_back = Position.from_algebraic(pos_str)
    print(f"Teste roundtrip a1: {pos_test} -> {pos_str} -> {pos_back}")
    print(f"Igualdade: {pos_test.file == pos_back.file and pos_test.rank == pos_back.rank}")

    # Testa todas as casas do board inicial
    inconsistencies = []
    for pos, piece in board.pieces.items():
        try:
            pos_str = str(pos)
            pos_from_str = Position.from_algebraic(pos_str)
            if not (pos_from_str.file == piece.position.file and pos_from_str.rank == piece.position.rank):
                inconsistencies.append((pos, pos_str, piece.position))
        except Exception as e:
            inconsistencies.append((pos, f"ERROR: {e}", piece.position))

    print(f"Inconsistências encontradas: {len(inconsistencies)}")
    for inc in inconsistencies[:5]:
        print(f"  {inc}")
except Exception as e:
    print(f"❌ Erro na análise: {e}")
    import traceback
    traceback.print_exc()
