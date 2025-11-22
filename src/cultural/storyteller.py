"""
Gerador de histórias para xadrez.
"""

from typing import List, Optional, Dict
from ..core.board import Board, Color, Piece, PieceType
from ..core.game import GameState
from .narrative import CulturalContext, NarrativeStyle

class StoryTheme:
    """Temas para histórias."""
    
    EPIC_BATTLE = {
        'intro': "Uma batalha épica está prestes a começar...",
        'midgame': "A batalha se intensifica com cada movimento...",
        'endgame': "O momento decisivo se aproxima...",
        'victory': "A vitória é conquistada com maestria!",
        'draw': "Um empate honroso encerra esta batalha lendária."
    }
    
    POLITICAL_INTRIGUE = {
        'intro': "No grande salão do palácio, uma disputa pelo poder começa...",
        'midgame': "Alianças são formadas e traições são planejadas...",
        'endgame': "O destino do reino está em jogo...",
        'victory': "Um novo poder emerge vitorioso!",
        'draw': "Um acordo diplomático é alcançado."
    }
    
    MYSTICAL_JOURNEY = {
        'intro': "Uma jornada mística tem início em terras antigas...",
        'midgame': "Forças místicas guiam cada movimento...",
        'endgame': "O destino dos reinos místicos será decidido...",
        'victory': "A profecia se cumpre!",
        'draw': "O equilíbrio místico é preservado."
    }

