from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
import json
import random

from ..core.engine import ChessEngine, Position, Piece, Move

@dataclass
class CulturalValues:
    """Valores fundamentais que definem uma cultura"""
    honor: float  # Influencia decisões de sacrifício (0-1)
    tradition: float  # Peso para movimentos tradicionais (0-1)
    innovation: float  # Propensão a movimentos não convencionais (0-1)
    collectivism: float  # Prioridade para proteção de peças (0-1)
    
    # Valores específicos de xadrez
    piece_values: Dict[str, float]  # Valor cultural das peças
    position_values: Dict[str, float]  # Valor de diferentes áreas do tabuleiro
    
    @property
    def piece_names(self) -> Dict[str, str]:
        """Retorna os nomes culturais das peças"""
        if self.tradition > 0.6:  # Europa Medieval
            return {
                'king': 'Rei',
                'queen': 'Rainha',
                'bishop': 'Bispo',
                'knight': 'Cavaleiro',
                'rook': 'Torre',
                'pawn': 'Peão'
            }
        else:  # Neo Tokyo
            return {
                'king': 'Comandante',
                'queen': 'IA Suprema',
                'bishop': 'Hacker',
                'knight': 'Mecha',
                'rook': 'Fortaleza',
                'pawn': 'Drone'
            }
    
    @classmethod
    def create_medieval_europe(cls) -> 'CulturalValues':
        return cls(
            honor=0.8,
            tradition=0.7,
            innovation=0.3,
            collectivism=0.4,
            piece_values={
                'king': 1.2,    # Realeza é muito valorizada
                'queen': 1.1,   # Poder feminino era raro, mas importante
                'bishop': 1.15, # Igreja era muito influente
                'knight': 1.1,  # Cavalaria era honorável
                'rook': 0.9,    # Defesa era importante, mas não glamourosa
                'pawn': 0.85    # Peasants eram desvalorizados
            },
            position_values={
                'center': 1.1,      # Controle do centro era importante
                'kingside': 1.05,   # Lado do rei era ligeiramente mais nobre
                'queenside': 0.95,  # Lado da rainha era secundário
                'back_rank': 1.1    # Proteção da realeza era crucial
            }
        )
    
    @classmethod
    def create_neo_tokyo(cls) -> 'CulturalValues':
        return cls(
            honor=0.3,
            tradition=0.2,
            innovation=0.9,
            collectivism=0.6,
            piece_values={
                'king': 0.9,    # Liderança mais distribuída
                'queen': 1.2,   # IA suprema é muito valorizada
                'bishop': 1.1,  # Hackers são importantes
                'knight': 1.0,  # Mechas são padrão
                'rook': 1.1,    # Fortalezas são cruciais
                'pawn': 1.0     # Drones são valorizados igualmente
            },
            position_values={
                'center': 1.2,      # Controle de rede é crucial
                'kingside': 1.0,    # Todos os setores são importantes
                'queenside': 1.0,   # Igualdade de setores
                'back_rank': 0.9    # Mobilidade é mais importante que defesa
            }
        )
    
    @classmethod
    def create_mystic_realm(cls) -> 'CulturalValues':
        return cls(
            honor=0.6,
            tradition=0.5,
            innovation=0.7,
            collectivism=0.8,
            piece_values={
                'king': 1.0,    # Poder místico é distribuído
                'queen': 1.2,   # Arquimaga é muito poderosa
                'bishop': 1.2,  # Magos são muito respeitados
                'knight': 0.9,  # Guardiões são servidores
                'rook': 1.0,    # Golens são neutros
                'pawn': 1.1     # Aprendizes têm potencial
            },
            position_values={
                'center': 1.3,      # Nexus de poder mágico
                'kingside': 1.0,    # Energia é fluida
                'queenside': 1.0,   # Energia é fluida
                'back_rank': 0.8    # Mobilidade mágica é mais importante
            }
        )

