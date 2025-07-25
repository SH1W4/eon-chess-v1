from src.core.engine import ChessEngine, Position, Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile
import time

def print_board(engine: ChessEngine):
    """Imprime o tabuleiro no terminal"""
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
    
    print("\n  a b c d e f g h")
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
    # Criar engine e IAs
    engine = ChessEngine()
    
    # Criar perfil agressivo
    aggressive_profile = PlayerProfile(
        aggression=0.8,
        risk_taking=0.7,
        positional=0.3
    )
    aggressive_ai = AdaptiveAI(aggressive_profile)
    
    # Criar perfil defensivo
    defensive_profile = PlayerProfile(
        aggression=0.2,
        risk_taking=0.3,
        positional=0.8
    )
    defensive_ai = AdaptiveAI(defensive_profile)
    
    # Jogar partida
    print("Iniciando partida: Agressivo (Brancas) vs Defensivo (Pretas)")
    print_board(engine)
    
    move_count = 0
    start_time = time.time()
    
    while not engine.is_checkmate() and not engine.is_stalemate() and move_count < 50:
        current_ai = aggressive_ai if engine.current_player == 'white' else defensive_ai
        move = current_ai.get_best_move(engine)
        
        if not move:
            print(f"Nenhum movimento disponível para {engine.current_player}")
            break
            
        engine.make_move(move)
        move_count += 1
        
        print(f"\nMovimento {move_count}:")
        print(f"{'Brancas' if engine.current_player == 'black' else 'Pretas'} jogaram: "
              f"{move.from_pos.to_algebraic()} -> {move.to_pos.to_algebraic()}")
        print_board(engine)
        
        if engine._is_in_check(engine.current_player):
            print(f"{engine.current_player} está em xeque!")
            
        # Mostrar tempo de pensamento
        if move_count > 1:
            thinking_time = current_ai.move_times[-1]
            print(f"Tempo de pensamento: {thinking_time:.2f} segundos")
        
        time.sleep(0.5)  # Pausa reduzida para melhor fluidez
    
    # Fim do jogo
    end_time = time.time()
    duration = end_time - start_time
    
    print("\nFim do jogo!")
    if engine.is_checkmate():
        winner = "Brancas" if engine.current_player == 'black' else "Pretas"
        print(f"{winner} venceram por xeque-mate!")
    elif engine.is_stalemate():
        print("Empate por afogamento!")
    else:
        print("Jogo interrompido após 50 movimentos")
    
    print(f"\nDuração: {duration:.1f} segundos")
    print(f"Total de movimentos: {move_count}")
    
    # Atualizar perfis
    if engine.is_checkmate():
        if engine.current_player == 'black':  # Brancas venceram
            aggressive_ai.update_profile('win', defensive_profile)
            defensive_ai.update_profile('loss', aggressive_profile)
        else:  # Pretas venceram
            aggressive_ai.update_profile('loss', defensive_profile)
            defensive_ai.update_profile('win', aggressive_profile)
    else:
        aggressive_ai.update_profile('draw', defensive_profile)
        defensive_ai.update_profile('draw', aggressive_profile)
    
    # Mostrar estatísticas finais
    print("\nEstatísticas do Perfil Agressivo:")
    print(f"Jogos: {aggressive_ai.profile.games_played}")
    print(f"Vitórias: {aggressive_ai.profile.wins}")
    print(f"Derrotas: {aggressive_ai.profile.losses}")
    print(f"Empates: {aggressive_ai.profile.draws}")
    print(f"Nível de Agressão: {aggressive_ai.profile.aggression:.2f}")
    print(f"Tomada de Risco: {aggressive_ai.profile.risk_taking:.2f}")
    
    print("\nEstatísticas do Perfil Defensivo:")
    print(f"Jogos: {defensive_ai.profile.games_played}")
    print(f"Vitórias: {defensive_ai.profile.wins}")
    print(f"Derrotas: {defensive_ai.profile.losses}")
    print(f"Empates: {defensive_ai.profile.draws}")
    print(f"Nível de Agressão: {defensive_ai.profile.aggression:.2f}")
    print(f"Tomada de Risco: {defensive_ai.profile.risk_taking:.2f}")

if __name__ == "__main__":
    main()
