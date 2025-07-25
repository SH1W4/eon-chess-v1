from src.core.engine import ChessEngine, Position, Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile
from src.cultural.cultural_engine import CulturalEngine
import time
import os

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board_with_culture(engine: ChessEngine, cultural: CulturalEngine):
    """Imprime o tabuleiro com nomes culturais das peças"""
    pieces_unicode = {
        ('pawn', 'white'): '♙',
        ('pawn', 'black'): '♟',
        ('rook', 'white'): '♖',
        ('rook', 'black'): '♜',
        ('knight', 'white'): '♘',
        ('knight', 'black'): '♞',
        ('bishop', 'white'): '♗',
        ('bishop', 'black'): '♝',
        ('queen', 'white'): '♕',
        ('queen', 'black'): '♛',
        ('king', 'white'): '♔',
        ('king', 'black'): '♚'
    }
    
    print(f"\nTema Atual: {cultural.current_theme.name}")
    print(f"Era: {cultural.current_theme.era}")
    print(f"{cultural.current_theme.description}\n")
    
    print("  a b c d e f g h")
    print("  ---------------")
    for row in range(8):
        print(f"{8-row}|", end=" ")
        for col in range(8):
            piece = engine.get_piece(Position(row, col))
            if piece:
                print(pieces_unicode[(piece.type, piece.color)], end=" ")
            else:
                print(".", end=" ")
        print(f"|{8-row}")
    print("  ---------------")
    print("  a b c d e f g h\n")

def main():
    # Criar engines
    engine = ChessEngine()
    cultural = CulturalEngine()
    
    # Criar perfis de IA
    aggressive_profile = PlayerProfile(
        aggression=0.8,
        risk_taking=0.7,
        positional=0.3
    )
    defensive_profile = PlayerProfile(
        aggression=0.2,
        risk_taking=0.3,
        positional=0.8
    )
    
    # Criar IAs
    white_ai = AdaptiveAI(aggressive_profile)
    black_ai = AdaptiveAI(defensive_profile)
    
    # Selecionar tema
    print("Escolha um tema cultural:")
    print("1. Medieval Europa")
    print("2. Neo Tokyo 2050")
    print("3. Reino Místico")
    print("4. Aleatório")
    
    choice = input("Sua escolha (1-4): ")
    clear_screen()
    
    if choice == "1":
        cultural.select_theme("medieval")
    elif choice == "2":
        cultural.select_theme("futuristic")
    elif choice == "3":
        cultural.select_theme("mystic")
    else:
        cultural.get_random_theme()
    
    # Mostrar descrições iniciais
    print("\nApresentando as forças em campo:")
    print("\nForças Brancas (Agressivas):")
    for piece_type in ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']:
        name = cultural.get_piece_name(piece_type)
        desc = cultural.get_piece_description(piece_type)
        print(f"{name}: {desc}")
    
    print("\nForças Negras (Defensivas):")
    for piece_type in ['king', 'queen', 'bishop', 'knight', 'rook', 'pawn']:
        name = cultural.get_piece_name(piece_type)
        desc = cultural.get_piece_description(piece_type)
        print(f"{name}: {desc}")
    
    input("\nPressione Enter para começar o jogo...")
    clear_screen()
    
    # Iniciar jogo
    move_count = 0
    start_time = time.time()
    last_capture = None
    
    while not engine.is_checkmate() and not engine.is_stalemate() and move_count < 50:
        current_ai = white_ai if engine.current_player == 'white' else black_ai
        move = current_ai.get_best_move(engine)
        
        if not move:
            print(f"Nenhum movimento disponível para {engine.current_player}")
            break
        
        # Verificar captura
        captured_piece = engine.get_piece(move.to_pos)
        
        # Fazer movimento
        engine.make_move(move)
        move_count += 1
        
        # Limpar tela e mostrar estado atual
        clear_screen()
        print_board_with_culture(engine, cultural)
        
        # Gerar narrativa do movimento
        print(f"\nMovimento {move_count}:")
        narrative = cultural.generate_move_narrative(
            move.piece.type,
            move.to_pos.to_algebraic()
        )
        print(narrative)
        
        # Eventos especiais
        if captured_piece:
            capture_narrative = cultural.generate_special_event(
                'capture',
                attacker_type=move.piece.type,
                defender_type=captured_piece.type
            )
            print(capture_narrative)
            last_capture = move_count
        
        if engine._is_in_check(engine.current_player):
            check_narrative = cultural.generate_special_event(
                'check',
                attacker_type=move.piece.type
            )
            print(check_narrative)
        
        # Atualizar estado narrativo
        cultural.update_narrative_state({
            'board': [[piece.__dict__ if piece else None for piece in row] 
                     for row in engine.board],
            'is_check': engine._is_in_check(engine.current_player),
            'last_move_was_capture': move_count == last_capture
        })
        
        # Verificar momentos dramáticos
        dramatic_moment = cultural.get_dramatic_moment()
        if dramatic_moment:
            print(f"\n{dramatic_moment}")
        
        time.sleep(1.5)
    
    # Fim do jogo
    clear_screen()
    print_board_with_culture(engine, cultural)
    
    print("\nFim da batalha!")
    if engine.is_checkmate():
        winner = "Forças Brancas" if engine.current_player == 'black' else "Forças Negras"
        winner_king = cultural.get_piece_name('king')
        loser_king = cultural.get_piece_name('king')
        print(f"Vitória! O {winner_king} das {winner} triunfa!")
        print(f"O {loser_king} inimigo foi derrotado em combate!")
    elif engine.is_stalemate():
        print("A batalha termina em um impasse! Nenhum lado conseguiu prevalecer!")
    else:
        print("A batalha foi interrompida sem um vencedor definido.")
    
    duration = time.time() - start_time
    print(f"\nDuração da batalha: {duration:.1f} segundos")
    print(f"Movimentos realizados: {move_count}")

if __name__ == "__main__":
    main()
