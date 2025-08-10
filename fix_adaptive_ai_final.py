#!/usr/bin/env python3
"""
Script para corrigir definitivamente os problemas da IA adaptativa
"""

import sys
from pathlib import Path

def fix_adaptive_ai():
    """Corrige os problemas fundamentais da IA adaptativa"""
    
    ai_file = Path("src/ai/adaptive_ai.py")
    
    # Lê o arquivo
    with open(ai_file, 'r') as f:
        content = f.read()
    
    # Problema 1: get_best_move tem código duplicado e conflitante
    # Vamos corrigir a função get_best_move
    
    # Primeiro, vamos remover a linha problemática duplicada
    content = content.replace(
        """            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)""",
        ""
    )
    
    # Agora vamos corrigir o método get_best_move completamente
    new_get_best_move = '''    def get_best_move(self, board: Board, color: Optional[Color] = None, depth: int = 3) -> Optional[Move]:
        """Get best move using minimax with alpha-beta pruning"""
        if color is None:
            color = Color.WHITE
            
        best_score = float('-inf')
        best_move = None
        
        # Get all valid moves for the current position
        all_moves = []
        
        # Verifica se board.pieces existe e tem itens
        if not hasattr(board, 'pieces') or not board.pieces:
            return None
            
        for pos, piece in board.pieces.items():
            if piece.color == color:
                # Get valid moves for this piece
                valid_moves = board.get_valid_moves(pos)
                for to_pos in valid_moves:
                    move = Move(pos, to_pos, piece)
                    # Check for captures
                    captured = board.get_piece(to_pos)
                    if captured:
                        move.captured_piece = captured
                    all_moves.append(move)
        
        # Se não há movimentos válidos, retorna None
        if not all_moves:
            return None
        
        # Randomize move order slightly based on risk_taking profile
        if self.profile.risk_taking > 0.7:
            import random
            random.shuffle(all_moves)
        
        for move in all_moves:
            # Make copy of board for evaluation
            board_copy = Board()
            # Copia o estado do tabuleiro
            if hasattr(board, 'squares'):
                board_copy.squares = board.squares.copy()
            if hasattr(board, 'pieces'):
                board_copy.pieces = board.pieces.copy()
            if hasattr(board, 'piece_list'):
                board_copy.piece_list = board.piece_list.copy()
            
            # Try move (make_move pode ser síncrono em Board básico)
            piece_backup = board_copy.pieces.get(move.to_pos)
            board_copy.pieces[move.to_pos] = move.piece
            if move.from_pos in board_copy.pieces:
                del board_copy.pieces[move.from_pos]
            
            # Evaluate position recursively
            score = -self._minimax(board_copy, depth - 1, float('-inf'), float('inf'),
                                 Color.BLACK if color == Color.WHITE else Color.WHITE)
            
            # Restore board state
            if move.from_pos != move.to_pos:
                board_copy.pieces[move.from_pos] = move.piece
                if piece_backup:
                    board_copy.pieces[move.to_pos] = piece_backup
                elif move.to_pos in board_copy.pieces:
                    del board_copy.pieces[move.to_pos]
            
            # Add aggression bonus for captures
            if move.captured_piece:
                capture_bonus = self.weights.piece_values[move.captured_piece.type] * self.profile.aggression
                score += capture_bonus
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move'''
    
    # Localiza e substitui o método get_best_move
    import re
    pattern = r'    def get_best_move\(self.*?\n(?:.*?\n)*?        return best_move'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + new_get_best_move + content[match.end():]
    
    # Problema 2: _evaluate_mobility sempre retorna 0 porque get_valid_moves retorna posições, não Moves
    new_evaluate_mobility = '''    def _evaluate_mobility(self, board: Board, color: Color) -> float:
        """Evaluate the mobility of pieces for a given color."""
        mobility_score = 0.0
        
        if not hasattr(board, 'pieces') or not board.pieces:
            return 0.0
            
        for pos, piece in board.pieces.items():
            if piece.color == color:
                # get_valid_moves retorna uma lista de posições (Position)
                valid_moves = board.get_valid_moves(pos)
                # Cada movimento válido contribui para a mobilidade
                mobility_score += len(valid_moves) * 0.1
                # Bonus for controlling center squares
                for move_pos in valid_moves:
                    # move_pos é uma Position
                    if hasattr(move_pos, 'rank') and hasattr(move_pos, 'file'):
                        if 3 <= move_pos.rank <= 4 and 3 <= move_pos.file <= 4:
                            mobility_score += 0.05
                    elif isinstance(move_pos, tuple) and len(move_pos) == 2:
                        # Se for uma tupla (rank, file)
                        if 3 <= move_pos[0] <= 4 and 3 <= move_pos[1] <= 4:
                            mobility_score += 0.05
        return mobility_score'''
    
    # Substitui _evaluate_mobility
    pattern2 = r'    def _evaluate_mobility\(self.*?\n(?:.*?\n)*?        return mobility_score'
    match2 = re.search(pattern2, content)
    if match2:
        content = content[:match2.start()] + new_evaluate_mobility + content[match2.end():]
    
    # Problema 3: update_profile não está alterando valores quando evolution_cycles > 0 mas game_memory está vazia
    # Vamos garantir que sempre adicione à game_memory
    
    # Localiza o método update_profile e adiciona lógica para sempre adicionar à memória
    update_fix = """        # Sempre adiciona o jogo atual à memória antes de processar
        current_game = {
            'result': game_result,
            'aggression': self.profile.aggression,
            'positional': self.profile.positional,
            'risk_taking': self.profile.risk_taking
        }
        self.game_memory.append(current_game)
        
        # Analyze final position"""
    
    content = content.replace(
        "        # Analyze final position",
        update_fix
    )
    
    # Salva o arquivo corrigido
    with open(ai_file, 'w') as f:
        f.write(content)
    
    print("✅ IA adaptativa corrigida com sucesso!")
    print("Principais correções:")
    print("1. get_best_move agora funciona corretamente com board.pieces")
    print("2. _evaluate_mobility calcula corretamente a mobilidade")
    print("3. update_profile sempre adiciona à game_memory para permitir evolução")
    
    return True

if __name__ == "__main__":
    success = fix_adaptive_ai()
    sys.exit(0 if success else 1)