class StoryGenerator:
    """Gera histórias dinâmicas baseadas no progresso do jogo."""
    
    def __init__(self, context: CulturalContext):
        self.context = context
        self.current_theme = StoryTheme.EPIC_BATTLE
        self.story_segments: List[str] = []
        self.piece_personalities: Dict[Piece, Dict[str, str]] = {}
        
    def _initialize_piece_personalities(self, board: Board):
        """Atribui personalidades às peças principais."""
        # Adaptação para o novo sistema de Board (baseado em dicionário/python-chess)
        if hasattr(board, 'pieces') and isinstance(board.pieces, dict):
            for pos, piece in board.pieces.items():
                if piece is not None and piece.type in [PieceType.KING, PieceType.QUEEN]:
                    personality = self._generate_personality(piece)
                    self.piece_personalities[piece] = personality
        else:
            # Fallback para sistema antigo (matriz)
            for row in range(8):
                for col in range(8):
                    piece = board.get_piece(row, col)
                    if piece is not None and piece.type in [PieceType.KING, PieceType.QUEEN]:
                        personality = self._generate_personality(piece)
                        self.piece_personalities[piece] = personality
                    
    def _generate_personality(self, piece: Piece) -> Dict[str, str]:
        """Gera uma personalidade para uma peça."""
        personalities = {
            PieceType.KING: {
                Color.WHITE: {
                    'name': 'Rei Alexandre',
                    'trait': 'sábio e justo',
                    'motivation': 'proteger seu reino'
                },
                Color.BLACK: {
                    'name': 'Rei Dario',
                    'trait': 'determinado e astuto',
                    'motivation': 'expandir seu império'
                }
            },
            PieceType.QUEEN: {
                Color.WHITE: {
                    'name': 'Rainha Helena',
                    'trait': 'poderosa e estrategista',
                    'motivation': 'garantir a vitória de seu povo'
                },
                Color.BLACK: {
                    'name': 'Rainha Artemísia',
                    'trait': 'feroz e brilhante',
                    'motivation': 'provar seu valor em batalha'
                }
            }
        }
        
        return personalities.get(piece.type, {}).get(piece.color, {})
        
    def generate_game_opening(self, board: Board) -> str:
        """Gera a narrativa de abertura do jogo."""
        self._initialize_piece_personalities(board)
        
        if self.context.style == NarrativeStyle.HISTORICAL:
            opening = (f"No ano de {self.context.era}, dois reinos poderosos "
                      "se encontram em um campo de batalha singular...")
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            opening = ("Os deuses observam atentamente enquanto dois destinos "
                      "se entrelaçam neste tabuleiro místico...")
        elif self.context.style == NarrativeStyle.DRAMATIC:
            opening = ("O ar está carregado de tensão enquanto os adversários "
                      "se preparam para um duelo épico...")
        elif self.context.style == NarrativeStyle.STRATEGIC:
            opening = ("Um embate estratégico está prestes a começar, onde cada "
                      "movimento pode mudar o curso da história...")
        else:  # EDUCATIONAL
            opening = ("Bem-vindos a uma jornada de aprendizado através do nobre "
                      "jogo de xadrez...")
            
        self.story_segments.append(opening)
        return opening
        
    def generate_midgame_narrative(self, 
                                 board: Board, 
                                 last_move: tuple,
                                 captured_piece: Optional[Piece]) -> str:
        """Gera narrativa para a fase média do jogo."""
        from_pos, to_pos = last_move
        moving_piece = board.get_piece(to_pos[0], to_pos[1])
        
        if not moving_piece:
            return ""
            
        # Gera narrativa baseada no contexto e estilo
        if self.context.style == NarrativeStyle.HISTORICAL:
            narrative = self._generate_historical_narrative(
                moving_piece, from_pos, to_pos, captured_piece)
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            narrative = self._generate_mythological_narrative(
                moving_piece, from_pos, to_pos, captured_piece)
        else:
            narrative = self._generate_default_narrative(
                moving_piece, from_pos, to_pos, captured_piece)
            
        self.story_segments.append(narrative)
        return narrative
        
    def _generate_historical_narrative(self,
                                     piece: Piece,
                                     from_pos: tuple,
                                     to_pos: tuple,
                                     captured_piece: Optional[Piece]) -> str:
        """Gera narrativa no estilo histórico."""
        personality = self.piece_personalities.get(piece, {})
        piece_name = personality.get('name', 'O comandante')
        
        narrative = f"{piece_name} avança suas forças"
        if captured_piece:
            narrative += f", conquistando uma posição estratégica do inimigo"
        else:
            narrative += f", fortalecendo sua posição no campo de batalha"
            
        return narrative
        
    def _generate_mythological_narrative(self,
                                       piece: Piece,
                                       from_pos: tuple,
                                       to_pos: tuple,
                                       captured_piece: Optional[Piece]) -> str:
        """Gera narrativa no estilo mitológico."""
        personality = self.piece_personalities.get(piece, {})
        piece_name = personality.get('name', 'O herói')
        
        narrative = f"{piece_name}, abençoado pelos deuses,"
        if captured_piece:
            narrative += f" derrota seu adversário em um duelo místico"
        else:
            narrative += f" move-se com graça divina pelo campo de batalha"
            
        return narrative
        
    def _generate_default_narrative(self,
                                  piece: Piece,
                                  from_pos: tuple,
                                  to_pos: tuple,
                                  captured_piece: Optional[Piece]) -> str:
        """Gera narrativa padrão."""
        piece_name = self.piece_personalities.get(piece, {}).get('name', 'A peça')
        
        narrative = f"{piece_name} realiza seu movimento"
        if captured_piece:
            narrative += f", eliminando uma peça adversária"
            
        return narrative
        
    def generate_endgame_narrative(self, board: Board, game_state: GameState) -> str:
        """Gera narrativa para o final do jogo."""
        if game_state == GameState.CHECKMATE:
            narrative = self._generate_victory_narrative(board)
        elif game_state == GameState.STALEMATE:
            narrative = self._generate_stalemate_narrative()
        elif game_state == GameState.DRAW:
            narrative = self._generate_draw_narrative()
        else:
            narrative = "A batalha continua..."
            
        self.story_segments.append(narrative)
        return narrative
        
    def _generate_victory_narrative(self, board: Board) -> str:
        """Gera narrativa de vitória."""
        if self.context.style == NarrativeStyle.HISTORICAL:
            return ("A batalha chega ao fim com uma vitória decisiva. "
                   "Os livros de história registrarão este dia.")
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            return ("Os deuses sorriram para o vencedor, cumprindo assim "
                   "as antigas profecias.")
        elif self.context.style == NarrativeStyle.DRAMATIC:
            return ("Em um movimento final brilhante, o destino da batalha "
                   "é selado com uma vitória memorável.")
        elif self.context.style == NarrativeStyle.STRATEGIC:
            return ("A superioridade estratégica se prova decisiva, "
                   "culminando em uma vitória bem calculada.")
        else:  # EDUCATIONAL
            return ("Uma vitória conquistada através da aplicação "
                   "magistral dos princípios do xadrez.")
                   
    def _generate_stalemate_narrative(self) -> str:
        """Gera narrativa de afogamento."""
        if self.context.style == NarrativeStyle.HISTORICAL:
            return ("O impasse tático resulta em um curioso empate, "
                   "onde nenhum lado pode avançar.")
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            return ("Os deuses, em sua sabedoria, decidem que nenhum "
                   "lado deve prevalecer nesta batalha.")
        else:
            return "A posição chega a um impasse, resultando em empate."
            
    def _generate_draw_narrative(self) -> str:
        """Gera narrativa de empate."""
        if self.context.style == NarrativeStyle.HISTORICAL:
            return ("Após uma batalha equilibrada, ambos os lados "
                   "concordam com um empate honroso.")
        elif self.context.style == NarrativeStyle.MYTHOLOGICAL:
            return ("O equilíbrio das forças místicas resulta em um "
                   "empate predestinado.")
        else:
            return "A partida termina em um empate justo."
            
    def get_complete_story(self) -> str:
        """Retorna a história completa do jogo."""
        return "\n\n".join(self.story_segments)
