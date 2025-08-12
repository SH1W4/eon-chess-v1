
import sys
sys.path.append('/Users/jx/WORKSPACE/PROJECTS/CHESS')

try:
    from src.core.board.board import Board, Position, PieceType, Color, Piece
    from src.core.engine import ChessEngine

    print("=== TESTE FOCAL h8->g8 ===")

    # Cria um board com torre em h8
    board = Board()
    board.setup_board()

    # Verifica se há peça em h8
    h8_piece = board.get_piece("h8")
    print(f"Peça em h8: {h8_piece}")
    print(f"Tipo da peça: {type(h8_piece)}")
    if h8_piece:
        print(f"Cor: {h8_piece.color}")
        print(f"Tipo: {h8_piece.type}")

    # Verifica keys do dicionário pieces
    print(f"Total de peças: {len(board.pieces)}")
    print("Primeiras 10 chaves:")
    for i, key in enumerate(list(board.pieces.keys())[:10]):
        piece = board.pieces[key]
        print(f"  {i+1}. {key} ({type(key).__name__}) -> {piece.type.name} {piece.color.name}")

    # Tenta diferentes formatos para h8
    test_keys = ["h8", "H8", (7, 7), (7, 0)]
    try:
        test_keys.append(Position.from_algebraic("h8"))
    except:
        pass
    
    for test_key in test_keys:
        try:
            found = board.pieces.get(test_key)
            print(f"Teste key {test_key} ({type(test_key).__name__}): {found is not None}")
        except Exception as e:
            print(f"Erro testando {test_key}: {e}")

    # Tenta o movimento
    engine = ChessEngine(board)
    try:
        result = engine.make_move("h8", "g8", Color.BLACK)
        print(f"Resultado do movimento h8->g8: {result}")
    except Exception as e:
        print(f"ERRO no movimento h8->g8: {e}")
        import traceback
        traceback.print_exc()
except Exception as e:
    print(f"❌ Erro no teste focal: {e}")
    import traceback
    traceback.print_exc()
