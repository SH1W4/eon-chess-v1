from typing import List, Optional, Tuple, Dict
import numpy as np
from ..core.engine import Move, Position
from ..optimization.cache import TranspositionTable, EvaluationCache, MovementCache, PositionHasher
from ..cultural.openings import CulturalOpeningBook
from ..cultural.narrative import CulturalNarrative

class AdaptiveAI:
    """Engine de IA adaptativa com influências culturais"""
    
    def __init__(self, culture_type: str = 'medieval'):
        self.culture = culture_type
        self.max_depth = 4
        
        # Sistema de cache otimizado
        self.position_hasher = PositionHasher()
        self.transposition_table = TranspositionTable(size=1000000)
        self.eval_cache = EvaluationCache(size=10000)
        self.movement_cache = MovementCache(size=5000)
        
        # Sistemas culturais
        self.opening_book = CulturalOpeningBook()
        self.narrative = CulturalNarrative(culture_type)
        
        # Estado do jogo
        self.move_history = []
        self.game_phase = 'opening'  # opening, middlegame, endgame
        self.material_balance = 0
    
    def evaluate_position(self, position: Position) -> float:
        """Avalia uma posição de acordo com critérios culturais"""
        pos_hash = self.position_hasher.hash_position(
            position.board,
            position.castle_rights,
            position.en_passant_square,
            position.white_to_move
        )
        
        # Verifica cache
        cached_eval = self.eval_cache.get(pos_hash)
        if cached_eval is not None:
            return cached_eval
        
        value = 0.0
        material_sum = 0.0
        
        # Valores base das peças
        piece_values = {
            'pawn': 1.0,
            'knight': 3.0,
            'bishop': 3.0,
            'rook': 5.0,
            'queen': 9.0
        }
        
        # Bônus culturais
        cultural_bonuses = {
            'medieval': {
                'knight': 0.2,  # Cavaleiros são mais valorizados
                'bishop': 0.1,  # Bispos representam poder clerical
                'king_safety': 1.2  # Proteção do rei é crucial
            },
            'futuristic': {
                'bishop': 0.2,  # Mobilidade diagonal valorizada
                'queen': 0.2,  # Poder centralizado
                'development': 1.1  # Desenvolvimento rápido
            }
        }
        
        # Avaliação de material e posição
        for piece in position.pieces:
            multiplier = 1 if piece.color == 'white' else -1
            base_value = piece_values.get(piece.type, 0)
            cultural_bonus = cultural_bonuses[self.culture].get(piece.type, 0)
            
            # Valor base + bônus cultural
            piece_value = (base_value + cultural_bonus) * multiplier
            value += piece_value
            material_sum += abs(base_value)
            
            # Bônus posicionais
            if piece.type == 'pawn':
                # Peões avançados são mais valiosos
                rank = piece.position[1]
                progress = rank if piece.color == 'white' else 7 - rank
                value += 0.05 * progress * multiplier
            
            elif piece.type in ['knight', 'bishop']:
                # Desenvolvimento de peças
                if not piece.has_moved:
                    dev_bonus = cultural_bonuses[self.culture].get('development', 1.0)
                    value -= 0.1 * dev_bonus * multiplier
        
        # Segurança do rei
        if self.culture == 'medieval':
            king_safety = self._evaluate_king_safety(position)
            value += king_safety * cultural_bonuses[self.culture]['king_safety']
        
        # Atualiza fase do jogo
        self._update_game_phase(material_sum)
        
        # Armazena no cache
        self.eval_cache.store(pos_hash, value)
        return value
    
    def get_best_move(self, position: Position) -> Optional[Move]:
        """Retorna o melhor movimento para a posição atual"""
        # Verifica livro de aberturas
        if self.game_phase == 'opening':
            book_move = self.opening_book.get_next_move(
                self.move_history,
                self.culture
            )
            if book_move:
                move = position.parse_move(book_move)
                if move in position.legal_moves():
                    self.move_history.append(move)
                    context = self.opening_book.get_cultural_context(
                        self.move_history,
                        self.culture
                    )
                    self.narrative.generate_move_narrative(move, context)
                    return move
        
        best_value = float('-inf') if position.white_to_move else float('inf')
        best_move = None
        
        # Ordena movimentos para melhorar poda
        moves = self._order_moves(position)
        
        # Busca com tabela de transposição
        alpha = float('-inf')
        beta = float('inf')
        
        for move in moves:
            new_pos = position.make_move(move)
            pos_hash = self.position_hasher.hash_position(
                new_pos.board,
                new_pos.castle_rights,
                new_pos.en_passant_square,
                new_pos.white_to_move
            )
            
            # Verifica tabela de transposição
            tt_entry = self.transposition_table.lookup(pos_hash)
            if tt_entry:
                depth, value, _, flag = tt_entry
                if depth >= self.max_depth - 1:
                    if flag == 'exact':
                        value_adj = value
                    elif flag == 'alpha' and value <= alpha:
                        value_adj = alpha
                    elif flag == 'beta' and value >= beta:
                        value_adj = beta
                    else:
                        # Calcula normalmente
                        value_adj = self.minimax(
                            new_pos, self.max_depth - 1,
                            alpha, beta,
                            not position.white_to_move
                        )
                else:
                    # Profundidade insuficiente, calcula normalmente
                    value_adj = self.minimax(
                        new_pos, self.max_depth - 1,
                        alpha, beta,
                        not position.white_to_move
                    )
            else:
                # Posição não encontrada, calcula normalmente
                value_adj = self.minimax(
                    new_pos, self.max_depth - 1,
                    alpha, beta,
                    not position.white_to_move
                )
            
            if position.white_to_move:
                if value_adj > best_value:
                    best_value = value_adj
                    best_move = move
                alpha = max(alpha, value_adj)
            else:
                if value_adj < best_value:
                    best_value = value_adj
                    best_move = move
                beta = min(beta, value_adj)
        
        if best_move:
            self.move_history.append(best_move)
            # Gera narrativa cultural
            context = {
                'phase': self.game_phase,
                'material_balance': self.material_balance,
                'position_value': best_value
            }
            self.narrative.generate_move_narrative(best_move, context)
            
            # Pode gerar momento dramático
            self.narrative.generate_dramatic_moment(
                best_value,
                self.game_phase,
                self.material_balance
            )
        
        return best_move
    
    def minimax(self, position: Position, depth: int,
               alpha: float, beta: float, is_maximizing: bool) -> float:
        """Implementa minimax com poda alpha-beta e tabela de transposição"""
        if depth == 0:
            return self.evaluate_position(position)
        
        pos_hash = self.position_hasher.hash_position(
            position.board,
            position.castle_rights,
            position.en_passant_square,
            position.white_to_move
        )
        
        # Verifica tabela de transposição
        tt_entry = self.transposition_table.lookup(pos_hash)
        if tt_entry:
            stored_depth, value, _, flag = tt_entry
            if stored_depth >= depth:
                if flag == 'exact':
                    return value
                elif flag == 'alpha' and value <= alpha:
                    return alpha
                elif flag == 'beta' and value >= beta:
                    return beta
        
        # Busca movimentos ordenados
        moves = self._order_moves(position)
        
        if is_maximizing:
            value = float('-inf')
            best_value = float('-inf')
            for move in moves:
                new_value = self.minimax(
                    position.make_move(move),
                    depth - 1, alpha, beta,
                    False
                )
                value = max(value, new_value)
                best_value = max(best_value, value)
                alpha = max(alpha, value)
                if alpha >= beta:
                    # Armazena bound superior
                    self.transposition_table.store(
                        pos_hash, depth, value, move, 'beta'
                    )
                    break
            
            # Armazena valor exato
            if value > alpha and value < beta:
                self.transposition_table.store(
                    pos_hash, depth, value, move, 'exact'
                )
            # Armazena bound inferior
            elif value <= alpha:
                self.transposition_table.store(
                    pos_hash, depth, value, move, 'alpha'
                )
            
            return value
        
        else:
            value = float('inf')
            best_value = float('inf')
            for move in moves:
                new_value = self.minimax(
                    position.make_move(move),
                    depth - 1, alpha, beta,
                    True
                )
                value = min(value, new_value)
                best_value = min(best_value, value)
                beta = min(beta, value)
                if alpha >= beta:
                    # Armazena bound inferior
                    self.transposition_table.store(
                        pos_hash, depth, value, move, 'alpha'
                    )
                    break
            
            # Armazena valor exato
            if value > alpha and value < beta:
                self.transposition_table.store(
                    pos_hash, depth, value, move, 'exact'
                )
            # Armazena bound superior
            elif value >= beta:
                self.transposition_table.store(
                    pos_hash, depth, value, move, 'beta'
                )
            
            return value
    
    def _order_moves(self, position: Position) -> List[Move]:
        """Ordena movimentos para melhorar poda alpha-beta"""
        # Verifica cache de movimentos
        pos_hash = self.position_hasher.hash_position(
            position.board,
            position.castle_rights,
            position.en_passant_square,
            position.white_to_move
        )
        
        cached_moves = self.movement_cache.get(pos_hash)
        if cached_moves:
            return cached_moves
        
        moves = list(position.legal_moves())
        scored_moves = []
        
        for move in moves:
            score = 0
            
            # Capturas são prioritárias
            if move.captured_piece:
                piece_values = {
                    'pawn': 1, 'knight': 3, 'bishop': 3,
                    'rook': 5, 'queen': 9
                }
                aggressor_value = piece_values.get(move.piece.type, 0)
                target_value = piece_values.get(move.captured_piece.type, 0)
                score = target_value * 10 - aggressor_value
            
            # Promoções são importantes
            if move.promotion:
                score += 8
            
            # Cheques são relevantes
            if move.is_check:
                score += 5
            
            # Movimentos do cache de transposição
            tt_entry = self.transposition_table.lookup(pos_hash)
            if tt_entry and tt_entry[2] == move:
                score += 1000  # Prioriza movimentos bons anteriores
            
            scored_moves.append((move, score))
        
        # Ordena por score
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        ordered_moves = [move for move, _ in scored_moves]
        
        # Armazena no cache
        self.movement_cache.store(pos_hash, ordered_moves)
        
        return ordered_moves
    
    def _evaluate_king_safety(self, position: Position) -> float:
        """Avalia a segurança do rei"""
        value = 0.0
        
        for color in ['white', 'black']:
            multiplier = 1 if color == 'white' else -1
            king = position.get_king(color)
            
            if not king:
                continue
            
            # Proteção de peões
            pawn_shield = sum(1 for p in position.get_pieces(color, 'pawn')
                             if abs(p.position[0] - king.position[0]) <= 1 and
                             ((color == 'white' and p.position[1] > king.position[1]) or
                              (color == 'black' and p.position[1] < king.position[1])))
            value += 0.2 * pawn_shield * multiplier
            
            # Roque realizado
            if king.has_castled:
                value += 0.5 * multiplier
            
            # Peças próximas ao rei
            defenders = sum(1 for p in position.get_pieces(color)
                          if p.type != 'king' and
                          max(abs(p.position[0] - king.position[0]),
                              abs(p.position[1] - king.position[1])) <= 2)
            value += 0.1 * defenders * multiplier
        
        return value
    
    def _update_game_phase(self, material_sum: float):
        """Atualiza a fase do jogo baseado no material"""
        total_initial = 78  # 2*(9+5+5+6+6+8) sem reis
        material_ratio = material_sum / total_initial
        
        if material_ratio > 0.8:
            self.game_phase = 'opening'
        elif material_ratio > 0.3:
            self.game_phase = 'middlegame'
        else:
            self.game_phase = 'endgame'
        
        self.material_balance = material_sum