class CulturalMemory:
    """Sistema de memória cultural que aprende e evolui"""
    def __init__(self):
        self.move_patterns = defaultdict(float)
        self.position_patterns = defaultdict(float)
        self.success_rates = defaultdict(lambda: [0, 0])  # [wins, total]
        self.learning_rate = 0.1
    
    def learn_from_move(self, move: Move, position: Dict, outcome: str) -> None:
        """Aprende de um movimento específico"""
        pattern = self._extract_move_pattern(move)
        position_pattern = self._extract_position_pattern(position)
        
        # Atualizar padrões
        success = 1.0 if outcome == 'success' else 0.0
        self.move_patterns[pattern] = (
            (1 - self.learning_rate) * self.move_patterns[pattern] +
            self.learning_rate * success
        )
        
        self.position_patterns[position_pattern] = (
            (1 - self.learning_rate) * self.position_patterns[position_pattern] +
            self.learning_rate * success
        )
        
        # Atualizar taxas de sucesso
        self.success_rates[pattern][1] += 1
        if outcome == 'success':
            self.success_rates[pattern][0] += 1
    
    def get_pattern_value(self, move: Move, position: Dict) -> float:
        """Retorna o valor cultural de um padrão"""
        pattern = self._extract_move_pattern(move)
        position_pattern = self._extract_position_pattern(position)
        
        move_value = self.move_patterns[pattern]
        position_value = self.position_patterns[position_pattern]
        
        # Calcular taxa de sucesso
        wins, total = self.success_rates[pattern]
        success_rate = wins / total if total > 0 else 0.5
        
        return (move_value + position_value + success_rate) / 3
    
    def _extract_move_pattern(self, move: Move) -> str:
        """Extrai padrão característico de um movimento"""
        return f"{move.piece.type}_{move.from_pos.to_algebraic()}_{move.to_pos.to_algebraic()}"
    
    def _extract_position_pattern(self, position: Dict) -> str:
        """Extrai padrão característico de uma posição"""
        return json.dumps(position, sort_keys=True)

class CulturalRituals:
    """Sistema de rituais e cerimônias culturais"""
    def __init__(self, values: CulturalValues):
        self.values = values
        self.sacred_squares = self._initialize_sacred_squares()
        self.ceremonial_patterns = self._initialize_ceremonial_patterns()
        self.ritual_state = {
            'opening_phase': True,
            'midgame_ceremony': False,
            'endgame_ritual': False
        }
    
    def _initialize_sacred_squares(self) -> Dict[str, float]:
        """Inicializa quadrados com significado especial"""
        squares = {}
        
        # Centro do tabuleiro
        center_value = self.values.position_values['center']
        squares.update({
            'e4': center_value, 'd4': center_value,
            'e5': center_value, 'd5': center_value
        })
        
        # Quadrados do rei
        king_value = self.values.piece_values['king']
        if self.values.tradition > 0.6:
            squares.update({
                'e1': king_value, 'e8': king_value,  # Posições tradicionais
                'g1': king_value * 0.8, 'g8': king_value * 0.8  # Roque
            })
        
        return squares
    
    def _initialize_ceremonial_patterns(self) -> List[Dict]:
        """Inicializa padrões cerimoniais importantes"""
        patterns = []
        
        # Padrões baseados em valores culturais
        if self.values.tradition > 0.6:
            patterns.append({
                'name': 'Traditional Opening',
                'moves': ['e2e4', 'd2d4'],
                'value': self.values.tradition
            })
        
        if self.values.innovation > 0.6:
            patterns.append({
                'name': 'Innovation Pattern',
                'moves': ['g1f3', 'b1c3'],
                'value': self.values.innovation
            })
        
        return patterns
    
    def evaluate_ritual_significance(self, move: Move, phase: str) -> float:
        """Avalia o significado ritual de um movimento"""
        significance = 0.0
        
        # Valor do quadrado sagrado
        if move.to_pos.to_algebraic() in self.sacred_squares:
            significance += self.sacred_squares[move.to_pos.to_algebraic()]
        
        # Valor cerimonial baseado na fase
        if phase == 'opening' and self.ritual_state['opening_phase']:
            significance += self._evaluate_opening_ceremony(move)
        elif phase == 'midgame' and not self.ritual_state['midgame_ceremony']:
            significance += self._evaluate_midgame_ceremony(move)
        elif phase == 'endgame' and not self.ritual_state['endgame_ritual']:
            significance += self._evaluate_endgame_ritual(move)
        
        return significance
    
    def _evaluate_opening_ceremony(self, move: Move) -> float:
        """Avalia significado cerimonial na abertura"""
        value = 0.0
        
        # Desenvolvimento de peças nobres
        if move.piece.type in ['knight', 'bishop'] and not move.piece.has_moved:
            value += self.values.tradition * 0.5
        
        # Controle do centro
        if move.to_pos.to_algebraic() in ['e4', 'd4', 'e5', 'd5']:
            value += self.values.position_values['center']
        
        return value
    
    def _evaluate_midgame_ceremony(self, move: Move) -> float:
        """Avalia significado cerimonial no meio-jogo"""
        value = 0.0
        
        # Atividade da rainha
        if move.piece.type == 'queen':
            value += self.values.piece_values['queen'] * 0.3
        
        # Estruturas de peões
        if move.piece.type == 'pawn':
            value += self._evaluate_pawn_structure(move)
        
        return value
    
    def _evaluate_endgame_ritual(self, move: Move) -> float:
        """Avalia significado cerimonial no final"""
        value = 0.0
        
        # Atividade do rei
        if move.piece.type == 'king':
            value += self.values.piece_values['king'] * 0.4
        
        # Promoção de peão
        if move.piece.type == 'pawn' and move.promotion_piece:
            value += self.values.piece_values[move.promotion_piece] * 0.6
        
        return value
    
    def _evaluate_pawn_structure(self, move: Move) -> float:
        """Avalia estrutura de peões"""
        return self.values.piece_values['pawn'] * self.values.collectivism

