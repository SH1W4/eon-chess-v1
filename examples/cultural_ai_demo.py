from src.core.engine import ChessEngine, Position, Move
from src.ai.adaptive_ai import AdaptiveAI, PlayerProfile
from src.cultural.integrated_culture import CulturalEngine
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
    
    cultura = "Europa Medieval" if cultural.values.tradition > 0.6 else "Neo Tokyo 2050"
    era = "Século XIII" if cultural.values.tradition > 0.6 else "Ano 2050"
    descricao = "Reino de honra e tradição" if cultural.values.tradition > 0.6 else "Metrópole cyberpunk do futuro"
    
    print(f"\nTema: {cultura}")
    print(f"Era: {era}")
    print(f"{descricao}\n")
    
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
    
    # Criar perfis de IA com diferentes culturas
    medieval_profile = PlayerProfile(
        aggression=0.8,
        risk_taking=0.7,
        positional=0.3
    )
    futuristic_profile = PlayerProfile(
        aggression=0.3,
        risk_taking=0.8,
        positional=0.7
    )
    
    # Criar IAs
    medieval_ai = AdaptiveAI(medieval_profile, 'medieval')
    futuristic_ai = AdaptiveAI(futuristic_profile, 'neo_tokyo')
    
    # Mostrar confronto de culturas
    print("\nConfrontro Cultural de Xadrez!")
    print("\nEuropa Medieval vs. Neo Tokyo 2050")
    print("\nEuropa Medieval (Brancas):")
    print("- Estilo agressivo e tradicional")
    print("- Forte senso de honra")
    print("- Valoriza sacrifícios nobres")
    
    print("\nNeo Tokyo 2050 (Pretas):")
    print("- Estilo inovador e tecnológico")
    print("- Alta adaptabilidade")
    print("- Valoriza eficiência e controle")
    
    input("\nPressione Enter para começar a batalha...")
    clear_screen()
    
    # Iniciar jogo
    move_count = 0
    start_time = time.time()
    last_capture = None
    
    while not engine.is_checkmate() and not engine.is_stalemate() and move_count < 50:
        current_ai = medieval_ai if engine.current_player == 'white' else futuristic_ai
        move = current_ai.get_best_move(engine)
        
        if not move:
            print(f"Nenhum movimento disponível para {engine.current_player}")
            break
        
        # Verificar captura
        captured_piece = engine.get_piece(move.to_pos)
        
        # Fazer movimento
        engine.make_move(move)
        move_count += 1
        
        # Atualizar estado cultural
        cultural = current_ai.cultural_engine
        cultural.update_game_state(move, {
            'board': [[piece.__dict__ if piece else None for piece in row] 
                     for row in engine.board],
            'current_player': engine.current_player,
            'move_count': move_count
        })
        
        # Limpar tela e mostrar estado atual
        clear_screen()
        print_board_with_culture(engine, cultural)
        
        # Mostrar narrativa cultural
        print(f"\nMovimento {move_count}:")
        narrative = cultural.get_cultural_narrative(move)
        print(narrative)
        
        # Eventos especiais
        if captured_piece:
            cultural.memory.learn_from_move(move, 
                {'type': 'capture', 'success': True}, 'success')
            last_capture = move_count
        
        if engine._is_in_check(engine.current_player):
            if current_ai.cultural_engine.values.honor > 0.6:
                print("\nUma situação de grande honra! O rei está ameaçado!")
            else:
                print("\nAlerta crítico! Sistema central comprometido!")
        
        # Mostrar momento dramático
        dramatic = cultural.get_dramatic_moment()
        if dramatic:
            print(f"\n{dramatic}")
        
        # Mostrar tempo de pensamento
        if move_count > 1:
            thinking_time = current_ai.move_times[-1]
            print(f"\nTempo de análise: {thinking_time:.2f} segundos")
        
        time.sleep(1.0)
    
    # Fim do jogo
    clear_screen()
    print_board_with_culture(engine, medieval_ai.cultural_engine)
    
    print("\nFim da Batalha entre Culturas!")
    if engine.is_checkmate():
        winner = "Europa Medieval" if engine.current_player == 'black' else "Neo Tokyo"
        winner_ai = medieval_ai if engine.current_player == 'black' else futuristic_ai
        loser_ai = futuristic_ai if engine.current_player == 'black' else medieval_ai
        
        print(f"\nVitória de {winner}!")
        
        if winner_ai.cultural_engine.values.honor > 0.6:
            print("Uma vitória honrosa que será lembrada através dos tempos!")
        else:
            print("Eficiência máxima alcançada. Objetivo conquistado.")
            
        # Atualizar perfis
        winner_ai.update_profile('win', loser_ai.profile)
        loser_ai.update_profile('loss', winner_ai.profile)
        
    elif engine.is_stalemate():
        print("\nUm empate! As culturas provaram ser igualmente poderosas!")
        medieval_ai.update_profile('draw', futuristic_ai.profile)
        futuristic_ai.update_profile('draw', medieval_ai.profile)
    else:
        print("\nA batalha foi interrompida sem um vencedor definido.")
    
    duration = time.time() - start_time
    print(f"\nDuração da batalha: {duration:.1f} segundos")
    print(f"Movimentos realizados: {move_count}")
    
    # Mostrar estatísticas culturais
    print("\nEstatísticas Culturais:")
    print("\nEuropa Medieval:")
    print(f"Honra: {medieval_ai.cultural_engine.values.honor:.2f}")
    print(f"Tradição: {medieval_ai.cultural_engine.values.tradition:.2f}")
    print(f"Adaptabilidade: {medieval_ai.profile.aggression:.2f}")
    
    print("\nNeo Tokyo:")
    print(f"Inovação: {futuristic_ai.cultural_engine.values.innovation:.2f}")
    print(f"Eficiência: {futuristic_ai.cultural_engine.values.collectivism:.2f}")
    print(f"Adaptabilidade: {futuristic_ai.profile.aggression:.2f}")

if __name__ == "__main__":
    main()
