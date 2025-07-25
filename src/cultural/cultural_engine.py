from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import random

@dataclass
class CulturalTheme:
    name: str
    description: str
    era: str
    piece_names: Dict[str, str]  # Nomes culturais para cada peça
    piece_descriptions: Dict[str, str]  # Descrições culturais para cada peça
    move_narratives: List[str]  # Templates para narrativas de movimentos
    special_events: List[str]  # Eventos especiais (xeque, captura, etc.)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CulturalTheme':
        return cls(
            name=data['name'],
            description=data['description'],
            era=data['era'],
            piece_names=data['piece_names'],
            piece_descriptions=data['piece_descriptions'],
            move_narratives=data['move_narratives'],
            special_events=data['special_events']
        )

class CulturalEngine:
    def __init__(self):
        # Carregar temas culturais
        self.themes: Dict[str, CulturalTheme] = self._load_themes()
        self.current_theme: Optional[CulturalTheme] = None
        self.narrative_state = {
            'tension': 0.0,  # 0 = calmo, 1 = muito tenso
            'momentum': 0.0,  # -1 = pretas dominando, 1 = brancas dominando
            'dramatic_moments': []  # Lista de momentos dramáticos no jogo
        }
    
    def _load_themes(self) -> Dict[str, CulturalTheme]:
        """Carrega os temas culturais dos arquivos de configuração"""
        themes = {}
        
        # Tema Medieval
        medieval = CulturalTheme(
            name="Medieval Europa",
            description="Um tema baseado na Europa Medieval, com cavaleiros, reis e castelos",
            era="Medieval",
            piece_names={
                'pawn': 'Camponês',
                'knight': 'Cavaleiro',
                'bishop': 'Bispo',
                'rook': 'Torre',
                'queen': 'Rainha',
                'king': 'Rei'
            },
            piece_descriptions={
                'pawn': 'Um humilde servo do reino, marchando com determinação',
                'knight': 'Um nobre cavaleiro montado em seu corcel de batalha',
                'bishop': 'Um sábio conselheiro espiritual da corte',
                'rook': 'Uma imponente torre de pedra, símbolo de força e proteção',
                'queen': 'A poderosa rainha, comandante suprema das forças do reino',
                'king': 'O majestoso rei, cuja proteção é vital para o reino'
            },
            move_narratives=[
                "O {piece} avança com determinação para {square}",
                "Com um movimento estratégico, {piece} ocupa {square}",
                "{piece} move-se cautelosamente para {square}",
                "Em uma demonstração de força, {piece} toma posição em {square}"
            ],
            special_events=[
                "O {attacker} captura o {defender} em uma batalha feroz!",
                "Xeque! O rei está sob ataque direto de {attacker}!",
                "O reino está em perigo! O rei precisa se proteger!",
                "Uma manobra brilhante coloca o {piece} em posição vantajosa!"
            ]
        )
        themes['medieval'] = medieval
        
        # Tema Futurista
        futuristic = CulturalTheme(
            name="Neo Tokyo 2050",
            description="Um cenário cyberpunk futurista com IA e tecnologia avançada",
            era="Futuro",
            piece_names={
                'pawn': 'Drone',
                'knight': 'Mecha',
                'bishop': 'Hacker',
                'rook': 'Fortaleza',
                'queen': 'IA Suprema',
                'king': 'Mainframe'
            },
            piece_descriptions={
                'pawn': 'Um drone de combate básico, mas eficiente',
                'knight': 'Um poderoso mecha com mobilidade única',
                'bishop': 'Um hacker expert em infiltração diagonal',
                'rook': 'Uma fortaleza móvel com poder de fogo linear',
                'queen': 'A IA mais avançada, capaz de qualquer operação',
                'king': 'O mainframe central, núcleo de toda a operação'
            },
            move_narratives=[
                "O {piece} executa protocolo de movimento para {square}",
                "Sistemas online: {piece} reposicionando para {square}",
                "{piece} calcula trajetória e avança para {square}",
                "Comando executado: {piece} assume controle de {square}"
            ],
            special_events=[
                "Download completo: {attacker} neutraliza {defender}!",
                "Alerta crítico! Mainframe sob ataque de {attacker}!",
                "Firewall comprometido! Sistema central em risco!",
                "Hack bem-sucedido: {piece} ganha acesso privilegiado!"
            ]
        )
        themes['futuristic'] = futuristic
        
        # Tema Místico
        mystic = CulturalTheme(
            name="Reino Místico",
            description="Um mundo de magia, criaturas místicas e poderes arcanos",
            era="Atemporal",
            piece_names={
                'pawn': 'Aprendiz',
                'knight': 'Guardião',
                'bishop': 'Mago',
                'rook': 'Golem',
                'queen': 'Arquimaga',
                'king': 'Grão-Mestre'
            },
            piece_descriptions={
                'pawn': 'Um jovem aprendiz de magia em treinamento',
                'knight': 'Um guardião místico montado em uma criatura mágica',
                'bishop': 'Um poderoso mago especialista em magias direcionais',
                'rook': 'Um imenso golem de pedra animado por magia antiga',
                'queen': 'A arquimaga suprema, mestre de todas as magias',
                'king': 'O grão-mestre da ordem mágica, fonte de poder místico'
            },
            move_narratives=[
                "O {piece} conjura um portal para {square}",
                "Com um gesto místico, {piece} teleporta para {square}",
                "{piece} canaliza energia mágica em direção a {square}",
                "Uma aura mística envolve {piece} ao mover para {square}"
            ],
            special_events=[
                "Em um duelo mágico, {attacker} domina {defender}!",
                "Perigo místico! O grão-mestre está sob ataque de {attacker}!",
                "A aura protetora falha! O grão-mestre precisa de proteção!",
                "O poder místico flui através de {piece}!"
            ]
        )
        themes['mystic'] = mystic
        
        return themes
    
    def select_theme(self, theme_name: str) -> bool:
        """Seleciona um tema cultural específico"""
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            return True
        return False
    
    def get_random_theme(self) -> CulturalTheme:
        """Seleciona um tema aleatório"""
        theme_name = random.choice(list(self.themes.keys()))
        self.current_theme = self.themes[theme_name]
        return self.current_theme
    
    def get_piece_name(self, piece_type: str) -> str:
        """Obtém o nome cultural de uma peça"""
        if not self.current_theme:
            self.get_random_theme()
        return self.current_theme.piece_names.get(piece_type, piece_type)
    
    def get_piece_description(self, piece_type: str) -> str:
        """Obtém a descrição cultural de uma peça"""
        if not self.current_theme:
            self.get_random_theme()
        return self.current_theme.piece_descriptions.get(piece_type, "")
    
    def generate_move_narrative(self, piece_type: str, target_square: str) -> str:
        """Gera uma narrativa para um movimento"""
        if not self.current_theme:
            self.get_random_theme()
            
        template = random.choice(self.current_theme.move_narratives)
        piece_name = self.get_piece_name(piece_type)
        
        return template.format(piece=piece_name, square=target_square)
    
    def generate_special_event(self, event_type: str, **kwargs) -> str:
        """Gera narrativa para eventos especiais (capturas, xeque, etc.)"""
        if not self.current_theme:
            self.get_random_theme()
            
        if event_type == 'capture':
            template = random.choice([e for e in self.current_theme.special_events 
                                    if '{attacker}' in e and '{defender}' in e])
            return template.format(
                attacker=self.get_piece_name(kwargs.get('attacker_type', '')),
                defender=self.get_piece_name(kwargs.get('defender_type', ''))
            )
        elif event_type == 'check':
            template = random.choice([e for e in self.current_theme.special_events 
                                    if 'Xeque' in e or 'perigo' in e.lower()])
            return template.format(attacker=self.get_piece_name(kwargs.get('attacker_type', '')))
        else:
            return random.choice(self.current_theme.special_events).format(
                piece=self.get_piece_name(kwargs.get('piece_type', ''))
            )
    
    def update_narrative_state(self, game_state: Dict) -> None:
        """Atualiza o estado narrativo baseado no estado do jogo"""
        # Análise de tensão
        self.narrative_state['tension'] = min(1.0, max(0.0, 
            self.narrative_state['tension'] + (
                0.2 if game_state.get('is_check', False) else
                0.1 if game_state.get('last_move_was_capture', False) else
                -0.1
            )
        ))
        
        # Análise de momentum
        piece_count = {'white': 0, 'black': 0}
        piece_value = {'white': 0, 'black': 0}
        
        for row in game_state.get('board', []):
            for piece in row:
                if piece:
                    piece_count[piece['color']] += 1
                    if piece['type'] in ['queen', 'rook', 'bishop', 'knight']:
                        piece_value[piece['color']] += 1
        
        total_value = piece_value['white'] + piece_value['black']
        if total_value > 0:
            self.narrative_state['momentum'] = (
                (piece_value['white'] - piece_value['black']) / total_value
            )
    
    def get_dramatic_moment(self) -> Optional[str]:
        """Gera um momento dramático baseado no estado narrativo"""
        if self.narrative_state['tension'] > 0.8:
            if abs(self.narrative_state['momentum']) > 0.6:
                side = "brancas" if self.narrative_state['momentum'] > 0 else "pretas"
                return f"A batalha atinge seu ápice! As {side} dominam o campo!"
            return "A tensão é palpável! Cada movimento pode ser decisivo!"
        
        if abs(self.narrative_state['momentum']) > 0.7:
            side = "brancas" if self.narrative_state['momentum'] > 0 else "pretas"
            return f"As {side} claramente têm a vantagem neste momento!"
            
        return None

    def save_state(self, filename: str) -> None:
        """Salva o estado cultural atual"""
        state = {
            'current_theme': self.current_theme.name if self.current_theme else None,
            'narrative_state': self.narrative_state
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
    
    def load_state(self, filename: str) -> None:
        """Carrega um estado cultural salvo"""
        with open(filename, 'r') as f:
            state = json.load(f)
            if state['current_theme']:
                self.select_theme(state['current_theme'])
            self.narrative_state = state['narrative_state']