class CulturalEngine:
    """Motor principal do sistema cultural"""
    def __init__(self, culture_name: str = 'medieval'):
        self.values = self._initialize_cultural_values(culture_name)
        self.memory = CulturalMemory()
        self.rituals = CulturalRituals(self.values)
        self.adaptation_rate = 0.1
        
        # Estado do jogo
        self.game_phase = 'opening'
        self.move_count = 0
        self.position_history = []
    
    def _initialize_cultural_values(self, culture_name: str) -> CulturalValues:
        """Inicializa valores culturais baseado na cultura escolhida"""
        if culture_name == 'medieval':
            return CulturalValues.create_medieval_europe()
        elif culture_name == 'neo_tokyo':
            return CulturalValues.create_neo_tokyo()
        elif culture_name == 'mystic':
            return CulturalValues.create_mystic_realm()
        else:
            return CulturalValues.create_medieval_europe()
    
    def evaluate_move(self, move: Move, position: Dict) -> float:
        """Avalia um movimento considerando aspectos culturais"""
        # Valor base do movimento
        base_value = self._evaluate_base_move(move)
        
        # Valor cultural da memória
        memory_value = self.memory.get_pattern_value(move, position)
        
        # Valor ritual
        ritual_value = self.rituals.evaluate_ritual_significance(
            move, self.game_phase
        )
        
        # Combinar valores
        return (
            base_value * 0.5 +
            memory_value * 0.3 +
            ritual_value * 0.2
        )
    
    def _evaluate_base_move(self, move: Move) -> float:
        """Avalia o valor base de um movimento"""
        value = 0.0
        
        # Valor cultural da peça
        piece_value = self.values.piece_values.get(move.piece.type, 1.0)
        value += piece_value
        
        # Valor posicional
        pos_value = self._get_position_value(move.to_pos)
        value += pos_value
        
        # Aspectos culturais específicos
        if self.values.honor > 0.6 and move.captured_piece:
            value += self._evaluate_capture_honor(move)
        
        if self.values.tradition > 0.6:
            value += self._evaluate_traditional_aspects(move)
        
        if self.values.innovation > 0.6:
            value += self._evaluate_innovative_aspects(move)
        
        if self.values.collectivism > 0.6:
            value += self._evaluate_collective_aspects(move)
        
        return value
    
    def _get_position_value(self, pos: Position) -> float:
        """Obtém o valor cultural de uma posição"""
        # Centro
        if pos.col in [3, 4] and pos.row in [3, 4]:
            return self.values.position_values['center']
        
        # Lado do rei
        if pos.col >= 4:
            return self.values.position_values['kingside']
        
        # Lado da rainha
        return self.values.position_values['queenside']
    
    def _evaluate_capture_honor(self, move: Move) -> float:
        """Avalia o aspecto honorável de uma captura"""
        if not move.captured_piece:
            return 0.0
            
        # Capturar peça mais valiosa é mais honroso
        attacker_value = self.values.piece_values[move.piece.type]
        defender_value = self.values.piece_values[move.captured_piece.type]
        
        if attacker_value < defender_value:
            return self.values.honor * 0.5  # Honra em vencer um oponente mais forte
        else:
            return -self.values.honor * 0.2  # Desonra em usar força excessiva
    
    def _evaluate_traditional_aspects(self, move: Move) -> float:
        """Avalia aspectos tradicionais do movimento"""
        value = 0.0
        
        # Movimentos tradicionais de desenvolvimento
        if self.game_phase == 'opening':
            if move.piece.type in ['knight', 'bishop'] and not move.piece.has_moved:
                value += self.values.tradition * 0.3
            
            if move.piece.type == 'pawn' and move.from_pos.col in [3, 4]:
                value += self.values.tradition * 0.2
        
        return value
    
    def _evaluate_innovative_aspects(self, move: Move) -> float:
        """Avalia aspectos inovadores do movimento"""
        value = 0.0
        
        # Movimentos não convencionais
        if self.game_phase == 'opening':
            if move.piece.type in ['knight', 'bishop']:
                if move.to_pos.col in [0, 7] or move.to_pos.row in [0, 7]:
                    value += self.values.innovation * 0.4
        
        # Sacrifícios posicionais
        if move.captured_piece:
            piece_value = self.values.piece_values[move.piece.type]
            captured_value = self.values.piece_values[move.captured_piece.type]
            if piece_value > captured_value:
                value += self.values.innovation * 0.3
        
        return value
    
    def _evaluate_collective_aspects(self, move: Move) -> float:
        """Avalia aspectos coletivos do movimento"""
        value = 0.0
        
        # Proteção de peças
        if self._protects_ally(move):
            value += self.values.collectivism * 0.4
        
        # Estruturas de peões
        if move.piece.type == 'pawn':
            if self._forms_pawn_chain(move):
                value += self.values.collectivism * 0.3
        
        return value
    
    def _protects_ally(self, move: Move) -> bool:
        """Verifica se o movimento protege uma peça aliada"""
        # Implementação simplificada
        return False
    
    def _forms_pawn_chain(self, move: Move) -> bool:
        """Verifica se o movimento forma uma cadeia de peões"""
        # Implementação simplificada
        return False
    
    def update_game_state(self, move: Move, position: Dict):
        """Atualiza o estado do jogo"""
        self.move_count += 1
        self.position_history.append(position)
        
        # Atualizar fase do jogo
        if self.move_count < 10:
            self.game_phase = 'opening'
        elif self.move_count < 30:
            self.game_phase = 'midgame'
        else:
            self.game_phase = 'endgame'
    
    def learn_from_game(self, moves: List[Move], positions: List[Dict], outcome: str):
        """Aprende com um jogo completo"""
        for move, position in zip(moves, positions):
            self.memory.learn_from_move(move, position, outcome)
    
    def adapt_to_opponent(self, opponent_style: Dict[str, float]):
        """Adapta valores culturais ao estilo do oponente"""
        # Ajustar valores mantendo a essência cultural
        for key, value in opponent_style.items():
            if hasattr(self.values, key):
                current = getattr(self.values, key)
                adapted = current * (1 - self.adaptation_rate) + value * self.adaptation_rate
                setattr(self.values, key, adapted)
    
    def get_cultural_narrative(self, move: Move) -> str:
        """Gera narrativa cultural para um movimento"""
        if not move:
            return ""
            
        # Base da narrativa
        narrative = f"O {self.values.piece_names[move.piece.type]} "
        
        # Adicionar contexto baseado na fase do jogo
        if self.game_phase == 'opening':
            narrative += self._get_opening_narrative(move)
        elif self.game_phase == 'midgame':
            narrative += self._get_midgame_narrative(move)
        else:
            narrative += self._get_endgame_narrative(move)
        
        return narrative
    
    def _get_opening_narrative(self, move: Move) -> str:
        """Gera narrativa para fase de abertura"""
        if move.piece.type in ['knight', 'bishop']:
            return "se desenvolve para uma posição estratégica"
        elif move.piece.type == 'pawn':
            return "avança para controlar o centro"
        return "se posiciona para a batalha"
    
    def _get_midgame_narrative(self, move: Move) -> str:
        """Gera narrativa para meio-jogo"""
        if move.captured_piece:
            return f"captura o {self.values.piece_names[move.captured_piece.type]} inimigo"
        return "manobra para uma posição vantajosa"
    
    def _get_endgame_narrative(self, move: Move) -> str:
        """Gera narrativa para final"""
        if move.piece.type == 'king':
            return "assume uma posição mais ativa"
        elif move.piece.type == 'pawn' and move.promotion_piece:
            return f"é promovido a {self.values.piece_names[move.promotion_piece]}"
        return "busca a vitória decisiva"
        
    def get_dramatic_moment(self) -> Optional[str]:
        """Gera momentos dramáticos baseados na situação atual do jogo"""
        # Implementação básica - pode ser expandida com mais lógica
        if self.game_phase == 'opening' and self.move_count == 5:
            if self.values.tradition > 0.6:
                return "As peças nobres se preparam para a grande batalha!"
            else:
                return "Sistemas de combate inicializados. Protocolos táticos ativos."
        
        if self.game_phase == 'midgame' and self.move_count == 15:
            if self.values.honor > 0.6:
                return "A batalha atinge seu momento mais intenso!"
            else:
                return "Processamento tático em nível máximo. Executando manobras avançadas."
        
        if self.game_phase == 'endgame' and self.move_count == 30:
            if self.values.tradition > 0.6:
                return "O momento decisivo se aproxima. Que a honra prevaleça!"
            else:
                return "Fase final iniciada. Objetivos prioritários redefinidos."
        
        return None
